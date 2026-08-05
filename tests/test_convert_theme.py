"""Tests for the 1.x -> 2.x theme converter (`ttkbootstrap.convert_theme`)."""
import json

import pytest

import ttkbootstrap as ttk
from ttkbootstrap import convert_theme

LEGACY_COLORS = {
    "primary": "#6a5acd",
    "secondary": "#6c757d",
    "success": "#02b875",
    "info": "#17a2b8",
    "warning": "#f0ad4e",
    "danger": "#d9534f",
    "light": "#ADB5BD",
    "dark": "#2b2b2b",
    "bg": "#1c1c1c",
    "fg": "#e9ecef",
    "selectbg": "#555555",
    "selectfg": "#ffffff",
    "border": "#333333",
    "inputfg": "#e9ecef",
    "inputbg": "#2b2b2b",
    "active": "#3a3a3a",
}


def legacy_spec(mode="dark", **overrides):
    """A 1.x theme spec, optionally with colors removed or replaced."""
    colors = dict(LEGACY_COLORS)
    colors.update(overrides)
    return {"type": mode, "colors": colors}


def write_user_py(tmp_path, themes, name="user.py"):
    """Write the exact file 1.x ttkcreator produced: ``USER_THEMES = <json>``."""
    path = tmp_path / name
    path.write_text(
        "USER_THEMES = " + json.dumps(themes, indent=4), encoding="utf-8"
    )
    return path


def write_json(tmp_path, themes, name="themes.json"):
    """Write a file in the ``Style.load_user_themes`` format."""
    path = tmp_path / name
    payload = {"themes": [{n: spec} for n, spec in themes.items()]}
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_converts_the_1x_ttkcreator_export(tmp_path):
    """A ``USER_THEMES`` .py — what 1.x exported — converts to a Theme call."""
    path = write_user_py(tmp_path, {"midnight": legacy_spec("dark")})
    source = convert_theme.convert(path)

    assert 'name="midnight"' in source
    assert 'primary="#6a5acd"' in source
    assert 'secondary="#6c757d"' in source
    assert 'dark=dict(background="#1c1c1c", foreground="#e9ecef")' in source
    assert source.rstrip().endswith(").register()")


def test_converts_the_load_user_themes_json(tmp_path):
    """The hand-written JSON format converts to the same anchors."""
    path = write_json(tmp_path, {"midnight": legacy_spec("dark")})
    source = convert_theme.convert(path)

    assert 'name="midnight"' in source
    assert 'primary="#6a5acd"' in source
    assert 'dark=dict(background="#1c1c1c", foreground="#e9ecef")' in source


def test_the_absent_mode_is_commented_not_invented(tmp_path):
    """A 1.x theme has one mode; the other is left for the user to fill in."""
    path = write_user_py(tmp_path, {"daylight": legacy_spec("light")})
    source = convert_theme.convert(path)

    assert 'light=dict(background="#1c1c1c"' in source
    assert "# dark=dict(background=..., foreground=...)" in source


def test_engine_derived_colors_are_not_emitted(tmp_path):
    """2.x derives these from the anchors, so carrying them over would lie."""
    path = write_user_py(tmp_path, {"midnight": legacy_spec()})
    source = convert_theme.convert(path)

    for key in convert_theme._DERIVED_KEYS:
        assert f"{key}=" not in source
    # the dropped values themselves must not appear either
    assert "#555555" not in source     # selectbg
    assert "#333333" not in source     # border


def test_a_theme_without_a_secondary_omits_the_token(tmp_path):
    """`secondary` is optional on `Theme`; it derives from the neutral ramp."""
    spec = legacy_spec()
    del spec["colors"]["secondary"]
    path = write_user_py(tmp_path, {"midnight": spec})
    source = convert_theme.convert(path)

    assert "secondary=" not in source
    assert 'primary="#6a5acd",' in source


def test_every_theme_in_the_file_converts_under_one_import(tmp_path):
    path = write_user_py(
        tmp_path,
        {"midnight": legacy_spec("dark"), "daylight": legacy_spec("light")},
    )
    source = convert_theme.convert(path)

    assert source.count("import ttkbootstrap as ttk") == 1
    assert source.count(").register()") == 2
    assert 'name="midnight"' in source and 'name="daylight"' in source


def test_a_missing_color_names_the_theme_and_the_key(tmp_path):
    spec = legacy_spec()
    del spec["colors"]["warning"]
    path = write_user_py(tmp_path, {"midnight": spec})

    with pytest.raises(ValueError, match="midnight.*warning"):
        convert_theme.convert(path)


def test_a_missing_mode_is_loud(tmp_path):
    path = write_user_py(tmp_path, {"midnight": {"colors": LEGACY_COLORS}})

    with pytest.raises(ValueError, match="midnight"):
        convert_theme.convert(path)


def test_a_py_file_without_user_themes_is_loud(tmp_path):
    path = tmp_path / "notthemes.py"
    path.write_text("COLORS = {}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="USER_THEMES"):
        convert_theme.convert(path)


def test_cli_writes_the_requested_file(tmp_path):
    source_file = write_user_py(tmp_path, {"midnight": legacy_spec()})
    out = tmp_path / "brand.py"

    assert convert_theme.main([str(source_file), "-o", str(out)]) == 0
    assert 'name="midnight"' in out.read_text(encoding="utf-8")


def test_cli_prints_to_stdout(tmp_path, capsys):
    source_file = write_user_py(tmp_path, {"midnight": legacy_spec()})

    convert_theme.main([str(source_file)])

    assert 'name="midnight"' in capsys.readouterr().out


def test_cli_exits_with_an_error_on_a_bad_file(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        convert_theme.main([str(bad)])
    assert excinfo.value.code == 2


def test_the_converted_snippet_registers_and_renders(root, tmp_path):
    """The end of the pipe: the emitted Python runs and themes real widgets."""
    path = write_user_py(tmp_path, {"convertedtheme": legacy_spec("dark")})
    source = convert_theme.convert(path)

    exec(compile(source, "converted.py", "exec"), {})

    style = root.style
    assert "convertedtheme-dark" in style.theme_names()

    style.theme_use("convertedtheme-dark")
    assert style.theme_mode == "dark"

    # the 2.x engine derives the plumbing the 1.x file no longer supplies
    assert style.colors.border and style.colors.inputbg
    ttk.Button(root, text="ok", bootstyle="primary").pack()
    ttk.Entry(root).pack()
    root.update_idletasks()