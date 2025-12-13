---
icon: fontawesome/solid/play
---

# First Application

Now that you have the package installed, assemble the core pieces that every ttkbootstrap 2 app shares: the `ttk.App` shell, theming hooks, and a layout that houses widgets, dialogs, and custom controls.

![Application diagram](https://placehold.co/800x800/FFFFFF/333333.webp?text=App%20Structure&font=lato)

## Anatomy

1. **App shell** — `ttk.App(title="...", theme="...")` boots the themed window, exposes the root, and handles DPI.
2. **Layout containers** — `Frame`, `Labelframe`, or custom `PageStack` nodes hold widgets.
3. **Widgets & dialogs** — Use the cataloged controls to drive UI detail.

## Sample application

```python
from ttkbootstrap import ttk

app = ttk.App(title="ttkbootstrap 2 First App", theme="cosmo")

main = ttk.Frame(app.window, padding=16)
main.pack(fill="both", expand=True)

ttk.Label(main, text="Quick details").grid(row=0, column=0, columnspan=2, pady=(0, 10))
ttk.Entry(main, bootstyle="info").grid(row=1, column=0, padx=(0, 8))
ttk.Button(main, text="Submit", bootstyle="success").grid(row=1, column=1)

ttk.Progressbar(main, bootstyle="info-striped", mode="indeterminate").grid(
    row=2, column=0, columnspan=2, pady=(12, 0), sticky="ew"
)

app.window.columnconfigure(0, weight=1)
main.columnconfigure((0, 1), weight=1)
app.mainloop()
```

## Tips

- Use `bootstyle` color/variant tokens (e.g., `primary`, `warning-outline`) to keep widgets aligned with the theme’s colors and styles.
- Wrap content in `ttk.Frame` or `ttk.Labelframe` for spacing and structure.
- Call `ttk.set_theme("cosmo")` or `ttk.toggle_theme()` to adjust the palette while the app runs.
