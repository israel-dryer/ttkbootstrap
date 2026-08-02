"""Sync tests for the generated type stubs (`src/ttkbootstrap/__init__.pyi`).

The stub restores what an IDE shows for a widget constructor (issue #1327). It
is generated from the per-widget reference pages by
`python tools/generate_widget_stubs.py`; these tests keep the three things it
depends on from drifting apart:

- the committed stub matches what the generator produces *now*, so editing an
  `Options` table without regenerating fails here rather than shipping a stale
  signature;
- every public name still resolves through the stub -- a stub file *replaces*
  the module for type checkers, so a new export that is not re-exported would
  silently vanish from `ttkbootstrap`;
- the reference tables still cover the live Tk option set. That one is a
  docs-completeness audit as much as a stub test: because the stub declares
  exactly the documented options and no `**kwargs`, an option Tk grew that the
  reference never documented would become a false positive in a user's type
  checker. Better to fail here.
"""
import importlib.util
import inspect
import pathlib
import re
import subprocess
import sys

import pytest

import ttkbootstrap as ttk


_REPO = pathlib.Path(__file__).resolve().parents[1]
_STUB = _REPO / "src" / "ttkbootstrap" / "__init__.pyi"
_REGENERATE = "regenerate with `python tools/generate_widget_stubs.py`"


def _load_generator():
    path = _REPO / "tools" / "generate_widget_stubs.py"
    spec = importlib.util.spec_from_file_location("_widget_stub_gen", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def generator():
    return _load_generator()


def test_stub_exists():
    assert _STUB.exists(), f"the type stub is missing; {_REGENERATE}"


def test_stub_matches_the_generator(tmp_path):
    """The committed stub is what the generator produces from the docs.

    Run in a subprocess, which is both how a developer runs the tool and the
    only way to read *unpatched* signatures: `enable_global_api()` wraps
    `__init__` on the tkinter classes, and another test in this suite enables
    it, so an in-process regeneration would see the wrapper's `(*args,
    **kwargs)` instead of each widget's real parameters.
    """
    out = tmp_path / "regenerated.pyi"
    result = subprocess.run(
        [sys.executable, str(_REPO / "tools" / "generate_widget_stubs.py"),
         "--output", str(out)],
        capture_output=True, text=True, cwd=_REPO,
    )
    assert result.returncode == 0, f"the generator failed:\n{result.stderr}"
    assert out.read_text(encoding="utf-8") == _STUB.read_text(encoding="utf-8"), (
        f"{_STUB.name} is out of date with the widget reference pages; {_REGENERATE}"
    )


def test_stub_is_valid_python(generator):
    import ast

    ast.parse(_STUB.read_text(encoding="utf-8"), type_comments=False)


def test_every_public_name_is_reachable_through_the_stub():
    """A stub replaces the module, so an omitted name disappears from the API."""
    stub = _STUB.read_text(encoding="utf-8")
    missing = [
        name for name in ttk.__all__
        if f" as {name}\n" not in stub
        and f" as {name}," not in stub
        and f"\nclass {name}(" not in stub
        and f"\n{name} = " not in stub
    ]
    assert not missing, (
        f"these public names are not reachable through the stub: {missing}; {_REGENERATE}"
    )


def test_constructor_docstrings_live_on_init_not_only_the_class():
    """The `Args:` block must be on `__init__`, which is what a hover reads.

    With the docstring only on the class, editors fall back to the runtime
    `BootMixin.__init__` and the tooltip describes `*args, **kwargs` -- the
    original bug wearing a different hat. It type-checks perfectly either way,
    so nothing else in this file would notice.
    """
    stub = _STUB.read_text(encoding="utf-8")
    undocumented = [
        name for name in _stubbed_classes()
        if not re.search(
            rf"^class {name}\(.*?\n    def __init__\(.*?\n    \) -> None:\n        \"\"\"",
            stub, re.S | re.M,
        )
    ]
    assert not undocumented, (
        f"these stubbed widgets have no docstring on __init__, so an editor will "
        f"show the mixin's generic text instead: {undocumented}; {_REGENERATE}"
    )


def test_class_summaries_come_from_the_reference_pages(generator):
    """A tooltip must say what the widget *is*, not just that it is themed.

    The runtime class docstrings are one-line stubs ("ttk Frame with
    ttkbootstrap theming (accepts `bootstyle=`)"), which is what a hover showed
    before the summary was taken from each reference page's opening prose.
    """
    stub = _STUB.read_text(encoding="utf-8")
    boilerplate = []
    for name in _stubbed_classes():
        found = re.search(
            rf'^class {name}\((?:Boot|AutoStyle)Mixin, [^)]+\):\n    """(.*?)"""',
            stub, re.M | re.S,
        )
        page_summary = generator._summary(name.lower(), "")
        if found is None or not page_summary:
            boilerplate.append(name)
            continue
        if " ".join(found.group(1).split()) != page_summary:
            boilerplate.append(name)
    assert not boilerplate, (
        "these stubbed widgets show a placeholder summary instead of their "
        f"reference page's description: {boilerplate}; {_REGENERATE}"
    )


def test_required_constructor_parameters_have_no_default():
    """`OptionMenu(master, variable)` needs both; the stub must say so.

    A default on a required parameter makes `ttk.OptionMenu()` type-check and
    then raise `TypeError` at runtime -- the stub being *more* permissive than
    the library, which is the one direction a stub must never be.
    """
    stub = _STUB.read_text(encoding="utf-8")
    signature = re.search(
        r"^class OptionMenu\(.*?\n    \) -> None:", stub, re.S | re.M
    ).group(0)
    for parameter in ("master", "variable"):
        assert re.search(rf"^        {parameter}: [^=\n]+,$", signature, re.M), (
            f"OptionMenu.{parameter} is required at runtime but the stub gives it "
            f"a default; {_REGENERATE}"
        )


def _stubbed_classes():
    """The widget classes the committed stub declares."""
    stub = _STUB.read_text(encoding="utf-8")
    return re.findall(r"^class (\w+)\((?:Boot|AutoStyle)Mixin, ", stub, re.M)


def test_every_generic_widget_is_stubbed():
    """Adding a widget must not silently leave it without a signature."""
    stubbed = set(_stubbed_classes())
    generic = set()
    for name in ttk.__all__:
        obj = getattr(ttk, name)
        if not isinstance(obj, type) or obj.__name__ != name:
            continue
        if not issubclass(obj, (ttk.BootMixin, ttk.AutoStyleMixin)):
            continue
        if obj in (ttk.BootMixin, ttk.AutoStyleMixin):
            continue
        if "__init__" not in vars(obj) or _is_generic(obj):
            generic.add(name)

    assert generic <= stubbed, (
        f"these widgets have no stubbed signature: {sorted(generic - stubbed)}; "
        f"{_REGENERATE}"
    )


def _is_generic(cls):
    """Whether a class's own `__init__` takes nothing but `*args, **kwargs`."""
    parameters = list(inspect.signature(cls.__init__).parameters.values())[1:]
    return all(p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD) for p in parameters)


