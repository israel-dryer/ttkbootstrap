import textwrap
from tkinter import X, N, END, RIGHT, BOTTOM, S

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Dialog
from ttkbootstrap.dialogs.message import Messagebox
from ttkbootstrap.dialogs.datepicker import DatePickerDialog
from ttkbootstrap.dialogs.fontpicker import FontPickerDialog
from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.ttk_types import StyleColor


class QueryDialog(Dialog):
    """A simple modal dialog class that can be used to build simple
    data input dialogs. Displays a prompt, and input box, and a set of
    buttons. Additional data manipulation can be performed on the
    user input post-hoc by overriding the `apply` method.

    Use a `Toplevel` widget for more advanced modal dialog designs.
    """

    def __init__(
        self,
        prompt,
        title=" ",
        initialvalue="",
        minvalue=None,
        maxvalue=None,
        width=65,
        datatype=str,
        padding=(20, 20),
        parent=None,
    ):
        """
        Parameters:

            prompt (str):
                A message to display in the message box above the entry
                widget.

            title (str):
                The string displayed as the title of the message box.
                This option is ignored on Mac OS X, where platform
                guidelines forbid the use of a title on this kind of
                dialog.

            initialvalue (Any):
                The initial value in the entry widget.

            minvalue (Any):
                The minimum allowed value. Only valid for int and float
                data types.

            maxvalue (Any):
                The maximum allowed value. Only valid for int and float
                data types.

            width (int):
                The maximum number of characters per line in the
                message. If the text stretches beyond the limit, the
                line will break at the word.

            parent (Widget):
                Makes the window the logical parent of the message box.
                The messagebox is displayed on top of its parent
                window.

            padding (Union[int, Tuple[int]]):
                The amount of space between the border and the widget
                contents.

            datatype (Union[int, str, float]):
                The data type used to validate the entry value.
        """
        super().__init__(parent, title)
        self._prompt = prompt
        self._initialvalue = initialvalue
        self._minvalue = minvalue
        self._maxvalue = maxvalue
        self._width = width
        self._datatype = datatype
        self._padding = padding
        self._result = None

    def create_body(self, master):
        """Overrides the parent method; adds the message and input
        section."""
        frame = ttk.Frame(master, padding=self._padding)
        if self._prompt:
            for p in self._prompt.split("\n"):
                prompt = "\n".join(textwrap.wrap(p, width=self._width))
                prompt_label = ttk.Label(frame, text=prompt)
                prompt_label.pack(pady=(0, 5), fill=X, anchor=N)

        entry = ttk.Entry(master=frame)
        entry.insert(END, self._initialvalue)
        entry.pack(pady=(0, 5), fill=X)
        entry.bind("<Return>", self.on_submit)
        entry.bind("<KP_Enter>", self.on_submit)
        entry.bind("<Escape>", self.on_cancel)
        frame.pack(fill=X, expand=True)
        self._initial_focus = entry

    def create_buttonbox(self, master):
        """Overrides the parent method; adds the message buttonbox"""
        frame = ttk.Frame(master, padding=(5, 10))

        submit = ttk.Button(
            master=frame,
            bootstyle="primary",
            text=MessageCatalog.translate("Submit"),
            command=self.on_submit,
        )
        submit.pack(padx=5, side=RIGHT)
        submit.lower()  # set focus traversal left-to-right

        cancel = ttk.Button(
            master=frame,
            bootstyle="secondary",
            text=MessageCatalog.translate("Cancel"),
            command=self.on_cancel,
        )
        cancel.pack(padx=5, side=RIGHT)
        cancel.lower()  # set focus traversal left-to-right

        ttk.Separator(self._toplevel).pack(fill=X)
        frame.pack(side=BOTTOM, fill=X, anchor=S)

    def on_submit(self, *_):
        """Save result, destroy the toplevel, and apply any post-hoc
        data manipulations."""
        self._result = self._initial_focus.get()
        valid_result = self.validate()
        if not valid_result:
            return  # keep toplevel open for valid response
        self._toplevel.destroy()
        self.apply()

    def on_cancel(self, *_):
        """Close the toplevel and return empty."""
        self._toplevel.destroy()
        return

    def validate(self):
        """Validate the data

        This method is called automatically to validate the data before
        the dialog is destroyed. Can be subclassed and overridden.
        """
        # no default checks required for string data types
        if self._datatype not in [float, int, complex]:
            return True

        # convert result to appropriate data type
        try:
            self._result = self._datatype(self._result)
        except ValueError:
            msg = MessageCatalog.translate("Should be of data type")
            Messagebox.ok(
                message=f"{msg} `{self._datatype}`",
                title=MessageCatalog.translate("Invalid data type"),
                parent=self._toplevel
            )
            return False

        # max value range
        if self._maxvalue is not None:
            if self._result > self._maxvalue:
                msg = MessageCatalog.translate("Number cannot be greater than")
                Messagebox.ok(
                    message=f"{msg} {self._maxvalue}",
                    title=MessageCatalog.translate("Out of range"),
                    parent=self._toplevel
                )
                return False

        # min value range
        if self._minvalue is not None:
            if self._result < self._minvalue:
                msg = MessageCatalog.translate("Number cannot be less than")
                Messagebox.ok(
                    message=f"{msg} {self._minvalue}",
                    title=MessageCatalog.translate("Out of range"),
                    parent=self._toplevel
                )
                return False

        # valid result
        return True

    def apply(self):
        """Process the data.

        This method is called automatically to process the data after
        the dialog is destroyed. By default, it does nothing.
        """
        pass  # override


