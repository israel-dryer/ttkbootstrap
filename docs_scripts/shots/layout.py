"""Shot factories for layout widget pages.

Covers static layout primitives: Frame, LabelFrame, Separator, Sizegrip,
and (TBD) PanedWindow, ScrollView, Scrollbar, Accordion, Expander.
"""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def frame(parent: tkinter.Widget) -> None:
    """A padded Frame containing a small form (label + entry + button)."""
    section = ttk.Frame(parent, padding=12, show_border=True)
    section.pack()
    ttk.Label(section, text="Email").grid(row=0, column=0, sticky="w", padx=(0, 8))
    ttk.Entry(section, width=24).grid(row=0, column=1, padx=(0, 8))
    ttk.Button(section, text="Subscribe").grid(row=0, column=2)


def labelframe(parent: tkinter.Widget) -> None:
    """A LabelFrame titled "Network" containing a few related controls."""
    box = ttk.LabelFrame(parent, text="Network", padding=12)
    box.pack()
    ttk.Label(box, text="Hostname").grid(row=0, column=0, sticky="w", pady=2)
    ttk.Entry(box, width=20).grid(row=0, column=1, padx=8, pady=2)
    ttk.Label(box, text="Port").grid(row=1, column=0, sticky="w", pady=2)
    ttk.Entry(box, width=6).grid(row=1, column=1, sticky="w", padx=8, pady=2)
    ttk.CheckButton(box, text="Use TLS").grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))


def separator(parent: tkinter.Widget) -> None:
    """Horizontal separator between form rows; vertical between two columns."""
    container = ttk.Frame(parent)
    container.pack()

    # Left column: two stacked rows separated by a horizontal Separator.
    left = ttk.Frame(container, padding=8)
    left.pack(side="left", anchor="n")
    ttk.Label(left, text="Account").pack(anchor="w")
    ttk.Entry(left, width=18).pack(anchor="w", pady=(2, 8))
    ttk.Separator(left, orient="horizontal").pack(fill="x", pady=4)
    ttk.Label(left, text="Profile").pack(anchor="w", pady=(8, 0))
    ttk.Entry(left, width=18).pack(anchor="w", pady=(2, 0))

    # Vertical separator between left column and right column.
    ttk.Separator(container, orient="vertical").pack(side="left", fill="y", padx=8)

    # Right column: a stack of buttons.
    right = ttk.Frame(container, padding=8)
    right.pack(side="left", anchor="n")
    ttk.Label(right, text="Actions").pack(anchor="w")
    ttk.Button(right, text="Save").pack(fill="x", pady=(8, 4))
    ttk.Button(right, text="Cancel", bootstyle="secondary").pack(fill="x")


def sizegrip(parent: tkinter.Widget) -> None:
    """A mini "status bar" with text on the left and a Sizegrip on the right."""
    bar = ttk.Frame(parent, padding=(8, 4), show_border=True, width=320, height=28)
    bar.pack_propagate(False)
    bar.pack()
    ttk.Label(bar, text="Ready", bootstyle="secondary").pack(side="left")
    ttk.SizeGrip(bar).pack(side="right")
