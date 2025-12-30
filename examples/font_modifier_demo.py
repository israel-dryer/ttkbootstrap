"""
Font Modifier Syntax Demo

Demonstrates the new font modifier syntax for ttkbootstrap widgets.
This allows inline font customization using bracket notation.

Syntax: family[size][weight][style]

Examples shown in this demo:
- Token-based fonts with modifiers
- Custom font families with modifiers
- Size specifications (points and pixels)
- Weight and style combinations
- Size token shortcuts
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_demo_window():
    """Create a demo window showing various font modifier examples."""

    root = ttk.Window(title="Font Modifier Syntax Demo", theme="cosmo")
    root.geometry("800x900")

    # Main container
    container = ttk.Frame(root, padding=20)
    container.pack(fill=BOTH, expand=YES)

    # Title
    title = ttk.Label(
        container,
        text="Font Modifier Syntax Examples",
        font="heading-xl[bold]",
        color="primary"
    )
    title.pack(pady=(0, 20))

    # Description
    desc = ttk.Label(
        container,
        text="The font modifier syntax allows you to customize fonts inline using bracket notation:",
        font="body",
        wraplength=700
    )
    desc.pack(pady=(0, 10))

    syntax = ttk.Label(
        container,
        text="Syntax: family[size][weight][style]",
        font="code[bold]",
        color="info"
    )
    syntax.pack(pady=(0, 20))

    # Examples Frame
    examples_frame = ttk.Frame(container)
    examples_frame.pack(fill=BOTH, expand=YES)

    # Create a list of examples
    examples = [
        # (font_spec, description)
        ("body[bold]", "Body font with bold weight"),
        ("body[italic]", "Body font with italic style"),
        ("body[bold,underline]", "Body font with bold and underline"),
        ("heading-lg[italic]", "Heading-lg token with italic"),
        ("label[16]", "Label token with 16pt size"),
        ("[sm][bold]", "Small size (10pt) with bold"),
        ("[lg][italic]", "Large size (14pt) with italic"),
        ("[16][bold,underline]", "16pt with bold and underline"),
        ("helvetica[16][bold]", "Helvetica, 16pt, bold"),
        ("helvetica[14px][bold,italic]", "Helvetica, 14 pixels, bold italic"),
        ("courier[12][normal]", "Courier, 12pt, normal weight"),
        ("arial[18][bold]", "Arial, 18pt, bold"),
        ("[xl][bold,italic,underline]", "XL size with multiple modifiers"),
        ("code", "Code token (monospace)"),
        ("hyperlink", "Hyperlink token (underlined)"),
    ]

    # Create labels for each example
    for i, (font_spec, description) in enumerate(examples):
        # Create a frame for each example
        example_frame = ttk.Frame(examples_frame)
        example_frame.pack(fill=X, pady=5)

        # Font spec label (left side)
        spec_label = ttk.Label(
            example_frame,
            text=f'font="{font_spec}"',
            font="code",
            width=40,
            color="secondary"
        )
        spec_label.pack(side=LEFT, padx=(0, 10))

        # Demo label (right side)
        demo_label = ttk.Label(
            example_frame,
            text=description,
            font=font_spec
        )
        demo_label.pack(side=LEFT, fill=X, expand=YES)

    # Separator
    sep = ttk.Separator(container, orient=HORIZONTAL)
    sep.pack(fill=X, pady=20)

    # Interactive section
    interactive_title = ttk.Label(
        container,
        text="Interactive Font Test",
        font="heading-md[bold]",
        color="success"
    )
    interactive_title.pack(pady=(0, 10))

    # Input frame
    input_frame = ttk.Frame(container)
    input_frame.pack(fill=X, pady=10)

    ttk.Label(input_frame, text="Enter font spec:", font="body").pack(side=LEFT, padx=(0, 10))

    font_var = ttk.StringVar(value="helvetica[16][bold]")
    font_entry = ttk.Entry(input_frame, textvariable=font_var, width=30)
    font_entry.pack(side=LEFT, padx=(0, 10))

    # Preview label
    preview_label = ttk.Label(
        container,
        text="This is a preview of your font specification",
        font=font_var.get(),
        color="info",
        padding=20
    )
    preview_label.pack(fill=X, pady=10)

    # Update button
    def update_preview():
        try:
            preview_label.configure(font=font_var.get())
            status_label.configure(text="✓ Font applied successfully", color="success")
        except Exception as e:
            status_label.configure(text=f"✗ Error: {str(e)}", color="danger")

    update_btn = ttk.Button(
        input_frame,
        text="Apply Font",
        command=update_preview,
        color="success"
    )
    update_btn.pack(side=LEFT)

    # Status label
    status_label = ttk.Label(container, text="", font="caption")
    status_label.pack(pady=5)

    # Additional info
    info_frame = ttk.Frame(container)
    info_frame.pack(fill=X, pady=20)

    info_text = """
Size Tokens: xs (8pt), sm (10pt), md (12pt), lg (14pt), xl (16pt), xxl (18pt)
Font Tokens: body, label, heading-md, heading-lg, heading-xl, display-lg, display-xl, code, hyperlink, etc.
Weight: bold, normal
Style: italic, roman
Modifiers: underline, overstrike
    """.strip()

    info_label = ttk.Label(
        info_frame,
        text=info_text,
        font="caption",
        justify=LEFT,
        color="secondary"
    )
    info_label.pack(fill=X)

    # Bind Enter key to update preview
    font_entry.bind('<Return>', lambda e: update_preview())

    root.mainloop()


if __name__ == "__main__":
    create_demo_window()