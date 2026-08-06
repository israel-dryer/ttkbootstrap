#!/usr/bin/env python
"""Generate `src/ttkbootstrap/__init__.pyi` from the authored widget reference.

The concrete widget classes in `ttkbootstrap/__init__.py` are one-liners
(`class Button(BootMixin, ttk.Button)`) whose constructor resolves through the
MRO to `BootMixin.__init__(self, *args, **kwargs)`. That is correct at runtime
and useless to an IDE: hovering `ttk.Button(...)` shows a generic signature and
a one-line docstring instead of the widget's parameters (issue #1327).

1.x shipped a hand-written `__init__.pyi` for the same reason. Rather than
hand-maintain 450 lines of parallel declarations -- which drift -- this tool
derives the stub from two sources that are already the truth:

- **Which classes need stubbing** is discovered, not listed: every class in
  `ttkbootstrap.__all__` that mixes in `BootMixin`/`AutoStyleMixin` and whose
  constructor is generic (`*args, **kwargs`). Add a widget and it is picked up.
- **What options each one takes** comes from the authored per-widget reference
  pages (`docs/reference/api/<widget>.rst`), whose `Options` list-tables carry
  the option name, type and description -- already reviewed, and already the
  documented surface (the #1244 audit settled what belongs there).

Everything else in `__all__` is re-exported, because a stub file *replaces* the
module for type checkers: a partial stub would hide `Style`, `App`,
`Messagebox` and the shipped widgets. Those all carry real annotated
signatures already, so a re-export is all they need.

Run it after adding a widget or editing an `Options` table:

    python tools/generate_widget_stubs.py

`tests/test_widget_stubs.py` fails until the committed stub matches, so the
stub can never silently drift from the reference -- and it also asserts the
reference tables still cover the live Tk option set, so a Tk version that adds
an option is a loud test failure here rather than a false positive in a user's
type checker.
"""
from __future__ import annotations

import argparse
import inspect
import keyword
import re
import sys
from pathlib import Path
from typing import NamedTuple

_ROOT = Path(__file__).resolve().parent.parent
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

_API_DOCS = _ROOT / "docs" / "reference" / "api"
_STUB = _SRC / "ttkbootstrap" / "__init__.pyi"

# The type strings the reference tables use, mapped to annotations. Closed on
# purpose: an unrecognized type is an error, not a silent `Any`, so a new
# spelling in the docs has to be considered here first.
#
# The unions are deliberately wider than the docs' shorthand, because Tk accepts
# more than one spelling of most values and a stub that rejects working code is
# worse than one that misses a wrong value. Each was probed:
#
# - a font is a tuple as often as a string -- `font=("Helvetica", 12)` is the
#   idiom the typography guide teaches;
# - `values=`/`columns=` take a tuple as readily as a list, and the library's
#   own screenshot scenes pass tuples;
# - an image can be a tkinter image, a Pillow `ImageTk.PhotoImage` (Pillow is
#   ttkbootstrap's one runtime dependency), or a Tk image *name* like
#   `"::tk::icons::warning"`.
_IMAGE = "str | PhotoImage | BitmapImage | PilImage"
_TYPES = {
    "str": "str",
    "int": "int",
    "bool": "bool",
    "float": "float",
    "list": "list[Any] | tuple[Any, ...]",
    "tuple": "tuple[Any, ...]",
    "any": "Any",
    "callable": "Callable[..., Any]",
    "Variable": "Variable",
    "PhotoImage": _IMAGE,
    "Menu": "Menu",
    "Widget": "Misc",
    "int | tuple": "int | tuple[Any, ...]",
    "int | float": "int | float",
    "int | str": "int | str",
    "str | tuple": "str | tuple[Any, ...]",
    "str | Font": "str | Font | tuple[Any, ...]",
    "datetime | date": "datetime | date",
    "datetime | date | None": "datetime | date | None",
}

