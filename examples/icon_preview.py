"""Visual preview for the 2.0 icon engine (PR 6a).

PR 6a adds the icon renderer + the public `Icon` atom and `icon_element` sugar,
but wires nothing into the builders yet -- so existing widgets look identical and
the headless suite only asserts color-at-pixel. This demo is the human eyeball:
it renders the glyph set PR 6b will adopt for the indicators, plus a live
`icon_element` custom checkbutton, with a light<->dark toggle to check the
transparent-knockout contrast on both backgrounds.

The widget tree is built **once**; the light<->dark toggle reconfigures each icon
label's `image=` in place (same size -> no relayout), so the switch is instant
instead of tearing down and recreating ~200 widgets.

Run:  python examples/icon_preview.py
"""
import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import LEFT, X, BOTH, YES
from ttkbootstrap.style import Colors, icon_element, layout, El, state_map


# The glyph set PR 6b maps onto the indicators (design: 2_0_icons_design.md).
INDICATOR_GLYPHS = [
    ("checkbutton off",  "square"),
    ("checkbutton on",   "check-square-fill"),
    ("checkbutton alt",  "dash-square-fill"),
    ("radio off",        "circle"),
    ("radio on",         "record-circle-fill"),
    ("switch off",       "toggle-off"),
    ("switch on",        "toggle-on"),
]
OTHER_GLYPHS = [
    ("chevron down",  "chevron-down"),
    ("chevron up",    "chevron-up"),
    ("chevron left",  "chevron-left"),
    ("chevron right", "chevron-right"),
    ("calendar",      "calendar"),
    ("calendar-event", "calendar-event"),
    ("grip",          "grip-horizontal"),
]

# A range of sizes to judge crispness at small indicator sizes and up.
SIZES = [16, 20, 24, 32]


