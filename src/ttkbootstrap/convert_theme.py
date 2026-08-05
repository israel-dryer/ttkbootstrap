"""Convert a ttkbootstrap 1.x theme file into a 2.x ``Theme(...).register()`` snippet.

Run it on a theme file saved by 1.x -- a ``user.py`` holding a ``USER_THEMES``
dict (what 1.x ttkcreator exported), or a JSON file in the
``Style.load_user_themes`` format -- and it prints Python you paste into your
own app::

    python -m ttkbootstrap.convert_theme mythemes.json
    python -m ttkbootstrap.convert_theme user.py -o brand.py

The five accent anchors, the optional secondary accent, and the theme's
background/foreground carry over. `border`, `inputbg`, `inputfg`, `selectbg`,
`selectfg`, and `active` are dropped: 2.x derives them from the anchors. A 1.x
theme declares one mode, so the generated family declares that mode and leaves
the opposite one commented out.
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


def load_legacy_themes(path):
    """Read a 1.x theme file and return its ``{name: spec}`` mapping.

    Parameters:

        path (str or Path):
            A ``.json`` file in the ``Style.load_user_themes`` format, or a
            ``.py`` file defining a ``USER_THEMES`` dict.

    Returns:

        dict:
            Each 1.x spec, keyed by theme name.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        themes = _themes_from_python(text, path)
    else:
        themes = _themes_from_json(text)
    if not themes:
        raise ValueError(f"{path}: no themes found.")
    return themes


def _themes_from_json(text):
    """Return ``{name: spec}`` from a ``load_user_themes``-format JSON file."""
    data = json.loads(text)
    entries = data.get("themes", data) if isinstance(data, dict) else data
    if isinstance(entries, dict):
        return dict(entries)
    themes = {}
    for entry in entries:
        themes.update(entry)
    return themes


def _themes_from_python(text, path):
    """Return ``{name: spec}`` from a 1.x ``user.py``-style theme store."""
    tree = ast.parse(text, filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if "USER_THEMES" in names or "STANDARD_THEMES" in names:
            return dict(ast.literal_eval(node.value))
    raise ValueError(f"{path}: no USER_THEMES assignment found.")


def _mode(name, spec):
    """Return the theme's ``light``/``dark`` mode."""
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

    primary = f'primary="{colors["primary"]}"'
    if colors.get("secondary"):
        primary += f', secondary="{colors["secondary"]}"'
    lines = [
        "ttk.Theme(",
        f'    name="{name}",',
        f"    {primary},",
        f'    success="{colors["success"]}", info="{colors["info"]}",',
        f'    warning="{colors["warning"]}", danger="{colors["danger"]}",',
        f'    {mode}=dict(background="{colors["bg"]}", '
        f'foreground="{colors["fg"]}"),',
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
        f"anchors below.",
        width=75,
    )
    header = [
        f"# Converted from {Path(path).name} by "
        f"python -m ttkbootstrap.convert_theme.",
        "#",
        *(f"# {line}" for line in note),
        "# Call register() once, after creating your App.",
        "",
        "import ttkbootstrap as ttk",
        "",
        "",
    ]
    blocks = [theme_snippet(name, spec) for name, spec in themes.items()]
    return "\n".join(header) + "\n\n".join(blocks) + "\n"


def main(argv=None):
    """Run the command-line converter."""
    parser = argparse.ArgumentParser(
        prog="python -m ttkbootstrap.convert_theme",
        description="Convert a ttkbootstrap 1.x theme file into a 2.x "
                    "Theme(...).register() snippet.",
    )
    parser.add_argument(
        "file", help="a 1.x theme file (.json, or a .py USER_THEMES store)"
    )
    parser.add_argument(
        "-o", "--output", help="write to this file instead of standard output"
    )
    args = parser.parse_args(argv)

    try:
        source = convert(args.file)
    except (OSError, ValueError, json.JSONDecodeError, SyntaxError) as error:
        parser.exit(2, f"{parser.prog}: {error}\n")

    if args.output:
        Path(args.output).write_text(source, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(source)
    return 0


if __name__ == "__main__":
    sys.exit(main())
