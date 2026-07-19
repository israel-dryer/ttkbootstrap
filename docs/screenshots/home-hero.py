"""Landing-page hero: a curated widget sampler.

Self-contained (adapted from the __main__ demo, not imported, so the two can
evolve independently). It answers the question a library visitor actually has --
"what do I get?" -- by showing the palette plus a broad spread of themed widgets:
the button family, inputs, indicators, a Tableview, and a Notebook holding the
choice controls. Labelled cards keep it a sampler, not a fake-app dashboard. The
harness forces the theme, so the header reads the live theme name.

Single scene, so it runs at module level (no SCENES dict) -> the harness writes
docs/_static/examples/home-hero-{light,dark}.png.
"""
import ttkbootstrap as ttk

app = ttk.App(title="ttkbootstrap")

# module-level vars persist for the life of the mainloop (no GC)
on = ttk.BooleanVar(value=True)
choice = ttk.StringVar(value="b")

bag = ttk.Frame(app, padding=12)
bag.pack(fill="both", expand=True)
for i in range(4):
    bag.columnconfigure(i, weight=1, uniform="col", minsize=210)

# header: wordmark + the live theme name
head = ttk.Frame(bag).grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 8))
ttk.Label(head, text="ttkbootstrap", font="-size 22 -weight bold").pack(side="left")
ttk.Label(head, text=app.style.theme.name, bootstyle="secondary",
          font="-size 12").pack(side="left", padx=8, pady=(10, 0))

# semantic accent swatches -- the palette at a glance
accents = ("primary", "secondary", "success", "info", "warning", "danger")
swatches = ttk.Frame(bag).grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 10))
for c in accents:
    ttk.Label(swatches, text=c, anchor="center", bootstyle=f"@{c}",
              padding=8).pack(side="left", fill="x", expand=True, padx=2)

# buttons: solid / outline / ghost, in color
btns = ttk.Labelframe(bag, text="Buttons", padding=10).grid(
    row=2, column=0, sticky="nsew", padx=(0, 6), pady=(0, 6))
ttk.Button(btns, text="Default").pack(fill="x", pady=3)
ttk.Button(btns, text="Primary", bootstyle="primary").pack(fill="x", pady=3)
ttk.Button(btns, text="Success outline", bootstyle="success outline").pack(fill="x", pady=3)
ttk.Button(btns, text="Info ghost", bootstyle="info ghost").pack(fill="x", pady=3)

# inputs
inp = ttk.Labelframe(bag, text="Inputs", padding=10).grid(
    row=2, column=1, sticky="nsew", padx=6, pady=(0, 6))
ttk.Entry(inp).pack(fill="x", pady=3).insert(0, "Entry")
cbo = ttk.Combobox(inp, values=("One", "Two", "Three"), state="readonly").pack(fill="x", pady=3)
cbo.current(0)
ttk.DateEntry(inp).pack(fill="x", pady=3)
ttk.Spinbox(inp, from_=0, to=10).pack(fill="x", pady=3).insert(0, "5")

# toolbuttons: the toggle side of the button family (shown ON)
tools = ttk.Labelframe(bag, text="Toolbuttons", padding=10).grid(
    row=2, column=2, sticky="nsew", padx=6, pady=(0, 6))
ttk.Checkbutton(tools, text="Default", bootstyle="toolbutton").pack(fill="x", pady=3).invoke()
ttk.Checkbutton(tools, text="Info outline", bootstyle="info outline toolbutton").pack(fill="x", pady=3).invoke()
ttk.Checkbutton(tools, text="Success ghost", bootstyle="success ghost toolbutton").pack(fill="x", pady=3).invoke()

# indicators: meter + progress
ind = ttk.Labelframe(bag, text="Indicators", padding=10).grid(
    row=2, column=3, sticky="nsew", padx=(6, 0), pady=(0, 6))
ttk.Meter(ind, meter_size=130, padding=0, amount_used=72, subtext="progress",
          bootstyle="info", interactive=False).pack()
ttk.Progressbar(ind, value=60, bootstyle="success striped").pack(fill="x", pady=(8, 4))
ttk.Progressbar(ind, value=40, bootstyle="warning thin").pack(fill="x", pady=4)

# tableview -- the data grid
tvf = ttk.Labelframe(bag, text="Tableview", padding=10).grid(
    row=3, column=0, columnspan=2, sticky="nsew", padx=(0, 6))
ttk.Tableview(
    tvf,
    bootstyle="primary",
    coldata=["Name", "Role"],
    rowdata=[
        ("Grace Hopper", "Engineer"),
        ("Alan Turing", "Researcher"),
        ("Barbara Liskov", "Architect"),
        ("Linus Torvalds", "Maintainer"),
    ],
    paginated=False,
    searchable=False,
    height=4,
).pack(fill="both", expand=True)

# notebook -- tabs holding the choice controls
nbf = ttk.Labelframe(bag, text="Notebook", padding=10).grid(
    row=3, column=2, columnspan=2, sticky="nsew", padx=(6, 0))
nb = ttk.Notebook(nbf).pack(fill="both", expand=True)
# Only the active tab renders in a static shot, so put every control we want
# seen on the FIRST tab -- checkbutton, radiobuttons, and a toggle together.
controls = ttk.Frame(nb, padding=10)
ttk.Checkbutton(controls, text="Enabled", variable=on).pack(anchor="w", pady=2)
ttk.Radiobutton(controls, text="Option A", value="a", variable=choice).pack(anchor="w", pady=2)
ttk.Radiobutton(controls, text="Option B", value="b", variable=choice).pack(anchor="w", pady=2)
ttk.Checkbutton(controls, text="Notifications", variable=on,
                bootstyle="success round toggle").pack(anchor="w", pady=2)
nb.add(controls, text="Controls")
# A second tab so the strip reads as a real notebook; its content is never
# captured (the active tab is the only one that renders), so keep it incidental.
nb.add(ttk.Frame(nb, padding=10), text="Details")

app._capture_full_window = True   # a real window -- show the chrome
app._capture_max_width = 960      # wider than the default doc-body shot
app.mainloop()