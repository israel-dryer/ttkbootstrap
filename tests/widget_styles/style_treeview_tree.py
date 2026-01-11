import ttkbootstrap as ttk

DARK = 'dark'
LIGHT = 'light'


def populate_tree(tree):
    """Add sample items to a treeview."""
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


def create_treeview_demo(root):
    """Create side-by-side comparison of default and compact density."""
    container = ttk.Frame(root, padding=10)

    # Left side - Default density
    left_frame = ttk.Frame(container)
    left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

    ttk.Label(left_frame, text="Default Density", font="-weight bold").pack(anchor='w', pady=(0, 5))

    tree_default = ttk.TreeView(
        left_frame,
        show='tree',
        density='default',
        select_background='primary[subtle]'
    )
    tree_default.pack(fill="both", expand=True)
    populate_tree(tree_default)

    # Right side - Compact density
    right_frame = ttk.Frame(container)
    right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

    ttk.Label(right_frame, text="Compact Density", font="-weight bold").pack(anchor='w', pady=(0, 5))

    tree_compact = ttk.TreeView(
        right_frame,
        show='tree',
        density='compact',
        select_background='primary[subtle]'
    )
    tree_compact.pack(fill="both", expand=True)
    populate_tree(tree_compact)

    return container


if __name__ == '__main__':
    root = ttk.Window(title="Treeview Density Demo", size=(800, 500))

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    create_treeview_demo(root).pack(fill='both', expand=True)

    root.mainloop()
