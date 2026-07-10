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
from ttkbootstrap.dialogs.query import QueryDialog
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


def test_close_before_show_is_a_safe_noop(root):
    # close() on a dialog that was never shown has no toplevel; it must be a
    # no-op rather than raising on None.
    dialog = MessageDialog(message="hi", parent=root)
    assert dialog._toplevel is None
    dialog.close()  # must not raise


def test_close_destroys_the_toplevel_and_is_idempotent(root):
    dialog = MessageDialog(message="hi", parent=root, buttons=["OK:primary"])
    dialog.build()
    dialog._toplevel.withdraw()
    assert dialog._toplevel.winfo_exists()
    dialog.close()
    assert not dialog._toplevel.winfo_exists()
    dialog.close()  # second call is a no-op (winfo_exists guard), must not raise


def test_close_is_safe_after_interpreter_teardown(root):
    # winfo_exists() raises TclError once the application is destroyed; close()
    # must swallow that and stay a no-op (matching the result property's guard),
    # not propagate the error out of a cleanup path. Simulate the torn-down
    # state with a stub rather than destroying a real root -- destroying a second
    # root would corrupt the process-wide Style singleton for other tests.
    import tkinter

    class _DeadToplevel:
        def winfo_exists(self):
            raise tkinter.TclError("application has been destroyed")

        def destroy(self):  # pragma: no cover - must never be reached
            raise AssertionError("destroy() should not run when the app is gone")

    dialog = MessageDialog(message="hi", parent=root)
    dialog._toplevel = _DeadToplevel()
    dialog.close()  # must not raise


def test_escape_binding_is_installed_for_dismissal(root):
    # The base class wires <Escape> to dismiss the dialog (it routes through the
    # public close()). Synthesizing the keypress needs a mapped window + running
    # loop the headless fixture can't guarantee, so assert the binding exists;
    # close()'s destroy behavior is covered above.
    dialog = MessageDialog(message="hi", parent=root, buttons=["OK:primary"])
    dialog.build()
    dialog._toplevel.withdraw()
    assert dialog._toplevel.bind("<Escape>"), "an <Escape> binding should be installed"


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


def test_datepicker_selection_highlight_does_not_bleed_across_months(root):
    # Regression: `datevar` (shared by every day cell) was only re-set in the
    # branch matching the selected month, so browsing to another month left it
    # pinned to the selected day number and that day was spuriously highlighted
    # in every month. Each redraw must clear it (0 = no cell) and re-select the
    # day only in the selected month.
    import datetime
    picker = DatePickerDialog(
        parent=root, start_date=datetime.date(2026, 7, 9), autoshow=False
    )
    try:
        assert picker.datevar.get() == 9          # selected month: day is selected
        picker.on_next_month()
        assert picker.datevar.get() == 0          # other month: nothing selected
        picker.on_next_year()
        assert picker.datevar.get() == 0
        picker.on_prev_year()
        picker.on_prev_month()
        assert picker.datevar.get() == 9          # back to selected month: restored
    finally:
        try:
            picker.root.destroy()
        except Exception:
            pass


def test_message_and_query_dialogs_use_consistent_button_spacing(root):
    # Regression: QueryDialog packed its Submit/Cancel buttons with padx=5 while
    # MessageDialog uses padx=2, so the Querybox button row read visibly looser
    # than the Messagebox row. The two sibling dialogs must space buttons alike.
    def button_padx(dlg):
        dlg.build()
        dlg._toplevel.withdraw()
        pads = [
            w.pack_info().get("padx")
            for child in dlg._toplevel.winfo_children()
            for w in child.winfo_children()
            if isinstance(w, ttk.Button)
        ]
        dlg._toplevel.destroy()
        return pads

    md = button_padx(
        MessageDialog("body", title="m", parent=root, buttons=["Cancel", "OK:primary"])
    )
    qd = button_padx(QueryDialog("prompt", title="q", parent=root))
    assert md and qd
    assert set(md) == set(qd) == {2}


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
