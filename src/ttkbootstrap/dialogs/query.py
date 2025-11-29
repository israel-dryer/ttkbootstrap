"""Query dialogs and querybox facade for data input."""

import textwrap
import tkinter
from datetime import date
from typing import Any, Callable, List, Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.dialogs.date import DateDialog
from ttkbootstrap.dialogs.dialog import Dialog, DialogButton
from ttkbootstrap.dialogs.fontdialog import FontDialog
from ttkbootstrap.dialogs.message import MessageBox
from ttkbootstrap.widgets.textentry import TextEntry
from ttkbootstrap.widgets.numericentry import NumericEntry
from ttkbootstrap.widgets.dateentry import DateEntry

EntryWidget = TextEntry | NumericEntry | DateEntry

class QueryDialog:
    """A modal dialog for collecting user input with validation.

    Emits:
        ``<<DialogResult>>`` with ``event.data = {"result": <value>, "confirmed": True/False}``.
    """

    def __init__(
            self,
            prompt: str,
            title: str = " ",
            value: Any = "",
            minvalue: Optional[Any] = None,
            maxvalue: Optional[Any] = None,
            width: int = 65,
            datatype: Any = str,
            padding: tuple[int, int] | int = (20, 20),
            master: Optional[tkinter.Misc] = None,
            items: Optional[List[str]] = None,
            value_format: Optional[str] = None,
            increment: Optional[int | float] = None,
    ) -> None:
        """Create a query dialog for collecting user input.

        Args:
            prompt: The prompt text to display above the input field. Supports multiline strings.
            title: The dialog window title.
            value: The initial value to populate in the input field.
            value_format: Optional ICU format pattern for formatting/parsing values.
                For numbers: e.g., '$#,##0.00' for currency, '#,##0.##' for decimals
                For dates: e.g., 'shortDate', 'longDate', 'yyyy-MM-dd'
                When provided, uses specialized Field widgets (TextEntry, NumericEntry, DateEntry).
            minvalue: Minimum allowed value for numeric data types. Ignored for strings.
            maxvalue: Maximum allowed value for numeric data types. Ignored for strings.
            increment: Step size for numeric fields (passed to NumericEntry).
            width: Maximum width in characters for text wrapping of the prompt.
            datatype: Expected data type for validation (str, int, float, date, complex).
            padding: Padding around the dialog content.
            master: Parent widget for the dialog.
            items: Optional list of items for dropdown selection. Shows a Combobox instead of Entry.
        """
        self._prompt = prompt
        self._value = value
        self._items = items
        self._minvalue = minvalue
        self._maxvalue = maxvalue
        self._width = width
        self._datatype = datatype
        self._padding = padding
        self._value_format = value_format
        self._increment = increment
        self._entry_widget: Optional[EntryWidget] = None
        self._master = master

        # Create the underlying dialog with inline button specifications
        self._dialog = Dialog(
            master=master,
            title=title,
            content_builder=self._create_content,
            buttons=[
                DialogButton(
                    text=MessageCatalog.translate("Cancel"),
                    role="cancel",
                    result=None,
                ),
                DialogButton(
                    text=MessageCatalog.translate("Submit"),
                    role="primary",
                    default=True,
                    command=lambda dlg: self._on_submit(),
                    closes=False,  # Don't close yet - we need to validate first
                ),
            ],
            minsize=(350, 120),
        )

    def _create_content(self, parent: tkinter.Widget) -> None:
        """Create the dialog body with prompt and input field."""
        frame = ttk.Frame(parent, padding=self._padding)

        # Create prompt label(s)
        if self._prompt:
            for p in self._prompt.split("\n"):
                prompt = "\n".join(textwrap.wrap(p, width=self._width))
                prompt_label = ttk.Label(frame, text=prompt)
                prompt_label.pack(pady=(0, 5), fill=X, anchor=N)

        # Create appropriate input field based on datatype and options
        if self._items is not None and len(self._items) > 0:
            # Combobox for item selection
            entry = ttk.Combobox(master=frame, values=self._items)
            entry.bind("<KeyRelease>", self._on_filter_list)
            if self._value:
                entry.set(self._value)
        elif self._datatype == date:
            # DateEntry for date input
            kwargs = {"value": self._value} if self._value else {}
            if self._value_format:
                kwargs["value_format"] = self._value_format
            kwargs.setdefault("initial_focus", True)
            entry = DateEntry(master=frame, label=None, show_message=False, **kwargs)
        elif self._datatype in (int, float):
            # NumericEntry for numeric input with validation
            kwargs = {"value": self._value if self._value else 0}
            if self._minvalue is not None:
                kwargs["minvalue"] = self._minvalue
            if self._maxvalue is not None:
                kwargs["maxvalue"] = self._maxvalue
            if self._value_format:
                kwargs["value_format"] = self._value_format
            if self._increment is not None:
                kwargs["increment"] = self._increment
            kwargs.setdefault("initial_focus", True)
            entry = NumericEntry(master=frame, label=None, show_message=False, **kwargs)
        else:
            # TextEntry for string input
            kwargs = {"value": str(self._value) if self._value else ""}
            if self._value_format:
                kwargs["value_format"] = self._value_format
            kwargs.setdefault("initial_focus", True)
            entry = TextEntry(master=frame, label=None, show_message=False, **kwargs)

        entry.pack(pady=(0, 5), fill=X)
        entry.bind("<Return>", self._on_submit)
        entry.bind("<KP_Enter>", self._on_submit)

        # Focus the entry field
        def _focus():
            if hasattr(entry, 'entry_widget'):
                entry.entry_widget.focus_set()
            else:
                entry.focus_set()

        _focus()
        # Ensure focus after dialog buttons set their own focus
        entry.after_idle(_focus)

        frame.pack(fill=X, expand=True)
        self._entry_widget = entry

    def _on_submit(self, *_: Any) -> None:
        """Handle submit (Enter key or button click)."""
        if not self._entry_widget:
            return

        # Get value from widget - Field widgets use .value, Entry/Combobox use .get()
        if hasattr(self._entry_widget, 'value'):
            # Field widgets (TextEntry, NumericEntry, DateEntry)
            result = self._entry_widget.value
            # Field widgets handle their own validation, so we can use the value directly
            if result is not None:
                self._dialog.result = result
                if self._dialog.toplevel:
                    self._dialog.toplevel.destroy()
        else:
            # Regular Entry/Combobox - use old validation logic
            result = self._entry_widget.get()
            if self._validate(result):
                self._dialog.result = self._datatype(result) if self._datatype != str else result
                if self._dialog.toplevel:
                    self._dialog.toplevel.destroy()

    def _on_filter_list(self, event: tkinter.Event) -> None:
        """Filter combobox items based on user input."""
        value = event.widget.get().lower()
        if not value:
            event.widget["values"] = self._items
        else:
            data = [k for k in self._items if value in k.lower()]
            event.widget["values"] = data

    def _validate(self, result: str) -> bool:
        """Validate the input data."""
        # No validation for string data types unless there's a list of items
        if self._datatype not in [float, int, complex] and (self._items is None or len(self._items) == 0):
            return True

        # Convert result to appropriate data type
        try:
            converted_result = self._datatype(result)
        except ValueError:
            msg = MessageCatalog.translate("Should be of data type")
            MessageBox.ok(
                message=f"{msg} `{self._datatype}`",
                title=MessageCatalog.translate("Invalid data type"),
                master=self._dialog.toplevel,
            )
            return False

        # Check max value range
        if self._maxvalue is not None and converted_result > self._maxvalue:
            msg = MessageCatalog.translate("Number cannot be greater than")
            MessageBox.ok(
                message=f"{msg} {self._maxvalue}",
                title=MessageCatalog.translate("Out of range"),
                master=self._dialog.toplevel,
            )
            return False

        # Check min value range
        if self._minvalue is not None and converted_result < self._minvalue:
            msg = MessageCatalog.translate("Number cannot be less than")
            MessageBox.ok(
                message=f"{msg} {self._minvalue}",
                title=MessageCatalog.translate("Out of range"),
                master=self._dialog.toplevel,
            )
            return False

        # Check if item is in list
        if self._items is not None and len(self._items) > 0 and result not in self._items:
            msg = MessageCatalog.translate("Select an item from the list")
            MessageBox.ok(
                message=msg,
                title=MessageCatalog.translate("Out of range"),
                master=self._dialog.toplevel,
            )
            return False

        return True

    def show(self, position: Optional[tuple[int, int]] = None) -> None:
        """Show the dialog.

        Args:
            position: x and y coordinates to position the dialog. If None, centers on parent.
        """
        self._dialog.show(position=position, modal=True)
        target = self._dialog.toplevel or self._master
        if target:
            payload = {"result": self._dialog.result, "confirmed": self._dialog.result is not None}
            try:
                target.event_generate("<<DialogResult>>", data=payload)
            except Exception:
                try:
                    target.event_generate("<<DialogResult>>")
                except Exception:
                    pass

    @property
    def result(self) -> Any:
        """The dialog result value."""
        return self._dialog.result

    def on_dialog_result(self, callback: Callable[[Any], None]) -> Optional[str]:
        """Bind a callback fired when the dialog produces a result.

        The callback receives ``event.data["result"]`` when available.

        Args:
            callback: Callable that receives the result payload.

        Returns:
            Binding identifier for use with ``off_dialog_result``.
        """
        target = self._dialog.toplevel or self._master
        if target is None:
            return None

        def handler(event):
            callback(getattr(event, "data", None))

        return target.bind("<<DialogResult>>", handler, add="+")

    def off_dialog_result(self, funcid: str) -> None:
        """Unbind a previously bound dialog result callback."""
        target = self._dialog.toplevel or self._master
        if target is None:
            return
        target.unbind("<<DialogResult>>", funcid)


