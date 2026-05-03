"""Shot factories for `docs/widgets/application/*.md` widgets.

Covers App and Toplevel. AppShell's screenshot lives in `navigation.py`
because its visual is a Toolbar + SideNav + content composition.

App and Toplevel are window classes: the renderer captures the inner
capture frame, which is exactly what these widgets host. The factories
below build a representative interior.
"""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def app(parent: tkinter.Widget) -> None:
    """Simple "Hello world" composition matching the App quick-start example."""
    box = ttk.Frame(parent, padding=24, width=460, height=220)
    box.pack_propagate(False)
    box.pack()
    ttk.Label(box, text="Hello, world!", font="heading[20]").pack(anchor="w")
    ttk.Label(
        box,
        text="A ttkbootstrap App is a themed Tk window with sensible defaults.",
        bootstyle="secondary",
    ).pack(anchor="w", pady=(4, 16))
    ttk.Button(box, text="Get started", accent="primary").pack(anchor="w")


def toplevel(parent: tkinter.Widget) -> None:
    """Settings-style mini layout representative of a Toplevel's content."""
    box = ttk.Frame(parent, padding=20, width=420, height=260)
    box.pack_propagate(False)
    box.pack()
    ttk.Label(box, text="Settings", font="heading[16]").pack(anchor="w", pady=(0, 12))
    ttk.CheckButton(box, text="Launch on startup", value=True).pack(anchor="w", pady=2)
    ttk.CheckButton(box, text="Send anonymous usage data", value=False).pack(anchor="w", pady=2)
    ttk.CheckButton(box, text="Show notifications", value=True).pack(anchor="w", pady=2)
    row = ttk.Frame(box)
    row.pack(side="bottom", fill="x", pady=(16, 0))
    ttk.Button(row, text="Save", accent="primary").pack(side="right")
    ttk.Button(row, text="Cancel", bootstyle="secondary").pack(side="right", padx=(0, 8))
