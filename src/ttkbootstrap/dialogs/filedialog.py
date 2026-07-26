"""Themed, in-library file dialog (X11 default; opt-in elsewhere).

This reproduces the layout of Tk's ``tkfbox.tcl`` chooser with themed ttk
widgets so the dialog follows the active ttkbootstrap theme. On X11 there is no
native chooser and Tk's fallback draws an unstyleable white Canvas panel (its
``::tk::IconList``); this dialog replaces that panel with a themed
``ttk.Treeview`` and drives navigation from Python instead of Tcl. On Windows
and macOS the native OS dialog stays the default, and this dialog is reached via
the ``native=False`` opt-in on the ``Querybox.get_*`` wrappers.

The four modes mirror ``tkinter.filedialog``: open one file, open several, save
as, and choose a directory. Callers reach them through
``Querybox.get_open_filename`` / ``get_open_filenames`` / ``get_save_filename``
/ ``get_directory``, which normalize a cancel to ``None``.

The directory-listing / filetype-filtering / hidden-file logic is pure Python
(module-level functions), kept separate from the widgets so it is unit-testable
without a display.
"""

import fnmatch
import os
import tkinter
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Sequence, Tuple, Union

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.style import Assets
from ttkbootstrap.style.engine import Style
from ttkbootstrap.internal.positioning import (
    center_on_parent,
    center_on_screen,
    ensure_on_screen,
)
from ttkbootstrap.utils import windowing_system
from .message import Messagebox

# Modes.
OPEN = "open"
SAVE = "save"
DIRECTORY = "directory"

# A dialog-only Treeview style so we can give the file listing taller rows
# without disturbing any other treeview in the app.
_ROW_STYLE = "Filedialog.Treeview"

# Logical size of the row icons.
_ICON_SIZE = 16

# Glob patterns that mean "match everything", normalized to a single "*".
_ALL_PATTERNS = frozenset(("*", "*.*", ""))


# ---------------------------------------------------------------------------
# Pure-Python backend (no Tk) — filetype parsing, filtering, listing.
# ---------------------------------------------------------------------------

def _coerce_glob(pattern: str) -> str:
    """Normalize one filetype pattern into an fnmatch glob.

    Mirrors what ``tkinter.filedialog`` accepts: a bare extension (``.txt`` or
    ``txt``) becomes ``*.txt``; ``*``/``*.*``/empty become ``*``; an already-
    globbed pattern (``*.py``) is returned unchanged.
    """
    p = pattern.strip()
    if p in _ALL_PATTERNS:
        return "*"
    if p.startswith("."):
        return "*" + p
    if "*" not in p and "?" not in p and "[" not in p:
        # A bare extension token like "txt" — Tk treats it as a suffix.
        return "*." + p
    return p


def _normalize_filetypes(
    filetypes: Optional[Sequence[Tuple[str, Any]]],
) -> List[Tuple[str, Tuple[str, ...]]]:
    """Normalize the ``filetypes`` contract into ``(label, globs)`` pairs.

    Accepts the stdlib forms — a sequence of ``(label, patterns)`` where
    ``patterns`` is a single glob string, a whitespace/``;``-separated string of
    globs, or a sequence of globs. Returns ``[]`` for a falsy ``filetypes`` (the
    caller supplies the all-files default), so the parsing here matches
    ``tkinter.filedialog`` and existing callers are unaffected by the route.
    """
    result: List[Tuple[str, Tuple[str, ...]]] = []
    for entry in filetypes or ():
        # tkinter accepts a Mac-type third element on macOS -- (label, patterns,
        # mactype) -- so index rather than unpack, which would raise on it.
        label, patterns = entry[0], entry[1]
        if isinstance(patterns, str):
            parts: Sequence[str] = patterns.replace(";", " ").split()
        else:
            parts = list(patterns)
        globs = tuple(_coerce_glob(p) for p in parts) or ("*",)
        result.append((label, globs))
    return result


def _matches(name: str, globs: Sequence[str]) -> bool:
    """Does ``name`` match any glob in ``globs`` (case-insensitive)?"""
    lname = name.lower()
    return any(fnmatch.fnmatch(lname, g.lower()) for g in globs)


