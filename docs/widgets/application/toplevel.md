---
title: Toplevel
---

# Toplevel

`Toplevel` creates a **secondary window** that shares the application's theme and event loop.

Use it for dialogs, tool palettes, inspectors, or any auxiliary window.

<figure markdown>
![toplevel](../../assets/dark/widgets-toplevel.png#only-dark)
![toplevel](../../assets/light/widgets-toplevel.png#only-light)
</figure>

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App(title="Main Window")

def open_window():
    win = ttk.Toplevel(title="Settings", size=(400, 300))
    ttk.Label(win, text="Secondary window").pack(padx=20, pady=20)

ttk.Button(app, text="Open Window", command=open_window).pack(pady=20)

app.mainloop()
```

---

## When to use

Use `Toplevel` when:

- you need a secondary window (settings panel, inspector, tool palette)

- you need a custom dialog beyond what the built-in dialogs provide

Consider a different control when:

- you need the main application window — use [App](app.md)

- you need a standard dialog — see [Dialogs](../dialogs/index.md)

---

## Additional resources

### Related widgets

- [App](app.md) — main application window

- [AppShell](appshell.md) — app window with built-in navigation

### API reference

- [`ttkbootstrap.Toplevel`](../../reference/app/Toplevel.md)
