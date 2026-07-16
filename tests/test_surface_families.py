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
    # the widget background paints the surface itself (regression: the builder
    # resolved the surface for text colors but never configured background=)
    assert _lookup(root, cb.cget("style"), "background") == str(b.colors.primary)


def test_radiobutton_on_surface_builds(root):
    b = StyleBuilderTTK(build=False)
    rb = ttk.Radiobutton(root, bootstyle="@card")
    assert rb.cget("style") == "@card.TRadiobutton"
    assert _lookup(root, rb.cget("style"), "foreground") == str(b.colors.fg)
    assert _lookup(root, rb.cget("style"), "background") == b.card_surface()


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


# --- bar families (scale / progressbar / scrollbar) ----------------------- #

def test_scale_tracks_surface(root):
    style = Style.get_instance()
    sc = ttk.Scale(root, bootstyle="@primary")
    assert sc.cget("style") == "@primary.Horizontal.TScale"
    assert style.style_exists_in_theme(sc.cget("style"))


def test_progressbar_trough_tracks_surface(root):
    b = StyleBuilderTTK(build=False)
    pb = ttk.Progressbar(root, bootstyle="@card")
    assert pb.cget("style") == "@card.Horizontal.TProgressbar"
    # recessed trough = border(surface); widget bg = the surface itself
    assert _lookup(root, pb.cget("style"), "troughcolor") == b.border(b.card_surface())
    assert _lookup(root, pb.cget("style"), "background") == b.card_surface()


def test_scrollbar_trough_tracks_surface(root):
    b = StyleBuilderTTK(build=False)
    sb = ttk.Scrollbar(root, bootstyle="@primary")
    # scrollbar default orient is vertical
    assert sb.cget("style") == "@primary.Vertical.TScrollbar"
    # the track floats the thumb on the (accent) surface, no visible channel
    assert _lookup(root, sb.cget("style"), "troughcolor") == b.colors.primary


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


# --- gate <-> recipe correspondence --------------------------------------- #

def test_every_gated_family_honors_surface(root):
    """Every family in `_SURFACE_FAMILIES` must actually emit the `@surface`
    prefix -- guards the hand-maintained gate against drifting from the recipes
    (a listed-but-unwired family would silently degrade instead)."""
    import ttkbootstrap.style.bootstyle as bs
    cases = {
        "button": ttk.Button(root, bootstyle="@card"),
        "checkbutton": ttk.Checkbutton(root, bootstyle="@card"),
        "radiobutton": ttk.Radiobutton(root, bootstyle="@card"),
        "toggle": ttk.Checkbutton(root, bootstyle="@card toggle"),
        "label": ttk.Label(root, bootstyle="@card"),
        "scale": ttk.Scale(root, bootstyle="@card"),
        "progressbar": ttk.Progressbar(root, bootstyle="@card"),
        "scrollbar": ttk.Scrollbar(root, bootstyle="@card"),
    }
    # the test must cover exactly the gate (update both together)
    assert set(cases) == set(bs._SURFACE_FAMILIES)
    for family, w in cases.items():
        assert w.cget("style").startswith("@card."), f"{family} dropped its surface"


def test_inverse_label_prefixes_not_degrades(root):
    """Every label variant honors the surface in its name (no degrade churn)."""
    assert (
        ttk.Label(root, bootstyle="@card inverse").cget("style")
        == "@card.Inverse.TLabel"
    )


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
