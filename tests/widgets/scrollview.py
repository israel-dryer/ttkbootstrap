"""
Demo and test script for the ScrollView widget.

This script demonstrates various features and configurations of the ScrollView widget:
- Different scrollbar visibility modes (always, never, hover, scroll)
- Different scroll directions (vertical, horizontal, both)
- Dynamic content updates
- Mouse wheel scrolling on all child widgets
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_demo_content(parent, rows=30, cols=3):
    """Create sample content for the scrollview."""
    ttk.Label(
        parent,
        text="Scroll with mouse wheel anywhere!",
        font=('Arial', 11, 'bold'),
        bootstyle='info'
    ).grid(row=0, column=0, columnspan=cols, pady=10, sticky='w')

    for i in range(rows):
        ttk.Label(parent, text=f"Row {i + 1}:").grid(
            row=i + 1, column=0, sticky='w', padx=5, pady=2
        )

        entry = ttk.Entry(parent, width=20)
        entry.insert(0, f"Entry {i + 1}")
        entry.grid(row=i + 1, column=1, padx=5, pady=2)

        ttk.Button(parent, text=f"Button {i + 1}").grid(
            row=i + 1, column=2, padx=5, pady=2
        )


def create_wide_content(parent, rows=20):
    """Create wide content for horizontal scrolling demo."""
    for i in range(rows):
        frame = ttk.Frame(parent)
        frame.pack(fill=X, pady=2)

        for j in range(10):
            ttk.Button(
                frame,
                text=f"Button {i + 1}-{j + 1}",
                width=15
            ).pack(side=LEFT, padx=2)


def demo_always_show():
    """Demo 1: Always show scrollbars (both directions)."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Always Show")

    scroll = ttk.ScrollView(frame, scroll_direction='both', scrollbar_visibility='always', scrollbar_style='rounded')
    scroll.pack(fill=BOTH, expand=True, padx=5, pady=5)

    content = ttk.Frame(scroll.canvas)
    scroll.add(content)

    create_demo_content(content)


def demo_never_show():
    """Demo 2: Never show scrollbars (scroll still works)."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Never Show")

    ttk.Label(
        frame,
        text="Scrollbars hidden, but mouse wheel still works!",
        bootstyle='warning'
    ).pack(pady=5)

    scroll = ttk.ScrollView(frame, scroll_direction='both', scrollbar_visibility='never')
    scroll.pack(fill=BOTH, expand=True, padx=5, pady=5)

    content = ttk.Frame(scroll.canvas)
    scroll.add(content)

    create_demo_content(content)


def demo_on_hover():
    """Demo 3: Show scrollbars on hover."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="On Hover")

    ttk.Label(
        frame,
        text="Hover over the area to see scrollbars & enable scrolling",
        bootstyle='info'
    ).pack(pady=5)

    scroll = ttk.ScrollView(frame, scroll_direction='both', scrollbar_visibility='hover')
    scroll.pack(fill=BOTH, expand=True, padx=5, pady=5)

    content = ttk.Frame(scroll.canvas)
    scroll.add(content)

    create_demo_content(content)


def demo_on_scroll():
    """Demo 4: Show scrollbars when scrolling, then auto-hide."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="On Scroll")

    ttk.Label(
        frame,
        text="Scrollbars appear when scrolling, then auto-hide after 1.5s",
        bootstyle='success'
    ).pack(pady=5)

    scroll = ttk.ScrollView(
        frame,
        scroll_direction='both',
        scrollbar_visibility='scroll',
        autohide_delay=1500
    )
    scroll.pack(fill=BOTH, expand=True, padx=5, pady=5)

    content = ttk.Frame(scroll.canvas)
    scroll.add(content)

    create_demo_content(content)


def demo_vertical_only():
    """Demo 5: Vertical scrolling only."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Vertical Only")

    scroll = ttk.ScrollView(frame, scroll_direction='vertical', scrollbar_visibility='always')
    scroll.pack(fill=BOTH, expand=True, padx=5, pady=5)

    content = ttk.Frame(scroll.canvas)
    scroll.add(content)

    create_demo_content(content, rows=40)


