"""Headless tests for the 2.0 shipped-widget dialog API normalization (PR A).

These exercise the *contract* changes -- signatures, result conventions,
deprecations, and re-exports -- WITHOUT opening a modal dialog. The dialog
facades block on ``grab_set``/``wait_window`` when shown, so nothing here calls
``.show()``; the modal appearance is left to the manual visual gate.
"""
import base64
import inspect
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox, Querybox
from ttkbootstrap.dialogs import message as message_mod
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


# --- MessageDialog icon forms (#1342) --------------------------------------

# A 1x1 transparent GIF, the smallest thing Tk's photo image reader accepts --
# used to exercise the base64-data and file-path forms.
_ONE_PIXEL_GIF = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"


def _icon_label(root, icon):
    """Build the icon Label the way create_body does, without showing a dialog."""
    dialog = MessageDialog(message="x", parent=root, icon=icon)
    return dialog._create_icon_label(root)


def _image_name(label):
    """The Tk image name on a Label -- cget yields a 1-tuple for a PhotoImage."""
    value = label.cget("image")
    if isinstance(value, (tuple, list)):
        value = value[0] if value else ""
    return str(value)


def test_icon_accepts_a_bootstrap_glyph_name(root):
    # The form the reference pages have always documented ("a Bootstrap Icons
    # glyph name"), and which used to warn and show nothing.
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        label = _icon_label(root, "question-circle-fill")
    assert label is not None
    assert _image_name(label)


def test_glyph_name_renders_at_the_dialog_size_in_the_theme_foreground(root):
    # The defaults a bare glyph name implies. ttk.Icon dedupes on
    # (name, size, color), so an identical call returns the same image name --
    # asserting the icon IS Icon(name, _ICON_SIZE) pins both the size and the
    # foreground color (no semantic color is guessed from the glyph name).
    label = _icon_label(root, "gear-fill")
    expected = ttk.Icon("gear-fill", message_mod._ICON_SIZE)
    assert _image_name(label) == expected


def test_a_custom_glyph_matches_the_built_in_alert_glyph_size(root):
    # A caller's glyph should carry the same visual weight as the glyph
    # show_info/show_error render for themselves.
    custom = _image_name(_icon_label(root, "gear-fill"))
    alert = message_mod._alert_icon("info")
    width = lambda name: root.tk.call("image", "width", name)
    assert width(custom) == width(alert)


def test_icon_accepts_a_rendered_icon_image_name(root):
    # The pre-#1342 form -- an explicit ttk.Icon(...), which stays the way to
    # ask for a non-default size or color -- keeps working unchanged.
    rendered = ttk.Icon("question-circle-fill", 40, "warning")
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        label = _icon_label(root, rendered)
    assert _image_name(label) == rendered


def test_icon_accepts_a_photoimage_object(root):
    photo = ttk.PhotoImage(data=_ONE_PIXEL_GIF)
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        label = _icon_label(root, photo)
    assert _image_name(label) == str(photo)


def test_icon_accepts_base64_image_data(root):
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        label = _icon_label(root, _ONE_PIXEL_GIF)
    assert label is not None


def test_icon_accepts_a_file_path(root, tmp_path):
    path = tmp_path / "icon.gif"
    path.write_bytes(base64.b64decode(_ONE_PIXEL_GIF))
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        label = _icon_label(root, str(path))
    assert label is not None


def test_an_unusable_icon_still_warns_and_shows_no_icon(root):
    # An unknown glyph name is not silently swallowed by the new candidate:
    # ttk.Icon raises ValueError, the remaining forms fail, and the dialog is
    # built without an icon rather than failing to open.
    with pytest.warns(UserWarning, match="could not be loaded"):
        assert _icon_label(root, "not-a-real-glyph-name") is None


@pytest.mark.parametrize("method", _MESSAGEBOX_METHODS)
def test_messagebox_icon_annotation_admits_more_than_str(method):
    # `icon: str` was true but useless -- ttk.Icon returns a str too, so all of
    # the accepted string forms and the rejected one shared a single type.
    annotation = inspect.signature(getattr(Messagebox, method)).parameters["icon"].annotation
    assert "PhotoImage" in str(annotation)


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


# --- Querybox file dialogs (native, surfaced through the facade) -----------

_FILE_METHODS = ["get_open_filename", "get_open_filenames", "get_save_filename", "get_directory"]


def test_filedialog_reexported_at_top_level():
    import tkinter
    assert ttk.filedialog is tkinter.filedialog
    assert "filedialog" in ttk.__all__


@pytest.mark.parametrize("method", _FILE_METHODS)
def test_querybox_file_methods_are_static_with_parent(method):
    assert isinstance(inspect.getattr_static(Querybox, method), staticmethod)
    assert "parent" in inspect.signature(getattr(Querybox, method)).parameters


def test_querybox_file_dialogs_normalize_cancel_to_none(monkeypatch):
    # The stdlib file dialogs return "" / () on cancel; the wrappers normalize
    # that to None to match the rest of the get_* facade. Monkeypatch the native
    # calls so no OS dialog opens. `native=True` forces the path under test
    # rather than trusting the host: on X11 the default routing is the themed
    # dialog, whose modal show() would hang the suite. The routing itself is
    # covered by test_use_native_filedialog_none_is_platform_aware.
    from ttkbootstrap.dialogs import query

    monkeypatch.setattr(query.filedialog, "askopenfilename", lambda **kw: "")
    assert Querybox.get_open_filename(native=True) is None
    monkeypatch.setattr(query.filedialog, "askopenfilename", lambda **kw: "C:/a/b.txt")
    assert Querybox.get_open_filename(native=True, title="Open") == "C:/a/b.txt"

    monkeypatch.setattr(query.filedialog, "askopenfilenames", lambda **kw: ())
    assert Querybox.get_open_filenames(native=True) is None
    monkeypatch.setattr(query.filedialog, "askopenfilenames", lambda **kw: ("a", "b"))
    assert Querybox.get_open_filenames(native=True) == ("a", "b")

    monkeypatch.setattr(query.filedialog, "asksaveasfilename", lambda **kw: "")
    assert Querybox.get_save_filename(native=True) is None
    monkeypatch.setattr(query.filedialog, "askdirectory", lambda **kw: "")
    assert Querybox.get_directory(native=True) is None