def _is_hidden(name: str, path: str) -> bool:
    """Is this entry hidden? Dotfiles everywhere; the hidden attribute on NT."""
    if name.startswith("."):
        return True
    if os.name == "nt":
        try:
            import ctypes

            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            # -1 == INVALID_FILE_ATTRIBUTES; 0x2 == FILE_ATTRIBUTE_HIDDEN.
            if attrs != -1 and attrs & 0x2:
                return True
        except Exception:
            pass
    return False


class _Entry:
    """A directory listing row (name, absolute path, kind, size, mtime)."""

    __slots__ = ("name", "path", "is_dir", "size", "mtime")

    def __init__(self, name: str, path: str, is_dir: bool,
                 size: Optional[int], mtime: Optional[float]) -> None:
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.size = size
        self.mtime = mtime


def _list_directory(
    dirpath: str,
    globs: Sequence[str],
    *,
    show_hidden: bool,
    dirs_only: bool = False,
) -> Tuple[List[_Entry], List[_Entry]]:
    """Return ``(dirs, files)`` for ``dirpath``, each name-sorted.

    ``globs`` filters files only — directories are always listed so the user can
    navigate. Hidden entries are dropped unless ``show_hidden``. In
    ``dirs_only`` mode (directory chooser) files are skipped entirely.
    Unreadable entries are skipped; an unreadable ``dirpath`` yields ``([], [])``.
    """
    dirs: List[_Entry] = []
    files: List[_Entry] = []
    try:
        with os.scandir(dirpath) as it:
            for e in it:
                try:
                    is_dir = e.is_dir()
                except OSError:
                    continue
                if not show_hidden and _is_hidden(e.name, e.path):
                    continue
                if is_dir:
                    dirs.append(_Entry(e.name, e.path, True, None, _safe_mtime(e)))
                elif not dirs_only and _matches(e.name, globs):
                    size, mtime = _safe_stat(e)
                    files.append(_Entry(e.name, e.path, False, size, mtime))
    except OSError:
        return [], []
    dirs.sort(key=lambda x: x.name.lower())
    files.sort(key=lambda x: x.name.lower())
    return dirs, files


def _safe_stat(entry: "os.DirEntry") -> Tuple[Optional[int], Optional[float]]:
    try:
        st = entry.stat()
        return st.st_size, st.st_mtime
    except OSError:
        return None, None


def _safe_mtime(entry: "os.DirEntry") -> Optional[float]:
    try:
        return entry.stat().st_mtime
    except OSError:
        return None


def _ancestors(path: str) -> List[str]:
    """Every path from ``path`` up to the filesystem root, nearest first."""
    parts: List[str] = []
    current = os.path.abspath(path)
    while True:
        parts.append(current)
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return parts


