from datetime import datetime
from ttkbootstrap.widgets import Frame, Entry, Button
from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.dialogs.query import Querybox


class DateEntry(Frame):
    """
    A themed date entry widget combining a text entry and a calendar popup button.

    This widget provides a convenient way to select a date using a calendar dialog.
    The selected date is formatted and displayed in the entry field. A calendar
    icon button next to the entry launches a modal date picker.

    Features:
    ---------
    - Combines an `Entry` and a `Button` into a single frame.
    - Launches a themed calendar popup on click.
    - Supports custom date formatting (`dateformat`).
    - Supports localization of the first weekday.
    - Generates `<<DateEntrySelected>>` virtual event when a date is chosen.
    - Configurable style using `color`, and themed calendar button (`variant='date'`).
    - Entry and Button subwidgets accessible via `.entry` and `.button`.

    Customization:
    --------------
    - `color`: applies to both entry and button
    - `popuptitle`: sets the title shown in the popup dialog
    - `startdate`: initial date value or dialog focus
    - `firstweekday`: sets the starting weekday (0=Monday, 6=Sunday)
    - `dateformat`: strftime-style formatting pattern

    Example:
        ```python
        DateEntry(root, color="primary", dateformat="%Y-%m-%d")
        ```
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
        """
        Initialize a new `DateEntry` widget.

        Parameters:
            master (Widget, optional):
                The parent container.

            dateformat (str, optional):
                Format string used to render and parse the date value in the entry.
                Defaults to locale-specific date ("%x"). See https://strftime.org/.

            firstweekday (int, optional):
                Index of the starting weekday in the popup (0 = Monday, 6 = Sunday).
                Defaults to 6 (Sunday).

            startdate (datetime, optional):
                The initial date displayed in the entry and calendar. Defaults to today.

            color (StyleColor, optional):
                The theme color applied to the entry and calendar button.

            popuptitle (str, optional):
                The title displayed in the date picker popup dialog.

            **kwargs:
                Additional options passed to the outer `Frame`, such as `padding`, `style`,
                or layout geometry options. The `width` option is passed to the internal entry.
        """
        self._dateformat = dateformat
        self._firstweekday = firstweekday

        self._start_date = startdate or datetime.today()
        self._color = color
        self._popup_title = popuptitle

        super().__init__(master, color=color, **kwargs)

        # add visual components
        entry_kwargs = {}
        if "width" in kwargs:
            entry_kwargs["width"] = kwargs.pop("width")

        self.entry = Entry(self, color=color, **entry_kwargs)
        self.entry.pack(side="left", fill="x", expand=1)
        self.button = DateButton(self, color=color, command=self._on_date_ask)
        self.button.pack(side="left")

        # starting value
        self.entry.insert("end", self._start_date.strftime(self._dateformat))

    def __getitem__(self, key: str):
        return self.configure(cnf=key)

    def __setitem__(self, key: str, value):
        self.configure(cnf=None, **{key: value})

    def _configure_set(self, **kwargs):
        """Override configures method to allow for setting custom
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
        """Override the configure get method"""
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
            old_date = datetime.strptime(_val, self._dateformat)
        except ValueError:
            print("[DateEntry] date entry text does not match", self._dateformat)
            old_date = datetime.today()
            self.entry.delete(0, "end")
            self.entry.insert("end", old_date.strftime(self._dateformat))

        self._start_date = old_date

        # get the new date and insert into the entry
        print('creating a datebox of color', self._color)
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
    A themed button styled as a calendar trigger for the DateEntry widget.

    This button uses a preset `variant='date'` to visually indicate its role
    as a date picker trigger. It is commonly used as a subcomponent of `DateEntry`.

    Parameters:
        master (Widget, optional):
            The parent container.

        color (StyleColor, optional):
            The style color for the button (e.g., "primary", "info").

        **kwargs:
            Additional ttk button options. The `variant` is automatically set to "date".
    """

    def __init__(self, master=None, color: StyleColor = "primary", **kwargs):
        kwargs.update(variant="date")
        super().__init__(master, color=color, **kwargs)
