"""Audit a built sdist + wheel before it is published.

``twine check`` validates *metadata*; it never opens the archives. Everything
that has actually gone wrong here is a contents problem instead:

* The vendored Bootstrap Icons font is package **data**. A wheel missing
  ``assets/icons/`` installs cleanly and then dies at the first icon render, so
  the failure lands on users rather than on the release.
* 2.0 shipped without the type stub, which silently disabled keyword checking
  in every editor until 2.1.1 put it back. A stub that is present in the repo
  but absent from the wheel looks identical from a checkout.
* ``dist/`` is gitignored and keeps whatever the last release built, so a glob
  can pick up a superseded version. Being explicit about *which* version is in
  the directory is the check that catches it.

Run it against a freshly built directory, optionally pinning the version the
release is supposed to be (in CI, the tag):

    python tools/check_dist.py dist
    python tools/check_dist.py dist --expect-version 2.2.2

Every check prints a PASS/FAIL line; the exit status is non-zero if any failed.
"""
import argparse
import re
import sys
import tarfile
import zipfile
from pathlib import Path

# Package data whose absence is invisible until runtime: the icon font and its
# glyph tables, the ttk element rasters the recolor pipeline draws from, and the
# typing marker plus the generated stub.
REQUIRED_IN_WHEEL = (
    "ttkbootstrap/assets/icons/bootstrap.ttf",
    "ttkbootstrap/assets/icons/glyphmap.json",
    "ttkbootstrap/assets/icons/icon_metrics.json",
    "ttkbootstrap/assets/elements/manifest.json",
    "ttkbootstrap/assets/elements/checkbox-checked.png",
    "ttkbootstrap/py.typed",
    "ttkbootstrap/__init__.pyi",
)

# The sdist is a build input, not a documentation bundle: docs/ and the
# development/ design notes stay out of it.
FORBIDDEN_IN_SDIST = ("docs/", "development/", "examples/", "gallery/")

REQUIRED_IN_SDIST = (
    "pyproject.toml",
    "LICENSE",
    "README.md",
    "src/ttkbootstrap/assets/icons/bootstrap.ttf",
    "src/ttkbootstrap/__init__.pyi",
)

_WHEEL_RE = re.compile(r"^ttkbootstrap-(?P<version>[^-]+)-py3-none-any\.whl$")
_SDIST_RE = re.compile(r"^ttkbootstrap-(?P<version>.+)\.tar\.gz$")

_failures = 0


def check(label, ok, detail=""):
    global _failures
    if not ok:
        _failures += 1
    print(f"{'PASS' if ok else 'FAIL'}  {label}{f' -- {detail}' if detail else ''}")
    return ok


def _one(dist, pattern, kind):
    """The single archive of `kind` in `dist`, with its version -- or (None, None)."""
    found = [(p, m) for p in sorted(dist.iterdir()) if (m := pattern.match(p.name))]
    if not check(f"exactly one {kind} in {dist}", len(found) == 1,
                 ", ".join(p.name for p, _ in found) or "none found"):
        return None, None
    path, match = found[0]
    return path, match.group("version")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist", type=Path, help="directory holding the built artifacts")
    parser.add_argument("--expect-version", help="the version this release is supposed to be")
    args = parser.parse_args(argv)

    if not args.dist.is_dir():
        print(f"FAIL  {args.dist} is not a directory")
        return 1

    wheel, wheel_version = _one(args.dist, _WHEEL_RE, "wheel")
    sdist, sdist_version = _one(args.dist, _SDIST_RE, "sdist")
    if wheel is None or sdist is None:
        return 1

    check("wheel and sdist carry the same version", wheel_version == sdist_version,
          f"wheel {wheel_version}, sdist {sdist_version}")
    if args.expect_version:
        check(f"version is {args.expect_version}", wheel_version == args.expect_version,
              f"built {wheel_version}")

    wheel_names = set(zipfile.ZipFile(wheel).namelist())
    for name in REQUIRED_IN_WHEEL:
        check(f"wheel contains {name}", name in wheel_names)

    with tarfile.open(sdist) as tar:
        # Every sdist path is prefixed with the ttkbootstrap-<version>/ root.
        sdist_names = {n.split("/", 1)[1] for n in tar.getnames() if "/" in n}
    for name in REQUIRED_IN_SDIST:
        check(f"sdist contains {name}", name in sdist_names)
    for prefix in FORBIDDEN_IN_SDIST:
        offenders = sorted(n for n in sdist_names if n.startswith(prefix))
        check(f"sdist excludes {prefix}", not offenders,
              f"e.g. {offenders[0]} ({len(offenders)} total)" if offenders else "")

    print()
    print(f"{'FAILED' if _failures else 'OK'}: {_failures} failed check(s)"
          if _failures else "OK: every check passed")
    return 1 if _failures else 0


if __name__ == "__main__":
    sys.exit(main())
