"""
Toolbar Demo

Demonstrates the Toolbar widget with:
- Icon buttons
- Labels
- Separators and spacers
- Window controls (minimize, maximize, close)
- Custom titlebar with window dragging
"""

import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.toolbar import Toolbar


def main():
    root = ttk.Window(theme="cosmo", title="Toolbar Demo", size=(800, 500))

    # --- Example 1: Basic toolbar ---
    ttk.Label(root, text="Basic Toolbar", font='heading').pack(anchor='w', padx=10, pady=(10, 5))

    toolbar1 = Toolbar(root, show_border=True)
    toolbar1.pack(fill='x', padx=10, pady=5)

    toolbar1.add_button(icon='house', command=lambda: print("Home"))
    toolbar1.add_button(icon='folder', command=lambda: print("Open"))
    toolbar1.add_button(icon='floppy', command=lambda: print("Save"))
    toolbar1.add_separator()
    toolbar1.add_button(icon='arrow-counterclockwise', command=lambda: print("Undo"))
    toolbar1.add_button(icon='arrow-clockwise', command=lambda: print("Redo"))
    toolbar1.add_spacer()
    toolbar1.add_button(icon='gear', command=lambda: print("Settings"))

    # --- Example 2: Toolbar with labels ---
    ttk.Label(root, text="Toolbar with Labels", font='heading').pack(anchor='w', padx=10, pady=(20, 5))

    toolbar2 = Toolbar(root, show_border=True)
    toolbar2.pack(fill='x', padx=10, pady=5)

    toolbar2.add_button(icon='list', command=lambda: print("Menu"))
    toolbar2.add_separator()
    toolbar2.add_label(text="My Application", font='heading-md')
    toolbar2.add_spacer()
    toolbar2.add_label(text="Ready")
    toolbar2.add_separator()
    toolbar2.add_button(icon='bell', command=lambda: print("Notifications"))
    toolbar2.add_button(icon='person-circle', command=lambda: print("Profile"))

    # --- Example 3: Toolbar with window controls ---
    ttk.Label(root, text="Toolbar with Window Controls", font='heading').pack(anchor='w', padx=10, pady=(20, 5))

    toolbar3 = Toolbar(root, show_window_controls=True, show_border=True)
    toolbar3.pack(fill='x', padx=10, pady=5)

    toolbar3.add_button(icon='list')
    toolbar3.add_separator()
    toolbar3.add_label(text="Custom Titlebar", font='heading-md')
    toolbar3.add_spacer()

    # --- Example 4: Custom titlebar demo button ---
    ttk.Label(root, text="Custom Titlebar Demo", font='heading').pack(anchor='w', padx=10, pady=(20, 5))

    def open_custom_titlebar_window():
        """Open a window with hidden native titlebar and custom toolbar."""
        win = ttk.Toplevel(root)
        win.title("Custom Titlebar Window")
        win.geometry("500x300")
        win.overrideredirect(True)  # Hide native titlebar

        # Custom titlebar
        titlebar = Toolbar(
            win,
            show_window_controls=True,
            draggable=True,
            bootstyle='primary',
        )
        titlebar.pack(fill='x')

        titlebar.add_button(icon='app-indicator')
        titlebar.add_label(text="Custom Window", font='heading-md', bootstyle='primary')
        titlebar.add_spacer()

        # Content
        content = ttk.Frame(win, padding=20)
        content.pack(fill='both', expand=True)

        ttk.Label(
            content,
            text="This window has a custom titlebar.\n\nDrag the toolbar to move the window.\nUse the window controls to minimize, maximize, or close.",
            wraplength=400,
        ).pack(expand=True)

    btn = ttk.Button(
        root,
        text="Open Custom Titlebar Window",
        command=open_custom_titlebar_window,
    )
    btn.pack(padx=10, pady=10)

    root.mainloop()


if __name__ == '__main__':
    main()