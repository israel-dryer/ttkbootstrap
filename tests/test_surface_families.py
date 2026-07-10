"""Surface-color family rollout tests (2.0 surface-color, PR 3).

Extends the `@<surface>` bootstyle token to the indicator + label families
(checkbutton, radiobutton, toggle, label), and covers the `_SURFACE_FAMILIES`
graceful-degrade net (a listed family whose recipe does not emit surface_prefix
falls back to the plain style, not a bare-clam unregistered name).
"""
import ttkbootstrap as ttk
from ttkbootstrap.style import Style
from ttkbootstrap.style.builders_ttk import StyleBuilderTTK


def _lookup(app, style_name, option):
    return app.tk.call("ttk::style", "lookup", style_name, f"-{option}")


# --- default (surfaceless) names unchanged -------------------------------- #

def test_family_default_names_unchanged(root):
    assert ttk.Label(root).cget("style") == "TLabel"
    assert ttk.Checkbutton(root).cget("style") == "TCheckbutton"
    assert ttk.Radiobutton(root).cget("style") == "TRadiobutton"
    assert ttk.Checkbutton(root, bootstyle="toggle").cget("style") == "Toggle"
    assert (
        ttk.Checkbutton(root, bootstyle="round-toggle").cget("style")
        == "Round.Toggle"
    )


# --- label ---------------------------------------------------------------- #

def test_label_tracks_surface(root):
    b = StyleBuilderTTK(build=False)
    lbl = ttk.Label(root, bootstyle="@card")
    assert lbl.cget("style") == "@card.TLabel"
    assert _lookup(root, lbl.cget("style"), "background") == b.card_surface()
    # near-bg card keeps the soft theme fg
    assert _lookup(root, lbl.cget("style"), "foreground") == str(b.colors.fg)


def test_label_on_accent_surface_flips_fg(root):
    b = StyleBuilderTTK(build=False)
    style = Style.get_instance()
    lbl = ttk.Label(root, bootstyle="@primary")
    assert lbl.cget("style") == "@primary.TLabel"
    assert _lookup(root, lbl.cget("style"), "background") == style.colors.primary
    assert _lookup(root, lbl.cget("style"), "foreground") == b.on_color(
        style.colors.primary
    )


def test_colored_label_keeps_accent_text_on_surface(root):
    """A colored label on a surface: accent text, surface background."""
    style = Style.get_instance()
    lbl = ttk.Label(root, bootstyle="@card info")
    assert lbl.cget("style") == "@card.info.TLabel"
    assert _lookup(root, lbl.cget("style"), "foreground") == style.colors.info


# --- checkbutton / radiobutton -------------------------------------------- #

def test_checkbutton_on_surface(root):
    b = StyleBuilderTTK(build=False)
    cb = ttk.Checkbutton(root, bootstyle="@primary")
    assert cb.cget("style") == "@primary.TCheckbutton"
    # label text reads against the accent surface
    assert _lookup(root, cb.cget("style"), "foreground") == b.on_color(
        b.colors.primary
    )


def test_radiobutton_on_surface_builds(root):
    b = StyleBuilderTTK(build=False)
    rb = ttk.Radiobutton(root, bootstyle="@card")
    assert rb.cget("style") == "@card.TRadiobutton"
    assert _lookup(root, rb.cget("style"), "foreground") == str(b.colors.fg)


# --- toggle --------------------------------------------------------------- #

def test_toggle_tracks_surface(root):
    style = Style.get_instance()
    tg = ttk.Checkbutton(root, bootstyle="@primary toggle")
    assert tg.cget("style") == "@primary.Toggle"
    assert _lookup(root, tg.cget("style"), "background") == style.colors.primary


def test_square_toggle_tracks_surface(root):
    style = Style.get_instance()
    tg = ttk.Checkbutton(root, bootstyle="@primary square-toggle")
    assert tg.cget("style") == "@primary.Square.Toggle"
    # square toggle sets background via the state map -> query the mapped state
    mapped = root.tk.call(
        "ttk::style", "lookup", tg.cget("style"), "-background", "selected"
    )
    assert mapped == style.colors.primary


# --- theme reactivity ----------------------------------------------------- #

def test_surfaced_family_is_theme_reactive(root):
    style = Style.get_instance()
    style.theme_use("bootstrap-light")
    tg = ttk.Checkbutton(root, bootstyle="@primary toggle")
    light = _lookup(root, tg.cget("style"), "background")
    style.theme_use("bootstrap-dark")
    dark = _lookup(root, tg.cget("style"), "background")
    assert tg.cget("style") == "@primary.Toggle"
    assert light != dark


# --- graceful-degrade net ------------------------------------------------- #

def test_surface_degrades_when_family_recipe_unwired(root, monkeypatch):
    """A family listed in the gate whose recipe ignores surface must degrade to
    the plain style (not an unregistered '@' name -> bare clam)."""
    import ttkbootstrap.style.bootstyle as bs
    style = Style.get_instance()
    monkeypatch.setattr(
        bs, "_SURFACE_FAMILIES", frozenset(bs._SURFACE_FAMILIES | {"entry"})
    )
    e = ttk.Entry(root, bootstyle="@card")
    assert "@" not in e.cget("style")
    assert style.style_exists_in_theme(e.cget("style"))
