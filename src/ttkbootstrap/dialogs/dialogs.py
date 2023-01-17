"""
    This module contains various base dialog base classes that can be 
    used to create custom dialogs for the end user. 

    These classes serve as the basis for the pre-defined static helper
    methods in the `Messagebox`, and `Querybox` container classes.
"""

import calendar
import textwrap
import locale
from datetime import datetime
from tkinter import font
import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.icons import Icon
from ttkbootstrap.constants import *
from tkinter import BaseWidget
from ttkbootstrap.localization import MessageCatalog


class Dialog(BaseWidget):
    """A simple dialog base class."""

    def __init__(self, parent=None, title="", alert=False):
        """
        Parameters:

            parent (Widget):
                Makes the window the logical parent of the message box.
                The messagebox is displayed on top of its parent window.

            title (str):
                The string displayed as the title of the message box.
                This option is ignored on Mac OS X, where platform
                guidelines forbid the use of a title on this kind of
                dialog.

            alert (bool):
                Ring the display's bell when the dialog is shown.
        """
        BaseWidget._setup(self, parent, {})
        self._winsys = self.master.tk.call("tk", "windowingsystem")
        self._parent = parent
        self._toplevel = None
        self._title = title or " "
        self._result = None
        self._alert = alert
        self._initial_focus = None

    def _locate(self):
        toplevel = self._toplevel
        if self._parent is None:
            master = toplevel.master
        else:
            master = self._parent
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        toplevel.geometry(f"+{x}+{y}")

    def show(self, position=None):
        """Show the popup dialog
        Parameters:

            position: Tuple[int, int]
                The x and y coordinates used to position the dialog. By
                default the dialog will anchor at the NW corner of the
                parent window.
        """
        self._result = None
        self.build()

        if position is None:
            self._locate()
        else:
            try:
                x, y = position
                self._toplevel.geometry(f'+{x}+{y}')
            except:
                self._locate()

        self._toplevel.deiconify()
        if self._alert:
            self._toplevel.bell()

        if self._initial_focus:
            self._initial_focus.focus_force()

        self._toplevel.grab_set()
        self._toplevel.wait_window()

    def create_body(self, master):
        """Create the dialog body.

        This method should be overridden and is called by the `build`
        method. Set the `self._initial_focus` for the widget that
        should receive the initial focus.

        Parameters:

            master (Widget):
                The parent widget.
        """
        raise NotImplementedError

    def create_buttonbox(self, master):
        """Create the dialog button box.

        This method should be overridden and is called by the `build`
        method. Set the `self._initial_focus` for the button that
        should receive the intial focus.

        Parameters:

            master (Widget):
                The parent widget.
        """
        raise NotImplementedError

    def build(self):
        """Build the dialog from settings"""

        # setup toplevel based on widowing system
        if self._winsys == "win32":
            self._toplevel = ttk.Toplevel(
                transient=self.master,
                title=self._title,
                resizable=(0, 0),
                minsize=(250, 15),
                iconify=True,
            )
        else:
            self._toplevel = ttk.Toplevel(
                transient=self.master,
                title=self._title,
                resizable=(0, 0),
                windowtype="dialog",
                iconify=True,
            )

        self._toplevel.withdraw()  # reset the iconify state

        # bind <Escape> event to window close
        self._toplevel.bind("<Escape>", lambda _: self._toplevel.destroy())

        # set position of popup from parent window
        # self._locate()

        # create widgets
        self.create_body(self._toplevel)
        self.create_buttonbox(self._toplevel)

        # update the window before showing
        self._toplevel.update_idletasks()

    @property
    def result(self):
        """Returns the result of the dialog."""
        return self._result


