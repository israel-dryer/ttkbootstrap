---
title: PageStack
icon: fontawesome/solid/layer-group
---


# PageStack

`PageStack` is a navigation container that manages multiple `Frame` pages with browser-like history, notifying lifecycle events and retaining themed styling from `Frame`.

---

## Overview

Highlights:

- Add pages via `add(key, widget)` or `add_page(key, **frame_kwargs)`; each key must be unique and can carry bootstyle/surface overrides via `PageOptions`.
- Navigate with `navigate(key, data=None, replace=False)`, and use `back()`/`forward()` to walk the history—`page`, `prev_page`, `nav`, `index`, `length`, `can_back`, and `can_forward` appear on the event payloads.
- Events such as `<<PageChanged>>`, `<<PageMounted>>`, `<<PageWillMount>>`, and `<<PageUnmounted>>` expose rich data that includes `reason`, `prev_data`, and `can_*` flags.
- `configure_page(key, ...)`, `remove(key)`, and `current()` let you inspect or mutate pages directly; `can_back()`/`can_forward()` help keep navigation buttons in sync.

Use `PageStack` for wizard flows, master/detail panes, or any multi-view layout where you want built-in history without plumbing your own stack logic.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

stack = ttk.PageStack(app)
stack.pack(fill="both", expand=True, padx=16, pady=16)

home = stack.add_page("home", padding=12, bootstyle="secondary")
ttk.Label(home, text="Home page").pack()

settings = stack.add_page("settings", padding=12)
ttk.Label(settings, text="Settings page").pack()

ttk.Button(app, text="Go to settings", command=lambda: stack.navigate("settings")).pack(pady=8)
ttk.Button(app, text="Back", command=stack.back).pack()

stack.navigate("home")

app.mainloop()
```

---

## History & lifecycle

- Navigation events carry context in `event.data`: `page`, `prev_page`, `prev_data`, `nav` ('push', 'back', 'forward'), `index`, `length`, `can_back`, `can_forward`.
- The widget records lifecycle so you can trigger animation when `<<PageMounted>>` fires or clean up when `<<PageUnmounted>>` triggers.
- Pass arbitrary `data` dicts through `navigate()` to share context between pages; the history retains the data for `back()`/`forward()` navigation.
- Call `navigate(..., replace=True)` to swap the current history entry instead of appending a new one.

---

## When to use PageStack

Choose `PageStack` for workflows with multiple discrete screens, such as wizards, form flows, or embedded views that should remember where the user has been. For simple tabbed experiences, prefer `Notebook`; for full window navigation use `NavigationManager`.

---

## Related widgets

- `Frame` (each page container)
- `Notebook` (tabbed pane alternative)