def _format_size(nbytes: Optional[int]) -> str:
    """Human-readable file size (``''`` for directories / unknown)."""
    if nbytes is None:
        return ""
    size = float(nbytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{int(size)} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return ""  # unreachable; keeps the type checker happy


def _format_mtime(ts: Optional[float]) -> str:
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except (OSError, ValueError, OverflowError):
        return ""


# ---------------------------------------------------------------------------
# The dialog.
# ---------------------------------------------------------------------------

class FileDialog:
    """A themed file chooser reproducing ``tkfbox.tcl``'s layout.

    Not a public widget — construct it through the ``Querybox.get_*`` facade,
    which selects native-vs-themed per platform and normalizes a cancel to
    ``None``. Call :meth:`show` (which returns the result and also sets
    :attr:`result`).

    Result by mode: a path ``str`` for open-single / save / directory, a
    ``tuple[str, ...]`` for open-multiple, and ``None`` on cancel.
    """

    def __init__(
        self,
        parent: Optional[tkinter.Misc] = None,
        *,
        title: Optional[str] = None,
        mode: str = OPEN,
        multiple: bool = False,
        filetypes: Optional[Sequence[Tuple[str, Any]]] = None,
        initialdir: Optional[str] = None,
        initialfile: Optional[str] = None,
        defaultextension: str = "",
    ) -> None:
        self._parent = parent
        self._mode = mode
        self._multiple = bool(multiple) and mode == OPEN
        self._filetypes = _normalize_filetypes(filetypes)
        self._defaultext = defaultextension
        self._initialfile = initialfile or ""
        self._cwd = os.path.abspath(initialdir or os.getcwd())
        self._title = title or _default_title(mode)
        self._result: Union[str, Tuple[str, ...], None] = None

        # Built in _build(); the current filetype's globs default to all-files.
        self._current_globs: Tuple[str, ...] = ("*",)
        self._rows: dict = {}
        self._toplevel: Optional[tkinter.Toplevel] = None

    # -- public ------------------------------------------------------------

    def show(
        self, position: Optional[Tuple[int, int]] = None
    ) -> Union[str, Tuple[str, ...], None]:
        """Build, show modally, and return the result (also on :attr:`result`)."""
        self._build()
        self._navigate(self._cwd)
        self._locate(position)
        self._toplevel.deiconify()
        self._name_entry.focus_set()
        self._toplevel.grab_set()
        self._toplevel.wait_window()
        return self._result

    @property
    def result(self) -> Union[str, Tuple[str, ...], None]:
        return self._result

    # -- construction ------------------------------------------------------

    def _build(self) -> None:
        winsys = windowing_system(self._parent)
        kwargs: dict = dict(
            transient=self._parent,
            title=self._title,
            iconify=True,
        )
        if winsys != "win32":
            kwargs["window_type"] = "dialog"
        self._toplevel = ttk.Toplevel(**kwargs)
        self._toplevel.withdraw()  # reset the iconify state
        self._toplevel.protocol("WM_DELETE_WINDOW", self._cancel)
        self._toplevel.bind("<Escape>", lambda _: self._cancel())

        self._path_var = ttk.StringVar(master=self._toplevel)
        self._name_var = ttk.StringVar(master=self._toplevel, value=self._initialfile)
        self._hidden_var = ttk.BooleanVar(master=self._toplevel, value=False)
        self._type_var = ttk.StringVar(master=self._toplevel)

        style = Style.get_instance()
        assets = Assets(style)
        colors = style.colors
        # Row icons come in two variants — a normal one colored to read on the
        # field background, and a "selected" one colored with `selectfg`. The
        # selection background is a neutral gray that a static accent color can
        # blend into (in a light theme `secondary` *is* the selection gray), so
        # we swap the icon color with the selection state — see _update_row_icons.
        self._folder_img = assets.icon("folder-fill", _ICON_SIZE, colors.warning)
        self._file_img = assets.icon(
            "file-earmark-text-fill", _ICON_SIZE, colors.get("secondary"))
        self._folder_img_sel = assets.icon("folder-fill", _ICON_SIZE, colors.selectfg)
        self._file_img_sel = assets.icon(
            "file-earmark-text-fill", _ICON_SIZE, colors.selectfg)
        self._up_img = assets.icon("arrow-90deg-up", _ICON_SIZE, colors.fg)

        container = ttk.Frame(self._toplevel, padding=8)
        container.pack(fill=BOTH, expand=YES)
        self._build_topbar(container)
        self._build_listing(container)
        self._build_form(container)

        # Size from content, never a hardcoded height: platform font/padding
        # differences (larger on X11) otherwise clip the bottom row. Open at a
        # comfortable default but never smaller than the content needs, and don't
        # let the window be shrunk to clip it.
        self._toplevel.update_idletasks()
        req_w = self._toplevel.winfo_reqwidth()
        req_h = self._toplevel.winfo_reqheight()
        self._toplevel.geometry(f"{max(640, req_w)}x{max(480, req_h)}")
        self._toplevel.minsize(req_w, req_h)

    def _build_topbar(self, master: tkinter.Misc) -> None:
        bar = ttk.Frame(master)
        bar.pack(side=TOP, fill=X, pady=(0, 6))
        ttk.Label(bar, text=MessageCatalog.translate("Directory:")).pack(
            side=LEFT, padx=(0, 6))
        up = ttk.Button(bar, image=self._up_img, command=self._go_up)
        up.pack(side=RIGHT, padx=(6, 0))
        self._dir_mb = ttk.Menubutton(bar, textvariable=self._path_var)
        self._dir_menu = ttk.Menu(self._dir_mb, tearoff=0)
        self._dir_mb.configure(menu=self._dir_menu)
        self._dir_mb.pack(side=LEFT, fill=X, expand=YES)

    def _build_listing(self, master: tkinter.Misc) -> None:
        frame = ttk.Frame(master)
        frame.pack(side=TOP, fill=BOTH, expand=YES)
        select = EXTENDED if self._multiple else BROWSE
        tree = ttk.Treeview(
            frame, columns=("size", "modified"), selectmode=select,
            show=(TREE, HEADINGS))
        # Give the listing taller rows than the default (flush) treeview so the
        # icons sit comfortably. Scoped to a dialog-only style (inherits the
        # themed Treeview colors) so no other treeview is affected. Row height is
        # DPI-physical — the icon size and font linespace already are.
        style = Style.get_instance()
        icon_h = style.scaling.image_size(_ICON_SIZE)[1]
        try:
            linespace = int(tree.tk.call("font", "metrics", "TkDefaultFont", "-linespace"))
        except tkinter.TclError:
            linespace = icon_h
        # Framework code writes via the internal _build_configure, not the public
        # Style.configure -- rowheight is a durable option, and the public path
        # would capture this as a fake user override (replayed on theme switch).
        style._build_configure(
            _ROW_STYLE, rowheight=max(icon_h, linespace) + round(0.7 * linespace))
        tree.configure(style=_ROW_STYLE)
        tree.heading("#0", text=MessageCatalog.translate("Name"), anchor=W)
        tree.heading("size", text=MessageCatalog.translate("Size"), anchor=W)
        tree.heading("modified", text=MessageCatalog.translate("Modified"), anchor=W)
        tree.column("#0", width=320, stretch=True)
        tree.column("size", width=90, stretch=False, anchor=E)
        tree.column("modified", width=140, stretch=False)
        vsb = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=RIGHT, fill=Y)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        tree.bind("<<TreeviewSelect>>", self._on_select)
        tree.bind("<Double-1>", self._on_activate)
        tree.bind("<Return>", self._on_activate)
        self._tree = tree

    def _build_form(self, master: tkinter.Misc) -> None:
        form = ttk.Frame(master)
        form.pack(side=BOTTOM, fill=X, pady=(6, 0))
        form.columnconfigure(1, weight=1)

        name_label = (MessageCatalog.translate("Selection:")
                      if self._mode == DIRECTORY
                      else MessageCatalog.translate("File name:"))
        ttk.Label(form, text=name_label, anchor=E).grid(
            row=0, column=0, sticky=EW, padx=(0, 6), pady=3)
        self._name_entry = ttk.Entry(form, textvariable=self._name_var)
        self._name_entry.grid(row=0, column=1, sticky=EW, pady=3)
        self._name_entry.bind("<Return>", lambda _: self._on_ok())
        ok_text = MessageCatalog.translate("OK")
        ttk.Button(form, text=ok_text, bootstyle=PRIMARY, command=self._on_ok).grid(
            row=0, column=2, sticky=EW, padx=(6, 0), pady=3)

        if self._mode != DIRECTORY:
            ttk.Label(form, text=MessageCatalog.translate("Files of type:"),
                      anchor=E).grid(row=1, column=0, sticky=EW, padx=(0, 6), pady=3)
            type_mb = ttk.Menubutton(form, textvariable=self._type_var)
            type_menu = ttk.Menu(type_mb, tearoff=0)
            type_mb.configure(menu=type_menu)
            type_mb.grid(row=1, column=1, sticky=EW, pady=3)
            self._build_type_menu(type_menu)

        cancel_text = MessageCatalog.translate("Cancel")
        ttk.Button(form, text=cancel_text, command=self._cancel).grid(
            row=1, column=2, sticky=EW, padx=(6, 0), pady=3)

        ttk.Checkbutton(
            form,
            text=MessageCatalog.translate("Show hidden files"),
            variable=self._hidden_var,
            command=self._refresh,
        ).grid(row=2, column=0, columnspan=2, sticky=W, pady=(6, 0))

    def _build_type_menu(self, menu: tkinter.Menu) -> None:
        types = self._filetypes or [
            (MessageCatalog.translate("All Files"), ("*",))]
        for label, globs in types:
            display = _type_label(label, globs)
            menu.add_command(
                label=display,
                command=lambda g=globs, d=display: self._set_filetype(g, d))
        first_label, first_globs = types[0]
        self._current_globs = first_globs
        self._type_var.set(_type_label(first_label, first_globs))

    # -- navigation & listing ---------------------------------------------

    def _navigate(self, path: str) -> None:
        self._cwd = os.path.abspath(path)
        self._path_var.set(self._cwd)
        self._rebuild_dir_menu()
        self._refresh()

    def _go_up(self) -> None:
        self._navigate(os.path.dirname(self._cwd))

    def _rebuild_dir_menu(self) -> None:
        self._dir_menu.delete(0, END)
        for anc in _ancestors(self._cwd):
            self._dir_menu.add_command(
                label=anc, command=lambda p=anc: self._navigate(p))

    def _refresh(self) -> None:
        tree = self._tree
        tree.delete(*tree.get_children())
        self._rows = {}
        dirs, files = _list_directory(
            self._cwd,
            self._current_globs,
            show_hidden=self._hidden_var.get(),
            dirs_only=self._mode == DIRECTORY,
        )
        for e in dirs:
            iid = tree.insert(
                "", END, text=f" {e.name}", image=self._folder_img,
                values=("", _format_mtime(e.mtime)))
            self._rows[iid] = e
        for e in files:
            iid = tree.insert(
                "", END, text=f" {e.name}", image=self._file_img,
                values=(_format_size(e.size), _format_mtime(e.mtime)))
            self._rows[iid] = e

    def _set_filetype(self, globs: Tuple[str, ...], display: str) -> None:
        self._current_globs = globs
        self._type_var.set(display)
        self._refresh()

    # -- selection handlers ------------------------------------------------

    def _selected_entries(self) -> List[_Entry]:
        return [self._rows[iid] for iid in self._tree.selection()
                if iid in self._rows]

    def _update_row_icons(self) -> None:
        """Recolor row icons by selection state.

        A static icon color can vanish into the neutral selection background, so
        selected rows use the `selectfg`-colored variant (which always contrasts
        the selection) and the rest keep the field-background variant.
        """
        selected = set(self._tree.selection())
        for iid, entry in self._rows.items():
            if iid in selected:
                img = self._folder_img_sel if entry.is_dir else self._file_img_sel
            else:
                img = self._folder_img if entry.is_dir else self._file_img
            self._tree.item(iid, image=img)

    def _on_select(self, event: Any = None) -> None:
        self._update_row_icons()
        sel = self._selected_entries()
        if not sel:
            return
        if self._mode == DIRECTORY:
            self._name_var.set(sel[0].path)
            return
        files = [e for e in sel if not e.is_dir]
        if not files:
            return
        if self._multiple and len(files) > 1:
            self._name_var.set(" ".join(_quote(e.name) for e in files))
        else:
            self._name_var.set(files[0].name)

    def _on_activate(self, event: Any = None) -> None:
        sel = self._selected_entries()
        if not sel:
            return
        entry = sel[0]
        if entry.is_dir:
            self._navigate(entry.path)
        elif self._mode != DIRECTORY:
            self._on_ok()

    # -- accept / cancel ---------------------------------------------------

    def _on_ok(self) -> None:
        if self._mode == DIRECTORY:
            sel = self._selected_entries()
            self._accept(sel[0].path if sel else self._cwd)
            return

        text = self._name_var.get().strip()
        if text and not (self._multiple and " " in text):
            candidate = text if os.path.isabs(text) else os.path.join(self._cwd, text)
            candidate = os.path.abspath(candidate)
            if os.path.isdir(candidate):
                self._navigate(candidate)
                return
            if self._mode == SAVE:
                candidate = self._apply_default_ext(candidate)
                if os.path.exists(candidate) and not self._confirm_overwrite(candidate):
                    return
                self._accept(candidate)
                return
            # OPEN with a typed name.
            if self._multiple:
                self._accept((candidate,))
                return
            if os.path.exists(candidate):
                self._accept(candidate)
                return
            self._toplevel.bell()
            return

        # No usable typed text — fall back to the tree selection.
        files = [e for e in self._selected_entries() if not e.is_dir]
        if not files:
            self._toplevel.bell()
            return
        if self._multiple:
            self._accept(tuple(e.path for e in files))
        else:
            self._accept(files[0].path)

    def _apply_default_ext(self, path: str) -> str:
        if self._defaultext and not os.path.splitext(path)[1]:
            ext = self._defaultext
            if not ext.startswith("."):
                ext = "." + ext
            return path + ext
        return path

    def _confirm_overwrite(self, path: str) -> bool:
        name = os.path.basename(path)
        prompt = MessageCatalog.translate("File already exists. Overwrite?")
        answer = Messagebox.yesno(f"{name}\n\n{prompt}", parent=self._toplevel)
        # Messagebox returns the (possibly localized) button text; compare against
        # the same translation rather than a raw "Yes" so non-English locales work.
        return answer == MessageCatalog.translate("Yes")

    def _accept(self, result: Union[str, Tuple[str, ...]]) -> None:
        # Match `tkinter.filedialog`, which returns forward-slash paths on every
        # platform (including Windows) — so callers see the same string whichever
        # dialog drew it.
        if isinstance(result, tuple):
            self._result = tuple(_to_tk_path(p) for p in result)
        else:
            self._result = _to_tk_path(result)
        self._close()

    def _cancel(self) -> None:
        self._result = None
        self._close()

    def _close(self) -> None:
        tl = self._toplevel
        if tl is None:
            return
        try:
            if tl.winfo_exists():
                tl.grab_release()
                tl.destroy()
        except tkinter.TclError:
            pass

    # -- positioning -------------------------------------------------------

    def _locate(self, position: Optional[Tuple[int, int]]) -> None:
        tl = self._toplevel
        tl.update_idletasks()
        if position is not None:
            try:
                x, y = ensure_on_screen(tl, *position)
            except Exception:
                x, y = self._center()
        else:
            x, y = self._center()
        # Apply the computed coordinates. Relying on the window manager to place
        # a transient dialog works on Windows/macOS but not on X11, where an
        # unplaced window lands at the virtual-desktop origin — between monitors
        # on a multi-head setup.
        tl.geometry(f"+{int(x)}+{int(y)}")

    def _center(self) -> Tuple[int, int]:
        """Coordinates that center the dialog over its parent (or the screen)."""
        if self._parent is not None:
            return center_on_parent(self._toplevel, self._parent)
        return center_on_screen(self._toplevel)


def _default_title(mode: str) -> str:
    if mode == DIRECTORY:
        return MessageCatalog.translate("Select Directory")
    if mode == SAVE:
        return MessageCatalog.translate("Save As")
    return MessageCatalog.translate("Open")


def _type_label(label: str, globs: Sequence[str]) -> str:
    """``"Text Files (*.txt)"`` — the filetype label with its patterns shown."""
    if not globs or tuple(globs) == ("*",):
        return f"{label} (*)"
    return f"{label} ({' '.join(globs)})"


def _quote(name: str) -> str:
    return f'"{name}"' if " " in name else name


def _to_tk_path(path: str) -> str:
    """Forward-slash separators, matching what ``tkinter.filedialog`` returns.

    Tk normalizes paths to ``/`` on every platform; ``Path.as_posix()`` does the
    same (a no-op off Windows), handling drive letters and mixed separators.
    """
    return Path(path).as_posix()
