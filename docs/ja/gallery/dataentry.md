# Simple Data Entry
This simple data entry form accepts user input and then prints it to the screen 
when submitted. 

![file search image example](../assets/gallery/simple_data_entry_light.png)

![file search image example](../assets/gallery/simple_data_entry_dark.png)

## Style Summary
The two examples above use the themes **litera** and **superhero**.

| Item          | Class     | Bootstyle |
| ---           | ---       | ---|
| Submit Button | `Button`  | success |
| Cancel Button | `Button`  | danger |
| Inputs        | `Entry`   | default |

## Example Code
[Run this code live](https://replit.com/@israel-dryer/data-entry#main.py) on repl.it

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class DataEntryForm(ttk.Frame):
    
    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)

        # form variables
        self.name = ttk.StringVar(value="")
        self.address = ttk.StringVar(value="")
        self.phone = ttk.StringVar(value="")

        # form header
        hdr_txt = "Please enter your contact information" 
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=10)

        # form entries
        self.create_form_entry("name", self.name)
        self.create_form_entry("address", self.address)
        self.create_form_entry("phone", self.phone)
        self.create_buttonbox()

    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_buttonbox(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="Submit",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        cnl_btn = ttk.Button(
            master=container,
            text="Cancel",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=6,
        )
        cnl_btn.pack(side=RIGHT, padx=5)

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

    app = ttk.Window("Data Entry", "superhero", resizable=(False, False))
    DataEntryForm(app)
    app.mainloop()
```