class MessageDialog(Dialog):
    """A simple modal dialog class that can be used to build simple
    message dialogs.

    Displays a message and a set of buttons. Each of the buttons in the
    message window is identified by a unique symbolic name. After the
    message window is popped up, the message box awaits for the user to
    select one of the buttons. Then it returns the symbolic name of the
    selected button. Use a `Toplevel` widget for more advanced modal
    dialog designs.
    """

    def __init__(
        self,
        message,
        title=" ",
        buttons=None,
        command=None,
        width=50,
        parent=None,
        alert=False,
        default=None,
        padding=(20, 20),
        icon=None,
        **kwargs,
    ):
        """
        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the message box.
                This option is ignored on Mac OS X, where platform
                guidelines forbid the use of a title on this kind of
                dialog.

            buttons (List[str]):
                A list of buttons to appear at the bottom of the popup
                messagebox. The buttons can be a list of strings which
                will define the symbolic name and the button text.
                `['OK', 'Cancel']`. Alternatively, you can assign a
                bootstyle to each button by using the colon to separate the
                button text and the bootstyle. If no colon is found, then
                the style is set to 'primary' by default.
                `['OK:success','Cancel:danger']`.

            command (Tuple[Callable, str]):
                The function to invoke when the user closes the dialog.
                The actual command is a tuple that consists of the
                function to call and the symbolic name of the button that
                closes the dialog.

            width (int):
                The maximum number of characters per line in the message.
                If the text stretches beyond the limit, the line will break
                at the word.

            parent (Widget):
                Makes the window the logical parent of the message box.
                The messagebox is displayed on top of its parent window.

            alert (bool):
                Ring the display's bell when the dialog is shown.

            default (str):
                The symbolic name of the default button. The default
                button is invoked when the the <Return> key is pressed.
                If no default is provided, the right-most button in the
                button list will be set as the default.,

            padding  (Union[int, Tuple[int]]):
                The amount of space between the border and the widget
                contents.

            icon (str):
                An image path, path-like object or image data to be
                displayed to the left of the text.

            **kwargs (Dict):
                Other optional keyword arguments.

        Example:

            ```python
            root = tk.Tk()

            md = MessageDialog("Displays a message with buttons.")
            md.show()
            ```
        """
        super().__init__(parent, title, alert)
        self._message = message
        self._command = command
        self._width = width
        self._alert = alert
        self._default = (default,)
        self._padding = padding
        self._icon = icon
        self._localize = kwargs.get("localize")

        if buttons is None:
            self._buttons = [
                f"{MessageCatalog.translate('Cancel')}:secondary",
                f"{MessageCatalog.translate('OK')}:primary",
            ]
        else:
            self._buttons = buttons

    def create_body(self, master):
        """Overrides the parent method; adds the message section."""
        container = ttk.Frame(master, padding=self._padding)
        if self._icon:
            try:
                # assume this is image data
                self._img = ttk.PhotoImage(data=self._icon)
                icon_lbl = ttk.Label(container, image=self._img)
                icon_lbl.pack(side=LEFT, padx=5)
            except:
                try:
                    # assume this is a file path
                    self._img = ttk.PhotoImage(file=self._icon)
                    icon_lbl = ttk.Label(container, image=self._img)
                    icon_lbl.pack(side=LEFT, padx=5)
                except:
                    # icon is neither data nor a valid file path
                    print("MessageDialog icon is invalid")

        if self._message:
            for msg in self._message.split("\n"):
                message = "\n".join(textwrap.wrap(msg, width=self._width))
                message_label = ttk.Label(container, text=message)
                message_label.pack(pady=(0, 3), fill=X, anchor=N)
        container.pack(fill=X, expand=True)

    def create_buttonbox(self, master):
        """Overrides the parent method; adds the message buttonbox"""
        frame = ttk.Frame(master, padding=(5, 5))

        button_list = []

        for i, button in enumerate(self._buttons[::-1]):
            cnf = button.split(":")
            if len(cnf) == 2:
                text, bootstyle = cnf
            else:
                text = cnf[0]
                bootstyle = "secondary"

            if self._localize == True:
                text = MessageCatalog.translate(text)

            btn = ttk.Button(frame, bootstyle=bootstyle, text=text)
            btn.configure(command=lambda b=btn: self.on_button_press(b))
            btn.pack(padx=2, side=RIGHT)
            btn.lower()  # set focus traversal left-to-right
            button_list.append(btn)

            if self._default is not None and text == self._default:
                self._initial_focus = btn
            elif self._default is None and i == 0:
                self._initial_focus = btn

        # bind default button to return key press and set focus
        self._toplevel.bind("<Return>", lambda _, b=btn: b.invoke())
        self._toplevel.bind("<KP_Enter>", lambda _, b=btn: b.invoke())

        ttk.Separator(self._toplevel).pack(fill=X)
        frame.pack(side=BOTTOM, fill=X, anchor=S)

        if not self._initial_focus:
            self._initial_focus = button_list[0]

    def on_button_press(self, button):
        """Save result, destroy the toplevel, and execute command."""
        self._result = button["text"]
        command = self._command
        if command is not None:
            command()
        self._toplevel.destroy()

    def show(self, position=None):
        """Create and display the popup messagebox."""
        super().show(position)


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


