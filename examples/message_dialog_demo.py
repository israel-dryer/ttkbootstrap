"""Demo for MessageDialog and Messagebox with icon provider integration."""

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageBox, MessageDialog


def demo_show_info():
    """Show info dialog."""
    result = MessageBox.show_info(
        message="This is an informational message.\nThe operation completed successfully.",
        title="Information",
        master=root
    )
    result_label.config(text=f"Result: {result}")


def demo_show_warning():
    """Show warning dialog."""
    result = MessageBox.show_warning(
        message="Warning: This action may have consequences.\nPlease proceed with caution.",
        title="Warning",
        master=root
    )
    result_label.config(text=f"Result: {result}")


def demo_show_error():
    """Show error dialog."""
    result = MessageBox.show_error(
        message="Error: The operation failed.\nPlease check your settings and try again.",
        title="Error",
        master=root
    )
    result_label.config(text=f"Result: {result}")


def demo_show_question():
    """Show question dialog."""
    result = MessageBox.show_question(
        message="Do you have any questions about this feature?\nFeel free to ask for help.",
        title="Question",
        master=root
    )
    result_label.config(text=f"Result: {result}")


def demo_ok():
    """Show OK dialog."""
    result = MessageBox.ok(
        message="This is a simple notification.\nClick OK to continue.",
        title="Notification",
        master=root
    )
    result_label.config(text=f"Result: {result}")


def demo_okcancel():
    """Show OK/Cancel dialog."""
    result = MessageBox.okcancel(
        message="Do you want to proceed with this action?",
        title="Confirm",
        master=root
    )
    if result == "OK":
        result_label.config(text=f"User confirmed: {result}", bootstyle="success")
    else:
        result_label.config(text=f"User cancelled: {result}", bootstyle="secondary")


def demo_yesno():
    """Show Yes/No dialog."""
    result = MessageBox.yesno(
        message="Would you like to save your changes?",
        title="Save Changes",
        master=root
    )
    if result == "Yes":
        result_label.config(text=f"User selected: {result}", bootstyle="success")
    else:
        result_label.config(text=f"User selected: {result}", bootstyle="danger")


def demo_yesnocancel():
    """Show Yes/No/Cancel dialog."""
    result = MessageBox.yesnocancel(
        message="You have unsaved changes.\nDo you want to save them before closing?",
        title="Unsaved Changes",
        master=root
    )
    result_label.config(text=f"User selected: {result}")


def demo_retrycancel():
    """Show Retry/Cancel dialog."""
    result = MessageBox.retrycancel(
        message="Connection to server failed.\nWould you like to retry?",
        title="Connection Error",
        master=root
    )
    if result == "Retry":
        result_label.config(text=f"User selected: {result}", bootstyle="info")
    else:
        result_label.config(text=f"User cancelled: {result}", bootstyle="secondary")


def demo_custom_icon_string():
    """Show dialog with custom icon (string)."""
    result = MessageDialog(
        message="This dialog uses a custom heart icon!",
        title="Custom Icon (String)",
        master=root,
        icon="heart-fill",
        buttons=["Close:primary"]
    )
    result.show()
    result_label.config(text=f"Custom icon dialog result: {result.result}")


def demo_custom_icon_dict():
    """Show dialog with custom icon (dict with size and color)."""
    result = MessageDialog(
        message="This dialog uses a large, colored star icon!",
        title="Custom Icon (Dict)",
        master=root,
        icon={"name": "star-fill", "size": 48, "color": "#ffc107"},
        buttons=["Awesome:success", "Close:secondary"]
    )
    result.show()
    result_label.config(text=f"Large custom icon result: {result.result}")


def demo_custom_buttons():
    """Show dialog with custom buttons and styling."""
    result = MessageDialog(
        message="This dialog has custom button configurations.\nEach button has its own style!",
        title="Custom Buttons",
        master=root,
        icon="gear-fill",
        buttons=["Cancel:danger", "Maybe:warning", "Sure:info", "Yes:success"],
        default="Yes"
    )
    result.show()
    result_label.config(text=f"Selected button: {result.result}")


