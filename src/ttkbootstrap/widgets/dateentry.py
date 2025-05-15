import tkinter as tk
from datetime import datetime
from tkinter import ttk

from ttkbootstrap.dialogs import Querybox


class DateEntry(ttk.Frame):
    """A date entry widget combines the `Combobox` and a `Button`
    with a callback attached to the `get_date` function.

    When pressed, a date chooser popup is displayed. The returned
    value is inserted into the combobox.

    The <<DateEntrySelected>> event is generated when a date is
    selected.

    The date chooser popup will use the date in the combobox as the
    date of focus if it is in the format specified by the
    `dateformat` parameter. By default, this format is "%Y-%m-%d".

    The bootstyle api may be used to change the style of the widget.
    The available colors include -> primary, secondary, success,
    info, warning, danger, light, dark.

    The starting weekday on the date chooser popup can be changed
    with the `firstweekday` parameter. By default this value is
    `6`, which represents "Sunday".

    The `Entry` and `Button` widgets are accessible from the
    `DateEntry.Entry` and `DateEntry.Button` properties.

    ![](../../assets/widgets/date-entry.png)
    """

    def __init__(
            self,
            master=None,
            dateformat=r"%x",
            firstweekday=6,
            startdate=None,
            bootstyle="",
            **kwargs,
    ):
        """
        Parameters:

            master (Widget, optional):
                The parent widget.

            dateformat (str, optional):
                The format string used to render the text in the entry
                widget. For more information on acceptable formats, see https://strftime.org/

            firstweekday (int, optional):
                Specifies the first day of the week. 0=Monday, 1=Tuesday,
                etc...

            startdate (datetime, optional):
                The date that is in focus when the widget is displayed. Default is
                current date.

            bootstyle (str, optional):
                A style keyword used to set the focus color of the entry
                and the background color of the date button. Available
                options include -> primary, secondary, success, info,
                warning, danger, dark, light.

            **kwargs (Dict[str, Any], optional):
                Other keyword arguments passed to the frame containing the
                entry and date button.
        """
        self._dateformat = dateformat
        self._firstweekday = firstweekday

        self._startdate = startdate or datetime.today()
        self._bootstyle = bootstyle
        super().__init__(master, **kwargs)

        # add visual components
        entry_kwargs = {"bootstyle": self._bootstyle}
        if "width" in kwargs:
            entry_kwargs["width"] = kwargs.pop("width")

        self.entry = ttk.Entry(self, **entry_kwargs)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        self.button = ttk.Button(
            master=self,
            command=self._on_date_ask,
            bootstyle=f"{self._bootstyle}-date",
        )
        self.button.pack(side=tk.LEFT)

        # starting value
        self.entry.insert(tk.END, self._startdate.strftime(self._dateformat))

    def __getitem__(self, key: str):
        return self.configure(cnf=key)

    def __setitem__(self, key: str, value):
        self.configure(cnf=None, **{key: value})

    def _configure_set(self, **kwargs):
        """Override configure method to allow for setting custom
        DateEntry parameters"""

        if "state" in kwargs:
            state = kwargs.pop("state")
            if state in ["readonly", "invalid"]:
                self.entry.configure(state=state)
            elif state in ("disabled", "normal"):
                self.entry.configure(state=state)
                self.button.configure(state=state)
            else:
                kwargs[state] = state
        if "dateformat" in kwargs:
            self._dateformat = kwargs.pop("dateformat")
        if "firstweekday" in kwargs:
            self._firstweekday = kwargs.pop("firstweekday")
        if "startdate" in kwargs:
            self._startdate = kwargs.pop("startdate")
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.pop("bootstyle")
            self.entry.configure(bootstyle=self._bootstyle)
            self.button.configure(bootstyle=[self._bootstyle, "date"])
        if "width" in kwargs:
            width = kwargs.pop("width")
            self.entry.configure(width=width)

        super(ttk.Frame, self).configure(**kwargs)

    def _configure_get(self, cnf):
        """Override the configure get method"""
        if cnf == "state":
            entrystate = self.entry.cget("state")
            buttonstate = self.button.cget("state")
            return {"Entry": entrystate, "Button": buttonstate}
        if cnf == "dateformat":
            return self._dateformat
        if cnf == "firstweekday":
            return self._firstweekday
        if cnf == "startdate":
            return self._startdate
        if cnf == "bootstyle":
            return self._bootstyle
        else:
            return super(ttk.Frame, self).configure(cnf=cnf)

    def configure(self, cnf=None, **kwargs):
        """Configure the options for this widget.

        Parameters:

            cnf (Dict[str, Any], optional):
                A dictionary of configuration options.

            **kwargs:
                Optional keyword arguments.
        """
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            return self._configure_set(**kwargs)

    def _on_date_ask(self):
        """Callback for pushing the date button"""
        _val = self.entry.get() or datetime.today().strftime(self._dateformat)
        try:
            self._startdate = datetime.strptime(_val, self._dateformat)
        except Exception as e:
            print("Date entry text does not match", self._dateformat)
            self._startdate = datetime.today()
            self.entry.delete(first=0, last=tk.END)
            self.entry.insert(
                tk.END, self._startdate.strftime(self._dateformat)
            )

        old_date = datetime.strptime(_val, self._dateformat)

        # get the new date and insert into the entry
        new_date = Querybox.get_date(
            parent=self.entry,
            startdate=old_date,
            firstweekday=self._firstweekday,
            bootstyle=self._bootstyle,
        )
        self.entry.delete(first=0, last=tk.END)
        self.entry.insert(tk.END, new_date.strftime(self._dateformat))
        self.entry.focus_force()
        self.event_generate("<<DateEntrySelected>>")
