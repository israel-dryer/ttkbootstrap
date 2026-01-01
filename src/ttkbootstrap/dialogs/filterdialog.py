"""FilterDialog - A dialog for filtering and selecting multiple items from a list.

This module provides a multi-select dialog with optional search and select-all
functionality. Items can be displayed with checkboxes, and the dialog supports
both standard and frameless (borderless) display modes.
"""

from tkinter import Widget
from typing import Any, Callable, Literal, Optional, Tuple, Union
from types import SimpleNamespace

from ttkbootstrap.widgets.primitives import CheckButton, Frame, Label, Separator
from ttkbootstrap.widgets.types import Master
from ttkbootstrap.widgets.composites.textentry import TextEntry
from ttkbootstrap.runtime.app import Window
from ttkbootstrap.dialogs import Dialog, DialogButton
from ttkbootstrap.widgets.composites.scrollview import ScrollView
from ttkbootstrap.runtime.window_utilities import AnchorPoint

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
            master: Master = None,
            enable_search: bool = False,
            enable_select_all: bool = False,
            items: list[str | dict[str, Any]] = None
    ):
        """Initialize the FilterDialogContent frame.

        Args:
            master: Parent widget. If None, uses the default root window.
            enable_search: If True, includes a search box to filter items by text.
            enable_select_all: If True, includes a "Select All" checkbox.
            items: List of items to display. Can be strings or dicts with keys:
                - text (str): Display text (required for dict items)
                - value (Any): Value to return when selected (defaults to text)
                - selected (bool): Initial selection state (defaults to False)
        """
        super().__init__(master)
        self._enable_search = enable_search
        self._enable_select_all = enable_select_all
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
        if self._enable_search:
            search_entry = ttk.TextEntry(self)
            search_entry.insert_addon(ttk.Label, 'before', icon='search')
            search_entry.pack(fill='x')
            search_entry.on_input(self._on_search_input)

        # Select all checkbox
        if self._enable_select_all:
            self._select_all_cb = ttk.Checkbutton(self, text='edit.select_all')
            self._select_all_cb.invoke()
            self._select_all_cb.invoke()
            self._select_all_cb['command'] = self._handle_select_all
            self._select_all_cb.pack(fill='x', padx=8, pady=(12, 8))
            ttk.Separator(self).pack(fill='x')

        # Scrollable container for checkboxes
        scroll_view = ScrollView(
            self,
            scroll_direction='vertical',
            scrollbar_visibility='always'
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

    !!! note "Events"

        ``<<SelectionChange>>``: Triggered when OK is clicked and selections are confirmed.
          Provides ``event.data`` with key: ``selected`` (list[Any]).

    Attributes:
        result (list[Any] | None): List of selected values after dialog is closed,
            or None if canceled.
    """

    def __init__(
            self,
            master: Master = None,
            title: str = "Filter",
            items: list[str | dict[str, Any]] = None,
            enable_search: bool = False,
            enable_select_all: bool = False,
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
            enable_search: If True, includes a search box to filter items by text.
            enable_select_all: If True, includes a "Select All" checkbox.
            frameless: If True, removes window decorations and displays with a
                border frame. Enables dismiss-on-outside-click behavior.
        """
        super().__init__(master)
        self._master = master if master else self.master
        self._title = title
        self._items = items or []
        self._enable_search = enable_search
        self._enable_select_all = enable_select_all
        self._frameless = frameless
        self._content: FilterDialogContent | None = None
        self._dialog: Dialog | None = None
        self.result: list[Any] | None = None

    def _build_content(self, parent):
        """Build the dialog content with FilterDialogContent."""
        self._content = FilterDialogContent(
            master=parent,
            enable_search=self._enable_search,
            enable_select_all=self._enable_select_all,
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
                self.event_generate('<<SelectionChange>>', data={"selected": self.result.copy()})

    def on_selection_changed(self, callback: Callable) -> str:
        """Bind to ``<<SelectionChange>>``. Callback receives ``event.data = {"selected": list[Any]}``.

        Returns:
            Binding identifier for use with off_selection_changed().
        """
        return self.bind('<<SelectionChange>>', callback, add=True)

    def off_selection_changed(self, bind_id: str = None):
        """Unbind callback from <<SelectionChange>> event.

        Args:
            bind_id: Binding identifier from on_selection_changed().
        """
        self.unbind('<<SelectionChange>>', bind_id)

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

    def show(
            self,
            position: Optional[Tuple[int, int]] = None,
            modal: Optional[bool] = None,
            *,
            anchor_to: Optional[Union[Widget, Literal["screen", "cursor", "parent"]]] = None,
            anchor_point: AnchorPoint = 'center',
            window_point: AnchorPoint = 'center',
            offset: Tuple[int, int] = (0, 0),
            auto_flip: Union[bool, Literal['vertical', 'horizontal']] = False
    ) -> Optional[list[Any]]:
        """Show the dialog and return the selected items.

        Args:
            position: Optional (x, y) coordinates to position the dialog.
                If provided, takes precedence over anchor-based positioning.
            modal: Override the mode's default modality.
                If None, uses True (modal mode).
            anchor_to: Positioning target. Can be:
                - Widget: Anchor to a specific widget
                - "screen": Anchor to screen edges/corners
                - "cursor": Anchor to mouse cursor location
                - "parent": Anchor to parent window (same as widget)
                - None: Centers on parent (default)
            anchor_point: Point on the anchor target (n, s, e, w, ne, nw, se, sw, center).
                Default 'center'.
            window_point: Point on the dialog window (n, s, e, w, ne, nw, se, sw, center).
                Default 'center'.
            offset: Additional (x, y) offset in pixels from the anchor position.
            auto_flip: Smart positioning to keep window on screen.
                - False: No flipping (default)
                - True: Flip both vertically and horizontally as needed
                - 'vertical': Only flip up/down
                - 'horizontal': Only flip left/right

        Returns:
            List of selected item values, or None if canceled.
        """
        self._dialog: Dialog = Dialog(
            master=self._master,
            title=self._title,
            content_builder=self._build_content,
            buttons=[
                DialogButton(text="button.cancel", role="cancel", result=None),
                DialogButton(
                    text="button.ok",
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

        self._dialog.show(
            position=position,
            modal=modal,
            anchor_to=anchor_to,
            anchor_point=anchor_point,
            window_point=window_point,
            offset=offset,
            auto_flip=auto_flip
        )
        return self.result
