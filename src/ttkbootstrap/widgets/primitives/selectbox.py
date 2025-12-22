from tkinter import Toplevel

from typing_extensions import Unpack

from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.composites.field import Field, FieldOptions
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.primitives.treeview import TreeView


class SelectBox(Field):
    """Dropdown-like field widget built on top of Field.

    Renders a field with a suffix button that opens a popup Treeview of available
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
            master=None,
            value: str = None,
            items: list[str] = None,
            label: str = None,
            message: str = None,
            allow_custom_values: bool = False,
            show_dropdown_button: bool = True,
            dropdown_button_icon: str = None,
            search_enabled: bool = False,
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
            search_enabled (bool): If True, allows typing in the entry to filter the popup list.
                When combined with allow_custom_values=False, the first filtered item is selected
                when the popup closes. With allow_custom_values=True, any typed value is kept.

        Other Parameters:
            allow_blank (bool): If True, empty input is allowed.
            bootstyle (str): The accent color of the focus ring and active border.
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
        self._search_enabled = search_enabled
        self._items = items or []
        self._last_selected_value = value
        self._popup_open = False
        self._dropdown_button_icon = dropdown_button_icon or 'chevron-down'

        # Configure entry state based on search and custom value settings
        if allow_custom_values or search_enabled:
            self.entry_widget.state(['!readonly'])
        else:
            self.readonly(True)
            self.after_idle(self._bind_readonly_selection_on_click)

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
            'filtering_in_progress': False
        }

        # Setup close handler
        def close_popup(event=None):
            self._close_popup(toplevel, popup_state)

        # Create and populate treeview
        tree = self._create_treeview(toplevel)
        self._populate_treeview(tree)

        # Setup event bindings based on mode
        self._setup_popup_bindings(toplevel, tree, popup_state, close_popup)

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

        toplevel = Toplevel(self)
        toplevel.withdraw()
        toplevel.overrideredirect(True)
        toplevel.minsize(width, 0)
        toplevel.geometry(f"+{x}+{y}")

        return toplevel

    def _create_treeview(self, toplevel):
        """Create and configure the treeview widget."""
        tree = TreeView(toplevel, bootstyle=self._bootstyle, show="tree", height=5, columns=['label'])
        tree.column("#0", width=0, stretch=False)
        tree.pack(fill="both", expand=1)
        return tree

    def _populate_treeview(self, tree):
        """Populate treeview with items and select current value."""
        selected = 0
        for i, item in enumerate(self._items):
            tree.insert('', 'end', i, text=item, values=(item,))
            if item == self.value:
                selected = i

        tree.selection_set(selected)
        if not self._search_enabled:
            tree.focus(selected)
        tree.see(selected)

    def _setup_popup_bindings(self, toplevel, tree, popup_state, close_popup):
        """Setup all event bindings for the popup."""
        # Escape always closes
        toplevel.bind("<Escape>", close_popup)

        # Setup mode-specific bindings
        if self._search_enabled:
            self._setup_search_bindings(toplevel, tree, popup_state, close_popup)
        else:
            toplevel.bind("<FocusOut>", close_popup)

        # Setup selection handler
        self._setup_selection_handler(tree, toplevel, popup_state)

    def _setup_search_bindings(self, toplevel, tree, popup_state, close_popup):
        """Setup search-specific event bindings."""
        # Initialize first filtered item
        if self._items:
            popup_state['first_filtered_item'] = self._items[0]

        # Filter function
        def filter_items(*args):
            if popup_state['popup_closed'] or not tree.winfo_exists():
                return

            popup_state['filtering_in_progress'] = True
            search_text = self.entry_widget.get().lower()

            # Clear and repopulate tree with filtered items
            for child in tree.get_children():
                tree.delete(child)

            first_match = None
            first_match_text = None
            for i, item in enumerate(self._items):
                if search_text in item.lower():
                    iid = tree.insert('', 'end', i, text=item, values=(item,))
                    if first_match is None:
                        first_match = iid
                        first_match_text = item

            popup_state['first_filtered_item'] = first_match_text

            if first_match:
                tree.selection_set(first_match)
                tree.see(first_match)

            popup_state['filtering_in_progress'] = False

        # Bind KeyRelease for filtering
        keyrelease_binding = self.entry_widget.bind('<KeyRelease>', lambda e: filter_items(), add='+')
        popup_state['key_bindings'].append(('<KeyRelease>', keyrelease_binding))

        # Bind Tab/Enter to select when custom values not allowed
        if not self._allow_custom_values:
            def on_tab_or_enter(event):
                if popup_state['popup_closed'] or not tree.winfo_exists():
                    return  # Allow default behavior

                selection = tree.selection()
                if selection:
                    popup_state['item_was_selected'] = True
                    self._get_selected_item(tree, toplevel)
                return 'break'

            tab_binding = self.entry_widget.bind('<Tab>', on_tab_or_enter)
            enter_binding = self.entry_widget.bind('<Return>', on_tab_or_enter)
            popup_state['key_bindings'].append(('<Tab>', tab_binding))
            popup_state['key_bindings'].append(('<Return>', enter_binding))

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
                try:
                    tx, ty = toplevel.winfo_rootx(), toplevel.winfo_rooty()
                    tw, th = toplevel.winfo_width(), toplevel.winfo_height()
                    if tx <= x <= tx + tw and ty <= y <= ty + th:
                        return
                except:
                    pass

            close_popup()

        def bind_click():
            if popup_state['popup_closed']:
                return
            root = self.winfo_toplevel()
            bind_id = root.bind('<Button-1>', on_root_click, add='+')
            popup_state['entry_focus_handler'] = bind_id

        self.after(100, bind_click)

    def _setup_selection_handler(self, tree, toplevel, popup_state):
        """Setup handler for item selection in treeview."""

        def bind_selection():
            if not tree.winfo_exists():
                return

            if self._search_enabled:
                # Use click handler to avoid selection events from filtering
                def on_tree_click(e):
                    item = tree.identify_row(e.y)
                    if item:
                        popup_state['item_was_selected'] = True
                        tree.selection_set(item)
                        self._get_selected_item(tree, toplevel)

                tree.bind('<Button-1>', on_tree_click)
            else:
                # Use TreeviewSelect event
                def on_select(e):
                    if popup_state['filtering_in_progress']:
                        return
                    popup_state['item_was_selected'] = True
                    self._get_selected_item(tree, toplevel)

                tree.bind('<<TreeviewSelect>>', on_select)

        self.after_idle(bind_selection)

    def _close_popup(self, toplevel, popup_state):
        """Close the popup and cleanup bindings."""
        if popup_state['popup_closed']:
            return

        popup_state['popup_closed'] = True
        self._popup_open = False

        # Unbind handlers
        if popup_state['entry_focus_handler'] is not None:
            try:
                if self._search_enabled:
                    root = self.winfo_toplevel()
                    root.unbind('<Button-1>', popup_state['entry_focus_handler'])
            except:
                pass

        # Unbind key bindings
        for sequence, funcid in popup_state['key_bindings']:
            try:
                self.entry_widget.unbind(sequence, funcid)
            except:
                pass

        # Destroy toplevel
        if toplevel.winfo_exists():
            toplevel.destroy()

        # Handle value selection for search mode without custom values
        if self._search_enabled and not self._allow_custom_values:
            if not popup_state['item_was_selected']:
                if popup_state['first_filtered_item'] is not None:
                    self._last_selected_value = popup_state['first_filtered_item']
                    self.value = popup_state['first_filtered_item']

    def _get_selected_item(self, tree, toplevel):
        """Handle item selection from the popup Treeview."""
        selection = tree.selection()
        if not selection:
            return

        item_id = selection[0]
        selected_value = tree.item(item_id, "text")
        self._last_selected_value = selected_value
        self.value = selected_value
        self._popup_open = False
        toplevel.destroy()

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

    @configure_delegate('search_enabled')
    def _delegate_search_enabled(self, value: bool = None):
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

