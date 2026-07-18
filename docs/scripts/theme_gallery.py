"""Capture one sample card per theme -> ``theming-card-<theme>.png``.

The Style engine is one-theme-per-process, so this re-execs itself once per
theme (``TTKB_GALLERY_THEME`` set) to capture a single card. The Themes catalog
page (``docs/themes.rst``) lays the 30 cards out by family: a family heading with
its light and dark cards side by side (so the light/dark toggle pair reads at a
glance). Cards have transparent corners (the pydata white-image bg is stripped by
the ``tb-gallery`` class).

    python docs/scripts/theme_gallery.py
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "docs" / "_static" / "examples"

FAMILIES = [
    "bootstrap", "pydata", "nord", "solarized", "catppuccin",
    "gruvbox", "dracula", "tokyo-night", "one", "everforest",
    "vapor", "minty", "pulse", "united", "sandstone",
]


def _capture_one(theme: str, out: str) -> None:
    """Build one theme's sample card and grab it to ``out`` (own process)."""
    import tkinter
    import ttkbootstrap as ttk
    from PIL import ImageGrab

    family = theme.rsplit("-", 1)[0]
    app = ttk.App(theme=theme)
    app.attributes("-topmost", True)
    app.after(0, lambda: app.geometry("+200+120"))
    app.minsize(259, 1)

    # Inset the card inside a holder so the grabbed card rect sits clear of the
    # window's rounded bottom corners (which would otherwise bleed the desktop).
    holder = ttk.Frame(app)
    holder.pack(fill="both", expand=True)
    card = ttk.Frame(holder, padding=12)
    card.pack(fill="x", padx=12, pady=12)
    combo = ttk.Combobox(card, values=[f"{family}-light", f"{family}-dark"], state="readonly")
    combo.set(theme)                       # the exact theme name, in a real widget
    combo.pack(fill="x")

    chips = ttk.Frame(card)
    chips.pack(fill="x", pady=(10, 10))
    for c in ["primary", "success", "info", "warning", "danger"]:
        ttk.Label(chips, bootstyle=f"@{c}", padding=(0, 10)).pack(
            side="left", fill="x", expand=True, padx=1)

    row = ttk.Frame(card)
    row.pack(fill="x")
    ttk.Button(row, text="Default", bootstyle="primary").pack(side="left", fill="x", expand=True, padx=(0, 6))
    ttk.Button(row, text="Outline", bootstyle="primary outline").pack(side="left", fill="x", expand=True, padx=(0, 6))
    ttk.Button(row, text="Ghost", bootstyle="primary ghost").pack(side="left", fill="x", expand=True)

    controls = ttk.Frame(card)
    controls.pack(fill="x", pady=(10, 0))
    app._vars = [tkinter.IntVar(value=1) for _ in range(3)]
    rb, cb, tg = app._vars
    ttk.Radiobutton(controls, variable=rb, value=1, bootstyle="primary").pack(side="left", padx=(0, 14))
    ttk.Checkbutton(controls, variable=cb, bootstyle="success").pack(side="left", padx=(0, 14))
    ttk.Checkbutton(controls, variable=tg, bootstyle="info round toggle").pack(side="left", padx=(0, 14))
    scale = ttk.Scale(controls, from_=0, to=100, bootstyle="primary")
    scale.set(60)
    scale.pack(side="left", fill="x", expand=True)

    def grab():
        app.update_idletasks()
        x, y = card.winfo_rootx(), card.winfo_rooty()
        img = ImageGrab.grab(bbox=(x, y, x + card.winfo_width(), y + card.winfo_height()))
        img.save(out)
        app.destroy()

    app.after(600, grab)
    app.mainloop()


def main():
    theme = os.environ.get("TTKB_GALLERY_THEME")
    if theme:                       # re-exec branch: capture one card
        _capture_one(theme, os.environ["TTKB_GALLERY_OUT"])
        return
    for fam in FAMILIES:
        for mode in ("light", "dark"):
            name = f"{fam}-{mode}"
            out = OUT / f"theming-card-{name}.png"
            subprocess.run(
                [sys.executable, __file__],
                env={**os.environ, "TTKB_GALLERY_THEME": name,
                     "TTKB_GALLERY_OUT": str(out)},
                cwd=str(REPO), check=True, capture_output=True, text=True,
            )
            print(f"{name} -> {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