class QueryBox:
    """Static methods for displaying query dialogs."""

    @staticmethod
    def get_color(
            master: Optional[tkinter.Misc] = None,
            title: str = "Color Chooser",
            value: Optional[str] = None,
            **kwargs: Any,
    ) -> Any:
        """Show a color picker dialog.

        Args:
            master: Parent widget for the dialog.
            title: The dialog window title.
            value: Initial color to display.
            **kwargs: Additional arguments including 'position'.

        Returns:
            Selected color or None if cancelled.
        """
        from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog

        position = kwargs.pop("position", None)
        dialog = ColorChooserDialog(master, title, value)
        dialog.show(position)
        return dialog.result

    @staticmethod
    def get_date(
            master: Optional[tkinter.Misc] = None,
            title: str = " ",
            first_weekday: int = 6,
            value: Optional[date] = None,
            bootstyle: str = "primary",
            on_result: Optional[Callable[[Any], None]] = None,
            **kwargs: Any,
    ) -> Optional[date]:
        """Show a date picker dialog.

        Args:
            master: Parent widget for the dialog.
            title: The dialog window title.
            first_weekday: First day of the week (0=Monday, 6=Sunday).
            value: Initial date to display.
            bootstyle: Style for the calendar.
            on_result: Optional callback receiving the dialog result payload.
            **kwargs: Additional arguments including 'position'.

        Returns:
            Selected date or None if cancelled.
        """
        position = kwargs.pop("position", None)
        dialog = DateDialog(
            master=master,
            title=title,
            first_weekday=first_weekday,
            initial_date=value,
            bootstyle=bootstyle,
        )
        if on_result:
            dialog.on_result(on_result)
        dialog.show(position)
        return dialog.result

    @staticmethod
    def get_string(
            prompt: str = "",
            title: str = " ",
            value: Optional[str] = None,
            master: Optional[tkinter.Misc] = None,
            value_format: Optional[str] = None,
            on_result: Optional[Callable[[Any], None]] = None,
            **kwargs: Any,
    ) -> Optional[str]:
        """Show a string input dialog.

        Args:
            prompt: The prompt text to display.
            title: The dialog window title.
            value: Initial value for the input field.
            master: Parent widget for the dialog.
            value_format: Optional ICU format pattern for parsing/formatting.
            on_result: Optional callback receiving the dialog result payload.
            **kwargs: Additional arguments including 'position'.

        Returns:
            Input string or None if cancelled.
        """
        value = value or ""
        position = kwargs.pop("position", None)
        dialog = QueryDialog(
            prompt,
            title,
            value,
            master=master,
            value_format=value_format,
            **kwargs,
        )
        if on_result:
            dialog.on_dialog_result(on_result)
        dialog.show(position)
        return dialog.result

    @staticmethod
    def get_item(
            prompt: str = "",
            title: str = " ",
            value: Optional[str] = None,
            items: Optional[List[str]] = None,
            master: Optional[tkinter.Misc] = None,
            on_result: Optional[Callable[[Any], None]] = None,
            **kwargs: Any,
    ) -> Optional[str]:
        """Show a dropdown selection dialog.

        Args:
            prompt: The prompt text to display.
            title: The dialog window title.
            value: Initial value for the input field.
            items: List of items to choose from.
            master: Parent widget for the dialog.
            on_result: Optional callback receiving the dialog result payload.
            **kwargs: Additional arguments including 'position'.

        Returns:
            Selected item or None if cancelled.
        """
        value = value or ""
        position = kwargs.pop("position", None)
        dialog = QueryDialog(
            prompt,
            title,
            value,
            items=items,
            master=master,
            **kwargs,
        )
        if on_result:
            dialog.on_dialog_result(on_result)
        dialog.show(position)
        return dialog.result

    @staticmethod
    def get_integer(
            prompt: str = "",
            title: str = " ",
            value: Optional[int] = None,
            minvalue: Optional[int] = None,
            maxvalue: Optional[int] = None,
            master: Optional[tkinter.Misc] = None,
            value_format: Optional[str] = None,
            increment: Optional[int] = None,
            on_result: Optional[Callable[[Any], None]] = None,
            **kwargs: Any,
    ) -> Optional[int]:
        """Show an integer input dialog with validation.

        Args:
            prompt: The prompt text to display.
            title: The dialog window title.
            value: Initial value for the input field.
            minvalue: Minimum allowed value.
            maxvalue: Maximum allowed value.
            increment: Step size for increment/decrement buttons.
            value_format: Optional ICU format pattern for parsing/formatting.
            master: Parent widget for the dialog.
            on_result: Optional callback receiving the dialog result payload.
            **kwargs: Additional arguments including 'position'.

        Returns:
            Integer value or None if cancelled.
        """
        value = value or ""
        position = kwargs.pop("position", None)
        dialog = QueryDialog(
            prompt,
            title,
            value,
            minvalue,
            maxvalue,
            datatype=int,
            master=master,
            value_format=value_format,
            increment=increment,
            **kwargs,
        )
        if on_result:
            dialog.on_dialog_result(on_result)
        dialog.show(position)
        return dialog.result

    @staticmethod
    def get_float(
            prompt: str = "",
            title: str = " ",
            value: Optional[float] = None,
            minvalue: Optional[float] = None,
            maxvalue: Optional[float] = None,
            master: Optional[tkinter.Misc] = None,
            value_format: Optional[str] = None,
            increment: Optional[float] = None,
            on_result: Optional[Callable[[Any], None]] = None,
            **kwargs: Any,
    ) -> Optional[float]:
        """Show a float input dialog with validation.

        Args:
            prompt: The prompt text to display.
            title: The dialog window title.
            value: Initial value for the input field.
            minvalue: Minimum allowed value.
            maxvalue: Maximum allowed value.
            master: Parent widget for the dialog.
            value_format: Optional ICU format pattern for parsing/formatting.
            increment: Step size for increment/decrement buttons.
            on_result: Optional callback receiving the dialog result payload.
            **kwargs: Additional arguments including 'position'.

        Returns:
            Float value or None if cancelled.
        """
        value = value or ""
        position = kwargs.pop("position", None)
        dialog = QueryDialog(
            prompt,
            title,
            value,
            minvalue,
            maxvalue,
            datatype=float,
            master=master,
            value_format=value_format,
            increment=increment,
            **kwargs,
        )
        if on_result:
            dialog.on_dialog_result(on_result)
        dialog.show(position)
        return dialog.result

    @staticmethod
    def get_font(master: Optional[tkinter.Misc] = None, **kwargs: Any) -> Any:
        """Show a font selection dialog.

        Args:
            master: Parent widget for the dialog.
            **kwargs: Additional arguments including 'position'.

        Returns:
            Selected font or None if cancelled.
        """
        position = kwargs.pop("position", None)
        dialog = FontDialog(master=master, **kwargs)
        dialog.show(position)
        return dialog.result
