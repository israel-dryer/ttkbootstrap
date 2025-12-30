"""Demo for the inline Calendar widget."""

from datetime import date

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, W, X
from ttkbootstrap import Calendar


def main():
    app = ttk.Window(title="Calendar Demo", theme="light")

    picker = Calendar(app, start_date=date.today(), selection_mode="range")
    picker.pack(fill=BOTH, expand=True)

    picker.on_date_selected(print)

    app.mainloop()


if __name__ == "__main__":
    main()