"""Tests for the themed in-library file dialog (`dialogs/filedialog.py`) and its
`Querybox.get_*` routing.

Two layers:

* **Backend** — the pure-Python listing/filter/parse helpers, exercised without
  a Tk root (no `root` fixture).
* **Dialog** — build the dialog against the shared root and drive its internals
  directly (select rows, hit OK/Cancel, navigate). `show()` is never called
  because its `wait_window()` would block the headless suite; the accept/cancel
  logic it wraps is what these assert.
"""

import os

import pytest

from ttkbootstrap.dialogs.filedialog import FileDialog
from ttkbootstrap.dialogs import filedialog as fd
from ttkbootstrap.dialogs.query import Querybox
from ttkbootstrap.localization import MessageCatalog


# ---------------------------------------------------------------------------
# Backend — pure Python, no root.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("pattern, expected", [
    (".txt", "*.txt"),
    ("txt", "*.txt"),
    ("*.py", "*.py"),
    ("*.*", "*"),
    ("*", "*"),
    ("", "*"),
    ("  .md  ", "*.md"),
])
def test_coerce_glob(pattern, expected):
    assert fd._coerce_glob(pattern) == expected


def test_normalize_filetypes_forms():
    # string, tuple-of-globs, and the all-files entry all normalize.
    got = fd._normalize_filetypes([
        ("Text", "*.txt"),
        ("Source", ("*.py", "*.pyw")),
        ("Semi", "*.a;*.b"),
        ("All", "*.*"),
    ])
    assert got == [
        ("Text", ("*.txt",)),
        ("Source", ("*.py", "*.pyw")),
        ("Semi", ("*.a", "*.b")),
        ("All", ("*",)),
    ]


def test_normalize_filetypes_empty():
    assert fd._normalize_filetypes(None) == []
    assert fd._normalize_filetypes([]) == []


@pytest.mark.parametrize("name, globs, expected", [
    ("a.TXT", ("*.txt",), True),      # case-insensitive
    ("a.py", ("*.txt",), False),
    ("a.py", ("*.txt", "*.py"), True),
    ("anything", ("*",), True),
])
def test_matches(name, globs, expected):
    assert fd._matches(name, globs) is expected


def test_is_hidden_dotfile():
    assert fd._is_hidden(".bashrc", "/home/x/.bashrc") is True
    assert fd._is_hidden("readme.txt", "/home/x/readme.txt") is False


@pytest.mark.parametrize("nbytes, expected", [
    (None, ""),
    (0, "0 B"),
    (1023, "1023 B"),
    (2048, "2.0 KB"),
    (5 * 1024 * 1024, "5.0 MB"),
])
def test_format_size(nbytes, expected):
    assert fd._format_size(nbytes) == expected


def test_list_directory_filters_and_sorts(tmp_path):
    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "keep.py").write_text("x")
    (tmp_path / ".hidden.txt").write_text("h")
    (tmp_path / "sub").mkdir()
    (tmp_path / ".dotdir").mkdir()

    dirs, files = fd._list_directory(str(tmp_path), ("*.txt",), show_hidden=False)
    assert [d.name for d in dirs] == ["sub"]              # dotdir filtered
    assert [f.name for f in files] == ["a.txt", "b.txt"]  # keep.py filtered, sorted

    # hidden shown
    dirs_h, files_h = fd._list_directory(str(tmp_path), ("*.txt",), show_hidden=True)
    assert ".dotdir" in [d.name for d in dirs_h]
    assert ".hidden.txt" in [f.name for f in files_h]

    # dirs_only skips files entirely (directory-chooser mode)
    dirs_o, files_o = fd._list_directory(
        str(tmp_path), ("*",), show_hidden=False, dirs_only=True)
    assert [d.name for d in dirs_o] == ["sub"]
    assert files_o == []


def test_list_directory_unreadable_returns_empty():
    dirs, files = fd._list_directory(
        os.path.join(os.sep, "no", "such", "path", "xyz"), ("*",), show_hidden=False)
    assert (dirs, files) == ([], [])


def test_ancestors_reaches_root():
    anc = fd._ancestors(os.getcwd())
    assert anc[0] == os.path.abspath(os.getcwd())
    # last element is its own parent (filesystem root / drive root)
    assert os.path.dirname(anc[-1]) == anc[-1]


def test_type_label():
    assert fd._type_label("All", ("*",)) == "All (*)"
    assert fd._type_label("Text", ("*.txt",)) == "Text (*.txt)"
    assert fd._type_label("Src", ("*.py", "*.pyw")) == "Src (*.py *.pyw)"


# ---------------------------------------------------------------------------
# Routing — Querybox selects native vs themed.
# ---------------------------------------------------------------------------

def test_use_native_filedialog_explicit_wins():
    # An explicit value always wins, regardless of platform.
    assert Querybox._use_native_filedialog(True, object()) is True
    assert Querybox._use_native_filedialog(False, object()) is False


