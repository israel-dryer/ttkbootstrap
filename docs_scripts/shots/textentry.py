"""Shot factories for `docs/widgets/inputs/textentry.md`."""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def states(parent: tkinter.Widget) -> None:
    ttk.TextEntry(parent, value="Active", label="Label", show_message=True).pack(side="left", padx=10)
    ttk.TextEntry(
        parent,
        value="Normal",
        label="Label",
        required=True,
        message="This field is required",
        show_message=True,
    ).pack(side="left", padx=10)
    ttk.TextEntry(parent, value="Readonly", state="readonly", label="Label", show_message=True).pack(side="left", padx=10)
    ttk.TextEntry(parent, value="Disabled", state="disabled", label="Label", show_message=True).pack(side="left", padx=10)


def addons(parent: tkinter.Widget) -> None:
    email = ttk.TextEntry(parent, label="Email")
    email.insert_addon(ttk.Label, position="before", icon="envelope")
    email.pack(side="left", padx=10, anchor="s")

    def _noop() -> None:
        pass

    search = ttk.TextEntry(parent)
    search.insert_addon(ttk.Button, position="after", icon="search", command=_noop)
    search.pack(side="left", padx=10, anchor="s")


def localization(parent: tkinter.Widget) -> None:
    ttk.TextEntry(parent, label="Currency", value=1234.56, value_format="currency").pack(side="left", padx=10)
    ttk.TextEntry(parent, label="Short Date", value="March 14, 1981", value_format="shortDate").pack(side="left", padx=10)
    ttk.TextEntry(parent, label="Fixed Point", value=15422354, value_format="fixedPoint").pack(side="left", padx=10)
