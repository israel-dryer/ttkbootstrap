import tkinter
from tkinter import ttk
from ttkbootstrap import Style


class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Simple data entry form')
        self.style = Style()
        self.form = EntryForm(self)
        self.form.pack(fill='both', expand='yes')


class EntryForm(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=(20, 10))
        self.columnconfigure(2, weight=1)

        # form variables
        self.name = tkinter.StringVar(value='', name='name')
        self.address = tkinter.StringVar(value='', name='address')
        self.phone = tkinter.StringVar(value='', name='phone')

        # form headers
        ttk.Label(self, text='Please enter your contact information', width=60).grid(columnspan=3, pady=10)

        # create label/entry rows
        for i, label in enumerate(['name', 'address', 'phone']):
            ttk.Label(self, text=label.title()).grid(row=i + 1, column=0, sticky='ew', pady=10, padx=(0, 10))
            ttk.Entry(self, textvariable=label).grid(row=i + 1, column=1, columnspan=2, sticky='ew')

        # submit button
        self.submit = ttk.Button(self, text='Submit', style='success.TButton', command=self.print_form_data)
        self.submit.grid(row=4, column=0, sticky='ew', pady=10, padx=(0, 10))

        # cancel button
        self.cancel = ttk.Button(self, text='Cancel', style='danger.TButton', command=self.quit)
        self.cancel.grid(row=4, column=1, sticky='ew')

    def print_form_data(self):
        print(self.name.get(), self.address.get(), self.phone.get())


if __name__ == '__main__':
    Application().mainloop()
