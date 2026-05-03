"""Shot factories for `docs/widgets/inputs/spinnerentry.md`."""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def states(parent: tkinter.Widget) -> None:
    ttk.SpinnerEntry(parent, value="Active", label="Label", show_message=True).pack(side="left", padx=10)
    ttk.SpinnerEntry(
        parent,
        value="Normal",
        label="Label",
        required=True,
        message="This field is required",
        show_message=True,
    ).pack(side="left", padx=10)
    ttk.SpinnerEntry(parent, value="Readonly", state="readonly", label="Label", show_message=True).pack(side="left", padx=10)
    ttk.SpinnerEntry(parent, value="Disabled", state="disabled", label="Label", show_message=True).pack(side="left", padx=10)


def addons(parent: tkinter.Widget) -> None:
    salary = ttk.SpinnerEntry(parent, label="Salary")
    salary.insert_addon(ttk.Label, position="before", icon="currency-euro")
    salary.pack(side="left", padx=10, anchor="s")

    size = ttk.SpinnerEntry(parent, label="Size", values=["Small", "Med", "Large"], value="Small")
    size.insert_addon(ttk.Button, position="before", icon="rulers")
    size.pack(side="left", padx=10, anchor="s")


def formats(parent: tkinter.Widget) -> None:
    ttk.SpinnerEntry(parent, label="Currency", value=9.99, increment=0.01, value_format="currency").pack(side="left", padx=10)
    ttk.SpinnerEntry(parent, label="Fixed Point", value=1500, increment=10, value_format="fixedPoint").pack(side="left", padx=10)
    ttk.SpinnerEntry(parent, label="Percent", value=0.25, increment=0.05, value_format="percent").pack(side="left", padx=10)
