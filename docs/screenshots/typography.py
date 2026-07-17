"""Screenshot scenes for docs/user-guide/feature-guides/typography.rst."""

import ttkbootstrap as ttk


def _sample(app):
    frm = ttk.Frame(app, padding=20)
    frm.pack()
    ttk.Label(frm, text="Quarterly report", font="TkHeadingFont").pack(anchor="w")
    ttk.Label(frm, text="Revenue rose 12% this quarter.").pack(anchor="w", pady=(4, 8))
    ttk.Button(frm, text="Save", bootstyle="primary").pack(anchor="w")
    app.mainloop()


def default():
    _sample(ttk.App(title="Typography"))


def custom():
    # A visibly different family so the restyle reads at a glance (Segoe UI, the
    # Windows default, would look identical). Rides the deferred-config seam.
    ttk.set_global_family("Georgia")
    _sample(ttk.App(title="Typography"))


def scale():
    app = ttk.App(title="Type scale")
    card = ttk.Frame(app, bootstyle="@card", padding=16)
    card.pack(padx=20, pady=20)
    ttk.Label(card, text="Heading", font="TkHeadingFont", bootstyle="@card").pack(anchor="w")
    ttk.Label(card, text="Body text sits at the default size.", bootstyle="@card").pack(
        anchor="w", pady=4)
    ttk.Label(card, text="CAPTION", font="-size 9", bootstyle="@card secondary").pack(anchor="w")
    app.mainloop()


SCENES = {
    "default": default,
    "custom": custom,
    "scale": scale,
}
