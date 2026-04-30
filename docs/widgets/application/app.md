---
title: App
---

# App

`App` is the **root application window** — the starting point for every ttkbootstrap application.

It wraps Tk with sensible defaults: theme initialization, DPI awareness, window sizing, and shortcut management.

<figure markdown>
![app](../../assets/dark/widgets-app.png#only-dark)
![app](../../assets/light/widgets-app.png#only-light)
</figure>

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App(title="My App", theme="cosmo", size=(800, 600))

ttk.Label(app, text="Hello, world!").pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use `App` when:

- you need a basic application window without built-in navigation

- you want full control over the layout

Consider a different control when:

- you need a sidebar + toolbar + page scaffold — use [AppShell](appshell.md)

- you need a secondary window — use [Toplevel](toplevel.md)

---

## Examples and patterns

### Window configuration

```python
app = ttk.App(
    title="My App",
    theme="cosmo-dark",
    size=(1024, 768),
    position=(100, 100),
    minsize=(640, 480),
    resizable=(True, True),
)
```

### Theme switching

```python
ttk.set_theme("flatly-dark")
ttk.toggle_theme()  # switches between light and dark
```

!!! note "macOS: window close ≠ quit"
    On macOS, `App` installs native quit behavior by default: clicking the close
    button **hides** the app (it stays in the Dock). **Cmd+Q** is the
    platform-conventional quit gesture.

    To restore cross-platform destroy-on-close behavior:
    ```python
    app = ttk.App(settings={"macos_quit_behavior": "classic"})
    ```
    See [Platform Differences](../../platform/platform-differences.md) for details.

---

## Additional resources

### Related widgets

- [AppShell](appshell.md) — app window with built-in navigation

- [Toplevel](toplevel.md) — secondary windows

### API reference

- [`ttkbootstrap.App`](../../reference/app/App.md)