# Per-option overrides where the page's type is a simplification. `takefocus`
# is documented `bool`, but Tk's domain is "" / 0 / 1 / a script name -- and ""
# is both the default and what `cget` returns, so `takefocus=""` is working code
# a plain `bool` would reject.
_OPTION_ANNOTATIONS = {
    "takefocus": "bool | str",
}

# Widgets whose constructor filters keywords instead of forwarding them to Tcl,
# so the reference page's option list overstates what it accepts. `configure`
# still takes the full set -- only construction is narrower.
#
# `ttk.OptionMenu.__init__` pops exactly these four and then
# `raise TclError('unknown option -%s')` for anything left, so the page's
# menubutton options (`text`, `width`, `padding`, `textvariable`, ...) crash at
# construction. Probed, and visible in tkinter's own source.
_CONSTRUCTOR_KEYWORDS = {
    "OptionMenu": {"style", "direction", "name", "command"},
}

class _Option(NamedTuple):
    """One row of a reference page's Options table."""

    name: str
    annotation: str
    description: str
    aliases: tuple[str, ...] = ()

    @property
    def constructor_only(self) -> bool:
        """Whether this option can only be set when the widget is created.

        The reference pages mark these "Constructor only." -- distinct from the
        "Constructor keyword." that labels ttkbootstrap's own additions, which
        `configure` does accept. Verified against runtime: `autostyle` raises
        `unknown option`, and `class`/`container`/`screen` raise "can't modify
        ... after widget is created".
        """
        return self.description.startswith("Constructor only.")


# `bootstyle`/`icon`/`autostyle` and friends are ttkbootstrap's own keywords:
# the mixin consumes them before delegating to the tk/ttk constructor, so they
# are accepted even by the root window, whose constructor takes no `**kw`.
_MIXIN_KEYWORDS = {"bootstyle", "icon", "icon_size", "icon_only", "autostyle"}

# Parameters that work but are deliberately absent from the reference, so a
# strict stub does not reject working code. They get no docstring entry -- the
# reference is what documents the surface. (Tk's `bd`/`bg`/`fg` abbreviations
# are *not* here: the reference documents them inline on the option they
# abbreviate, so they are parsed rather than listed.)
#
# `name` is constructor-only and universal. `style` is the raw ttk escape hatch
# that `bootstyle` fronts, and `class_` a real Tcl option on ttk widgets -- on
# classic tk widgets only Frame/Toplevel extract it, and the reference pages that
# document `class` are exactly those, so it is not added for the rest (probed:
# `Text(class_=...)` raises `unknown option "-class"`).
# `background` is the entry-family compat option, a verified-deliberate
# exclusion in the #1244 reference audit.
_CONSTRUCTOR_ONLY = {"name": "str"}
_TTK_EXTRAS = {"style": "str", "class_": "str"}
_ENTRY_FAMILY_COMPAT = {"background": "str"}


def _accepted(name: str, base, documented: set[str]) -> tuple[dict, dict]:
    """Return the (constructor, configure) extras for one widget.

    Derived in one place so the two signatures cannot drift apart.
    """
    shared: dict[str, str] = {}
    if base.__module__ == "tkinter.ttk":
        shared.update(_TTK_EXTRAS)
    if name in ("Entry", "Combobox", "Spinbox"):
        shared.update(_ENTRY_FAMILY_COMPAT)

    constructor = {**_CONSTRUCTOR_ONLY, **shared}
    return (
        {k: v for k, v in constructor.items() if k not in documented},
        {k: v for k, v in shared.items() if k not in documented},
    )

# The reference tables describe options, not the parameters a widget's
# constructor takes positionally. Those are read off the live tk/ttk base
# signature (below), and annotated/described from this table -- tkinter's own
# stubs are not importable at generation time, and there are only a handful.
_POSITIONAL = {
    "master": ("Misc | None", "The parent widget."),
    "variable": ("Variable | None", "The variable holding the selected value."),
    "default": ("str | None", "The value to show before a choice is made."),
    "values": ("str", "The choices offered in the dropdown."),
    "screenName": ("str | None", "The X display to open the window on."),
    "baseName": ("str | None", "The base for the profile file name."),
    "className": ("str", "The widget class of the root window."),
    "useTk": ("bool", "Whether to initialize the Tk subsystem."),
    "sync": ("bool", "Whether to execute X server commands synchronously."),
    "use": ("str | None", "The window id to embed this interpreter into."),
}

