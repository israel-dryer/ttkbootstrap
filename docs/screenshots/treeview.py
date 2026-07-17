"""Screenshot scenes for docs/widgets/treeview.rst."""

import ttkbootstrap as ttk


def hero():
    app = ttk.App(title="Treeview")
    frm = ttk.Frame(app, padding=10).pack()

    tree = ttk.Treeview(frm, columns=("size", "modified"), bootstyle="info",
                        height=6)
    tree.heading("#0", text="Name")
    tree.heading("size", text="Size")
    tree.heading("modified", text="Modified")
    tree.column("#0", width=180)
    tree.column("size", width=80, anchor="e")
    tree.column("modified", width=110, anchor="e")
    tree.pack()

    src = tree.insert("", "end", text="src", open=True, values=("—", "today"))
    tree.insert(src, "end", text="app.py", values=("4 KB", "today"))
    tree.insert(src, "end", text="utils.py", values=("2 KB", "yesterday"))
    tree.insert("", "end", text="README.md", values=("1 KB", "last week"))

    app.mainloop()


SCENES = {
    "hero": hero,
}
