"""Visual spot-check for theme-aware widget icons (apply_icon + icon=).

Shows a grid of icon buttons across the button variants that matter for the
foreground-follow contract -- solid, outline (inverts), toggle (inverts), ghost,
link -- plus a label and check/radio. Flip the theme with the switcher and watch
every glyph re-color to the new theme (and the outline/toggle glyphs invert to
the on-accent color on hover/press) with no code touching the icons.

    python examples/icon_button_preview.py
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

app = ttk.Window("Theme-aware icons", themename="bootstrap-light")

top = ttk.Frame(app, padding=10)
top.pack(fill=X)
ttk.Label(top, text="Theme:").pack(side=LEFT, padx=(0, 6))
theme_var = ttk.StringVar(value=app.style.theme.name)
themes = sorted(app.style.theme_names())
ttk.Combobox(top, textvariable=theme_var, values=themes, width=22,
             bootstyle="primary").pack(side=LEFT)
ttk.Button(top, text="Apply", bootstyle="primary", icon="check-lg",
           command=lambda: app.style.theme_use(theme_var.get())).pack(side=LEFT, padx=6)

body = ttk.Frame(app, padding=10)
body.pack(fill=BOTH, expand=YES)

# (label, bootstyle) for the button variants; icon= sugar on each
variants = [
    ("Solid", "primary"),
    ("Outline (inverts)", "primary-outline"),
    ("Toggle (inverts)", "primary-toggle"),
    ("Ghost", "primary-ghost"),
    ("Link", "primary-link"),
    ("Danger", "danger"),
    ("Success outline", "success-outline"),
    ("Disabled", "primary"),
]
for i, (label, boot) in enumerate(variants):
    b = ttk.Button(body, text=label, bootstyle=boot, icon="gear-fill")  # default size 14
    if label == "Disabled":
        b.configure(state=DISABLED)
    b.grid(row=i // 4, column=i % 4, padx=6, pady=6, sticky=EW)
for c in range(4):
    body.columnconfigure(c, weight=1)

# label + check/radio also carry the mixin sugar
row = ttk.Frame(app, padding=10)
row.pack(fill=X)
ttk.Label(row, text="Label with icon", icon="info-circle-fill",
          bootstyle="info").pack(side=LEFT, padx=6)
ttk.Checkbutton(row, text="Check", icon="star",
                bootstyle="warning").pack(side=LEFT, padx=6)
ttk.Radiobutton(row, text="Radio", icon="bookmark",
                bootstyle="success").pack(side=LEFT, padx=6)

app.mainloop()