class DatePickerDialog:
    """A dialog that displays a calendar popup and returns the
    selected date as a datetime object.

    The current date is displayed by default unless the `startdate`
    parameter is provided.

    The month can be changed by clicking the chevrons to the left
    and right of the month-year title.

    Left-click the arrow to move the calendar by one month.
    Right-click the arrow to move the calendar by one year.
    Right-click the title to reset the calendar to the start date.

    The starting weekday can be changed with the `firstweekday`
    parameter for geographies that do not start the calendar on
    Sunday, which is the default.

    The widget grabs focus and all screen events until released.
    If you want to cancel a date selection, click the 'X' button
    at the top-right corner of the widget.

    The bootstyle api may be used to change the style of the widget.
    The available colors include -> primary, secondary, success,
    info, warning, danger, light, dark.

    ![](../../assets/dialogs/date-picker-dialog.png)

    """

    locale.setlocale(locale.LC_ALL, locale.setlocale(locale.LC_TIME, ""))

    def __init__(
        self,
        parent=None,
        title=" ",
        firstweekday=6,
        startdate=None,
        bootstyle=PRIMARY,
    ):
        """
        Parameters:

            parent (Widget):
                The parent widget; the popup will appear to the
                bottom-right of the parent widget. If no parent is
                provided, the widget is centered on the screen.

            title (str):
                The text that appears on the titlebar.

            firstweekday (int):
                Specifies the first day of the week. 0=Monday,
                1=Tuesday, etc...

            startdate (datetime):
                The date to be in focus when the widget is
                displayed.

            bootstyle (str):
                The following colors can be used to change the color of
                the title and hover / pressed color -> primary,
                secondary, info, warning, success, danger, light, dark.
        """
        self.parent = parent
        self.root = ttk.Toplevel(
            title=title,
            transient=self.parent,
            resizable=(False, False),
            topmost=True,
            minsize=(226, 1),
            iconify=True,
        )
        self.firstweekday = firstweekday
        self.startdate = startdate or datetime.today().date()
        self.bootstyle = bootstyle or PRIMARY

        self.date_selected = self.startdate
        self.date = startdate or self.date_selected
        self.calendar = calendar.Calendar(firstweekday=firstweekday)

        self.titlevar = ttk.StringVar()
        self.datevar = ttk.IntVar()

        self._setup_calendar()
        self.root.grab_set()
        self.root.wait_window()

    def _setup_calendar(self):
        """Setup the calendar widget"""
        # create the widget containers
        self.frm_calendar = ttk.Frame(
            master=self.root, padding=0, borderwidth=0, relief=FLAT
        )
        self.frm_calendar.pack(fill=BOTH, expand=YES)
        self.frm_title = ttk.Frame(self.frm_calendar, padding=(3, 3))
        self.frm_title.pack(fill=X)
        self.frm_header = ttk.Frame(self.frm_calendar, bootstyle=SECONDARY)
        self.frm_header.pack(fill=X)

        # setup the toplevel widget
        self.root.withdraw()  # reset the iconify state
        self.frm_calendar.update_idletasks()  # actualize geometry

        # create visual components
        self._draw_titlebar()
        self._draw_calendar()

        # make toplevel visible
        self._set_window_position()
        self.root.deiconify()

    def _update_widget_bootstyle(self):
        self.frm_title.configure(bootstyle=self.bootstyle)
        self.title.configure(bootstyle=f"{self.bootstyle}-inverse")
        self.prev_period.configure(style=f"Chevron.{self.bootstyle}.TButton")
        self.next_period.configure(style=f"Chevron.{self.bootstyle}.TButton")

    def _draw_calendar(self):
        self._update_widget_bootstyle()
        self._set_title()
        self._current_month_days()
        self.frm_dates = ttk.Frame(self.frm_calendar)
        self.frm_dates.pack(fill=BOTH, expand=YES)

        for row, weekday_list in enumerate(self.monthdays):
            for col, day in enumerate(weekday_list):
                self.frm_dates.columnconfigure(col, weight=1)
                if day == 0:
                    ttk.Label(
                        master=self.frm_dates,
                        text=self.monthdates[row][col].day,
                        anchor=CENTER,
                        padding=5,
                        bootstyle=SECONDARY,
                    ).grid(row=row, column=col, sticky=NSEW)
                else:
                    if all(
                        [
                            day == self.date_selected.day,
                            self.date.month == self.date_selected.month,
                            self.date.year == self.date_selected.year,
                        ]
                    ):
                        day_style = "secondary-toolbutton"
                    else:
                        day_style = f"{self.bootstyle}-calendar"

                    def selected(x=row, y=col):
                        self._on_date_selected(x, y)

                    btn = ttk.Radiobutton(
                        master=self.frm_dates,
                        variable=self.datevar,
                        value=day,
                        text=day,
                        bootstyle=day_style,
                        padding=5,
                        command=selected,
                    )
                    btn.grid(row=row, column=col, sticky=NSEW)

    def _draw_titlebar(self):
        """Draw the calendar title bar which includes the month title
        and the buttons that increment and decrement the selected
        month.

        In addition to the previous and next MONTH commands that are
        assigned to the button press, a "right-click" event is assigned
        to each button that causes the calendar to move to the previous
        and next YEAR.
        """
        # create and pack the title and action buttons
        self.prev_period = ttk.Button(
            master=self.frm_title, text="«", command=self.on_prev_month
        )
        self.prev_period.pack(side=LEFT)

        self.title = ttk.Label(
            master=self.frm_title,
            textvariable=self.titlevar,
            anchor=CENTER,
            font="-weight bold",
        )
        self.title.pack(side=LEFT, fill=X, expand=YES)

        self.next_period = ttk.Button(
            master=self.frm_title,
            text="»",
            command=self.on_next_month,
        )
        self.next_period.pack(side=LEFT)

        # bind "year" callbacks to action buttons
        self.prev_period.bind("<Button-3>", self.on_prev_year, "+")
        self.next_period.bind("<Button-3>", self.on_next_year, "+")
        self.title.bind("<Button-1>", self.on_reset_date)

        # create and pack days of the week header
        for col in self._header_columns():
            ttk.Label(
                master=self.frm_header,
                text=col,
                anchor=CENTER,
                padding=5,
                bootstyle=(SECONDARY, INVERSE),
            ).pack(side=LEFT, fill=X, expand=YES)

    def _set_title(self):
        _titledate = f'{self.date.strftime("%B %Y")}'
        self.titlevar.set(value=_titledate.capitalize())

    def _current_month_days(self):
        """Fetch the day numbers and dates for all days in the current
        month. `monthdays` is a list of days as integers, and
        `monthdates` is a list of `datetime` objects.
        """
        self.monthdays = self.calendar.monthdayscalendar(
            year=self.date.year, month=self.date.month
        )
        self.monthdates = self.calendar.monthdatescalendar(
            year=self.date.year, month=self.date.month
        )

    def _header_columns(self):
        """Create and return a list of weekdays to be used as a header
        in the calendar. The order of the weekdays is based on the
        `firstweekday` property.

        Returns:

            List[str]:
                A list of weekday column names for the calendar header.
        """
        weekdays = [
            MessageCatalog.translate("Mo"),
            MessageCatalog.translate("Tu"),
            MessageCatalog.translate("We"),
            MessageCatalog.translate("Th"),
            MessageCatalog.translate("Fr"),
            MessageCatalog.translate("Sa"),
            MessageCatalog.translate("Su"),
        ]
        header = weekdays[self.firstweekday :] + weekdays[: self.firstweekday]
        return header

    def _on_date_selected(self, row, col):
        """Callback for selecting a date.

        An index is assigned to each date button that corresponds to
        the dates in the `monthdates` matrix. When the user clicks a
        button to select a date, the index from this button is used
        to lookup the date value of the button based on the row and
        column index reference. This value is saved in the
        `date_selected` property and the `Toplevel` is destroyed.

        Parameters:

            index (Tuple[int, int]):
                A row and column index of the date selected; to be
                found in the `monthdates` matrix.

        Returns:

            datetime:
                The date selected
        """
        self.date_selected = self.monthdates[row][col]
        self.root.destroy()

    def _selection_callback(func):
        """Calls the decorated `func` and redraws the calendar."""

        def inner(self, *args):
            func(self, *args)
            self.frm_dates.destroy()
            self._draw_calendar()

        return inner

    @_selection_callback
    def on_next_month(self):
        """Increment the calendar data to the next month"""
        year, month = self._nextmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_next_year(self, *_):
        """Increment the calendar data to the next year"""
        year = self.date.year + 1
        month = self.date.month
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_prev_month(self):
        """Decrement the calendar to the previous year"""
        year, month = self._prevmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_prev_year(self, *_):
        year = self.date.year - 1
        month = self.date.month
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_reset_date(self, *_):
        """Set the calendar to the start date"""
        self.date = self.startdate

    def _set_window_position(self):
        """Move the window the to bottom-right of the parent widget, or
        the top-left corner of the master window if no parent is 
        provided.
        """
        if self.parent:
            xpos = self.parent.winfo_rootx() + self.parent.winfo_width()
            ypos = self.parent.winfo_rooty() + self.parent.winfo_height()
            self.root.geometry(f"+{xpos}+{ypos}")
        else:
            xpos = self.root.master.winfo_rootx()
            ypos = self.root.master.winfo_rooty()
            self.root.geometry(f"+{xpos}+{ypos}")

    @staticmethod
    def _nextmonth(year, month):
        if month == 12:
            return year + 1, 1
        else:
            return year, month + 1

    @staticmethod
    def _prevmonth(year, month):
        if month == 1:
            return year - 1, 12
        else:
            return year, month - 1


