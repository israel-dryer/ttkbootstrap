"""Context menu widget for displaying popup menus.

Provides a customizable context menu with support for commands, checkbuttons,
radiobuttons, and separators.
"""

from tkinter import BooleanVar, IntVar, StringVar, TclError, Toplevel, Widget
from typing import Any, Callable, Union

from ttkbootstrap.widgets.primitives import RadioToggle, CheckToggle, Frame, Label, Separator
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.types import Master
from ttkbootstrap.widgets.primitives.checkbutton import CheckButton
from ttkbootstrap.widgets.composites.compositeframe import CompositeFrame
from ttkbootstrap.widgets.mixins import CustomConfigMixin, configure_delegate
from ttkbootstrap.widgets.primitives.radiobutton import RadioButton


class _CommandItemFrame(CompositeFrame):
    """Container frame for command items that delegates to the inner button.

    Uses CompositeFrame for automatic state propagation across children.
    """

    def __init__(self, master, **kwargs):
        self._button: Button | None = None  # Must be set before super().__init__
        super().__init__(master, **kwargs)

    def invoke(self):
        """Delegate invoke to the button."""
        if self._button:
            return self._button.invoke()

    def state(self, statespec=None):
        """Get or set state, propagating to button when setting."""
        if statespec is None:
            # Getter: return button state if available
            if self._button:
                return self._button.state()
            return super().state()
        else:
            # Setter: set state on self (for Composite propagation)
            # Button and label get state from Composite directly since they're registered
            return super().state(statespec)

    def configure(self, cnf=None, **kwargs):
        """Delegate configure to the button for common options."""
        if self._button:
            return self._button.configure(cnf, **kwargs)
        return super().configure(cnf, **kwargs)


class ContextMenuItem:
    """Data class for context menu items.

    Attributes:
        type (str): Type of menu item ('command', 'checkbutton', 'radiobutton', 'separator').
        kwargs (dict): Additional keyword arguments for the item.
    """

    def __init__(self, type: str, **kwargs) -> None:
        """Initialize a context menu item.

        Args:
            type (str): Type of menu item ('command', 'checkbutton', 'radiobutton', 'separator').
            **kwargs: Additional arguments passed to the widget.
        """
        self.type: str = type
        self.kwargs: dict[str, Any] = kwargs


