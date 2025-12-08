"""Menu utilities for ttkbootstrap.

This module provides utilities for creating menus with icon support and
theme-aware color updates.

Classes:
    MenuManager: Manages menus with icon support and theme-aware color updates

Functions:
    create_menu: Convenience function to create a menu with icon and theme support

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.menu import create_menu

    app = ttk.Window()

    menu_items = [
        {
            "label": "File",
            "items": [
                {"label": "Open", "icon": "folder2-open"},
                {"label": "Save", "icon": "save"},
                {"type": "separator"},
                {"label": "Exit", "command": app.quit, "icon": "x-circle"}
            ],
        },
        {
            "label": "Edit",
            "items": [
                {"label": "Undo", "icon": "arrow-counterclockwise"},
                {"label": "Redo", "icon": "arrow-clockwise"},
            ]
        }
    ]

    create_menu(app, menu_items)
    app.mainloop()
    ```
"""
import tkinter as tk
from tkinter import font, ttk
from typing import Any, Union

from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.style import use_style


class MenuManager:
    """Manages menus with icon support and theme-aware color updates.

    This class provides a declarative way to create menus with automatic icon
    support and theme-aware color updates. When the theme changes, all menu
    icons are automatically updated to match the new theme's foreground color.

    The MenuManager tracks all menu items that have icons and listens for
    <<ThemeChanged>> events on the root window. When a theme change is detected,
    it recreates and updates all icons to ensure they match the new theme.

    Attributes:
        parent: The parent widget (typically a Window or Toplevel).
        style: The Style instance for accessing theme colors.
        icon_provider: The icon provider function for creating icons.
        menu_items: Dictionary tracking menu items with icons for theme updates.
    """

    def __init__(self, parent: Any):
        """Initialize the MenuManager.

        Sets up the menu manager with the given parent widget, initializes
        the style and icon provider, and establishes theme change monitoring
        to automatically update icon colors when themes change.

        Args:
            parent: The parent widget, typically a Window, Toplevel, or root
                widget. This is used to access the style, icon provider, and
                to bind theme change events.
        """
        self.parent = parent
        self.style = use_style()
        self.menu_items = {}  # Track menu items with icons for updates

        # Set up theme change monitoring
        self._setup_theme_monitoring()

    def _setup_theme_monitoring(self):
        """Set up monitoring for <<ThemeChanged>> events on the root window."""
        # Get the root window
        root = self.parent.winfo_toplevel() if hasattr(self.parent, 'winfo_toplevel') else self.parent

        # Bind to theme change event on root
        if hasattr(root, 'bind'):
            root.bind('<<ThemeChanged>>', self._on_theme_changed, add='+')

    def _on_theme_changed(self, event=None):
        """Update all menu icon colors when theme changes."""
        fg_color = self.style.style_builder.color('foreground')

        # Update all menu items (including cascades)
        for menu, index, icon_name, size in self.menu_items.values():
            # Recreate the icon with new foreground color
            new_icon = BootstrapIcon(icon_name, size, fg_color)

            try:
                menu.entryconfigure(index, image=new_icon)
            except tk.TclError:
                # Menu item may have been deleted
                pass

    def _parse_icon_spec(self, icon_spec: Union[str, dict]) -> tuple[str, int]:
        """Parse icon specification into name and size tuple."""
        # Use menu font linespace as default icon size
        menu_font = font.nametofont("TkMenuFont")
        default_size = menu_font.metrics("linespace")

        if isinstance(icon_spec, str):
            return icon_spec, default_size
        elif isinstance(icon_spec, dict):
            name = icon_spec.get('name')
            size = icon_spec.get('size', default_size)
            return name, size
        return None, default_size

    def create_menu(self, parent: Any, items: list[dict]):
        """Create a menu from a list of item dictionaries.

        Args:
            parent: The parent widget (Window, Toplevel, or Menu).
            items: List of menu item dictionaries defining the menu structure.

        Returns:
            The created Menu object.
        """
        menubar = None

        # If parent is a window, create the menubar first
        if not isinstance(parent, tk.Menu):
            menubar = tk.Menu(parent, tearoff=0)
            parent['menu'] = menubar
            parent = menubar  # Now work with the menubar

        for options in items:
            options = options.copy()
            sub_items = options.pop('items', [])

            # Handle icon for cascade menu BEFORE popping tearoff
            icon_spec = options.pop('icon', None)
            icon_name = None
            icon_size = 16

            if icon_spec:
                icon_name, icon_size = self._parse_icon_spec(icon_spec)

                if icon_name:
                    # Get foreground color
                    fg_color = self.style.style_builder.color('foreground')
                    # Create icon with current foreground color
                    icon = BootstrapIcon(icon_name, icon_size, fg_color)
                    options['image'] = icon
                    options['compound'] = options.get('compound', 'left')

            options.setdefault('tearoff', 0)

            # Create a menu for this item
            menu = tk.Menu(parent, tearoff=options.pop('tearoff'))

            # Add it as a cascade to the parent menu
            parent.add_cascade(menu=menu, **options)

            # Track cascade icon if present
            if icon_name:
                # Get the index of the cascade we just added
                cascade_index = parent.index('end')
                item_id = f"{id(parent)}_cascade_{cascade_index}"
                self.menu_items[item_id] = (parent, cascade_index, icon_name, icon_size)

            # Add all sub-items to this menu
            self._add_menu_items(menu, sub_items)

        return parent if isinstance(parent, tk.Menu) else menubar

    def _add_menu_items(self, menu: tk.Menu, items: list[dict]):
        """Add items to a menu with icon support and theme tracking."""
        for opts in items:
            opts = opts.copy()

            # Check if this is a submenu (cascade)
            if 'items' in opts:
                # This item has subitems, so it's a cascade
                # Pass to create_menu which will handle the cascade
                self.create_menu(menu, [opts])
            else:
                # Regular menu item (not a cascade)
                # Handle icon if present
                icon_spec = opts.pop('icon', None)
                icon_name = None
                icon_size = 16

                if icon_spec:
                    icon_name, icon_size = self._parse_icon_spec(icon_spec)

                    if icon_name:
                        # Get foreground color
                        fg_color = self.style.style_builder.color('foreground')
                        # Create icon with current foreground color
                        icon = BootstrapIcon(icon_name, icon_size, fg_color)
                        opts['image'] = icon
                        opts['compound'] = opts.get('compound', 'left')

                if 'type' not in opts:
                    menu.add_command(**opts)
                    if icon_name:
                        index = menu.index('end')
                        self._track_icon(menu, index, icon_name, icon_size)
                elif opts['type'] == 'checkbutton':
                    opts.pop('type')
                    menu.add_checkbutton(**opts)
                    if icon_name:
                        index = menu.index('end')
                        self._track_icon(menu, index, icon_name, icon_size)
                elif opts['type'] == 'radiobutton':
                    opts.pop('type')
                    menu.add_radiobutton(**opts)
                    if icon_name:
                        index = menu.index('end')
                        self._track_icon(menu, index, icon_name, icon_size)
                elif opts['type'] == 'command':
                    opts.pop('type')
                    menu.add_command(**opts)
                    if icon_name:
                        index = menu.index('end')
                        self._track_icon(menu, index, icon_name, icon_size)
                elif opts['type'] == 'separator':
                    menu.add_separator()

    def _track_icon(self, menu: tk.Menu, index: int, icon_name: str, icon_size: int):
        """Register a menu item with an icon for automatic theme updates."""
        item_id = f"{id(menu)}_{index}"
        self.menu_items[item_id] = (menu, index, icon_name, icon_size)


