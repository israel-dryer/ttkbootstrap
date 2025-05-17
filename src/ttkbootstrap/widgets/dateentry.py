from datetime import datetime
from ttkbootstrap.widgets import Frame, Entry, Button
from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.dialogs.query import Querybox


class DateEntry(Frame):
    """
    A themed entry widget with an attached calendar popup for date selection.

    Combines a `ttk.Entry` and a themed `Button` to create a date picker. Users
    can either type a date or select one from a popup calendar, with the date
    displayed in the desired format.

    Features:
        - Built-in calendar button to pick a date interactively
        - Supports custom date formats and starting weekday
        - Fires `<<DateEntrySelected>>` virtual event after selection
        - Fully themed appearance using `color`
        - Internal entry and button accessible via `.entry` and `.button`

    Example:
        >>> from ttkbootstrap.widgets import DateEntry
        >>> date_entry = DateEntry(
        ...     root,
        ...     color="primary",
        ...     dateformat="%Y-%m-%d",
        ...     popuptitle="Pick a Date"
        ... )
        >>> date_entry.pack()

    Args:
        master (Misc, optional):
            Parent widget for this composite component.

        dateformat (str, optional):
            Format string used for displaying the date. Defaults to "%x".

        firstweekday (int, optional):
            Starting day of the week for the popup (0=Monday, 6=Sunday). Default is 6.

        startdate (datetime, optional):
            Initial value shown in both the entry and the calendar popup.

        color (StyleColor, optional):
            Theme color used for both entry and calendar button styling.

        popuptitle (str, optional):
            Title displayed on the popup calendar window.

        **kwargs (dict):
            Additional options passed to the outer `Frame`. If `width` is supplied,
            it is forwarded to the inner entry widget.
    """

    def __init__(
        self,
        master=None,
        dateformat=r"%x",
        firstweekday=6,
        startdate=None,
        color: StyleColor = "primary",
        popuptitle: str = "Select a date",
        **kwargs,
    ):
        self._dateformat = dateformat
        self._firstweekday = firstweekday
        self._start_date = startdate or datetime.today()
        self._color = color
        self._popup_title = popuptitle

        super().__init__(master, color=color, **kwargs)

        entry_kwargs = {}
        if "width" in kwargs:
            entry_kwargs["width"] = kwargs.pop("width")

        self.entry = Entry(self, color=color, **entry_kwargs)
        self.entry.pack(side="left", fill="x", expand=1)
        self.button = DateButton(self, color=color, command=self._on_date_ask)
        self.button.pack(side="left")

        self.entry.insert("end", self._start_date.strftime(self._dateformat))

    def __getitem__(self, key: str):
        return self.configure(cnf=key)

    def __setitem__(self, key: str, value):
        self.configure(cnf=None, **{key: value})

    def _configure_set(self, **kwargs):
        """
        Set configuration values for DateEntry-specific and inherited options.

        Args:
            **kwargs: Configuration options.
        """
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
            self._start_date = kwargs.pop("startdate")
        if "color" in kwargs:
            self._color = kwargs.pop("color")
            self.entry.configure(color=self._color)
            self.button.configure(color=self._color, variant="date")
        if "width" in kwargs:
            width = kwargs.pop("width")
            self.entry.configure(width=width)

        super(Frame, self).configure(**kwargs)

    def _configure_get(self, cnf):
        """
        Retrieve a configuration value.

        Args:
            cnf (str): Name of the configuration option.

        Returns:
            Value of the configuration option.
        """
        if cnf == "state":
            entry_date = self.entry.cget("state")
            button_state = self.button.cget("state")
            return {"Entry": entry_date, "Button": button_state}
        if cnf == "dateformat":
            return self._dateformat
        if cnf == "firstweekday":
            return self._firstweekday
        if cnf == "startdate":
            return self._start_date
        if cnf == "color":
            return self._color
        else:
            return super(Frame, self).configure(cnf=cnf)

    def configure(self, cnf=None, **kwargs):
        """
        Unified configure interface for both getting and setting options.

        Args:
            cnf (str, optional): Name of the configuration option to retrieve.
            **kwargs: Options to configure.

        Returns:
            The requested configuration value if `cnf` is provided.
        """
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            return self._configure_set(**kwargs)

    def _on_date_ask(self):
        """
        Internal callback invoked when the calendar button is pressed.
        Shows the calendar dialog and updates the entry field.
        """
        _val = self.entry.get() or datetime.today().strftime(self._dateformat)

        try:
            old_date = datetime.strptime(_val, self._dateformat)
        except ValueError:
            print("[DateEntry] date entry text does not match", self._dateformat)
            old_date = datetime.today()
            self.entry.delete(0, "end")
            self.entry.insert("end", old_date.strftime(self._dateformat))

        self._start_date = old_date

        new_date = Querybox.get_date(
            parent=self.entry,
            title=self._popup_title,
            firstweekday=self._firstweekday,
            startdate=old_date,
            color=self._color,
        )
        self.entry.delete(0, "end")
        self.entry.insert("end", new_date.strftime(self._dateformat))
        self.entry.focus_force()
        self.event_generate("<<DateEntrySelected>>")


class DateButton(Button):
    """
    A themed calendar trigger button used in conjunction with `DateEntry`.

    This button is styled using the "date" variant and is designed to be placed
    next to an entry field to open a calendar popup.

    Args:
        master (Misc, optional):
            Parent widget for this button.

        color (StyleColor, optional):
            Theme color applied to the button (e.g., "primary", "info").

        **kwargs (dict):
            Additional keyword arguments passed to the underlying `ttk.Button`.
            The `variant` is automatically set to "date" for consistent styling.
    """

    def __init__(self, master=None, color: StyleColor = "primary", **kwargs):
        kwargs.update(variant="date")
        super().__init__(master, color=color, **kwargs)
