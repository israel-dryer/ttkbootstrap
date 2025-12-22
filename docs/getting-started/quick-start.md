---
title: Quickstart
---

# Quickstart (5-Minute App)

This quickstart gets a themed ttkbootstrap window on screen in just a few minutes.

You will:

- install the package,
- create a minimal application,
- run it,
- and learn how to change themes at runtime.

The goal is to give you a **working mental model**, not to introduce every feature.

---

## 1. Verify Prerequisites

Make sure your environment meets these requirements:

- **Python 3.10 or newer**, with Tk support  
  (Tk 8.6 ships with most official Python installers)

- Verify your interpreter:
  ```bash
  python --version
  python -m pip --version
  ```

- Upgrade pip to ensure the latest wheels are used:
  ```bash
  python -m pip install --upgrade pip
  ```

---

## 2. Install ttkbootstrap

Install the package using pip:

```bash
python -m pip install ttkbootstrap
```

Optional:

- Use a virtual environment for isolation
- Pin a specific version if needed:
  ```bash
  python -m pip install ttkbootstrap==2.0.0
  ```

---

## 3. Create a Minimal Application

Create a file named `main.py` with the following contents:

```python
import ttkbootstrap as ttk

app = ttk.App(theme="solar")

frame = ttk.Frame(app.window, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Welcome to ttkbootstrap v2").pack(pady=(0, 10))
ttk.Button(frame, text="Launch", bootstyle="success").pack()

app.mainloop()
```

This example demonstrates:

- the application shell,
- a container-driven layout,
- semantic styling via bootstyle tokens,
- and theme-aware widgets.

---

## 4. Run the Application

Run the script from your terminal:

```bash
python main.py
```

You should see a themed window appear immediately.

---

## 5. Change Themes at Runtime

Themes can be changed without restarting the application.

Common helpers include:

- Apply a specific theme:
  ```python
  ttk.set_theme("cosmo")
  ```

- Toggle between light and dark variants:
  ```python
  ttk.toggle_theme()
  ```

- List available themes:
  ```python
  ttk.get_themes()
  ```

All widgets update automatically when the theme changes.

---

## 6. Next Steps

Once you have this running, you can:

- explore additional **Widgets** such as inputs, dialogs, and data views,
- read **First Application** to understand layout and structure more deeply,
- review **Installation** for advanced setup and extras,
- explore the **Design System** to understand color, typography, layout, and interaction patterns.

This quickstart is intentionally simple—everything else builds on this foundation.
