"""FilterDialog - A dialog for filtering and selecting multiple items from a list.

This module provides a multi-select dialog with optional search and select-all
functionality. Items can be displayed with checkboxes, and the dialog supports
both standard and frameless (borderless) display modes.
"""

from typing import Any
from types import SimpleNamespace

from ttkbootstrap.widgets.primitives import CheckButton, Frame, Label, Separator
from ttkbootstrap.widgets.composites.textentry import TextEntry
from ttkbootstrap.api.window import Window
from ttkbootstrap.dialogs import Dialog, DialogButton
from ttkbootstrap.widgets.composites.scrollview import ScrollView

ttk = SimpleNamespace(
    Checkbutton=CheckButton,
    Frame=Frame,
    Label=Label,
    Separator=Separator,
    TextEntry=TextEntry,
    Window=Window,
)


class FilterDialogContent(ttk.Frame):
    """Internal content frame for FilterDialog.

    This frame contains the search box, select-all checkbox, and scrollable
    list of checkboxes for filtering items.
    """

    def __init__(
            self,
            master=None,
            allow_search: bool = False,
            allow_select_all: bool = False,
            items: list[str | dict[str, Any]] = None
    ):
        """Initialize the FilterDialogContent frame.

        Args:
            master: Parent widget. If None, uses the default root window.
            allow_search: If True, includes a search box to filter items by text.
            allow_select_all: If True, includes a "Select All" checkbox.
            items: List of items to display. Can be strings or dicts with keys:
                - text (str): Display text (required for dict items)
                - value (Any): Value to return when selected (defaults to text)
                - selected (bool): Initial selection state (defaults to False)
        """
        super().__init__(master)
        self._allow_search = allow_search
        self._allow_select_all = allow_select_all
        self._selected_items = []
        self._items = self._normalize_items(items)
        self._filter: str | None = None
        self._check_buttons: dict[str, ttk.Checkbutton] = {}
        self._select_all_cb: ttk.Checkbutton | None = None
        self._scroll_container: ttk.Frame | None = None
        self._build_content()

    def _normalize_items(self, items: list[str | dict[str, Any]] | None) -> list[dict[str, Any]]:
        """Normalize items to a consistent dict format.

        Args:
            items: List of strings or dicts representing items.

        Returns:
            List of dicts with 'text', 'value', and 'selected' keys.

        Raises:
            ValueError: If a dict item is missing the 'text' key.
        """
        if items is None:
            return []

        out = []
        for item in items:
            if isinstance(item, str):
                out.append(dict(text=item, value=item, selected=False))
            else:
                if 'text' not in item:
                    raise ValueError('Item must have "text" key')

                if 'selected' not in item:
                    item['selected'] = False
                item.setdefault('value', item['text'])
                if item['selected']:
                    self._selected_items.append(item['value'])
                out.append(item)
        return out

    def _build_content(self):
        """Build and layout all UI components."""
        # Search box
        if self._allow_search:
            search_entry = ttk.TextEntry(self)
            search_entry.insert_addon(ttk.Label, 'before', icon='search')
            search_entry.pack(fill='x')
            search_entry.on_input(self._on_search_input)

        # Select all checkbox
        if self._allow_select_all:
            self._select_all_cb = ttk.Checkbutton(self, text='Select All')
            self._select_all_cb.invoke()
            self._select_all_cb.invoke()
            self._select_all_cb['command'] = self._handle_select_all
            self._select_all_cb.pack(fill='x', padx=8, pady=(12, 8))
            ttk.Separator(self).pack(fill='x')

        # Scrollable container for checkboxes
        scroll_view = ScrollView(
            self,
            direction='vertical',
            show_scrollbar='always'
        )
        scroll_view.pack(fill='both', expand=False, pady=(8, 0))
        scroll_view.configure(height=230)

        self._scroll_container = ttk.Frame(scroll_view.canvas)
        scroll_view.add(self._scroll_container)

        # Stretch container frame to canvas width for full-width checkboxes
        def _configure_scroll_width(event):
            scroll_view.canvas.itemconfig(scroll_view._window_id, width=event.width)
        scroll_view.canvas.bind('<Configure>', _configure_scroll_width)

        # Add item checkboxes
        for item in self._items:
            cb = ttk.Checkbutton(self._scroll_container, text=item['text'])
            cb.invoke()
            if not item['selected']:
                cb.invoke()
            cb['command'] = lambda value=item['value']: self._on_item_clicked(value)
            cb.pack(fill='x', padx=8, pady=8)
            self._check_buttons[item['text']] = cb

    def _handle_select_all(self):
        """Toggle selection state of all checkboxes."""
        if 'selected' in self._select_all_cb.state():
            for item in self._check_buttons.values():
                item.instate(['!selected'], item.invoke)
        else:
            for item in self._check_buttons.values():
                item.instate(['selected'], item.invoke)

    def _on_search_input(self, event):
        """Filter visible checkboxes based on search text."""
        self._filter = (event.data['text'] or '').lower()

        for key, cb in self._check_buttons.items():
            if self._filter in key.lower():
                cb.pack(fill='x', padx=8, pady=8)
            else:
                cb.pack_forget()

    def _on_item_clicked(self, value):
        """Update selected items list when a checkbox is clicked."""
        if value in self._selected_items:
            self._selected_items.remove(value)
        else:
            self._selected_items.append(value)

    def get_selected_items(self):
        """Return the list of selected item values."""
        return self._selected_items


