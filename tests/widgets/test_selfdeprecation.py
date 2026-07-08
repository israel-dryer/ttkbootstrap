"""Regression tests: ToolTip and ToastNotification must not emit a
`DeprecationWarning` from ttkbootstrap's own code (PR 0 of the 2.0 widget-API
review).

After the PR B Window normalization, both widgets injected the *legacy*
`overrideredirect`/`windowtype` spellings into their internal `Toplevel`, which
routed through `_compat.normalize_window_kwargs` and warned on every
tooltip hover / toast show. They now inject the canonical
`override_redirect`/`window_type` (keyword-only `Toplevel` params), so the
warning is gone. The warning fires when the `Toplevel` is *built* (on show), not
at widget construction, so the tests drive the show path.
"""
import warnings

import ttkbootstrap as ttk
from ttkbootstrap.widgets.toast import ToastNotification
from ttkbootstrap.widgets.tooltip import ToolTip


def test_tooltip_show_is_deprecation_warning_free(root):
    btn = ttk.Button(root, text="hover me")
    btn.pack()
    tip = ToolTip(btn, text="a tip")
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        tip.show_tip()  # builds the Toplevel; legacy kwargs would raise here
        tip.hide_tip()


def test_toast_show_is_deprecation_warning_free(root):
    toast = ToastNotification("Title", "Message", duration=1000)
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        toast.show_toast()  # builds the Toplevel
    toast.hide_toast()
