"""
Demo for the ListView widget

This demo showcases the ListView widget's features including:
- Virtual scrolling for efficient rendering of large datasets
- Multiple selection modes (single, multi, none)
- Selection controls (checkboxes/radio buttons)
- Delete functionality
- Focus states
- Interactive features (chevron, drag handles)
"""

import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites import ListView, MemoryDataSource


def create_sample_data(count=1000):
    """Create sample data for the ListView."""
    return [
        {
            'id': i,
            'title': f'Item {i}',
            'text': f'This is the description for item {i}',
            'caption': f'Created: 2024-0{(i % 9) + 1}-{(i % 28) + 1:02d}'
        }
        for i in range(count)
    ]


def main():
    """Main demo application."""
    root = ttk.App(title="ListView Widget Demo", theme="docs-light", size=(1200, 700))
    root.geometry("1200x700")

    # Main container
    main_container = ttk.Frame(root, padding=20)
    main_container.pack(fill='both', expand=True)

    # Title
    title = ttk.Label(
        main_container,
        text="ListView Widget Demo",
        font=('Helvetica', 18, 'bold')
    )
    title.pack(pady=(0, 15), anchor='w')

    # Create three columns for different ListView examples
    columns = ttk.Frame(main_container)
    columns.pack(fill='both', expand=True)

    # Column 1: Simple ListView
    col1 = ttk.Frame(columns, padding=10)
    col1.pack(side='left', fill='both', expand=True)

    ttk.Label(col1, text="Simple ListView", font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
    ttk.Label(col1, text="Basic list with 1000 items", font=('Helvetica', 9)).pack(anchor='w', pady=(0, 10))

    simple_data = create_sample_data(1000)
    simple_list = ListView(
        col1,
        items=simple_data,
        enable_focus_state=True,
        alternating_row_mode='even',
        enable_hover_state=False,
        show_separator=True,

    )
    simple_list.pack(fill='both', expand=True)

    # Add counter for simple list
    simple_label = ttk.Label(col1, text=f"Total: {len(simple_data)} items")
    simple_label.pack(pady=(5, 0), anchor='w')

    # Column 2: Multi-select ListView
    col2 = ttk.Frame(columns, padding=10)
    col2.pack(side='left', fill='both', expand=True)

    ttk.Label(col2, text="Multi-Select ListView", font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
    ttk.Label(col2, text="Select multiple items", font=('Helvetica', 9)).pack(anchor='w', pady=(0, 10))

    multi_data = create_sample_data(500)
    multi_list = ListView(
        col2,
        items=multi_data,
        selection_mode='multi',
        show_selection_controls=True,
        enable_focus_state=True,
        show_separator=True,
        show_chevron=True
    )
    multi_list.pack(fill='both', expand=True)

    # Add controls for multi-select list
    multi_controls = ttk.Frame(col2)
    multi_controls.pack(pady=(5, 0), fill='x')

    selected_label = ttk.Label(multi_controls, text="Selected: 0")
    selected_label.pack(side='left')

    def update_multi_selection(event=None):
        selected = multi_list.get_selected()
        selected_label.config(text=f"Selected: {len(selected)}")

    multi_list.bind('<<SelectionChanged>>', update_multi_selection)

    ttk.Button(
        multi_controls,
        text="Select All",
        command=lambda: (multi_list.select_all(), update_multi_selection()),
        bootstyle='secondary-outline',
        width=12
    ).pack(side='right', padx=(5, 0))

    ttk.Button(
        multi_controls,
        text="Clear",
        command=lambda: (multi_list.clear_selection(), update_multi_selection()),
        bootstyle='secondary-outline',
        width=12
    ).pack(side='right')

    # Column 3: Feature-rich ListView
    col3 = ttk.Frame(columns, padding=10)
    col3.pack(side='left', fill='both', expand=True)

    ttk.Label(col3, text="Feature-rich ListView", font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
    ttk.Label(col3, text="With delete & single-select", font=('Helvetica', 9)).pack(anchor='w', pady=(0, 10))

    feature_data = create_sample_data(300)
    feature_list = ListView(
        col3,
        items=feature_data,
        selection_mode='single',
        show_selection_controls=True,
        enable_focus_state=True,
        show_separator=True,
        enable_dragging=True,
        enable_deleting=True,
        show_chevron=True
    )
    feature_list.pack(fill='both', expand=True)

    # Add controls for feature list
    feature_controls = ttk.Frame(col3)
    feature_controls.pack(pady=(5, 0), fill='x')

    feature_label = ttk.Label(feature_controls, text=f"Total: {len(feature_data)} items")
    feature_label.pack(side='left')

    def update_feature_count(event=None):
        datasource = feature_list.get_datasource()
        count = datasource.total_count()
        feature_label.config(text=f"Total: {count} items")

    feature_list.bind('<<ItemDeleted>>', update_feature_count)

    ttk.Button(
        feature_controls,
        text="Add Item",
        command=lambda: (
            feature_list.insert_item({
                'title': f'New Item {feature_list.get_datasource().total_count() + 1}',
                'text': 'Newly added item',
                'caption': 'Just now'
            }),
            update_feature_count()
        ),
        bootstyle='success-outline',
        width=12
    ).pack(side='right', padx=(5, 0))

    ttk.Button(
        feature_controls,
        text="Scroll Top",
        command=feature_list.scroll_to_top,
        bootstyle='secondary-outline',
        width=12
    ).pack(side='right', padx=(5, 0))

    ttk.Button(
        feature_controls,
        text="Scroll Bottom",
        command=feature_list.scroll_to_bottom,
        bootstyle='secondary-outline',
        width=12
    ).pack(side='right')

    # Instructions
    ttk.Separator(main_container).pack(fill='x', pady=(15, 10))

    instructions_frame = ttk.Frame(main_container)
    instructions_frame.pack(fill='x')

    ttk.Label(
        instructions_frame,
        text="Features:",
        font=('Helvetica', 11, 'bold')
    ).pack(anchor='w', pady=(0, 5))

    instructions = [
        "• Virtual scrolling efficiently handles thousands of items",
        "• Use mouse wheel or scrollbar to navigate",
        "• Tab key navigates between focusable items",
        "• Click selection controls or items to select",
        "• Delete button removes items from the list"
    ]

    for instruction in instructions:
        ttk.Label(instructions_frame, text=instruction, font=('Helvetica', 9)).pack(anchor='w', padx=10)

    simple_list.on_item_selected(lambda x: print(x.data))
    multi_list.on_item_selected(lambda x: print(x.data))
    feature_list.on_item_selected(lambda x: print(x.data))

    root.mainloop()


if __name__ == '__main__':
    main()