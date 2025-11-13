"""Wrapping an existing tk.Variable and demonstrating multi-subscribe.

Shows:
- Signal.from_variable wrapping a tk.IntVar
- Multiple subscriptions (same callback twice) and trace ids
- Interop: updating via tk_var.set and via Signal.set
- Unsubscribing by callback removes all its subscriptions
"""

import time
import tkinter as tk

from ttkbootstrap.signals import Signal


def main() -> None:
    root = tk.Tk()
    root.withdraw()

    tk_var = tk.IntVar(value=5)
    sig = Signal.from_variable(tk_var)

    def cb_a(v: int) -> None:
        print(f"A -> {v}")

    def cb_b(v: int) -> None:
        print(f"B -> {v}")

    # Subscribe same callback twice to demonstrate multiple fids
    fid1 = sig.subscribe(cb_a, immediate=True)  # prints 5
    fid2 = sig.subscribe(cb_a)                  # no immediate print

    # Also another distinct callback
    sig.subscribe(cb_b, immediate=True)         # prints 5

    print(f"cb_a fids: {fid1}, {fid2}")

    # Update via tk_var; Signal subscriptions should fire
    tk_var.set(6)  # A prints twice, B once
    root.update_idletasks(); time.sleep(0.05)

    # Update via Signal; tk_var stays in sync
    sig.set(7)     # A prints twice, B once
    root.update_idletasks(); time.sleep(0.05)

    # Unsubscribe all cb_a subscriptions by callback
    sig.unsubscribe(cb_a)
    sig.set(8)     # Only B prints
    root.update_idletasks(); time.sleep(0.05)

    # Clear remaining
    sig.unsubscribe_all()
    sig.set(9)     # no output
    root.update_idletasks(); time.sleep(0.05)

    root.destroy()


if __name__ == "__main__":
    main()

