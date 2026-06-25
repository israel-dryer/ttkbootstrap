"""Shared pytest fixtures for the ttkbootstrap headless test suite.

ttkbootstrap's :class:`~ttkbootstrap.style.Style` is a process-wide singleton
(``Style.instance``) bound to the Tk root that first created it. When each test
creates and destroys its own ``Window`` the singleton ends up pointing at a
destroyed root, so a later test's theming silently no-ops (e.g. a
``theme_use(...)`` that never reaches a live interpreter). Run alone the tests
pass; run together they bleed into each other.

Following the bootstack approach, GUI tests share a SINGLE session-wide root
(`_session_root`) that is never destroyed mid-session. The per-test `root`
fixture hands that root to a test and, on teardown, destroys the widgets the
test created and restores the active theme — so each test starts clean without
paying for (or mis-binding) a fresh root.
"""
import tkinter

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style import Style


@pytest.fixture(scope="session", autouse=True)
def _session_root():
    """The one Tk root for the whole test session.

    Created once, withdrawn, and reused by every test. Creating it also binds
    the ``Style`` singleton and initializes the Tcl message catalog, so the
    localization tests have a live interpreter without managing their own root.
    """
    Style.instance = None
    app = ttk.Window()
    app.withdraw()
    app.update_idletasks()
    try:
        yield app
    finally:
        try:
            app.destroy()
        except tkinter.TclError:
            pass
        Style.instance = None


@pytest.fixture
def root(_session_root):
    """The shared root for a test, scene- and theme-reset afterward.

    Widgets the test parents into the root are destroyed on teardown and the
    active theme is restored, so a test that changes either does not leak into
    the next one.
    """
    app = _session_root
    style = app.style
    theme_before = style.theme.name
    keep = {str(w) for w in app.winfo_children()}
    try:
        yield app
    finally:
        for w in list(app.winfo_children()):
            if str(w) not in keep:
                try:
                    w.destroy()
                except tkinter.TclError:
                    pass
        if style.theme.name != theme_before:
            style.theme_use(theme_before)
        app.update_idletasks()