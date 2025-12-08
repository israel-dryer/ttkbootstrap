from typing import Any, Literal

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Dialog, DialogButton
from ttkbootstrap import ScrollView


class FilterDialogContent(ttk.Frame):

    def __init__(
            self,
            master=None,
            allow_search: bool = False,
            allow_select_all: bool = False,
            items: list[str | dict[str, Any]] = None
    ):
        super().__init__(master)
        self._allow_search = allow_search
        self._allow_select_all = allow_select_all

        # always includes the 'value' or 'text' if value is not provided.
        self._selected_items = []

        # If filter is a dict, then is can have {"text": str, "value": Any, "selected": bool}
        self._items = self._normalize_items(items)

        self._filter: str | dict | None = None

        self._check_buttons: dict[str, ttk.Checkbutton] = {}
        self._select_all_cb: ttk.Checkbutton | None = None
        self._scroll_container: ttk.Frame | None = None
        self._build_content()

    def _normalize_items(self, items: list[str | dict[str, Any]] | None) -> list[dict[str, Any]]:
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

        # add search
        if self._allow_search:
            search_entry = ttk.TextEntry(self)
            search_entry.insert_addon(ttk.Label, 'before', icon='search')
            search_entry.pack(fill='x')
            search_entry.on_input(self._on_search_input)

        # add select all
        if self._allow_select_all:
            self._select_all_cb = ttk.Checkbutton(self, text='Select All')
            self._select_all_cb.invoke()
            self._select_all_cb.invoke()
            self._select_all_cb['command'] = self._handle_select_all
            self._select_all_cb.pack(fill='x', padx=8, pady=(12, 8))
            ttk.Separator(self).pack(fill='x')

        # Create scrollable container for checkboxes
        scroll_view = ScrollView(
            self,
            direction='vertical',
            show_scrollbar='always'
        )
        # Set a specific height instead of expand to leave room for footer
        scroll_view.pack(fill='both', expand=False, pady=(8, 0))
        scroll_view.configure(height=230)

        # Container frame inside scroll view
        self._scroll_container = ttk.Frame(scroll_view.canvas)
        scroll_view.add(self._scroll_container)

        # add items to scrollable container
        for item in self._items:
            cb = ttk.Checkbutton(self._scroll_container, text=item['text'])
            cb.invoke()
            if not item['selected']:
                cb.invoke()
            cb['command'] = lambda value=item['value']: self._on_item_clicked(value)
            cb.pack(fill='x', padx=8, pady=8)
            self._check_buttons[item['text']] = cb

    def _handle_select_all(self):
        if 'selected' in self._select_all_cb.state():
            for item in self._check_buttons.values():
                item.instate(['!selected'], item.invoke)
        else:
            for item in self._check_buttons.values():
                item.instate(['selected'], item.invoke)

    def _on_search_input(self, event):
        self._filter = (event.data['text'] or '').lower()
        print('Filter', self._filter)

        for key, cb in self._check_buttons.items():
            print("Evaluating filter for ", key)
            if self._filter in key.lower():
                cb.pack(fill='x', padx=8, pady=8)
            else:
                cb.pack_forget()

    def _on_item_clicked(self, value):
        if value in self._selected_items:
            self._selected_items.remove(value)
        else:
            self._selected_items.append(value)

        print(self._selected_items)

    def get_selected_items(self):
        """Return the list of selected item values."""
        return self._selected_items


class FilterDialog:
    """A dialog for filtering and selecting multiple items from a list.

    This dialog displays a list of checkboxes with optional search and select-all
    functionality. When the user clicks OK, the selected values are stored in
    the result property.

    Args:
        master: Parent widget for the dialog
        title: Dialog window title
        items: List of items to display. Can be strings or dicts with keys:
            - text: Display text (required)
            - value: Value to return when selected (defaults to text)
            - selected: Initial selection state (defaults to False)
        allow_search: If True, adds a search box to filter items
        allow_select_all: If True, adds a "Select All" checkbox
        frameless: If True, hides the window decorations and shows a border

    Example:
        >>> dialog = FilterDialog(
        ...     master=root,
        ...     title="Filter Options",
        ...     items=["Red", "Green", {"text": "Blue", "selected": True}],
        ...     allow_search=True,
        ...     allow_select_all=True
        ... )
        >>> dialog.show()
        >>> print(dialog.result)  # ['Blue'] or None if cancelled
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
        self._master = master
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

    def _on_ok(self, dialog: Dialog):
        """Handle OK button click - save selected items to result."""
        if self._content:
            self.result = self._content.get_selected_items()

    def show(self):
        """Show the dialog and return the selected items when closed."""
        # Use popover mode when frameless for dismiss on outside click
        dialog_mode: Literal['modal', 'popover'] = "popover" if self._frameless else "modal"

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
            mode=dialog_mode,
            frameless=self._frameless
        )

        self._dialog.show()
        return self.result