class ContextMenu(CustomConfigMixin):
    """A customizable context menu widget.

    Displays a popup menu with support for command buttons, checkbuttons,
    radiobuttons, and separators. The menu automatically hides when clicking
    outside or when an item is selected.

    Items can be accessed by key (str) or index (int) for backward compatibility.
    """

    def __init__(
            self,
            master: Master = None,
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
            show_border=True,
            padding=4,
            surface='overlay'
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

        # Track menu items by key with insertion order
        self._items: dict[str, Widget] = {}
        self._item_order: list[str] = []
        self._counter = 0  # For auto-generating keys
        self._highlighted_index = -1

        # Add initial items if provided
        if items:
            self.add_items(items)

        # Setup keyboard bindings
        self._setup_keyboard_bindings()

    def _generate_key(self) -> str:
        """Generate an auto key for an item."""
        key = f"item_{self._counter}"
        self._counter += 1
        return key

    def _resolve_key(self, key_or_index: str | int) -> str:
        """Resolve a key or index to a key.

        Args:
            key_or_index: Either a string key or integer index.

        Returns:
            The string key.

        Raises:
            KeyError: If key not found.
            IndexError: If index out of range.
        """
        if isinstance(key_or_index, int):
            try:
                return self._item_order[key_or_index]
            except IndexError as exc:
                raise IndexError(f"ContextMenu item index {key_or_index} out of range") from exc
        else:
            if key_or_index not in self._items:
                raise KeyError(f"No item with key '{key_or_index}'")
            return key_or_index

    def _register_item(self, key: str | None, widget: Widget) -> str:
        """Register an item with optional key, auto-generating if needed.

        Args:
            key: Optional key. Auto-generated if None.
            widget: The widget to register.

        Returns:
            The key used (either provided or auto-generated).

        Raises:
            ValueError: If key already exists.
        """
        if key is None:
            key = self._generate_key()

        if key in self._items:
            raise ValueError(f"Item with key '{key}' already exists")

        self._items[key] = widget
        self._item_order.append(key)
        return key

    def on_item_click(self, callback: Callable) -> None:
        """Set item click callback. Callback receives ``item_info = {'type': str, 'text': str, 'value': Any}``."""
        self._on_item_click_callback = callback

    def off_item_click(self) -> None:
        """Remove the item click callback."""
        self._on_item_click_callback = None

    def add_command(
            self,
            text: str = None,
            icon: str = None,
            command: Callable = None,
            disabled: bool = False,
            shortcut: str = None,
            key: str = None
    ) -> Button:
        """Add a command button to the menu.

        Args:
            text (str): Button text label.
            icon (str): Optional icon name. Uses 'empty' placeholder if None
                to maintain text alignment with items that have icons.
            command (Callable): Function to call when clicked.
            disabled (bool): If True, the item is disabled and cannot be clicked.
            shortcut (str): Optional keyboard shortcut label (e.g., "Ctrl+S").
                Displayed on the right side with muted foreground.
            key (str): Optional unique identifier. Auto-generated if not provided.

        Returns:
            Button: The created Button widget.
        """
        if shortcut:
            # Use CompositeFrame container for items with shortcuts
            # This handles state propagation (hover, pressed, focus) across children
            container = _CommandItemFrame(self._frame, variant='context-frame')
            container.pack(fill='x', padx=0, pady=0)

            btn = Button(
                container,
                text=text,
                icon=icon or 'empty',
                compound='left',
                variant='context-item',
                command=lambda: self._handle_item_click('command', text, command)
            )
            btn.pack(side='left', fill='x', expand=True)

            shortcut_label = Label(
                container,
                text=shortcut,
                variant='context-label',
                padding=(0, 0, 4, 0)
            )
            shortcut_label.pack(side='right')

            # Register children with CompositeFrame for state propagation
            container.register_composite(btn)
            container.register_composite(shortcut_label)

            container._button = btn
            if disabled:
                container.set_disabled(True)

            self._register_item(key, container)
            return btn
        else:
            # Simple button without shortcut
            btn = Button(
                self._frame,
                text=text,
                icon=icon or 'empty',
                compound='left',
                variant='context-item',
                command=lambda: self._handle_item_click('command', text, command)
            )
            if disabled:
                btn.state(['disabled'])
            btn.pack(fill='x', padx=0, pady=0)
            self._register_item(key, btn)
            return btn

    def add_checkbutton(
            self,
            text: str = None,
            value: bool = False,
            command: Callable = None,
            key: str = None
    ) -> CheckButton:
        """Add a checkbutton to the menu.

        Args:
            text (str): Checkbutton text label.
            value (bool): Initial checked state.
            command (Callable): Function to call when toggled.
            key (str): Optional unique identifier. Auto-generated if not provided.

        Returns:
            CheckButton: The created CheckButton widget.
        """
        var = BooleanVar(value=value)

        def on_toggle():
            self._handle_item_click('checkbutton', text, command, var.get())

        cb = CheckToggle(
            self._frame,
            text=text,
            variable=var,
            variant='context-check',
            command=on_toggle
        )
        cb.pack(fill='x', padx=0, pady=0)
        cb._variable = var  # Store reference to prevent garbage collection
        self._register_item(key, cb)
        return cb

    def add_radiobutton(
            self,
            text: str = None,
            value: Any = None,
            variable: Union[StringVar, IntVar] = None,
            command: Callable = None,
            key: str = None
    ) -> RadioButton:
        """Add a radiobutton to the menu.

        Args:
            text (str): Radiobutton text label.
            value (Any): Value to set when selected.
            variable (StringVar | IntVar): Tkinter Variable to link with.
            command (Callable): Function to call when selected.
            key (str): Optional unique identifier. Auto-generated if not provided.

        Returns:
            RadioButton: The created RadioButton widget.
        """

        def on_select():
            self._handle_item_click('radiobutton', text, command, value)

        rb = RadioToggle(
            self._frame,
            text=text,
            value=value,
            variable=variable,
            variant='context-radio',
            command=on_select
        )
        rb.pack(fill='x', padx=0, pady=0)
        self._register_item(key, rb)
        return rb

    def add_separator(self, key: str = None) -> Separator:
        """Add a horizontal separator to the menu.

        Args:
            key (str): Optional unique identifier. Auto-generated if not provided.

        Returns:
            Separator: The created Separator widget.
        """
        sep = Separator(self._frame, orient='horizontal')
        sep.pack(fill='x', padx=0, pady=3)
        self._register_item(key, sep)
        return sep

    def add_item(self, type: str, **kwargs: Any) -> Widget:
        """Add a menu item based on type.

        Args:
            type (str): Type of item ('command', 'checkbutton', 'radiobutton', 'separator').
            **kwargs: Arguments passed to the appropriate add_* method.

        Returns:
            Widget: The created widget.
        """
        if type == 'command':
            return self.add_command(**kwargs)
        elif type == 'checkbutton':
            return self.add_checkbutton(**kwargs)
        elif type == 'radiobutton':
            return self.add_radiobutton(**kwargs)
        elif type == 'separator':
            return self.add_separator(**kwargs)
        else:
            raise ValueError(f"Unknown item type: {type}")

    def add_items(self, items: list) -> None:
        """Add multiple items at once.

        Args:
            items (list): List of ContextMenuItem objects or dictionaries with 'type' and 'kwargs'.
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

    def keys(self) -> tuple[str, ...]:
        """Get all item keys in order.

        Returns:
            A tuple of all item keys in the order they were added.
        """
        return tuple(self._item_order)

    def insert_item(self, index: int, type: str, **kwargs: Any) -> Widget:
        """Insert a new item at the given index.

        Args:
            index (int): Position to insert the item at.
            type (str): Type of item ('command', 'checkbutton', 'radiobutton', 'separator').
            **kwargs: Arguments passed to the appropriate add_* method.

        Returns:
            Widget: The created widget.
        """
        before_key = self._item_order[index] if 0 <= index < len(self._item_order) else None
        before_widget = self._items[before_key] if before_key else None

        widget = self.add_item(type, **kwargs)

        if before_widget is None:
            return widget

        # Get the key of the just-added widget (last in order)
        new_key = self._item_order.pop()

        pack_info = widget.pack_info()
        widget.pack_forget()
        pack_info.pop('in', None)
        pack_info['before'] = before_widget
        widget.pack(**pack_info)

        # Insert key at correct position
        self._item_order.insert(index, new_key)
        return widget

    def item(self, key_or_index: str | int) -> Widget:
        """Get a menu item by key or index.

        Args:
            key_or_index: The key (str) or index (int) of the item to retrieve.

        Returns:
            The menu item widget.

        Raises:
            KeyError: If no item with the given key exists.
            IndexError: If the index is out of range.
        """
        key = self._resolve_key(key_or_index)
        return self._items[key]

    def remove_item(self, key_or_index: str | int) -> None:
        """Remove and destroy the item by key or index.

        Args:
            key_or_index: Key (str) or index (int) of the item to remove.
        """
        key = self._resolve_key(key_or_index)
        widget = self._items.pop(key)
        self._item_order.remove(key)

        try:
            widget.destroy()
        except TclError:
            pass
        return None

    def move_item(self, from_key_or_index: str | int, to_index: int) -> Widget:
        """Reorder an existing item to a new index.

        Args:
            from_key_or_index: Key (str) or index (int) of the item to move.
            to_index (int): New index for the item.

        Returns:
            Widget: The moved widget.
        """
        key = self._resolve_key(from_key_or_index)
        widget = self._items[key]

        # Remove from current position in order
        self._item_order.remove(key)

        pack_info = widget.pack_info()
        widget.pack_forget()

        # Clamp destination to valid bounds
        if to_index < 0:
            to_index = 0
        if to_index > len(self._item_order):
            to_index = len(self._item_order)

        # Insert at new position
        self._item_order.insert(to_index, key)
        before_key = self._item_order[to_index + 1] if to_index + 1 < len(self._item_order) else None
        before_widget = self._items[before_key] if before_key else None

        pack_info.pop('in', None)
        pack_info.pop('in_', None)
        pack_info.pop('before', None)
        pack_info.pop('after', None)
        if before_widget:
            pack_info['before'] = before_widget
        widget.pack(in_=self._frame, **pack_info)
        return widget

    def configure_item(self, key_or_index: str | int, option: str | None = None, **kwargs: Any) -> Any:
        """Configure an individual menu item by key or index.

        Args:
            key_or_index: Key (str) or index (int) of the item to configure.
            option: Optional option name to query (getter path).
            **kwargs: Option values to set (setter path).

        Returns:
            - When called with no kwargs and no option: full option map for the item.
            - When called with option only: a 5-tuple matching tkinter's configure.
            - When called with kwargs: the result of the underlying widget's configure.
        """
        key = self._resolve_key(key_or_index)
        widget = self._items[key]

        # Getter: all options
        if option is None and not kwargs:
            return widget.configure()

        # Getter: single option
        if option is not None and not kwargs:
            return widget.configure(option)

        # Setter path
        return widget.configure(**kwargs)

    def show(self, position: tuple[int, int] = None) -> None:
        """Show the context menu.

        Args:
            position (tuple): Optional screen coordinate (x, y) to align to. If provided,
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

        # Start with no item highlighted (keyboard nav will highlight on first arrow key)
        self._highlighted_index = -1

        # Setup click outside handler if enabled
        if self._hide_on_outside_click:
            self._setup_click_outside_handler()

    def _setup_keyboard_bindings(self) -> None:
        """Setup keyboard navigation bindings on the toplevel."""
        self._toplevel.bind('<Escape>', lambda e: self.hide())
        self._toplevel.bind('<Down>', self._on_arrow_down)
        self._toplevel.bind('<Up>', self._on_arrow_up)
        self._toplevel.bind('<Return>', self._on_enter)
        self._toplevel.bind('<KP_Enter>', self._on_enter)

    def _get_actionable_items(self) -> list:
        """Return list of items that can be navigated to (excludes separators)."""
        return [self._items[key] for key in self._item_order if not isinstance(self._items[key], Separator)]

    def _on_arrow_down(self, event) -> str:
        """Handle arrow down key."""
        actionable = self._get_actionable_items()
        if not actionable:
            return 'break'

        # Find next actionable item
        current = self._highlighted_index
        next_idx = current + 1 if current < len(actionable) - 1 else 0
        self._update_highlight(next_idx)
        return 'break'

    def _on_arrow_up(self, event) -> str:
        """Handle arrow up key."""
        actionable = self._get_actionable_items()
        if not actionable:
            return 'break'

        # Find previous actionable item
        current = self._highlighted_index
        prev_idx = current - 1 if current > 0 else len(actionable) - 1
        self._update_highlight(prev_idx)
        return 'break'

    def _on_enter(self, event) -> str:
        """Handle enter key to activate highlighted item."""
        actionable = self._get_actionable_items()
        if not actionable or self._highlighted_index < 0:
            return 'break'

        if 0 <= self._highlighted_index < len(actionable):
            item = actionable[self._highlighted_index]
            # Simulate a click by invoking the button
            item.invoke()
        return 'break'

    def _update_highlight(self, new_index: int) -> None:
        """Update the highlighted item."""
        actionable = self._get_actionable_items()
        if not actionable:
            self._highlighted_index = -1
            return

        # Clamp index
        new_index = max(0, min(new_index, len(actionable) - 1))

        # Remove highlight from old item
        if 0 <= self._highlighted_index < len(actionable):
            actionable[self._highlighted_index].state(['!focus'])

        # Add highlight to new item
        actionable[new_index].state(['focus'])
        self._highlighted_index = new_index

    def hide(self) -> None:
        """Hide the context menu."""
        # Unbind click handler first
        self._cancel_click_outside_after()
        self._unbind_click_outside_handler()

        # Clear highlight state
        self._clear_highlight()

        if self._toplevel.winfo_exists():
            self._toplevel.withdraw()

    def _clear_highlight(self) -> None:
        """Clear the highlight from the current item."""
        actionable = self._get_actionable_items()
        if 0 <= self._highlighted_index < len(actionable):
            actionable[self._highlighted_index].state(['!focus'])
        self._highlighted_index = -1

    def destroy(self) -> None:
        """Destroy the context menu and cleanup resources."""
        # Unbind click handler
        self._cancel_click_outside_after()
        self._unbind_click_outside_handler()

        # Destroy toplevel
        if self._toplevel.winfo_exists():
            self._toplevel.destroy()

    def _handle_item_click(self, type: str, text: str, command: Callable = None, value: Any = None) -> None:
        """Handle item click events.

        Args:
            type (str): Type of item clicked.
            text (str): Text of the item.
            command (Callable): Command to execute.
            value (Any): Value associated with the item.
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

    def _setup_click_outside_handler(self) -> None:
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

    def _unbind_click_outside_handler(self) -> None:
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

    def _cancel_click_outside_after(self) -> None:
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
            # Return items in order
            return [self._items[key] for key in self._item_order]

        # Destroy existing widgets before replacing
        for widget in self._items.values():
            try:
                widget.destroy()
            except TclError:
                pass
        self._items = {}
        self._item_order = []
        self._counter = 0
        self.add_items(value)
        return None