class FontDialog(Dialog):

    """A dialog that displays a variety of options for choosing a font.

    This dialog constructs and returns a `Font` object based on the
    options selected by the user. The initial font is based on OS
    settings and will vary.

    The font object is returned when the **Ok** button is pressed and
    can be passed to any widget that accepts a _font_ configuration
    option.

    ![](../../assets/dialogs/querybox-get-font.png)
    """

    def __init__(self, title="Font Selector", parent=None):
        title = MessageCatalog.translate(title)
        super().__init__(parent=parent, title=title)
        self._style = ttk.Style()
        self._default = font.nametofont("TkDefaultFont")
        self._actual = self._default.actual()
        self._size = ttk.Variable(value=self._actual["size"])
        self._family = ttk.Variable(value=self._actual["family"])
        self._slant = ttk.Variable(value=self._actual["slant"])
        self._weight = ttk.Variable(value=self._actual["weight"])
        self._overstrike = ttk.Variable(value=self._actual["overstrike"])
        self._underline = ttk.Variable(value=self._actual["underline"])
        self._preview_font = font.Font()
        self._slant.trace_add("write", self._update_font_preview)
        self._weight.trace_add("write", self._update_font_preview)
        self._overstrike.trace_add("write", self._update_font_preview)
        self._underline.trace_add("write", self._update_font_preview)

        _headingfont = font.nametofont("TkHeadingFont")
        _headingfont.configure(weight="bold")

        self._update_font_preview()
        self._families = set([self._family.get()])
        for f in font.families():
            if all([f, not f.startswith("@"), "emoji" not in f.lower()]):
                self._families.add(f)

    def create_body(self, master):
        width = utility.scale_size(master, 600)
        height = utility.scale_size(master, 500)
        self._toplevel.geometry(f"{width}x{height}")

        family_size_frame = ttk.Frame(master, padding=10)
        family_size_frame.pack(fill=X, anchor=N)
        self._initial_focus = self._font_families_selector(family_size_frame)
        self._font_size_selector(family_size_frame)
        self._font_options_selectors(master, padding=10)
        self._font_preview(master, padding=10)

    def create_buttonbox(self, master):
        container = ttk.Frame(master, padding=(5, 10))
        container.pack(fill=X)

        ok_btn = ttk.Button(
            master=container,
            bootstyle="primary",
            text=MessageCatalog.translate("OK"),
            command=self._on_submit,
        )
        ok_btn.pack(side=RIGHT, padx=5)
        ok_btn.bind("<Return>", lambda _: ok_btn.invoke())

        cancel_btn = ttk.Button(
            master=container,
            bootstyle="secondary",
            text=MessageCatalog.translate("Cancel"),
            command=self._on_cancel,
        )
        cancel_btn.pack(side=RIGHT, padx=5)
        cancel_btn.bind("<Return>", lambda _: cancel_btn.invoke())

    def _font_families_selector(self, master):
        container = ttk.Frame(master)
        container.pack(fill=BOTH, expand=YES, side=LEFT)

        header = ttk.Label(
            container,
            text=MessageCatalog.translate("Family"),
            font="TkHeadingFont",
        )
        header.pack(fill=X, pady=(0, 2), anchor=N)

        listbox = ttk.Treeview(
            master=container,
            height=5,
            show="",
            columns=[0],
        )
        listbox.column(0, width=utility.scale_size(listbox, 250))
        listbox.pack(side=LEFT, fill=BOTH, expand=YES)

        listbox_vbar = ttk.Scrollbar(
            container,
            command=listbox.yview,
            orient=VERTICAL,
            bootstyle="rounded",
        )
        listbox_vbar.pack(side=RIGHT, fill=Y)
        listbox.configure(yscrollcommand=listbox_vbar.set)

        for f in self._families:
            listbox.insert("", iid=f, index=END, tags=[f], values=[f])
            listbox.tag_configure(f, font=(f, self._size.get()))

        iid = self._family.get()
        listbox.selection_set(iid)  # select default value
        listbox.see(iid)  # ensure default is visible
        listbox.bind(
            "<<TreeviewSelect>>", lambda e: self._on_select_font_family(e)
        )
        return listbox

    def _font_size_selector(self, master):
        container = ttk.Frame(master)
        container.pack(side=LEFT, fill=Y, padx=(10, 0))

        header = ttk.Label(
            container,
            text=MessageCatalog.translate("Size"),
            font="TkHeadingFont",
        )
        header.pack(fill=X, pady=(0, 2), anchor=N)

        sizes_listbox = ttk.Treeview(container, height=7, columns=[0], show="")
        sizes_listbox.column(0, width=utility.scale_size(sizes_listbox, 24))

        sizes = [*range(8, 13), *range(13, 30, 2), 36, 48, 72]
        for s in sizes:
            sizes_listbox.insert("", iid=s, index=END, values=[s])

        iid = self._size.get()
        sizes_listbox.selection_set(iid)
        sizes_listbox.see(iid)
        sizes_listbox.bind(
            "<<TreeviewSelect>>", lambda e: self._on_select_font_size(e)
        )

        sizes_listbox_vbar = ttk.Scrollbar(
            master=container,
            orient=VERTICAL,
            command=sizes_listbox.yview,
            bootstyle="round",
        )
        sizes_listbox.configure(yscrollcommand=sizes_listbox_vbar.set)
        sizes_listbox.pack(side=LEFT, fill=Y, expand=YES, anchor=N)
        sizes_listbox_vbar.pack(side=LEFT, fill=Y, expand=YES)

    def _font_options_selectors(self, master, padding: int):
        container = ttk.Frame(master, padding=padding)
        container.pack(fill=X, padx=2, pady=2, anchor=N)

        weight_lframe = ttk.Labelframe(
            container, text=MessageCatalog.translate("Weight"), padding=5
        )
        weight_lframe.pack(side=LEFT, fill=X, expand=YES)
        opt_normal = ttk.Radiobutton(
            master=weight_lframe,
            text=MessageCatalog.translate("normal"),
            value="normal",
            variable=self._weight,
        )
        opt_normal.invoke()
        opt_normal.pack(side=LEFT, padx=5, pady=5)
        opt_bold = ttk.Radiobutton(
            master=weight_lframe,
            text=MessageCatalog.translate("bold"),
            value="bold",
            variable=self._weight,
        )
        opt_bold.pack(side=LEFT, padx=5, pady=5)

        slant_lframe = ttk.Labelframe(
            container, text=MessageCatalog.translate("Slant"), padding=5
        )
        slant_lframe.pack(side=LEFT, fill=X, padx=10, expand=YES)
        opt_roman = ttk.Radiobutton(
            master=slant_lframe,
            text=MessageCatalog.translate("roman"),
            value="roman",
            variable=self._slant,
        )
        opt_roman.invoke()
        opt_roman.pack(side=LEFT, padx=5, pady=5)
        opt_italic = ttk.Radiobutton(
            master=slant_lframe,
            text=MessageCatalog.translate("italic"),
            value="italic",
            variable=self._slant,
        )
        opt_italic.pack(side=LEFT, padx=5, pady=5)

        effects_lframe = ttk.Labelframe(
            container, text=MessageCatalog.translate("Effects"), padding=5
        )
        effects_lframe.pack(side=LEFT, padx=(2, 0), fill=X, expand=YES)
        opt_underline = ttk.Checkbutton(
            master=effects_lframe,
            text=MessageCatalog.translate("underline"),
            variable=self._underline,
        )
        opt_underline.pack(side=LEFT, padx=5, pady=5)
        opt_overstrike = ttk.Checkbutton(
            master=effects_lframe,
            text=MessageCatalog.translate("overstrike"),
            variable=self._overstrike,
        )
        opt_overstrike.pack(side=LEFT, padx=5, pady=5)

    def _font_preview(self, master, padding: int):
        container = ttk.Frame(master, padding=padding)
        container.pack(fill=BOTH, expand=YES, anchor=N)

        header = ttk.Label(
            container,
            text=MessageCatalog.translate("Preview"),
            font="TkHeadingFont",
        )
        header.pack(fill=X, pady=2, anchor=N)

        content = MessageCatalog.translate(
            "The quick brown fox jumps over the lazy dog."
        )
        self._preview_text = ttk.Text(
            master=container,
            height=3,
            font=self._preview_font,
            highlightbackground=self._style.colors.primary,
        )
        self._preview_text.insert(END, content)
        self._preview_text.pack(fill=BOTH, expand=YES)
        container.pack_propagate(False)

    def _on_select_font_family(self, e):
        tree: ttk.Treeview = self._toplevel.nametowidget(e.widget)
        fontfamily = tree.selection()[0]
        self._family.set(value=fontfamily)
        self._update_font_preview()

    def _on_select_font_size(self, e):
        tree: ttk.Treeview = self._toplevel.nametowidget(e.widget)
        fontsize = tree.selection()[0]
        self._size.set(value=fontsize)
        self._update_font_preview()

    def _on_submit(self) -> font.Font:
        self._toplevel.destroy()
        return self.result

    def _on_cancel(self):
        self._toplevel.destroy()

    def _update_font_preview(self, *_):
        family = self._family.get()
        size = self._size.get()
        slant = self._slant.get()
        overstrike = self._overstrike.get()
        underline = self._underline.get()

        self._preview_font.config(
            family=family,
            size=size,
            slant=slant,
            overstrike=overstrike,
            underline=underline,
        )
        try:
            self._preview_text.configure(font=self._preview_font)
        except:
            pass
        self._result = self._preview_font