def demo_horizontal_only():
    """Demo 6: Horizontal scrolling only."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Horizontal Only")

    ttk.Label(
        frame,
        text="Use Shift+MouseWheel for horizontal scrolling",
        bootstyle='info'
    ).pack(pady=5)

    scroll = ttk.ScrollView(frame, scroll_direction='horizontal', scrollbar_visibility='always')
    scroll.pack(fill=BOTH, expand=True, padx=5, pady=5)

    content = ttk.Frame(scroll.canvas)
    scroll.add(content)

    create_wide_content(content)


def demo_dynamic_content():
    """Demo 7: Dynamic content addition and configuration."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Dynamic Content")

    # Control panel
    control_frame = ttk.Frame(frame)
    control_frame.pack(fill=X, padx=5, pady=5)

    ttk.Label(control_frame, text="Add widgets dynamically:").pack(side=LEFT, padx=5)

    scroll = ttk.ScrollView(frame, scroll_direction='both', scrollbar_visibility='always')
    scroll.pack(fill=BOTH, expand=True, padx=5, pady=5)

    content = ttk.Frame(scroll.canvas)
    scroll.add(content)

    # Initial content
    ttk.Label(
        content,
        text="Click 'Add Row' to add more content",
        font=('Arial', 11, 'bold')
    ).pack(pady=10)

    counter = {'value': 0}

    def add_row():
        """Add a new row of widgets."""
        counter['value'] += 1
        row_frame = ttk.Frame(content)
        row_frame.pack(fill=X, pady=2, padx=5)

        ttk.Label(row_frame, text=f"Row {counter['value']}:").pack(side=LEFT, padx=5)

        entry = ttk.Entry(row_frame, width=20)
        entry.insert(0, f"Dynamic Entry {counter['value']}")
        entry.pack(side=LEFT, padx=5)

        ttk.Button(row_frame, text=f"Button {counter['value']}").pack(side=LEFT, padx=5)

        # Refresh bindings to ensure new widgets can scroll
        scroll.refresh_bindings()

    def clear_content():
        """Clear all dynamic content."""
        for widget in content.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()
        counter['value'] = 0

    ttk.Button(control_frame, text="Add Row", command=add_row, bootstyle='success').pack(
        side=LEFT, padx=2
    )
    ttk.Button(control_frame, text="Clear", command=clear_content, bootstyle='danger').pack(
        side=LEFT, padx=2
    )

    # Configuration controls
    config_frame = ttk.Frame(frame)
    config_frame.pack(fill=X, padx=5, pady=5)

    ttk.Label(config_frame, text="Scrollbar Mode:").pack(side=LEFT, padx=5)

    mode_var = ttk.StringVar(value='always')

    def change_mode():
        scroll.configure(scrollbar_visibility=mode_var.get())

    modes = [
        ('Always', 'always'),
        ('Never', 'never'),
        ('Hover', 'hover'),
        ('Scroll', 'scroll')
    ]

    for text, value in modes:
        ttk.RadioButton(
            config_frame,
            text=text,
            value=value,
            variable=mode_var,
            command=change_mode
        ).pack(side=LEFT, padx=2)


def demo_nested_frames():
    """Demo 8: Complex nested widget structure."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Nested Widgets")

    scroll = ttk.ScrollView(frame, scroll_direction='both', scrollbar_visibility='always')
    scroll.pack(fill=BOTH, expand=True, padx=5, pady=5)

    content = ttk.Frame(scroll.canvas)
    scroll.add(content)

    ttk.Label(
        content,
        text="Complex nested widget hierarchy - scroll anywhere!",
        font=('Arial', 11, 'bold'),
        bootstyle='primary'
    ).pack(pady=10)

    for i in range(10):
        # Create a labelframe for each section
        lf = ttk.LabelFrame(content, text=f"Section {i + 1}")
        lf.pack(fill=X, padx=10, pady=5)

        # Add nested frames with various widgets
        for j in range(3):
            nested_frame = ttk.Frame(lf)
            nested_frame.pack(fill=X, padx=5, pady=2)

            ttk.Label(nested_frame, text=f"Item {j + 1}:").pack(side=LEFT, padx=5)

            ttk.Entry(nested_frame, width=15).pack(side=LEFT, padx=2)

            ttk.CheckButton(nested_frame, text="Option").pack(side=LEFT, padx=2)

            ttk.Button(nested_frame, text="Action", width=10).pack(side=LEFT, padx=2)


if __name__ == '__main__':
    root = ttk.Window(
        title="ScrollView Widget Demo",
        theme="darkly"
    )

    # Header
    header = ttk.Frame(root, bootstyle='dark')
    header.pack(fill=X, padx=10, pady=10)

    ttk.Label(
        header,
        text="ScrollView Widget Demo",
        font=('Arial', 16, 'bold'),
        bootstyle='dark'
    ).pack(side=LEFT)

    ttk.Label(
        header,
        text="Hover over any widget and scroll with your mouse wheel!",
        font=('Arial', 10),
        bootstyle='secondary'
    ).pack(side=LEFT, padx=20)

    # Create notebook for different demos
    notebook = ttk.Notebook(root)
    notebook.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

    # Add all demo tabs
    demo_always_show()
    demo_never_show()
    demo_on_hover()
    demo_on_scroll()
    demo_vertical_only()
    demo_horizontal_only()
    demo_dynamic_content()
    demo_nested_frames()

    root.mainloop()
