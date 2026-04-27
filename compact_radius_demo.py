"""Quick demo to visually inspect compact input corner radius.

Shows compact-density inputs side by side with default-density inputs
so the corner radius difference can be compared at a glance.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def main():
    app = ttk.App(title="Compact Radius Check", size=(700, 480))

    outer = ttk.Frame(app, padding=24)
    outer.pack(fill=BOTH, expand=YES)

    # -- Column headers -------------------------------------------------------
    ttk.Label(outer, text="Default", font="heading[bold]").grid(
        row=0, column=0, sticky=W, padx=(0, 40), pady=(0, 12))
    ttk.Label(outer, text="Compact", font="heading[bold]").grid(
        row=0, column=1, sticky=W, pady=(0, 12))

    widgets = [
        ("Text Entry",     ttk.TextEntry,    dict(label="Full Name", value="Jane Doe")),
        ("Numeric Entry",  ttk.NumericEntry, dict(label="Age", value=34, show_spin_buttons=True)),
        ("Password Entry", ttk.PasswordEntry, dict(label="Password")),
        ("Spinner Entry",  ttk.SpinnerEntry,  dict(label="Role", values=["Admin", "User", "Guest"])),
    ]

    for row, (_, cls, kw) in enumerate(widgets, start=1):
        cls(outer, **kw, density="default").grid(
            row=row, column=0, sticky=EW, padx=(0, 40), pady=6)
        cls(outer, **kw, density="compact").grid(
            row=row, column=1, sticky=EW, pady=6)

    outer.columnconfigure(0, weight=1)
    outer.columnconfigure(1, weight=1)

    app.mainloop()


if __name__ == "__main__":
    main()