"""Demonstration of grouped forms with FormDialog.

This demo focuses specifically on GroupItem functionality, showing:
- Multiple groups in a single form
- Nested groups
- Multi-column groups
- Groups with different field types
"""

from datetime import date

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import FormDialog, DialogButton
from ttkbootstrap.widgets.composites.form import FieldItem, GroupItem


def demo_basic_groups(parent):
    """Form with multiple basic groups."""
    items = [
        GroupItem(
            label="🔐 Authentication",
            col_count=1,
            items=[
                FieldItem(key="username", label="Username"),
                FieldItem(key="password", label="Password", editor="passwordentry"),
                FieldItem(key="remember_me", label="Remember me", dtype=bool, editor="toggle"),
            ],
        ),
        GroupItem(
            label="📧 Contact Information",
            col_count=2,
            items=[
                FieldItem(key="email", label="Email", columnspan=2),
                FieldItem(key="phone", label="Phone"),
                FieldItem(key="mobile", label="Mobile"),
            ],
        ),
        GroupItem(
            label="📍 Address",
            col_count=1,
            items=[
                FieldItem(key="street", label="Street Address"),
                FieldItem(key="city", label="City"),
                FieldItem(key="zipcode", label="Zip Code"),
            ],
        ),
    ]

    initial_data = {
        "username": "demo_user",
        "password": "",
        "remember_me": True,
        "email": "user@example.com",
        "phone": "555-0100",
        "mobile": "555-0200",
        "street": "123 Main St",
        "city": "Springfield",
        "zipcode": "12345",
    }

    dialog = FormDialog(
        master=parent,
        title="User Profile - Basic Groups",
        data=initial_data,
        items=items,
        col_count=1,
        min_col_width=350,
    )
    dialog.show()

    if dialog.result:
        print("Basic groups result:", dialog.result)
        ttk.Toast(
            title="Profile Updated",
            message="Your profile has been saved successfully",
            duration=3000,
            bootstyle="success",
        ).show()


def demo_multicolumn_groups(parent):
    """Form with multi-column group layouts."""
    items = [
        GroupItem(
            label="Personal Details",
            col_count=3,
            items=[
                FieldItem(key="first_name", label="First Name"),
                FieldItem(key="middle_name", label="Middle Name"),
                FieldItem(key="last_name", label="Last Name"),
                FieldItem(key="birth_date", label="Birth Date", dtype="date"),
                FieldItem(key="ssn", label="SSN"),
                FieldItem(key="gender", label="Gender", editor="selectbox",
                         editor_options={"items": ["Male", "Female", "Other", "Prefer not to say"]}),
            ],
        ),
        GroupItem(
            label="Employment Information",
            col_count=2,
            items=[
                FieldItem(key="job_title", label="Job Title"),
                FieldItem(key="department", label="Department", editor="selectbox",
                         editor_options={"items": ["Engineering", "Sales", "Marketing", "HR", "Finance"]}),
                FieldItem(key="employee_id", label="Employee ID"),
                FieldItem(key="hire_date", label="Hire Date", dtype="date"),
                FieldItem(key="salary", label="Annual Salary", dtype="float"),
                FieldItem(key="full_time", label="Full Time", dtype=bool, editor="checkbutton"),
            ],
        ),
        GroupItem(
            label="Benefits",
            col_count=2,
            items=[
                FieldItem(key="health_insurance", label="Health Insurance", dtype=bool, editor="toggle"),
                FieldItem(key="dental_insurance", label="Dental Insurance", dtype=bool, editor="toggle"),
                FieldItem(key="vision_insurance", label="Vision Insurance", dtype=bool, editor="toggle"),
                FieldItem(key="retirement_plan", label="401(k) Plan", dtype=bool, editor="toggle"),
            ],
        ),
    ]

    initial_data = {
        "first_name": "John",
        "middle_name": "Q",
        "last_name": "Doe",
        "birth_date": date(1990, 5, 15),
        "ssn": "***-**-1234",
        "gender": "Male",
        "job_title": "Senior Developer",
        "department": "Engineering",
        "employee_id": "EMP-12345",
        "hire_date": date(2020, 3, 1),
        "salary": 95000.0,
        "full_time": True,
        "health_insurance": True,
        "dental_insurance": True,
        "vision_insurance": False,
        "retirement_plan": True,
    }

    dialog = FormDialog(
        master=parent,
        title="Employee Record - Multi-Column Groups",
        data=initial_data,
        items=items,
        col_count=1,
        min_col_width=400,
        height=500,
    )
    dialog.show()

    if dialog.result:
        print("Multi-column groups result:", dialog.result)
        ttk.Toast(
            title="Employee Record Updated",
            message=f"Record for {dialog.result['first_name']} {dialog.result['last_name']} saved",
            duration=3000,
            bootstyle="info",
        ).show()


