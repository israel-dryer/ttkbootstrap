"""Visual gate for the 2.0 recolorable ttk element assets.

Run with `python examples/recolor_assets_preview.py`, then switch between the
light and dark themes and inspect normal, selected, disabled, and oriented
variants of every migrated widget family.
"""
import tkinter as tk

import ttkbootstrap as ttk


class Preview:
    def __init__(self, app):
        self.app = app
        self.style = app.style
        self.variables = []
        self.body = ttk.Frame(app, padding=16)
        self.body.pack(fill="both", expand=True)
        self._build_header()
        self._build_widgets()

    def _build_header(self):
        header = ttk.Frame(self.body)
        header.pack(fill="x", pady=(0, 12))
        self.title = ttk.Label(header, font="-size 14 -weight bold")
        self.title.pack(side="left")
        self.switch = ttk.Button(
            header, bootstyle="secondary", command=self._toggle_theme)
        self.switch.pack(side="right")
        self._refresh_header()

    def _build_widgets(self):
        indicators = ttk.Labelframe(
            self.body, text="Indicators", padding=12)
        indicators.pack(fill="x", pady=6)
        for column, color in enumerate(("primary", "success", "warning", "light")):
            group = ttk.Frame(indicators)
            group.grid(row=0, column=column, padx=12, sticky="n")
            ttk.Label(group, text=color).pack(anchor="w")
            check_var = tk.IntVar(value=1)
            self.variables.append(check_var)
            ttk.Checkbutton(
                group, text="Checked", variable=check_var,
                bootstyle=color).pack(anchor="w", pady=2)
            radio_var = tk.IntVar(value=1)
            self.variables.append(radio_var)
            ttk.Radiobutton(
                group, text="Selected", variable=radio_var, value=1,
                bootstyle=color).pack(anchor="w", pady=2)
            round_var = tk.BooleanVar(value=True)
            square_var = tk.BooleanVar(value=False)
            self.variables.extend((round_var, square_var))
            ttk.Checkbutton(
                group, text="Round switch", variable=round_var,
                bootstyle=f"{color}-round-toggle").pack(anchor="w", pady=2)
            ttk.Checkbutton(
                group, text="Square switch", variable=square_var,
                bootstyle=f"{color}-square-toggle").pack(anchor="w", pady=2)
            disabled = ttk.Checkbutton(group, text="Disabled", bootstyle=color)
            disabled.pack(anchor="w", pady=2)
            disabled.state(["disabled", "selected"])

        motion = ttk.Labelframe(
            self.body, text="Scale / scrollbar", padding=12)
        motion.pack(fill="both", expand=True, pady=6)
        ttk.Scale(motion, from_=0, to=100, value=55,
                  bootstyle="primary").pack(fill="x", pady=8)
        ttk.Scrollbar(motion, orient="horizontal",
                      bootstyle="primary").pack(fill="x", pady=8)
        ttk.Scrollbar(motion, orient="horizontal",
                      bootstyle="round-success").pack(fill="x", pady=8)
        verticals = ttk.Frame(motion)
        verticals.pack(fill="both", expand=True, pady=6)
        ttk.Scale(verticals, orient="vertical", from_=100, to=0, value=45,
                  bootstyle="warning").pack(side="left", fill="y", padx=12)
        sb = ttk.Scrollbar(verticals, orient="vertical", bootstyle="info")
        sb.set(0.25, 0.50)
        sb.pack(side="left", fill="y", padx=12)

        progress = ttk.Labelframe(
            verticals, text="Progressbar variants", padding=12)
        progress.pack(side="left", fill="both", expand=True, padx=12)
        for style_name in ("primary", "success-thin", "info-striped"):
            ttk.Label(progress, text=style_name).pack(anchor="w")
            ttk.Progressbar(
                progress, value=65, bootstyle=style_name).pack(
                    fill="x", pady=(2, 10))

    def _refresh_header(self):
        current = self.style.theme.name
        other = "darkly" if current == "flatly" else "flatly"
        self.title.configure(text=f"Recolorable element assets — {current}")
        self.switch.configure(text=f"Switch to {other}")

    def _toggle_theme(self):
        other = "darkly" if self.style.theme.name == "flatly" else "flatly"
        self.style.theme_use(other)
        self._refresh_header()


if __name__ == "__main__":
    app = ttk.Window(
        title="ttkbootstrap 2.0 — recolorable assets",
        themename="flatly", size=(820, 720))
    Preview(app)
    app.mainloop()