def create_menu(parent: Any, items: list[dict]) -> tk.Menu:
    """Create a menu with icon and theme support.

    This is a convenience function that creates or retrieves a MenuManager
    for the parent window and uses it to build a menu from a declarative
    structure. The resulting menu automatically updates icon colors when
    the theme changes.

    Each menu item is defined by a dictionary that can contain:
        - **label** (str): The text displayed for the menu item
        - **icon** (str or dict): Icon specification. Can be a string icon
          name (e.g., "folder2-open") or a dict with 'name' and 'size' keys
          (e.g., {"name": "folder2-open", "size": 20})
        - **items** (list): List of submenu items for cascade menus
        - **command** (callable): Callback function executed when clicked
        - **type** (str): Menu item type - 'command', 'checkbutton',
          'radiobutton', or 'separator'
        - **variable** (Variable): Tkinter variable for checkbutton/radiobutton
        - **value** (Any): Value for radiobutton items
        - Any other valid Tkinter menu item options (accelerator, underline, etc.)

    Args:
        parent: The parent widget (Window, Toplevel, or Menu). If a Window
            or Toplevel is provided, the menu becomes the window's menubar.
            If a Menu is provided, items are added to that menu.
        items: List of dictionaries defining the menu structure. Each
            dictionary represents a menu item with its configuration.

    Returns:
        The created Menu object. For window menubars, this is the menubar
        itself. For menus attached to other widgets, this is the menu.

    Examples:
        Basic menubar with icons:
            ```python
            import ttkbootstrap as ttk

            app = ttk.Window()

            menu_items = [
                {
                    "label": "File",
                    "items": [
                        {"label": "New", "icon": "file-plus", "command": new_file},
                        {"label": "Open", "icon": "folder2-open", "command": open_file},
                        {"type": "separator"},
                        {"label": "Exit", "icon": "x-circle", "command": app.quit}
                    ]
                },
                {
                    "label": "Edit",
                    "items": [
                        {"label": "Undo", "icon": "arrow-counterclockwise"},
                        {"label": "Redo", "icon": "arrow-clockwise"}
                    ]
                }
            ]

            ttk.create_menu(app, menu_items)
            app.mainloop()
            ```

        Nested submenus with custom icon sizes:
            ```python
            menu_items = [
                {
                    "label": "File",
                    "items": [
                        {
                            "label": "Recent",
                            "icon": {"name": "clock-history", "size": 18},
                            "items": [
                                {"label": "Document 1.txt"},
                                {"label": "Document 2.txt"}
                            ]
                        }
                    ]
                }
            ]
            ```

        Menu with checkbuttons and radiobuttons:
            ```python
            view_var = ttk.BooleanVar(value=True)
            theme_var = ttk.StringVar(value="light")

            menu_items = [
                {
                    "label": "View",
                    "items": [
                        {
                            "label": "Show Toolbar",
                            "type": "checkbutton",
                            "variable": view_var
                        }
                    ]
                },
                {
                    "label": "Theme",
                    "items": [
                        {
                            "label": "Light",
                            "type": "radiobutton",
                            "variable": theme_var,
                            "value": "light"
                        },
                        {
                            "label": "Dark",
                            "type": "radiobutton",
                            "variable": theme_var,
                            "value": "dark"
                        }
                    ]
                }
            ]
            ```
    """
    # Get or create MenuManager for this window
    root = parent.winfo_toplevel() if hasattr(parent, 'winfo_toplevel') else parent

    if not hasattr(root, '_menu_manager'):
        root._menu_manager = MenuManager(root)

    return root._menu_manager.create_menu(parent, items)


__all__ = ['MenuManager', 'create_menu']
