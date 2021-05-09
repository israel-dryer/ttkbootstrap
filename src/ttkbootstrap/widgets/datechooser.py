import calendar
from datetime import datetime
from tkinter import IntVar, Toplevel, StringVar
from tkinter import ttk
from tkinter.ttk import Frame, Entry

from PIL import Image, ImageTk, ImageDraw
from ttkbootstrap import Style, Colors


def ask_date(parent=None,
             startdate=None,
             firstweekday=6
             ):
    """Generate a popup date chooser and return the selected date
    
    Args:
        parent (Widget): The parent widget; the popup will appear to the bottom-right of the parent widget. If no
            date is provided; it will default to the current month, and the current date will be highlighted.
        startdate (datetime): the date to be in focus when the widget is displayed. Current date is default.
        firstweekday (int): specifies the first day of the week. ``0`` is Monday, ``6`` is Sunday (the default).

    Returns:
        The date selected; the current date if no date is selected.
    """
    chooser = DateChooserPopup(parent=parent, startdate=startdate, firstweekday=firstweekday)
    return chooser.date_selected


class DateEntry(Frame):

    def __init__(self,
                 master=None,
                 dateformat='%B %d, %Y',
                 firstweekday=6,
                 startdate=None,
                 **kw
                 ):
        """
        Args:
            master (Widget): The parent widget.
            dateformat (str): The format string used to render the text in the entry widget. Default is '%B %d, %Y'.
            firstweekday (int): Specifies the first day of the week. ``0`` is Monday, ``6`` is Sunday (the default).
            startdate (datetime): The date to be in focus when the calendar is displayed. Current date is default.
            **kw: Optional keyword arguments to be passed to containing frame widget.
        """
        super().__init__(master=master, **kw)
        self.dateformat = dateformat
        self.firstweekday = firstweekday
        self.image = self.draw_button_image('white')
        self.startdate = startdate or datetime.today()

        # widget layout
        self.entry = Entry(self, name='date-entry')
        self.entry.pack(side='left', fill='x', expand='yes')
        self.button = ttk.Button(self, image=self.image, command=self.on_date_ask, padding=(2, 2))
        self.button.pack(side='left')

        # TODO consider adding data validation: https://www.geeksforgeeks.org/python-tkinter-validating-entry-widget/
        self.entry.insert('end', self.startdate.strftime(dateformat))  # starting entry value

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

    def on_date_ask(self):
        """A callback for when a date is requested from the widget button.
        
        Try to grab the initial date from the entry if possible. However, if this date is note valid, use the current
        date and print a message to the console.
        """
        try:
            self.startdate = datetime.strptime(self.entry.get(), self.dateformat)
        except Exception as e:
            print(e)
            self.startdate = datetime.today()
        olddate = datetime.strptime(self.entry.get() or self.startdate, self.dateformat)
        newdate = ask_date(self.entry, startdate=olddate, firstweekday=self.firstweekday)
        self.entry.delete('0', 'end')
        self.entry.insert('end', newdate.strftime(self.dateformat))
        self.entry.focus_force()


