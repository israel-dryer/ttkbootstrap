"""Shot factories for `docs/widgets/inputs/*.md` widgets that don't yet
have their own factory module (Scale, ScrolledText)."""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def scale(parent: tkinter.Widget) -> None:
    """Horizontal scale + a value label that mirrors its current value."""
    column = ttk.Frame(parent, padding=8)
    column.pack()

    header = ttk.Frame(column, width=320)
    header.pack(fill="x")
    ttk.Label(header, text="Volume").pack(side="left")
    ttk.Label(header, text="65", bootstyle="secondary").pack(side="right")

    s = ttk.Scale(column, from_=0, to=100, value=65, length=320)
    s.pack(pady=(8, 0))


def labeledscale(parent: tkinter.Widget) -> None:
    """LabeledScale at value 65.

    Note: the initial value label position appears off-center for the
    rendered thumb; tracked as a widget-side bug to fix separately.
    """
    column = ttk.Frame(parent, padding=8)
    column.pack()
    ttk.LabeledScale(column, value=65, minvalue=0, maxvalue=100, width=360).pack()


def passwordentry(parent: tkinter.Widget) -> None:
    """PasswordEntry with masked value and helper message."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    pwd = ttk.PasswordEntry(
        column,
        label="Password",
        required=True,
        message="Must be at least 8 characters",
        show_message=True,
        width=28,
    )
    pwd.insert(0, "hunter2hunter2")
    pwd.pack()


def pathentry(parent: tkinter.Widget) -> None:
    """PathEntry showing a typical file path."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    path = ttk.PathEntry(
        column,
        label="Input file",
        message="Select a CSV file to import",
        show_message=True,
        width=36,
    )
    path.insert(0, "~/Documents/quarterly-report.csv")
    path.pack()


def timeentry(parent: tkinter.Widget) -> None:
    """TimeEntry showing a value."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    t = ttk.TimeEntry(column, label="Start time", value="08:30", width=20)
    t.pack()


def scrolledtext(parent: tkinter.Widget) -> None:
    """ScrolledText with multi-line content and a visible scroll thumb."""
    box = ttk.Frame(parent, width=420, height=160)
    box.pack_propagate(False)
    box.pack()
    st = ttk.ScrolledText(box, scrollbar_visibility="always")
    st.pack(fill="both", expand=True)
    # Insert enough rows to force scrollbar overflow.
    lines = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco.",
        "Duis aute irure dolor in reprehenderit in voluptate.",
        "Excepteur sint occaecat cupidatat non proident.",
        "Sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "Curabitur pretium tincidunt lacus. Nulla gravida orci a odio.",
        "Nullam varius, turpis et commodo pharetra.",
        "Vestibulum ante ipsum primis in faucibus orci luctus.",
        "Mauris venenatis tellus in sem auctor faucibus.",
        "Praesent dapibus neque id cursus faucibus.",
        "Sed posuere consectetur est at lobortis.",
    ]
    st.insert("end", "\n".join(lines * 3) + "\n")
