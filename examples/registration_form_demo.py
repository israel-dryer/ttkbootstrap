"""Registration form demo using ttkbootstrap Form and SelectBox."""

from datetime import date

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, W
from ttkbootstrap.widgets.composites.form import FieldItem, Form, GroupItem, TabItem, TabsItem


def main():
    app = ttk.Window(title="Registration Form", theme="flatly")

    initial_data = {
        "first_name": "",
        "last_name": "",
        "email": "",
        "password": "",
        "confirm_password": "",
        "country": "United States",
        "state": "",
        "birth_date": date.today(),
        "newsletter": True,
        "timezone": "UTC",
        "two_factor": False,
    }

    items = [
        GroupItem(
            label="Account",
            col_count=2,
            items=[
                FieldItem(key="first_name", label="First Name", editor="textentry"),
                FieldItem(key="last_name", label="Last Name", editor="textentry"),
                FieldItem(key="email", label="Email", editor="textentry"),
                FieldItem(key="birth_date", label="Birth Date", dtype="date"),
                FieldItem(key="password", label="Password", editor="passwordentry"),
                FieldItem(key="confirm_password", label="Confirm Password", editor="passwordentry"),
                FieldItem(key="state", label="State/Region", editor="textentry"),
                FieldItem(
                    key="country",
                    label="Country",
                    editor="selectbox",
                    editor_options={"items": ["United States", "Canada", "Mexico", "United Kingdom", "Germany", "France"]},
                ),
            ],
        ),
        TabsItem(
            tabs=[
                TabItem(
                    label="Preferences",
                    items=[
                        FieldItem(key="newsletter", label="Subscribe to newsletter", dtype="bool", editor="toggle"),
                        FieldItem(
                            key="timezone",
                            label="Time Zone",
                            editor="selectbox",
                            editor_options={
                                "items": ["UTC", "US/Eastern", "US/Central", "US/Mountain", "US/Pacific", "Europe/London"]
                            },
                        ),
                    ],
                ),
                TabItem(
                    label="Security",
                    items=[
                        FieldItem(key="two_factor", label="Enable Two-Factor Auth", dtype="bool", editor="toggle"),
                    ],
                ),
            ]
        ),
    ]

    ttk.Label(app, text="Registration Form").pack(anchor=W, padx=20, pady=(16, 6))
    form = Form(
        app,
        data=initial_data,
        items=items,
        col_count=2,
        min_col_width=280,
        scrollable=False,
        buttons=[
            {"text": "Cancel", "role": "cancel", "result": None},
            {"text": "Register", "role": "primary", "result": "register", "command": lambda x: submit()},
        ],
        on_data_changed=lambda data: print("Changed:", data),
    )
    form.pack(fill=BOTH, expand=True, padx=20, pady=20)

    def submit():
        print("Submitted:", form.data)
        ttk.Toast(
            title="Registration",
            message="Form submitted",
            duration=2000,
            bootstyle="success",
        ).show()

    app.update_idletasks()
    app.minsize(app.winfo_reqwidth(), app.winfo_reqheight())

    app.mainloop()


if __name__ == "__main__":
    main()
