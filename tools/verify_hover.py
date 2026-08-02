#!/usr/bin/env python
"""Verify what an editor actually shows when you hover a widget constructor.

The type stub (`src/ttkbootstrap/__init__.pyi`) exists for one user-visible
reason: hovering `ttk.Button(` should list that widget's parameters, and
autocomplete should offer them (issue #1327). `tests/test_widget_stubs.py`
proves the stub is *in sync with the docs*, and a type checker proves the
signature *resolves* -- neither proves the tooltip has useful content in it.

That gap is not hypothetical. The first working version of the stub type-checked
perfectly and still showed the wrong tooltip: the docstring sat on the class, so
editors read `__init__` and fell back to `BootMixin.__init__`, whose text
describes `*args, **kwargs`. Only a hover request caught it.

So this asks a real language server for the real tooltip. It is a **manual
gate**, not a test: it needs `pyright` and `jedi`, which are developer tools
rather than runtime or CI dependencies.

    pip install pyright jedi
    python tools/verify_hover.py

Two engines are queried because they fail differently and neither is the
reporter's editor:

- **pyright** -- what VS Code / Pylance runs. Driven over LSP
  (`textDocument/hover`), so the output below is the tooltip markdown verbatim.
- **jedi** -- used by several other editors. Checked for the signature, the
  docstring, and that a partially typed `boot` completes to `bootstyle=`.

**PyCharm is not covered** and cannot be driven from a script; it reads the same
PEP 484 stub, but if a report mentions PyCharm specifically, click it there.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

# Deliberately mirrors how the docs tell people to write code, so the tooltips
# checked here are the ones a reader of the docs will actually summon.
_SAMPLE = '''import ttkbootstrap as tb

app = tb.App()
frame = tb.Frame(app, padding=10, bootstyle="info")
button = tb.Button(app, text="Click", bootstyle="success")
entry = tb.Entry(app, show="*")
text = tb.Text(app, wrap="word")
'''

# (label, line, column) of the class name to hover, both 0-indexed.
_TARGETS = [
    ("tb.Frame", 3, 11),
    ("tb.Button", 4, 12),
    ("tb.Entry", 5, 11),
    ("tb.Text", 6, 10),
]

# A tooltip that fell back to the mixin says this instead of the widget's own
# parameters -- the exact regression this script exists to catch.
_FALLBACK_MARKERS = (
    "Positional arguments forwarded to the wrapped",
    "Keyword arguments forwarded to the wrapped",
)


class _LanguageServer:
    """A minimal LSP client -- enough to open a file and ask for a hover."""

    def __init__(self, executable: Path):
        self._process = subprocess.Popen(
            [str(executable), "--stdio"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
        self._next_id = 1

    def request(self, method: str, params: dict):
        message_id = self._send(method, params)
        while True:
            message = self._read()
            if message is None:
                return None
            if message.get("id") == message_id and "result" in message:
                return message["result"]

    def notify(self, method: str, params: dict) -> None:
        self._send(method, params, notify=True)

    def close(self) -> None:
        self._process.terminate()

    def _send(self, method: str, params: dict, notify: bool = False):
        message = {"jsonrpc": "2.0", "method": method, "params": params}
        if not notify:
            message["id"] = self._next_id
            self._next_id += 1
        body = json.dumps(message).encode()
        self._process.stdin.write(b"Content-Length: %d\r\n\r\n%s" % (len(body), body))
        self._process.stdin.flush()
        return message.get("id")

    def _read(self):
        headers = {}
        while True:
            line = self._process.stdout.readline()
            if not line:
                return None
            line = line.strip()
            if not line:
                break
            key, _, value = line.decode().partition(": ")
            headers[key.lower()] = value
        return json.loads(self._process.stdout.read(int(headers["content-length"])))


def _pyright_hovers(sample: Path) -> dict[str, str]:
    executable = _find("pyright-langserver")
    server = _LanguageServer(executable)
    try:
        server.request("initialize", {
            "processId": None,
            "rootUri": sample.parent.as_uri(),
            "capabilities": {
                "textDocument": {"hover": {"contentFormat": ["markdown", "plaintext"]}}
            },
            "initializationOptions": {"python": {"pythonPath": sys.executable}},
        })
        server.notify("initialized", {})
        server.notify("textDocument/didOpen", {
            "textDocument": {
                "uri": sample.as_uri(), "languageId": "python",
                "version": 1, "text": _SAMPLE,
            }
        })
        hovers = {}
        for label, line, column in _TARGETS:
            result = server.request("textDocument/hover", {
                "textDocument": {"uri": sample.as_uri()},
                "position": {"line": line, "character": column},
            })
            hovers[label] = ((result or {}).get("contents") or {}).get("value", "")
        return hovers
    finally:
        server.close()


def _find(executable: str) -> Path:
    candidate = Path(sys.executable).parent / f"{executable}.exe"
    if candidate.exists():
        return candidate
    candidate = Path(sys.executable).parent / executable
    if candidate.exists():
        return candidate
    raise SystemExit(
        f"{executable} is not next to {sys.executable}. Install the developer "
        "tools this gate needs: pip install pyright jedi"
    )


def _check_pyright(hovers: dict[str, str]) -> list[str]:
    failures = []
    for label, hover in hovers.items():
        widget = label.split(".")[1]
        print(f"--- pyright hover: {label} " + "-" * (50 - len(label)))
        print(hover.strip() or "  *** EMPTY ***")
        print()
        if not hover.strip():
            failures.append(f"{label}: the hover is empty")
            continue
        if any(marker in hover for marker in _FALLBACK_MARKERS):
            failures.append(
                f"{label}: the tooltip fell back to BootMixin.__init__ -- the "
                "stub's __init__ is missing its docstring"
            )
        if f"class {widget}(" not in hover:
            failures.append(f"{label}: no constructor signature in the tooltip")
        if "Args:" not in hover:
            failures.append(f"{label}: no Args: block, so parameters are undescribed")
    return failures


def _check_jedi() -> list[str]:
    try:
        import jedi
    except ImportError:
        raise SystemExit("jedi is not installed: pip install pyright jedi")

    failures = []
    signatures = jedi.Script(
        code="import ttkbootstrap as tb\ntb.Frame(", path="probe.py"
    ).get_signatures(2, 9)
    parameters = [p.name for s in signatures for p in s.params]
    print(f"--- jedi signature: tb.Frame -> {len(parameters)} parameters")
    print(f"    {parameters}\n")
    if "bootstyle" not in parameters:
        failures.append("jedi: bootstyle is not in the resolved signature")
    if "padding" not in parameters:
        failures.append("jedi: padding is not in the resolved signature")

    partial = 'import ttkbootstrap as tb\napp = tb.App()\nf = tb.Frame(app, boot'
    completions = [
        c.name for c in
        jedi.Script(code=partial, path="probe.py").complete(3, len(partial.split("\n")[-1]))
    ]
    print(f"--- jedi completion: 'boot' -> {completions}\n")
    if not any(c.startswith("bootstyle") for c in completions):
        failures.append("jedi: 'boot' does not complete to bootstyle=")
    return failures


def main() -> None:
    print(f"stub: {_ROOT / 'src' / 'ttkbootstrap' / '__init__.pyi'}")
    print(f"python: {sys.executable}\n")

    with tempfile.TemporaryDirectory() as directory:
        sample = Path(directory) / "hover_sample.py"
        sample.write_text(_SAMPLE, encoding="utf-8")
        failures = _check_pyright(_pyright_hovers(sample))

    failures += _check_jedi()

    checks = len(_TARGETS) + 1
    if failures:
        print(f"[FAIL] {len(failures)} problem(s) across {checks} checks:")
        for failure in failures:
            print(f"  - {failure}")
        raise SystemExit(1)
    print(f"[PASS] {checks}/{checks} -- tooltips carry the widget's own parameters.")
    print("NOTE: PyCharm is not covered here; check it by hand for a PyCharm report.")


if __name__ == "__main__":
    main()
