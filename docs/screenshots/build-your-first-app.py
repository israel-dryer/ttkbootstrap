"""Screenshot scenes for docs/user-guide/getting-started/build-your-first-app.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class ContactBook(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self.pack(fill=BOTH, expand=YES)

        self.name = ttk.StringVar()
        self.email = ttk.StringVar()
        self.category = ttk.StringVar(value="Friend")

        self._build_form()
        self._build_table()
        self._build_status()

    def _build_form(self):
        form = ttk.Labelframe(self, text="New contact", padding=12)
        form.pack(fill=X)
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky=W, padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.name).grid(row=0, column=1, sticky=EW, pady=4)

        ttk.Label(form, text="Email").grid(row=1, column=0, sticky=W, padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.email).grid(row=1, column=1, sticky=EW, pady=4)

        ttk.Label(form, text="Category").grid(row=2, column=0, sticky=W, padx=(0, 8), pady=4)
        ttk.Combobox(form, textvariable=self.category,
                     values=["Friend", "Family", "Work"], state="readonly").grid(
            row=2, column=1, sticky=EW, pady=4)

        ttk.Button(form, text="Add contact", bootstyle="success").grid(
            row=3, column=1, sticky=E, pady=(8, 0))

    def _build_table(self):
        self.table = ttk.Tableview(
            self,
            coldata=["Name", "Email", "Category"],
            rowdata=[
                ["Ada Lovelace", "ada@example.com", "Work"],
                ["Grace Hopper", "grace@example.com", "Work"],
                ["Alan Turing", "alan@example.com", "Friend"],
            ],
            searchable=True,
            bootstyle="primary",
            height=6,
        )
        self.table.pack(fill=BOTH, expand=YES, pady=(16, 8))

    def _build_status(self):
        self.status = ttk.Label(self, text="3 contact(s).", bootstyle="secondary")
        self.status.pack(fill=X)


def hero():
    app = ttk.App(title="Contact Book", size=(560, 520))
    ContactBook(app)
    app._capture_full_window = True  # it's a finished app — show the window chrome
    app.mainloop()


def form():
    # The "New contact" labelframe alone (Step 2 state — before the button).
    app = ttk.App(title="New contact", size=(360, 170))
    frm = ttk.Frame(app, padding=16)
    frm.pack(fill=BOTH, expand=YES)
    box = ttk.Labelframe(frm, text="New contact", padding=12)
    box.pack(fill=X)
    box.columnconfigure(1, weight=1)
    ttk.Label(box, text="Name").grid(row=0, column=0, sticky=W, padx=(0, 8), pady=4)
    ttk.Entry(box).grid(row=0, column=1, sticky=EW, pady=4)
    ttk.Label(box, text="Email").grid(row=1, column=0, sticky=W, padx=(0, 8), pady=4)
    ttk.Entry(box).grid(row=1, column=1, sticky=EW, pady=4)
    ttk.Label(box, text="Category").grid(row=2, column=0, sticky=W, padx=(0, 8), pady=4)
    ttk.Combobox(box, values=["Friend", "Family", "Work"], state="readonly").grid(
        row=2, column=1, sticky=EW, pady=4)
    app.mainloop()


def _email(app, value, valid):
    frm = ttk.Frame(app, padding=16)
    frm.pack(fill=BOTH, expand=YES)
    entry = ttk.Entry(frm, width=26)
    entry.insert(0, value)
    entry.pack()
    ttk.Validation.regex(entry, r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def flag():
        entry.validate()  # run the rule once → sets the invalid state on failure

    app.after(300, flag)
    app.mainloop()


def email_invalid():
    _email(ttk.App(title="Email"), "ada@work", False)


def email_valid():
    _email(ttk.App(title="Email"), "ada@example.com", True)


SCENES = {
    "hero": hero,
    "form": form,
    "email-invalid": email_invalid,
    "email-valid": email_valid,
}
