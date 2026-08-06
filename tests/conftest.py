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
from ttkbootstrap.style.scaling import Scaling


def _pin_baseline_density(app):
    """Pin the test root to standard density, so `Scaling.factor` is exactly 1.

    Assets and pixel geometry scale to the display -- that is the point -- so a
    test asserting an exact pixel size is really asserting a display. On a
    scaled screen (Windows at 125%, the factory default on most laptops) four
    such tests failed on a clean checkout, with a one-pixel assertion and no
    hint why. Pinning the shared root covers any other test carrying the same
    latent assumption, and demotes CI's `-dpi 96` from load-bearing to
    belt-and-braces.

    `baseline` rather than a literal: it is 4/3 everywhere except aqua before
    Tk 9, which reports 1.0 for the same standard density.

    Pinned after the root is built, since `Window()` creates the root and the
    `Style` together. The handful of styles built eagerly at that point carry
    the host's density; every asset a test builds, and every style built lazily
    on first use, comes after this.
    """
    app.tk.call("tk", "scaling", Scaling.for_widget(app).baseline)


@pytest.fixture(scope="session", autouse=True)
def _session_root():
    """The one Tk root for the whole test session.

    Created once, withdrawn, and reused by every test. Creating it also binds
    the ``Style`` singleton and initializes the Tcl message catalog, so the
    localization tests have a live interpreter without managing their own root.
    """
    Style.instance = None
    app = ttk.Window()
    _pin_baseline_density(app)
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