class Preview:
    """Build the structure once; recolor every icon in place on theme switch."""

    def __init__(self, app):
        self.app = app
        self.style = app.style
        # icon labels, tagged with how their color is sourced each theme:
        #   ("fg", name, size) | ("role", name, role)  role in accent/muted/disabled
        self.icon_labels = []          # [(label, kind, name, extra)]
        self.checkbuttons = []         # the live icon_element widgets (recreated)
        self._fav_built = set()        # element_create is one-shot per element name
        self._build_structure()
        self.apply_theme(self.style.theme.name)

    # -- colors for the current theme -------------------------------------- #
    def _palette(self):
        c = self.style.colors
        return {
            "fg": c.fg,
            "accent": c.primary,
            "muted": Colors.make_transparent(0.4, c.fg, c.bg),
            "disabled": Colors.make_transparent(0.3, c.fg, c.bg),
        }

    # -- one-time widget construction -------------------------------------- #
    def _build_structure(self):
        app = self.app
        top = ttk.Frame(app, padding=10)
        top.pack(fill=X)
        self.header = ttk.Label(top, text="", font="-size 13 -weight bold")
        self.header.pack(side=LEFT)
        self.switch_btn = ttk.Button(top, text="", bootstyle="secondary",
                                     command=self._toggle_theme)
        self.switch_btn.pack(side="right")

        body = ttk.Frame(app, padding=10)
        body.pack(fill=BOTH, expand=YES)

        left = ttk.Frame(body)
        left.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))
        self._grid_section(left, "Indicator glyphs (PR 6b: check / radio / switch)",
                            INDICATOR_GLYPHS)

        right = ttk.Frame(body)
        right.pack(side=LEFT, fill=BOTH, expand=YES)
        self._grid_section(right, "Other glyph-shaped assets (arrows / date / grip)",
                           OTHER_GLYPHS)

        self.fav_frame = ttk.Labelframe(
            right, text="icon_element — live state→icon swap", padding=12)
        self.fav_frame.pack(fill=X, pady=6)
        ttk.Label(self.fav_frame, text="Toggle — the glyph swaps star ↔ star-fill:"
                  ).pack(anchor="w")
        self.cb_holder = ttk.Frame(self.fav_frame)
        self.cb_holder.pack(fill=X)

    def _grid_section(self, parent, title, glyphs):
        lf = ttk.Labelframe(parent, text=title, padding=10)
        lf.pack(fill=X, pady=6)
        ttk.Label(lf, text="").grid(row=0, column=0, padx=6)
        for col, size in enumerate(SIZES, start=1):
            ttk.Label(lf, text=f"{size}px").grid(row=0, column=col, padx=10)
        ttk.Label(lf, text="accent / muted / disabled").grid(
            row=0, column=len(SIZES) + 1, padx=10)
        for row, (label, name) in enumerate(glyphs, start=1):
            ttk.Label(lf, text=f"{label}\n{name}", justify=LEFT).grid(
                row=row, column=0, sticky="w", padx=6, pady=2)
            for col, size in enumerate(SIZES, start=1):
                lbl = ttk.Label(lf)
                lbl.grid(row=row, column=col, padx=10, pady=2)
                self.icon_labels.append((lbl, "fg", name, size))
            sw = ttk.Frame(lf)
            sw.grid(row=row, column=len(SIZES) + 1, padx=10)
            for role in ("accent", "muted", "disabled"):
                lbl = ttk.Label(sw)
                lbl.pack(side=LEFT, padx=2)
                self.icon_labels.append((lbl, role, name, 24))

    # -- per-theme update (no teardown) ------------------------------------ #
    def apply_theme(self, themename):
        self.style.theme_use(themename)
        pal = self._palette()
        for lbl, kind, name, extra in self.icon_labels:
            color = pal["fg"] if kind == "fg" else pal[kind]
            size = extra
            lbl.configure(image=ttk.Icon(name, size=size, color=color))
        self.header.configure(text=f"Icon engine preview  —  theme: {themename}")
        other = "darkly" if themename == "flatly" else "flatly"
        self.switch_btn.configure(text=f"Switch to {other}")
        self._build_favorites(themename, pal)

    def _toggle_theme(self):
        other = "darkly" if self.style.theme.name == "flatly" else "flatly"
        self.apply_theme(other)

    def _build_favorites(self, themename, pal):
        # The icon_element images are baked per theme, so the style is theme
        # -namespaced and built once each; the 3 checkbuttons are cheap to recreate.
        favstyle = f"Fav.{themename}.TCheckbutton"
        if favstyle not in self._fav_built:
            element = f"{favstyle}.indicator"
            self.style._build_configure(favstyle, foreground=self.style.colors.fg)
            state_map(self.style, favstyle, foreground={"disabled": pal["disabled"]})
            icon_element(self.style, element, size=24,
                         default={"name": "star-fill", "color": "warning"},  # selected
                         states={"!selected": "star"},                       # off → fg
                         border=4, sticky="w")
            layout(self.style, favstyle, El("Checkbutton.padding", sticky="nsew", children=[
                El(element, side="left", sticky=""),
                El("Checkbutton.focus", side="left", sticky="", children=[
                    El("Checkbutton.label", sticky="nsew")])]))
            # Register so BootMixin honors `style=favstyle` as a real style (else it
            # re-resolves the name as a bootstyle string -> base TCheckbutton).
            self.style._register_ttkstyle(favstyle)
            self._fav_built.add(favstyle)

        for cb in self.checkbuttons:
            cb.destroy()
        self.checkbuttons.clear()
        for text, start_on, is_disabled in (
            ("Favorite this (starts on)", True, False),
            ("And this one (starts off)", False, False),
            ("Disabled (off)", False, True),
        ):
            # A real BooleanVar gives a clean two-state !selected<->selected toggle;
            # without one the widget starts 'alternate' and the swap reads as broken.
            var = tk.BooleanVar(value=start_on)
            cb = ttk.Checkbutton(self.cb_holder, text=text, style=favstyle, variable=var)
            cb._preview_var = var  # keep a ref alive
            cb.pack(anchor="w", pady=3)
            if is_disabled:
                cb.configure(state="disabled")
            self.checkbuttons.append(cb)


if __name__ == "__main__":
    app = ttk.Window(title="ttkbootstrap 2.0 — icon engine preview", themename="flatly",
                     size=(1100, 720))
    Preview(app)
    app.mainloop()
