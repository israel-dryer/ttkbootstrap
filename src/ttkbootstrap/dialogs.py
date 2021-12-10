"""
    This module contains various base dialog base classes that can be 
    used to create custom dialogs for the end user. 

    These classes serve as the basis for the pre-defined static helper
    methods in the `Messagebox`, and `Querybox` container classes.
"""

import calendar
import textwrap
from datetime import datetime
import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
from ttkbootstrap import utility
from tkinter import Toplevel, Variable
from tkinter import _get_default_root
from ttkbootstrap.constants import *


class Dialog:
    """A simple dialog base class."""

    def __init__(
        self,
        parent=None,
        title=None,
        alert=False
    ):
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
        self.master = parent or _get_default_root('Dialog')
        self._winsys = self.master.tk.call('tk', 'windowingsystem')
        self._toplevel = None
        self._title = title
        self._result = None
        self._alert = alert
        self._initial_focus = None

    def _locate(self):
        toplevel = self._toplevel
        master = toplevel.master
        screen_height = toplevel.winfo_screenheight()
        screen_width = toplevel.winfo_screenwidth()

        toplevel.update_idletasks()
        if master.winfo_viewable():
            m_width = master.winfo_width()
            m_height = master.winfo_height()
            m_x = master.winfo_rootx()
            m_y = master.winfo_rooty()
        else:
            m_width = screen_width
            m_height = screen_height
            m_x = m_y = 0
        w_width = toplevel.winfo_reqwidth()
        w_height = toplevel.winfo_reqheight()
        x = int(m_x + (m_width - w_width) * 0.45)
        y = int(m_y + (m_height - w_height) * 0.3)
        if x+w_width > screen_width:
            x = screen_width - w_width
        elif x < 0:
            x = 0
        if y+w_height > screen_height:
            y = screen_height - w_height
        elif y < 0:
            y = 0
        toplevel.geometry(f'+{x}+{y}')

    def show(self):
        """Show the popup dialog"""

        self._result = None
        self.build()
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
        if self._winsys == 'win32':
            self._toplevel = Toplevel(self.master)
            self._toplevel.attributes('-toolwindow')
            self._toplevel.minsize(250, 15)
        else:
            self._toplevel = Toplevel(self.master)
            self._toplevel.attributes('-type', 'dialog')

        self._toplevel.withdraw()  # hide until drawn
        self._toplevel.resizable(0, 0)
        self._toplevel.transient(self.master)
        self._toplevel.title(self._title)

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
        title=None,
        buttons=['Cancel:secondary', 'OK:primary'],
        command=None,
        width=50,
        parent=None,
        alert=False,
        default=None,
        padding=(20, 20)
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

        Example:

            ```python
            root = tk.Tk()

            md = MessageDialog("Displays a message with buttons.")
            md.show()
            ```
        """
        super().__init__(parent, title)
        self._message = message
        self._buttons = buttons
        self._command = command
        self._width = width
        self._alert = alert
        self._default = default,
        self._padding = padding

    def create_body(self, master):
        """Overrides the parent method; adds the message section."""
        frame = ttk.Frame(master, padding=self._padding)
        if self._message:
            for i, msg in enumerate(self._message.split('\n')):
                message = '\n'.join(textwrap.wrap(msg, width=self._width))
                message_label = ttk.Label(frame, text=message)
                message_label.pack(pady=(0, 5), fill=X, anchor=N)
        frame.pack(fill=X, expand=True)

    def create_buttonbox(self, master):
        """Overrides the parent method; adds the message buttonbox"""
        frame = ttk.Frame(master, padding=(5, 10))

        button_list = []

        for i, button in enumerate(self._buttons[::-1]):
            cnf = button.split(':')
            if len(cnf) == 2:
                text, bootstyle = cnf
            else:
                text = cnf[0]
                bootstyle = 'secondary'

            btn = ttk.Button(frame, bootstyle=bootstyle, text=text)
            btn.bind('<Return>', lambda _: btn.invoke())
            btn.configure(command=lambda b=btn: self.on_button_press(b))
            btn.pack(padx=5, side=RIGHT)
            btn.lower()  # set focus traversal left-to-right
            button_list.append(btn)

            if self._default is not None and text == self._default:
                self._initial_focus = btn
            elif self._default is None and i == 0:
                self._initial_focus = btn

        # bind default button to return key press and set focus
        self._toplevel.bind('<Return>', lambda _, b=btn: b.invoke())
        self._toplevel.bind('<KP_Enter>', lambda _, b=btn: b.invoke())

        ttk.Separator(self._toplevel).pack(fill=X)
        frame.pack(side=BOTTOM, fill=X, anchor=S)

        if not self._initial_focus:
            self._initial_focus = button_list[0]

    def on_button_press(self, button):
        """Save result, destroy the toplevel, and execute command."""
        self._result = button['text']
        command = self._command
        if command is not None:
            command()
        self._toplevel.destroy()

    def show(self):
        """Create and display the popup messagebox."""
        super().show()


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
        """Overrides the parent method; adds the message buttonbox"""
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
    """

    def __init__(
        self,
        parent=None,
        title='',
        firstweekday=6,
        startdate=None,
        bootstyle='primary',
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
        self.root = tk.Toplevel()
        self.root.title(title)
        self.firstweekday = firstweekday
        self.startdate = startdate or datetime.today().date()
        self.bootstyle = bootstyle or 'primary'

        self.date_selected = self.startdate
        self.date = startdate or self.date_selected
        self.calendar = calendar.Calendar(firstweekday=firstweekday)

        self.titlevar = tk.StringVar()
        self.datevar = tk.IntVar()

        self._setup_calendar()
        self.root.grab_set()
        self.root.wait_window()

    def _setup_calendar(self):
        """Setup the calendar widget"""
        # create the widget containers
        self.frm_calendar = ttk.Frame(
            master=self.root,
            padding=0,
            borderwidth=1,
            relief=tk.RAISED
        )
        self.frm_calendar.pack(fill=tk.BOTH, expand=tk.YES)
        self.frm_title = ttk.Frame(self.frm_calendar, padding=(3, 3))
        self.frm_title.pack(fill=tk.X)
        self.frm_header = ttk.Frame(self.frm_calendar, bootstyle='secondary')
        self.frm_header.pack(fill=tk.X)

        # setup the toplevel widget
        self.root.withdraw()
        self.root.transient(self.parent)
        # self.root.overrideredirect(True)
        self.root.resizable(False, False)
        self.frm_calendar.update_idletasks()  # actualize geometry

        # create visual components
        self._draw_titlebar()
        self._draw_calendar()

        # make toplevel visible
        self._set_window_position()
        self.root.deiconify()
        self.root.attributes('-topmost', True)

    def _update_widget_bootstyle(self):
        self.frm_title.configure(bootstyle=self.bootstyle)
        self.title.configure(bootstyle=f'{self.bootstyle}-inverse')
        self.prev_period.configure(style=f'Chevron.{self.bootstyle}.TButton')
        self.next_period.configure(style=f'Chevron.{self.bootstyle}.TButton')

    def _draw_calendar(self):
        self._update_widget_bootstyle()
        self.root.minsize(width=226, height=1)
        self._set_title()
        self._current_month_days()
        self.frm_dates = ttk.Frame(self.frm_calendar)
        self.frm_dates.pack(fill=tk.BOTH, expand=tk.YES)

        for row, weekday_list in enumerate(self.monthdays):
            for col, day in enumerate(weekday_list):
                self.frm_dates.columnconfigure(col, weight=1)
                if day == 0:
                    ttk.Label(
                        master=self.frm_dates,
                        text=self.monthdates[row][col].day,
                        anchor=tk.CENTER,
                        padding=5,
                        bootstyle='secondary'
                    ).grid(
                        row=row, column=col, sticky=tk.NSEW
                    )
                else:
                    if all([
                        day == self.date_selected.day,
                        self.date.month == self.date_selected.month,
                        self.date.year == self.date_selected.year
                    ]):
                        day_style = 'secondary-toolbutton'
                    else:
                        day_style = f'{self.bootstyle}-calendar'

                    def selected(x=row, y=col): self._on_date_selected(x, y)

                    btn = ttk.Radiobutton(
                        master=self.frm_dates,
                        variable=self.datevar,
                        value=day,
                        text=day,
                        bootstyle=day_style,
                        padding=5,
                        command=selected
                    )
                    btn.grid(row=row, column=col, sticky=tk.NSEW)

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
            master=self.frm_title,
            text='«',
            command=self.on_prev_month
        )
        self.prev_period.pack(side=tk.LEFT)

        self.title = ttk.Label(
            master=self.frm_title,
            textvariable=self.titlevar,
            anchor=tk.CENTER,
            font='-size 10 -weight bold'
        )
        self.title.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        self.next_period = ttk.Button(
            master=self.frm_title,
            text='»',
            command=self.on_next_month,
        )
        self.next_period.pack(side=tk.LEFT)

        # bind "year" callbacks to action buttons
        self.prev_period.bind('<Button-3>', self.on_prev_year, '+')
        self.next_period.bind('<Button-3>', self.on_next_year, '+')
        self.title.bind('<Button-1>', self.on_reset_date)

        # create and pack days of the week header
        for col in self._header_columns():
            ttk.Label(
                master=self.frm_header,
                text=col,
                anchor=tk.CENTER,
                padding=5,
                bootstyle='secondary-inverse'
            ).pack(
                side=tk.LEFT,
                fill=tk.X,
                expand=tk.YES
            )

    def _set_title(self):
        _titledate = f'{self.date.strftime("%B %Y")}'
        self.titlevar.set(value=_titledate)

    def _current_month_days(self):
        """Fetch the day numbers and dates for all days in the current
        month. `monthdays` is a list of days as integers, and 
        `monthdates` is a list of `datetime` objects.
        """
        self.monthdays = self.calendar.monthdayscalendar(
            year=self.date.year,
            month=self.date.month
        )
        self.monthdates = self.calendar.monthdatescalendar(
            year=self.date.year,
            month=self.date.month
        )

    def _header_columns(self):
        """Create and return a list of weekdays to be used as a header
        in the calendar. The order of the weekdays is based on the 
        `firstweekday` property.

        Returns:

            List[str]:
                A list of weekday column names for the calendar header.
        """
        weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        header = weekdays[self.firstweekday:] + weekdays[:self.firstweekday]
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
        year, month = calendar._nextmonth(self.date.year, self.date.month)
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
        year, month = calendar._prevmonth(self.date.year, self.date.month)
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
        to the middle of the screen if no parent is provided.
        """
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        if self.parent:
            xpos = self.parent.winfo_rootx() + self.parent.winfo_width()
            ypos = self.parent.winfo_rooty() + self.parent.winfo_height()
            self.root.geometry(f'+{xpos}+{ypos}')
        else:
            xpos = self.root.winfo_screenwidth() // 2 - width
            ypos = self.root.winfo_screenheight() // 2 - height
            self.root.geometry(f'+{xpos}+{ypos}')


class FontDialog(Dialog):

    """A dialog that displays a variety of options for choosing a font.

    This dialog constructs and returns a `Font` object based on the
    options selected by the user. The initial font is based on OS 
    settings and will vary.

    The font object is returned when the **Ok** button is pressed and 
    can be passed to any widget that accepts a _font_ configuration
    option.       
    """

    def __init__(self, title='Font Selector', parent=None):
        super().__init__(parent=parent, title=title)
        self._style = ttk.Style()
        self._default = font.nametofont('TkDefaultFont')
        self._actual = self._default.actual()
        self._size = Variable(value=self._actual['size'])
        self._family = Variable(value=self._actual['family'])
        self._slant = Variable(value=self._actual['slant'])
        self._weight = Variable(value=self._actual['weight'])
        self._overstrike = Variable(value=self._actual['overstrike'])
        self._underline = Variable(value=self._actual['underline'])
        self._preview_font = font.Font()
        self._slant.trace_add("write", self._update_font_preview)
        self._weight.trace_add("write", self._update_font_preview)
        self._overstrike.trace_add("write", self._update_font_preview)
        self._underline.trace_add("write", self._update_font_preview)

        _headingfont = font.nametofont('TkHeadingFont')
        _headingfont.configure(weight='bold')

        self._update_font_preview()

        self._families = []
        for f in font.families():
            if f and not f.startswith('@') and 'emoji' not in f.lower():
                self._families.append(f)

    def create_body(self, master):
        width = utility.scale_size(master, 600)
        height = utility.scale_size(master, 375)
        self._toplevel.geometry(f'{width}x{height}')

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
            bootstyle='primary',
            text='OK',
            command=self._on_submit
        )
        ok_btn.pack(side=RIGHT, padx=5)
        ok_btn.bind("<Return>", lambda _: ok_btn.invoke())

        cancel_btn = ttk.Button(
            master=container,
            bootstyle='secondary',
            text='Cancel',
            command=self._on_cancel
        )
        cancel_btn.pack(side=RIGHT, padx=5)
        cancel_btn.bind("<Return>", lambda _: cancel_btn.invoke())

    def _font_families_selector(self, master):
        container = ttk.Frame(master)
        container.pack(fill=BOTH, expand=YES, side=LEFT)

        header = ttk.Label(container, text='Font Family', font='TkHeadingFont')
        header.pack(fill=X, pady=(0, 2), anchor=N)

        listbox = ttk.Treeview(
            master=container,
            height=5,
            show='',
            columns=[0],
        )
        listbox.column(0, width=utility.scale_size(listbox, 250))
        listbox.pack(side=LEFT, fill=BOTH, expand=YES)

        listbox_vbar = ttk.Scrollbar(
            container,
            command=listbox.yview,
            orient=VERTICAL,
            bootstyle='rounded'
        )
        listbox_vbar.pack(side=RIGHT, fill=Y)
        listbox.configure(yscrollcommand=listbox_vbar.set)

        for f in self._families:
            listbox.insert('', iid=f, index=END, tags=[f], values=[f])
            listbox.tag_configure(f, font=(f, self._size.get()))

        iid = self._family.get()
        listbox.selection_set(iid)  # select default value
        listbox.see(iid)  # ensure default is visible
        listbox.bind("<<TreeviewSelect>>",
                     lambda e: self._on_select_font_family(e))
        return listbox

    def _font_size_selector(self, master):
        container = ttk.Frame(master)
        container.pack(side=LEFT, fill=Y, padx=(10, 0))

        header = ttk.Label(container, text='Size', font='TkHeadingFont')
        header.pack(fill=X, pady=(0, 2), anchor=N)

        sizes_listbox = ttk.Treeview(container, height=7, columns=[0], show='')
        sizes_listbox.column(0, width=utility.scale_size(sizes_listbox, 24))

        sizes = [*range(8, 12), *range(12, 30, 2), 36, 48, 72]
        for s in sizes:
            sizes_listbox.insert('', iid=s, index=tk.END, values=[s])

        iid = self._size.get()
        sizes_listbox.selection_set(iid)
        sizes_listbox.see(iid)
        sizes_listbox.bind("<<TreeviewSelect>>",
                           lambda e: self._on_select_font_size(e))

        sizes_listbox_vbar = ttk.Scrollbar(
            master=container,
            orient=VERTICAL,
            command=sizes_listbox.yview,
            bootstyle='round'
        )
        sizes_listbox.configure(yscrollcommand=sizes_listbox_vbar.set)
        sizes_listbox.pack(side=LEFT, fill=Y, expand=YES, anchor=N)
        sizes_listbox_vbar.pack(side=LEFT, fill=Y, expand=YES)

    def _font_options_selectors(self, master, padding: int):
        container = ttk.Frame(master, padding=padding)
        container.pack(fill=X, padx=2, pady=2, anchor=N)

        weight_lframe = ttk.Labelframe(container, text="Weight", padding=5)
        weight_lframe.pack(side=LEFT, fill=X, expand=YES)
        opt_normal = ttk.Radiobutton(
            master=weight_lframe,
            text='normal',
            value='normal',
            variable=self._weight
        )
        opt_normal.invoke()
        opt_normal.pack(side=LEFT, padx=5, pady=5)
        opt_bold = ttk.Radiobutton(
            master=weight_lframe,
            text='bold',
            value='bold',
            variable=self._weight
        )
        opt_bold.pack(side=LEFT, padx=5, pady=5)

        slant_lframe = ttk.Labelframe(container, text="Slant", padding=5)
        slant_lframe.pack(side=LEFT, fill=X, padx=10, expand=YES)
        opt_roman = ttk.Radiobutton(
            master=slant_lframe,
            text='roman',
            value='roman',
            variable=self._slant
        )
        opt_roman.invoke()
        opt_roman.pack(side=LEFT, padx=5, pady=5)
        opt_italic = ttk.Radiobutton(
            master=slant_lframe,
            text='italic',
            value='italic',
            variable=self._slant
        )
        opt_italic.pack(side=LEFT, padx=5, pady=5)

        effects_lframe = ttk.Labelframe(container, text="Effects", padding=5)
        effects_lframe.pack(side=LEFT, padx=(2, 0), fill=X, expand=YES)
        opt_underline = ttk.Checkbutton(
            master=effects_lframe,
            text='underline',
            variable=self._underline
        )
        opt_underline.pack(side=LEFT, padx=5, pady=5)
        opt_overstrike = ttk.Checkbutton(
            master=effects_lframe,
            text='overstrike',
            variable=self._overstrike
        )
        opt_overstrike.pack(side=LEFT, padx=5, pady=5)

    def _font_preview(self, master, padding: int):
        container = ttk.Frame(master, padding=padding)
        container.pack(fill=BOTH, expand=YES, anchor=N)

        header = ttk.Label(container, text="Preview", font="TkHeadingFont")
        header.pack(fill=X, pady=2, anchor=N)

        content = "The quick brown fox jumped over the lazy dog."
        self._preview_text = tk.Text(
            master=container,
            height=3,
            font=self._preview_font,
            highlightbackground=self._style.colors.primary
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
            underline=underline
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
    def ok(message, title=None, alert=False, parent=None, **kwargs):
        """Display a modal dialog box with an OK button and and optional
        bell alert. 

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
        sd = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=['OK:primary'],
            **kwargs
        )
        sd.show()

    @staticmethod
    def okcancel(message, title=None, alert=False, parent=None, **kwargs):
        """Displays a modal dialog box with OK and Cancel buttons and
        return the symbolic name of the button pressed.

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
        sd = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            **kwargs
        )
        sd.show()
        return sd.result

    @staticmethod
    def yesno(message, title=None, alert=False, parent=None, **kwargs):
        """Display a modal dialog box with YES and NO buttons and return
        the symbolic name of the button pressed.

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
        sd = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            buttons=['No', 'Yes:primary'],
            alert=alert,
            **kwargs
        )
        sd.show()
        return sd.result

    @staticmethod
    def yesnocancel(message, title=None, alert=False, parent=None, **kwargs):
        """Display a modal dialog box with YES, NO, and Cancel buttons,
        and return the symbolic name of the button pressed.

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

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        sd = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=['Cancel', 'No', 'Yes:primary'],
            **kwargs
        )
        sd.show()
        return sd.result

    @staticmethod
    def retrycancel(message, title=None, alert=False, parent=None, **kwargs):
        """Display a modal dialog box with RETRY and Cancel buttons;
        returns the symbolic name of the button pressed.

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
        sd = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=['Cancel', 'Retry:primary'],
            **kwargs
        )
        sd.show()
        return sd.result


