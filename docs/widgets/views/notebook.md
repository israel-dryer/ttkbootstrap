---
title: Notebook
icon: fontawesome/solid/folder
---


# Notebook

`Notebook` is a themed tabbed container with enhanced navigation, localization helpers, and lifecycle events that makes multi-pane layouts feel consistent with the rest of the ttkbootstrap design system.

---

## Overview

Notebook extends `ttk.Notebook` by:

- accepting `bootstyle`, `surface_color`, and `style_options` so the tab bar colors match your palette while still giving you native padding/height/width options.
- allowing tabs to be referenced by auto-generated or explicit keys (`tab1`, `'settings'`, widget instances, or indices) for reliable API control.
- exposing `add_frame()`/`insert_frame()` helpers that create ergonomic frame panes with optional localization tokens.
- emitting enriched events (`<<NotebookTabChanged>>`, `<<NotebookTabActivated>>`, `<<NotebookTabDeactivated>>`) whose `.data` payload includes the current/previous tab metadata plus reason/via information.
- supporting hide/show operations (`hide`, `forget`) that keep the tab registry in sync so you can temporarily remove tabs without rebuilding the widget.

Use Notebook for dashboards, tabbed settings panels, or any UI where you need a fixed tab bar with themed styling and predictable navigation.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

nb = ttk.Notebook(app, bootstyle="secondary")
nb.pack(fill="both", expand=True, padx=16, pady=16)

home = ttk.Frame(nb, padding=16)
ttk.Label(home, text="Home content").pack()
nb.add(home, text="Home", key="home")

settings = ttk.Frame(nb, padding=16)
ttk.Label(settings, text="Settings content").pack()
nb.add(settings, text="Settings", key="settings")

nb.on_tab_changed(lambda e: print("Tab changed:", e.data))

app.mainloop()
```

---

## Tabs & events

- Each tab can specify `state`, `sticky`, `padding`, `text`, `compound`, `image`, `underline`, etc., through `add()`/`tab()` calls.
- Use keys or widget references to switch tabs: `nb.select("settings")`, `nb.hide("home")`, or `nb.index(widget)`.
- The event data from `<<NotebookTabChanged>>` includes `current`/`previous` tab refs and `reason` (`'user'`, `'api'`, `'hide'`, `'forget'`, `'reorder'`) plus `via` (`'click'`, `'key'`, `'programmatic'`).
- Bind `on_tab_activated`/`on_tab_deactivated` helpers to react specifically when tabs gain or lose focus.
- Localization tokens stored via `fmtargs` are refreshed automatically when the `<<LocaleChanged>>` event fires.

---

## When to use Notebook

Pick Notebook for tabbed panels where the active tab should remain themed, easily referenced, and capable of reporting why it changed. For wizards consider `PageStack`; for groups of fields use `Frame`/`LabelFrame` inside each tab pane.

---

## Related widgets

- `Frame` / `LabelFrame` (tab content holders)
- `Pane` (PanedWindow for split views)
- `PageStack` (wizard-style navigation)
