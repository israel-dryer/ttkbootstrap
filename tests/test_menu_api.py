"""Menu API: the macOS application-menu helpers on ``ttk.Menu``.

The helpers wrap the native macOS application menu (the special apple/window/help
menus and the ``tk::mac`` standard commands) so callers stay in Python. On the
CI platform (win32/x11) the ``add_*_menu`` helpers no-op; the aqua path is
exercised by forcing the windowing-system probe.
"""

import ttkbootstrap as ttk
import ttkbootstrap.menu as menu_mod


def _force_aqua(monkeypatch):
    """Make ``Menu`` believe it is running on macOS."""
    monkeypatch.setattr(menu_mod, "windowing_system", lambda widget: "aqua")


def test_menu_is_the_extended_class(root):
    assert isinstance(ttk.Menu(root), menu_mod.Menu)
    for name in ("add_application_menu", "add_window_menu", "add_help_menu",
                 "on_preferences", "on_quit"):
        assert hasattr(ttk.Menu(root), name), name


def test_application_and_window_menus_are_none_off_mac(root):
    menubar = ttk.Menu(root)
    assert menubar.add_application_menu() is None
    assert menubar.add_window_menu() is None


def test_on_hooks_are_noop_off_mac(root):
    menubar = ttk.Menu(root)
    # Must not raise and must not register the mac commands off-aqua.
    menubar.on_preferences(lambda: None)
    menubar.on_quit(lambda: None)
    assert not root.tk.call("info", "commands", "::tk::mac::ShowPreferences")
    assert not root.tk.call("info", "commands", "::tk::mac::Quit")


def test_help_menu_is_a_real_cascade_off_mac(root):
    menubar = ttk.Menu(root)
    help_menu = menubar.add_help_menu(command=lambda: None)
    assert isinstance(help_menu, ttk.Menu)
    # It is attached to the bar as a cascade.
    assert menubar.index("end") is not None
    # `command` is ignored off-aqua — no ShowHelp registered.
    assert not root.tk.call("info", "commands", "::tk::mac::ShowHelp")


def test_special_menu_names_on_mac(root, monkeypatch):
    _force_aqua(monkeypatch)
    menubar = ttk.Menu(root)
    app_menu = menubar.add_application_menu()
    window_menu = menubar.add_window_menu()
    help_menu = menubar.add_help_menu()
    assert isinstance(app_menu, ttk.Menu)
    assert str(app_menu).endswith(".apple")
    assert str(window_menu).endswith(".window")
    assert str(help_menu).endswith(".help")


def test_standard_commands_registered_on_mac(root, monkeypatch):
    _force_aqua(monkeypatch)
    menubar = ttk.Menu(root)
    app_menu = menubar.add_application_menu()
    try:
        app_menu.on_preferences(lambda: None)
        app_menu.on_quit(lambda: None)
        menubar.add_help_menu(command=lambda: None)
        assert root.tk.call("info", "commands", "::tk::mac::ShowPreferences")
        assert root.tk.call("info", "commands", "::tk::mac::Quit")
        assert root.tk.call("info", "commands", "::tk::mac::ShowHelp")
    finally:
        # The commands live on the shared interpreter; don't leak into other tests.
        for cmd in ("tk::mac::ShowPreferences", "tk::mac::Quit", "tk::mac::ShowHelp"):
            try:
                root.tk.deletecommand(cmd)
            except Exception:
                pass
