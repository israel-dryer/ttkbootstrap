"""Screenshot scenes for docs/user-guide/feature-guides/menus.rst.

A posted native menu doesn't block the Tcl loop on Windows but dismisses when
focus moves, so these use the harness parent-capture: announce the window rect
via ``capture_via_parent()``, post the menu (drawn inside the rect), and let the
harness parent grab the region while the child holds it.
"""

import ttkbootstrap as ttk


def file_menu():
    app = ttk.App(title="Editor", size=(360, 280))
    menubar = ttk.Menu(app)
    app.config(menu=menubar)

    file_m = ttk.Menu(menubar, tearoff=False)
    file_m.add_command(label="New")
    file_m.add_command(label="Open…")
    file_m.add_separator()
    file_m.add_command(label="Exit")
    menubar.add_cascade(label="File", menu=file_m)

    edit_m = ttk.Menu(menubar, tearoff=False)
    for item in ("Cut", "Copy", "Paste"):
        edit_m.add_command(label=item)
    menubar.add_cascade(label="Edit", menu=edit_m)

    ttk.Label(app, text="Document", padding=20).pack(anchor="nw")

    def post():
        app.capture_via_parent()
        file_m.tk_popup(app.winfo_rootx() + 4, app.winfo_rooty())   # drop below "File"

    app.after(500, post)
    app.mainloop()


def context():
    app = ttk.App(title="Editor", size=(320, 220))
    ttk.Label(app, text="Right-click the text", padding=40).pack(expand=True)
    menu = ttk.Menu(app, tearoff=False)
    for item in ("Cut", "Copy", "Paste"):
        menu.add_command(label=item)

    def post():
        app.capture_via_parent()
        menu.tk_popup(app.winfo_rootx() + 110, app.winfo_rooty() + 70)

    app.after(500, post)
    app.mainloop()


SCENES = {
    "file_menu": file_menu,
    "context": context,
}
