"""
Simple demo for the ListItem widget

This demo showcases various features of the ListItem widget including:
- Basic text display (title, text, caption)
- Selection modes (single, multi, none)
- Chevron indicators
- Delete functionality
- Drag and drop handles
"""

import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.listitem import ListItem


def main():
    """Main demo application"""
    root = ttk.Window(title="ListItem Widget Demo", theme="darkly")
    root.geometry("700x650")

    # Create main container with padding
    container = ttk.Frame(root, padding=20)
    container.pack(fill='both', expand=True)

    # Title
    title = ttk.Label(
        container,
        text="ListItem Widget Demo",
        font=('Helvetica', 18, 'bold')
    )
    title.pack(pady=(0, 15), anchor='w')

    # Basic Items Section
    ttk.Label(container, text="Basic Items", font=('Helvetica', 12, 'bold')).pack(pady=(5, 5), anchor='w')

    item1 = ListItem(container, enable_focus_state=True)
    item1.update_data({'title': 'Simple Item', 'item_index': 0})
    item1.pack(fill='x', pady=2)

    item2 = ListItem(container, enable_focus_state=True)
    item2.update_data({
        'title': 'Item with Description',
        'text': 'This item has both a title and descriptive text',
        'item_index': 1
    })
    item2.pack(fill='x', pady=2)

    item3 = ListItem(container, enable_focus_state=True)
    item3.update_data({
        'title': 'Complete Item',
        'text': 'This item has a title, text, and caption',
        'caption': 'Caption appears in smaller text below',
        'item_index': 2
    })
    item3.pack(fill='x', pady=2)

    item4 = ListItem(container, enable_focus_state=True)
    item4.update_data({
        'icon': {'name': 'star-fill'},
        'title': 'Item with Icon',
        'text': 'This item has an icon on the left',
        'item_index': 3
    })
    item4.pack(fill='x', pady=2)

    # Selection Mode Section
    ttk.Label(container, text="Selection Modes", font=('Helvetica', 12, 'bold')).pack(pady=(15, 5), anchor='w')

    # Single selection
    for i in range(2):
        item = ListItem(
            container,
            selection_mode='single',
            show_selection_controls=True,
            enable_focus_state=True
        )
        item.update_data({
            'title': f'Single Select {i+1}',
            'text': 'Radio button style selection',
            'item_index': i,
            'selected': i == 0
        })
        item.pack(fill='x', pady=2)

    # Multi selection
    for i in range(2):
        item = ListItem(
            container,
            selection_mode='multi',
            show_selection_controls=True,
            enable_focus_state=True
        )
        item.update_data({
            'title': f'Multi Select {i+1}',
            'text': 'Checkbox style selection',
            'item_index': i
        })
        item.pack(fill='x', pady=2)

    # Features Section
    ttk.Label(container, text="Features", font=('Helvetica', 12, 'bold')).pack(pady=(15, 5), anchor='w')

    chevron_item = ListItem(container, show_chevron=True, enable_focus_state=True)
    chevron_item.update_data({
        'title': 'Chevron Item',
        'text': 'Has a chevron indicator on the right',
        'item_index': 0
    })
    chevron_item.pack(fill='x', pady=2)

    def on_delete(event):
        print(f"Delete clicked for: {delete_item.data['title']}")
        delete_item.pack_forget()

    delete_item = ListItem(container, enable_deleting=True, enable_focus_state=True)
    delete_item.update_data({
        'title': 'Deletable Item',
        'text': 'Click the X to delete',
        'item_index': 1
    })
    delete_item.pack(fill='x', pady=2)
    delete_item.bind('<<ItemDeleting>>', on_delete)

    drag_item = ListItem(container, enable_dragging=True, enable_focus_state=True)
    drag_item.update_data({
        'title': 'Draggable Item',
        'text': 'Use the grip handle to drag',
        'item_index': 2
    })
    drag_item.pack(fill='x', pady=2)

    separator_item = ListItem(container, show_separator=True, enable_focus_state=True)
    separator_item.update_data({
        'title': 'Item with Separator',
        'text': 'Has a separator line below',
        'item_index': 3
    })
    separator_item.pack(fill='x', pady=2)

    # Instructions
    ttk.Separator(container).pack(fill='x', pady=15)
    ttk.Label(container, text="Try clicking, hovering, and using Tab to navigate!",
              font=('Helvetica', 10, 'italic')).pack(anchor='w')

    root.mainloop()


if __name__ == '__main__':
    main()