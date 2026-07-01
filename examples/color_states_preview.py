"""Visual gate for the 2.0 private color-derivation helpers.

Run with `python examples/color_states_preview.py`. Exercise hover, pressed,
selected, focus, and disabled states for every color column, then switch among
the six representative themes from the header.
"""
import tkinter as tk

import ttkbootstrap as ttk


THEMES = ("flatly", "minty", "morph", "darkly", "solar", "vapor")
COLORS = ("primary", "warning", "info", "light", "dark")


class ColorStatesPreview:
    def __init__(self, app):
        self.app = app
        self.style = app.style
        self.variables = []
        body = ttk.Frame(app, padding=16)
        body.pack(fill="both", expand=True)
        self._build_header(body)

        canvas = tk.Canvas(body, highlightthickness=0)
        scrollbar = ttk.Scrollbar(body, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        content = ttk.Frame(canvas, padding=(0, 8))
        window = canvas.create_window((0, 0), window=content, anchor="nw")
        content.bind(
            "<Configure>",
            lambda _event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(window, width=event.width),
        )

        self._build_buttons(content)
        self._build_fields(content)
        self._build_indicators(content)
        self._build_motion(content)
        self._build_tree(content)

    def _build_header(self, parent):
        header = ttk.Frame(parent)
        header.pack(fill="x", pady=(0, 8))
        ttk.Label(
            header,
            text="Color-state derivation",
            font="-size 15 -weight bold",
        ).pack(side="left")
        ttk.Label(
            header,
            text="Hold mouse button to inspect pressed; Tab for focus",
        ).pack(side="left", padx=20)
        chooser = ttk.Combobox(
            header, values=THEMES, state="readonly", width=12
        )
        chooser.set(self.style.theme.name)
        chooser.pack(side="right")
        chooser.bind("<<ComboboxSelected>>", self._select_theme)

    def _build_buttons(self, parent):
        section = ttk.Labelframe(parent, text="Filled controls", padding=12)
        section.pack(fill="x", pady=6)
        for column, color in enumerate(COLORS):
            group = ttk.Frame(section)
            group.grid(row=0, column=column, padx=8, sticky="nsew")
            section.columnconfigure(column, weight=1)
            ttk.Label(group, text=color, font="-weight bold").pack(pady=3)
            ttk.Button(group, text="Button", bootstyle=color).pack(
                fill="x", pady=3
            )
            ttk.Button(
                group, text="Outline", bootstyle=f"{color}-outline"
            ).pack(fill="x", pady=3)
            ttk.Menubutton(
                group, text="Menu", bootstyle=color
            ).pack(fill="x", pady=3)
            toolvar = tk.BooleanVar(value=True)
            self.variables.append(toolvar)
            ttk.Checkbutton(
                group,
                text="Toolbutton",
                variable=toolvar,
                bootstyle=f"{color}-toolbutton",
            ).pack(fill="x", pady=3)
            disabled = ttk.Button(group, text="Disabled", bootstyle=color)
            disabled.pack(fill="x", pady=3)
            disabled.state(["disabled"])

    def _build_fields(self, parent):
        section = ttk.Labelframe(
            parent, text="Field disabled and readonly states", padding=12
        )
        section.pack(fill="x", pady=6)
        for row, color in enumerate(COLORS):
            ttk.Label(section, text=color, width=9).grid(row=row, column=0)

            entry = ttk.Entry(section, bootstyle=color)
            entry.insert(0, "Disabled entry")
            entry.state(["disabled"])
            entry.grid(row=row, column=1, sticky="ew", padx=8, pady=4)

            readonly = ttk.Combobox(
                section,
                values=("Readonly combobox",),
                state="readonly",
                bootstyle=color,
            )
            readonly.current(0)
            readonly.grid(row=row, column=2, sticky="ew", padx=8, pady=4)

            disabled_combo = ttk.Combobox(
                section,
                values=("Disabled combobox",),
                bootstyle=color,
            )
            disabled_combo.current(0)
            disabled_combo.state(["disabled"])
            disabled_combo.grid(
                row=row, column=3, sticky="ew", padx=8, pady=4
            )

            spinbox = ttk.Spinbox(
                section, values=("Disabled spinbox",), bootstyle=color
            )
            spinbox.set("Disabled spinbox")
            spinbox.state(["disabled"])
            spinbox.grid(row=row, column=4, sticky="ew", padx=8, pady=4)

        for column in range(1, 5):
            section.columnconfigure(column, weight=1)

    def _build_indicators(self, parent):
        section = ttk.Labelframe(parent, text="Indicators", padding=12)
        section.pack(fill="x", pady=6)
        for column, color in enumerate(COLORS):
            group = ttk.Frame(section)
            group.grid(row=0, column=column, padx=8, sticky="nsew")
            section.columnconfigure(column, weight=1)
            checkvar = tk.BooleanVar(value=True)
            radiovar = tk.IntVar(value=1)
            togglevar = tk.BooleanVar(value=True)
            self.variables.extend((checkvar, radiovar, togglevar))
            ttk.Checkbutton(
                group, text=color, variable=checkvar, bootstyle=color
            ).pack(anchor="w", pady=3)
            ttk.Radiobutton(
                group,
                text="Radio",
                variable=radiovar,
                value=1,
                bootstyle=color,
            ).pack(anchor="w", pady=3)
            ttk.Checkbutton(
                group,
                text="Toggle",
                variable=togglevar,
                bootstyle=f"{color}-round-toggle",
            ).pack(anchor="w", pady=3)
            disabled = ttk.Checkbutton(group, text="Disabled", bootstyle=color)
            disabled.pack(anchor="w", pady=3)
            disabled.state(["disabled", "selected"])

    def _build_motion(self, parent):
        section = ttk.Labelframe(
            parent, text="Scale, scrollbar, and date button", padding=12
        )
        section.pack(fill="x", pady=6)
        for row, color in enumerate(COLORS):
            ttk.Label(section, text=color, width=9).grid(row=row, column=0)
            ttk.Scale(
                section, from_=0, to=100, value=55, bootstyle=color
            ).grid(row=row, column=1, sticky="ew", padx=8, pady=4)
            scrollbar = ttk.Scrollbar(
                section, orient="horizontal", bootstyle=color
            )
            scrollbar.set(0.25, 0.65)
            scrollbar.grid(row=row, column=2, sticky="ew", padx=8, pady=4)
            ttk.DateEntry(section, bootstyle=color).grid(
                row=row, column=3, padx=8, pady=4
            )
            disabled_date = ttk.Button(
                section, bootstyle=f"{color}-date"
            )
            disabled_date.state(["disabled"])
            disabled_date.grid(row=row, column=4, padx=8, pady=4)
        section.columnconfigure(1, weight=1)
        section.columnconfigure(2, weight=1)

    def _build_tree(self, parent):
        section = ttk.Labelframe(parent, text="Treeview", padding=12)
        section.pack(fill="both", expand=True, pady=6)
        tree = ttk.Treeview(
            section, columns=("state",), show="tree headings", height=5
        )
        tree.heading("#0", text="Color")
        tree.heading("state", text="Select rows; hover headings")
        for color in COLORS:
            tree.insert("", "end", text=color, values=("normal",))
        tree.pack(fill="both", expand=True)

    def _select_theme(self, event):
        self.style.theme_use(event.widget.get())


if __name__ == "__main__":
    app = ttk.Window(
        title="ttkbootstrap 2.0 — color states",
        themename="flatly",
        size=(1080, 820),
    )
    ColorStatesPreview(app)
    app.mainloop()
