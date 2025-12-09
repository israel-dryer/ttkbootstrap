"""
AppConfig Demo - Demonstrates global configuration management

This example shows how to use AppConfig to set global preferences for your
ttkbootstrap application, including theme, window properties, and more.
"""

import ttkbootstrap as ttk
from ttkbootstrap import AppConfig


def example1_basic_usage():
    """Example 1: Basic AppConfig usage with theme and window size."""
    print("Example 1: Basic AppConfig Usage")
    print("-" * 50)

    # Set global configuration
    AppConfig.set(
        theme="darkly",
        window_size=(800, 600),
        window_position=(100, 100)
    )

    # Show what's been configured
    print("Configuration set:")
    print(f"  Theme: {AppConfig.get('theme')}")
    print(f"  Window size: {AppConfig.get('window_size')}")
    print(f"  Window position: {AppConfig.get('window_position')}")
    print()

    # Create window - it will automatically use AppConfig defaults
    root = ttk.Window()

    # Add some widgets to demonstrate the theme
    ttk.Label(
        root,
        text="This window uses AppConfig defaults",
        font=("Helvetica", 14)
    ).pack(padx=20, pady=20)

    ttk.Button(
        root,
        text="Primary Button",
        bootstyle="primary"
    ).pack(padx=20, pady=5)

    ttk.Button(
        root,
        text="Success Button",
        bootstyle="success"
    ).pack(padx=20, pady=5)

    ttk.Button(
        root,
        text="Close",
        bootstyle="danger",
        command=root.destroy
    ).pack(padx=20, pady=5)

    root.mainloop()


def example2_override_defaults():
    """Example 2: Overriding AppConfig defaults."""
    print("Example 2: Overriding AppConfig Defaults")
    print("-" * 50)

    # Set global configuration
    AppConfig.set(
        theme="cosmo",
        window_size=(600, 400),
        window_alpha=0.95
    )

    print("Global configuration:")
    print(f"  Theme: {AppConfig.get('theme')}")
    print(f"  Window size: {AppConfig.get('window_size')}")
    print(f"  Window alpha: {AppConfig.get('window_alpha')}")
    print()

    # Create first window using defaults
    root = ttk.Window(title="Window 1 (Uses Defaults)")
    ttk.Label(
        root,
        text="This window uses AppConfig defaults",
        font=("Helvetica", 12)
    ).pack(padx=20, pady=20)

    # Create second window with explicit overrides
    window2 = ttk.Window(
        title="Window 2 (Overrides Defaults)",
        theme="superhero",  # Override theme
        size=(400, 300),        # Override size
        position=(200, 200)     # Explicit position
    )
    ttk.Label(
        window2,
        text="This window overrides the defaults",
        font=("Helvetica", 12)
    ).pack(padx=20, pady=20)

    ttk.Button(
        root,
        text="Close All",
        command=root.quit
    ).pack(pady=10)

    root.mainloop()


def example3_all_config_options():
    """Example 3: Demonstrating all AppConfig options."""
    print("Example 3: All AppConfig Options")
    print("-" * 50)

    # Set comprehensive configuration
    AppConfig.set(
        # Theme & Styling
        theme="flatly",
        font=("Segoe UI", 11),

        # Window Defaults
        window_size=(900, 700),
        window_minsize=(400, 300),
        window_maxsize=(1200, 900),
        window_resizable=(True, True),
        window_scaling=1.0,
        window_hdpi=True,
        window_alpha=0.98,

        # Icons & Assets
        icons="bootstrap",

        # Localization
        language="en",
        date_format="%Y-%m-%d"
    )

    # Display all configuration
    print("All configuration settings:")
    all_config = AppConfig.get_all()
    for key, value in sorted(all_config.items()):
        print(f"  {key}: {value}")
    print()

    # Create window with these defaults
    root = ttk.Window(title="Comprehensive AppConfig Demo")

    # Create a frame with all the config info
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Current AppConfig Settings",
        font=("Helvetica", 14, "bold")
    ).pack(pady=(0, 10))

    # Create text widget to show configuration
    text = ttk.Text(frame, height=20, width=60)
    text.pack(fill="both", expand=True, pady=(0, 10))

    # Add configuration to text widget
    for key, value in sorted(all_config.items()):
        text.insert("end", f"{key}: {value}\n")

    text.configure(state="disabled")  # Make read-only

    # Add buttons
    button_frame = ttk.Frame(frame)
    button_frame.pack()

    ttk.Button(
        button_frame,
        text="Reset Config",
        bootstyle="warning",
        command=lambda: reset_and_update(text)
    ).pack(side="left", padx=5)

    ttk.Button(
        button_frame,
        text="Close",
        bootstyle="danger",
        command=root.destroy
    ).pack(side="left", padx=5)

    def reset_and_update(text_widget):
        """Reset configuration and update display."""
        AppConfig.reset()
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("end", "Configuration has been reset!\n")
        text_widget.insert("end", "All values are now at defaults (None).\n")
        text_widget.configure(state="disabled")

    root.mainloop()


def example4_check_and_get():
    """Example 4: Using has() and get() methods."""
    print("Example 4: Checking and Getting Configuration")
    print("-" * 50)

    # Reset first to start clean
    AppConfig.reset()

    # Set only some configuration
    AppConfig.set(
        theme="darkly",
        window_size=(700, 500)
    )

    # Check what's configured
    print("Checking configuration with has():")
    print(f"  Has theme? {AppConfig.has('theme')}")
    print(f"  Has window_size? {AppConfig.has('window_size')}")
    print(f"  Has window_alpha? {AppConfig.has('window_alpha')}")
    print()

    # Get values with defaults
    print("Getting values with defaults:")
    print(f"  Theme: {AppConfig.get('theme', 'cosmo')}")
    print(f"  Window size: {AppConfig.get('window_size', (800, 600))}")
    print(f"  Window alpha: {AppConfig.get('window_alpha', 1.0)}")
    print()

    # Create window
    root = ttk.Window(title="Check and Get Demo")

    info_text = f"""Configuration Check Results:

Theme is set: {AppConfig.has('theme')}
Window size is set: {AppConfig.has('window_size')}
Window alpha is set: {AppConfig.has('window_alpha')}

Actual values:
Theme: {AppConfig.get('theme', 'not set')}
Window size: {AppConfig.get('window_size', 'not set')}
Window alpha: {AppConfig.get('window_alpha', 'not set')}
"""

    ttk.Label(
        root,
        text=info_text,
        justify="left",
        font=("Courier", 10)
    ).pack(padx=20, pady=20)

    ttk.Button(
        root,
        text="Close",
        command=root.destroy
    ).pack(pady=10)

    root.mainloop()


def main():
    """Run selected example."""
    print("\n" + "=" * 50)
    print("AppConfig Demo Examples")
    print("=" * 50)
    print("\nAvailable examples:")
    print("1. Basic Usage")
    print("2. Override Defaults")
    print("3. All Config Options")
    print("4. Check and Get Methods")
    print("\nUncomment the example you want to run in main()")
    print("=" * 50 + "\n")

    # Run example 1 by default
    # Uncomment the example you want to run:

    example1_basic_usage()
    # example2_override_defaults()
    # example3_all_config_options()
    # example4_check_and_get()


if __name__ == "__main__":
    main()
