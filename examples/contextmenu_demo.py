"""ContextMenu widget demonstration.

Demonstrates various features of the ContextMenu widget including:
- Command buttons with icons
- Checkbuttons for toggleable options
- Radiobuttons for exclusive selections
- Separators for visual organization
- Item click callbacks
"""

import ttkbootstrap as ttk
from ttkbootstrap import ContextMenu


def main():
    root = ttk.Window()
    root.title("ContextMenu Demo")
    root.geometry("500x400")

    ttk.Label(
        root,
        text="ContextMenu Widget Demo",
        font=("Helvetica", 16, "bold")
    ).pack(pady=10)

    # Create context menu (right-click anywhere in the window)
    menu = ContextMenu(
        master=root,
        anchor='nw',      # menu corner to align
        attach='nw',      # aligns to the click point provided to show()
        offset=(0, 0),
        hide_on_outside_click=True,
    )

    # Add command items with icons
    menu.add_command(text="New", icon="file-earmark", command=lambda: print("New file"))
    menu.add_command(text="Open", icon="folder2-open", command=lambda: print("Open file"))
    menu.add_command(text="Save", icon="floppy", command=lambda: print("Save file"))
    menu.add_separator()

    # Add checkbuttons
    menu.add_checkbutton(text="Show Grid", value=True, command=lambda: print("Toggle grid"))
    menu.add_checkbutton(text="Show Rulers", value=False, command=lambda: print("Toggle rulers"))
    menu.add_checkbutton(text="Snap to Grid", value=False, command=lambda: print("Toggle snap"))
    menu.add_separator()

    # Add radiobuttons with shared variable
    view_var = ttk.StringVar(value="list")
    menu.add_radiobutton(text="List View", value="list", variable=view_var, command=lambda: print("List view"))
    menu.add_radiobutton(text="Grid View", value="grid", variable=view_var, command=lambda: print("Grid view"))
    menu.add_radiobutton(text="Details View", value="details", variable=view_var, command=lambda: print("Details view"))
    menu.add_separator()

    # Add exit command
    menu.add_command(text="Exit", icon="door-open", command=root.quit)

    # Register item click callback
    def on_item_clicked(data):
        status_label.configure(
            text=f"Last action: {data['type']} - {data['text']} - Value: {data['value']}"
        )
        print(f"Item clicked: {data}")

    menu.on_item_click(on_item_clicked)

    # Show menu on right-click
    def show_context_menu(event):
        menu.show(position=(event.x_root, event.y_root))

    root.bind('<Button-3>', show_context_menu)

    # Instructions
    instructions = ttk.LabelFrame(root, text="Instructions", padding=10)
    instructions.pack(fill='x', padx=20, pady=10)

    ttk.Label(
        instructions,
        text="- Right-click anywhere to show the context menu"
    ).pack(anchor='w')
    ttk.Label(
        instructions,
        text="- Click menu items to see callbacks in action"
    ).pack(anchor='w')
    ttk.Label(
        instructions,
        text="- Click outside the menu to hide it"
    ).pack(anchor='w')

    # Status label
    status_label = ttk.Label(
        root,
        text="Right-click to open context menu",
        font=("Helvetica", 10),
        color="secondary"
    )
    status_label.pack(pady=20)

    # Example: Create menu programmatically with items list
    frame2 = ttk.LabelFrame(root, text="Programmatic Menu", padding=10)
    frame2.pack(fill='x', padx=20, pady=10)

    ttk.Label(
        frame2,
        text="Click the button to show a programmatically created menu"
    ).pack()

    btn = ttk.Button(
        frame2,
        text="Show Dynamic Menu",
        command=lambda: show_dynamic_menu(),
        color="info"
    )
    btn.pack(pady=5)

    # Create menu once and reuse it to preserve state
    # Align menu's top-left to the button's bottom-left with a small vertical gap
    dynamic_menu = ContextMenu(
        master=root,
        target=btn,
        anchor='nw',
        attach='sw',
        offset=(0, 4),
        hide_on_outside_click=True,
    )
    dynamic_menu.add_command(text='Copy', icon='clipboard2', command=lambda: print('Copy'))
    dynamic_menu.add_command(text='Paste', icon='clipboard2-check', command=lambda: print('Paste'))
    dynamic_menu.add_separator()
    dynamic_menu.add_checkbutton(text='Bold', value=False, command=lambda: print('Bold toggled'))
    dynamic_menu.add_checkbutton(text='Italic', value=False, command=lambda: print('Italic toggled'))

    def show_dynamic_menu():
        dynamic_menu.show()

    root.mainloop()


if __name__ == '__main__':
    main()