def demo_nested_groups(parent):
    """Form with nested groups demonstrating hierarchy."""
    items = [
        GroupItem(
            label="Project Configuration",
            col_count=1,
            items=[
                FieldItem(key="project_name", label="Project Name"),
                FieldItem(key="description", label="Description", editor="text",
                         editor_options={"height": 3}),
                GroupItem(
                    label="Repository Settings",
                    col_count=2,
                    items=[
                        FieldItem(key="repo_url", label="Repository URL", columnspan=2),
                        FieldItem(key="branch", label="Default Branch"),
                        FieldItem(key="private", label="Private Repo", dtype=bool, editor="checkbutton"),
                    ],
                ),
                GroupItem(
                    label="Build Configuration",
                    col_count=2,
                    items=[
                        FieldItem(key="build_command", label="Build Command", columnspan=2),
                        FieldItem(key="test_command", label="Test Command", columnspan=2),
                        FieldItem(key="auto_build", label="Auto Build", dtype=bool, editor="toggle"),
                        FieldItem(key="auto_test", label="Auto Test", dtype=bool, editor="toggle"),
                    ],
                ),
            ],
        ),
        GroupItem(
            label="Deployment Settings",
            col_count=1,
            items=[
                GroupItem(
                    label="Production Environment",
                    col_count=2,
                    items=[
                        FieldItem(key="prod_url", label="Production URL", columnspan=2),
                        FieldItem(key="prod_api_key", label="API Key", editor="passwordentry"),
                        FieldItem(key="prod_enabled", label="Enabled", dtype=bool, editor="toggle"),
                    ],
                ),
                GroupItem(
                    label="Staging Environment",
                    col_count=2,
                    items=[
                        FieldItem(key="staging_url", label="Staging URL", columnspan=2),
                        FieldItem(key="staging_api_key", label="API Key", editor="passwordentry"),
                        FieldItem(key="staging_enabled", label="Enabled", dtype=bool, editor="toggle"),
                    ],
                ),
            ],
        ),
    ]

    initial_data = {
        "project_name": "MyAwesomeApp",
        "description": "A revolutionary application that changes everything",
        "repo_url": "https://github.com/user/myawesomeapp",
        "branch": "main",
        "private": True,
        "build_command": "npm run build",
        "test_command": "npm test",
        "auto_build": True,
        "auto_test": True,
        "prod_url": "https://myawesomeapp.com",
        "prod_api_key": "",
        "prod_enabled": True,
        "staging_url": "https://staging.myawesomeapp.com",
        "staging_api_key": "",
        "staging_enabled": True,
    }

    dialog = FormDialog(
        master=parent,
        title="Project Settings - Nested Groups",
        data=initial_data,
        items=items,
        col_count=1,
        min_col_width=400,
        height=600,
    )
    dialog.show()

    if dialog.result:
        print("Nested groups result:", dialog.result)
        ttk.Toast(
            title="Project Settings Saved",
            message=f"Configuration for '{dialog.result['project_name']}' has been saved",
            duration=3000,
            bootstyle="success",
        ).show()


