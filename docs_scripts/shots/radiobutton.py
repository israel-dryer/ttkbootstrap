"""Shot factories for `docs/widgets/selection/radiobutton.md`."""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def states(parent: tkinter.Widget) -> None:
    sig = ttk.Signal(0)
    ttk.RadioButton(parent, signal=sig, text="Selected", value=0).pack(side="left", padx=10)
    ttk.RadioButton(parent, signal=sig, text="Unselected", value=1).pack(side="left", padx=10)
    ttk.RadioButton(parent, signal=sig, text="Disabled", value=3, state="disabled").pack(side="left", padx=10)


def colors(parent: tkinter.Widget) -> None:
    sig = ttk.Signal(0)
    for label, color in [
        ("Primary", "primary"),
        ("Secondary", "secondary"),
        ("Success", "success"),
        ("Info", "info"),
        ("Warning", "warning"),
        ("Danger", "danger"),
    ]:
        kwargs: dict = {"signal": sig, "text": label, "value": 0}
        if color != "primary":
            kwargs["bootstyle"] = color
        ttk.RadioButton(parent, **kwargs).pack(side="left", padx=10)
