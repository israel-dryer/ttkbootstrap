"""Surface-color preview (2.0 surface-color).

A visual spot-check for the `@<surface>` bootstyle token: the same controls on
the application background vs. on accent-colored surfaces. Each accent panel is a
producing frame (`bootstyle="<accent>"`); the controls on it carry the matching
`@<accent>` surface token so their flat backgrounds, off-indicators, and text
read against the panel instead of the app background.

Toggle light/dark (top-right) to confirm every surfaced style repaints.

Run:  python examples/surface_preview.py
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


ACCENTS = ("primary", "success", "danger", "dark")


def build_controls(parent, surface):
    """Fill `parent` with one of each family. `surface` is "" or an accent token.

    On an accent panel the controls use a *light* accent so the indicator glyphs
    and ghost fill stay legible against the panel (a `@primary primary` control
    would render accent-on-accent -- the user's call, but not a useful preview).
    """
    at = f"@{surface} " if surface else ""       # surface prefix
    color = "light " if surface else ""          # legible-on-accent accent
    ttk.Label(parent, text=f"surface: {surface or 'background'}",
              bootstyle=f"{at}{color}".strip() or None).pack(anchor=W, pady=(0, 8))
    ttk.Checkbutton(parent, text="Checkbutton", bootstyle=f"{at}{color}".strip()
                    ).pack(anchor=W, pady=2)
    ttk.Radiobutton(parent, text="Radiobutton", value=1,
                    bootstyle=f"{at}{color}".strip()).pack(anchor=W, pady=2)
    ttk.Checkbutton(parent, text="Toggle", bootstyle=f"{at}{color}toggle".strip()
                    ).pack(anchor=W, pady=2)
    ttk.Button(parent, text="Ghost button", bootstyle=f"{at}{color}ghost".strip()
               ).pack(anchor=W, pady=(2, 0))
    # bar families: trough/track derives from the surface (2.0 PR 4)
    ttk.Scale(parent, value=40, from_=0, to=100,
              bootstyle=f"{at}{color}".strip()).pack(anchor=W, fill=X, pady=(8, 2))
    ttk.Progressbar(parent, value=60, bootstyle=f"{at}{color}".strip()
                    ).pack(anchor=W, fill=X, pady=2)
    bar = ttk.Frame(parent)
    bar.pack(anchor=W, fill=X, pady=2)
    sb = ttk.Scrollbar(bar, orient=HORIZONTAL, bootstyle=f"{at}{color}".strip())
    sb.set(0.2, 0.6)  # partial thumb so both track and thumb show
    sb.pack(fill=X)


def main():
    app = ttk.Window(title="Surface color preview", themename="bootstrap-light",
                     size=(720, 340))

    top = ttk.Frame(app, padding=10)
    top.pack(fill=X)
    ttk.Label(top, text="@<surface> bootstyle token", font="-size 13 -weight bold"
              ).pack(side=LEFT)

    def toggle_theme():
        name = app.style.theme.name
        app.style.theme_use(
            "bootstrap-dark" if name == "bootstrap-light" else "bootstrap-light"
        )

    ttk.Button(top, text="Toggle light/dark", bootstyle="secondary-outline",
               command=toggle_theme).pack(side=RIGHT)

    row = ttk.Frame(app, padding=10)
    row.pack(fill=BOTH, expand=YES)

    # baseline: the app background (no surface token)
    base = ttk.Frame(row, padding=15)
    base.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)
    build_controls(base, "")

    # one producing accent panel per accent
    for accent in ACCENTS:
        panel = ttk.Frame(row, bootstyle=accent, padding=15)
        panel.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)
        build_controls(panel, accent)

    app.mainloop()


if __name__ == "__main__":
    main()
