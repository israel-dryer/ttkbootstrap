"""Structural sync test for the generated styling partials (docs Workstream H).

Each ttk-styled family has an includable rST *partial*
(`docs/reference/api/_style/<family>.rst`) that a widget's API reference page
folds into its **Styling options** section. The partials carry live ttk
introspection (element options, layout, states) that varies by Tcl/Tk version
and OS -- byte-comparing them would make CI flake on a Tk point-release. So this
test is deliberately **structural**:

- every family the registry produces must have a committed partial;
- every committed partial must be ``.. include::``d by some API page, so a new
  family can't be generated and then left orphaned (unreachable) in the docs.

Content freshness is the author's documented offline regen step
(`python tools/generate_style_reference.py`).
"""
import importlib.util
import pathlib
import re


_REPO = pathlib.Path(__file__).resolve().parents[1]
_PARTIAL_DIR = _REPO / "docs" / "reference" / "api" / "_style"
_API_DIR = _REPO / "docs" / "reference" / "api"

_INCLUDE_RE = re.compile(r"\.\. include:: /reference/api/_style/([\w-]+)\.rst")


def _load_generator():
    path = _REPO / "tools" / "generate_style_reference.py"
    spec = importlib.util.spec_from_file_location("_style_ref_gen", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _included_families():
    families = set()
    for rst in _API_DIR.glob("*.rst"):
        families.update(_INCLUDE_RE.findall(rst.read_text(encoding="utf-8")))
    return families


def _secondary_includes():
    """Partials a page folds in *after* its first one, i.e. as a variant section.

    Derived from the `.. include::` order on each API page, which is what
    actually determines the heading level the partial needs.
    """
    nested = set()
    for rst in _API_DIR.glob("*.rst"):
        found = _INCLUDE_RE.findall(rst.read_text(encoding="utf-8"))
        nested.update(found[1:])
    return nested


def test_style_reference_families_nonempty():
    gen = _load_generator()
    families = gen.style_reference_families()
    assert families, "the builder registry should yield styled families"
    # registry and the `_FAMILIES` metadata must agree (raises otherwise)
    gen._check_families()


def test_every_family_has_a_committed_partial():
    gen = _load_generator()
    for family in gen.style_reference_families():
        partial = _PARTIAL_DIR / f"{family}.rst"
        assert partial.exists(), (
            f"missing styling partial {partial.name}; regenerate with "
            "`python tools/generate_style_reference.py`"
        )


def test_every_partial_is_included_by_an_api_page():
    # No orphan styling partials: each family's partial must be folded into some
    # widget's API reference page, or its hand-styling surface is unreachable.
    gen = _load_generator()
    included = _included_families()
    for family in gen.style_reference_families():
        assert family in included, (
            f"styling partial '{family}' is not `.. include::`d by any "
            "docs/reference/api/*.rst page; fold it into the relevant widget's "
            "Styling options section."
        )


def test_nested_partials_match_the_pages():
    # A partial included *after* another one on the same page renders as a
    # variant section underneath it, so its subsections must be a heading level
    # deeper -- otherwise they repeat the parent's headings at the same level and
    # read as duplicates. Keep the generator's set and the pages in step.
    gen = _load_generator()
    assert gen.NESTED_PARTIALS == _secondary_includes(), (
        "tools/generate_style_reference.py NESTED_PARTIALS disagrees with the "
        "`.. include::` order in docs/reference/api/. Update the set and "
        "regenerate with `python tools/generate_style_reference.py`."
    )


def test_nested_partials_use_a_deeper_heading_rule():
    # The mechanical consequence of the above: nested partials underline with
    # `^`, standalone ones with `~`.
    gen = _load_generator()
    for family in gen.style_reference_families():
        body = (_PARTIAL_DIR / f"{family}.rst").read_text(encoding="utf-8")
        rules = {line[0] for line in body.split("\n")
                 if line and set(line) in ({"~"}, {"^"})}
        expected = "^" if family in gen.NESTED_PARTIALS else "~"
        assert rules == {expected}, (
            f"styling partial '{family}' underlines with {sorted(rules)}; "
            f"expected only '{expected}'. Regenerate with "
            "`python tools/generate_style_reference.py`."
        )