# Positional parameters a caller never passes: `cnf` is tkinter's legacy
# options dict, superseded by keyword arguments, and `widget` is ttk.Entry's
# internal subclassing hook (Combobox/Spinbox pass the Tcl command name through
# it) -- absent from ttk's own documented options.
_LEGACY_POSITIONAL = {"cnf", "widget"}


class _Positional(NamedTuple):
    """One positional parameter of a widget's live tk/ttk constructor."""

    name: str
    annotation: str
    description: str
    is_varargs: bool
    required: bool


def _positional(base) -> list[_Positional]:
    """Read a widget's positional parameters off its live tk/ttk base.

    This is what keeps `Tk` (`screenName`, `baseName`, ...) and `OptionMenu`
    (`variable`, `default`, `*values`) correct without hand-listing their
    signatures -- including which are *required*: `OptionMenu` needs `master`
    and `variable`, and a stub that defaulted them would let `OptionMenu()`
    type-check and then raise `TypeError`.
    """
    parameters = list(inspect.signature(base.__init__).parameters.values())[1:]
    out = []
    for parameter in parameters:
        if parameter.name in _LEGACY_POSITIONAL or parameter.kind is parameter.VAR_KEYWORD:
            continue
        if parameter.kind not in (parameter.POSITIONAL_OR_KEYWORD, parameter.VAR_POSITIONAL):
            continue
        known = _POSITIONAL.get(parameter.name)
        if known is None:
            raise SystemExit(
                f"{base.__name__}.__init__ takes {parameter.name!r} positionally; "
                f"add it to _POSITIONAL in {Path(__file__).name} with an "
                "annotation and a description."
            )
        annotation, description = known
        is_varargs = parameter.kind is parameter.VAR_POSITIONAL
        out.append(_Positional(
            parameter.name, annotation, description, is_varargs,
            required=not is_varargs and parameter.default is parameter.empty,
        ))
    return out

_HEADER = '''"""Type stubs for ttkbootstrap's public API.

GENERATED by `tools/generate_widget_stubs.py` from the widget reference pages
under `docs/reference/api/`. Do not edit by hand -- run the generator instead;
`tests/test_widget_stubs.py` enforces that this file matches.

The concrete widget classes below get an explicit constructor so editors and
type checkers can see each widget's options. At runtime they are the one-line
subclasses in `__init__.py`, whose shared mixin constructor is generic.
"""
from __future__ import annotations

from datetime import date, datetime
from tkinter import BitmapImage, Misc, PhotoImage, Variable
from tkinter.font import Font

# Pillow is ttkbootstrap's one runtime dependency, so its image type is always
# importable and an `image=` option legitimately accepts it.
from PIL.ImageTk import PhotoImage as PilImage
from typing import Any, Callable

from ttkbootstrap.style import AutoStyleMixin as AutoStyleMixin, BootMixin as BootMixin

# Assigned in `__init__.py` rather than imported, so `_reexports` -- which
# sources every name from an import statement -- cannot reach it.
__version__: str
'''


def _flatten(text: str) -> str:
    """Render a reST table cell as one line of plain prose for a docstring."""
    # Cross-references carry no weight in a tooltip; keep the visible label.
    text = re.sub(r":ref:`([^<`]+?)\s*<[^>]+>`", r"\1", text)
    text = re.sub(r":doc:`([^<`]+?)\s*<[^>]+>`", r"\1", text)
    text = re.sub(r":[a-z:]+:`([^`]+)`", r"\1", text)
    text = text.replace("**", "")
    text = re.sub(r"``([^`]+)``", r"\1", text)
    return _docstring_safe(" ".join(text.split()))


