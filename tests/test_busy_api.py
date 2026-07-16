"""The busy-method shim (`ttkbootstrap.internal.busy.BusyMixin`).

tkinter grew the ``busy``/``tk_busy_*`` methods in Python 3.13; the underlying
Tcl ``tk busy`` command is Tk 8.6 and works on every Python we support. These
tests pin that the shim presents the same surface either way -- delegating to
tkinter's methods when they exist and issuing the same Tcl call when they don't.

``tk busy`` is not supported on macOS (aqua), so these tests assert Tk's
*bookkeeping* (status/cget/current), which is consistent across platforms,
rather than whether input is actually blocked.
"""
import tkinter

import pytest

import ttkbootstrap as ttk


NATIVE = hasattr(tkinter.Misc, "tk_busy_hold")

ALIASES = [
    "busy", "busy_hold", "tk_busy", "tk_busy_hold",
    "busy_forget", "tk_busy_forget",
    "busy_status", "tk_busy_status",
    "busy_cget", "tk_busy_cget",
    "busy_configure", "busy_config", "tk_busy_config", "tk_busy_configure",
    "busy_current", "tk_busy_current",
]


@pytest.fixture
def widgets(root):
    """A window, a ttk widget, and a tk widget -- the three mixin paths."""
    frame = ttk.Frame(root)
    frame.pack()
    canvas = ttk.Canvas(root)
    canvas.pack()
    root.update_idletasks()
    return root, frame, canvas


@pytest.mark.parametrize("name", ALIASES)
def test_every_alias_is_present_on_a_window(root, name):
    assert callable(getattr(root, name))


def test_aliases_present_on_ttk_and_tk_widgets(widgets):
    _, frame, canvas = widgets
    for name in ALIASES:
        assert callable(getattr(frame, name)), f"ttk widget missing {name}"
        assert callable(getattr(canvas, name)), f"tk widget missing {name}"


def test_hold_status_forget_round_trip(widgets):
    _, frame, _ = widgets
    assert frame.busy_status() is False
    frame.busy(cursor="watch")
    assert frame.busy_status() is True
    frame.busy_forget()
    assert frame.busy_status() is False


def test_cursor_option_reaches_tk(widgets):
    _, frame, _ = widgets
    frame.busy(cursor="watch")
    try:
        assert frame.busy_cget("cursor") == "watch"
    finally:
        frame.busy_forget()


def test_busy_configure_updates_the_cursor(widgets):
    _, frame, _ = widgets
    frame.busy(cursor="watch")
    try:
        frame.busy_configure(cursor="clock")
        assert frame.busy_cget("cursor") == "clock"
    finally:
        frame.busy_forget()


def test_busy_current_lists_held_widgets(widgets):
    root, frame, _ = widgets
    assert frame not in root.busy_current()
    frame.busy(cursor="watch")
    try:
        assert frame in root.busy_current()
    finally:
        frame.busy_forget()
    assert frame not in root.busy_current()


def test_busy_status_returns_a_real_bool(widgets):
    """Not the Tcl "0"/"1" string -- callers write `if w.busy_status():`."""
    _, frame, _ = widgets
    assert isinstance(frame.busy_status(), bool)
    frame.busy()
    try:
        assert isinstance(frame.busy_status(), bool)
    finally:
        frame.busy_forget()


def test_tk_busy_hold_and_busy_are_the_same_call(widgets):
    _, frame, _ = widgets
    frame.tk_busy_hold(cursor="watch")
    try:
        assert frame.busy_status() is True
    finally:
        frame.tk_busy_forget()
    assert frame.busy_status() is False


@pytest.mark.skipif(not NATIVE, reason="tkinter has no native busy methods")
def test_delegates_to_tkinter_when_native(widgets, monkeypatch):
    """On 3.13+ the shim must hand off rather than reimplement."""
    _, frame, _ = widgets
    called = []
    monkeypatch.setattr(
        tkinter.Misc, "tk_busy_hold",
        lambda self, **kw: called.append(kw), raising=True,
    )
    frame.busy(cursor="watch")
    assert called == [{"cursor": "watch"}]


def test_fallback_path_works_without_native_methods(widgets, monkeypatch):
    """Force the < 3.13 branch and prove the tk.call fallback is equivalent.

    This is the path 3.10-3.12 users actually take, so it is exercised here
    even on a newer interpreter.
    """
    _, frame, _ = widgets
    for name in ("tk_busy_hold", "tk_busy_forget", "tk_busy_status",
                 "tk_busy_cget"):
        monkeypatch.delattr(tkinter.Misc, name, raising=False)

    frame.busy(cursor="watch")
    try:
        assert frame.busy_status() is True
        assert frame.busy_cget("cursor") == "watch"
    finally:
        frame.busy_forget()
    assert frame.busy_status() is False