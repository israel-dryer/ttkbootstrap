"""The themed popup-menu border (issue #1309).

Tk gives ``tk.Menu`` no border color of its own, so the border is painted by
putting the *menu* background in ``colors.border`` and every entry in
``colors.bg`` -- entries tile the whole interior of a popup, leaving only the
1px strip showing. See ``StyleBuilderTK._paint_menu_hairline``.

Only x11 needs it: Windows and macOS draw menus with native OS chrome, which
supplies the border. The builder picks the path from a single
``scaling.windowing_system`` probe, so **both** branches are exercised by forcing
that probe rather than by trusting the host -- otherwise a developer on Linux
tests only the x11 branch and a developer on macOS only the other one.

These assert the configuration the painter applies. The border was verified
against real pixels on X11 (``xwd`` capture of a posted menu, all four edges
reading exactly ``colors.border``); a headless suite cannot post and capture.
"""

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style.builders_tk import _MENU_HAIRLINE_TAG
from ttkbootstrap.style.scaling import Scaling


def _force_windowing_system(monkeypatch, name):
    """Make the style builder believe it is running on `name`."""
    monkeypatch.setattr(
        Scaling, "windowing_system", property(lambda self: name)
    )


def _paint(root, menu):
    """Paint `menu` as posting it would, without needing a display."""
    builder = root.style._get_builder_tk()
    builder._paint_menu_hairline(menu)


@pytest.fixture
def x11(monkeypatch):
    _force_windowing_system(monkeypatch, "x11")


def test_menu_reserves_the_border_strip_on_x11(root, x11):
    menu = ttk.Menu(root)
    assert int(menu.cget("borderwidth")) == root.style.scaling.logical(1)
    assert _MENU_HAIRLINE_TAG in menu.bindtags()


@pytest.mark.parametrize("system", ["win32", "aqua"])
def test_native_platforms_keep_the_borderless_menu(root, monkeypatch, system):
    """Windows and macOS get the OS's own menu chrome; we must not touch it."""
    _force_windowing_system(monkeypatch, system)
    menu = ttk.Menu(root)
    assert int(menu.cget("borderwidth")) == 0
    assert _MENU_HAIRLINE_TAG not in menu.bindtags()
    assert str(menu.cget("background")) == root.style.colors.bg


def test_painting_draws_the_border_in_the_theme_border_color(root, x11):
    menu = ttk.Menu(root)
    menu.add_command(label="Open")
    menu.add_separator()
    menu.add_command(label="Save")
    _paint(root, menu)

    colors = root.style.colors
    assert str(menu.cget("background")) == colors.border
    for index in range(menu.index("end") + 1):
        assert str(menu.entrycget(index, "background")) == colors.bg


def test_an_entry_added_after_theming_does_not_show_the_border_color(root, x11):
    """Entries inherit the menu background, so a late entry would come up in the
    border color; the repaint on ``<Map>`` catches it before the menu is drawn."""
    menu = ttk.Menu(root)
    menu.add_command(label="Open")
    _paint(root, menu)

    menu.add_command(label="Added later")
    assert str(menu.entrycget(1, "background")) == ""  # inherits: would be border
    _paint(root, menu)
    assert str(menu.entrycget(1, "background")) == root.style.colors.bg


def test_a_never_posted_menu_is_not_painted(root, x11):
    """The guard that keeps a menubar intact.

    A menubar's entries cover only the left of the bar, so painting it would
    flood the rest with the border color. Tk displays a menubar through a
    *clone*, so the widget styled here never maps -- and only a map paints.
    """
    menubar = ttk.Menu(root)
    menubar.add_cascade(label="File")
    root.configure(menu=menubar)
    try:
        assert str(menubar.cget("background")) == root.style.colors.bg
        assert not getattr(menubar, "_tb_menu_hairline", False)
    finally:
        root.configure(menu="")


def test_entries_follow_a_theme_switch(root, x11):
    menu = ttk.Menu(root)
    menu.add_command(label="Open")
    _paint(root, menu)

    root.style.theme_use("bootstrap-dark")
    colors = root.style.colors
    assert str(menu.cget("background")) == colors.border
    assert str(menu.entrycget(0, "background")) == colors.bg


def test_an_entry_given_its_own_color_keeps_it(root, x11):
    menu = ttk.Menu(root)
    menu.add_command(label="Plain")
    menu.add_command(label="Custom")
    menu.entryconfigure(1, background="#ff0000")
    _paint(root, menu)

    assert str(menu.entrycget(0, "background")) == root.style.colors.bg
    assert str(menu.entrycget(1, "background")) == "#ff0000"


def test_repainting_is_idempotent(root, x11):
    menu = ttk.Menu(root)
    menu.add_command(label="Open")
    for _ in range(3):
        _paint(root, menu)
    colors = root.style.colors
    assert str(menu.cget("background")) == colors.border
    assert str(menu.entrycget(0, "background")) == colors.bg


def test_an_empty_menu_paints_without_error(root, x11):
    """``index("end")`` is None for a menu with no entries."""
    menu = ttk.Menu(root)
    _paint(root, menu)
    assert str(menu.cget("background")) == root.style.colors.border