@pytest.mark.parametrize("name", _stubbed_classes())
def test_reference_tables_cover_the_live_tk_options(name, root, generator):
    """Every real Tk option is documented, or deliberately excluded.

    The stub declares no `**kwargs`, so an undocumented-but-real option would be
    rejected by a type checker on code that works. The exclusions are the ones
    the generator adds back itself, plus Tcl's `from` (documented under
    tkinter's `from_` spelling).

    This doubles as a docs-completeness audit: a Tk version or platform that
    grows an option the reference never documented fails here, which is where
    it can be fixed, rather than in a user's type checker.
    """
    if name == "Tk":
        pytest.skip(
            "constructing a second root would mis-bind the Style singleton "
            "(see tests/conftest.py); the root's options are covered by tkframe"
        )
    options = generator._options(name.lower())
    if not options:
        pytest.skip(f"no Options table on docs/reference/api/{name.lower()}.rst")

    allowed = (
        set(generator._CONSTRUCTOR_ONLY)
        | set(generator._TTK_EXTRAS)
        | set(generator._ENTRY_FAMILY_COMPAT)
        | {"class", "from"}
    )
    cls = getattr(ttk, name)
    widget = cls(root, ttk.StringVar(), "a") if name == "OptionMenu" else cls(root)

    gap = sorted(set(widget.configure().keys()) - generator._spellings(options) - allowed)
    assert not gap, (
        f"{name}: these live Tk options are absent from "
        f"docs/reference/api/{name.lower()}.rst, so the stub would reject "
        f"working code: {gap}. Document them, then {_REGENERATE}."
    )
