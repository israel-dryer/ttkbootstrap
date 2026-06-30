"""Visual gate for 2.0 scaling and recolorable ttk element assets.

Run once per nominal scale, then switch between the light and dark themes:

`python examples/recolor_assets_preview.py --scale 1.25`

Supported factors are 1.0, 1.25, 1.5, and 2.0. Inspect normal, selected,
disabled, and oriented raster variants on the Assets tab and representative
Tk-facing builder geometry on the Geometry tab.
"""
import argparse
import platform
import tkinter as tk

import ttkbootstrap as ttk


class Preview:
    def __init__(self, app, factor):
        self.app = app
        self.factor = factor
        self.style = app.style
        self.variables = []
        self.body = ttk.Frame(app, padding=16)
        self.body.pack(fill="both", expand=True)
        self._build_header()
        tabs = ttk.Notebook(self.body)
        tabs.pack(fill="both", expand=True)
        assets = ttk.Frame(tabs, padding=8)
        geometry = ttk.Frame(tabs, padding=8)
        tabs.add(assets, text="Assets")
        tabs.add(geometry, text="Geometry")
        self._build_widgets(assets)
        self._build_geometry(geometry)

    def _build_header(self):
        header = ttk.Frame(self.body)
        header.pack(fill="x", pady=(0, 12))
        self.title = ttk.Label(header, font="-size 14 -weight bold")
        self.title.pack(side="left")
        self.switch = ttk.Button(
            header, bootstyle="secondary", command=self._toggle_theme)
        self.switch.pack(side="right")
        self._refresh_header()

    def _build_widgets(self, parent):
        indicators = ttk.Labelframe(
            parent, text="Indicators", padding=12)
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
            parent, text="Scale / scrollbar", padding=12)
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

    def _build_geometry(self, parent):
        buttons = ttk.Labelframe(parent, text="Buttons and fields", padding=12)
        buttons.pack(fill="x", pady=6)
        ttk.Button(buttons, text="Primary", bootstyle="primary").grid(
            row=0, column=0, padx=6, pady=6)
        ttk.Button(buttons, text="Outline", bootstyle="success-outline").grid(
            row=0, column=1, padx=6, pady=6)
        ttk.DateEntry(buttons, bootstyle="primary").grid(
            row=0, column=2, padx=6, pady=6)
        ttk.Entry(buttons).grid(row=1, column=0, padx=6, pady=6, sticky="ew")
        ttk.Combobox(buttons, values=("Combobox", "Second value")).grid(
            row=1, column=1, padx=6, pady=6, sticky="ew")
        ttk.Spinbox(buttons, from_=0, to=10).grid(
            row=1, column=2, padx=6, pady=6, sticky="ew")
        for column in range(3):
            buttons.columnconfigure(column, weight=1)

        panes = ttk.Panedwindow(parent, orient="horizontal")
        panes.pack(fill="x", pady=8)
        left = ttk.Frame(panes, padding=12, bootstyle="light")
        right = ttk.Frame(panes, padding=12, bootstyle="secondary")
        ttk.Label(left, text="Panedwindow left").pack()
        ttk.Label(right, text="Panedwindow right", bootstyle="inverse").pack()
        panes.add(left, weight=1)
        panes.add(right, weight=1)

        tree = ttk.Treeview(
            parent, columns=("value",), show="tree headings", height=5)
        tree.heading("#0", text="Treeview")
        tree.heading("value", text="Value")
        tree.column("#0", width=180)
        tree.column("value", width=180)
        for index in range(4):
            tree.insert("", "end", text=f"Row {index + 1}", values=(index * 25,))
        tree.pack(fill="both", expand=True, pady=8)
        ttk.Sizegrip(parent).pack(anchor="se")

    def _refresh_header(self):
        current = self.style.theme.name
        other = "darkly" if current == "flatly" else "flatly"
        percent = round(self.factor * 100)
        self.title.configure(text=f"Scaling preview — {percent}% — {current}")
        self.switch.configure(text=f"Switch to {other}")

    def _toggle_theme(self):
        other = "darkly" if self.style.theme.name == "flatly" else "flatly"
        self.style.theme_use(other)
        self._refresh_header()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scale", type=float, choices=(1.0, 1.25, 1.5, 2.0), default=1.0)
    args = parser.parse_args()
    baseline = 1.0 if platform.system() == "Darwin" else 4 / 3
    app = ttk.Window(
        title="ttkbootstrap 2.0 — scaling preview",
        themename="flatly", size=(900, 760), scaling=baseline * args.scale)
    Preview(app, args.scale)
    app.mainloop()
