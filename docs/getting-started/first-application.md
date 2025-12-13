---
icon: fontawesome/solid/play
---

# First Application

The first real window puts the shell, layout containers, and styled widgets together so you have a runnable ttkbootstrap 2 program. This page details the anatomy of a simple app, includes a sample, and highlights the runtime theming hooks you will reuse everywhere.

![Application diagram](https://placehold.co/800x800/FFFFFF/333333.webp?text=App%20Structure&font=lato)

## Anatomy
1. **App shell** - `ttk.App(title="ttkbootstrap 2 First App", theme="solar")` instantiates a theme-aware window, exposes the root, and keeps DPI scaling under control.
2. **Layout containers** - `Frame`, `Labelframe`, `ScrollView`, or the new `PageStack` nodes organize widgets while letting you control padding, stretching, and focus order.
3. **Widgets & data** - Inputs, data display widgets, and progress indicators all respect the shared Bootstyle tokens and typography tokens you pick.

## Sample application

```python
from ttkbootstrap import ttk

app = ttk.App(title="ttkbootstrap 2 First App", theme="solar")

main = ttk.Frame(app.window, padding=16)
main.pack(fill="both", expand=True)

ttk.Label(main, text="Quick details").grid(row=0, column=0, columnspan=2, pady=(0, 10))
ttk.Entry(main, bootstyle="info", width=20).grid(row=1, column=0, padx=(0, 8))
ttk.Button(main, text="Submit", bootstyle="success-outline", width=12).grid(row=1, column=1)

ttk.Progressbar(main, bootstyle="info-striped", mode="indeterminate").grid(
    row=2, column=0, columnspan=2, pady=(12, 0), sticky="ew"
)

main.columnconfigure((0, 1), weight=1)
app.mainloop()
```

## Runtime theming

- Call `ttk.set_theme("cosmo")` to lock into a specific registered palette.
- Use `ttk.toggle_theme()` to switch between the light and dark variants bundled with most themes.
- `Style.list_themes()` returns the names you can present in a selector or settings dialog.

## Styling tips

- Use `bootstyle` color and variant tokens to update the widget with consistent theme colors and styles (for example, `bootstyle="success-outline"`, `info-striped`, or `primary-link`).
- Let `Style.colors` or a custom `ThemeProvider` anchor your colors instead of hardcoding hex values so the tokens stay tied to the current palette.
- Wrap groups of inputs in `ttk.Frame` or `ttk.Labelframe` to control spacing and align with the layout guidance in the design system.
