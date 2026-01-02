"""Query dialogs and querybox facade for data input."""

import textwrap
import tkinter
from datetime import date
from typing import Any, List, Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.localization import MessageCatalog
from .base import Dialog
from .datepicker import DatePickerDialog
from .fontdialog import FontDialog
from .message import Messagebox


class QueryDialog(Dialog):
    """A simple modal dialog class for collecting user input."""

    def __init__(
            self,
            prompt: str,
            title: str = " ",
            initialvalue: Any = "",
            minvalue: Optional[Any] = None,
            maxvalue: Optional[Any] = None,
            width: int = 65,
            datatype: Any = str,
            padding: "tuple[int, int] | int" = (20, 20),
            parent: Optional[tkinter.Misc] = None,
            items: Optional[List[str]] = None,
    ) -> None:
        """Create a query dialog for collecting user input.

        Parameters:

            prompt (str):
                The prompt text to display above the input field. Supports
                multiline strings (separated by \\n).

            title (str):
                The dialog window title (default=' ').

            initialvalue (Any):
                The initial value to populate in the input field (default='').

            minvalue (Any):
                Minimum allowed value for numeric data types (int, float, complex).
                Ignored for strings.

            maxvalue (Any):
                Maximum allowed value for numeric data types (int, float, complex).
                Ignored for strings.

            width (int):
                Maximum width in characters for text wrapping of the prompt
                (default=65).

            datatype (type):
                Expected data type for validation (str, int, float, complex).
                When set to int, float, or complex, the input will be validated
                and converted (default=str).

            padding (int | tuple):
                Padding around the dialog content. Can be a single int or
                tuple (horizontal, vertical) (default=(20, 20)).

            parent (Widget):
                Parent widget. The dialog will be centered on this widget.

            items (List[str]):
                Optional list of items for dropdown selection. If provided,
                shows a Combobox instead of Entry. The Combobox supports
                filtering by typing. If items are provided, the input must
                match one from the list.
        """
        super().__init__(parent, title)
        self._prompt = prompt
        self._initialvalue = initialvalue
        self._items = items
        self._minvalue = minvalue
        self._maxvalue = maxvalue
        self._width = width
        self._datatype = datatype
        self._padding = padding
        self._result = None

    def create_body(self, master: tkinter.Misc) -> None:
        frame = ttk.Frame(master, padding=self._padding)
        if self._prompt:
            for p in self._prompt.split("\n"):
                prompt = "\n".join(textwrap.wrap(p, width=self._width))
                prompt_label = ttk.Label(frame, text=prompt)
                prompt_label.pack(pady=(0, 5), fill=X, anchor=N)
        if self._items is None or len(self._items) == 0:
            entry = ttk.Entry(master=frame)
        else:
            entry = ttk.Combobox(master=frame, values=self._items)
            entry.bind("<KeyRelease>", self.on_filter_list)
        entry.insert(END, self._initialvalue)
        entry.pack(pady=(0, 5), fill=X)
        entry.bind("<Return>", self.on_submit)
        entry.bind("<KP_Enter>", self.on_submit)
        entry.bind("<Escape>", self.on_cancel)
        frame.pack(fill=X, expand=True)
        self._initial_focus = entry

    def create_buttonbox(self, master: tkinter.Misc) -> None:
        frame = ttk.Frame(master, padding=(5, 10))

        submit = ttk.Button(
            master=frame,
            bootstyle="primary",
            text=MessageCatalog.translate("Submit"),
            command=self.on_submit,
        )
        submit.pack(padx=5, side=RIGHT)
        submit.lower()

        cancel = ttk.Button(
            master=frame,
            bootstyle="secondary",
            text=MessageCatalog.translate("Cancel"),
            command=self.on_cancel,
        )
        cancel.pack(padx=5, side=RIGHT)
        cancel.lower()

        ttk.Separator(self._toplevel).pack(fill=X)
        frame.pack(side=BOTTOM, fill=X, anchor=S)

    def on_submit(self, *_: Any) -> None:
        self._result = self._initial_focus.get()
        valid_result = self.validate()
        if not valid_result:
            return  # keep toplevel open for valid response
        self._toplevel.destroy()
        self.apply()

    def on_cancel(self, *_: Any) -> None:
        self._toplevel.destroy()
        return

    def on_filter_list(self, event: tkinter.Event) -> None:
        value = event.widget.get().lower()
        if not value:
            event.widget["values"] = self._items
        else:
            data = [k for k in self._items if value in k.lower()]
            event.widget["values"] = data

    def validate(self) -> bool:
        """Validate the data before closing."""
        # no default checks required for string data types,
        # unless there is a list of items to pick from
        if self._datatype not in [float, int, complex] and (self._items is None or len(self._items) == 0):
            return True

        # convert result to appropriate data type
        try:
            self._result = self._datatype(self._result)
        except ValueError:
            msg = MessageCatalog.translate("Should be of data type")
            Messagebox.ok(
                message=f"{msg} `{self._datatype}`",
                title=MessageCatalog.translate("Invalid data type"),
                parent=self._toplevel,
            )
            return False

        # max value range
        if self._maxvalue is not None and self._result > self._maxvalue:
            msg = MessageCatalog.translate("Number cannot be greater than")
            Messagebox.ok(
                message=f"{msg} {self._maxvalue}",
                title=MessageCatalog.translate("Out of range"),
                parent=self._toplevel,
            )
            return False

        # min value range
        if self._minvalue is not None and self._result < self._minvalue:
            msg = MessageCatalog.translate("Number cannot be less than")
            Messagebox.ok(
                message=f"{msg} {self._minvalue}",
                title=MessageCatalog.translate("Out of range"),
                parent=self._toplevel,
            )
            return False

        # item in list
        if self._items is not None and len(self._items) > 0 and self._result not in self._items:
            msg = MessageCatalog.translate("Select an item from the list")
            Messagebox.ok(
                message=msg,
                title=MessageCatalog.translate("Out of range"),
                parent=self._toplevel,
            )
            return False

        return True

    def apply(self) -> None:
        """Process the data after closing (no-op by default)."""
        pass


