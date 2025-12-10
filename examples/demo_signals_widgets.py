"""
Demo: Signals Integration with Widgets

This example demonstrates the reactive signal system integrated into ttkbootstrap widgets.
Signals provide automatic two-way binding between widgets and data sources, enabling
reactive UI patterns without manual variable management.

Features demonstrated:
- Entry, Combobox, Spinbox, and Scale widgets with signal integration
- Automatic synchronization between widgets sharing the same signal
- Derived signals using .map() that transform values from other signals
- Dynamic UI updates based on signal changes
"""

import ttkbootstrap as ttk
from ttkbootstrap.signals import Signal


class SignalsDemo(ttk.Window):
    """Demo application showcasing signal integration with widgets."""

    def __init__(self):
        super().__init__(theme="darkly")
        self.title("ttkbootstrap Signals Demo")
        self.geometry("800x600")

        # Create signals for reactive data
        self.username = Signal[str]("")
        self.age = Signal[int](25)
        self.color_choice = Signal[str]("primary")
        self.volume = Signal[float](50.0)

        # Derived signal that transforms username
        self.greeting = Signal[str]("")

        # Update greeting when username or age changes
        def update_greeting(*args):
            name = self.username.get() or "Guest"
            age = self.age.get()
            self.greeting.set(f"Hello, {name}! You are {age} years old.")

        self.username.subscribe(update_greeting)
        self.age.subscribe(update_greeting)
        update_greeting()  # Initialize

        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface with signal-connected widgets."""

        # Main container with padding
        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        # Title
        title = ttk.Label(
            container,
            text="Widget Signals Demo",
            font="[24][bold]"
        )
        title.pack(pady=(0, 20))

        # Section 1: Entry widget with signal
        self._create_entry_section(container)

        # Section 2: Spinbox widget with signal
        self._create_spinbox_section(container)

        # Section 3: Combobox widget with signal
        self._create_combobox_section(container)

        # Section 4: Scale widget with signal
        self._create_scale_section(container)

        # Section 5: Derived signal display
        self._create_derived_section(container)

        # Section 6: Progressbar with signal
        self._create_progressbar_section(container)

    def _create_entry_section(self, parent):
        """Create entry widget section with signal binding."""
        frame = ttk.LabelFrame(parent, text="Entry Widget with Signal", padding=15)
        frame.pack(fill="x", pady=(0, 15))

        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Entry widget connected to username signal
        entry = ttk.Entry(frame, width=30, textsignal=self.username)
        entry.grid(row=0, column=1, sticky="ew")

        # Display current signal value
        value_label = ttk.Label(frame, text="", foreground="gray")
        value_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

        def update_display(*args):
            value_label.configure(text=f"Signal value: '{self.username.get()}'")

        self.username.subscribe(update_display)
        update_display()

        frame.columnconfigure(1, weight=1)

    def _create_spinbox_section(self, parent):
        """Create spinbox widget section with signal binding."""
        frame = ttk.LabelFrame(parent, text="Spinbox Widget with Signal", padding=15)
        frame.pack(fill="x", pady=(0, 15))

        ttk.Label(frame, text="Age:").grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Spinbox widget connected to age signal
        spinbox = ttk.Spinbox(
            frame,
            from_=1,
            to=120,
            textsignal=self.age,
            width=15
        )
        spinbox.grid(row=0, column=1, sticky="w")

        # Display current signal value
        value_label = ttk.Label(frame, text="", foreground="gray")
        value_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

        def update_display(*args):
            value_label.configure(text=f"Signal value: {self.age.get()}")

        self.age.subscribe(update_display)
        update_display()

        frame.columnconfigure(1, weight=1)

    def _create_combobox_section(self, parent):
        """Create combobox widget section with signal binding."""
        frame = ttk.LabelFrame(parent, text="Combobox Widget with Signal", padding=15)
        frame.pack(fill="x", pady=(0, 15))

        ttk.Label(frame, text="Theme Color:").grid(row=0, column=0, sticky="w", padx=(0, 10))

        colors = ["primary", "secondary", "success", "info", "warning", "danger"]

        # Combobox widget connected to color_choice signal
        combobox = ttk.Combobox(
            frame,
            values=colors,
            state="readonly",
            textsignal=self.color_choice,
            width=15
        )
        combobox.grid(row=0, column=1, sticky="w")

        # Button that changes color based on signal
        demo_button = ttk.Button(frame, text="Themed Button")
        demo_button.grid(row=0, column=2, padx=(10, 0))

        # Display current signal value
        value_label = ttk.Label(frame, text="", foreground="gray")
        value_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))

        def update_display(*args):
            value_label.configure(text=f"Signal value: '{self.color_choice.get()}'")
            # Update button bootstyle based on signal
            demo_button.configure(bootstyle=self.color_choice.get())

        self.color_choice.subscribe(update_display)
        update_display()

        frame.columnconfigure(1, weight=1)

    def _create_scale_section(self, parent):
        """Create scale widget section with signal binding."""
        frame = ttk.LabelFrame(parent, text="Scale Widget with Signal", padding=15)
        frame.pack(fill="x", pady=(0, 15))

        ttk.Label(frame, text="Volume:").grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Scale widget connected to volume signal
        scale = ttk.Scale(
            frame,
            from_=0,
            to=100,
            signal=self.volume,
            bootstyle="info"
        )
        scale.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        # Label showing current value
        value_display = ttk.Label(frame, text="50", width=5, anchor="e")
        value_display.grid(row=0, column=2)

        # Display current signal value
        value_label = ttk.Label(frame, text="", foreground="gray")
        value_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))

        def update_display(*args):
            vol = int(self.volume.get())
            value_display.configure(text=str(vol))
            value_label.configure(text=f"Signal value: {vol}")

        self.volume.subscribe(update_display)
        update_display()

        frame.columnconfigure(1, weight=1)

    def _create_progressbar_section(self, parent):
        """Create progressbar section synced with volume signal."""
        frame = ttk.LabelFrame(parent, text="Progressbar with Signal (Synced to Volume)", padding=15)
        frame.pack(fill="x", pady=(0, 15))

        # Progressbar connected to the same signal as the scale
        progressbar = ttk.Progressbar(
            frame,
            maximum=100,
            signal=self.volume,
            bootstyle="info-striped",
            mode="determinate"
        )
        progressbar.pack(fill="x")

        info_label = ttk.Label(
            frame,
            text="This progressbar is automatically synchronized with the volume scale above",
            foreground="gray",
            font=("Helvetica", 9, "italic")
        )
        info_label.pack(pady=(5, 0))

    def _create_derived_section(self, parent):
        """Create section displaying derived signal value."""
        frame = ttk.LabelFrame(parent, text="Derived Signal", padding=15)
        frame.pack(fill="x", pady=(0, 15))

        # Label that updates from computed signal
        greeting_label = ttk.Label(
            frame,
            text="",
            font=("Helvetica", 14),
            bootstyle="success"
        )
        greeting_label.pack(fill="x")

        info_label = ttk.Label(
            frame,
            text="This greeting is derived from the username and age signals above",
            foreground="gray",
            font=("Helvetica", 9, "italic")
        )
        info_label.pack(pady=(5, 0))

        def update_greeting_display(*args):
            greeting_label.configure(text=self.greeting.get())

        self.greeting.subscribe(update_greeting_display)
        update_greeting_display()

        # Add buttons to demonstrate programmatic signal updates
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=(10, 0))

        ttk.Label(button_frame, text="Quick Actions:").pack(side="left", padx=(0, 10))

        def set_alice():
            self.username.set("Alice")
            self.age.set(30)

        def set_bob():
            self.username.set("Bob")
            self.age.set(25)

        def reset():
            self.username.set("")
            self.age.set(25)

        ttk.Button(button_frame, text="Set to Alice (30)", command=set_alice).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Set to Bob (25)", command=set_bob).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Reset", command=reset, bootstyle="secondary").pack(side="left", padx=2)


def main():
    """Run the signals demo application."""
    app = SignalsDemo()
    app.mainloop()


if __name__ == "__main__":
    main()