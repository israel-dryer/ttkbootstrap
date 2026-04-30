"""Shot factories for `docs/widgets/data-display/*.md` widgets.

Covers visually-rich read-only widgets: Label, Badge, Progressbar,
FloodGauge, Meter (and TBD ListView, TableView, TreeView).
"""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def label(parent: tkinter.Widget) -> None:
    """Sampler showing a few common Label fonts/accents."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    ttk.Label(column, text="Display heading", font="heading[20]").pack(anchor="w", pady=(0, 4))
    ttk.Label(column, text="Section title", font="heading[14]").pack(anchor="w", pady=(0, 4))
    ttk.Label(column, text="Body text reads at the default size.").pack(anchor="w")
    ttk.Label(column, text="Secondary caption", bootstyle="secondary").pack(anchor="w", pady=(2, 0))


def badge(parent: tkinter.Widget) -> None:
    """Row of Badge accents covering the standard palette."""
    row = ttk.Frame(parent, padding=8)
    row.pack()
    for accent in ["primary", "secondary", "success", "info", "warning", "danger"]:
        ttk.Badge(row, text=accent.title(), accent=accent).pack(side="left", padx=4)


def progressbar(parent: tkinter.Widget) -> None:
    """Determinate progress bars at three different values."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    for label_text, value, accent in [
        ("Downloading", 25, "primary"),
        ("Processing", 60, "info"),
        ("Uploading", 90, "success"),
    ]:
        row = ttk.Frame(column, width=320)
        row.pack(fill="x", pady=4)
        ttk.Label(row, text=label_text).pack(side="left")
        ttk.Label(row, text=f"{value}%", bootstyle="secondary").pack(side="right")
        pb = ttk.Progressbar(column, maximum=100, value=value, bootstyle=accent, length=320)
        pb.pack(pady=(2, 6))


def floodgauge(parent: tkinter.Widget) -> None:
    """Two FloodGauges showing different fill amounts."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    fg1 = ttk.FloodGauge(column, value=35, mask="Disk: {}%", length=360)
    fg1.pack(pady=(0, 6))
    fg2 = ttk.FloodGauge(column, value=78, mask="Memory: {}%", bootstyle="warning", length=360)
    fg2.pack()


def meter(parent: tkinter.Widget) -> None:
    """Two Meters showing different metrics (battery, downloads)."""
    row = ttk.Frame(parent, padding=8)
    row.pack()
    ttk.Meter(row, amountused=68, amounttotal=100, subtext="Battery", textright="%").pack(side="left", padx=8)
    ttk.Meter(row, amountused=42, amounttotal=100, subtext="Downloads", bootstyle="info").pack(side="left", padx=8)
