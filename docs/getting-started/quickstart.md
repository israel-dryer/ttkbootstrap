---
icon: fontawesome/solid/rocket
---

# Quickstart (5-Minute App)

Get a themed Tk window on screen and configure a couple of controls without leaving this page. The following steps walk through the prerequisites, install, and runtime helpers you need for a runnable ttkbootstrap 2 app.

![Quickstart hero](https://placehold.co/800x800/FFFFFF/333333.webp?text=Quickstart&font=lato)

## 1. Verify prerequisites

- Python 3.10 or newer with Tk support (Tk 8.6 ships with most installers).
- python --version and python -m pip --version confirm the interpreter matches the requirement.
- Upgrade pip before installing to keep wheels current: python -m pip install --upgrade pip.

## 2. Install the package

`ash
python -m pip install ttkbootstrap
`

Use pipx install ttkbootstrap to isolate the CLI helpers, or pin the version (	tkbootstrap==2.0.0) if you need to freeze dependencies.

## 3. Create the minimal app

Save this to main.py:

`python
from ttkbootstrap import ttk

app = ttk.App(theme="solar")

frame = ttk.Frame(app.window, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Welcome to ttkbootstrap 2").pack(pady=(0, 10))
ttk.Button(frame, bootstyle="success", text="Launch").pack()

app.mainloop()
`

## 4. Run it

`
python main.py
`

## 5. Tweak themes at runtime

- 	tk.set_theme("cosmo") applies a specific registered theme without restarting the app.
- 	tk.toggle_theme() switches between light and dark palettes on demand.
- Explore Style.list_themes() if you need to populate a selector of available palettes.

## 6. Next steps

- Build on this frame by experimenting with inputs, data display widgets, and Bootstyle tokens.
- Read the Installation and First Application pages for runtime helpers and layout guidance.
- Visit the Design system section to align your widgets with shared colors, typography, and stateful variants.