class Querybox:
    """This class contains various static methods that request data 
    from the end user."""

    @staticmethod
    def get_date(
        parent=None,
        title='',
        firstweekday=6,
        startdate=None,
        bootstyle='primary'
    ):
        """Shows a calendar popup and returns the selection.

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
            bootstyle=bootstyle
        )
        return chooser.date_selected

    @staticmethod
    def get_string(prompt='', title=None, initialvalue=None, parent=None,
                   **kwargs):
        """Request a string type input from the user.

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
        initialvalue = initialvalue or ''
        dialog = QueryDialog(prompt, title, initialvalue, parent=parent,
                             **kwargs)
        dialog.show()
        return dialog._result

    @staticmethod
    def get_integer(prompt='', title=None, initialvalue=None, minvalue=None,
                    maxvalue=None, parent=None, **kwargs):
        """Request an integer type input from the user.

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
        initialvalue = initialvalue or ''
        dialog = QueryDialog(prompt, title, initialvalue, minvalue, maxvalue,
                             datatype=int, parent=parent, **kwargs)
        dialog.show()
        return dialog._result

    @staticmethod
    def get_float(prompt='', title=None, initialvalue=None, minvalue=None,
                  maxvalue=None, parent=None, **kwargs):
        """Request a float type input from the user.

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
        initialvalue = initialvalue or ''
        dialog = QueryDialog(prompt, title, initialvalue, minvalue, maxvalue,
                             datatype=float, parent=parent, **kwargs)
        dialog.show()
        return dialog._result

    @staticmethod
    def get_font(parent=None, **kwargs):
        """Request a customized font

        Parameters:

            master (Widget):
                Makes the window the logical parent of the dialog box. The
                dialog is displayed on top of its parent window.

            **kwargs (Dict):
                Other keyword arguments.

        Returns:

            Font:
                A font object.
        """
        dialog = FontDialog(parent=parent, **kwargs)
        dialog.show()
        return dialog.result
