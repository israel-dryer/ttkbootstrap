"""Convert a ttkbootstrap 1.x theme file into a 2.x ``Theme(...).register()`` snippet.

Run it on a theme file saved by 1.x -- a ``user.py`` holding a ``USER_THEMES``
dict, a ``.py`` holding the ``ThemeDefinition(...)`` call ttkcreator's *Export
theme definition* wrote, or a JSON file in the ``Style.load_user_themes``
format -- and it prints Python you paste into your own app::

    ttkb convert-theme mythemes.json
    ttkb convert-theme user.py -o brand.py

The module stays runnable as ``python -m ttkbootstrap.convert_theme``, which is
what to use when the scripts directory is not on PATH.

The five accent anchors, the optional secondary accent, and the theme's
background/foreground carry over. `border`, `inputbg`, `inputfg`, `selectbg`,
`selectfg`, and `active` are dropped: 2.x derives them from the anchors. The
`light` and `dark` accents are dropped too: 2.x derives that pair from the
`neutral` ramp, which you set with `Theme(neutral=...)`. A 1.x theme declares
one mode, so the generated family declares that mode and leaves the opposite
one commented out.
"""
import argparse
import ast
import json
import sys
import textwrap
from pathlib import Path

#: 1.x color keys that carry over to a `Theme` anchor of the same name.
_ACCENT_KEYS = ("primary", "success", "info", "warning", "danger")

#: 1.x color keys the 2.x engine derives rather than reads.
_DERIVED_KEYS = ("border", "inputbg", "inputfg", "selectbg", "selectfg", "active")

#: 1.x accent keys 2.x derives from the `neutral` ramp instead.
_NEUTRAL_KEYS = ("light", "dark")


def _literal(value):
    """Render a value as a Python string literal, escaping what it contains.

    JSON string escapes are a subset of Python's, so `json.dumps` gives a
    double-quoted literal that survives a quote or a backslash in a theme name
    or a color -- the generated file is source we tell people to run.
    """
    return json.dumps(str(value))


def load_legacy_themes(path):
    """Read a 1.x theme file and return its ``{name: spec}`` mapping.

    Parameters:

        path (str or Path):
            A ``.json`` file in the ``Style.load_user_themes`` format, or a
            ``.py`` file defining a ``USER_THEMES`` dict or a
            ``ThemeDefinition(...)`` call.

    Returns:

        dict:
            Each 1.x spec, keyed by theme name.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        themes = _themes_from_python(text, path)
    else:
        themes = _themes_from_json(text, path)
    if not themes:
        raise ValueError(f"{path}: no themes found.")
    return themes


def _themes_from_json(text, path):
    """Return ``{name: spec}`` from a ``load_user_themes``-format JSON file."""
    data = json.loads(text)
    entries = data.get("themes", data) if isinstance(data, dict) else data
    if isinstance(entries, dict):
        return dict(entries)
    if not isinstance(entries, list):
        raise ValueError(
            f"{path}: expected a theme mapping or a list of them, got "
            f"{type(entries).__name__}."
        )
    themes = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError(
                f"{path}: expected each entry to be a theme mapping, got "
                f"{type(entry).__name__}."
            )
        themes.update(entry)
    return themes


def _themes_from_python(text, path):
    """Return ``{name: spec}`` from a 1.x ``user.py`` store or a ttkcreator
    ``ThemeDefinition`` export."""
    tree = ast.parse(text, filename=str(path))
    themes = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if "USER_THEMES" in names or "STANDARD_THEMES" in names:
            store = ast.literal_eval(node.value)
            if not isinstance(store, dict):
                raise ValueError(
                    f"{path}: expected USER_THEMES to be a mapping of themes, "
                    f"got {type(store).__name__}."
                )
            return dict(store)
        call = _theme_definition_call(node.value)
        if call is not None:
            themes.update(_spec_from_definition(call, path))
    if themes:
        return themes
    raise ValueError(
        f"{path}: found neither a USER_THEMES assignment nor a "
        "ThemeDefinition(...) call."
    )


def _theme_definition_call(node):
    """Return the node when it is a ``ThemeDefinition(...)`` call, else None."""
    if not isinstance(node, ast.Call):
        return None
    func = node.func
    name = (
        func.attr if isinstance(func, ast.Attribute)
        else getattr(func, "id", None)
    )
    return node if name == "ThemeDefinition" else None


def _spec_from_definition(call, path):
    """Return ``{name: spec}`` from ttkcreator's *Export theme definition* file.

    That export writes ``ThemeDefinition(name=..., themetype=...,
    colors={...})``. 1.x took those three positionally as ``(name, colors,
    themetype)``, with `themetype` defaulting to light, so both spellings are
    read.
    """
    args = dict(zip(("name", "colors", "themetype"), call.args))
    args.update({kw.arg: kw.value for kw in call.keywords if kw.arg})
    try:
        name = ast.literal_eval(args["name"])
        colors = ast.literal_eval(args["colors"])
    except KeyError as error:
        raise ValueError(
            f"{path}: ThemeDefinition(...) is missing {error.args[0]}."
        ) from None
    mode = "light"
    if "themetype" in args:
        mode = ast.literal_eval(args["themetype"])
    return {name: {"type": mode, "colors": colors}}


def _mode(name, spec):
    """Return the theme's ``light``/``dark`` mode."""
    if not isinstance(spec, dict):
        raise ValueError(
            f"theme {name!r}: expected a spec mapping, got "
            f"{type(spec).__name__}."
        )
    mode = spec.get("mode") or spec.get("type")
    if mode not in ("light", "dark"):
        raise ValueError(
            f"theme {name!r}: expected a 'mode' (or 1.x 'type') of 'light' or "
            f"'dark', got {mode!r}."
        )
    return mode


