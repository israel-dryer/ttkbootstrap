---
title: Notebook
icon: fontawesome/solid/folder
---

# Notebook

`Notebook` is a themed tabbed container widget. It extends `ttk.Notebook` with ttkbootstrap styling, **key-based tab referencing**, optional **auto-generated tab keys**, and **enriched tab lifecycle events** that tell you *what changed* and *why*.

<!--
IMAGE: Notebook overview
Suggested: Notebook with 3 tabs (Home/Settings/About) in both light and dark themes
Theme variants: light / dark
-->

---

## Basic usage

Create a notebook and add tab frames:

```python
import ttkbootstrap as ttk

app = ttk.App()

nb = ttk.Notebook(app, bootstyle="primary")
nb.pack(fill="both", expand=True, padx=20, pady=20)

home = nb.add_frame(label="Home", key="home", frame_options=dict(padding=10))
settings = nb.add_frame(label="Settings", key="settings", frame_options=dict(padding=10))

ttk.Label(home, text="Home content").pack(anchor="w")
ttk.Label(settings, text="Settings content").pack(anchor="w")

app.mainloop()
```

<!--
IMAGE: Basic Notebook example
Suggested: Notebook with two tabs, each showing distinct content
-->

You can also add existing widgets as tabs:

```python
import ttkbootstrap as ttk

app = ttk.App()

nb = ttk.Notebook(app)
nb.pack(fill="both", expand=True)

page = ttk.Frame(nb, padding=10)
ttk.Label(page, text="I was created outside the notebook").pack(anchor="w")

nb.add(page, key="external", text="External")

app.mainloop()
```

---

## What problem it solves

Tabbed layouts are a classic desktop pattern for switching between related views without opening new windows. ttkbootstrap’s `Notebook` improves the standard `ttk.Notebook` by adding:

- **Stable tab keys** so you can reference tabs without relying on fragile indices
- **Auto keys** (`tab1`, `tab2`, …) when you don’t provide one
- **Hide/show and remove** helpers that keep the internal registry consistent
- **Enriched events** that include `current`, `previous`, `reason`, and `via`
- Built-in support for **bootstyle**, `surface_color`, and style options

---

## Core concepts

### Tabs can be referenced by key, index, or widget

Most notebook APIs accept a “tab reference” that can be:

- **key** (`str`) — recommended (stable, human-friendly)
- **index** (`int`) — 0-based position in the tab bar
- **widget** — the actual child widget used as the tab content

Examples:

```python
nb.select("settings")    # by key
nb.select(0)             # by index
nb.select(settings)      # by widget
```

!!! tip "Prefer keys"
    Indices change when tabs are inserted, removed, or reordered. Keys remain stable across those operations.

---

### Creating tabs with `add_frame` and `insert_frame`

`add_frame(...)` is the fastest way to create a new tab page:

```python
page = nb.add_frame(label="Logs", key="logs", frame_options=dict(padding=10))
```

To insert at a specific position:

```python
page = nb.insert_frame(0, label="Start", key="start", frame_options=dict(padding=10))
```

Both methods create a `ttk.Frame` tab for you and return it.

---

### Tab labels can be localized

`Notebook` supports a translation-aware `text` token on tabs. If you pass a translation key, it is translated immediately and automatically refreshed when the locale changes.

You can also provide formatting arguments via `fmtargs`.

```python
nb.add(page, key="recent", text="tabs.recent", fmtargs=("Today",))
```

!!! note "Tokens vs literal strings"
    If your `text` value is a localization token, it will be retranslated on locale changes.
    If it’s a literal string, it is used as-is.

---

## Common options & patterns

### Hide and show tabs

Hide a tab without removing it:

```python
nb.hide("settings")
```

To remove a tab and clean its registry entries, use `remove(...)`:

```python
nb.remove("settings")
```

!!! tip "Hide vs remove"
    Use `hide(...)` when you want to temporarily remove a tab from the bar.
    Use `remove(...)` when the tab should be forgotten and its key should no longer be valid.

---

### Disable a tab

Tabs can be disabled using `tab(...)` configuration:

```python
nb.tab("settings", state="disabled")
```

---

### Reorder tabs

Use `insert(...)` to reorder existing tabs by moving a widget to a new index (or insert a new one). Keys remain stable even if indices change.

---

## Events

`Notebook` emits enriched lifecycle events:

- `<<NotebookTabChanged>>`
- `<<NotebookTabActivated>>`
- `<<NotebookTabDeactivated>>`

Prefer the helper methods to subscribe/unsubscribe:

```python
def on_changed(event):
    data = getattr(event, "data", None) or {}
    print("current:", data.get("current"))
    print("previous:", data.get("previous"))
    print("reason:", data.get("reason"))
    print("via:", data.get("via"))

nb.on_tab_changed(on_changed)
```

To unbind, keep the returned `funcid`:

```python
funcid = nb.on_tab_changed(on_changed)
nb.off_tab_changed(funcid)
```

### Event payload

For `on_tab_changed(...)`, `event.data` includes:

- `current`: `{index, key, label}` or `None`
- `previous`: `{index, key, label}` or `None`
- `reason`: `"user" | "api" | "hide" | "forget" | "reorder" | "unknown"`
- `via`: `"click" | "key" | "programmatic" | "unknown"`

<!--
IMAGE: Notebook event payload
Suggested: Diagram showing previous -> current transition and reason/via fields
-->

!!! tip "Track navigation state"
    Use `reason` and `via` to distinguish user clicks from programmatic navigation (e.g., wizard flow, validation redirects).

---

## UX guidance

- Keep tab labels short and scannable
- Avoid putting too many tabs in one notebook (consider grouping or side navigation)
- Use `hide(...)` for feature flags or permission-based tabs
- Use `on_tab_changed(...)` to persist the last selected tab between sessions

---

## When to use / when not to

**Use Notebook when:**

- You have multiple related views that share the same window area
- Switching views should be fast and non-destructive
- You want a familiar desktop “tabs” experience

**Avoid Notebook when:**

- The workflow is sequential (use `PageStack` / wizard flow)
- You have many sections that don’t fit as tabs (consider sidebar navigation)
- Tab contents are heavy and should load lazily (consider on-demand creation)

---

## Related widgets

- **PageStack** — view switching for step-by-step navigation or wizards
- **Frame** — common page container inside tabs
- **PanedWindow** — split layouts often paired with tabbed views
