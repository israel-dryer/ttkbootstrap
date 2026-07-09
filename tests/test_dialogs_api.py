"""Headless tests for the 2.0 shipped-widget dialog API normalization (PR A).

These exercise the *contract* changes -- signatures, result conventions,
deprecations, and re-exports -- WITHOUT opening a modal dialog. The dialog
facades block on ``grab_set``/``wait_window`` when shown, so nothing here calls
``.show()``; the modal appearance is left to the manual visual gate.
"""
import inspect
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox, Querybox
from ttkbootstrap.dialogs.base import Dialog
from ttkbootstrap.dialogs.message import MessageDialog
from ttkbootstrap.dialogs.datepicker import DatePickerDialog


_MESSAGEBOX_METHODS = [
    "show_info", "show_warning", "show_error", "show_question",
    "ok", "okcancel", "yesno", "yesnocancel", "retrycancel",
]


# --- re-exports ------------------------------------------------------------

def test_dialog_surface_reexported_at_top_level():
    for name in (
        "Messagebox", "Querybox", "Dialog", "MessageDialog", "QueryDialog",
        "DatePickerDialog", "FontDialog", "ColorChooser", "ColorChooserDialog",
        "ColorDropperDialog",
    ):
        assert hasattr(ttk, name), f"ttk.{name} should be re-exported"
        assert name in ttk.__all__


# --- Messagebox uniform, keyword-only signatures ---------------------------

@pytest.mark.parametrize("method", _MESSAGEBOX_METHODS)
def test_messagebox_parent_and_alert_are_keyword_only(method):
    sig = inspect.signature(getattr(Messagebox, method))
    params = sig.parameters
    # message + title stay positional-or-keyword; the rest are keyword-only.
    assert params["message"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params["title"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    for name in ("parent", "alert", "position", "buttons", "icon", "localize"):
        assert name in params, f"{method} missing named param {name!r}"
        assert params[name].kind is inspect.Parameter.KEYWORD_ONLY, (
            f"{method}.{name} should be keyword-only"
        )


def test_messagebox_rejects_positional_parent(root):
    # parent is keyword-only now, so a positional 3rd arg raises before any
    # dialog is built -- no window is shown.
    with pytest.raises(TypeError):
        Messagebox.ok("message", "title", root)


# --- result convention -----------------------------------------------------

def test_base_result_is_safe_without_a_toplevel(root):
    # A dialog that was constructed but never shown has no toplevel; reading
    # .result must not raise (it used to call grab_release unconditionally).
    dialog = MessageDialog(message="hi", parent=root)
    assert dialog._toplevel is None
    assert dialog.result is None


def test_querybox_get_string_returns_via_result_property():
    # Every get_* now returns dialog.result, not the private ._result.
    src = inspect.getsource(Querybox.get_string)
    assert "dialog.result" in src
    assert "dialog._result" not in src


# --- MessageDialog.command de-vestigialization -----------------------------

def test_command_plain_callable_stored_without_warning(root):
    called = []
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        dialog = MessageDialog(message="x", parent=root, command=lambda: called.append(1))
    assert callable(dialog._command)


def test_command_tuple_form_is_deprecated_and_unwrapped(root):
    fn = lambda: None
    with pytest.warns(DeprecationWarning):
        dialog = MessageDialog(message="x", parent=root, command=(fn, "label"))
    # the callable is unwrapped from the legacy (callable, label) tuple
    assert dialog._command is fn


# --- ColorChoice dedupe ----------------------------------------------------

def test_colorchoice_is_a_single_type():
    from ttkbootstrap.dialogs.colorchooser import ColorChoice as CC1
    from ttkbootstrap.dialogs.colordropper import ColorChoice as CC2
    assert CC1 is CC2


# --- get_date cancellation -------------------------------------------------

def test_get_date_signature_returns_optional_and_position_kwonly():
    sig = inspect.signature(Querybox.get_date)
    assert sig.parameters["position"].kind is inspect.Parameter.KEYWORD_ONLY


def test_datepicker_result_is_none_until_a_day_is_selected(root):
    # autoshow=False builds the calendar without grabbing/blocking.
    chooser = DatePickerDialog(parent=root, autoshow=False)
    try:
        # No selection yet -> cancellation semantics -> None, even though
        # date_selected defaults to today.
        assert chooser.date_selected is not None
        assert chooser._selection_made is False
        assert chooser.result is None

        # Simulate a real pick (the flag is what _on_date_selected sets).
        picked = chooser.date_selected
        chooser._selection_made = True
        assert chooser.result == picked
    finally:
        try:
            chooser.root.destroy()
        except Exception:
            pass


def test_datepicker_has_show_and_autoshow():
    sig = inspect.signature(DatePickerDialog.__init__)
    assert "autoshow" in sig.parameters
    assert hasattr(DatePickerDialog, "show")
    assert isinstance(inspect.getattr_static(DatePickerDialog, "result"), property)


# --- ColorChooser: builds under the 2.0 default (no global monkey-patch) ----
# Regression: the swatch/preview widgets used native tk.Frame/tk.Label with
# `autostyle=False`, which stock tkinter rejects unless enable_global_api() has
# patched the tk constructors. They now use the blessed ttk.TkFrame/ttk.TkLabel
# (AutoStyleMixin), which honor `autostyle=` in both modes.

def test_blessed_tk_label_opts_out_of_theming(root):
    lbl = ttk.TkLabel(root, text="x", background="#ff0000", autostyle=False)
    from ttkbootstrap.style import AutoStyleMixin
    assert isinstance(lbl, AutoStyleMixin)
    assert getattr(lbl, "_tb_no_autostyle", False) is True
    assert lbl.cget("background") == "#ff0000"   # theme did not repaint it


def test_colorchooser_builds_without_global_api(root):
    from ttkbootstrap.dialogs.colorchooser import ColorChooser
    cc = ColorChooser(root, initialcolor="#3366cc")
    assert isinstance(cc.preview, ttk.TkFrame)
    assert isinstance(cc.preview_lbl, ttk.TkLabel)


def test_colorchooserdialog_build_without_global_api(root):
    from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
    dlg = ColorChooserDialog(initialcolor="#3366cc")
    dlg.build()   # full body + buttonbox (regressed on the ToolTip call)
    assert dlg._toplevel is not None
    dlg._toplevel.destroy()
