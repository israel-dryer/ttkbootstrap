---
icon: fontawesome/solid/rocket
---

# Quickstart (5-Minute App)

This page mirrors the “5-minute app” so you can bootstrap a themed window and a few widgets without reading the full reference. The entire flow should take less than five minutes if your environment is ready.

![Quickstart hero](https://placehold.co/800x800/FFFFFF/333333.webp?text=Quickstart&font=lato)

## 1. Install the package

```bash
python -m pip install ttkbootstrap
```

## 2. Create a minimal app

Save the following to `main.py`:

```python
from ttkbootstrap import ttk

app = ttk.App(theme="solar")

frame = ttk.Frame(app.window, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Welcome to ttkbootstrap 2").pack(pady=(0, 10))
ttk.Button(frame, bootstyle="success", text="Launch").pack()

app.mainloop()
```

Run it:

```bash
python main.py
```

## 3. Next steps

- Switch the theme by calling `ttk.set_theme("cyborg")` or reopen the app with a different `theme` argument.
- Toggle between light and dark with `ttk.toggle_theme()`.
- Inspect other widgets in the new catalog (see Widgets → Inputs/Data Display/Feedback).
- Check the Guides section for runtime, theming, and deployment advice once the UI is stable.
