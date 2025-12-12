"""Basic usage of ttkbootstrap.signals.Signal without visible UI.

Demonstrates:
- Creating a Signal
- Subscribing (with immediate fire)
- Setting values and observing callbacks
- Derived signals with map()
- Unsubscribing
"""

import time
import tkinter as tk

from ttkbootstrap.core.signals import Signal


def main() -> None:
    # Create a hidden Tk interpreter for tk.Variable support
    root = tk.Tk()
    root.withdraw()

    counter = Signal(0)

    def on_change(v: int) -> None:
        print(f"counter changed -> {v}")

    # Fire immediately with current value
    counter.subscribe(on_change, immediate=True)

    # Derived signal that doubles the value
    doubled = counter.map(lambda x: x * 2)
    doubled.subscribe(lambda v: print(f"doubled -> {v}"), immediate=True)

    # Update values
    for i in range(1, 4):
        counter.set(i)
        # Process Tk events to flush traces in some environments
        root.update_idletasks()
        time.sleep(0.05)

    # Unsubscribe the original callback
    counter.unsubscribe(on_change)
    counter.set(99)  # will not print from on_change, only from doubled
    root.update_idletasks()

    root.destroy()


if __name__ == "__main__":
    main()