class Messagebox:
    """This class contains various static methods that show popups with
    a message to the end user with various arrangments of buttons
    and alert options."""

    @staticmethod
    def show_info(message, title=" ", parent=None, alert=False, **kwargs):
        """Display a modal dialog box with an OK button and an INFO
        icon.

        ![](../../assets/dialogs/messagebox-show-info.png)

        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            alert (bool):
                Specified whether to ring the display bell.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        dialog = MessageDialog(
            message=message,
            title=title,
            alert=alert,
            parent=parent,
            buttons=["OK:primary"],
            icon=Icon.info,
            localize=True,
            **kwargs
        )
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog.show(position)

    @staticmethod
    def show_warning(message, title=" ", parent=None, alert=True, **kwargs):
        """Display a modal dialog box with an OK button and a
        warning icon. Also will ring the display bell.

        ![](../../assets/dialogs/messagebox-show-warning.png)

        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            alert (bool):
                Specified whether to ring the display bell.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            buttons=["OK:primary"],
            icon=Icon.warning,
            alert=alert,
            localize=True,
            **kwargs,
        )
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog.show(position)

    @staticmethod
    def show_error(message, title=" ", parent=None, alert=True, **kwargs):
        """Display a modal dialog box with an OK button and an
        error icon. Also will ring the display bell.

        ![](../../assets/dialogs/messagebox-show-error.png)

        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            alert (bool):
                Specified whether to ring the display bell.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            buttons=["OK:primary"],
            icon=Icon.error,
            alert=alert,
            localize=True,
            **kwargs,
        )
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog.show(position)

    @staticmethod
    def show_question(
        message,
        title=" ",
        parent=None,
        buttons=["No:secondary", "Yes:primary"],
        alert=True,
        **kwargs,
    ):
        """Display a modal dialog box with yes, no buttons and a
        question icon. Also will ring the display bell. You may also
        change the button scheme using the `buttons` parameter.

        ![](../../assets/dialogs/messagebox-show-question.png)

        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            buttons (List[str]):
                A list of buttons to appear at the bottom of the popup
                messagebox. The buttons can be a list of strings which
                will define the symbolic name and the button text.
                `['OK', 'Cancel']`. Alternatively, you can assign a
                bootstyle to each button by using the colon to separate the
                button text and the bootstyle. If no colon is found, then
                the style is set to 'primary' by default.
                `['Yes:success','No:danger']`.

            alert (bool):
                Specified whether to ring the display bell.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            buttons=buttons,
            icon=Icon.question,
            alert=alert,
            localize=True,
            **kwargs,
        )
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog.show(position)
        return dialog.result

    @staticmethod
    def ok(message, title=" ", alert=False, parent=None, **kwargs):
        """Display a modal dialog box with an OK button and and optional
        bell alert.

        ![](../../assets/dialogs/messagebox-ok.png)

        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            alert (bool):
                Specified whether to ring the display bell.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        dialog = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=["OK:primary"],
            localize=True,
            **kwargs,
        )
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog.show(position)

    @staticmethod
    def okcancel(message, title=" ", alert=False, parent=None, **kwargs):
        """Displays a modal dialog box with OK and Cancel buttons and
        return the symbolic name of the button pressed.

        ![](../../assets/dialogs/messagebox-ok-cancel.png)

        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            alert (bool):
                Specified whether to ring the display bell.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        dialog = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            localize=True,
            **kwargs,
        )
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog.show(position)
        return dialog.result

    @staticmethod
    def yesno(message, title=" ", alert=False, parent=None, **kwargs):
        """Display a modal dialog box with YES and NO buttons and return
        the symbolic name of the button pressed.

        ![](../../assets/dialogs/messagebox-yes-no.png)

        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            alert (bool):
                Specified whether to ring the display bell.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        dialog = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            buttons=["No", "Yes:primary"],
            alert=alert,
            localize=True,
            **kwargs,
        )
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog.show(position)
        return dialog.result

    @staticmethod
    def yesnocancel(message, title=" ", alert=False, parent=None, **kwargs):
        """Display a modal dialog box with YES, NO, and Cancel buttons,
        and return the symbolic name of the button pressed.

        ![](../../assets/dialogs/messagebox-yes-no-cancel.png)

        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            alert (bool):
                Specified whether to ring the display bell.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            **kwargs (Dict):
                Optional keyword arguments.

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        dialog = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=["Cancel", "No", "Yes:primary"],
            localize=True,
            **kwargs,
        )
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog.show(position)
        return dialog.result

    @staticmethod
    def retrycancel(message, title=" ", alert=False, parent=None, **kwargs):
        """Display a modal dialog box with RETRY and Cancel buttons;
        returns the symbolic name of the button pressed.

        ![](../../assets/dialogs/messagebox-retry-cancel.png)

        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            alert (bool):
                Specified whether to ring the display bell.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        dialog = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=["Cancel", "Retry:primary"],
            localize=True,
            **kwargs,
        )
        if "position" in kwargs:
            position = kwargs.pop("position")
        else:
            position = None
        dialog.show(position)
        return dialog.result


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
        from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog

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
        startdate=None,
        bootstyle="primary",
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

            bootstyle (str):
                The following colors can be used to change the color of the
                title and hover / pressed color -> primary, secondary, info,
                warning, success, danger, light, dark.

        Returns:

            datetime:
                The date selected; the current date if no date is selected.
        """
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
        dialog = FontDialog(parent=parent, **kwargs)
        dialog.show(position)
        return dialog.result
