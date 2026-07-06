"""Visual spot-check for the `neutral` bootstyle color (2.0).

Shows the new low-emphasis `neutral` / `neutral-outline` buttons next to the
existing options (primary, secondary, light, link) so the calm, bordered neutral
look can be compared against the accented styles across states, in both light and
dark themes. Run it and toggle the theme:

    python examples/neutral_preview.py
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

STYLES = [
    ("neutral", "neutral"),
    ("neutral-outline", "neutral-outline"),
    ("primary", "primary"),
    ("secondary", "secondary"),
    ("light", "light"),
    ("link", "link"),
]

LIGHT_THEME = "bootstrap-light"
DARK_THEME = "bootstrap-dark"


class NeutralPreview(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.pack(fill=BOTH, expand=YES)

        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 15))
        ttk.Label(header, text="neutral vs accented buttons", font="-size 14 -weight bold").pack(side=LEFT)
        self.theme_btn = ttk.Button(header, text="Toggle light/dark",
                                     bootstyle="neutral", command=self.toggle_theme)
        self.theme_btn.pack(side=RIGHT)

        # column headers
        grid = ttk.Frame(self)
        grid.pack(fill=X)
        for col, state in enumerate(("bootstyle", "normal", "disabled")):
            ttk.Label(grid, text=state, font="-weight bold", width=18,
                      anchor=W).grid(row=0, column=col, padx=6, pady=6, sticky=W)

        for row, (label, style) in enumerate(STYLES, start=1):
            ttk.Label(grid, text=label, width=18, anchor=W).grid(
                row=row, column=0, padx=6, pady=4, sticky=W)
            ttk.Button(grid, text="Button", bootstyle=style).grid(
                row=row, column=1, padx=6, pady=4, sticky=W)
            disabled = ttk.Button(grid, text="Button", bootstyle=style)
            disabled.configure(state=DISABLED)
            disabled.grid(row=row, column=2, padx=6, pady=4, sticky=W)

    def toggle_theme(self):
        style = ttk.Style.get_instance()
        current = style.theme.name
        style.theme_use(DARK_THEME if current == LIGHT_THEME else LIGHT_THEME)


if __name__ == "__main__":
    app = ttk.Window("Neutral color preview", themename=LIGHT_THEME)
    NeutralPreview(app)
    app.mainloop()