@pytest.mark.parametrize("winsys, native", [
    ("x11", False),      # themed on Linux/Unix (Tk's fallback ignores the theme)
    ("win32", True),     # native OS chooser on Windows
    ("aqua", True),      # native OS chooser on macOS
])
def test_use_native_filedialog_none_is_platform_aware(monkeypatch, winsys, native):
    monkeypatch.setattr("ttkbootstrap.dialogs.query.windowing_system",
                        lambda w: winsys)
    assert Querybox._use_native_filedialog(None, object()) is native


def test_use_native_filedialog_no_root_defaults_native(monkeypatch):
    # With no interpreter to query, native is the safe default.
    monkeypatch.setattr("tkinter._get_default_root", lambda: None)
    assert Querybox._use_native_filedialog(None) is True


def test_native_false_routes_to_themed(monkeypatch):
    captured = {}

    class _Fake:
        def __init__(self, parent, **kwargs):
            captured["parent"] = parent
            captured["kwargs"] = kwargs

        def show(self):
            return "/picked/path"

    monkeypatch.setattr("ttkbootstrap.dialogs.filedialog.FileDialog", _Fake)
    out = Querybox.get_open_filename(
        native=False, title="Pick", filetypes=[("Text", "*.txt")],
        initialdir="/tmp")
    assert out == "/picked/path"
    assert captured["kwargs"]["mode"] == "open"
    assert captured["kwargs"]["multiple"] is False
    assert captured["kwargs"]["title"] == "Pick"
    assert captured["kwargs"]["filetypes"] == [("Text", "*.txt")]


def test_native_false_routes_multiple(monkeypatch):
    seen = {}

    class _Fake:
        def __init__(self, parent, **kwargs):
            seen.update(kwargs)

        def show(self):
            return ("/a", "/b")

    monkeypatch.setattr("ttkbootstrap.dialogs.filedialog.FileDialog", _Fake)
    out = Querybox.get_open_filenames(native=False)
    assert out == ("/a", "/b")
    assert seen["mode"] == "open" and seen["multiple"] is True


# ---------------------------------------------------------------------------
# Dialog — build against the shared root and drive the internals.
# ---------------------------------------------------------------------------

def _iid_for(dlg, name):
    for iid, entry in dlg._rows.items():
        if entry.name == name:
            return iid
    raise AssertionError(f"{name!r} not listed; have {[e.name for e in dlg._rows.values()]}")


def _build(root, tmp_path, **kwargs):
    dlg = FileDialog(root, initialdir=str(tmp_path), **kwargs)
    dlg._build()
    dlg._navigate(dlg._cwd)
    return dlg


def test_open_selecting_a_file_accepts_its_path(root, tmp_path):
    target = tmp_path / "report.txt"
    target.write_text("x")
    (tmp_path / "other.py").write_text("y")

    dlg = _build(root, tmp_path, mode="open",
                 filetypes=[("Text", "*.txt")])
    # only the .txt matched the active filter
    assert set(e.name for e in dlg._rows.values()) == {"report.txt"}

    dlg._tree.selection_set(_iid_for(dlg, "report.txt"))
    dlg._on_select()
    assert dlg._name_var.get() == "report.txt"
    dlg._on_ok()
    assert dlg._result == target.as_posix()


def test_open_double_click_directory_navigates(root, tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "inner.txt").write_text("z")

    dlg = _build(root, tmp_path, mode="open")
    dlg._tree.selection_set(_iid_for(dlg, "sub"))
    dlg._on_activate()  # double-click a directory descends into it
    assert dlg._cwd == str(tmp_path / "sub")
    assert "inner.txt" in [e.name for e in dlg._rows.values()]
    assert dlg._result is None  # navigating is not accepting


def test_open_nonexistent_typed_name_does_not_accept(root, tmp_path):
    dlg = _build(root, tmp_path, mode="open")
    dlg._name_var.set("ghost.txt")
    dlg._on_ok()
    assert dlg._result is None
    assert dlg._toplevel.winfo_exists()  # dialog stayed open


def test_go_up_navigates_to_parent(root, tmp_path):
    (tmp_path / "sub").mkdir()
    dlg = _build(root, tmp_path / "sub", mode="open")
    dlg._go_up()
    assert dlg._cwd == str(tmp_path)


def test_save_new_name_accepts_joined_path(root, tmp_path):
    dlg = _build(root, tmp_path, mode="save")
    dlg._name_var.set("newfile.txt")
    dlg._on_ok()
    assert dlg._result == (tmp_path / "newfile.txt").as_posix()


def test_save_applies_default_extension(root, tmp_path):
    dlg = _build(root, tmp_path, mode="save", defaultextension=".txt")
    dlg._name_var.set("noext")
    dlg._on_ok()
    assert dlg._result == (tmp_path / "noext.txt").as_posix()