def _docstring_safe(text: str) -> str:
    """Reject text that would break the triple-quoted docstring it lands in.

    Neither case exists in the reference today. Checked anyway because the
    failure without it is a `SyntaxError` in a *generated* file, which is a
    confusing place to debug a docs edit from.
    """
    if '"""' in text or text.endswith("\\"):
        raise SystemExit(
            f"the text {text[:60]!r}... cannot go in a docstring (it contains "
            'a triple quote or ends in a backslash). Reword it in '
            "docs/reference/api/."
        )
    return text


def _parameter(option: str) -> str:
    """Return the Python spelling of a Tk option name.

    A few Tk options collide with Python keywords; tkinter spells those with a
    trailing underscore (`class_`, `from_`). Anything else that collides is an
    error rather than a guess, so a new one gets looked at.
    """
    if not keyword.iskeyword(option):
        return option
    if option in ("class", "from", "in"):
        return f"{option}_"
    raise SystemExit(
        f"option {option!r} is a Python keyword with no established tkinter "
        f"spelling; add one to _parameter() in {Path(__file__).name}."
    )


# The reference pages close their opening paragraph with a sentence about the
# page itself ("This page is the complete reference for its options..."). Useful
# on the page, meaningless in a tooltip, so it is cut.
_PAGE_META = re.compile(r"\s*This page is\b.*$", re.S)


def _summary(page: str, fallback: str) -> str:
    """The widget's description, taken from its reference page's opening prose.

    The runtime class docstrings are one-line stubs ("ttk Frame with
    ttkbootstrap theming"), which tells a reader nothing about what the widget
    *is*. The reference pages open with authored prose that does, so a tooltip
    gets that instead. Falls back to the runtime docstring for a class whose
    page has no lead paragraph.
    """
    path = _API_DOCS / f"{page}.rst"
    if not path.exists():
        return fallback
    lead = re.search(
        r"^[A-Za-z][^\n]*\n=+\n\n(.*?)\n\n",
        path.read_text(encoding="utf-8"), re.S | re.M,
    )
    if not lead:
        return fallback
    return _PAGE_META.sub("", _flatten(lead.group(1))).strip() or fallback


def _options(page: str) -> list[tuple[str, str, str]]:
    """Parse a reference page's `Options` list-table.

    Returns (option, type, description) in the order the page lists them, so
    the generated signature reads the way the documentation does (`bootstyle`
    first).
    """
    path = _API_DOCS / f"{page}.rst"
    if not path.exists():
        return []
    body = path.read_text(encoding="utf-8")
    # `\Z` matters: without it a page whose Options table is the *last* section
    # parses as zero options, and the stub would then declare that widget with no
    # keywords at all -- every one of them a type error, and nothing would fail,
    # since the sync test compares against the same empty output.
    section = re.search(
        r"^Options\n-+\n(.*?)(?=\n[A-Za-z][^\n]*\n-{3,}\n|\Z)", body, re.S | re.M
    )
    if not section:
        return []
    # The option cell is the name, optionally followed by Tk's abbreviation in
    # parentheses -- ``background`` (``bg``). Both spellings are real options.
    rows = re.findall(
        r"^   \* - ``([a-z_0-9]+)``([^\n]*)\n     - ``([^`]+)``\n     - (.*?)(?=\n   \* - |\Z)",
        section.group(1),
        re.S | re.M,
    )
    if len(rows) != len(re.findall(r"^   \* - ``[a-z_0-9]+``", section.group(1), re.M)):
        raise SystemExit(
            f"{path.name}: the Options table has rows this parser cannot read; "
            "every row must be name / type / description."
        )
    parsed = []
    for name, trailer, type_string, description in rows:
        annotation = _TYPES.get(type_string.strip())
        if annotation is None:
            raise SystemExit(
                f"{path.name}: option {name!r} has unrecognized type "
                f"{type_string.strip()!r}. Add it to _TYPES in "
                f"{Path(__file__).name} (and pick the annotation deliberately)."
            )
        aliases = re.findall(r"``([a-z_0-9]+)``", trailer)
        parameter = _parameter(name)
        parsed.append(
            _Option(parameter, _OPTION_ANNOTATIONS.get(parameter, annotation),
                    _flatten(description), tuple(_parameter(a) for a in aliases))
        )
    return parsed


