"""The ttkbootstrap ``Menu`` widget.

A themed ``tk.Menu`` (via ``AutoStyleMixin``) plus small helpers for the native
macOS application menu — the special application/window/help menus and the
standard ``tk::mac`` commands — so callers reach them through Python instead of
raw Tcl. The helpers are no-ops on Windows and Linux, so one code path builds a
native-feeling menu bar on every platform.
"""

import tkinter as tk

from ttkbootstrap.style import AutoStyleMixin
from ttkbootstrap.utils import windowing_system


class Menu(AutoStyleMixin, tk.Menu):
    """A ``tk.Menu`` with ttkbootstrap theming (accepts ``autostyle=``).

    Beyond the standard ``add_command``/``add_cascade``/``add_checkbutton``/…
    menu API, this adds helpers for the macOS application-menu structure. On
    Windows and Linux — which have no application menu — the ``add_*_menu``
    helpers and the ``on_*`` hooks are no-ops (returning ``None`` where a menu
    would be created), so the same code builds a native menu bar everywhere.
    """

    def _is_aqua(self):
        return windowing_system(self) == "aqua"

    def add_application_menu(self):
        """Add and return the macOS **application menu** — the bold, app-named
        menu at the left of the bar, where *About*, *Preferences…*, and *Quit*
        belong.

        Returns the application :class:`Menu` on macOS, or ``None`` on Windows
        and Linux (which have no application menu). Wire the standard items with
        the returned menu's :meth:`on_preferences` / :meth:`on_quit`; add an
        *About* item with an ordinary ``add_command``.
        """
        if not self._is_aqua():
            return None
        app_menu = type(self)(self, name="apple")
        self.add_cascade(menu=app_menu)
        return app_menu

    def add_window_menu(self, label="Window"):
        """Add and return the macOS standard **Window** menu, or ``None`` on
        Windows and Linux."""
        if not self._is_aqua():
            return None
        window_menu = type(self)(self, name="window")
        self.add_cascade(menu=window_menu, label=label)
        return window_menu

    def add_help_menu(self, label="Help", command=None):
        """Add and return a **Help** menu.

        On macOS this is the standard Help menu, and ``command`` — if given — is
        wired to the native Help search via ``tk::mac::ShowHelp``. On Windows and
        Linux it is an ordinary cascade labeled ``label``; add your own items to
        the returned menu (``command`` is ignored there).
        """
        if self._is_aqua():
            help_menu = type(self)(self, name="help")
            self.add_cascade(menu=help_menu, label=label)
            if command is not None:
                self.tk.createcommand("tk::mac::ShowHelp", command)
            return help_menu
        help_menu = type(self)(self, tearoff=False)
        self.add_cascade(menu=help_menu, label=label)
        return help_menu

    # -- Standard commands. Meaningful only on macOS (on the application menu). --

    def on_preferences(self, callback):
        """Enable the macOS **Preferences…** item (``⌘,``) and call ``callback``
        when it is chosen. No-op on Windows and Linux. Call on the menu returned
        by :meth:`add_application_menu`."""
        if self._is_aqua():
            self.tk.createcommand("tk::mac::ShowPreferences", callback)

    def on_quit(self, callback):
        """Call ``callback`` when the user chooses macOS **Quit** (``⌘Q``). No-op
        on Windows and Linux. Call on the menu returned by
        :meth:`add_application_menu`."""
        if self._is_aqua():
            self.tk.createcommand("tk::mac::Quit", callback)
