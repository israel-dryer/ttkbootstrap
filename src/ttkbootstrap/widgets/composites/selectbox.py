from tkinter import Toplevel

from typing_extensions import Unpack

from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.composites.scrollview import ScrollView
from ttkbootstrap.widgets.composites.field import Field, FieldOptions
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master


class SelectBox(Field):
    """Dropdown-like field widget built on top of Field.

    Renders a field with a suffix button that opens a popup list of available
    items. Selecting an item updates the field value and emits ``<<Change>>``.

    !!! note "Events"

          ``<<Change>>``: Fired when the selection changes (user or code).
          Provides ``event.data`` with keys: ``value``, ``prev_value``, ``text``.

    Attributes:
        entry_widget (TextEntryPart): The underlying entry widget.
        label_widget (Label): The label widget.
        message_widget (Label): The message label widget.
        addons (dict[str, Widget]): Dictionary of inserted addon widgets by name.
        variable (Variable): Tkinter Variable linked to entry text.
        signal (Signal): Signal object for reactive updates.
    """

    def __init__(
            self,
            master: Master = None,
            value: str = None,
            items: list[str] = None,
            label: str = None,
            message: str = None,
            allow_custom_values: bool = False,
            show_dropdown_button: bool = True,
            dropdown_button_icon: str = None,
            enable_search: bool = False,
            **kwargs: Unpack[FieldOptions]
    ):
        """Create a SelectBox widget.

        Args:
            master: Parent widget. If None, uses the default root window.
            value (str): Initial selected value; should typically be present in ``items``.
            items (list): Sequence of string options to present in the popup list.
            label (str): Optional label text shown above the field.
            message (str): Optional helper/error message shown below the field.
            allow_custom_values (bool): If True, the entry is editable so users can type
                arbitrary values in addition to choosing from the list.
            show_dropdown_button (bool): If True (default), the dropdown button is shown. This option is
                ignored if custom values are allowed.
            dropdown_button_icon (str): The icon to display on the dropdown button.
            enable_search (bool): If True, allows typing in the entry to filter the popup list.
                When combined with allow_custom_values=False, the first filtered item is selected
                when the popup closes. With allow_custom_values=True, any typed value is kept.

        Other Parameters:
            allow_blank (bool): If True, empty input is allowed.
            accent (str): Accent token for styling the focus ring and active border.
            value_format (str): ICU format pattern for parsing/formatting.
            font (str): Font for text display.
            foreground (str): Text color.
            initial_focus (bool): If True, widget receives focus when created.
            justify (str): Text justification ('left', 'center', 'right').
            show_message (bool): If True, displays message text below the field.
            padding (str | int | tuple): Padding around the entry widget.
            state (str): The widget state ('normal', 'disabled', 'readonly').
            textvariable (Variable): Tkinter Variable to link with the entry text.
            textsignal (Signal): Signal object for reactive text updates.
            width (int): Width of the entry in characters.
            required (bool): If True, field cannot be empty.
        """
        super().__init__(master, value=value, label=label, message=message, **kwargs)

        self._allow_custom_values = allow_custom_values
        self._search_enabled = enable_search
        self._items = items or []
        self._last_selected_value = value
        self._popup_open = False
        self._dropdown_button_icon = dropdown_button_icon or 'chevron-down'
        self._popup_frame = None
        self._item_labels = []

        # Add dropdown button if needed
        if allow_custom_values or show_dropdown_button:
            self.insert_addon(
                Button,
                position="after",
                name="dropdown",
                icon=self._dropdown_button_icon,
                icon_only=True,
                command=self._on_dropdown_click
            )

        # Configure entry state based on search and custom value settings
        if allow_custom_values or enable_search:
            self.entry_widget.state(['!readonly'])
        else:
            # Set entry to readonly but keep dropdown button enabled
            self.entry_widget.state(['readonly'])
            self.after_idle(self._bind_readonly_selection_on_click)

    def _on_dropdown_click(self):
        """Handle dropdown button click by focusing entry then showing popup."""
        self.entry_widget.focus_set()
        self._show_selection_options()

    def _bind_readonly_selection_on_click(self):
        """Bind entry click to show popup when in readonly mode."""
        self.entry_widget.bind('<Button-1>', lambda _: self.after_idle(self._show_selection_options), add='+')

    def _show_selection_options(self):
        """Create and display the popup list of selectable items."""
        if not self._items or self._popup_open:
            return

        self._popup_open = True
        self.update_idletasks()

        # Create popup toplevel
        toplevel = self._create_popup_toplevel()

        # Create tracking variables for popup state
        popup_state = {
            'item_was_selected': False,
            'popup_closed': False,
            'first_filtered_item': None,
            'entry_focus_handler': None,
            'key_bindings': [],
            'highlighted_index': max(0, self.selected_index),
        }

        # Setup close handler
        def close_popup(event=None):
            self._close_popup(toplevel, popup_state)

        # Create popup content frame with items
        self._popup_frame = self._create_popup_frame(toplevel, popup_state)

        # Setup event bindings based on mode
        self._setup_popup_bindings(toplevel, popup_state, close_popup)

        # Show popup and set focus
        toplevel.deiconify()
        toplevel.lift()

        if self._search_enabled:
            self.entry_widget.focus_force()
            self.entry_widget.icursor('end')
        else:
            toplevel.focus_force()

    def _create_popup_toplevel(self):
        """Create and position the popup toplevel window."""
        x = self.winfo_rootx() + 3
        y = self.entry_widget.winfo_rooty() + self.entry_widget.winfo_height() + 8
        width = self.winfo_width() - 6
        max_height = 200  # Maximum popup height in pixels

        toplevel = Toplevel(self)
        toplevel.withdraw()
        toplevel.overrideredirect(True)
        toplevel.minsize(width, 0)
        toplevel.maxsize(width * 2, max_height)
        toplevel.geometry(f"{width}x{max_height}+{x}+{y}")

        return toplevel

    def _create_popup_frame(self, toplevel, popup_state):
        """Create popup frame with scrollable item list."""
        # Outer frame with border and padding
        outer_frame = Frame(toplevel, padding=3, show_border=True)
        outer_frame.pack(fill='both', expand=True)

        # Create scrollview inside the outer frame
        scrollview = ScrollView(
            outer_frame,
            scroll_direction='vertical',
            scrollbar_visibility='always',
        )
        scrollview.pack(fill='both', expand=True)

        # Create inner frame for items
        inner_frame = Frame(scrollview)
        scrollview.add(inner_frame)

        # Make inner frame fill the canvas width
        def on_canvas_configure(event):
            scrollview.canvas.itemconfig(scrollview._window_id, width=event.width)
        scrollview.canvas.bind('<Configure>', on_canvas_configure, add='+')

        # Expand scrollregion to include vertical padding so content doesn't clip borders
        def on_inner_frame_configure(event):
            bbox = scrollview.canvas.bbox('all')
            if bbox:
                x0, y0, x1, y1 = bbox
                padding_y = 1
                scrollview.canvas.configure(scrollregion=(x0, y0 - padding_y, x1, y1 + padding_y))
        inner_frame.bind('<Configure>', on_inner_frame_configure, add='+')

        self._item_labels = []
        current_value = self.value

        # Get accent from Field's _accent attribute, fallback to primary if None
        accent = getattr(self, '_accent', None) or 'primary'

        for i, item in enumerate(self._items):
            btn = Button(
                inner_frame,
                text=item,
                accent=accent,
                variant='selectbox_item',
                command=lambda v=item: self._on_item_click(v, toplevel, popup_state)
            )
            btn.pack(fill='x')

            # Store item value on button for retrieval
            btn._item_value = item
            btn._item_index = i

            # Apply selected state if this is the current value
            if item == current_value:
                btn.state(['selected'])

            self._item_labels.append(btn)

        return scrollview

    def _on_item_click(self, value, toplevel, popup_state):
        """Handle click on item."""
        popup_state['item_was_selected'] = True
        self._set_selected_value(value, toplevel, popup_state)

    def _update_highlight(self, popup_state, new_index):
        """Update the highlighted item in the popup."""
        visible_buttons = [btn for btn in self._item_labels if btn.winfo_manager()]
        if not visible_buttons:
            return

        # Clamp index to valid range
        new_index = max(0, min(new_index, len(visible_buttons) - 1))
        old_index = popup_state['highlighted_index']

        # Remove highlight from old button
        if 0 <= old_index < len(visible_buttons):
            visible_buttons[old_index].state(['!selected'])

        # Add highlight to new button
        visible_buttons[new_index].state(['selected'])
        popup_state['highlighted_index'] = new_index

        # Scroll to make highlighted item visible
        btn = visible_buttons[new_index]
        if self._popup_frame and self._popup_frame.winfo_exists():
            self._popup_frame.canvas.update_idletasks()
            # Get button position relative to canvas
            btn_y = btn.winfo_y()
            btn_height = btn.winfo_height()
            canvas_height = self._popup_frame.canvas.winfo_height()

            # Scroll if needed
            scroll_top = self._popup_frame.canvas.canvasy(0)
            scroll_bottom = scroll_top + canvas_height

            if btn_y < scroll_top:
                self._popup_frame.canvas.yview_moveto(btn_y / self._popup_frame.canvas.bbox('all')[3])
            elif btn_y + btn_height > scroll_bottom:
                target = (btn_y + btn_height - canvas_height) / self._popup_frame.canvas.bbox('all')[3]
                self._popup_frame.canvas.yview_moveto(target)

    def _setup_popup_bindings(self, toplevel, popup_state, close_popup):
        """Setup all event bindings for the popup."""
        # Escape always closes
        toplevel.bind("<Escape>", close_popup)

        # Arrow key navigation
        def on_arrow_down(event):
            self._update_highlight(popup_state, popup_state['highlighted_index'] + 1)
            return 'break'

        def on_arrow_up(event):
            self._update_highlight(popup_state, popup_state['highlighted_index'] - 1)
            return 'break'

        def on_enter(event):
            visible_buttons = [btn for btn in self._item_labels if btn.winfo_manager()]
            idx = popup_state['highlighted_index']
            if 0 <= idx < len(visible_buttons):
                popup_state['item_was_selected'] = True
                self._set_selected_value(visible_buttons[idx]._item_value, toplevel, popup_state)
            return 'break'

        toplevel.bind("<Down>", on_arrow_down)
        toplevel.bind("<Up>", on_arrow_up)
        toplevel.bind("<Return>", on_enter)

        # Also bind to entry widget for search mode
        if self._search_enabled:
            self._setup_search_bindings(toplevel, popup_state, close_popup)
            entry_down = self.entry_widget.bind('<Down>', on_arrow_down, add='+')
            entry_up = self.entry_widget.bind('<Up>', on_arrow_up, add='+')
            entry_enter = self.entry_widget.bind('<Return>', on_enter, add='+')
            popup_state['key_bindings'].append(('<Down>', entry_down))
            popup_state['key_bindings'].append(('<Up>', entry_up))
            popup_state['key_bindings'].append(('<Return>', entry_enter))
        else:
            toplevel.bind("<FocusOut>", close_popup)

        # Apply initial highlight
        self._update_highlight(popup_state, popup_state['highlighted_index'])

    def _setup_search_bindings(self, toplevel, popup_state, close_popup):
        """Setup search-specific event bindings."""
        # Initialize first filtered item
        if self._items:
            popup_state['first_filtered_item'] = self._items[0]
        popup_state['last_search_text'] = self.entry_widget.get().lower()

        # Filter function
        def filter_items(*args):
            if popup_state['popup_closed'] or not self._popup_frame or not self._popup_frame.winfo_exists():
                return

            search_text = self.entry_widget.get().lower()

            # Skip if search text hasn't changed (e.g., arrow key release)
            if search_text == popup_state['last_search_text']:
                return
            popup_state['last_search_text'] = search_text

            # Show/hide buttons based on filter
            first_visible = None
            for btn in self._item_labels:
                if search_text in btn._item_value.lower():
                    btn.pack(fill='x')
                    if first_visible is None:
                        first_visible = btn
                else:
                    btn.pack_forget()

            # Track first filtered item for auto-select
            popup_state['first_filtered_item'] = first_visible._item_value if first_visible else None

            # Reset highlight to first visible item
            self._update_highlight(popup_state, 0)

        # Bind KeyRelease for filtering
        keyrelease_binding = self.entry_widget.bind('<KeyRelease>', lambda e: filter_items(), add='+')
        popup_state['key_bindings'].append(('<KeyRelease>', keyrelease_binding))

        # Bind Tab to select highlighted item
        def on_tab(event):
            if popup_state['popup_closed']:
                return
            visible_buttons = [btn for btn in self._item_labels if btn.winfo_manager()]
            idx = popup_state['highlighted_index']
            if 0 <= idx < len(visible_buttons):
                popup_state['item_was_selected'] = True
                self._set_selected_value(visible_buttons[idx]._item_value, toplevel, popup_state)
            return 'break'

        tab_binding = self.entry_widget.bind('<Tab>', on_tab)
        popup_state['key_bindings'].append(('<Tab>', tab_binding))

        # Setup click-outside detection
        def on_root_click(event):
            x, y = event.x_root, event.y_root

            # Check if click is inside entry widget
            ex, ey = self.entry_widget.winfo_rootx(), self.entry_widget.winfo_rooty()
            ew, eh = self.entry_widget.winfo_width(), self.entry_widget.winfo_height()
            if ex <= x <= ex + ew and ey <= y <= ey + eh:
                return

            # Check if click is inside toplevel
            if toplevel.winfo_exists():
                tx, ty = toplevel.winfo_rootx(), toplevel.winfo_rooty()
                tw, th = toplevel.winfo_width(), toplevel.winfo_height()
                if tx <= x <= tx + tw and ty <= y <= ty + th:
                    return

            close_popup()

        def bind_click():
            if popup_state['popup_closed']:
                return
            root = self.winfo_toplevel()
            bind_id = root.bind('<Button-1>', on_root_click, add='+')
            popup_state['entry_focus_handler'] = bind_id

        self.after(100, bind_click)

    def _close_popup(self, toplevel, popup_state):
        """Close the popup and cleanup bindings."""
        if popup_state['popup_closed']:
            return

        popup_state['popup_closed'] = True
        self._popup_open = False

        # Unbind handlers
        if popup_state['entry_focus_handler'] is not None and self._search_enabled:
            root = self.winfo_toplevel()
            root.unbind('<Button-1>', popup_state['entry_focus_handler'])

        # Unbind key bindings
        for sequence, funcid in popup_state['key_bindings']:
            self.entry_widget.unbind(sequence, funcid)

        # Destroy toplevel
        if toplevel.winfo_exists():
            toplevel.destroy()

        # Clean up popup references
        self._popup_frame = None
        self._item_labels = []

        # Handle value selection for search mode without custom values
        if self._search_enabled and not self._allow_custom_values:
            if not popup_state['item_was_selected']:
                if popup_state['first_filtered_item'] is not None:
                    self._last_selected_value = popup_state['first_filtered_item']
                    self.value = popup_state['first_filtered_item']

    def _set_selected_value(self, selected_value, toplevel, popup_state):
        """Set the selected value and close the popup."""
        if selected_value is None:
            return

        self._last_selected_value = selected_value
        self.value = selected_value
        self._close_popup(toplevel, popup_state)

    @configure_delegate('items')
    def _delegate_items(self, value: list[str] = None):
        """Get or set the available items for the SelectBox."""
        if value is None:
            return self._items
        else:
            self._items = value or []
        return None

    @configure_delegate('allow_custom_values')
    def _delegate_allow_custom_values(self, value: bool = None):
        """Get or set whether free-form text entry is allowed."""
        if value is None:
            return self._allow_custom_values
        else:
            self._allow_custom_values = value
            if value or self._search_enabled:
                self.entry_widget.state(['!readonly'])
            else:
                self.readonly(True)
        return None

    @configure_delegate('enable_search')
    def _delegate_enable_search(self, value: bool = None):
        """Get or set whether search filtering is enabled."""
        if value is None:
            return self._search_enabled
        else:
            self._search_enabled = value
            if value or self._allow_custom_values:
                self.entry_widget.state(['!readonly'])
            else:
                self.readonly(True)
        return None

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        if value is not None:
            return self.value
        else:
            self.value = value
            return None

    @property
    def selected_index(self):
        """Get or set the selected index.

        Returns -1 if the current value is not in the items list.
        Setting to -1 or None clears the selection.
        """
        try:
            return self._items.index(self.value)
        except (ValueError, TypeError):
            return -1

    @selected_index.setter
    def selected_index(self, index):
        if index is None or index == -1:
            self.value = ""
        elif 0 <= index < len(self._items):
            self.value = self._items[index]
        else:
            raise IndexError(f"index {index} out of range for {len(self._items)} items")

    @property
    def value(self):
        """Get or set the selected value."""
        return Field.value.fget(self)

    @value.setter
    def value(self, value):
        """Set the selected value and emit ``<<Change>>`` when it differs."""
        prev_value = Field.value.fget(self)
        Field.value.fset(self, value)
        new_value = Field.value.fget(self)
        if new_value != prev_value:
            self.entry_widget._prev_changed_value = new_value
            if not getattr(self, "_suppress_changed_event", False):
                self.entry_widget.event_generate(
                    '<<Change>>',
                    data={
                        'value': new_value,
                        'prev_value': prev_value,
                        'text': self.entry_widget.get()
                    },
                    when="tail"
                )

