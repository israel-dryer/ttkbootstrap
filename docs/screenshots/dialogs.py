"""Screenshot scenes for docs/user-guide/feature-guides/dialogs.rst."""

import tkinter
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import (
    ColorChooserDialog,
    DatePickerDialog,
    MessageDialog,
)


def _target_child(app):
    """Raise the dialog Toplevel above the -topmost app and target it."""
    tops = [w for w in app.winfo_children() if isinstance(w, tkinter.Toplevel)]
    if tops:
        tops[0].attributes("-topmost", True)
        tops[0].lift()
        app._capture_target = tops[0]


def message():
    app = ttk.App(title="App")
    ttk.Label(app, text="Editor", padding=20).pack()
    dialog = MessageDialog(
        "Apply changes to all items, or just this one?",
        title="Apply changes",
        buttons=["Cancel:secondary", "This one:primary", "All:success"],
        parent=app,
    )
    dialog.show(wait_for_result=False)   # non-modal, so the capture can proceed
    app.after(250, lambda: _target_child(app))
    app.mainloop()


def date():
    # The calendar popover dismisses on focus move, so use the parent-capture:
    # announce the (tall) window rect, open the calendar (it drops within), and
    # the harness parent grabs the region while it's up.
    from ttkbootstrap.widgets import DateEntry
    app = ttk.App(title="Due date", size=(300, 340))
    frm = ttk.Frame(app, padding=20)
    frm.pack(anchor="n", fill="x")
    picker = DateEntry(frm)
    picker.pack(anchor="w")

    def open_cal():
        app.capture_via_parent()
        picker.button.invoke()   # opens the modal calendar (drops below the field)

    app.after(500, open_cal)
    app.mainloop()


def color():
    app = ttk.App(title="App")
    ttk.Label(app, text="Editor", padding=20).pack()
    dlg = ColorChooserDialog(parent=app, initialcolor="#3498db")
    dlg.show(wait_for_result=False)

    def wire():
        tops = [w for w in app.winfo_children() if isinstance(w, tkinter.Toplevel)]
        if tops:
            tops[0].geometry("+80+40")   # fully on-screen (it centers on the tiny app -> clips)
            tops[0].attributes("-topmost", True)
            tops[0].lift()
            tops[0].update_idletasks()
            app._capture_target = tops[0]

    app.after(300, wire)
    app.mainloop()


def custom():
    app = ttk.App(title="Editor")
    ttk.Label(app, text="Editor", padding=20).pack()
    win = ttk.Toplevel(master=app, title="New contact")
    win.minsize(330, 1)   # comfortable width; height auto-sizes -> buttons at the bottom
    frm = ttk.Frame(win, padding=20)
    frm.pack(fill="both", expand=True)
    frm.columnconfigure(1, weight=1)
    ttk.Label(frm, text="Name").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)
    ttk.Entry(frm).grid(row=0, column=1, sticky="ew", pady=6)
    ttk.Label(frm, text="Email").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)
    ttk.Entry(frm).grid(row=1, column=1, sticky="ew", pady=6)
    btns = ttk.Frame(frm)
    btns.grid(row=2, column=0, columnspan=2, sticky="e", pady=(14, 0))
    ttk.Button(btns, text="Cancel", bootstyle="secondary").pack(side="left", padx=(0, 6))
    ttk.Button(btns, text="OK", bootstyle="primary").pack(side="left")

    def _raise():
        win.attributes("-topmost", True)
        win.lift()

    app.after(200, _raise)
    app._capture_target = win
    app.mainloop()


def file():
    # The themed file dialog (what X11 shows by default; native=False forces it
    # elsewhere). Build it non-modally against a controlled temp directory so the
    # listing is clean and reproducible, select a file so the selection styling +
    # filename field read, and capture the toplevel.
    import os
    import tempfile
    from ttkbootstrap.dialogs.filedialog import FileDialog

    app = ttk.App(title="App")
    ttk.Label(app, text="Editor", padding=20).pack()

    folder = tempfile.mkdtemp(prefix="ttk_filedialog_docs_")
    for name in ("Documents", "Downloads", "Projects"):
        os.makedirs(os.path.join(folder, name), exist_ok=True)
    for name in ("meeting-notes.txt", "README.txt", "budget.csv", "todo.md"):
        with open(os.path.join(folder, name), "w") as handle:
            handle.write("sample")

    dlg = FileDialog(app, mode="open", initialdir=folder,
                     filetypes=[("All files", "*.*"), ("Text files", "*.txt")])
    dlg._build()
    dlg._navigate(dlg._cwd)
    dlg._path_var.set("My Documents")   # clean directory label for the shot
    for iid, entry in dlg._rows.items():
        if entry.name == "README.txt":
            dlg._tree.selection_set(iid)
            dlg._on_select()
            break

    win = dlg._toplevel
    win.geometry("+80+40")
    win.deiconify()

    def wire():
        win.attributes("-topmost", True)
        win.lift()
        win.update_idletasks()
        app._capture_target = win

    app.after(300, wire)
    app.mainloop()


SCENES = {
    "message": message,
    "date": date,
    "color": color,
    "custom": custom,
    "file": file,
}
