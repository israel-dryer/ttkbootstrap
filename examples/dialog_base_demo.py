"""Demo for the Dialog base class showing various usage patterns."""

import ttkbootstrap as ttk
from ttkbootstrap.dialogs.base import Dialog


class SimpleDialog(Dialog):
    """A simple dialog with a text entry and OK/Cancel buttons."""

    def __init__(self, parent=None, title="Simple Dialog", prompt="Enter your name:"):
        super().__init__(parent, title, alert=False)
        self.prompt = prompt

    def create_body(self, master):
        """Create the dialog body with a label and entry."""
        frame = ttk.Frame(master, padding=20)
        frame.pack(fill='both', expand=True)

        # Prompt label
        label = ttk.Label(frame, text=self.prompt, font='TkDefaultFont 11')
        label.pack(pady=(0, 10))

        # Entry field
        self.entry = ttk.Entry(frame, width=30)
        self.entry.pack(fill='x')
        self.entry.focus_set()

        # Set initial focus to the entry
        self._initial_focus = self.entry

    def create_buttonbox(self, master):
        """Create OK/Cancel buttons."""
        # Separator
        ttk.Separator(master).pack(fill='x')

        # Button frame
        button_frame = ttk.Frame(master, padding=10)
        button_frame.pack(fill='x')

        # Cancel button
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            bootstyle="secondary",
            command=self.on_cancel,
            width=10
        )
        cancel_btn.pack(side='right', padx=(5, 0))

        # OK button
        ok_btn = ttk.Button(
            button_frame,
            text="OK",
            bootstyle="primary",
            command=self.on_ok,
            width=10
        )
        ok_btn.pack(side='right')

        # Bind Enter key to OK
        self.entry.bind('<Return>', lambda e: self.on_ok())

    def on_ok(self):
        """Handle OK button - save result and close."""
        self._result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        """Handle Cancel button - clear result and close."""
        self._result = None
        self.destroy()


class ConfirmDialog(Dialog):
    """A confirmation dialog with custom message and Yes/No buttons."""

    def __init__(self, parent=None, title="Confirm", message="Are you sure?", alert=True):
        super().__init__(parent, title, alert)
        self.message = message

    def create_body(self, master):
        """Create the dialog body with a message."""
        frame = ttk.Frame(master, padding=30)
        frame.pack(fill='both', expand=True)

        # Icon
        icon_label = ttk.Label(frame, text="❓", font='TkDefaultFont 32')
        icon_label.pack(side='left', padx=(0, 15))

        # Message
        msg_label = ttk.Label(frame, text=self.message, font='TkDefaultFont 11', wraplength=300)
        msg_label.pack(side='left', fill='both', expand=True)

    def create_buttonbox(self, master):
        """Create Yes/No buttons."""
        ttk.Separator(master).pack(fill='x')

        button_frame = ttk.Frame(master, padding=10)
        button_frame.pack(fill='x')

        # No button
        no_btn = ttk.Button(
            button_frame,
            text="No",
            bootstyle="secondary",
            command=lambda: self.on_choice(False),
            width=10
        )
        no_btn.pack(side='right', padx=(5, 0))

        # Yes button
        yes_btn = ttk.Button(
            button_frame,
            text="Yes",
            bootstyle="danger",
            command=lambda: self.on_choice(True),
            width=10
        )
        yes_btn.pack(side='right')

        # Set initial focus to Yes button
        self._initial_focus = yes_btn

        # Bind keyboard shortcuts
        yes_btn.bind('<Return>', lambda e: self.on_choice(True))

    def on_choice(self, value):
        """Handle button press - save choice and close."""
        self._result = value
        self.destroy()


class MultiFieldDialog(Dialog):
    """A dialog with multiple input fields."""

    def __init__(self, parent=None):
        super().__init__(parent, title="User Registration", alert=False)

    def create_body(self, master):
        """Create form with multiple fields."""
        frame = ttk.Frame(master, padding=20)
        frame.pack(fill='both', expand=True)

        # Title
        title = ttk.Label(frame, text="Create New Account", font='TkDefaultFont 14 bold')
        title.pack(pady=(0, 15))

        # Name field
        ttk.Label(frame, text="Full Name:").pack(anchor='w')
        self.name_entry = ttk.Entry(frame, width=40)
        self.name_entry.pack(fill='x', pady=(2, 10))

        # Email field
        ttk.Label(frame, text="Email:").pack(anchor='w')
        self.email_entry = ttk.Entry(frame, width=40)
        self.email_entry.pack(fill='x', pady=(2, 10))

        # Password field
        ttk.Label(frame, text="Password:").pack(anchor='w')
        self.password_entry = ttk.Entry(frame, width=40, show="*")
        self.password_entry.pack(fill='x', pady=(2, 10))

        # Set initial focus
        self._initial_focus = self.name_entry

    def create_buttonbox(self, master):
        """Create Register/Cancel buttons."""
        ttk.Separator(master).pack(fill='x')

        button_frame = ttk.Frame(master, padding=10)
        button_frame.pack(fill='x')

        # Cancel button
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            bootstyle="secondary",
            command=self.on_cancel,
            width=12
        )
        cancel_btn.pack(side='right', padx=(5, 0))

        # Register button
        register_btn = ttk.Button(
            button_frame,
            text="Register",
            bootstyle="success",
            command=self.on_register,
            width=12
        )
        register_btn.pack(side='right')

        # Bind Enter to register
        self.password_entry.bind('<Return>', lambda e: self.on_register())

    def on_register(self):
        """Validate and save registration data."""
        data = {
            'name': self.name_entry.get(),
            'email': self.email_entry.get(),
            'password': self.password_entry.get()
        }

        # Simple validation
        if not data['name'] or not data['email'] or not data['password']:
            # In a real app, you'd show an error message
            return

        self._result = data
        self.destroy()

    def on_cancel(self):
        """Cancel registration."""
        self._result = None
        self.destroy()


