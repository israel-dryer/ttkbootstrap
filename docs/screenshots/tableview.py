"""Screenshot scenes for docs/widgets/tableview.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.widgets import Tableview


def hero():
    app = ttk.App(title="Tableview")
    frm = ttk.Frame(app, padding=10).pack(fill="both", expand=True)

    table = Tableview(
        frm,
        coldata=["Name", "Role", "Age"],
        rowdata=[
            ["Ada Lovelace", "Engineer", 36],
            ["Grace Hopper", "Admiral", 85],
            ["Alan Turing", "Cryptographer", 41],
            ["Katherine Johnson", "Mathematician", 101],
            ["Margaret Hamilton", "Engineer", 88],
        ],
        searchable=True,
        paginated=True,
        height=5,
        bootstyle="primary",
    ).pack(fill="both", expand=True)
    table.view.selection_remove(*table.view.selection())

    app.mainloop()


SCENES = {
    "hero": hero,
}
