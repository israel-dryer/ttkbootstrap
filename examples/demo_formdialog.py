"""Demonstration of the FormDialog widget.

Shows various uses of FormDialog for data entry in modal dialogs:
- Simple auto-inferred forms
- Explicit layout with groups and tabs
- Custom validation
- Different button configurations
"""

from datetime import date

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import FormDialog, DialogButton
from ttkbootstrap.widgets.composites.form import FieldItem, GroupItem, TabItem, TabsItem


def demo_simple_form(parent):
    """Simple form with auto-inferred fields."""
    initial_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "age": 34,
        "email": "jane@example.com",
        "active": True,
        "salary": 75000.0,
    }

    dialog = FormDialog(
        master=parent,
        title="Edit User - Simple Form",
        data=initial_data,
        col_count=2,
    )
    dialog.show(anchor_to="screen")

    if dialog.result:
        print("Simple form result:", dialog.result)
        ttk.Toast(
            title="Form Submitted",
            message=f"User {dialog.result['first_name']} {dialog.result['last_name']} updated!",
            duration=3000,
            accent="success",
        ).show()
    else:
        print("Simple form cancelled")


def demo_explicit_layout(parent):
    """Form with explicit layout using groups and tabs."""
    items = [
        GroupItem(
            label="Account Information",
            col_count=2,
            items=[
                FieldItem(key="username", label="Username"),
                FieldItem(key="password", label="Password", editor="passwordentry"),
                FieldItem(key="email", label="Email Address"),
                FieldItem(key="role", label="Role", editor="selectbox",
                         editor_options={"items": ["Admin", "User", "Viewer", "Guest"]}),
            ],
        ),
        TabsItem(
            tabs=[
                TabItem(
                    label="Preferences",
                    items=[
                        FieldItem(key="newsletter", label="Subscribe to Newsletter", dtype=bool, editor="toggle"),
                        FieldItem(key="theme", label="Theme", editor="selectbox",
                                 editor_options={"items": ["Light", "Dark", "Auto"]}),
                        FieldItem(key="language", label="Language", editor="selectbox",
                                 editor_options={"items": ["English", "Spanish", "French", "German"]}),
                    ],
                ),
                TabItem(
                    label="Limits",
                    items=[
                        FieldItem(key="daily_limit", label="Daily API Limit", dtype="int"),
                        FieldItem(key="storage_quota", label="Storage Quota (GB)", dtype="float"),
                        FieldItem(key="max_connections", label="Max Connections", dtype="int"),
                    ],
                ),
            ],
        ),
    ]

    initial_data = {
        "username": "jdoe",
        "password": "",
        "email": "jdoe@example.com",
        "role": "User",
        "newsletter": True,
        "theme": "Auto",
        "language": "English",
        "daily_limit": 1000,
        "storage_quota": 10.0,
        "max_connections": 5,
    }

    dialog = FormDialog(
        master=parent,
        title="User Profile Settings",
        data=initial_data,
        items=items,
        col_count=1,
        height=400,
    )
    dialog.show(anchor_to="screen")

    if dialog.result:
        print("Explicit layout result:", dialog.result)
        ttk.Toast(
            title="Settings Saved",
            message="Profile settings have been updated",
            duration=3000,
            accent="info",
        ).show()
    else:
        print("Explicit layout cancelled")


def demo_with_validation(parent):
    """Form with custom validation logic."""

    def validate_and_save(dlg):
        """Custom validation before accepting the form."""
        data = dlg.form.data

        # Check required fields
        if not data.get("product_name"):
            ttk.Toast(
                title="Validation Error",
                message="Product name is required!",
                duration=3000,
                accent="danger",
            ).show()
            return  # Don't set result, keep dialog open

        if data.get("price", 0) <= 0:
            ttk.Toast(
                title="Validation Error",
                message="Price must be greater than 0!",
                duration=3000,
                accent="danger",
            ).show()
            return

        # If validation passes, set result and close
        dlg.result = data

    items = [
        FieldItem(key="product_name", label="Product Name"),
        FieldItem(key="description", label="Description", editor="text", editor_options={"height": 4}),
        FieldItem(key="price", label="Price ($)", dtype="float"),
        FieldItem(key="quantity", label="Quantity", dtype="int"),
        FieldItem(key="in_stock", label="In Stock", dtype=bool, editor="checkbutton"),
        FieldItem(key="category", label="Category", editor="selectbox",
                 editor_options={"items": ["Electronics", "Clothing", "Food", "Books", "Other"]}),
    ]

    initial_data = {
        "product_name": "",
        "description": "",
        "price": 0.0,
        "quantity": 1,
        "in_stock": True,
        "category": "Other",
    }

    dialog = FormDialog(
        master=parent,
        title="Add New Product",
        data=initial_data,
        items=items,
        col_count=2,
        buttons=[
            DialogButton(text="Cancel", role="cancel", result=None),
            DialogButton(text="Save", role="primary", command=validate_and_save, default=True),
        ],
    )
    dialog.show(anchor_to="screen")

    if dialog.result:
        print("Product saved:", dialog.result)
        ttk.Toast(
            title="Product Added",
            message=f"Product '{dialog.result['product_name']}' has been added",
            duration=3000,
            accent="success",
        ).show()
    else:
        print("Product add cancelled")