# --- positioning -----------------------------------------------------------
#
# `_locate` is exercised directly (never via `show()`, which blocks on
# grab_set/wait_window); `build()` is all it needs.

def _built_dialog(root, message="hello", **kwargs):
    dlg = MessageDialog(message, parent=root, **kwargs)
    dlg.build()
    dlg._toplevel.update_idletasks()
    return dlg


def _locate_and_capture(dialog, *args):
    """Run `_locate` and return the (x, y) it applied.

    Record the call instead of reading `geometry()` back afterwards: on X11 the
    readback is not the position that was just requested. A dialog is withdrawn
    while it is positioned, and an unmapped window reports the placement the
    window manager has in mind rather than the request (probed under XWayland:
    a dialog asked for +4460+20 reads back +32+32); once mapped it tracks the
    frame, not the client. What these tests are about is whether `_locate`
    applies coordinates at all.
    """
    import re

    toplevel = dialog._toplevel
    applied = []
    real = toplevel.geometry

    def spy(spec=None):
        # Only a set call carries a spec; a query would append None and break
        # the parse below.
        if spec is not None:
            applied.append(spec)
        return real(spec)

    toplevel.geometry = spy
    try:
        dialog._locate(*args)
    finally:
        del toplevel.geometry
    assert applied, "no geometry was applied"
    m = re.search(r"\+(-?\d+)\+(-?\d+)$", applied[-1])
    assert m is not None, f"no +x+y in the applied geometry {applied[-1]!r}"
    return int(m.group(1)), int(m.group(2))


def test_locate_applies_center_over_parent(root):
    # _locate must apply the centered coordinates rather than leave placement to
    # the window manager, which drops an X11 transient at the virtual-desktop
    # origin -- between monitors on a multi-head setup. The centered result is
    # also clamped onto the monitor, so compare against the clamped value.
    from ttkbootstrap.internal.positioning import center_on_parent, ensure_on_screen

    dlg = _built_dialog(root)
    size = dlg._footprint()
    expected = ensure_on_screen(
        dlg._toplevel, *center_on_parent(dlg._toplevel, root, size=size), size=size
    )
    assert _locate_and_capture(dlg) == expected
    dlg.close()


def test_centering_never_places_a_dialog_past_its_parent_origin(root):
    # Centering a dialog that is wider or taller than its parent yields a
    # negative offset; pinning it to the parent's origin keeps it from hanging
    # off the parent's top-left, which on a multi-head X11 layout puts it on the
    # neighboring screen or in the seam between the two.
    from ttkbootstrap.internal.positioning import _window_size

    # An own parent, not the shared session root, so "smaller than the dialog"
    # holds no matter what earlier tests left the root requesting.
    parent = ttk.Toplevel(root)
    parent.withdraw()
    parent.update_idletasks()
    dlg = _built_dialog(root, message="a message wide enough to outgrow the parent")
    dlg._parent = parent
    assert dlg._toplevel.winfo_reqwidth() > _window_size(parent)[0]

    x, y = dlg._center()
    assert x >= parent.winfo_rootx()
    assert y >= parent.winfo_rooty()
    dlg.close()
    parent.destroy()


def test_locate_without_a_parent_still_applies_a_position(root):
    # parent=None falls back to the dialog's master; it must still be placed.
    dlg = MessageDialog("hello")
    dlg.build()
    x, y = _locate_and_capture(dlg)
    assert x >= 0 and y >= 0
    dlg.close()


def test_locate_applies_an_offset_only_geometry(root):
    # The legacy helper re-applied a width x height along with the offset, so
    # positioning could resize the dialog build() had already sized. Record the
    # geometry calls rather than reading them back: a withdrawn toplevel reports
    # its unmapped 1x1 size, not the size that was requested.
    dlg = _built_dialog(root)
    applied = []
    dlg._toplevel.geometry = lambda spec=None: applied.append(spec)
    dlg._locate()
    assert applied and all(spec.startswith("+") for spec in applied), applied
    del dlg._toplevel.geometry
    dlg.close()


def test_footprint_measures_the_mapped_size_not_the_content(root):
    # A dialog is withdrawn when it is positioned, so it has no realized size,
    # and its requested size ignores the minsize floor build() pins. Centering
    # and clamping against the smaller content size misplaces the dialog by the
    # difference -- for a short message that is over 100px of width.
    dlg = _built_dialog(root, message="ok")
    tl = dlg._toplevel
    min_width, min_height = tl.wm_minsize()
    assert tl.winfo_reqwidth() < min_width, "expected the minsize floor to bind"
    assert dlg._footprint() == (
        max(tl.winfo_reqwidth(), min_width),
        max(tl.winfo_reqheight(), min_height),
    )
    dlg.close()


def test_locate_keeps_the_whole_footprint_on_screen(root):
    # Clamping against the content size reserves too little room and leaves the
    # dialog's right edge -- where the buttons live -- past the screen edge.
    dlg = _built_dialog(root, message="ok")
    right_edge = root.winfo_vrootx() + root.winfo_vrootwidth()
    dlg._center = lambda: (right_edge - 10, 0)  # hard against the right edge
    x, _ = _locate_and_capture(dlg)
    assert x + dlg._footprint()[0] <= right_edge
    dlg.close()
