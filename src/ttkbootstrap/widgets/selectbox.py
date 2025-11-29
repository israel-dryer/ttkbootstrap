from tkinter import Toplevel

from typing_extensions import Unpack

from ttkbootstrap.widgets.button import Button
from ttkbootstrap.widgets.field import Field, FieldOptions
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.treeview import Treeview


class SelectBox(Field):
    """Dropdown-like field widget built on top of :class:`Field`.

    A SelectBox renders a standard field with a suffix button that opens a small
    popup window containing a ``Treeview`` of the available items. Selecting an
    item updates the field value and emits ``<<Changed>>`` so consumers can
    react to both user-driven and programmatic value updates.

    Features:
        - Inline dropdown button that opens a popup list of items
        - Uses the underlying entry widget for value storage and events
        - Emits ``<<Changed>>`` when the selection changes (user or code)
        - Items can be configured at runtime via ``configure(items=[...])``
    """

    def __init__(
            self,
            master=None,
            value: str = None,
            items: list[str] = None,
            label: str = None,
            message: str = None,
            allow_custom_values: bool = False,
            **kwargs: Unpack[FieldOptions]
    ):
        """Create a SelectBox widget.

        Args:
            master: Parent widget or window.
            value: Initial selected value; should typically be present in ``items``.
            items: Sequence of string options to present in the popup list.
            label: Optional label text shown above the field.
            message: Optional helper/error message shown below the field.
            allow_custom_values: If True, the entry is editable so users can type
                arbitrary values in addition to choosing from the list.
            **kwargs: Additional :class:`FieldOptions` forwarded to ``Field`` and
                the underlying entry (e.g., ``bootstyle``, ``width``, ``textvariable``).
        """
        super().__init__(master, value=value, label=label, message=message, **kwargs)

        self._allow_custom_values = allow_custom_values
        self.readonly(not allow_custom_values)

        self._items = items or []
        self._button_pack = {}
        self.insert_addon(
            Button,
            position="after",
            name="dropdown",
            icon="chevron-down",
            command=self._show_selection_options
        )

    def _show_selection_options(self):
        """Create and display the popup list of selectable items."""
        if not self._items:
            return

        # Make sure this widget's geometry is up to date
        self.update_idletasks()

        # Get absolute screen position for the SelectBox
        x = self.winfo_rootx() + 4
        y = self.entry_widget.winfo_rooty() + self.entry_widget.winfo_height() + 6

        width = self.winfo_width() - 8

        toplevel = Toplevel(self)
        toplevel.withdraw()
        toplevel.overrideredirect(True)

        # Set min width and initial geometry
        toplevel.minsize(width, 0)
        # height will grow with the Treeview; we just care about x/y and width
        toplevel.geometry(f"+{x}+{y}")

        # close when focus leaves the popup
        def close_popup(event=None):
            if toplevel.winfo_exists():
                toplevel.destroy()

        toplevel.bind("<FocusOut>", close_popup)
        toplevel.bind("<Escape>", close_popup)

        tree = Treeview(toplevel, bootstyle=self._bootstyle, show="tree", height=5, columns=['label'])
        tree.column("#0", width=0, stretch=False)
        tree.pack(fill="both", expand=1)

        selected = 0
        for i, item in enumerate(self._items):
            tree.insert('', 'end', i, text=item, values=(item,))
            if item == self.value:
                selected = i

        tree.selection_set(selected)
        tree.focus(selected)
        tree.see(selected)

        # Bind after idle so initial selection doesn't close the popup
        self.after_idle(
            lambda: tree.bind(
                '<<TreeviewSelect>>',
                lambda e: self._get_selected_item(tree, toplevel)
            )
        )

        toplevel.deiconify()
        toplevel.lift()
        toplevel.focus_force()

    @configure_delegate('items')
    def _config_items(self, value: list[str] = None):
        """Get or set the available items for the SelectBox."""
        if value is None:
            return self._items
        else:
            self._items = value or []
        return None

    @configure_delegate('allow_custom_values')
    def _config_allow_custom_values(self, value: bool = None):
        """Get or set whether free-form text entry is allowed."""
        if value is None:
            return self._allow_custom_values
        else:
            self._allow_custom_values = value
            self.readonly(not value)
        return None

    @property
    def value(self):
        """Get or set the selected value."""
        return Field.value.fget(self)

    @value.setter
    def value(self, value):
        """Set the selected value and emit ``<<Changed>>`` when it differs."""
        prev_value = Field.value.fget(self)
        Field.value.fset(self, value)
        new_value = Field.value.fget(self)
        if new_value != prev_value:
            # keep change tracking in sync and emit <<Changed>> for programmatic updates
            self.entry_widget._prev_changed_value = new_value
            if not getattr(self, "_suppress_changed_event", False):
                self.entry_widget.event_generate(
                    '<<Changed>>',
                    data={
                        'value': new_value,
                        'prev_value': prev_value,
                        'text': self.entry_widget.get()
                    },
                    when="tail"
                )

    def _get_selected_item(self, tree, top):
        """Handle item selection from the popup Treeview."""
        item_id = tree.selection()[0]
        self.value = tree.item(item_id, "text")
        top.destroy()
