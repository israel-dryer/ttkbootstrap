"""Screenshot scenes for docs/user-guide/foundations/layout-with-grid.rst."""

import ttkbootstrap as ttk


def sticky():
    # Step 2 state: labels pinned west, entries stretched east-west (no padding
    # yet — Step 3 adds it).
    app = ttk.App(title="Sign in", size=(300, 110))
    form = ttk.Frame(app, padding=20)
    form.pack(fill="both", expand=True)
    form.columnconfigure(1, weight=1)

    ttk.Label(form, text="Email").grid(row=0, column=0, sticky="w")
    ttk.Entry(form).grid(row=0, column=1, sticky="ew")
    ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w")
    ttk.Entry(form).grid(row=1, column=1, sticky="ew")
    app._capture_full_window = True  # layout shown at the app level
    app.mainloop()


def _finished(app):
    form = ttk.Frame(app, padding=20)
    form.pack(fill="both", expand=True)
    form.columnconfigure(1, weight=1)

    ttk.Label(form, text="Email").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    ttk.Entry(form).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    ttk.Entry(form, show="•").grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    ttk.Button(form, text="Sign in", bootstyle="primary").grid(
        row=2, column=0, columnspan=2, sticky="e", padx=5, pady=(10, 0))
    app._capture_full_window = True  # layout shown at the app level
    app.mainloop()


def narrow():
    _finished(ttk.App(title="Sign in", size=(260, 150)))


def wide():
    _finished(ttk.App(title="Sign in", size=(440, 150)))


SCENES = {
    "sticky": sticky,
    "narrow": narrow,
    "wide": wide,
}