class Querybox:
    """This class contains various static methods that request data
    from the end user."""

    @staticmethod
    def get_color(
        parent=None, title="Color Chooser", initialcolor=None, **kwargs
    ):
        """Show a color picker and return the select color when the
        user pressed OK.

        ![](../../assets/dialogs/querybox-get-color.png)

        Parameters:

            parent (Widget):
                The parent widget.

            title (str):
                Optional text that appears on the titlebar.

            initialcolor (str):
                The initial color to display in the 'Current' color
                frame.

        Returns:

            Tuple[rgb, hsl, hex]:
                The selected color in various colors models.
        """
        from ttkbootstrap.dialogs import ColorChooserDialog

        dialog = ColorChooserDialog(parent, title, initialcolor)
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog.show(position)
        return dialog.result

    @staticmethod
    def get_date(
        parent=None,
        title=" ",
        firstweekday=6,
        startdate: 'datetime' = None,
        color: StyleColor = "primary",
    ):
        """Shows a calendar popup and returns the selection.

        ![](../../assets/dialogs/querybox-get-date.png)

        Parameters:

            parent (Widget):
                The parent widget; the popup will appear to the
                bottom-right of the parent widget. If no parent is
                provided, the widget is centered on the screen.

            title (str):
                The text that appears on the popup titlebar.

            firstweekday (int):
                Specifies the first day of the week. `0` is Monday, `6` is
                Sunday (the default).

            startdate (datetime):
                The date to be in focus when the widget is displayed;

            color (str):
                The color of the titlebar and and hover / pressed color

        Returns:

            datetime:
                The date selected; the current date if no date is selected.
        """
        chooser = DatePickerDialog(
            parent=parent,
            title=title,
            firstweekday=firstweekday,
            startdate=startdate,
            color=color,
        )
        return chooser.date_selected

    @staticmethod
    def get_string(
        prompt="", title=" ", initialvalue=None, parent=None, **kwargs
    ):
        """Request a string type input from the user.

        ![](../../assets/dialogs/querybox-get-string.png)

        Parameters:

            prompt (str):
                A message to display in the message box above the entry
                widget.

            title (str):
                The string displayed as the title of the message box. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            initialvalue (Any):
                The initial value in the entry widget.

            parent (Widget):
                Makes the window the logical parent of the message box. The
                messagebox is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            str:
                The string value of the entry widget.
        """
        initialvalue = initialvalue or ""
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog = QueryDialog(
            prompt, title, initialvalue, parent=parent, **kwargs
        )
        dialog.show(position)
        return dialog._result

    @staticmethod
    def get_integer(
        prompt="",
        title=" ",
        initialvalue=None,
        minvalue=None,
        maxvalue=None,
        parent=None,
        **kwargs,
    ):
        """Request an integer type input from the user.

        ![](../../assets/dialogs/querybox-get-integer.png)

        Parameters:

            prompt (str):
                A message to display in the message box above the entry
                widget.

            title (str):
                The string displayed as the title of the message box. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            initialvalue (int):
                The initial value in the entry widget.

            minvalue (int):
                The minimum allowed value.

            maxvalue (int):
                The maximum allowed value.

            parent (Widget):
                Makes the window the logical parent of the message box. The
                messagebox is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            int:
                The integer value of the entry widget.
        """
        initialvalue = initialvalue or ""
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog = QueryDialog(
            prompt,
            title,
            initialvalue,
            minvalue,
            maxvalue,
            datatype=int,
            parent=parent,
            **kwargs,
        )
        dialog.show(position)
        return dialog._result

    @staticmethod
    def get_float(
        prompt="",
        title=" ",
        initialvalue=None,
        minvalue=None,
        maxvalue=None,
        parent=None,
        **kwargs,
    ):
        """Request a float type input from the user.

        ![](../../assets/dialogs/querybox-get-float.png)

        Parameters:

            prompt (str):
                A message to display in the message box above the entry
                widget.

            title (str):
                The string displayed as the title of the message box. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            initialvalue (float):
                The initial value in the entry widget.

            minvalue (float):
                The minimum allowed value.

            maxvalue (float):
                The maximum allowed value.

            parent (Widget):
                Makes the window the logical parent of the message box. The
                messagebox is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            float:
                The float value of the entry widget.
        """
        initialvalue = initialvalue or ""
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog = QueryDialog(
            prompt,
            title,
            initialvalue,
            minvalue,
            maxvalue,
            datatype=float,
            parent=parent,
            **kwargs,
        )
        dialog.show(position)
        return dialog._result

    @staticmethod
    def get_font(parent=None, **kwargs):
        """Request a customized font

        ![](../../assets/dialogs/querybox-get-font.png)

        Parameters:

            parent (Widget):
                Makes the window the logical parent of the dialog box. The
                dialog is displayed on top of its parent window.

            **kwargs (Dict):
                Other keyword arguments.

        Returns:

            Font:
                A font object.
        """
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog = FontPickerDialog(parent=parent, **kwargs)
        dialog.show(position)
        return dialog.result
