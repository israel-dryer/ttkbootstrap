"""Demo for QueryDialog and Querybox with various input types."""

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryBox


def demo_get_string():
    """Show string input dialog."""
    result = QueryBox.get_string(
        prompt="What is your name?",
        title="Name Input",
        value="John Doe",
        master=root
    )
    if result:
        result_label.config(text=f"Name entered: {result}", bootstyle="info")
    else:
        result_label.config(text="String input cancelled", bootstyle="secondary")


def demo_get_string_multiline():
    """Show string input with multiline prompt."""
    result = QueryBox.get_string(
        prompt="Please enter your email address.\nThis will be used for account verification.\nMake sure it's valid!",
        title="Email Input",
        value="user@example.com",
        master=root
    )
    if result:
        result_label.config(text=f"Email entered: {result}", bootstyle="success")
    else:
        result_label.config(text="Email input cancelled", bootstyle="secondary")


def demo_get_item():
    """Show item selection dialog with dropdown."""
    items = ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript", "Swift", "Kotlin"]
    result = QueryBox.get_item(
        prompt="Select your favorite programming language:",
        title="Language Selection",
        value="Python",
        items=items,
        master=root
    )
    if result:
        result_label.config(text=f"Selected language: {result}", bootstyle="success")
    else:
        result_label.config(text="Language selection cancelled", bootstyle="secondary")


def demo_get_item_filtered():
    """Show item selection with many items (filterable)."""
    countries = [
        "United States", "Canada", "United Kingdom", "Germany", "France",
        "Spain", "Italy", "Netherlands", "Belgium", "Switzerland",
        "Australia", "New Zealand", "Japan", "South Korea", "China",
        "India", "Brazil", "Mexico", "Argentina", "Chile"
    ]
    result = QueryBox.get_item(
        prompt="Select your country:\n(You can type to filter the list)",
        title="Country Selection",
        items=countries,
        master=root
    )
    if result:
        result_label.config(text=f"Selected country: {result}", bootstyle="info")
    else:
        result_label.config(text="Country selection cancelled", bootstyle="secondary")


def demo_get_integer():
    """Show integer input with validation."""
    result = QueryBox.get_integer(
        prompt="Enter your age:",
        title="Age Input",
        value=25,
        minvalue=0,
        maxvalue=120,
        master=root
    )
    if result is not None:
        result_label.config(text=f"Age entered: {result}", bootstyle="success")
    else:
        result_label.config(text="Age input cancelled", bootstyle="secondary")


def demo_get_integer_range():
    """Show integer input with strict range."""
    result = QueryBox.get_integer(
        prompt="Enter a number between 1 and 100:",
        title="Range Input",
        value=50,
        minvalue=1,
        maxvalue=100,
        master=root
    )
    if result is not None:
        result_label.config(text=f"Number entered: {result} (valid range: 1-100)", bootstyle="info")
    else:
        result_label.config(text="Range input cancelled", bootstyle="secondary")


def demo_get_float():
    """Show float input with validation."""
    result = QueryBox.get_float(
        prompt="Enter the product price:",
        title="Price Input",
        value=19.99,
        minvalue=0.01,
        maxvalue=9999.99,
        master=root
    )
    if result is not None:
        result_label.config(text=f"Price entered: ${result:.2f}", bootstyle="success")
    else:
        result_label.config(text="Price input cancelled", bootstyle="secondary")


def demo_get_float_percentage():
    """Show float input for percentage."""
    result = QueryBox.get_float(
        prompt="Enter discount percentage:",
        title="Discount Input",
        value=15.0,
        minvalue=0.0,
        maxvalue=100.0,
        master=root
    )
    if result is not None:
        result_label.config(text=f"Discount: {result}%", bootstyle="warning")
    else:
        result_label.config(text="Discount input cancelled", bootstyle="secondary")


def demo_get_color():
    """Show color picker dialog."""
    result = QueryBox.get_color(
        title="Choose a Color",
        initialcolor="#3498db",
        master=root
    )
    if result:
        # result is a Color object, need to get hex value
        result_label.config(
            text=f"Color selected: {result.hex}",
            bootstyle="primary",
            background=result.hex
        )
    else:
        result_label.config(text="Color selection cancelled", bootstyle="secondary", background="")


def demo_get_date():
    """Show date picker dialog."""
    result = QueryBox.get_date(
        title="Select a Date",
        master=root
    )
    if result:
        result_label.config(text=f"Date selected: {result.strftime('%Y-%m-%d')}", bootstyle="info")
    else:
        result_label.config(text="Date selection cancelled", bootstyle="secondary")


def demo_get_font():
    """Show font picker dialog."""
    result = QueryBox.get_font(master=root)
    if result:
        result_label.config(
            text=f"Font selected: {result.actual()['family']} {result.actual()['size']}pt",
            bootstyle="success",
            font=result
        )
    else:
        result_label.config(text="Font selection cancelled", bootstyle="secondary")


