"""
Demo and test script for the ScrolledText widget.

This script demonstrates various features and configurations of the ScrolledText widget:
- Different scrollbar visibility modes (always, never, on-hover, on-scroll)
- Different scroll directions (vertical, horizontal, both)
- Text insertion and manipulation
- Custom scrollbar styling
- Backwards compatibility with legacy API
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolledtext import ScrolledText


SAMPLE_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
cupidatat non proident, sunt in culpa qui officia deserunt mollit
anim id est laborum.

Key Features of ScrolledText:
- Built on the modern ScrollView widget
- Full mouse wheel scrolling support
- Configurable scrollbar visibility modes
- Supports both vertical and horizontal scrolling
- Backwards compatible with legacy API
- Custom scrollbar styling options

Try scrolling with your mouse wheel anywhere on the text!

"""

WIDE_TEXT = """This is a very long line of text that extends far beyond the normal width of the text widget to demonstrate horizontal scrolling functionality. Keep reading to see more content..."""


def demo_always_show():
    """Demo 1: Always show scrollbars."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Always Show")

    ttk.Label(
        frame,
        text="Scrollbars always visible",
        font=('Arial', 12, 'bold'),
        bootstyle='info'
    ).pack(pady=10)

    st = ScrolledText(
        frame,
        height=15,
        show_scrollbar='always',
        scrollbar_style='primary'
    )
    st.pack(fill=BOTH, expand=YES, padx=10, pady=5)

    st.insert(END, SAMPLE_TEXT * 5)

def demo_never_show():
    """Demo 2: Never show scrollbars (scrolling still works)."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Never Show")

    ttk.Label(
        frame,
        text="Scrollbars hidden, but mouse wheel scrolling still works!",
        font=('Arial', 12, 'bold'),
        bootstyle='warning'
    ).pack(pady=10)

    st = ScrolledText(
        frame,
        height=15,
        show_scrollbar='never'
    )
    st.pack(fill=BOTH, expand=YES, padx=10, pady=5)

    st.insert(END, SAMPLE_TEXT * 5)


def demo_on_hover():
    """Demo 3: Show scrollbars on hover."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="On Hover")

    ttk.Label(
        frame,
        text="Hover over the text area to see scrollbars",
        font=('Arial', 12, 'bold'),
        bootstyle='info'
    ).pack(pady=10)

    st = ScrolledText(
        frame,
        height=15,
        show_scrollbar='on-hover',
        scrollbar_style='success'
    )
    st.pack(fill=BOTH, expand=YES, padx=10, pady=5)

    st.insert(END, SAMPLE_TEXT * 5)


def demo_on_scroll():
    """Demo 4: Show scrollbars when scrolling, then auto-hide."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="On Scroll")

    ttk.Label(
        frame,
        text="Scrollbars appear when scrolling, auto-hide after 1.5s",
        font=('Arial', 12, 'bold'),
        bootstyle='success'
    ).pack(pady=10)

    st = ScrolledText(
        frame,
        height=15,
        show_scrollbar='on-scroll',
        scrollbar_style='info',
        autohide_delay=1500
    )
    st.pack(fill=BOTH, expand=YES, padx=10, pady=5)

    st.insert(END, SAMPLE_TEXT * 5)


def demo_horizontal():
    """Demo 5: Horizontal scrolling with both scrollbars."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Both Scrollbars")

    ttk.Label(
        frame,
        text="Vertical and Horizontal scrolling (Shift+MouseWheel for horizontal)",
        font=('Arial', 12, 'bold'),
        bootstyle='primary'
    ).pack(pady=10)

    st = ScrolledText(
        frame,
        height=15,
        direction='both',
        show_scrollbar='always',
        scrollbar_style='danger'
    )
    st.pack(fill=BOTH, expand=YES, padx=10, pady=5)

    # Insert wide text
    st.insert(END, "Horizontal Scrolling Demo\n" + "=" * 80 + "\n\n")
    for i in range(20):
        st.insert(END, f"Line {i+1}: {WIDE_TEXT}\n")


def demo_text_operations():
    """Demo 6: Text widget operations and methods."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Text Operations")

    # Control panel
    control_frame = ttk.Frame(frame)
    control_frame.pack(fill=X, padx=10, pady=10)

    ttk.Label(
        control_frame,
        text="Text Widget Operations:",
        font=('Arial', 11, 'bold')
    ).pack(side=LEFT, padx=5)

    st = ScrolledText(
        frame,
        height=15,
        show_scrollbar='always',
        scrollbar_style='success'
    )
    st.pack(fill=BOTH, expand=YES, padx=10, pady=5)

    st.insert(END, SAMPLE_TEXT * 3)

    def append_text():
        st.insert(END, "\n--- New content appended ---\n" + SAMPLE_TEXT)
        st.see(END)  # Scroll to end

    def clear_text():
        st.delete('1.0', END)

    def get_text():
        content = st.get('1.0', END)
        lines = len(content.splitlines())
        chars = len(content)
        status_label.configure(
            text=f"Text contains {lines} lines and {chars} characters"
        )

    ttk.Button(
        control_frame,
        text="Append Text",
        command=append_text,
        bootstyle='success'
    ).pack(side=LEFT, padx=2)

    ttk.Button(
        control_frame,
        text="Clear All",
        command=clear_text,
        bootstyle='danger'
    ).pack(side=LEFT, padx=2)

    ttk.Button(
        control_frame,
        text="Get Info",
        command=get_text,
        bootstyle='info'
    ).pack(side=LEFT, padx=2)

    status_label = ttk.Label(
        frame,
        text="Ready",
        font=('Arial', 10),
        bootstyle='secondary'
    )
    status_label.pack(pady=5)


