import tkinter as tk
from tkinter import ttk
from ttkbootstrap.dialogs.calendar import ask_date
from datetime import datetime


class DateEntry(ttk.Frame):

    def __init__(
        self,
        master=None,
        dateformat=r"%Y-%m-%d",
        firstweekday=6,
        startdate=None,
        bootstyle='primary',
        **kwargs
    ):
        """A date entry widget combines the `Combobox` and a `Button` 
        with a callback attached to the `ask_date` function.

        When pressed, a date chooser popup is displayed. The returned 
        value is inserted into the combobox.

        The date chooser popup will use the date in the combobox as the 
        date of focus if it is in the format specified by the 
        `dateformat` parameter. By default, this format is "%Y-%m-%d".

        The bootstyle api may be used to change the style of the widget.
        The available colors include -> primary, secondary, success, 
        info, warning, danger, light, dark.

        The starting weekday on the date chooser popup can be changed 
        with the `firstweekday` parameter. By default this value is 
        `6`, which represents "Sunday".

        Parameters
        ----------
        master : Widget, optional
            The parent wiget.

        dateformat : str, optional
            The format string used to render the text in the entry
            widget. Default = "%Y-%m-%d. For more information on 
            acceptable formats, see https://strftime.org/
        
        firstweekday : int, optional
            Specifies the first day of the week. 0=Monday, 1=Tuesday, 
            etc...  Default = 6 (Sunday).

        startdate : datetime, optional
            The date that is in focus when the widget is displayed. By 
            default, the current date.

        bootstyle : str
            A style keyword used to set the focus color of the entry
            and the background color of the date button. Available 
            options include -> primary, secondary, success, info,
            warning, danger, dark, light.    
        
        **kwargs : Dict[str, Any]
            Other keyword arguments passed to the frame containing the 
            entry and date button.
        """
        self.dateformat = dateformat
        self.firstweekday = firstweekday
        
        self.startdate = startdate or datetime.today()
        self.bootstyle = bootstyle
        super().__init__(master, **kwargs)

        # add visual components
        self.entry = ttk.Entry(self, bootstyle=self.bootstyle)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        self.button = ttk.Button(
            master=self, 
            command=self.on_date_ask, 
            bootstyle=f'{self.bootstyle}-date'
        )
        self.button.pack(side=tk.LEFT)

        # starting value
        self.entry.insert(tk.END, self.startdate.strftime(self.dateformat))

    def configure(self, *args, **kwargs):
        """Override configure method to allow for setting disabled and 
        readonly state on entry/button"""
        if 'state' in kwargs:
            state = kwargs.pop('state')
            if state in ['readonly', 'invalid']:
                self.entry.configure(state=state)
            elif    state == 'disabled':
                self.entry.configure(state=state)
                self.button.configure(state=state)
            else:
                kwargs[state] = state    
        super(ttk.Frame, self).configure(*args, **kwargs)

    def on_date_ask(self):
        """Callback for pushing the date button"""
        _val = self.entry.get()
        try:
            self.startdate = datetime.strptime(_val, self.dateformat)
        except Exception as e:
            print("Date entry text does not match", self.dateformat)
            self.startdate = datetime.today()
            self.entry.delete(first=0, last=tk.END)
            self.entry.insert(tk.END, self.startdate.strftime(self.dateformat))

        old_date = datetime.strptime(_val or self.startdate, self.dateformat)
        
        # get the new date and insert into the entry
        new_date = ask_date(
            parent=self.entry,
            startdate=old_date,
            firstweekday=self.firstweekday,
            bootstyle=self.bootstyle
        )
        self.entry.delete(first=0, last=tk.END)
        self.entry.insert(tk.END, new_date.strftime(self.dateformat))
        self.entry.focus_force()
