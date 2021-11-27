import calendar
from datetime import datetime
import tkinter as tk
import ttkbootstrap as ttk


class DatePickerPopup:
    
    def __init__(
        self,
        parent=None,
        title='',
        firstweekday=6,
        startdate=None,
        bootstyle='primary',
    ):
        """A widget that displays a calendar popup and returns the 
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

        Parameters
        ----------
        parent : Widget
            The parent widget; the popup will appear to the bottom-right
            of the parent widget. If no parent is provided, the widget
            is centered on the screen.

        title : str
            The text that appears on the titlebar. By default = ''.

        firstweekday : int
            Specifies the first day of the week. 0=Monday, 1=Tuesday, 
            etc.... Default = 6 (Sunday).

        startdate : datetime
            The date to be in focus when the widget is displayed.
            Default = Current date.

        bootstyle : str
            The following colors can be used to change the color of the
            title and hover / pressed color -> primary, secondary, info,
            warning, success, danger, light, dark.            
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
        
        self.setup_calendar()
        self.root.grab_set()
        self.root.wait_window()

    def setup_calendar(self):
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
        #self.root.overrideredirect(True)
        self.root.resizable(False, False)
        self.frm_calendar.update_idletasks() # actualize geometry

        # create visual components
        self.draw_titlebar()
        self.draw_calendar()
        
        # make toplevel visible
        self.set_window_position()
        self.root.deiconify()
        self.root.attributes('-topmost', True)

    def update_widget_bootstyle(self):
        self.frm_title.configure(bootstyle=self.bootstyle)
        self.title.configure(bootstyle=f'{self.bootstyle}-inverse')
        self.prev_period.configure(style=f'Chevron.{self.bootstyle}.TButton')
        self.next_period.configure(style=f'Chevron.{self.bootstyle}.TButton')

    def draw_calendar(self):
        self.update_widget_bootstyle()
        self.root.minsize(width=226, height=1)
        self.set_title()
        self.current_month_days()
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

                    def selected(x=row, y=col): self.on_date_selected(x, y)

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

    def draw_titlebar(self):
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
        for col in self.header_columns():
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

    def set_title(self):
        _titledate = f'{self.date.strftime("%B %Y")}'
        self.titlevar.set(value=_titledate)

    def current_month_days(self):
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

    def header_columns(self):
        """Create and return a list of weekdays to be used as a header
        in the calendar. The order of the weekdays is based on the 
        `firstweekday` property.
        
        Returns
        -------
        List[str]
            A list of weekday column names for the calendar header.
        """
        weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        header = weekdays[self.firstweekday:] + weekdays[:self.firstweekday]
        return header

    def on_date_selected(self, row, col):
        """Callback for selecting a date.
        
        An index is assigned to each date button that corresponds to
        the dates in the `monthdates` matrix. When the user clicks a 
        button to select a date, the index from this button is used 
        to lookup the date value of the button based on the row and 
        column index reference. This value is saved in the 
        `date_selected` property and the `Toplevel` is destroyed.

        Parameters
        ----------
        index : Tuple[int, int]
            A row and column index of the date selected; to be found
            in the `monthdates` matrix.

        Returns
        -------
        datetime
            The date selected
        """
        self.date_selected = self.monthdates[row][col]
        self.root.destroy()

    def selection_callback(func):
        """Calls the decorated `func` and redraws the calendar."""
        def inner(self, *args):
            func(self, *args)
            self.frm_dates.destroy()
            self.draw_calendar()
        return inner

    @selection_callback
    def on_next_month(self):
        """Increment the calendar data to the next month"""
        year, month = calendar._nextmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()

    @selection_callback
    def on_next_year(self, *_):
        """Increment the calendar data to the next year"""
        year = self.date.year + 1
        month = self.date.month
        self.date = datetime(year=year, month=month, day=1).date()

    @selection_callback
    def on_prev_month(self):
        """Decrement the calendar to the previous year"""
        year, month = calendar._prevmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()        

    @selection_callback
    def on_prev_year(self, *_):
        year = self.date.year - 1
        month = self.date.month
        self.date = datetime(year=year, month=month, day=1).date()

    @selection_callback
    def on_reset_date(self, *_):
        """Set the calendar to the start date"""
        self.date = self.startdate

    def set_window_position(self):
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


def ask_date(
    parent=None,
    title='',
    firstweekday=6,
    startdate=None,
    bootstyle='primary'
):
    """Shows a calendar popup and returns the selection.

    Parameters
    ----------
    parent : Widget
        The parent widget; the popup will appear to the bottom-right of 
        the parent widget. If no parent is provided, the widget is 
        centered on the screen. 

    title: str
        The text that appears on the popup titlebar. By default = ''.

    firstweekday : int
        Specifies the first day of the week. ``0`` is Monday, ``6`` is 
        Sunday (the default). 

    startdate : datetime
        The date to be in focus when the widget is displayed; 
        Default = `datetime.today().date()`

    bootstyle : str
        The following colors can be used to change the color of the
        title and hover / pressed color -> primary, secondary, info,
        warning, success, danger, light, dark.       
        
    Returns
    -------
    datetime
        The date selected; the current date if no date is selected.
    """
    chooser = DatePickerPopup(
        parent=parent,
        title=title,
        firstweekday=firstweekday,
        startdate=startdate,
        bootstyle=bootstyle
    )
    return chooser.date_selected
