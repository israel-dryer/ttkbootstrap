import calendar
import re
from datetime import datetime
from tkinter import IntVar, Toplevel, StringVar
from tkinter import ttk
from tkinter.ttk import Frame, Entry

from PIL import Image, ImageTk, ImageDraw
from ttkbootstrap import Style

COLOR_PATTERN = re.compile(r'(^primary|secondary|success|info|warning|danger)')


def ask_date(parent=None,
             startdate=None,
             firstweekday=6,
             style='TCalendar'):
    """Generate a popup date chooser and return the selected date
    
    Args:
        parent (Widget): The parent widget; the popup will appear to the bottom-right of the parent widget. If no
            parent is provided, the widget is centered on the screen.
        firstweekday (int): Specifies the first day of the week. ``0`` is Monday, ``6`` is Sunday (the default).
        startdate (datetime): The date to be in focus when the widget is displayed; defaults to the current date.
        style (str): The ``ttk`` style used to render the widget.

    Returns:
        The date selected; the current date if no date is selected.
    """
    chooser = DateChooserPopup(parent=parent, startdate=startdate, firstweekday=firstweekday, style=style)
    return chooser.date_selected


class DateEntry(Frame):
    """A date entry widget that combines a ``ttk.Combobox`` and a ttk.Button`` with a callback attached to the
    ``ask_date`` function.

    When pressed, displays a date chooser popup and then inserts the returned value into the combobox.

    Optionally set the ``startdate`` of the date chooser popup by typing in a date that is consistent with the format
    that you have specified with the ``dateformat`` parameter. By default this is `%Y-%m-%d`.

    Change the style of the widget by using the `TCalendar` style, with the colors: 'primary', 'secondary',
    'success', 'info', 'warning', 'danger'. By default, the `primary.TCalendar` style is applied.

    Change the starting weekday with the ``firstweekday`` parameter for geographies that do not start the week
    on `Sunday`, which is the widget default.
    """

    def __init__(self,
                 master=None,
                 dateformat='%Y-%m-%d',
                 firstweekday=6,
                 startdate=None,
                 style='TCalendar',
                 **kw):
        """
        Args:
            master (Widget): The parent widget.
            dateformat (str): The format string used to render the text in the entry widget. Default is '%Y-%m-%d'. For
                more information on date formats, see the python documentation or https://strftime.org/.
            firstweekday (int): Specifies the first day of the week. ``0`` is Monday, ``6`` is Sunday (the default).
            startdate (datetime): The date to be in focus when the calendar is displayed. Current date is default.
            **kw: Optional keyword arguments to be passed to containing frame widget.
        """
        super().__init__(master=master, **kw)
        self.dateformat = dateformat
        self.firstweekday = firstweekday
        self.startdate = startdate or datetime.today()
        self.base_style = style

        # entry widget
        entry_style, button_style = self.generate_widget_styles()
        self.entry = Entry(self, name='date-entry', style=entry_style)
        self.entry.pack(side='left', fill='x', expand='yes')

        # calendar button
        image_color = self.tk.call("ttk::style", "lookup", button_style, '-%s' % 'foreground', None, None)
        if 'system' in image_color.lower():
            self.image = self.draw_button_image(self.convert_system_color(image_color))
        else:
            self.image = self.draw_button_image(image_color)
        self.button = ttk.Button(self, image=self.image, command=self.on_date_ask, padding=(2, 2), style=button_style)
        self.button.pack(side='left')

        # TODO consider adding data validation: https://www.geeksforgeeks.org/python-tkinter-validating-entry-widget/
        self.entry.insert('end', self.startdate.strftime(dateformat))  # starting entry value

    def convert_system_color(self, systemcolorname):
        """Convert a system color name to a hexadecimal value

        Args:
            systemcolorname (str): a system color name, such as `SystemButtonFace`
        """
        r, g, b = [x >> 8 for x in self.winfo_rgb(systemcolorname)]
        return f'#{r:02x}{g:02x}{b:02x}'

    def draw_button_image(self, color):
        """Draw a calendar button image of the specified color

        Image reference: https://www.123rf.com/photo_117523637_stock-vector-modern-icon-calendar-button-applications.html

        Args:
            color (str): the color to draw the image foreground.

        Returns:
            PhotoImage: the image created for the calendar button.
        """
        im = Image.new('RGBA', (21, 22))
        draw = ImageDraw.Draw(im)

        # outline
        draw.rounded_rectangle([1, 3, 20, 21], radius=2, outline=color, width=1)

        # page spirals
        draw.rectangle([4, 1, 5, 5], fill=color)
        draw.rectangle([10, 1, 11, 5], fill=color)
        draw.rectangle([16, 1, 17, 5], fill=color)

        # row 1
        draw.rectangle([7, 9, 9, 11], fill=color)
        draw.rectangle([11, 9, 13, 11], fill=color)
        draw.rectangle([15, 9, 17, 11], fill=color)

        # row 2
        draw.rectangle([3, 13, 5, 15], fill=color)
        draw.rectangle([7, 13, 9, 15], fill=color)
        draw.rectangle([11, 13, 13, 15], fill=color)
        draw.rectangle([15, 13, 17, 15], fill=color)

        # row 3
        draw.rectangle([3, 17, 5, 19], fill=color)
        draw.rectangle([7, 17, 9, 19], fill=color)
        draw.rectangle([11, 17, 13, 19], fill=color)

        return ImageTk.PhotoImage(im)

    def generate_widget_styles(self):
        """Generate all the styles required for this widget from the ``base_style``.

        Returns:
            Tuple[str]: the styles to be used for entry and button widgets.
        """
        match = re.search(COLOR_PATTERN, self.base_style)
        color = '' if not match else match.group(0) + '.'
        entry_style = f'{color}TEntry'
        button_style = f'{color}TButton'
        return entry_style, button_style

    def on_date_ask(self):
        """A callback for the date push button.
        
        Try to grab the initial date from the entry if possible. However, if this date is not valid, use the current
        date and print a warning message to the console.
        """
        try:
            self.startdate = datetime.strptime(self.entry.get(), self.dateformat)
        except Exception as e:
            print(e)
            self.startdate = datetime.today()
        olddate = datetime.strptime(self.entry.get() or self.startdate, self.dateformat)
        newdate = ask_date(self.entry, startdate=olddate, firstweekday=self.firstweekday, style=self.base_style)
        self.entry.delete('0', 'end')
        self.entry.insert('end', newdate.strftime(self.dateformat))
        self.entry.focus_force()


