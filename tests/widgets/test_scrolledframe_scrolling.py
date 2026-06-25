"""Regression tests for ScrolledFrame enable/disable scrolling (PR #1064).

A user calling ``disable_scrolling()`` must stay disabled even when the
mouse later enters the frame. Previously ``_on_enter`` called the public
``enable_scrolling()``, silently re-enabling scrolling on the next hover.

Runnable headlessly with pytest.
"""
import ttkbootstrap as ttk
from ttkbootstrap.widgets.scrolled import ScrolledFrame

# Mousewheel binding sequence differs by windowing system.
_SEQUENCES = ("<MouseWheel>", "<Button-4>", "<Button-5>")


def _make_frame(app):
    frame = ScrolledFrame(app, autohide=False)
    child = ttk.Label(frame, text="hi")
    child.pack()
    app.update_idletasks()
    return frame, child


def _is_bound(child):
    bindings = child.bind()
    return any(seq in bindings for seq in _SEQUENCES)


def test_disable_survives_hover(root):
    """The core bug: hovering must not re-enable a disabled frame."""
    frame, child = _make_frame(root)
    frame.enable_scrolling()
    assert _is_bound(child)

    frame.disable_scrolling()
    assert not _is_bound(child)

    # Mouse enters the frame: must remain disabled.
    frame._on_enter(None)
    assert not _is_bound(child)


def test_enabled_hover_rebinds(root):
    """When enabled, normal hover-in/out (autohide path) still works."""
    frame, child = _make_frame(root)
    frame.enable_scrolling()
    frame._on_leave(None)
    assert not _is_bound(child)
    frame._on_enter(None)
    assert _is_bound(child)