class DateChooserPopup:

    def __init__(self,
                 parent=None,
                 firstweekday=6,
                 startdate=None
                 ):
        """
        Args:
            parent (Widget): The parent widget; the popup is displayed to the bottom-right of the parent widget.
            startdate (datetime): The date to be in focus when the calendar is displayed. Current date is default.
            firstweekday (int): Specifies the first day of the week. ``0`` is Monday, ``6`` is Sunday (the default).
            **kw:
        """
        self.parent = parent
        self.root = Toplevel()
        self.firstweekday = firstweekday
        self.startdate = startdate

        self.date_selected = startdate or datetime.today()
        self.date = startdate or self.date_selected
        self.calendar = calendar.Calendar(firstweekday=firstweekday)

        self.cframe = ttk.Frame(self.root, padding=0, borderwidth=1, relief='raised')
        self.xframe = ttk.Frame(self.cframe, style='primary.TFrame')
        self.tframe = ttk.Frame(self.cframe, style='primary.TFrame')
        self.wframe = ttk.Frame(self.cframe)
        self.dframe = None

        self.titlevar = StringVar(value=f'{self.date.strftime("%B %Y")}')
        self.datevar = IntVar()

        self.setup()
        self.root.grab_set()
        self.root.wait_window()

    def define_style(self):
        pass

    def draw_calendar(self):
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

                        day_style = 'success.Toolbutton'
                    else:
                        day_style = 'calendar.primary.Outline.Toolbutton'

                    rb = ttk.Radiobutton(self.dframe, variable=self.datevar, value=day, text=day, style=day_style)
                    rb.configure(padding=(0, 0, 0, 10), command=lambda x=row, y=col: self.on_date_selected([x, y]))
                    rb.grid(row=row, column=col, sticky='nswe')

    def draw_titlebar(self):
        """Create the title bar"""
        # previous month button
        self.btn_prev = ttk.Button(self.tframe, text='«', style='primary.TButton', command=self.on_prev_month)
        self.btn_prev.configure(style='chevron.primary.TButton')
        self.btn_prev.pack(side='left')
        # month and year title
        self.title_label = ttk.Label(self.tframe, textvariable=self.titlevar, anchor='center')
        self.title_label.configure(style='primary.Inverse.TLabel', font='helvetica 11')
        self.title_label.pack(side='left', fill='x', expand='yes')
        # next month button
        self.btn_next = ttk.Button(self.tframe, text='»', style='primary.TButton', command=self.on_next_month)
        self.btn_next.configure(style='chevron.primary.TButton')
        self.btn_next.pack(side='left')
        # days of the week header
        for wd in self.weekday_header():
            wd_lbl = ttk.Label(self.wframe, text=wd, anchor='center', padding=(0, 5, 0, 10))
            wd_lbl.configure(style='secondary.Inverse.TLabel')
            wd_lbl.pack(side='left', fill='x', expand='yes')

    def on_date_selected(self, index):
        row, col = index
        self.date_selected = self.monthdates[row][col]
        self.root.destroy()

    def on_next_month(self):
        year, month = calendar._nextmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()
        self.dframe.destroy()
        self.draw_calendar()

    def on_prev_month(self):
        year, month = calendar._prevmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()
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
            xpos = self.root.winfo_screenwidth()//2 - w
            ypos = self.root.winfo_screenheight() //2 - h
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
        ttk.Button(self.xframe, text="⨉", command=self.root.destroy, style='exit.primary.TButton').pack(side='right')
        self.draw_titlebar()
        self.draw_calendar()
        self.root.deiconify()  # make the window visible.
        self.root.attributes('-topmost', True)

    def weekday_header(self):
        """Returns a list of weekdays to be used as a header in the calendar based on the firstweekday"""
        weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        return weekdays[self.firstweekday:] + weekdays[:self.firstweekday]


if __name__ == '__main__':
    # TODO setup the styling in the __init__ file, and setup the class so that it can be easilily modified.
    # TODO add documentation to all classes and methods.
    # TODO reduce the padding on the DateEntry button for dark themes to account for the removed border on dark
    #   theme entry widgets.

    style = Style('lumen')
    pressed_vd = -0.2
    disabled_bg = (Colors.update_hsv(style.colors.inputbg, vd=-0.2) if style.theme.type == 'light' else
                   Colors.update_hsv(style.colors.inputbg, vd=-0.3))
    style.configure('calendar.primary.Outline.Toolbutton',
                    lightcolor=style.colors.bg,
                    darkcolor=style.colors.bg,
                    bordercolor=style.colors.bg)
    style.configure('exit.primary.TButton',
                    relief='flat',
                    font='helvetica 12')
    style.configure('chevron.primary.TButton', font='helvetica 14')
    style.map('exit.primary.TButton',
              background=[
                  ('disabled', disabled_bg),
                  ('pressed', '!disabled', Colors.update_hsv(style.colors.primary, vd=pressed_vd)),
                  ('hover', '!disabled', style.colors.danger)])

    root = style.master
    root.title('Date Chooser')
    DateEntry(padding=10).pack(fill='x', expand='yes')
    root.mainloop()