def _colors(name, spec):
    """Return the theme's color mapping, checking the keys conversion needs."""
    colors = spec.get("colors")
    if not isinstance(colors, dict):
        raise ValueError(f"theme {name!r}: missing a 'colors' mapping.")
    missing = [k for k in _ACCENT_KEYS + ("bg", "fg") if not colors.get(k)]
    if missing:
        raise ValueError(
            f"theme {name!r}: missing color(s) {', '.join(missing)}."
        )
    return colors


def theme_snippet(name, spec):
    """Render one 1.x theme spec as a ``ttk.Theme(...).register()`` call.

    Parameters:

        name (str):
            The theme name; becomes the family name, so the call registers
            ``<name>-light`` or ``<name>-dark``.

        spec (dict):
            A 1.x spec — ``{'type': 'light'|'dark', 'colors': {...}}``.

    Returns:

        str:
            The rendered call, without a trailing newline.
    """
    mode = _mode(name, spec)
    colors = _colors(name, spec)
    other = "dark" if mode == "light" else "light"

    primary = f"primary={_literal(colors['primary'])}"
    if colors.get("secondary"):
        primary += f", secondary={_literal(colors['secondary'])}"
    lines = [
        "ttk.Theme(",
        f"    name={_literal(name)},",
        f"    {primary},",
        f"    success={_literal(colors['success'])}, "
        f"info={_literal(colors['info'])},",
        f"    warning={_literal(colors['warning'])}, "
        f"danger={_literal(colors['danger'])},",
        f"    {mode}=dict(background={_literal(colors['bg'])}, "
        f"foreground={_literal(colors['fg'])}),",
        f"    # {other}=dict(background=..., foreground=...),"
        f"  # 1.x theme was {mode}-only",
        ").register()",
    ]
    return "\n".join(lines)


def convert(path):
    """Convert a 1.x theme file into a runnable Python module.

    Parameters:

        path (str or Path):
            The 1.x ``.json`` or ``.py`` theme file.

    Returns:

        str:
            Python source registering every theme in the file.
    """
    themes = load_legacy_themes(path)
    dropped = ", ".join(_DERIVED_KEYS[:-1]) + f", and {_DERIVED_KEYS[-1]}"
    note = textwrap.wrap(
        f"The 1.x {dropped} values are dropped; 2.x derives them from the "
        f"anchors below. So are the {' and '.join(_NEUTRAL_KEYS)} accents; 2.x "
        f"derives that pair from the neutral ramp, which Theme(neutral=...) "
        f"sets.",
        width=75,
    )
    # A registered theme is selectable by name, and the name is `<family>-<mode>`
    # rather than the 1.x name -- so show it. Naming the first theme names the
    # one they just converted.
    first, first_spec = next(iter(themes.items()))
    registered = f"{first}-{_mode(first, first_spec)}"
    header = [
        f"# Converted from {Path(path).name} by ttkb convert-theme.",
        "#",
        *(f"# {line}" for line in note),
        "#",
        "# Import this module, then select the theme by name:",
        f"#     app = ttk.App(theme={_literal(registered)})",
        "",
        "import ttkbootstrap as ttk",
        "",
        "",
    ]
    blocks = [theme_snippet(name, spec) for name, spec in themes.items()]
    return "\n".join(header) + "\n\n".join(blocks) + "\n"


#: One-line summary, shared by this module's parser and the `ttkb` subcommand.
DESCRIPTION = (
    "Convert a ttkbootstrap 1.x theme file into a 2.x Theme(...).register() "
    "snippet."
)


def add_arguments(parser):
    """Add the converter's arguments to `parser`.

    Shared with the `ttkb convert-theme` subcommand so the two spellings cannot
    drift apart.
    """
    parser.add_argument(
        "file",
        help="a 1.x theme file (.json, or a .py USER_THEMES / ThemeDefinition "
             "store)",
    )
    parser.add_argument(
        "-o", "--output", help="write to this file instead of standard output"
    )
    return parser


def run(args, parser):
    """Convert the file named by `args`, reporting failures through `parser`."""
    try:
        source = convert(args.file)
        if args.output:
            Path(args.output).write_text(source, encoding="utf-8")
    except (OSError, ValueError, SyntaxError) as error:
        parser.exit(2, f"{parser.prog}: {error}\n")

    if args.output:
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(source)
    return 0


def main(argv=None):
    """Run the command-line converter."""
    parser = argparse.ArgumentParser(
        prog="python -m ttkbootstrap.convert_theme", description=DESCRIPTION
    )
    add_arguments(parser)
    return run(parser.parse_args(argv), parser)


if __name__ == "__main__":
    sys.exit(main())