def demo_positioned_dialog():
    """Show dialog at specific position."""
    result = QueryBox.get_string(
        prompt="This dialog appears at position (200, 200)",
        title="Positioned Dialog",
        value="Custom position",
        master=root,
        position=(200, 200)
    )
    if result:
        result_label.config(text=f"Positioned dialog result: {result}")
    else:
        result_label.config(text="Positioned dialog cancelled")


# Create main application window
root = ttk.Window(theme="cosmo")
root.title("Query Dialog Demo")
root.geometry("700x700")

# Header
header = ttk.Frame(root, bootstyle="primary")
header.pack(fill='x', pady=(0, 20))
title_label = ttk.Label(
    header,
    text="Query Dialog & Querybox Demo",
    font='TkDefaultFont 16 bold',
    foreground="white"
)
title_label.pack(pady=15)

# Main content
content = ttk.Frame(root, padding=20)
content.pack(fill='both', expand=True)

# Instructions
instructions = ttk.Label(
    content,
    text="Click buttons below to test different input dialog types with validation:",
    font='TkDefaultFont 10'
)
instructions.pack(pady=(0, 15))

# Create notebook for organized demos
notebook = ttk.Notebook(content)
notebook.pack(fill='both', expand=True)

# Tab 1: String Inputs
string_frame = ttk.Frame(notebook, padding=10)
notebook.add(string_frame, text="String Input")

string_demos = [
    ("Simple String", demo_get_string, "primary"),
    ("Multiline Prompt", demo_get_string_multiline, "info"),
]

for label, command, style in string_demos:
    btn = ttk.Button(
        string_frame,
        text=label,
        bootstyle=style,
        command=command,
        width=25
    )
    btn.pack(pady=5, fill='x')

# Tab 2: Item Selection
item_frame = ttk.Frame(notebook, padding=10)
notebook.add(item_frame, text="Item Selection")

item_demos = [
    ("Select from List", demo_get_item, "success"),
    ("Filterable List", demo_get_item_filtered, "info"),
]

for label, command, style in item_demos:
    btn = ttk.Button(
        item_frame,
        text=label,
        bootstyle=style,
        command=command,
        width=25
    )
    btn.pack(pady=5, fill='x')

# Tab 3: Numeric Inputs
numeric_frame = ttk.Frame(notebook, padding=10)
notebook.add(numeric_frame, text="Numeric Input")

numeric_demos = [
    ("Integer Input", demo_get_integer, "primary"),
    ("Integer with Range", demo_get_integer_range, "warning"),
    ("Float Input", demo_get_float, "success"),
    ("Percentage Input", demo_get_float_percentage, "info"),
]

for label, command, style in numeric_demos:
    btn = ttk.Button(
        numeric_frame,
        text=label,
        bootstyle=style,
        command=command,
        width=25
    )
    btn.pack(pady=5, fill='x')

# Tab 4: Special Pickers
picker_frame = ttk.Frame(notebook, padding=10)
notebook.add(picker_frame, text="Special Pickers")

picker_demos = [
    ("Color Picker", demo_get_color, "primary"),
    ("Date Picker", demo_get_date, "info"),
    ("Font Picker", demo_get_font, "success"),
]

for label, command, style in picker_demos:
    btn = ttk.Button(
        picker_frame,
        text=label,
        bootstyle=style,
        command=command,
        width=25
    )
    btn.pack(pady=5, fill='x')

# Tab 5: Advanced
advanced_frame = ttk.Frame(notebook, padding=10)
notebook.add(advanced_frame, text="Advanced")

advanced_demos = [
    ("Positioned Dialog", demo_positioned_dialog, "secondary"),
]

for label, command, style in advanced_demos:
    btn = ttk.Button(
        advanced_frame,
        text=label,
        bootstyle=style,
        command=command,
        width=25
    )
    btn.pack(pady=5, fill='x')

# Result display
result_frame = ttk.LabelFrame(content, text="Last Dialog Result", padding=15)
result_frame.pack(fill='x', pady=(20, 0))

result_label = ttk.Label(
    result_frame,
    text="No dialog shown yet",
    font='TkDefaultFont 10',
    bootstyle="secondary"
)
result_label.pack()

# Footer
footer_frame = ttk.Frame(root)
footer_frame.pack(pady=10)

footer1 = ttk.Label(
    footer_frame,
    text="Press ESC to cancel • Press ENTER to submit",
    font='TkDefaultFont 9 italic',
    bootstyle="secondary"
)
footer1.pack()

footer2 = ttk.Label(
    footer_frame,
    text="Validation errors will show inline dialogs",
    font='TkDefaultFont 8 italic',
    bootstyle="secondary"
)
footer2.pack()

root.mainloop()