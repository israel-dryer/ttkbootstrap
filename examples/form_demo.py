"""Demonstration of the ttkbootstrap Form widget.

Shows both inferred field generation from data and an explicit form layout
using groups and tabs.
"""

from datetime import date

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.form import (
    FieldItem,
    Form,
    GroupItem,
    TabItem,
    TabsItem,
)


def main():
    app = ttk.Window(title="Form Demo", themename="flatly")
    app.geometry("900x520")

    # --- inferred form -------------------------------------------------
    inferred_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "age": 34,
        "email": "jane@example.com",
        "salary": 120000.50,
        "active": True,
        "start_date": date.today(),
    }

    ttk.Label(app, text="Inferred Form").pack(anchor=W, padx=20, pady=(15, 4))
    inferred_form = Form(
        app,
        data=inferred_data,
        col_count=2,
        min_col_width=220,
        buttons=[
            "Cancel",
            {"text": "Submit", "role": "primary", "result": "submitted"},
        ],
        on_data_changed=lambda data: print("Inferred changed:", data),
        show_scrollbar="never",
    )
    inferred_form.pack(fill=X, padx=20)

    # --- explicit layout ----------------------------------------------
    ttk.Label(app, text="Explicit Form Layout").pack(anchor=W, padx=20, pady=(16, 4))

    explicit_items = [
        GroupItem(
            label="Profile",
            col_count=2,
            items=[
                FieldItem(key="username", label="Username"),
                FieldItem(key="password", label="Password", editor="passwordentry"),
                FieldItem(key="role", label="Role", editor="selectbox", editor_options={"items": ["Admin", "User", "Viewer"]}),
                FieldItem(key="join_date", label="Join Date", dtype="date"),
            ],
        ),
        TabsItem(
            label=None,
            tabs=[
                TabItem(
                    label="Preferences",
                    items=[
                        FieldItem(key="newsletter", label="Newsletter", dtype=bool, editor="toggle"),
                        FieldItem(key="timezone", label="Time Zone", editor="selectbox", editor_options={"items": ["UTC", "US/Eastern", "US/Central", "US/Pacific"]}),
                    ],
                ),
                TabItem(
                    label="Limits",
                    items=[
                        FieldItem(key="daily_limit", label="Daily Limit", dtype="float"),
                        FieldItem(key="quota", label="Quota", dtype="int"),
                    ],
                ),
            ],
        ),
    ]

    explicit_form = Form(
        app,
        data={
            "username": "jdoe",
            "role": "Admin",
            "newsletter": True,
            "timezone": "UTC",
            "daily_limit": 500.0,
            "quota": 25,
        },
        items=explicit_items,
        col_count=2,
        min_col_width=250,
        buttons=[
            {"text": "Cancel", "role": "cancel", "result": None},
            {"text": "Save", "role": "primary", "result": "saved"},
        ],
        on_data_changed=lambda data: print("Explicit changed:", data),
        show_scrollbar="on-scroll",
        height=260,
    )
    explicit_form.pack(fill=BOTH, expand=True, padx=20, pady=(0, 15))

    def show_results():
        print("Inferred result:", inferred_form.get_data())
        print("Explicit result:", explicit_form.get_data())

    ttk.Button(app, text="Print Results", command=show_results, bootstyle="secondary").pack(pady=(0, 15))

    app.mainloop()


if __name__ == "__main__":
    main()