def stub_targets():
    """Return the exported classes whose constructor an IDE cannot read.

    Discovered rather than listed: a `BootMixin`/`AutoStyleMixin` subclass whose
    `__init__` takes only `*args, **kwargs` has nothing widget-specific for an
    editor to show. The mixins themselves are excluded -- their generic
    constructor is the point.
    """
    import ttkbootstrap as tb
    from ttkbootstrap.style import AutoStyleMixin, BootMixin

    targets, aliases = {}, {}
    for name in tb.__all__:
        obj = getattr(tb, name)
        if not inspect.isclass(obj) or obj in (BootMixin, AutoStyleMixin):
            continue
        if not issubclass(obj, (BootMixin, AutoStyleMixin)):
            continue
        parameters = list(inspect.signature(obj.__init__).parameters.values())[1:]
        if any(p.kind is not p.VAR_POSITIONAL and p.kind is not p.VAR_KEYWORD
               for p in parameters):
            continue  # a real signature of its own; nothing to restore
        if obj.__name__ != name:
            aliases[name] = obj.__name__  # e.g. LabelFrame = Labelframe
            continue
        mixin = "BootMixin" if issubclass(obj, BootMixin) else "AutoStyleMixin"
        base = next(
            c for c in obj.__mro__
            if c.__module__ in ("tkinter", "tkinter.ttk") and c is not object
        )
        targets[name] = _Target(mixin, base, obj.__doc__ or "", obj.__module__)
    return targets, aliases


class _Target(NamedTuple):
    """A widget class the stub re-declares."""

    mixin: str
    base: type
    """The tk/ttk class -- where the positional parameters come from."""
    runtime_docstring: str
    module: str
    """Where the class is actually defined."""

    @property
    def bases(self) -> str:
        """The base list to declare the stubbed class with.

        A class defined in `__init__.py` has no other source, so the stub
        rebuilds it from the mixin and the tk/ttk class. A class defined
        *elsewhere* has real members of its own that would be erased by that:
        `ttkbootstrap.menu.Menu` carries the five macOS application-menu methods
        (#1174), and re-declaring it as `(AutoStyleMixin, tkinter.Menu)` makes
        them unreachable to a type checker. Subclassing the real class keeps
        them and still lets the stub state the constructor.
        """
        if self.module == "ttkbootstrap":
            return f"{self.mixin}, {_base_alias(self.base)}"
        return f"_{self.module.rsplit('.', 1)[-1].capitalize()}{self.base.__name__}"


def _base_alias(base: type) -> str:
    return f"_{base.__module__.split('.')[-1]}{base.__name__}"


