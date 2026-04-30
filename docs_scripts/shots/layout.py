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


def accordion(parent: tkinter.Widget) -> None:
    """Three sections: General (expanded), Advanced, About (both collapsed)."""
    acc = ttk.Accordion(parent, width=360)
    acc.pack()

    general = acc.add(title="General", expanded=True)
    general_content = general.add()
    ttk.CheckButton(general_content, text="Enable feature").pack(anchor="w", padx=8, pady=4)
    ttk.CheckButton(general_content, text="Show notifications").pack(anchor="w", padx=8, pady=4)

    advanced = acc.add(title="Advanced", expanded=False)
    ttk.Label(advanced.add(), text="Advanced options").pack()

    about = acc.add(title="About", expanded=False)
    ttk.Label(about.add(), text="Version 1.0").pack()


def expander(parent: tkinter.Widget) -> None:
    """Two Expanders: one collapsed, one expanded with checkboxes inside."""
    column = ttk.Frame(parent)
    column.pack()

    collapsed = ttk.Expander(column, title="Display", expanded=False, width=320)
    collapsed.pack(fill="x", pady=(0, 8))
    inner_a = collapsed.add()
    ttk.CheckButton(inner_a, text="Dark mode").pack(anchor="w", padx=8, pady=2)

    expanded = ttk.Expander(column, title="Settings", expanded=True, width=320)
    expanded.pack(fill="x")
    inner_b = expanded.add()
    ttk.CheckButton(inner_b, text="Enable notifications").pack(anchor="w", padx=8, pady=2)
    ttk.CheckButton(inner_b, text="Auto-save").pack(anchor="w", padx=8, pady=2)
    ttk.CheckButton(inner_b, text="Send diagnostics").pack(anchor="w", padx=8, pady=2)


def panedwindow(parent: tkinter.Widget) -> None:
    """Horizontal split: narrow sidebar on the left, content on the right."""
    box = ttk.Frame(parent, width=480, height=200)
    box.pack_propagate(False)
    box.pack()
    pw = ttk.PanedWindow(box, orient="horizontal")
    pw.pack(fill="both", expand=True)
    sidebar = ttk.Frame(pw, padding=12, width=140)
    content = ttk.Frame(pw, padding=12)
    pw.add(sidebar, weight=0)
    pw.add(content, weight=1)
    ttk.Label(sidebar, text="Sidebar", font="heading[14]").pack(anchor="w")
    for item in ["Inbox", "Sent", "Drafts", "Archive"]:
        ttk.Label(sidebar, text=item).pack(anchor="w", pady=2)
    ttk.Label(content, text="Content", font="heading[14]").pack(anchor="w")
    ttk.Label(content, text="Select an item from the sidebar to view it here.").pack(anchor="w", pady=(8, 0))


def scrollbar(parent: tkinter.Widget) -> None:
    """A Text widget framed by vertical + horizontal Scrollbars."""
    box = ttk.Frame(parent, width=420, height=180)
    box.pack_propagate(False)
    box.pack()
    text = ttk.Text(box, wrap="none", height=8, width=40)
    text.grid(row=0, column=0, sticky="nsew")
    ys = ttk.Scrollbar(box, orient="vertical", command=text.yview)
    ys.grid(row=0, column=1, sticky="ns")
    xs = ttk.Scrollbar(box, orient="horizontal", command=text.xview)
    xs.grid(row=1, column=0, sticky="ew")
    text.configure(xscrollcommand=xs.set, yscrollcommand=ys.set)
    box.rowconfigure(0, weight=1)
    box.columnconfigure(0, weight=1)
    # Insert content wide enough to make the horizontal scrollbar useful and
    # tall enough to make the vertical scrollbar useful.
    text.insert("1.0", "\n".join(f"Row {i:02d} — quick brown fox jumps over the lazy dog" for i in range(1, 24)))


def scrollview(parent: tkinter.Widget) -> None:
    """ScrollView listing a long stack of label rows."""
    box = ttk.Frame(parent, width=320, height=200)
    box.pack_propagate(False)
    box.pack()
    sv = ttk.ScrollView(box)
    sv.pack(fill="both", expand=True)
    content = sv.add()
    for i in range(1, 21):
        ttk.Label(content, text=f"Item {i:02d}").pack(anchor="w", padx=12, pady=3)


def card(parent: tkinter.Widget) -> None:
    """A Card with a title, body line, and a primary action button."""
    box = ttk.Card(parent, padding=20)
    box.pack()
    ttk.Label(box, text="Project settings", font="heading[14]").pack(anchor="w")
    ttk.Label(
        box,
        text="Configure how this project builds and deploys.",
        bootstyle="secondary",
        width=36,
    ).pack(anchor="w", pady=(4, 12))
    ttk.Button(box, text="Open settings").pack(anchor="w")


def gridframe(parent: tkinter.Widget) -> None:
    """3-column GridFrame auto-placing six buttons across two rows."""
    grid = ttk.GridFrame(parent, columns=3, gap=8, padding=12, sticky_items="ew")
    grid.pack()
    for label in ["One", "Two", "Three", "Four", "Five", "Six"]:
        ttk.Button(grid, text=label).grid()


def packframe(parent: tkinter.Widget) -> None:
    """Vertical PackFrame stacking three full-width buttons with a gap."""
    stack = ttk.PackFrame(
        parent,
        direction="vertical",
        gap=8,
        padding=12,
        fill_items="x",
    )
    stack.pack()
    ttk.Button(stack, text="Save", width=20).pack()
    ttk.Button(stack, text="Discard", bootstyle="secondary").pack()
    ttk.Button(stack, text="Cancel", bootstyle="ghost").pack()