def demo_legacy_api():
    """Demo 7: Backwards compatibility with legacy API."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Legacy API")

    ttk.Label(
        frame,
        text="Using legacy API (autohide, vbar, hbar parameters)",
        font=('Arial', 12, 'bold'),
        bootstyle='info'
    ).pack(pady=10)

    # Using old autohide parameter
    st1 = ScrolledText(
        frame,
        height=7,
        autohide=True,  # Maps to show_scrollbar='on-hover'
        vbar=True,
        hbar=False
    )
    st1.pack(fill=BOTH, expand=YES, padx=10, pady=5)

    st1.insert(END, "Legacy API: autohide=True\n" + "=" * 40 + "\n\n")
    st1.insert(END, SAMPLE_TEXT * 2)

    ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=10, pady=5)

    # Using old vbar/hbar parameters
    st2 = ScrolledText(
        frame,
        height=7,
        vbar=True,
        hbar=True  # Maps to direction='both'
    )
    st2.pack(fill=BOTH, expand=YES, padx=10, pady=5)

    st2.insert(END, "Legacy API: vbar=True, hbar=True\n" + "=" * 40 + "\n\n")
    st2.insert(END, f"Wide content: {WIDE_TEXT}\n" * 5)


def demo_custom_styling():
    """Demo 8: Custom scrollbar styling and configuration."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Custom Styling")

    ttk.Label(
        frame,
        text="Dynamic configuration and custom styling",
        font=('Arial', 12, 'bold'),
        bootstyle='primary'
    ).pack(pady=10)

    st = ScrolledText(
        frame,
        height=15,
        show_scrollbar='always',
        scrollbar_style='primary'
    )
    st.pack(fill=BOTH, expand=YES, padx=10, pady=5)

    st.insert(END, SAMPLE_TEXT * 5)

    # Configuration controls
    config_frame = ttk.Frame(frame)
    config_frame.pack(fill=X, padx=10, pady=10)

    ttk.Label(config_frame, text="Scrollbar Mode:").pack(side=LEFT, padx=5)

    mode_var = ttk.StringVar(value='always')

    def change_mode():
        st.configure(show_scrollbar=mode_var.get())

    for text, value in [('Always', 'always'), ('Never', 'never'),
                        ('On Hover', 'on-hover'), ('On Scroll', 'on-scroll')]:
        ttk.Radiobutton(
            config_frame,
            text=text,
            value=value,
            variable=mode_var,
            command=change_mode
        ).pack(side=LEFT, padx=2)

    ttk.Label(config_frame, text="Scrollbar Style:").pack(side=LEFT, padx=(20, 5))

    style_var = ttk.StringVar(value='primary')

    def change_style():
        st.configure(scrollbar_style=style_var.get())

    for style in ['primary', 'success', 'danger', 'warning', 'info']:
        ttk.Radiobutton(
            config_frame,
            text=style.title(),
            value=style,
            variable=style_var,
            command=change_style,
            bootstyle=style
        ).pack(side=LEFT, padx=2)


if __name__ == '__main__':
    root = ttk.Window(
        title="ScrolledText Widget Demo",
        themename="darkly",
        size=(1000, 700)
    )

    # Header
    header = ttk.Frame(root, bootstyle='dark')
    header.pack(fill=X, padx=10, pady=10)

    ttk.Label(
        header,
        text="ScrolledText Widget Demo",
        font=('Arial', 16, 'bold'),
        bootstyle='dark'
    ).pack(side=LEFT)

    ttk.Label(
        header,
        text="Mouse wheel scrolling works everywhere!",
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
    demo_horizontal()
    demo_text_operations()
    demo_legacy_api()
    demo_custom_styling()

    root.mainloop()
