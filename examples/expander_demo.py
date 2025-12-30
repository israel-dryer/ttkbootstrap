"""
Expander Widget Demo

Demonstrates the Expander widget features:
- Expand/collapse content
- Icons in header
- Different initial states
- Programmatic control
"""

import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites import Expander


def main():
    root = ttk.App(theme="dark")
    root.title("Expander Demo")
    root.geometry("500x600")

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill='both', expand=True)

    # --- Basic Expander ---
    basic = Expander(main_frame, icon="bootstrap", color='primary', variant='solid', title="Basic Expander", highlight=True, show_border=True)
    basic.pack(fill='x', pady=5)

    basic_content = basic.add()
    ttk.Label(basic_content, text="This is the expandable content.").pack(anchor='w', padx=10, pady=10)

    # --- Expander with Active State (hover/pressed) ---
    active = Expander(
        main_frame,
        title="With Active State",
        icon="cursor"
    )
    active.pack(fill='x', pady=5)

    active_content = active.add()
    ttk.Label(active_content, text="Hover over the header to see the active state.").pack(anchor='w', padx=10, pady=10)

    # --- Expander with Icon ---
    with_icon = Expander(main_frame, title="Settings", icon="gear")
    with_icon.pack(fill='x', pady=5)

    icon_content = with_icon.add()
    ttk.Label(icon_content, text="Settings content goes here.").pack(anchor='w', padx=10, pady=5)
    ttk.CheckButton(icon_content, text="Enable notifications").pack(anchor='w', padx=10)
    ttk.CheckButton(icon_content, text="Dark mode").pack(anchor='w', padx=10, pady=(0, 10))

    # --- Initially Collapsed ---
    collapsed = Expander(main_frame, title="Advanced Options", icon="sliders", expanded=False)
    collapsed.pack(fill='x', pady=5)

    collapsed_content = collapsed.add()
    ttk.Label(collapsed_content, text="These options are hidden by default.").pack(anchor='w', padx=10, pady=10)

    # --- Non-collapsible (leaf item) ---
    leaf = Expander(main_frame, title="Home", icon="house", collapsible=False)
    leaf.pack(fill='x', pady=5)

    # --- Nested Expanders ---
    parent = Expander(main_frame, title="Files", icon="folder")
    parent.pack(fill='x', pady=5)

    parent_content = parent.add()

    child1 = Expander(parent_content, title="Documents", icon="file-earmark-text", expanded=False)
    child1.pack(fill='x', pady=2, padx=10)

    child1_content = child1.add()
    ttk.Label(child1_content, text="Your documents").pack(anchor='w', padx=10, pady=5)

    child2 = Expander(parent_content, title="Pictures", icon="image", expanded=False)
    child2.pack(fill='x', pady=2, padx=10)

    child2_content = child2.add()
    ttk.Label(child2_content, text="Your pictures").pack(anchor='w', padx=10, pady=5)

    # --- Controls ---
    controls = ttk.LabelFrame(main_frame, text="Programmatic Control", padding=10)
    controls.pack(fill='x', pady=20)

    def expand_all():
        basic.expand()
        with_icon.expand()
        collapsed.expand()
        parent.expand()
        child1.expand()
        child2.expand()

    def collapse_all():
        basic.collapse()
        with_icon.collapse()
        collapsed.collapse()
        parent.collapse()
        child1.collapse()
        child2.collapse()

    def toggle_first():
        basic.toggle()

    btn_frame = ttk.Frame(controls)
    btn_frame.pack()

    ttk.Button(btn_frame, text="Expand All", command=expand_all).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Collapse All", command=collapse_all).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Toggle First", command=toggle_first).pack(side='left', padx=5)

    root.mainloop()


if __name__ == '__main__':
    main()