class DateChooserPopup:
    """A custom **ttkbootstrap** widget that displays a calendar and allows the user to select a date which is returned
    as a ``datetime`` object for the date selected.

    The widget displays the current date by default unless a ``startdate`` is provided. The month can be changed by
    clicking on the chevrons to the right and left of the month-year title which is displayed on the top-center of
    the widget. A "left-click" will move the calendar `one month`. A "right-click" will move the calendar
    `one year`.

    A "right-click" on the `month-year` title will reset the calendar widget to the starting date.

    The starting weekday can be changed with the ``firstweekday`` parameter for geographies that do not start the
    week on `Sunday`, which is the widget default.

    The widget grabs focus and all screen events until released. If you want to cancel a date selection, you must
    click on the "X" button at the top-right hand corner of the widget.

    Styles can be applied to the widget by using the `TCalendar` style with the optional colors: 'primary',
    'secondary', 'success', 'info', 'warning', and 'danger'. By default, the `primary.TCalendar` style is applied.
    """

    def __init__(self,
                 parent=None,
                 firstweekday=6,
                 startdate=None,
                 style='TCalendar'):
        """
        Args:
            parent (Widget): The parent widget; the popup is displayed to the bottom-right of the parent widget.
            startdate (datetime): The date to be in focus when the calendar is displayed. Current date is default.
            firstweekday (int): Specifies the first day of the week. ``0`` is Monday, ``6`` is Sunday (the default).
            style (str): The ``ttk`` style used to render the widget.
            **kw:
        """
        self.parent = parent
        self.root = Toplevel()
        self.firstweekday = firstweekday
        self.startdate = startdate
        self.styles = {'calendar': style}
        self.generate_widget_styles()

        self.date_selected = startdate or datetime.today()
        self.date = startdate or self.date_selected
        self.calendar = calendar.Calendar(firstweekday=firstweekday)

        self.cframe = ttk.Frame(self.root, padding=0, borderwidth=1, relief='raised', style=self.styles['frame'])
        self.xframe = ttk.Frame(self.cframe, style=self.styles['frame'])
        self.tframe = ttk.Frame(self.cframe, style=self.styles['frame'])
        self.wframe = ttk.Frame(self.cframe)
        self.dframe = None

        self.titlevar = StringVar(value=f'{self.date.strftime("%B %Y")}')
        self.datevar = IntVar()

        self.setup()
        self.root.grab_set()
        self.root.wait_window()

    def draw_calendar(self):
        """Create the days of the week elements"""
        self.titlevar.set(f'{self.date.strftime("%B %Y")}')
        self.monthdays = self.calendar.monthdayscalendar(self.date.year, self.date.month)
        self.monthdates = self.calendar.monthdatescalendar(self.date.year, self.date.month)

        self.dframe = ttk.Frame(self.cframe)
        self.dframe.pack(fill='both', expand='yes')
        self.set_geometry()

        # calendar days
        for row, wk in enumerate(self.monthdays):
            for col, day in enumerate(wk):
                self.dframe.columnconfigure(col, weight=1)
                if day == 0:
                    lbl = ttk.Label(self.dframe, text=self.monthdates[row][col].day, anchor='center')
                    lbl.configure(style='secondary.TLabel', padding=(0, 0, 0, 10))
                    lbl.grid(row=row, column=col, sticky='nswe')
                else:
                    if all([
                        day == self.date_selected.day,
                        self.date.month == self.date_selected.month,
                        self.date.year == self.date_selected.year
                    ]):
                        day_style = self.styles['selected']
                    else:
                        day_style = self.styles['calendar']

                    rb = ttk.Radiobutton(self.dframe, variable=self.datevar, value=day, text=day, style=day_style)
                    rb.configure(padding=(0, 0, 0, 10), command=lambda x=row, y=col: self.on_date_selected([x, y]))
                    rb.grid(row=row, column=col, sticky='nswe')

    def draw_titlebar(self):
        """Create the title bar"""
        # previous month button
        self.btn_prev = ttk.Button(self.tframe, text='«', style=self.styles['chevron'], command=self.on_prev_month)
        self.btn_prev.bind('<Button-3>', self.on_prev_year, '+')
        self.btn_prev.pack(side='left')

        # month and year title
        self.title_label = ttk.Label(self.tframe, textvariable=self.titlevar, anchor='center')
        self.title_label.configure(style=self.styles['title'], font='helvetica 11')
        self.title_label.pack(side='left', fill='x', expand='yes')
        self.title_label.bind('<Button-1>', self.on_reset_date)

        # next month button
        self.btn_next = ttk.Button(self.tframe, text='»', command=self.on_next_month, style=self.styles['chevron'])
        self.btn_next.bind('<Button-3>', self.on_next_year, '+')
        self.btn_next.pack(side='left')

        # days of the week header
        for wd in self.weekday_header():
            wd_lbl = ttk.Label(self.wframe, text=wd, anchor='center', padding=(0, 5, 0, 10))
            wd_lbl.configure(style='secondary.Inverse.TLabel')
            wd_lbl.pack(side='left', fill='x', expand='yes')

    def generate_widget_styles(self):
        """Generate all the styles required for this widget from the ``base_style``."""
        match = re.search(COLOR_PATTERN, self.styles['calendar'])
        color = 'primary.' if not match else match.group(0) + '.'
        self.styles.update({'chevron': f'chevron.{color}TButton'})
        self.styles.update({'exit': f'exit.{color}TButton'})
        self.styles.update({'title': f'{color}Inverse.TLabel'})
        self.styles.update({'frame': f'{color}TFrame'})
        self.styles.update({'selected': f'{color}Toolbutton'})

    def on_date_selected(self, index):
        """Callback for selecting a date.

        Assign the selected date to the ``date_selected`` property and then destroy the toplevel widget.

        Args:
            index (Tuple[int]): a tuple containing the row and column index of the date selected to be found in the
                ``monthdates`` property.
        """
        row, col = index
        self.date_selected = self.monthdates[row][col]
        self.root.destroy()

    def on_next_month(self):
        """Callback for changing calendar to next month"""
        year, month = calendar._nextmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()
        self.dframe.destroy()
        self.draw_calendar()

    def on_next_year(self, *args):
        """Callback for changing calendar to next year"""
        year = self.date.year + 1
        self.date = datetime(year=year, month=self.date.month, day=1).date()
        self.dframe.destroy()
        self.draw_calendar()

    def on_prev_month(self):
        """Callback for changing calendar to previous month"""
        year, month = calendar._prevmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()
        self.dframe.destroy()
        self.draw_calendar()

    def on_prev_year(self, *args):
        """Callback for changing calendar to previous year"""
        year = self.date.year - 1
        self.date = datetime(year=year, month=self.date.month, day=1).date()
        self.dframe.destroy()
        self.draw_calendar()

    def on_reset_date(self, *args):
        """Callback for clicking the month-year title; reset the date to the start date"""
        self.date = self.startdate
        self.dframe.destroy()
        self.draw_calendar()

    def set_geometry(self):
        """Adjust the window size based on the number of weeks in the month"""
        w = 226
        h = 255 if len(self.monthdates) == 5 else 285  # this needs to be adjusted if I change the font size.
        if self.parent:
            xpos = self.parent.winfo_rootx() + self.parent.winfo_width()
            ypos = self.parent.winfo_rooty() + self.parent.winfo_height()
            self.root.geometry(f'{w}x{h}+{xpos}+{ypos}')
        else:
            xpos = self.root.winfo_screenwidth() // 2 - w
            ypos = self.root.winfo_screenheight() // 2 - h
            self.root.geometry(f'{w}x{h}+{xpos}+{ypos}')

    def setup(self):
        """Setup the calendar widget"""
        self.cframe.pack(fill='both', expand='yes')
        self.xframe.pack(fill='x')
        self.tframe.pack(fill='x')
        self.wframe.pack(fill='x')

        # setup the top level window
        self.root.withdraw()  # hide the window until setup is complete
        self.root.transient(self.parent)
        self.root.overrideredirect(True)
        self.root.resizable(False, False)
        self.cframe.update_idletasks()  # actualize the geometry

        # create the visual components
        ttk.Button(self.xframe, text="⨉", command=self.root.destroy, style=self.styles['exit']).pack(side='right')
        self.draw_titlebar()
        self.draw_calendar()
        self.root.deiconify()  # make the window visible.
        self.root.attributes('-topmost', True)

    def weekday_header(self):
        """Creates and returns a list of weekdays to be used as a header in the calendar based on the firstweekday. The
        order of the weekdays is based on the ``firstweekday`` property.

        Returns:
            List: a list of weekday headers
        """
        weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        return weekdays[self.firstweekday:] + weekdays[:self.firstweekday]


if __name__ == '__main__':
    style = Style()
    root = style.master
    root.title('Date Chooser')

    DateEntry(padding=10).pack(fill='x', expand='yes')

    root.mainloop()