class Querybox:
    """Static methods that request data from the end user."""

    @staticmethod
    def get_color(
            parent: Optional[tkinter.Misc] = None,
            title: str = "Color Chooser",
            initialcolor: Optional[str] = None,
            **kwargs: Any,
    ) -> Any:
        """Show a color picker and return the selected color when OK is pressed."""
        from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog

        dialog = ColorChooserDialog(parent, title, initialcolor)
        position = kwargs.pop("position", None)
        dialog.show(position)
        return dialog.result

    @staticmethod
    def get_date(
            parent: Optional[tkinter.Misc] = None,
            title: str = " ",
            firstweekday: int = 6,
            startdate: Optional[date] = None,
            bootstyle: str = "primary",
    ) -> date:
        chooser = DatePickerDialog(
            parent=parent,
            title=title,
            firstweekday=firstweekday,
            startdate=startdate,
            bootstyle=bootstyle,
        )
        return chooser.date_selected

    @staticmethod
    def get_string(
            prompt: str = "",
            title: str = " ",
            initialvalue: Optional[str] = None,
            parent: Optional[tkinter.Misc] = None,
            **kwargs: Any,
    ) -> Optional[str]:
        initialvalue = initialvalue or ""
        position = kwargs.pop("position", None)
        dialog = QueryDialog(prompt, title, initialvalue, parent=parent, **kwargs)
        dialog.show(position)
        return dialog._result

    @staticmethod
    def get_item(
            prompt: str = "",
            title: str = " ",
            initialvalue: Optional[str] = None,
            items: Optional[List[str]] = None,
            parent: Optional[tkinter.Misc] = None,
            **kwargs: Any,
    ) -> Optional[str]:
        initialvalue = initialvalue or ""
        position = kwargs.pop("position", None)
        dialog = QueryDialog(prompt, title, initialvalue, items=items, parent=parent, **kwargs)
        dialog.show(position)
        return dialog._result

    @staticmethod
    def get_integer(
            prompt: str = "",
            title: str = " ",
            initialvalue: Optional[int] = None,
            minvalue: Optional[int] = None,
            maxvalue: Optional[int] = None,
            parent: Optional[tkinter.Misc] = None,
            **kwargs: Any,
    ) -> Optional[int]:
        initialvalue = initialvalue or ""
        position = kwargs.pop("position", None)
        datatype = kwargs.pop("datatype", int)
        dialog = QueryDialog(
            prompt,
            title,
            initialvalue,
            minvalue,
            maxvalue,
            datatype=datatype,
            parent=parent,
            **kwargs,
        )
        dialog.show(position)
        return dialog._result

    @staticmethod
    def get_float(
            prompt: str = "",
            title: str = " ",
            initialvalue: Optional[float] = None,
            minvalue: Optional[float] = None,
            maxvalue: Optional[float] = None,
            parent: Optional[tkinter.Misc] = None,
            **kwargs: Any,
    ) -> Optional[float]:
        initialvalue = initialvalue or ""
        position = kwargs.pop("position", None)
        datatype = kwargs.pop("datatype", float)
        dialog = QueryDialog(
            prompt,
            title,
            initialvalue,
            minvalue,
            maxvalue,
            datatype=datatype,
            parent=parent,
            **kwargs,
        )
        dialog.show(position)
        return dialog._result

    @staticmethod
    def get_font(parent: Optional[tkinter.Misc] = None, **kwargs: Any):
        position = kwargs.pop("position", None)
        dialog = FontDialog(parent=parent, **kwargs)
        dialog.show(position)
        return dialog.result
