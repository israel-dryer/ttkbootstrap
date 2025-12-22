"""Context menu widget for displaying popup menus.

Provides a customizable context menu with support for commands, checkbuttons,
radiobuttons, and separators.
"""

from tkinter import BooleanVar, IntVar, StringVar, TclError, Toplevel, Widget
from typing import Any, Callable, Union

from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.checkbutton import CheckButton
from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.mixins import CustomConfigMixin, configure_delegate
from ttkbootstrap.widgets.primitives.radiobutton import RadioButton
from ttkbootstrap.widgets.primitives.separator import Separator


class ContextMenuItem:
    """Data class for context menu items.

    Attributes:
        type: Type of menu item ('command', 'checkbutton', 'radiobutton', 'separator')
        kwargs: Additional keyword arguments for the item
    """

    def __init__(self, type: str, **kwargs):
        """Initialize a context menu item.

        Args:
            type: Type of menu item
            **kwargs: Additional arguments passed to the widget
        """
        self.type = type
        self.kwargs = kwargs


class ContextMenu(CustomConfigMixin):
    """A customizable context menu widget.

    Displays a popup menu with support for command buttons, checkbuttons,
    radiobuttons, and separators. The menu automatically hides when clicking
    outside or when an item is selected.

    Examples:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.composites.contextmenu import ContextMenu

        root = ttk.Window()

        # Create context menu
        menu = ContextMenu(
            master=root,
            target=root,
            anchor='nw',      # menu corner to align
            attach='se',      # target corner to align to
            offset=(0, 0),    # additional x/y offset
            hide_on_outside_click=True
        )

        # Add items
        menu.add_command(text="Open", icon="folder2-open", command=lambda: print("Open"))
        menu.add_command(text="Save", icon="floppy", command=lambda: print("Save"))
        menu.add_separator()
        menu.add_checkbutton(text="Show Grid", value=True)
        menu.add_separator()
        menu.add_command(text="Exit", icon="x-lg", command=root.quit)

        # Show on right-click
        def show_menu(event):
            menu.show(position=(event.x_root, event.y_root))

        root.bind('<Button-3>', show_menu)

        root.mainloop()
        ```
    """

    def __init__(
            self,
            master=None,
            minwidth: int = 150,
            width: int = None,
            minheight: int = None,
            height: int = None,
            target: Widget = None,
            anchor: str = 'nw',
            attach: str = 'se',
            offset: tuple[int, int] = (0, 0),
            hide_on_outside_click: bool = True,
            items: list[ContextMenuItem] = None
    ):
        """Initialize a ContextMenu widget.

        Args:
            master: Parent widget. If None, uses the default root window.
            minwidth: Minimum width for the menu in pixels. Default is 150.
            width: Fixed width for the menu in pixels. If None, uses minwidth.
            minheight: Minimum height for the menu in pixels. If None, auto-sizes.
            height: Fixed height for the menu in pixels. If None, auto-sizes to content.
            target: Target widget to attach the menu to. Used for relative positioning.
            anchor: Anchor point on the menu to align (e.g., 'nw', 'ne', 'sw', 'se', 'center').
            attach: Anchor point on the target to align to (same options as anchor).
            offset: Tuple (dx, dy) applied after alignment.
            hide_on_outside_click: If True, menu hides when clicking outside.
                Default is True.
            items: List of ContextMenuItem objects to add initially.
        """
        super().__init__()
        self._master = master
        self._target = target
        self._minwidth = minwidth
        self._width = width
        self._minheight = minheight
        self._height = height
        self._anchor = (anchor or 'nw').lower()
        self._attach = (attach or 'nw').lower()
        self._offset = offset or (0, 0)
        self._hide_on_outside_click = hide_on_outside_click
        self._on_item_click_callback = None
        self._click_handler_id = None
        self._click_binding_root = None
        self._click_bind_after_id = None

        # Create toplevel window
        self._toplevel = Toplevel(master)
        self._toplevel.withdraw()
        self._toplevel.overrideredirect(True)

        # Create frame with border and padding
        self._frame = Frame(
            self._toplevel,
            padding=3,
            show_border=True,
            bootstyle='default'
        )
        self._frame.pack(fill='both', expand=True)

        # Configure size constraints
        if width:
            self._frame.configure(width=width)
        if height:
            self._frame.configure(height=height)

        # Set minimum size on toplevel
        if minwidth or minheight:
            self._toplevel.minsize(minwidth or 0, minheight or 0)

        # Track menu items
        self._items = []

        # Add initial items if provided
        if items:
            self.add_items(items)

    def on_item_click(self, callback: Callable[[dict], Any]) -> None:
        """Register callback for item clicks.

        The callback receives a dictionary with:
            - type: Item type ('command', 'checkbutton', 'radiobutton')
            - text: Item text
            - value: Item value (for checkbuttons and radiobuttons)

        Args:
            callback: Function to call when an item is clicked
        """
        self._on_item_click_callback = callback

    def off_item_click(self):
        """Unregister callback for item clicks."""
        self._on_item_click_callback = None

    def add_command(self, text: str = None, icon: str = None, command: Callable = None):
        """Add a command button to the menu.

        Args:
            text: Button text label
            icon: Optional icon name
            command: Function to call when clicked

        Returns:
            The created Button widget
        """
        btn = Button(
            self._frame,
            text=text,
            icon=icon,
            compound='left' if icon else 'text',
            bootstyle='context_item',
            command=lambda: self._handle_item_click('command', text, command)
        )
        btn.pack(fill='x', padx=0, pady=0)
        self._items.append(btn)
        return btn

    def add_checkbutton(self, text: str = None, value: bool = False, command: Callable = None):
        """Add a checkbutton to the menu.

        Args:
            text: Checkbutton text label
            value: Initial checked state
            command: Function to call when toggled

        Returns:
            The created Checkbutton widget
        """
        var = BooleanVar(value=value)

        def on_toggle():
            self._handle_item_click('checkbutton', text, command, var.get())

        cb = CheckButton(
            self._frame,
            text=text,
            variable=var,
            bootstyle='context_check-toolbutton',
            command=on_toggle
        )
        cb.pack(fill='x', padx=0, pady=0)
        cb._variable = var  # Store reference to prevent garbage collection
        self._items.append(cb)
        return cb

    def add_radiobutton(
            self,
            text: str = None,
            value: Any = None,
            variable: Union[StringVar, IntVar] = None,
            command: Callable = None
    ):
        """Add a radiobutton to the menu.

        Args:
            text: Radiobutton text label
            value: Value to set when selected
            variable: Tkinter Variable to link with (StringVar or IntVar)
            command: Function to call when selected

        Returns:
            The created Radiobutton widget
        """

        def on_select():
            self._handle_item_click('radiobutton', text, command, value)

        rb = RadioButton(
            self._frame,
            text=text,
            value=value,
            variable=variable,
            bootstyle='context_radio-toolbutton',
            command=on_select
        )
        rb.pack(fill='x', padx=0, pady=0)
        self._items.append(rb)
        return rb

    def add_separator(self):
        """Add a horizontal separator to the menu.

        Returns:
            The created Separator widget
        """
        sep = Separator(self._frame, orient='horizontal')
        sep.pack(fill='x', padx=0, pady=3)
        self._items.append(sep)
        return sep

    def add_item(self, type: str, **kwargs):
        """Add a menu item based on type.

        Args:
            type: Type of item ('command', 'checkbutton', 'radiobutton', 'separator')
            **kwargs: Arguments passed to the appropriate add_* method

        Returns:
            The created widget
        """
        if type == 'command':
            return self.add_command(**kwargs)
        elif type == 'checkbutton':
            return self.add_checkbutton(**kwargs)
        elif type == 'radiobutton':
            return self.add_radiobutton(**kwargs)
        elif type == 'separator':
            return self.add_separator()
        else:
            raise ValueError(f"Unknown item type: {type}")

    def add_items(self, items: list):
        """Add multiple items at once.

        Args:
            items: List of ContextMenuItem objects or dictionaries with 'type' and 'kwargs'
        """
        for item in items:
            if isinstance(item, ContextMenuItem):
                self.add_item(item.type, **item.kwargs)
            elif isinstance(item, dict):
                item_type = item.get('type')
                kwargs = {k: v for k, v in item.items() if k != 'type'}
                self.add_item(item_type, **kwargs)

    def items(self, value=None):
        """Get or set the current menu items."""
        if value is None:
            return self._delegate_items(None)
        self._delegate_items(value)
        return None

    def insert_item(self, index: int, type: str, **kwargs):
        """Insert a new item at the given index."""
        before_widget = self._items[index] if 0 <= index < len(self._items) else None

        widget = self.add_item(type, **kwargs)

        if before_widget is None:
            return widget

        pack_info = widget.pack_info()
        widget.pack_forget()
        pack_info.pop('in', None)
        pack_info['before'] = before_widget
        widget.pack(**pack_info)

        self._items.pop()
        self._items.insert(index, widget)
        return widget

    def remove_item(self, index: int):
        """Remove and destroy the item at the given index."""
        try:
            widget = self._items.pop(index)
        except IndexError as exc:
            raise IndexError(f"ContextMenu item index {index} out of range") from exc

        try:
            widget.destroy()
        except TclError:
            pass
        return None

    def move_item(self, from_index: int, to_index: int):
        """Reorder an existing item to a new index."""
        try:
            widget = self._items.pop(from_index)
        except IndexError as exc:
            raise IndexError(f"ContextMenu item index {from_index} out of range") from exc

        pack_info = widget.pack_info()
        widget.pack_forget()

        # Clamp destination to valid bounds
        if to_index < 0:
            to_index = 0
        if to_index > len(self._items):
            to_index = len(self._items)

        self._items.insert(to_index, widget)
        before_widget = self._items[to_index + 1] if to_index + 1 < len(self._items) else None

        pack_info.pop('in', None)
        pack_info.pop('in_', None)
        pack_info.pop('before', None)
        pack_info.pop('after', None)
        if before_widget:
            pack_info['before'] = before_widget
        widget.pack(in_=self._frame, **pack_info)
        return widget

    def configure_item(self, index: int, option: str | None = None, **kwargs):
        """Configure an individual menu item by index.

        Args:
            index: Zero-based index of the item in insertion order.
            option: Optional option name to query (getter path).
            **kwargs: Option values to set (setter path).

        Returns:
            - When called with no kwargs and no option: full option map for the item.
            - When called with option only: a 5-tuple matching tkinter's configure.
            - When called with kwargs: the result of the underlying widget's configure.
        """
        try:
            widget = self._items[index]
        except IndexError as exc:
            raise IndexError(f"ContextMenu item index {index} out of range") from exc

        # Getter: all options
        if option is None and not kwargs:
            return widget.configure()

        # Getter: single option
        if option is not None and not kwargs:
            return widget.configure(option)

        # Setter path
        return widget.configure(**kwargs)

    def show(self, position: tuple[int, int] = None):
        """Show the context menu.

        Args:
            position: Optional screen coordinate (x, y) to align to. If provided,
                the menu's anchor will align to this point. Negative x/y are
                treated as offsets from the screen's right/bottom.
        """
        # Update geometry before showing
        self._toplevel.update_idletasks()

        # Determine position
        pos = self._compute_position(position)
        if pos:
            self._toplevel.geometry(f"+{pos[0]}+{pos[1]}")

        # Show the menu
        self._toplevel.deiconify()
        self._toplevel.lift()
        self._toplevel.focus_force()

        # Setup click outside handler if enabled
        if self._hide_on_outside_click:
            self._setup_click_outside_handler()

    def hide(self):
        """Hide the context menu."""
        # Unbind click handler first
        self._cancel_click_outside_after()
        self._unbind_click_outside_handler()

        if self._toplevel.winfo_exists():
            self._toplevel.withdraw()

    def destroy(self):
        """Destroy the context menu and cleanup resources."""
        # Unbind click handler
        self._cancel_click_outside_after()
        self._unbind_click_outside_handler()

        # Destroy toplevel
        if self._toplevel.winfo_exists():
            self._toplevel.destroy()

    def _handle_item_click(self, type: str, text: str, command: Callable = None, value: Any = None):
        """Handle item click events.

        Args:
            type: Type of item clicked
            text: Text of the item
            command: Command to execute
            value: Value associated with the item
        """
        # Prepare event data
        data = {
            'type': type,
            'text': text,
            'value': value
        }

        # Call registered callback
        if self._on_item_click_callback:
            self._on_item_click_callback(data)

        # Execute item command
        if command:
            command()

        # Hide menu after item click
        self.hide()

    def _compute_position(self, position: tuple[int, int] | None) -> tuple[int, int] | None:
        """Compute screen coordinates for the menu based on anchor/attach/offset."""

        def anchor_offsets(key: str, width: int, height: int) -> tuple[float, float]:
            table = {
                'nw': (0, 0),
                'n': (width / 2, 0),
                'ne': (width, 0),
                'w': (0, height / 2),
                'center': (width / 2, height / 2),
                'e': (width, height / 2),
                'sw': (0, height),
                's': (width / 2, height),
                'se': (width, height),
            }
            if key not in table:
                raise ValueError(f"Invalid anchor '{key}'. Use one of: {', '.join(table.keys())}")
            return table[key]

        # Ensure geometry is up to date for accurate size
        self._toplevel.update_idletasks()

        menu_w = self._toplevel.winfo_reqwidth()
        menu_h = self._toplevel.winfo_reqheight()

        # Base point: from provided position or target attach
        base_x = base_y = None

        if position is not None:
            base_x, base_y = position
            screen_w = self._toplevel.winfo_screenwidth()
            screen_h = self._toplevel.winfo_screenheight()
            if base_x < 0:
                base_x = screen_w + base_x
            if base_y < 0:
                base_y = screen_h + base_y
        elif self._target and self._target.winfo_exists():
            self._target.update_idletasks()
            target_w = self._target.winfo_width()
            target_h = self._target.winfo_height()
            base_x = self._target.winfo_rootx()
            base_y = self._target.winfo_rooty()
            attach_dx, attach_dy = anchor_offsets(self._attach, target_w, target_h)
            base_x += attach_dx
            base_y += attach_dy
        else:
            return None

        menu_dx, menu_dy = anchor_offsets(self._anchor, menu_w, menu_h)
        final_x = int(base_x - menu_dx + self._offset[0])
        final_y = int(base_y - menu_dy + self._offset[1])
        return final_x, final_y

    def _setup_click_outside_handler(self):
        """Setup handler to hide menu when clicking outside."""

        def on_click(event):
            # Don't process if menu is not visible
            if not self._toplevel.winfo_viewable():
                return

            # Check if click is inside the menu
            try:
                x, y = event.x_root, event.y_root
                tx = self._toplevel.winfo_rootx()
                ty = self._toplevel.winfo_rooty()
                tw = self._toplevel.winfo_width()
                th = self._toplevel.winfo_height()

                # Click is outside if coordinates are not within bounds
                if not (tx <= x <= tx + tw and ty <= y <= ty + th):
                    self.hide()
            except TclError:
                # If the menu has been torn down, ensure it is hidden
                self.hide()

        def bind_click():
            # Clear the pending after id once we run
            self._click_bind_after_id = None

            # Skip binding if the menu is already hidden
            if not (self._toplevel.winfo_exists() and self._toplevel.winfo_viewable()):
                return

            if self._toplevel.winfo_exists():
                self._unbind_click_outside_handler()
                root = self._get_binding_root()
                if root and root.winfo_exists():
                    self._click_binding_root = root
                    self._click_handler_id = root.bind('<Button-1>', on_click, add='+')

        # Delay binding to avoid capturing the click that shows the menu
        self._cancel_click_outside_after()
        self._click_bind_after_id = self._toplevel.after(100, bind_click)

    def _get_binding_root(self) -> Widget | None:
        """Return the widget to bind click-outside events to."""
        candidate = self._target or self._master or self._toplevel.master
        if candidate:
            try:
                return candidate.winfo_toplevel()
            except TclError:
                return None
        return None

    def _unbind_click_outside_handler(self):
        """Remove the click-outside binding if present."""
        if not self._click_handler_id or not self._click_binding_root:
            return

        try:
            if self._click_binding_root.winfo_exists():
                self._click_binding_root.unbind('<Button-1>', self._click_handler_id)
        except TclError:
            pass
        finally:
            self._click_handler_id = None
            self._click_binding_root = None

    def _cancel_click_outside_after(self):
        """Cancel any scheduled click-outside binding."""
        if self._click_bind_after_id and self._toplevel.winfo_exists():
            try:
                self._toplevel.after_cancel(self._click_bind_after_id)
            except TclError:
                pass
        self._click_bind_after_id = None

    # ----- Configuration delegates -------------------------------------------------

    @configure_delegate('minwidth')
    def _delegate_minwidth(self, value: int | None):
        """Get or set the minimum width."""
        if value is None:
            return self._minwidth
        self._minwidth = value
        return self._toplevel.minsize(value or 0, self._minheight or 0)

    @configure_delegate('minheight')
    def _delegate_minheight(self, value: int | None):
        """Get or set the minimum height."""
        if value is None:
            return self._minheight
        self._minheight = value
        return self._toplevel.minsize(self._minwidth or 0, value or 0)

    @configure_delegate('width')
    def _delegate_width(self, value: int | None):
        """Get or set the fixed width."""
        if value is None:
            return self._width
        self._width = value
        return self._frame.configure(width=value if value is not None else '')

    @configure_delegate('height')
    def _delegate_height(self, value: int | None):
        """Get or set the fixed height."""
        if value is None:
            return self._height
        self._height = value
        return self._frame.configure(height=value if value is not None else '')

    @configure_delegate('anchor')
    def _delegate_anchor(self, value: str | None):
        """Get or set the menu anchor."""
        if value is None:
            return self._anchor
        self._anchor = (value or 'nw').lower()
        return None

    @configure_delegate('attach')
    def _delegate_attach(self, value: str | None):
        """Get or set the target attach anchor."""
        if value is None:
            return self._attach
        self._attach = (value or 'nw').lower()
        return None

    @configure_delegate('offset')
    def _delegate_offset(self, value: tuple[int, int] | None):
        """Get or set the positional offset."""
        if value is None:
            return self._offset
        try:
            dx, dy = value  # type: ignore[misc]
        except Exception:
            dx, dy = (0, 0)
        self._offset = (dx, dy)
        return None

    @configure_delegate('hide_on_outside_click')
    def _delegate_hide_on_outside_click(self, value: bool | None):
        """Get or set outside-click hide behavior."""
        if value is None:
            return self._hide_on_outside_click
        self._hide_on_outside_click = bool(value)
        return None

    @configure_delegate('target')
    def _delegate_target(self, value: Widget | None):
        """Get or set the target widget used for positioning."""
        if value is None:
            return self._target
        self._target = value
        return None

    @configure_delegate('items')
    def _delegate_items(self, value: list[ContextMenuItem] | None):
        """Get or replace the menu items."""
        if value is None:
            return self._items

        # Destroy existing widgets before replacing
        for widget in self._items:
            try:
                widget.destroy()
            except TclError:
                pass
        self._items = []
        self.add_items(value)
        return None

