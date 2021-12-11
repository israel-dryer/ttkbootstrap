"""
    Author: Israel Dryer
    Modified: 2021-12-11
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class DataEntryForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)

        self.name = ttk.StringVar(value="")
        self.address = ttk.StringVar(value="")
        self.phone = ttk.StringVar(value="")

        # add header label
        ttk.Label(
            master=self, text="Please enter your contact information", width=50
        ).pack(fill=X, pady=10)

        # add form entries
        self.create_form_entry("name", self.name)
        self.create_form_entry("address", self.address)
        self.create_form_entry("phone", self.phone)
        self.create_buttonbox()

    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        ttk.Label(master=container, text=label.title(), width=10).pack(
            side=LEFT, padx=5
        )
        ttk.Entry(master=container, textvariable=variable).pack(
            side=LEFT, padx=5, fill=X, expand=YES
        )

    def create_buttonbox(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))
        btn = ttk.Button(
            master=container,
            text="Submit",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        btn.pack(side=RIGHT, padx=5)
        btn.focus_set()

        ttk.Button(
            master=container,
            text="Cancel",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=6,
        ).pack(side=RIGHT, padx=5)

    def on_submit(self):
        """Print the contents to console and return the values."""
        print("Name:", self.name.get())
        print("Address:", self.address.get())
        print("Phone:", self.phone.get())
        return self.name.get(), self.address.get(), self.phone.get()

    def on_cancel(self):
        """Cancel and close the application."""
        self.quit()


if __name__ == "__main__":

    app = ttk.Window(
        title="Simple data entry file", 
        themename="superhero", 
        resizable=(False, False),
    )
    DataEntryForm(app)
    app.mainloop()
