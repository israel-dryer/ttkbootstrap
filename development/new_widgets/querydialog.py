import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Dialog
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import textwrap


class QueryDialog(Dialog):
    """A modal dialog class for requesting user input.

    A simple modal dialog class that can be used to build simple
    message dialogs.

    Displays a prompt, an entry widget, and a set of Submit and
    Cancel buttons. When the user clicks submit or presses <Return>,
    the entry value is stored in the `result` property.

    Use a `Toplevel` widget for more advanced modal dialog designs.    
    """

    def __init__(
        self,
        prompt,
        title=None,
        initialvalue='',
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

            initial_value (Any):
                The initial value in the entry widget.

            min_value (Any):
                The minimum allowed value. Only valid for int and float
                data types.

            max_value (Any):
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

            data_type (Union[int, str, float]):
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
        """Create the toplevel message body"""
        frame = ttk.Frame(master, padding=self._padding)
        if self._prompt:
            for p in self._prompt.split('\n'):
                prompt = '\n'.join(textwrap.wrap(p, width=self._width))
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
        """Create the toplevel button box"""
        frame = ttk.Frame(master, padding=(5, 10))

        submit = ttk.Button(
            master=frame,
            bootstyle='primary',
            text='Submit',
            command=self.on_submit
        )
        submit.pack(padx=5, side=RIGHT)
        submit.lower()  # set focus traversal left-to-right

        cancel = ttk.Button(
            master=frame,
            bootstyle='secondary',
            text='Cancel',
            command=self.on_cancel
        )
        cancel.pack(padx=5, side=RIGHT)
        cancel.lower()  # set focus traversal left-to-right

        ttk.Separator(self._toplevel).pack(fill=X)
        frame.pack(side=BOTTOM, fill=X, anchor=S)

    def on_submit(self, *_):
        """Submit callback"""
        self._result = self._initial_focus.get()
        valid_result = self.validate()
        if not valid_result:
            return  # keep toplevel open for valid response
        self._toplevel.destroy()
        self.apply()

    def on_cancel(self, *_):
        """Cancel callback"""
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
            Messagebox.ok(
                message=f"Should be of data type `{self._datatype}`",
                title="Invalid data type"
            )
            return False

        # max value range
        if self._maxvalue is not None:
            if self._result > self._maxvalue:
                Messagebox.ok(
                    message=f"Number cannot be greater than {self._maxvalue}",
                    title="Out of Range"
                )
                return False

        # min value range
        if self._minvalue is not None:
            if self._result < self._minvalue:
                Messagebox.ok(
                    message=f"Number cannot be less than {self._minvalue}",
                    title="Out of Range"
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


if __name__ == '__main__':

    import tkinter as tk
    from ttkbootstrap import utility
    import ttkbootstrap as ttk
    utility.enable_high_dpi_awareness()

    root = tk.Tk()
    style = ttk.Style('darkly')
    dialog = QueryDialog(
        prompt="Enter the appropriate number",
        datatype=int,
        minvalue=10,
        maxvalue=100
    )
    dialog.show()
