"""Re-export coverage for the shipped widgets that were unreachable as
``ttk.<Name>`` before the 2.0 widget-API review (PR 1).

Before this pass ``ToolTip`` and ``ToastNotification`` were only importable from
``ttkbootstrap.widgets``, and ``ScrolledText``/``ScrolledFrame`` were not exported
from the widgets package at all (only via ``ttkbootstrap.widgets.scrolled``). They
now match every other shipped widget: reachable at the top level and listed in the
relevant ``__all__``.
"""
import ttkbootstrap as ttk
from ttkbootstrap import widgets as _widgets
from ttkbootstrap.widgets.scrolled import ScrolledFrame, ScrolledText
from ttkbootstrap.widgets.toast import ToastNotification
from ttkbootstrap.widgets.tooltip import ToolTip


def test_popup_widgets_reexported_at_top_level():
    assert ttk.ToolTip is ToolTip
    assert ttk.ToastNotification is ToastNotification
    for name in ("ToolTip", "ToastNotification"):
        assert name in ttk.__all__


def test_scrolled_widgets_reexported_at_top_level():
    assert ttk.ScrolledText is ScrolledText
    assert ttk.ScrolledFrame is ScrolledFrame
    for name in ("ScrolledText", "ScrolledFrame"):
        assert name in ttk.__all__


def test_scrolled_widgets_reexported_from_widgets_package():
    # These were previously not imported into the widgets package at all.
    assert _widgets.ScrolledText is ScrolledText
    assert _widgets.ScrolledFrame is ScrolledFrame
    for name in ("ScrolledText", "ScrolledFrame"):
        assert name in _widgets.__all__
