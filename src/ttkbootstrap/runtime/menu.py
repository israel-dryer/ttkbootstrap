"""Menu utilities for ttkbootstrap.

This module provides utilities for creating menus with icon support and
theme-aware color updates.

Examples:
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
from typing import Any, Optional, Union

from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.core.localization import MessageCatalog
from ttkbootstrap.style.style import get_style


class MenuManager:
    """Manages menus with icon support and theme-aware color updates.

    This class provides a declarative way to create menus with automatic icon
    support and theme-aware color updates. When the theme changes, all menu
    icons are automatically updated to match the new theme's foreground color.

    The MenuManager tracks all menu items that have icons and listens for
    `<<ThemeChanged>>` events on the root window. When a theme change is detected,
    it recreates and updates all icons to ensure they match the new theme.

    Attributes:
        parent: The parent widget (typically a Window or Toplevel).
        style: The Style instance for accessing theme colors.
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
        self.parent: Any = parent
        self.style = get_style()
        self.menu_items: dict[str, tuple[tk.Menu, int, str, int]] = {}

        # Set up theme change monitoring
        self._setup_theme_monitoring()

    @classmethod
    def for_widget(cls, widget: Any) -> "MenuManager":
        """Return the singleton MenuManager for ``widget``'s root window.

        Creates one on first access and stores it on the root as
        ``_menu_manager``. Use this to share icon-tracking and theme
        monitoring across all tk.Menu-based widgets in an application
        (menubars, context menus, etc.) without each one binding its own
        ``<<ThemeChanged>>`` handler.
        """
        root = widget.winfo_toplevel() if hasattr(widget, 'winfo_toplevel') else widget
        existing = getattr(root, '_menu_manager', None)
        if existing is not None:
            return existing
        mgr = cls(root)
        try:
            root._menu_manager = mgr
        except Exception:
            pass
        return mgr

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

    # ----- Public helpers for tk.Menu callers --------------------------------

    @staticmethod
    def translate_label(text: Optional[str]) -> Optional[str]:
        """Run a label through ``MessageCatalog.translate``.

        Semantic keys (e.g. ``'table.sort_asc'``) become localized strings;
        plain text passes through unchanged because ``translate`` returns
        the source when no translation is registered.
        """
        if not text:
            return text
        try:
            return MessageCatalog.translate(text)
        except Exception:
            return text

    def resolve_icon(self, icon_spec: Union[str, dict, None]) -> tuple[Any, Optional[str], int]:
        """Resolve an icon spec to a ``(PhotoImage, name, size)`` triple.

        Returns ``(None, None, 0)`` for empty/unsupported specs. The returned
        PhotoImage is the same kind ``MenuManager`` uses internally for its
        own menus, so the caller can pass it straight to
        ``menu.add_command(image=..., compound='left')``.
        """
        if not icon_spec or icon_spec == 'empty':
            return None, None, 0
        name, size = self._parse_icon_spec(icon_spec)
        if not name:
            return None, None, 0
        try:
            fg = self.style.style_builder.color('foreground')
            icon = BootstrapIcon(name, size, fg)
        except Exception:
            return None, None, 0
        return icon, name, size

    def register_icon(self, menu: tk.Menu, index: int, icon_name: str, icon_size: int) -> None:
        """Track a menu item for theme-aware icon re-rendering.

        Call after ``menu.add_*(image=icon)`` so subsequent
        ``<<ThemeChanged>>`` events refresh the entry's icon color.
        """
        self._track_icon(menu, index, icon_name, icon_size)

    def unregister_menu(self, menu: tk.Menu) -> None:
        """Drop all tracking entries for ``menu``.

        Call when the menu is being destroyed or fully rebuilt so stale
        ``(menu, index)`` references don't try to reconfigure deleted entries
        on the next ``<<ThemeChanged>>``.
        """
        prefix = f"{id(menu)}_"
        for key in [k for k in self.menu_items if k.startswith(prefix)]:
            del self.menu_items[key]

    def _parse_icon_spec(self, icon_spec: Union[str, dict]) -> tuple[Optional[str], int]:
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

    def create_menu(self, parent: Any, items: list[dict]) -> tk.Menu:
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

            # Translate the label so semantic keys (e.g. 'menu.file') resolve
            # via MessageCatalog. Plain text passes through unchanged.
            if 'label' in options:
                options['label'] = self.translate_label(options['label'])

            # Handle icon for cascade menu BEFORE popping tearoff
            icon_spec = options.pop('icon', None)
            icon_name = None
            icon_size = 16

            if icon_spec:
                icon, icon_name, icon_size = self.resolve_icon(icon_spec)
                if icon is not None:
                    options['image'] = icon
                    options['compound'] = options.get('compound', 'left')

            options.setdefault('tearoff', 0)

            # Create a menu for this item
            menu = tk.Menu(parent, tearoff=options.pop('tearoff'))

            # Add it as a cascade to the parent menu
            parent.add_cascade(menu=menu, **options)

            # Track cascade icon if present
            if icon_name:
                self.register_icon(parent, parent.index('end'), icon_name, icon_size)

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
                continue

            # Regular menu item (not a cascade)
            if 'label' in opts:
                opts['label'] = self.translate_label(opts['label'])

            icon_spec = opts.pop('icon', None)
            icon_name = None
            icon_size = 0
            if icon_spec:
                icon, icon_name, icon_size = self.resolve_icon(icon_spec)
                if icon is not None:
                    opts['image'] = icon
                    opts['compound'] = opts.get('compound', 'left')

            item_type = opts.pop('type', 'command')
            if item_type == 'separator':
                menu.add_separator()
                continue

            adder = {
                'command': menu.add_command,
                'checkbutton': menu.add_checkbutton,
                'radiobutton': menu.add_radiobutton,
            }.get(item_type, menu.add_command)
            adder(**opts)

            if icon_name:
                self.register_icon(menu, menu.index('end'), icon_name, icon_size)

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

            app = ttk.App()

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


__all__ = ['create_menu']