def demo_mixed_layout(parent):
    """Form mixing groups with ungrouped fields."""
    items = [
        FieldItem(key="order_id", label="Order ID"),
        FieldItem(key="order_date", label="Order Date", dtype="date"),
        GroupItem(
            label="Customer Information",
            col_count=2,
            items=[
                FieldItem(key="customer_name", label="Name", columnspan=2),
                FieldItem(key="customer_email", label="Email"),
                FieldItem(key="customer_phone", label="Phone"),
            ],
        ),
        GroupItem(
            label="Shipping Address",
            col_count=1,
            items=[
                FieldItem(key="ship_street", label="Street"),
                FieldItem(key="ship_city", label="City"),
                FieldItem(key="ship_state", label="State"),
                FieldItem(key="ship_zip", label="ZIP Code"),
            ],
        ),
        GroupItem(
            label="Order Details",
            col_count=2,
            items=[
                FieldItem(key="product", label="Product", columnspan=2),
                FieldItem(key="quantity", label="Quantity", dtype="int"),
                FieldItem(key="unit_price", label="Unit Price", dtype="float"),
                FieldItem(key="tax", label="Tax Rate (%)", dtype="float"),
                FieldItem(key="discount", label="Discount (%)", dtype="float"),
            ],
        ),
        FieldItem(key="notes", label="Order Notes", editor="text",
                 editor_options={"height": 3}),
        FieldItem(key="rush_order", label="Rush Order", dtype=bool, editor="checkbutton"),
    ]

    initial_data = {
        "order_id": "ORD-2024-001",
        "order_date": date.today(),
        "customer_name": "Jane Smith",
        "customer_email": "jane.smith@example.com",
        "customer_phone": "555-1234",
        "ship_street": "456 Oak Avenue",
        "ship_city": "Portland",
        "ship_state": "OR",
        "ship_zip": "97201",
        "product": "Deluxe Widget Set",
        "quantity": 3,
        "unit_price": 49.99,
        "tax": 8.5,
        "discount": 10.0,
        "notes": "Please handle with care",
        "rush_order": False,
    }

    dialog = FormDialog(
        master=parent,
        title="Order Entry - Mixed Layout",
        data=initial_data,
        items=items,
        col_count=1,
        min_col_width=350,
        height=550,
    )
    dialog.show()

    if dialog.result:
        print("Mixed layout result:", dialog.result)
        total = dialog.result['quantity'] * dialog.result['unit_price']
        total_with_tax = total * (1 + dialog.result['tax'] / 100)
        total_final = total_with_tax * (1 - dialog.result['discount'] / 100)
        ttk.Toast(
            title="Order Submitted",
            message=f"Order {dialog.result['order_id']} total: ${total_final:.2f}",
            duration=3000,
            bootstyle="success",
        ).show()


def main():
    app = ttk.Window(title="Grouped Form Demo", theme="flatly", size=(650, 500))

    # Title
    title = ttk.Label(
        app,
        text="Grouped Form Examples",
        font=("TkDefaultFont", 18, "bold"),
    )
    title.pack(pady=20)

    # Description
    desc = ttk.Label(
        app,
        text="Explore different GroupItem layouts and configurations",
        font=("TkDefaultFont", 11),
        color="secondary",
    )
    desc.pack(pady=(0, 10))

    # Separator
    ttk.Separator(app, orient=HORIZONTAL).pack(fill=X, padx=40, pady=15)

    # Button container with grid layout
    button_frame = ttk.Frame(app)
    button_frame.pack(expand=True, pady=20)

    # Demo buttons in a grid
    demos = [
        ("Basic Groups", demo_basic_groups, "primary",
         "Multiple groups in a single form"),
        ("Multi-Column Groups", demo_multicolumn_groups, "info",
         "Groups with 2-3 column layouts"),
        ("Nested Groups", demo_nested_groups, "success",
         "Groups within groups for hierarchy"),
        ("Mixed Layout", demo_mixed_layout, "warning",
         "Combination of groups and standalone fields"),
    ]

    for i, (text, command, style, tooltip) in enumerate(demos):
        btn_container = ttk.Frame(button_frame)
        btn_container.pack(pady=6, fill=X, padx=30)

        btn = ttk.Button(
            btn_container,
            text=text,
            command=lambda cmd=command: cmd(app),
            color=style,
            width=28,
        )
        btn.pack(side=LEFT)

        desc_label = ttk.Label(
            btn_container,
            text=f"  —  {tooltip}",
            font=("TkDefaultFont", 9),
            color="secondary",
        )
        desc_label.pack(side=LEFT, padx=(10, 0))

    # Separator
    ttk.Separator(app, orient=HORIZONTAL).pack(fill=X, padx=40, pady=20)

    # Exit button
    ttk.Button(
        app,
        text="Exit Demo",
        command=app.destroy,
        color="secondary",
        variant="outline",
        width=20,
    ).pack(pady=(0, 20))

    app.mainloop()


if __name__ == "__main__":
    main()
