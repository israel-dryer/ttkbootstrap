"""
Grid Comparison Demo

Demonstrates the difference between building a complex grid layout with:
1. Regular Frame + manual grid configuration
2. GridFrame with declarative configuration

Both produce the same visual result, but GridFrame requires less boilerplate.
"""

import ttkbootstrap as ttk


def create_with_frame(parent: ttk.Frame) -> ttk.Frame:
    """Build a form layout using regular Frame with manual grid calls."""

    frame = ttk.Frame(parent, padding=20)

    # Manual column configuration
    frame.columnconfigure(0, weight=0, minsize=100)  # Labels column
    frame.columnconfigure(1, weight=1, minsize=200)  # Inputs column
    frame.columnconfigure(2, weight=0, minsize=80)   # Actions column

    # Manual row configuration
    for i in range(7):
        frame.rowconfigure(i, weight=0, pad=6)

    # Header - manual row/column/sticky/columnspan
    header = ttk.Label(frame, text="User Registration", font=("", 14, "bold"))
    header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

    # Row 1: Username
    ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky="e", padx=(0, 10))
    username = ttk.Entry(frame)
    username.grid(row=1, column=1, sticky="ew")
    ttk.Button(frame, text="Check", color="info", variant="outline").grid(row=1, column=2, sticky="ew", padx=(10, 0))

    # Row 2: Email
    ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky="e", padx=(0, 10))
    email = ttk.Entry(frame)
    email.grid(row=2, column=1, sticky="ew")
    ttk.Button(frame, text="Verify", color="info", variant="outline").grid(row=2, column=2, sticky="ew", padx=(10, 0))

    # Row 3: Password
    ttk.Label(frame, text="Password:").grid(row=3, column=0, sticky="e", padx=(0, 10))
    password = ttk.Entry(frame, show="*")
    password.grid(row=3, column=1, columnspan=2, sticky="ew")

    # Row 4: Confirm Password
    ttk.Label(frame, text="Confirm:").grid(row=4, column=0, sticky="e", padx=(0, 10))
    confirm = ttk.Entry(frame, show="*")
    confirm.grid(row=4, column=1, columnspan=2, sticky="ew")

    # Row 5: Options (checkbuttons)
    ttk.Label(frame, text="Options:").grid(row=5, column=0, sticky="ne", padx=(0, 10), pady=(5, 0))

    options_frame = ttk.Frame(frame)
    options_frame.grid(row=5, column=1, columnspan=2, sticky="w")
    ttk.CheckButton(options_frame, text="Subscribe to newsletter").pack(anchor="w")
    ttk.CheckButton(options_frame, text="Accept terms and conditions").pack(anchor="w")

    # Row 6: Buttons
    buttons_frame = ttk.Frame(frame)
    buttons_frame.grid(row=6, column=0, columnspan=3, sticky="e", pady=(15, 0))
    ttk.Button(buttons_frame, text="Cancel", color="secondary").pack(side="left", padx=(0, 10))
    ttk.Button(buttons_frame, text="Register", color="primary").pack(side="left")

    return frame


