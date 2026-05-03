"""Shot factories for `docs/widgets/inputs/dateentry.md`.

Note: the historical `widgets-dateentry-popup.png` shows the calendar
popup open. That requires programmatically opening the dropdown after
the window is mapped; not yet implemented here.
"""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def states(parent: tkinter.Widget) -> None:
    ttk.DateEntry(parent, value="2030-12-31", label="Active", show_message=True, width=16).pack(side="left", padx=10)
    ttk.DateEntry(
        parent,
        value="2030-12-31",
        label="Normal",
        required=True,
        message="This field is required",
        show_message=True,
        width=16,
    ).pack(side="left", padx=10)
    ttk.DateEntry(parent, value="2030-12-31", state="readonly", label="Readonly", show_message=True, width=16).pack(side="left", padx=10)
    ttk.DateEntry(parent, value="2030-12-31", state="disabled", label="Disabled", show_message=True, width=16).pack(side="left", padx=10)


def addons(parent: tkinter.Widget) -> None:
    birthday = ttk.DateEntry(parent, label="Birthday")
    birthday.insert_addon(ttk.Label, position="before", icon="cake-fill")
    birthday.pack(side="left", padx=10, anchor="s")


def formats(parent: tkinter.Widget) -> None:
    ttk.DateEntry(parent, label="Short Date", value="March 14, 1981", value_format="shortDate").pack(side="left", padx=10)
    ttk.DateEntry(parent, label="Long Date", value="1981-03-14", value_format="longDate").pack(side="left", padx=10)
