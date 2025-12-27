import ttkbootstrap as ttk

DARK = 'dark'
LIGHT = 'light'


def create_treeview_style():
    frame = ttk.Frame(root, padding=5)

    # Create Treeview
    tree = ttk.TreeView(root, show="tree")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Define columns (optional – here we use just the built-in #0 column for labels)
    # If you want extra data columns, you can uncomment this part:
    # tree["columns"] = ("size", "modified")
    # tree.heading("#0", text="Name", anchor="w")
    # tree.heading("size", text="Size", anchor="w")
    # tree.heading("modified", text="Modified", anchor="w")

    # Add parents
    parent1 = tree.insert("", "end", text="Parent 1", open=True)
    parent2 = tree.insert("", "end", text="Parent 2", open=False)
    parent3 = tree.insert("", "end", text="Parent 3", open=False)

    # Add children to Parent 1
    tree.insert(parent1, "end", text="Child 1.1")
    tree.insert(parent1, "end", text="Child 1.2")
    child13 = tree.insert(parent1, "end", text="Child 1.3", open=True)

    # Grandchildren under Child 1.3
    tree.insert(child13, "end", text="Grandchild 1.3.1")
    tree.insert(child13, "end", text="Grandchild 1.3.2")

    # Add children to Parent 2
    tree.insert(parent2, "end", text="Child 2.1")
    tree.insert(parent2, "end", text="Child 2.2")

    # Add children to Parent 3
    tree.insert(parent3, "end", text="Child 3.1")

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    create_treeview_style().pack(side='left')

    root.mainloop()
