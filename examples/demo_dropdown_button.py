import ttkbootstrap as ttk
from ttkbootstrap import ContextMenuItem


def main():
    root = ttk.Window(theme="flatly", title="DropdownButton Demo", size=(420, 320))

    ttk.Label(root, text="DropdownButton", font=("Segoe UI", 16, "bold")).pack(pady=12)

    status = ttk.Label(root, text="Select an item...", anchor="w")
    status.pack(fill="x", padx=16, pady=(0, 12))

    def on_item(data):
        status.configure(text=f"Last: {data['type']} – {data['text']} – {data.get('value')}")

    # Basic dropdown with command/check/radio
    items = [
        ContextMenuItem(type="command", text="Open", icon="folder2-open"),
        ContextMenuItem(type="command", text="Save", icon="floppy"),
        ContextMenuItem(type="separator"),
        ContextMenuItem(type="checkbutton", text="Show Grid", value=True),
        ContextMenuItem(type="checkbutton", text="Snap to Grid", value=False),
        ContextMenuItem(type="separator"),
        ContextMenuItem(type="radiobutton", text="List View", value="list", variable=ttk.StringVar(value="list")),
        ContextMenuItem(type="radiobutton", text="Grid View", value="grid", variable=ttk.StringVar(value="list")),
        ContextMenuItem(type="radiobutton", text="Detail View", value="detail", variable=ttk.StringVar(value="list")),
    ]

    dd = ttk.DropdownButton(
        root,
        text="Actions",
        items=items,
        bootstyle="primary",
        icon="bootstrap-fill",
        dropdown_button_icon="chevron-down",
    )
    dd.pack(padx=16, pady=8, fill="x")
    dd.on_item_click(on_item)

    # Ghost style, icon-only, custom chevron, and popdown options
    alt = ttk.DropdownButton(
        root,
        text="More",
        items=[
            ContextMenuItem(type="command", text="Rename", icon="pencil"),
            ContextMenuItem(type="command", text="Duplicate", icon="copy"),
            ContextMenuItem(type="separator"),
            ContextMenuItem(type="command", text="Delete", icon="trash"),
        ],
        bootstyle="ghost",
        icon_only=True,
        icon="three-dots-vertical",
        dropdown_button_icon="caret-down-fill",
        popdown_options={"offset": (6, 6)},
    )
    alt.pack(padx=16, pady=8, anchor="e")
    alt.on_item_click(on_item)

    # Toggle chevron visibility at runtime
    def toggle_chevron():
        current = dd['show_dropdown_button']
        dd['show_dropdown_button'] = not current
        status.configure(text=f"Chevron visible: {not current}")

    ttk.Button(root, text="Toggle Chevron", command=toggle_chevron).pack(padx=16, pady=12)

    root.mainloop()


if __name__ == "__main__":
    main()