def demo_multiline_message():
    """Show dialog with long multiline message."""
    long_message = """This is a very long message that demonstrates text wrapping.

The MessageDialog automatically wraps text to fit within the specified width.
This makes it easy to display longer messages without worrying about manual formatting.

You can also include multiple paragraphs, as shown here.
Each paragraph will be properly formatted and displayed."""

    result = MessageDialog(
        message=long_message,
        title="Long Message Example",
        master=root,
        icon="file-text-fill",
        buttons=["Got it:primary"],
        width=60
    )
    result.show()
    result_label.config(text="Long message dialog closed")


def demo_no_icon():
    """Show dialog without any icon."""
    result = MessageBox.okcancel(
        message="This dialog has no icon.\nSometimes simpler is better.",
        title="Simple Dialog",
        master=root
    )
    result_label.config(text=f"No-icon dialog result: {result}")


# Create main application window
root = ttk.Window(themename="cosmo")
root.title("Message Dialog Demo")
root.geometry("700x650")

# Header
header = ttk.Frame(root, bootstyle="primary")
header.pack(fill='x', pady=(0, 20))
title_label = ttk.Label(
    header,
    text="Message Dialog & Messagebox Demo",
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
    text="Click buttons below to test different message dialog types with icon provider:",
    font='TkDefaultFont 10'
)
instructions.pack(pady=(0, 15))

# Create notebook for organized demos
notebook = ttk.Notebook(content)
notebook.pack(fill='both', expand=True)

# Tab 1: Standard Dialogs
standard_frame = ttk.Frame(notebook, padding=10)
notebook.add(standard_frame, text="Standard Dialogs")

standard_demos = [
    ("Info Dialog", demo_show_info, "info"),
    ("Warning Dialog", demo_show_warning, "warning"),
    ("Error Dialog", demo_show_error, "danger"),
    ("Question Dialog", demo_show_question, "primary"),
]

for label, command, style in standard_demos:
    btn = ttk.Button(
        standard_frame,
        text=label,
        bootstyle=style,
        command=command,
        width=25
    )
    btn.pack(pady=5, fill='x')

# Tab 2: Button Variations
buttons_frame = ttk.Frame(notebook, padding=10)
notebook.add(buttons_frame, text="Button Variations")

button_demos = [
    ("OK", demo_ok, "secondary"),
    ("OK / Cancel", demo_okcancel, "primary"),
    ("Yes / No", demo_yesno, "success"),
    ("Yes / No / Cancel", demo_yesnocancel, "info"),
    ("Retry / Cancel", demo_retrycancel, "warning"),
]

for label, command, style in button_demos:
    btn = ttk.Button(
        buttons_frame,
        text=label,
        bootstyle=style,
        command=command,
        width=25
    )
    btn.pack(pady=5, fill='x')

# Tab 3: Custom Options
custom_frame = ttk.Frame(notebook, padding=10)
notebook.add(custom_frame, text="Custom Options")

custom_demos = [
    ("Custom Icon (String)", demo_custom_icon_string, "primary"),
    ("Custom Icon (Dict)", demo_custom_icon_dict, "warning"),
    ("Custom Buttons", demo_custom_buttons, "info"),
    ("Long Message", demo_multiline_message, "secondary"),
    ("No Icon", demo_no_icon, "dark"),
]

for label, command, style in custom_demos:
    btn = ttk.Button(
        custom_frame,
        text=label,
        bootstyle=style,
        command=command,
        width=25
    )
    btn.pack(pady=5, fill='x')

# Result display
result_frame = ttk.Labelframe(content, text="Last Dialog Result", padding=15)
result_frame.pack(fill='x', pady=(15, 0))

result_label = ttk.Label(
    result_frame,
    text="No dialog shown yet",
    font='TkDefaultFont 10',
    bootstyle="secondary"
)
result_label.pack()

# Footer
footer = ttk.Label(
    root,
    text="Press ESC in any dialog to cancel • Icons provided by icon provider",
    font='TkDefaultFont 9 italic',
    bootstyle="secondary"
)
footer.pack(pady=10)

root.mainloop()