def demo_simple_dialog(parent):
    """Demo: Simple text input dialog."""
    dialog = SimpleDialog(parent, title="Enter Name", prompt="What is your name?")
    dialog.show()

    result = dialog.result
    if result:
        result_label.config(text=f"You entered: {result}")
    else:
        result_label.config(text="Dialog was cancelled")


def demo_confirm_dialog(parent):
    """Demo: Confirmation dialog."""
    dialog = ConfirmDialog(
        parent,
        title="Confirm Action",
        message="Do you want to delete all files?\nThis action cannot be undone.",
        alert=True
    )
    dialog.show()

    result = dialog.result
    if result:
        result_label.config(text="User confirmed: YES", bootstyle="danger")
    else:
        result_label.config(text="User confirmed: NO", bootstyle="secondary")


def demo_multi_field_dialog(parent):
    """Demo: Multi-field registration dialog."""
    dialog = MultiFieldDialog(parent)
    dialog.show()

    result = dialog.result
    if result:
        result_label.config(
            text=f"Registered:\nName: {result['name']}\nEmail: {result['email']}",
            bootstyle="success"
        )
    else:
        result_label.config(text="Registration cancelled")


def demo_non_modal_dialog(parent):
    """Demo: Non-modal dialog (doesn't block)."""
    dialog = SimpleDialog(parent, title="Non-Modal", prompt="This dialog is non-modal")
    dialog.show(wait_for_result=False)
    result_label.config(text="Dialog opened non-modally (you can still interact with main window)")


def demo_positioned_dialog(parent):
    """Demo: Dialog with custom position."""
    dialog = SimpleDialog(parent, title="Positioned", prompt="This dialog is at (100, 100)")
    dialog.show(position=(100, 100))

    result = dialog.result
    if result:
        result_label.config(text=f"Positioned dialog result: {result}")
    else:
        result_label.config(text="Positioned dialog cancelled")


def demo_reusable_dialog(parent):
    """Demo: Showing the same dialog multiple times."""
    global reusable_dialog

    if 'reusable_dialog' not in globals():
        reusable_dialog = SimpleDialog(parent, title="Reusable Dialog", prompt="Dialog instance #1")

    reusable_dialog.show()
    result = reusable_dialog.result

    if result:
        result_label.config(text=f"Reusable dialog result: {result}")
    else:
        result_label.config(text="Reusable dialog cancelled")


# Create main application window
root = ttk.Window(themename="cosmo")
root.title("Dialog Base Class Demo")
root.geometry("600x500")

# Header
header = ttk.Frame(root, bootstyle="primary")
header.pack(fill='x', pady=(0, 20))
title_label = ttk.Label(
    header,
    text="Dialog Base Class Demonstrations",
    font='TkDefaultFont 16 bold'
)
title_label.pack(pady=15)

# Main content
content = ttk.Frame(root, padding=20)
content.pack(fill='both', expand=True)

# Instructions
instructions = ttk.Label(
    content,
    text="Click the buttons below to test different dialog patterns:",
    font='TkDefaultFont 10'
)
instructions.pack(pady=(0, 20))

# Demo buttons
button_frame = ttk.Frame(content)
button_frame.pack(fill='both', expand=True)

demos = [
    ("Simple Input Dialog", demo_simple_dialog, "primary"),
    ("Confirmation Dialog", demo_confirm_dialog, "warning"),
    ("Multi-Field Dialog", demo_multi_field_dialog, "success"),
    ("Non-Modal Dialog", demo_non_modal_dialog, "info"),
    ("Positioned Dialog", demo_positioned_dialog, "secondary"),
    ("Reusable Dialog", demo_reusable_dialog, "dark"),
]

for i, (label, command, style) in enumerate(demos):
    btn = ttk.Button(
        button_frame,
        text=label,
        bootstyle=style,
        command=lambda c=command: c(root),
        width=25
    )
    btn.pack(pady=5, fill='x')

# Result display
result_frame = ttk.Labelframe(content, text="Result", padding=15)
result_frame.pack(fill='x', pady=(20, 0))

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
    text="Press ESC in any dialog to cancel",
    font='TkDefaultFont 9 italic',
    bootstyle="secondary"
)
footer.pack(pady=10)

root.mainloop()
