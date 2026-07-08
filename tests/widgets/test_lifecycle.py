"""Lifecycle/leak regression tests (2.0 Workstreams A & B).

Widgets that schedule `after()` loops or add variable traces must release
those resources when they are reconfigured or destroyed. Otherwise a destroyed
widget keeps firing callbacks (raising `TclError`) or is kept alive by an
external variable's trace.

Workstream A (the engine repaint rewrite) also removed the `Publisher`: the
theme walk now repaints the live widget tree directly, so nothing subscribes a
per-widget closure at construction (the old leak class). The combobox tests
below assert that the engine holds no `Publisher` subscriptions and that a
theme switch still repaints every mounted widget via the version-stamped walk.

Runnable headlessly with pytest.
"""
import tkinter as tk

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.internal.publisher import Publisher
from ttkbootstrap.widgets.floodgauge import Floodgauge
from ttkbootstrap.widgets.meter import Meter


# --------------------------------------------------------------------------- #
# Floodgauge (canvas)
# --------------------------------------------------------------------------- #
def test_floodgauge_external_var_trace_released_on_destroy(root):
    """Destroying a Floodgauge detaches traces from an external variable."""
    var = ttk.IntVar(master=root, value=0)
    fg = Floodgauge(root, variable=var)
    root.update_idletasks()
    assert len(var.trace_info()) == 1

    fg.destroy()
    assert len(var.trace_info()) == 0


def test_floodgauge_configure_variable_no_trace_accumulation(root):
    """Swapping the variable via configure removes the old trace."""
    fg = Floodgauge(root)
    v1 = ttk.IntVar(master=root)
    fg.configure(variable=v1)
    assert len(v1.trace_info()) == 1

    v2 = ttk.IntVar(master=root)
    fg.configure(variable=v2)
    assert len(v1.trace_info()) == 0  # old trace gone
    assert len(v2.trace_info()) == 1  # new var traced exactly once


def test_floodgauge_destroy_cancels_animation(root):
    """A running animation loop is cancelled on destroy."""
    fg = Floodgauge(root, mode="indeterminate")
    fg.pack()
    root.update_idletasks()
    fg.start()
    assert fg._after_id is not None

    fg.destroy()
    assert fg._after_id is None
    root.update()  # a stale after-callback would raise here


# --------------------------------------------------------------------------- #
# Meter
# --------------------------------------------------------------------------- #
def test_meter_interactive_toggle_no_bind_accumulation(root):
    """Toggling interactive mode does not accumulate indicator bindings."""
    m = Meter(root, interactive=True)
    root.update_idletasks()
    assert len(m._bindids) == 2

    # Re-asserting interactive must not add a second pair of bindings.
    m.configure(interactive=True)
    assert len(m._bindids) == 2

    m.configure(interactive=False)
    assert len(m._bindids) == 0


def test_meter_value_trace_released_on_destroy(root):
    """Destroying a meter detaches its value-variable trace."""
    m = Meter(root, amount_used=10)
    root.update_idletasks()
    var = m.amount_used_var
    assert len(var.trace_info()) == 1

    m.destroy()
    assert len(var.trace_info()) == 0


# --------------------------------------------------------------------------- #
# Engine repaint walk (Workstream A) — Publisher elimination
# --------------------------------------------------------------------------- #
def test_engine_holds_no_publisher_subscriptions(root):
    """The engine no longer subscribes per-widget closures to the Publisher.

    The old leak class was a strong ref held by a Publisher closure for every
    styled widget. Creating widgets (incl. a combobox, the last subscriber)
    must leave the subscriber count untouched.
    """
    base = Publisher.subscriber_count()
    widgets = [
        ttk.Button(root, bootstyle="primary"),
        ttk.Combobox(root, values=["a", "b"]),
        ttk.Frame(root),
    ]
    for w in widgets:
        w.pack()
    root.update_idletasks()
    assert Publisher.subscriber_count() == base == 0


def test_theme_walk_stamps_and_repaints_mounted_widgets(root):
    """A theme switch repaints the live tree and restamps every widget."""
    style = root.style
    btn = ttk.Button(root, bootstyle="primary")
    frame = ttk.Frame(root)
    nested = ttk.Label(frame, bootstyle="info")
    cb = ttk.Combobox(root, values=["a", "b"])
    for w in (btn, frame, cb):
        w.pack()
    nested.pack()
    root.update_idletasks()

    start = style.theme.name
    other = "bootstrap-dark" if start != "bootstrap-dark" else "bootstrap-light"
    bg_before = style.lookup("primary.TButton", "background")

    style.theme_use(other)
    root.update_idletasks()

    # every mounted widget, including a deeply nested one, is now current
    version = style._theme_version
    for w in (btn, frame, nested, cb):
        assert getattr(w, "_theme_version", None) == version

    # the (theme, style) pair was actually rebuilt for the new theme
    assert style.lookup("primary.TButton", "background") != bg_before


def test_autostyle_false_widget_skipped_by_walk(root):
    """A tk widget created with autostyle=False is never touched by the walk.

    The blessed tk widgets (`ttk.Canvas` etc.) carry `AutoStyleMixin`, so the
    `autostyle=` keyword is delivered through the concrete subclass rather than
    a global monkey-patch.
    """
    style = root.style
    start = style.theme.name
    other = "bootstrap-dark" if start != "bootstrap-dark" else "bootstrap-light"

    plain = ttk.Canvas(root, autostyle=False, background="#abcdef")
    styled = ttk.Canvas(root)
    plain.pack()
    styled.pack()
    root.update_idletasks()
    styled_before = styled.cget("background")

    style.theme_use(other)
    root.update_idletasks()

    # opted-out widget keeps its manual color and is never stamped
    assert plain.cget("background") == "#abcdef"
    assert not hasattr(plain, "_theme_version")
    # a normal autostyled widget still repaints
    assert styled.cget("background") != styled_before


def test_theme_switch_cycles_do_not_leak_subscribers(root):
    """Repeated create/destroy/theme-switch cycles leave no residual refs."""
    style = root.style
    start = style.theme.name
    other = "bootstrap-dark" if start != "bootstrap-dark" else "bootstrap-light"

    for _ in range(5):
        w = ttk.Combobox(root, values=["a", "b"])
        w.pack()
        root.update_idletasks()
        style.theme_use(other)
        style.theme_use(start)
        w.destroy()
        root.update_idletasks()

    assert Publisher.subscriber_count() == 0


# --------------------------------------------------------------------------- #
# Single-root enforcement (Workstream A)
# --------------------------------------------------------------------------- #
def test_second_live_root_raises(root):
    """Creating a second root while one is live raises a clear RuntimeError.

    The guard fires before the second Tk interpreter is built, so the shared
    session root and Style singleton are left untouched.
    """
    with pytest.raises(RuntimeError, match="single application root"):
        ttk.Window()