def demo_registration_form(parent):
    """Registration form with multiple validation steps."""

    def validate_registration(dlg):
        """Validate registration form."""
        data = dlg.form.data

        # Check all required fields
        if not data.get("email") or "@" not in data.get("email", ""):
            ttk.Toast(
                title="Invalid Email",
                message="Please enter a valid email address",
                duration=3000,
                accent="warning",
            ).show()
            return

        if not data.get("password") or len(data.get("password", "")) < 8:
            ttk.Toast(
                title="Weak Password",
                message="Password must be at least 8 characters",
                duration=3000,
                accent="warning",
            ).show()
            return

        if data.get("password") != data.get("confirm_password"):
            ttk.Toast(
                title="Password Mismatch",
                message="Passwords do not match",
                duration=3000,
                accent="danger",
            ).show()
            return

        # All validations passed
        dlg.result = data

    items = [
        GroupItem(
            label="Personal Information",
            col_count=2,
            items=[
                FieldItem(key="first_name", label="First Name"),
                FieldItem(key="last_name", label="Last Name"),
                FieldItem(key="birth_date", label="Birth Date", dtype="date"),
                FieldItem(key="country", label="Country", editor="selectbox",
                         editor_options={"items": ["United States", "Canada", "United Kingdom", "Other"]}),
            ],
        ),
        GroupItem(
            label="Account Details",
            col_count=2,
            items=[
                FieldItem(key="email", label="Email Address", columnspan=2),
                FieldItem(key="password", label="Password", editor="passwordentry"),
                FieldItem(key="confirm_password", label="Confirm Password", editor="passwordentry"),
            ],
        ),
        GroupItem(
            label="Preferences",
            col_count=1,
            items=[
                FieldItem(key="newsletter", label="Subscribe to newsletter", dtype=bool, editor="toggle"),
                FieldItem(key="terms", label="I agree to the terms and conditions", dtype=bool, editor="checkbutton"),
            ],
        ),
    ]

    initial_data = {
        "first_name": "",
        "last_name": "",
        "birth_date": date.today(),
        "country": "United States",
        "email": "",
        "password": "",
        "confirm_password": "",
        "newsletter": True,
        "terms": False,
    }

    dialog = FormDialog(
        master=parent,
        title="User Registration",
        data=initial_data,
        items=items,
        col_count=1,
        scrollable=True,
        buttons=[
            DialogButton(text="Cancel", role="cancel", result=None),
            DialogButton(text="Register", role="primary", command=validate_registration, default=True),
        ],
    )
    dialog.show(anchor_to="screen")

    if dialog.result:
        print("Registration successful:", {k: v for k, v in dialog.result.items() if k not in ["password", "confirm_password"]})
        ttk.Toast(
            title="Registration Complete",
            message=f"Welcome, {dialog.result['first_name']}!",
            duration=3000,
            accent="success",
        ).show()
    else:
        print("Registration cancelled")


def main():
    app = ttk.Window(title="FormDialog Demo", theme="flatly")
    #app.geometry("600x400")

    # Title
    title = ttk.Label(
        app,
        text="FormDialog Examples",
        font=("TkDefaultFont", 16, "bold"),
    )
    title.pack(pady=20)

    # Description
    desc = ttk.Label(
        app,
        text="Click a button to open a FormDialog demonstration",
        font=("TkDefaultFont", 10),
    )
    desc.pack(pady=(0, 30))

    # Button container
    button_frame = ttk.Frame(app)
    button_frame.pack(expand=True)

    # Demo buttons
    ttk.Button(
        button_frame,
        text="Simple Form (Auto-Inferred)",
        command=lambda: demo_simple_form(app),
        accent="primary",
        width=30,
    ).pack(pady=8)

    ttk.Button(
        button_frame,
        text="Explicit Layout (Groups & Tabs)",
        command=lambda: demo_explicit_layout(app),
        accent="info",
        width=30,
    ).pack(pady=8)

    ttk.Button(
        button_frame,
        text="Form with Validation",
        command=lambda: demo_with_validation(app),
        accent="success",
        width=30,
    ).pack(pady=8)

    ttk.Button(
        button_frame,
        text="Registration Form",
        command=lambda: demo_registration_form(app),
        accent="warning",
        width=30,
    ).pack(pady=8)

    # Exit button
    ttk.Button(
        app,
        text="Exit",
        command=app.destroy,
        accent="secondary",
        variant="outline",
        width=20,
    ).pack(pady=20)

    app.mainloop()


if __name__ == "__main__":
    main()