def _signature(name: str, options, base, summary: str) -> list[str]:
    """Build the `__init__` lines for one widget, docstring included.

    The docstring is rendered here, from the same `described` list the signature
    is built from, so the parameters documented and the parameters accepted
    cannot disagree.
    """
    positional = _positional(base)
    documented = _constructor_options(name, base, options)

    lines = ["    def __init__(", "        self,"]
    described = []
    for parameter in positional:
        if parameter.is_varargs:
            lines.append(f"        *{parameter.name}: {parameter.annotation},")
            described.append((f"*{parameter.name}", parameter.description))
            continue
        # A required parameter gets no default, so omitting it is an error in an
        # editor rather than a `TypeError` at runtime.
        default = "" if parameter.required else " = ..."
        lines.append(f"        {parameter.name}: {parameter.annotation}{default},")
        described.append((parameter.name, parameter.description))
    if not any(p.is_varargs for p in positional):
        lines.append("        *,")

    for option in documented:
        lines.append(f"        {option.name}: {option.annotation} = ...,")
        for alias in option.aliases:
            lines.append(f"        {alias}: {option.annotation} = ...,")
        label = option.name + (f" ({', '.join(option.aliases)})" if option.aliases else "")
        described.append((label, option.description))

    extras, _ = _accepted(name, base, _spellings(documented))
    if not _accepts_options(base):
        extras = {}
    allowed = _CONSTRUCTOR_KEYWORDS.get(name)
    if allowed is not None:
        extras = {k: v for k, v in extras.items() if k in allowed}
    if extras:
        lines.append("        # Accepted spellings outside the documented surface.")
        for option, annotation in sorted(extras.items()):
            lines.append(f"        {option}: {annotation} = ...,")

    # The docstring goes on `__init__`, not just the class: an editor showing a
    # constructor call reads it from there, and if the stub leaves it out the
    # editor falls back to the runtime `BootMixin.__init__` -- which describes
    # `*args, **kwargs` and tells the reader nothing about the widget. Verified
    # against pyright's `textDocument/hover` response.
    lines.append("    ) -> None:")
    lines += _args_docstring(summary, described)
    return lines


def _spellings(options) -> set[str]:
    """Every parameter name a set of options contributes, aliases included."""
    return {o.name for o in options} | {a for o in options for a in o.aliases}


def _accepts_options(base) -> bool:
    """Whether a widget's constructor takes option keywords at all.

    Every tk/ttk widget forwards `**kw` to Tcl -- except the root window, whose
    constructor is `Tk.__init__(screenName, baseName, ...)` with no `**kw` at
    all. Passing it a surface option is a `TypeError` (verified), so the root's
    documented options belong to `configure` only.
    """
    return any(
        p.kind is p.VAR_KEYWORD
        for p in inspect.signature(base.__init__).parameters.values()
    )


def _constructor_options(name, base, options):
    """Return the documented options a constructor accepts as keywords."""
    # The mixin pops its own keywords before delegating, so those always work.
    allowed = _CONSTRUCTOR_KEYWORDS.get(name)
    if allowed is not None:
        return [o for o in options if o.name in allowed | _MIXIN_KEYWORDS]
    if _accepts_options(base):
        return options
    return [o for o in options if o.name in _MIXIN_KEYWORDS]


def _docstring(summary: str) -> list[str]:
    """Render the class docstring -- the one-line summary from the runtime class."""
    return ['    """' + _docstring_safe(" ".join(summary.split())) + '"""']


def _args_docstring(summary: str, described) -> list[str]:
    """Render `__init__`'s docstring: the summary plus an Args: block.

    `described` comes from `_signature`, so the parameters documented here and
    the parameters accepted there cannot disagree.
    """
    lines = ['        """' + " ".join(summary.split()).rstrip()]
    if described:
        lines += ["", "        Args:"]
        # One line per parameter, however long. An editor soft-wraps a hover
        # tooltip, but it renders a hard line break as a break -- wrapping here
        # chops every description into ragged fragments. (Confirmed by reading
        # pyright's hover markdown both ways.)
        for parameter, description in described:
            lines.append(f"            {parameter}: {description}")
    lines.append('        """')
    return lines