class FilterDialog(ttk.Frame):
    """A dialog for filtering and selecting multiple items from a list.

    This dialog displays a list of checkboxes with optional search and select-all
    functionality. When the user clicks OK, the selected values are stored in
    the result property.

    Events:
        <<SelectionChanged>>: Triggered when OK is clicked and selections are confirmed.
            event.data = {"selected": list[Any]}

    Args:
        master: Parent widget for the dialog. If None, uses the default root window.
        title: Dialog window title. Defaults to "Filter".
        items: List of items to display. Can be strings or dicts with keys:
            - text (str): Display text (required for dict items)
            - value (Any): Value to return when selected (defaults to text)
            - selected (bool): Initial selection state (defaults to False)
        allow_search: If True, adds a search box to filter items by text.
            Defaults to False.
        allow_select_all: If True, adds a "Select All" checkbox at the top.
            Defaults to False.
        frameless: If True, removes window decorations (title bar, borders) and
            displays the dialog with a border frame. Useful for dropdown-style
            menus. Enables dismiss-on-outside-click behavior. Defaults to False.

    Attributes:
        result: List of selected values after dialog is closed, or None if cancelled.

    Example:
        Basic usage:

        >>> import ttkbootstrap as ttk
        >>> from ttkbootstrap.dialogs import FilterDialog
        >>>
        >>> root = ttk.Window()
        >>> dialog = FilterDialog(
        ...     master=root,
        ...     title="Select Colors",
        ...     items=["Red", "Green", "Blue", "Yellow"],
        ...     allow_search=True,
        ...     allow_select_all=True
        ... )
        >>> result = dialog.show()
        >>> print(result)  # e.g., ['Red', 'Blue'] or None if cancelled

        With pre-selected items:

        >>> items = [
        ...     {"text": "Red", "value": "red"},
        ...     {"text": "Green", "value": "green", "selected": True},
        ...     {"text": "Blue", "value": "blue", "selected": True}
        ... ]
        >>> dialog = FilterDialog(master=root, items=items)
        >>> result = dialog.show()
        >>> print(result)  # e.g., ['green', 'blue']

        Frameless popover style:

        >>> dialog = FilterDialog(
        ...     master=root,
        ...     items=["Option 1", "Option 2", "Option 3"],
        ...     frameless=True
        ... )
        >>> result = dialog.show()

        With selection change event:

        >>> def on_selection(event):
        ...     print(f"Selected: {event.data['selected']}")
        >>>
        >>> dialog = FilterDialog(master=root, items=["Red", "Green", "Blue"])
        >>> dialog.on_selection_changed(on_selection)
        >>> dialog.show()
    """

    def __init__(
            self,
            master=None,
            title: str = "Filter",
            items: list[str | dict[str, Any]] = None,
            allow_search: bool = False,
            allow_select_all: bool = False,
            frameless: bool = False
    ):
        """Initialize the FilterDialog.

        Args:
            master: Parent widget. If None, uses the default root window.
            title: Dialog window title.
            items: List of items to display. Can be strings or dicts with keys:
                - text (str): Display text (required for dict items)
                - value (Any): Value to return when selected (defaults to text)
                - selected (bool): Initial selection state (defaults to False)
            allow_search: If True, includes a search box to filter items by text.
            allow_select_all: If True, includes a "Select All" checkbox.
            frameless: If True, removes window decorations and displays with a
                border frame. Enables dismiss-on-outside-click behavior.
        """
        super().__init__(master)
        self._master = master if master else self.master
        self._title = title
        self._items = items or []
        self._allow_search = allow_search
        self._allow_select_all = allow_select_all
        self._frameless = frameless
        self._content: FilterDialogContent | None = None
        self._dialog: Dialog | None = None
        self.result: list[Any] | None = None

    def _build_content(self, parent):
        """Build the dialog content with FilterDialogContent."""
        self._content = FilterDialogContent(
            master=parent,
            allow_search=self._allow_search,
            allow_select_all=self._allow_select_all,
            items=self._items
        )
        padding = 0 if self._frameless else 10
        self._content.pack(fill='both', expand=True, padx=padding, pady=padding)

        # Setup dismiss-on-click for frameless after dialog is built
        if self._frameless:
            parent.after(10, self._setup_frameless_dismiss)

    def _on_ok(self, dialog: Dialog):
        """Save selected items to result when OK button is clicked."""
        if self._content:
            self.result = self._content.get_selected_items()
            # Generate selection changed event on confirmation
            if self.result is not None:
                self.event_generate('<<SelectionChanged>>', data={"selected": self.result.copy()})

    def on_selection_changed(self, callback):
        """Bind callback to <<SelectionChanged>> event.

        Args:
            callback: Function receiving event with event.data = {"selected": list}

        Returns:
            Binding identifier for use with off_selection_changed().
        """
        return self.bind('<<SelectionChanged>>', callback, add=True)

    def off_selection_changed(self, funcid: str = None):
        """Unbind callback from <<SelectionChanged>> event.

        Args:
            funcid: Binding identifier from on_selection_changed().
        """
        self.unbind('<<SelectionChanged>>', funcid)

    def _on_click(self, event):
        """Check if click is outside dialog and dismiss if so."""
        if not self._dialog or not self._dialog.toplevel:
            return

        try:
            # Get dialog window bounds
            x = self._dialog.toplevel.winfo_rootx()
            y = self._dialog.toplevel.winfo_rooty()
            w = self._dialog.toplevel.winfo_width()
            h = self._dialog.toplevel.winfo_height()

            # Check if click is outside dialog
            if not (x <= event.x_root <= x + w and y <= event.y_root <= y + h):
                self._dialog.toplevel.destroy()
        except:
            pass

    def _setup_frameless_dismiss(self):
        """Setup dismiss-on-outside-click for frameless dialogs."""
        if self._frameless and self._dialog and self._dialog.toplevel:
            # Bind to root window to catch all clicks
            root = self._dialog.toplevel.winfo_toplevel()
            while root.master:
                root = root.master.winfo_toplevel()
            root.bind('<Button-1>', self._on_click, add='+')

    def show(self, position: tuple[int, int] | None = None):
        """Show the dialog and return the selected items.

        Args:
            position: Optional (x, y) coordinates to position the dialog.
                If None, the dialog will be centered on the parent.

        Returns:
            List of selected item values, or None if cancelled.
        """
        self._dialog = Dialog(
            master=self._master,
            title=self._title,
            content_builder=self._build_content,
            buttons=[
                DialogButton(text="Cancel", role="cancel", result=None),
                DialogButton(
                    text="OK",
                    role="primary",
                    result=True,
                    default=True,
                    command=self._on_ok
                )
            ],
            minsize=(250, 200),
            maxsize=(250, 380),
            resizable=(False, True),
            mode="modal",
            frameless=self._frameless
        )

        self._dialog.show(position=position)
        return self.result
