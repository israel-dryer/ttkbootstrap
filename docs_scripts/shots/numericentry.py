"""Shot factories for `docs/widgets/inputs/numericentry.md`.

The historical `widgets-numericentry-colors.mp4` is animated; that's
for Phase 6F, not the static manifest here.
"""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def states(parent: tkinter.Widget) -> None:
    ttk.NumericEntry(parent, value=123456, label="Active", show_message=True, width=15).pack(side="left", padx=10)
    ttk.NumericEntry(
        parent,
        value=123456,
        label="Normal",
        required=True,
        message="This field is required",
        show_message=True,
        width=15,
    ).pack(side="left", padx=10)
    ttk.NumericEntry(parent, value=123456, state="readonly", label="Readonly", show_message=True, width=15).pack(side="left", padx=10)
    ttk.NumericEntry(parent, value=123456, state="disabled", label="Disabled", show_message=True, width=15).pack(side="left", padx=10)


def addons(parent: tkinter.Widget) -> None:
    salary = ttk.NumericEntry(parent, label="Salary")
    salary.insert_addon(ttk.Label, position="before", icon="currency-euro")
    salary.pack(side="left", padx=10, anchor="s")

    size = ttk.NumericEntry(parent, label="Size", show_spin_buttons=False)
    size.insert_addon(ttk.Button, position="before", icon="rulers")
    size.insert_addon(ttk.Label, position="after", text="cm", font="label[9]")
    size.pack(side="left", padx=10, anchor="s")


def formats(parent: tkinter.Widget) -> None:
    ttk.NumericEntry(parent, label="Currency", value=1234.56, value_format="currency").pack(side="left", padx=10)
    ttk.NumericEntry(parent, label="Fixed Point", value=15422354, value_format="fixedPoint").pack(side="left", padx=10)
    ttk.NumericEntry(parent, label="Percent", value=0.35, value_format="percent").pack(side="left", padx=10)
