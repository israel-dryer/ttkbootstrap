"""
    Author: Israel Dryer
    Modified: 2021-11-10
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.style import utility
utility.enable_high_dpi_awareness()

class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Simple data entry form')
        self.style = ttk.Style('superhero')
        self.form = EntryForm(self)
        self.form.pack(fill='both', expand='yes')


class EntryForm(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=(20, 10))
        self.columnconfigure(2, weight=1)

        # form variables
        self.name = tk.StringVar(value='', name='name')
        self.address = tk.StringVar(value='', name='address')
        self.phone = tk.StringVar(value='', name='phone')

        # form headers
        ttk.Label(
            master=self, 
            text='Please enter your contact information', 
            width=60
        ).grid(columnspan=3, pady=10)

        # create label/entry rows
        for i, label in enumerate(['name', 'address', 'phone']):
            ttk.Label(
                master=self, 
                text=label.title()
            ).grid(row=i + 1, column=0, sticky='ew', pady=10, padx=(0, 10))
            
            ttk.Entry(
                master=self, 
                textvariable=label
            ).grid(row=i + 1, column=1, columnspan=2, sticky=tk.EW)

        # submit button
        self.submit = ttk.Button(
            master=self, 
            text='Submit', 
            bootstyle='success', 
            command=self.print_form_data
        ).grid(
            row=4, 
            column=0, 
            sticky=tk.EW, 
            pady=10, 
            padx=(0, 10)
        )

        # cancel button
        self.cancel = ttk.Button(
            master=self, 
            text='Cancel', 
            bootstyle='danger', 
            command=self.quit
        ).grid(row=4, column=1, sticky=tk.EW)

    def print_form_data(self):
        print(self.name.get(), self.address.get(), self.phone.get())


if __name__ == '__main__':
    Application().mainloop()