def _reexports(stubbed: set[str]) -> list[str]:
    """Re-export every other public name, mirroring `__init__.py`'s own imports.

    A stub replaces the module for type checkers, so anything omitted here
    would simply vanish from `ttkbootstrap`. The source of each name is taken
    from the runtime module's import statements rather than from the object's
    `__module__`: that keeps the stub pointing at the same public paths the
    package itself uses (`ttkbootstrap.dialogs`, not `dialogs.message`), and it
    preserves renames such as `families as font_families`.
    """
    import ast

    import ttkbootstrap as tb

    tree = ast.parse((_SRC / "ttkbootstrap" / "__init__.py").read_text(encoding="utf-8"))
    origin: dict[str, tuple[str, str]] = {}
    # Only module-level imports. `ast.walk` would also reach the function-local
    # ones -- `OptionMenu.__init__` imports `Bootstyle` from the implementation
    # module `style.bootstyle` -- and a nested hit landing last would re-export a
    # public name through an internal path.
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                origin[alias.asname or alias.name] = (node.module, alias.name)

    exported = [n for n in tb.__all__ if n not in stubbed]
    missing = [n for n in exported if n not in origin]
    if missing:
        raise SystemExit(
            f"no import statement in __init__.py provides {missing!r}; the stub "
            "cannot re-export a name it cannot source."
        )

    by_module: dict[str, list[tuple[str, str]]] = {}
    for name in exported:
        module, original = origin[name]
        by_module.setdefault(module, []).append((original, name))

    lines = []
    for module in sorted(by_module):
        pairs = sorted(by_module[module], key=lambda p: p[1])
        joined = ", ".join(f"{o} as {n}" for o, n in pairs)
        statement = f"from {module} import {joined}"
        if len(statement) <= 88:
            lines.append(statement)
        else:
            lines.append(f"from {module} import (")
            lines += [f"    {o} as {n}," for o, n in pairs]
            lines.append(")")
    return lines


def render() -> str:
    targets, aliases = stub_targets()
    lines = [_HEADER]

    imports = set()
    for name, target in targets.items():
        if target.module == "ttkbootstrap":
            imports.add((target.base.__module__, target.base.__name__,
                         _base_alias(target.base)))
        else:
            # Subclass the real implementation, so its own members survive.
            imports.add((target.module, name, target.bases))
    for module, symbol, alias in sorted(imports):
        lines.append(f"from {module} import {symbol} as {alias}")
    lines.append("")
    lines += _reexports(set(targets) | set(aliases))
    lines.append("")

    for name, target in targets.items():
        page = name.lower()
        options = _options(page)
        if not options and (_API_DOCS / f"{page}.rst").exists():
            raise SystemExit(
                f"{page}.rst exists but no options were parsed from it, so {name} "
                "would be stubbed with no keywords at all -- every one of them a "
                "type error. Check that its Options table is a name/type/"
                "description list-table."
            )
        summary = _summary(page, target.runtime_docstring)
        lines.append("")
        lines.append(f"class {name}({target.bases}):")
        lines += _docstring(summary)
        lines += _signature(name, options, target.base, summary)
        lines += _configure(options, target.base, name)

    for alias, target in aliases.items():
        lines += ["", f"{alias} = {target}"]

    return "\n".join(lines) + "\n"


def _configure(options, base, name: str) -> list[str]:
    """Type `configure`/`config` with the options settable after creation."""
    if not any(not o.constructor_only for o in options):
        return []
    lines = ["", "    def configure(", "        self,", "        cnf: Any = ...,", "        *,"]
    # ttkbootstrap's own keywords are settable here too: `configure(bootstyle=)`
    # restyles and `configure(icon=)` mints a new icon style (both verified).
    # Creation-time options are not, so the reference's "Constructor only."
    # marker drops them.
    settable = [o for o in options if not o.constructor_only]
    for option in settable:
        lines.append(f"        {option.name}: {option.annotation} = ...,")
        for alias in option.aliases:
            lines.append(f"        {alias}: {option.annotation} = ...,")
    _, extras = _accepted(name, base, _spellings(options))
    for option, annotation in sorted(extras.items()):
        lines.append(f"        {option}: {annotation} = ...,")
    lines.append("    ) -> Any: ...")
    lines.append("    config = configure")
    return lines


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--output",
        type=Path,
        default=_STUB,
        help="where to write the stub (default: the committed path). The sync "
             "test points this at a temporary file to compare without writing.",
    )
    arguments = parser.parse_args(argv)

    arguments.output.write_text(render(), encoding="utf-8")
    targets, aliases = stub_targets()
    print(f"wrote {arguments.output}")
    print(f"  {len(targets)} widget classes stubbed, {len(aliases)} aliased")


if __name__ == "__main__":
    main()