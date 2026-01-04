"""Demo for the MenuBar composite widget."""
import ttkbootstrap as ttk
from ttkbootstrap import ContextMenuItem


def main():
    root = ttk.App(title="MenuBar Demo", size=(600, 400), theme='light')

    status = ttk.Label(root, text="Select a menu item...", anchor="w")

    def on_item(data):
        status.configure(text=f"Selected: {data['type']} - {data['text']}")

    def show_about():
        status.configure(text="About: MenuBar Demo v1.0")

    def show_help():
        status.configure(text="Help: Press F1 for help")

    # File commands
    def new_file():
        status.configure(text="Action: New file")

    def open_file():
        status.configure(text="Action: Open file")

    def save_file():
        status.configure(text="Action: Save file")

    # Edit commands
    def undo():
        status.configure(text="Action: Undo")

    def redo():
        status.configure(text="Action: Redo")

    def cut():
        status.configure(text="Action: Cut")

    def copy():
        status.configure(text="Action: Copy")

    def paste():
        status.configure(text="Action: Paste")

    # Register keyboard shortcuts
    # Uses 'Mod' which becomes Ctrl on Windows/Linux, Command on Mac
    shortcuts = ttk.get_shortcuts()
    shortcuts.register("new", "Mod+N", new_file)
    shortcuts.register("open", "Mod+O", open_file)
    shortcuts.register("save", "Mod+S", save_file)
    shortcuts.register("undo", "Mod+Z", undo)
    shortcuts.register("redo", "Mod+Shift+Z", redo)
    shortcuts.register("cut", "Mod+X", cut)
    shortcuts.register("copy", "Mod+C", copy)
    shortcuts.register("paste", "Mod+V", paste)
    shortcuts.register("help", "F1", show_help)
    shortcuts.bind_to(root)

    # Create menubar
    menubar = ttk.MenuBar(root, gap=6)
    menubar.pack(fill="both")

    # File menu (before/left region)
    # Shortcut keys reference registered shortcuts - display text is automatic
    file_menu = menubar.add_menu(
        "File",
        items=[
            ContextMenuItem(type="command", text="New", command=new_file, shortcut="new"),
            ContextMenuItem(type="command", text="Open", icon="folder2-open", command=open_file, shortcut="open"),
            ContextMenuItem(type="command", text="Save", icon="floppy", command=save_file, shortcut="save"),
            ContextMenuItem(type="command", text="Save As...", icon="floppy-fill"),
            ContextMenuItem(type="separator"),
            ContextMenuItem(type="command", text="Exit", icon="x-lg", command=root.destroy),
        ]
    )
    file_menu.on_item_click(on_item)

    # Edit menu (before/left region)
    edit_menu = menubar.add_menu(
        "Edit",
        items=[
            ContextMenuItem(type="command", text="Undo", icon="arrow-counterclockwise", command=undo, shortcut="undo"),
            ContextMenuItem(type="command", text="Redo", icon="arrow-clockwise", command=redo, shortcut="redo"),
            ContextMenuItem(type="separator"),
            ContextMenuItem(type="command", text="Cut", icon="scissors", command=cut, shortcut="cut"),
            ContextMenuItem(type="command", text="Copy", icon="copy", command=copy, shortcut="copy"),
            ContextMenuItem(type="command", text="Paste", icon="clipboard", command=paste, shortcut="paste"),
        ]
    )
    edit_menu.on_item_click(on_item)

    # View menu (before/left region)
    view_var = ttk.StringVar(value="normal")
    view_menu = menubar.add_menu(
        "View",
        items=[
            ContextMenuItem(type="checkbutton", text="Show Toolbar", value=True),
            ContextMenuItem(type="checkbutton", text="Show Sidebar", value=True),
            ContextMenuItem(type="checkbutton", text="Show Status Bar", value=True),
            ContextMenuItem(type="separator"),
            ContextMenuItem(type="radiobutton", text="Normal", value="normal", variable=view_var),
            ContextMenuItem(type="radiobutton", text="Compact", value="compact", variable=view_var),
            ContextMenuItem(type="radiobutton", text="Full Screen", value="fullscreen", variable=view_var),
        ]
    )
    view_menu.on_item_click(on_item)

    menubar.add_label('My Application', region='center', font='body[bold]')

    # Help button (after/right region)
    menubar.add_button(
        "Help",
        region="after",
        command=show_help,
        icon="question-circle",
    )

    # Account menu (after/right region)
    account_menu = menubar.add_menu(
        "Account",
        region="after",
        items=[
            ContextMenuItem(type="command", text="Profile", icon="person"),
            ContextMenuItem(type="command", text="Settings", icon="gear"),
            ContextMenuItem(type="separator"),
            ContextMenuItem(type="command", text="Sign Out", icon="box-arrow-right"),
        ],
        icon="person-circle",
    )
    account_menu.on_item_click(on_item)


    # Main content area
    content = ttk.Frame(root)
    content.pack(fill="both", expand=True, padx=16, pady=16)

    ttk.Label(
        content,
        text="MenuBar Demo",
        font="caption[bold]",
    ).pack()

    ttk.Label(
        content,
        text="The MenuBar widget provides a flexible horizontal bar with three regions:\n"
             "- 'before' (left): File, Edit, View menus\n"
             "- 'center': Application title (stays centered)\n"
             "- 'after' (right): Help, Account, About buttons",
        justify="left",
    ).pack()

    # Status bar
    ttk.Separator(root).pack(fill="x", padx=8)
    status.pack(fill="x", padx=16, pady=8)

    root.mainloop()


if __name__ == "__main__":
    main()