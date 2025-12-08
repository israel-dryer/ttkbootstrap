import ttkbootstrap as ttk

DARK = 'dark'
LIGHT = 'light'


def create_treeview_style():
    # Create frame for padding
    container = ttk.Frame(root)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Create the Treeview
    columns = ("first_name", "last_name", "email")

    tree = ttk.TreeView(
        container,
        columns=columns,
        show="headings",
        height=8,
    )
    tree.pack(fill="both", expand=True)

    # Define headings (column titles)
    tree.heading("first_name", text="First Name", anchor="w")
    tree.heading("last_name", text="Last Name", anchor="w")
    tree.heading("email", text="Email", anchor="w")

    # Define column widths and alignment
    tree.column("first_name", width=120, anchor="w")
    tree.column("last_name", width=120, anchor="w")
    tree.column("email", width=240, anchor="w")

    # Sample data
    data = [
        ("Alice", "Johnson", "alice@example.com"),
        ("Bob", "Smith", "bob.smith@example.com"),
        ("Charlie", "Brown", "charlie.brown@example.com"),
        ("Diana", "Prince", "diana@themiscira.org"),
        ("Alice", "Johnson", "alice@example.com"),
        ("Bob", "Smith", "bob.smith@example.com"),
        ("Charlie", "Brown", "charlie.brown@example.com"),
        ("Diana", "Prince", "diana@themiscira.org"),
        ("Alice", "Johnson", "alice@example.com"),
        ("Bob", "Smith", "bob.smith@example.com"),
        ("Charlie", "Brown", "charlie.brown@example.com"),
        ("Diana", "Prince", "diana@themiscira.org"),
    ]

    # Insert rows
    for row in data:
        tree.insert("", "end", values=row)

    return container


def change_style():
    if style.theme_use() == DARK:
        style.theme_use(LIGHT)
    else:
        style.theme_use(DARK)


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    create_treeview_style().pack(side='left')

    root.mainloop()