def test_save_overwrite_confirmed(root, tmp_path, monkeypatch):
    existing = tmp_path / "dup.txt"
    existing.write_text("old")
    yes = MessageCatalog.translate("Yes")
    monkeypatch.setattr(
        "ttkbootstrap.dialogs.filedialog.Messagebox.yesno",
        staticmethod(lambda *a, **k: yes))
    dlg = _build(root, tmp_path, mode="save")
    dlg._name_var.set("dup.txt")
    dlg._on_ok()
    assert dlg._result == existing.as_posix()


def test_save_overwrite_declined_stays_open(root, tmp_path, monkeypatch):
    (tmp_path / "dup.txt").write_text("old")
    no = MessageCatalog.translate("No")
    monkeypatch.setattr(
        "ttkbootstrap.dialogs.filedialog.Messagebox.yesno",
        staticmethod(lambda *a, **k: no))
    dlg = _build(root, tmp_path, mode="save")
    dlg._name_var.set("dup.txt")
    dlg._on_ok()
    assert dlg._result is None
    assert dlg._toplevel.winfo_exists()


def test_directory_mode_lists_only_dirs(root, tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "file.txt").write_text("x")
    dlg = _build(root, tmp_path, mode="directory")
    assert set(e.name for e in dlg._rows.values()) == {"sub"}


def test_directory_selecting_returns_dir(root, tmp_path):
    (tmp_path / "sub").mkdir()
    dlg = _build(root, tmp_path, mode="directory")
    dlg._tree.selection_set(_iid_for(dlg, "sub"))
    dlg._on_select()
    dlg._on_ok()
    assert dlg._result == (tmp_path / "sub").as_posix()


def test_directory_no_selection_returns_cwd(root, tmp_path):
    dlg = _build(root, tmp_path, mode="directory")
    dlg._on_ok()
    assert dlg._result == tmp_path.as_posix()


def test_cancel_returns_none(root, tmp_path):
    (tmp_path / "a.txt").write_text("x")
    dlg = _build(root, tmp_path, mode="open")
    dlg._tree.selection_set(_iid_for(dlg, "a.txt"))
    dlg._on_select()
    dlg._cancel()
    assert dlg._result is None


def test_show_hidden_toggle_relists(root, tmp_path):
    (tmp_path / "visible.txt").write_text("v")
    (tmp_path / ".secret.txt").write_text("s")
    dlg = _build(root, tmp_path, mode="open")
    assert ".secret.txt" not in [e.name for e in dlg._rows.values()]
    dlg._hidden_var.set(True)
    dlg._refresh()
    assert ".secret.txt" in [e.name for e in dlg._rows.values()]


def test_result_uses_forward_slashes_like_native(root, tmp_path):
    # tkinter.filedialog returns forward-slash paths on every platform; the
    # themed dialog must match so callers are agnostic to which drew it.
    target = tmp_path / "doc.txt"
    target.write_text("x")
    dlg = _build(root, tmp_path, mode="open")
    dlg._tree.selection_set(_iid_for(dlg, "doc.txt"))
    dlg._on_select()
    dlg._on_ok()
    assert "\\" not in dlg._result
    assert dlg._result == target.as_posix()


def test_row_icon_swaps_on_selection(root, tmp_path):
    # A selected row uses the selectfg-colored icon variant so it never blends
    # into the neutral selection background; deselected rows revert.
    (tmp_path / "a.txt").write_text("a")
    dlg = _build(root, tmp_path, mode="open")
    iid = _iid_for(dlg, "a.txt")

    assert dlg._tree.item(iid, "image")[0] == str(dlg._file_img)
    dlg._tree.selection_set(iid)
    dlg._on_select()
    assert dlg._tree.item(iid, "image")[0] == str(dlg._file_img_sel)
    dlg._tree.selection_remove(iid)
    dlg._on_select()
    assert dlg._tree.item(iid, "image")[0] == str(dlg._file_img)


def test_listing_uses_taller_scoped_rowheight(root, tmp_path):
    # The dialog's rows are taller than the default flush treeview, via a
    # dialog-scoped style that leaves the global Treeview untouched.
    dlg = _build(root, tmp_path, mode="open")
    style = root.style
    scoped = int(style.lookup("Filedialog.Treeview", "rowheight"))
    base = int(style.lookup("Treeview", "rowheight"))
    assert scoped > base


def test_multiple_open_returns_tuple(root, tmp_path):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    dlg = _build(root, tmp_path, mode="open", multiple=True)
    dlg._tree.selection_set(_iid_for(dlg, "a.txt"), _iid_for(dlg, "b.txt"))
    dlg._on_select()
    dlg._on_ok()
    assert dlg._result == ((tmp_path / "a.txt").as_posix(), (tmp_path / "b.txt").as_posix())