def create_with_gridframe(parent: ttk.Frame) -> ttk.GridFrame:
    """Build the same form layout using GridFrame with declarative config."""

    # Declare structure upfront: label column (100px min), input column (flex), action column (80px min)
    # sticky_items="ew" applies to all children by default
    # gap=(10, 6) provides consistent spacing automatically
    grid = ttk.GridFrame(
        parent,
        columns=["100px", 1, "80px"],  # minsize for cols 0 and 2, weight=1 for col 1
        gap=(10, 6),
        padding=20,
        sticky_items="ew",  # Default sticky for all children
    )

    # Header - use grid() with overrides
    ttk.Label(grid, text="User Registration", font=("", 14, "bold")).grid(
        row=0, column=0, columnspan=3, sticky="w", pady=(0, 10)
    )

    # Row 1: Username
    ttk.Label(grid, text="Username:").grid(row=1, column=0, sticky="e")
    ttk.Entry(grid).grid(row=1, column=1)  # Uses default "ew"
    ttk.Button(grid, text="Check", color="info", variant="outline").grid(row=1, column=2)

    # Row 2: Email
    ttk.Label(grid, text="Email:").grid(row=2, column=0, sticky="e")
    ttk.Entry(grid).grid(row=2, column=1)
    ttk.Button(grid, text="Verify", color="info", variant="outline").grid(row=2, column=2)

    # Row 3: Password
    ttk.Label(grid, text="Password:").grid(row=3, column=0, sticky="e")
    ttk.Entry(grid, show="*").grid(row=3, column=1, columnspan=2)

    # Row 4: Confirm Password
    ttk.Label(grid, text="Confirm:").grid(row=4, column=0, sticky="e")
    ttk.Entry(grid, show="*").grid(row=4, column=1, columnspan=2)

    # Row 5: Options
    ttk.Label(grid, text="Options:").grid(row=5, column=0, sticky="ne", pady=(5, 0))

    options = ttk.Frame(grid)  # Use plain Frame like the other example
    options.grid(row=5, column=1, columnspan=2, sticky="w")
    ttk.CheckButton(options, text="Subscribe to newsletter").pack(anchor="w")
    ttk.CheckButton(options, text="Accept terms and conditions").pack(anchor="w")

    # Row 6: Buttons
    buttons = ttk.Frame(grid)  # Use plain Frame like the other example
    buttons.grid(row=6, column=0, columnspan=3, sticky="e", pady=(15, 0))
    ttk.Button(buttons, text="Cancel", color="secondary").pack(side="left", padx=(0, 10))
    ttk.Button(buttons, text="Register", color="primary").pack(side="left")

    return grid


def main():
    app = ttk.App(title="Grid Comparison Demo", theme="cosmo", size=(900, 500))

    # Create a notebook to show both approaches side by side
    notebook = ttk.Notebook(app)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Tab 1: Regular Frame approach
    frame_tab = notebook.add(text="Frame + grid()", key="frame", padding=10)

    info1 = ttk.Label(
        frame_tab,
        text="Using regular Frame requires manual columnconfigure/rowconfigure calls,\n"
             "plus explicit padx/pady on each widget for consistent spacing.",
        foreground="gray",
    )
    info1.pack(anchor="w", pady=(0, 10))

    frame_example = create_with_frame(frame_tab)
    frame_example.pack(fill="both", expand=True)

    # Tab 2: GridFrame approach
    gridframe_tab = notebook.add(text="GridFrame", key="gridframe", padding=10)

    info2 = ttk.Label(
        gridframe_tab,
        text="Using GridFrame with grid(), column weights are declared upfront with columns=[...],\n"
             "gap=(10, 6) provides spacing, and sticky_items='ew' sets default alignment.",
        foreground="gray",
    )
    info2.pack(anchor="w", pady=(0, 10))

    gridframe_example = create_with_gridframe(gridframe_tab)
    gridframe_example.pack(fill="both", expand=True)

    # Code comparison panel at the bottom
    comparison = ttk.LabelFrame(app, text="Code Comparison", padding=10)
    comparison.pack(fill="x", padx=10, pady=(0, 10))

    comparison_text = ttk.Label(
        comparison,
        text=(
            "Frame + .grid(): columnconfigure(0, weight=0, minsize=100) × 3 columns\n"
            "                 rowconfigure(i, weight=0, pad=6) × 7 rows\n"
            "                 padx=(0, 10) + sticky='ew' on each widget\n\n"
            "GridFrame:       columns=['100px', 1, '80px'], gap=(10, 6), sticky_items='ew'\n"
            "                 Minsizes, weights, spacing, and sticky declared once."
        ),
        font=("Consolas", 9),
        justify="left",
    )
    comparison_text.pack(anchor="w")

    app.mainloop()


if __name__ == "__main__":
    main()
