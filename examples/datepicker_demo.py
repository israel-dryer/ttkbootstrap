"""Demo for the inline Calendar widget."""

from datetime import date

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, W, X
from ttkbootstrap import Calendar


def main():
    app = ttk.Window(title="Calendar Demo", theme="dark")

    picker = Calendar(app, start_date=date.today(), bootstyle="success", selection_mode="range")
    picker.pack(fill=BOTH, expand=True)

    picker.on_date_selected(print)

    # output = ttk.Label(app, text=f"Selected: {picker.date.isoformat()}", bootstyle="secondary")
    # output.pack(fill=X, padx=14, pady=(0, 10))

    # def on_pick(event):
    #     output.configure(text=f"Selected: {event.data['date'].isoformat()}")

    # picker.on_date_selected(on_pick)
    #
    # ttk.Button(
    #     app,
    #     text="Reset to Today",
    #     bootstyle="secondary",
    #     command=lambda: picker.set_date(date.today())
    # ).pack(padx=14, pady=(0, 14))

    app.mainloop()


if __name__ == "__main__":
    main()