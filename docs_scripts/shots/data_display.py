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


def listview(parent: tkinter.Widget) -> None:
    """ListView with five rows showing icon + title + caption."""
    from ttkbootstrap.widgets.composites.list.listview import ListView

    items = [
        {"id": 1, "icon": "file-earmark-text", "title": "Quarterly report", "caption": "Updated 2 minutes ago"},
        {"id": 2, "icon": "file-earmark-image", "title": "Cover photo", "caption": "1.2 MB · PNG"},
        {"id": 3, "icon": "file-earmark-music", "title": "Theme song", "caption": "3:24 · MP3"},
        {"id": 4, "icon": "file-earmark-zip", "title": "Project archive", "caption": "184 MB"},
        {"id": 5, "icon": "file-earmark-pdf", "title": "Contract", "caption": "Signed"},
    ]
    box = ttk.Frame(parent, padding=8, width=460, height=280)
    box.pack_propagate(False)
    box.pack()
    lv = ListView(box, items=items, selection_mode="single", striped=True)
    lv.pack(fill="both", expand=True)


def tableview(parent: tkinter.Widget) -> None:
    """TableView with four columns and a handful of rows."""
    box = ttk.Frame(parent, padding=8, width=520, height=260)
    box.pack_propagate(False)
    box.pack()
    columns = [
        {"text": "Name", "key": "name", "width": 140},
        {"text": "Owner", "key": "owner", "width": 120},
        {"text": "Status", "key": "status", "width": 100},
        {"text": "Updated", "key": "updated", "width": 120},
    ]
    rows = [
        {"name": "Onboarding", "owner": "A. Chen", "status": "Active", "updated": "2026-04-25"},
        {"name": "Reporting", "owner": "L. Park", "status": "Active", "updated": "2026-04-24"},
        {"name": "Migrations", "owner": "J. Diaz", "status": "Paused", "updated": "2026-04-19"},
        {"name": "Notifications", "owner": "M. Patel", "status": "Active", "updated": "2026-04-12"},
        {"name": "Telemetry", "owner": "S. Khan", "status": "Done", "updated": "2026-04-04"},
    ]
    tv = ttk.TableView(
        box,
        columns=columns,
        rows=rows,
        striped=True,
        enable_search=False,
        enable_filtering=False,
        show_table_status=False,
    )
    tv.pack(fill="both", expand=True)


def treeview(parent: tkinter.Widget) -> None:
    """TreeView showing a small hierarchical project structure."""
    box = ttk.Frame(parent, padding=8, width=440, height=320)
    box.pack_propagate(False)
    box.pack()
    tv = ttk.TreeView(box, columns=("size",), show="tree headings", height=10)
    tv.heading("#0", text="Name")
    tv.heading("size", text="Size")
    tv.column("#0", width=240)
    tv.column("size", width=100, anchor="e")
    src = tv.insert("", "end", text="src", open=True)
    tv.insert(src, "end", text="app.py", values=("4.2 KB",))
    tv.insert(src, "end", text="utils.py", values=("1.8 KB",))
    widgets = tv.insert(src, "end", text="widgets", open=True)
    tv.insert(widgets, "end", text="button.py", values=("3.1 KB",))
    tv.insert(widgets, "end", text="entry.py", values=("2.5 KB",))
    tests = tv.insert("", "end", text="tests", open=True)
    tv.insert(tests, "end", text="test_app.py", values=("0.9 KB",))
    tv.insert("", "end", text="README.md", values=("2.0 KB",))
    tv.pack(fill="both", expand=True)
