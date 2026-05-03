"""Shot factories for additional selection widget pages.

The existing checkbutton/radiobutton modules cover those two; this
module covers Switch, CheckToggle, RadioToggle, OptionMenu, Calendar.
"""

from __future__ import annotations

import datetime
import tkinter
from typing import Callable

import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.calendar import Calendar


def switch(parent: tkinter.Widget) -> None:
    """Two switches: one on, one off."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    ttk.Switch(column, text="Enable dark mode", value=True).pack(anchor="w", pady=4)
    ttk.Switch(column, text="Send notifications", value=False).pack(anchor="w", pady=4)


def checktoggle(parent: tkinter.Widget) -> Callable[[], None]:
    """Toolbar-style toggle row with one selected option."""
    row = ttk.Frame(parent, padding=8)
    row.pack()
    bold = ttk.CheckToggle(row, text="Bold")
    bold.pack(side="left", padx=2)
    italic = ttk.CheckToggle(row, text="Italic")
    italic.pack(side="left", padx=2)
    underline = ttk.CheckToggle(row, text="Underline")
    underline.pack(side="left", padx=2)

    def finalize() -> None:
        # Italic pressed, others unpressed.
        italic.invoke()

    return finalize


def radiotoggle(parent: tkinter.Widget) -> None:
    """Three radio toggles for view mode (Grid selected via signal)."""
    row = ttk.Frame(parent, padding=8)
    row.pack()
    view = ttk.Signal("list")
    ttk.RadioToggle(row, text="Grid", signal=view, value="grid", icon="grid").pack(side="left", padx=2)
    ttk.RadioToggle(row, text="List", signal=view, value="list", icon="list").pack(side="left", padx=2)
    ttk.RadioToggle(row, text="Cards", signal=view, value="cards", icon="card-image").pack(side="left", padx=2)


def optionmenu(parent: tkinter.Widget) -> None:
    """Single OptionMenu showing the current value."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    ttk.Label(column, text="Priority").pack(anchor="w", pady=(0, 4))
    ttk.OptionMenu(column, value="Medium", options=["Low", "Medium", "High"]).pack(anchor="w")


def calendar(parent: tkinter.Widget) -> None:
    """Calendar in range mode (auto-displays two consecutive months) with a
    range selected that spans the boundary."""
    box = ttk.Frame(parent, padding=8)
    box.pack()
    cal = Calendar(
        box,
        selection_mode="range",
        value=datetime.date(2026, 1, 15),
        accent="primary",
    )
    cal.pack()
    cal.set_range(datetime.date(2026, 1, 22), datetime.date(2026, 2, 7))


def radiogroup(parent: tkinter.Widget) -> None:
    """Vertical RadioGroup labeled "Plan" with three options ("Pro" selected)."""
    box = ttk.Frame(parent, padding=8)
    box.pack()
    group = ttk.RadioGroup(box, text="Plan", orient="vertical", value="pro")
    group.add("Basic", value="basic")
    group.add("Pro", value="pro")
    group.add("Enterprise", value="enterprise")
    group.pack()


def togglegroup(parent: tkinter.Widget) -> None:
    """Horizontal single-mode ToggleGroup acting as a view-mode segmented control."""
    box = ttk.Frame(parent, padding=8)
    box.pack()
    group = ttk.ToggleGroup(box, mode="single", value="grid")
    group.add("Grid", value="grid")
    group.add("List", value="list")
    group.add("Cards", value="cards")
    group.pack()
