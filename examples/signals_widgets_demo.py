"""Using Signal with ttkbootstrap widgets.

Demonstrates binding a Signal to widget textvariables and reacting to
changes with a subscriber.
"""

import ttkbootstrap as ttk
from ttkbootstrap.signals import Signal
from ttkbootstrap.signals.integration import enable_widget_integration


def main() -> None:
    app = ttk.Window(title="Signals + Widgets Demo", themename="flatly")
    # Ensure Signals can be passed directly to textvariable/variable
    enable_widget_integration()

    sig = Signal("")

    ttk.Label(app, text="Your name:").pack(padx=10, pady=(10, 4), anchor="w")
    ttk.Entry(app, textvariable=sig, width=30).pack(padx=10, pady=(0, 10), fill="x")

    output = ttk.Label(app, text="Hello!")
    output.pack(padx=10, pady=(0, 10), anchor="w")

    # Update label whenever name changes; fire once immediately
    sig.subscribe(lambda v: output.configure(text=f"Hello, {v or '...'}!"), immediate=True)

    # Demonstrate map(): uppercase view of name
    upper = sig.map(lambda s: s.upper())
    ttk.Label(app, text="Uppercase:").pack(padx=10, pady=(10, 4), anchor="w")
    ttk.Entry(app, textvariable=upper, width=30, state="readonly").pack(padx=10, pady=(0, 10), fill="x")

    app.mainloop()


if __name__ == "__main__":
    main()
