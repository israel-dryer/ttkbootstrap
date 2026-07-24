"""Bootstyle value-token preview.

A visual spot-check for the value tokens the bootstyle grammar now accepts in its
two color-bearing slots:

  - a raw hex color            bootstyle="#2f2f2f"
  - a ramp-addressed role      bootstyle="primary[300]"
  - a hex surface + accent     bootstyle="@#2b2d42 light"
  - a ramp surface + accent    bootstyle="@primary[100] primary[700]"

Toggle light/dark (top-right) to see the contract: a **ramp** token is semantic
and re-resolves against the new theme's anchor, while a **raw hex** is a frozen
snapshot that stays put. The derived states of a hex accent (hover/pressed/text)
still recompute, so a hex button stays usable in both modes.

Run:  python examples/value_token_preview.py
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


HEXES = ("#2f2f2f", "#e63946", "#2a9d8f", "#e9c46a", "#6d597a")
RAMP_STOPS = (100, 300, 500, 700, 900)
RAMP_ROLES = ("primary", "success", "danger")


def section(parent, title):
    """A titled block that packs vertically; returns its body frame."""
    ttk.Label(parent, text=title, font="-size 11 -weight bold").pack(
        anchor=W, pady=(12, 4)
    )
    body = ttk.Frame(parent)
    body.pack(fill=X)
    return body


def build_hex_accents(parent):
    """Raw-hex accents: each button IS that color, text auto-contrasted."""
    body = section(parent, "Raw hex accents  —  bootstyle=\"#rrggbb\"")
    for hexcode in HEXES:
        ttk.Button(body, text=hexcode, bootstyle=hexcode, width=10).pack(
            side=LEFT, padx=(0, 6)
        )
    # 3-digit shorthand is accepted and normalized to 6
    ttk.Button(body, text="#f0a (short)", bootstyle="#f0a", width=12).pack(
        side=LEFT, padx=(0, 6)
    )


def build_ramp_accents(parent):
    """Ramp accents: one role stepped 100->900 (tint through shade)."""
    body = section(parent, "Ramp accents  —  bootstyle=\"role[stop]\"")
    for role in RAMP_ROLES:
        rowf = ttk.Frame(body)
        rowf.pack(fill=X, pady=2)
        ttk.Label(rowf, text=role, width=9).pack(side=LEFT)
        for stop in RAMP_STOPS:
            token = f"{role}[{stop}]"
            ttk.Button(rowf, text=str(stop), bootstyle=token, width=6).pack(
                side=LEFT, padx=(0, 4)
            )


def build_value_surfaces(parent):
    """Value tokens in the @surface slot: hex and ramp panels."""
    body = section(parent, "Value surfaces  —  @#hex  and  @role[stop]")

    # a hex surface panel with a legible light accent control on it
    hex_panel = ttk.Frame(body, bootstyle="#2b2d42", padding=14)
    hex_panel.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 6))
    ttk.Label(hex_panel, text="@#2b2d42", bootstyle="@#2b2d42 light").pack(anchor=W)
    ttk.Checkbutton(hex_panel, text="Checkbutton",
                    bootstyle="@#2b2d42 light").pack(anchor=W, pady=(6, 2))
    ttk.Button(hex_panel, text="Ghost", bootstyle="@#2b2d42 light ghost").pack(
        anchor=W, pady=2
    )

    # a ramp surface panel (a pale primary tint) with a deep primary control
    ramp_panel = ttk.Frame(body, bootstyle="primary[100]", padding=14)
    ramp_panel.pack(side=LEFT, fill=BOTH, expand=YES, padx=6)
    ttk.Label(ramp_panel, text="@primary[100]",
              bootstyle="@primary[100] primary[800]").pack(anchor=W)
    ttk.Checkbutton(ramp_panel, text="Checkbutton",
                    bootstyle="@primary[100] primary[700]").pack(anchor=W, pady=(6, 2))
    ttk.Button(ramp_panel, text="Ghost",
               bootstyle="@primary[100] primary[700] ghost").pack(anchor=W, pady=2)


def build_reactivity(parent):
    """Side-by-side hex vs ramp swatch so the theme toggle shows the contract."""
    body = section(parent, "Theme-reactivity  —  toggle light/dark to compare")
    ttk.Button(body, text="frozen hex  #3b79d5", bootstyle="#3b79d5",
               width=22).pack(side=LEFT, padx=(0, 8))
    ttk.Button(body, text="reactive  primary[500]", bootstyle="primary[500]",
               width=22).pack(side=LEFT)
    ttk.Label(
        parent,
        text=("The hex button keeps #3b79d5 in both themes; the ramp button "
              "follows each theme's primary anchor."),
        bootstyle="secondary",
    ).pack(anchor=W, pady=(6, 0))


def build_interactive(parent):
    """Type a hex and apply it live to a preview button."""
    body = section(parent, "Try your own hex")
    var = ttk.StringVar(value="#ff6b6b")
    preview = ttk.Button(body, text="preview", bootstyle=var.get(), width=12)

    def apply(*_):
        value = var.get().strip()
        if value:
            try:
                preview.configure(bootstyle=value)
                preview.configure(text=value)
            except Exception:
                pass  # invalid hex already warns via the resolver

    entry = ttk.Entry(body, textvariable=var, width=12)
    entry.pack(side=LEFT, padx=(0, 6))
    entry.bind("<Return>", apply)
    ttk.Button(body, text="Apply", bootstyle="secondary-outline",
               command=apply).pack(side=LEFT, padx=(0, 12))
    preview.pack(side=LEFT)


def main():
    app = ttk.Window(title="Bootstyle value tokens", theme="bootstrap-light",
                     size=(760, 620))

    top = ttk.Frame(app, padding=(14, 12))
    top.pack(fill=X)
    ttk.Label(top, text="Bootstyle value tokens", font="-size 14 -weight bold"
              ).pack(side=LEFT)

    def toggle_theme():
        name = app.style.theme.name
        app.style.theme_use(
            "bootstrap-dark" if name == "bootstrap-light" else "bootstrap-light"
        )

    ttk.Button(top, text="Toggle light/dark", bootstyle="secondary-outline",
               command=toggle_theme).pack(side=RIGHT)

    body = ttk.Frame(app, padding=(14, 0, 14, 12))
    body.pack(fill=BOTH, expand=YES)

    build_hex_accents(body)
    build_ramp_accents(body)
    build_value_surfaces(body)
    build_reactivity(body)
    build_interactive(body)

    app.mainloop()


if __name__ == "__main__":
    main()