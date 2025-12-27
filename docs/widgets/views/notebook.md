---
title: Notebook
---

# Notebook

`Notebook` is a **tabbed view container** that shows one page at a time and lets users switch views by clicking tabs.

ttkbootstrap's `Notebook` extends `ttk.Notebook` with:

- **key-based tab references** (stable, human-friendly)

- optional **auto-generated keys**

- helpers for **hide/show/remove** while keeping the tab registry consistent

- **enriched tab lifecycle events** that describe *what changed* and *why*

<!--
IMAGE: Notebook overview
Suggested: Notebook with 3 tabs (Home/Settings/About) in both light and dark themes
Theme variants: light / dark
-->

---

## Quick start

Create a notebook and add tabs using `add()`:

```python
import ttkbootstrap as ttk

app = ttk.App()

nb = ttk.Notebook(app, bootstyle="primary")
nb.pack(fill="both", expand=True, padx=20, pady=20)

# add() creates a Frame and returns it
home = nb.add(text="Home", key="home")
settings = nb.add(text="Settings", key="settings")

ttk.Label(home, text="Home content").pack(anchor="w", padx=10, pady=10)
ttk.Label(settings, text="Settings content").pack(anchor="w", padx=10, pady=10)

app.mainloop()
```

You can also add an existing widget as a tab:

```python
page = ttk.Frame(nb, padding=10)
ttk.Label(page, text="I was created outside the notebook").pack(anchor="w")

nb.add(page, key="external", text="External")
```

---

## When to use

Use `Notebook` when:

- you have multiple related views sharing the same window area

- switching views should be fast and non-destructive

- you want a familiar desktop "tabs" model

Consider a different control when:

- the workflow is sequential (wizard/flow) - use [PageStack](pagestack.md) instead

- back/forward history matters - use [PageStack](pagestack.md) instead

- you have many sections that don't fit well as tabs - consider a side navigation pattern

---

## Appearance

### Styling

Apply a bootstyle to change the tab accent color:

```python
nb = ttk.Notebook(app, bootstyle="primary")
```

!!! link "Design System"
    See [Colors & Themes](../../design-system/colors.md) for available bootstyle values.

---

## Examples and patterns

### Tab references

Most notebook APIs accept a "tab reference" that can be:

- **key** (`str`) - recommended (stable)

- **index** (`int`) - 0-based position

- **widget** - the tab's content widget

```python
nb.select("settings")    # by key
nb.select(0)             # by index
nb.select(settings)      # by widget
```

!!! tip "Prefer keys"
    Indices change when tabs are inserted, removed, or reordered. Keys remain stable.

### Creating tabs

Use `add()` without a child to create a Frame automatically:

```python
page = nb.add(text="Logs", key="logs")
ttk.Label(page, text="Log content").pack()
```

Use `insert()` to add at a specific position:

```python
page = nb.insert(0, text="Start", key="start")
```

Frame options (padding, bootstyle, etc.) can be passed directly:

```python
page = nb.add(text="Settings", key="settings", padding=10, bootstyle="primary")
```

### Localized tab labels

`Notebook` supports translation-aware tab text (tokens retranslate on locale changes). You can also provide formatting args:

```python
nb.add(page, key="recent", text="tabs.recent", fmtargs=("Today",))
```

### Hide vs remove

Hide a tab without forgetting it:

```python
nb.hide("settings")
```

Remove a tab and clean its registry entry:

```python
nb.remove("settings")
```

!!! tip "Hide vs remove"
    Use `hide(...)` for temporary visibility (feature flags, permissions).
    Use `remove(...)` when the tab should be forgotten entirely.

### Disable a tab

```python
nb.tab("settings", state="disabled")
```

### Reorder tabs

Use `insert(...)` to move a widget to a new index. Keys remain stable even if indices change.

### Events

`Notebook` emits enriched lifecycle events:

- `<<NotebookTabChanged>>`

- `<<NotebookTabActivated>>`

- `<<NotebookTabDeactivated>>`

Use the helper methods to subscribe/unsubscribe:

```python
def on_changed(event):
    data = getattr(event, "data", None) or {}
    print("current:", data.get("current"))
    print("previous:", data.get("previous"))
    print("reason:", data.get("reason"))
    print("via:", data.get("via"))

funcid = nb.on_tab_changed(on_changed)
# nb.off_tab_changed(funcid)
```

### Event payload

For `on_tab_changed(...)`, `event.data` includes:

- `current`: `{index, key, label}` or `None`

- `previous`: `{index, key, label}` or `None`

- `reason`: `"user" | "api" | "hide" | "forget" | "reorder" | "unknown"`

- `via`: `"click" | "key" | "programmatic" | "unknown"`

!!! tip "Track navigation state"
    Use `reason` and `via` to distinguish user clicks from programmatic navigation (wizards, validation redirects).

---

## Behavior

### UX guidance

- Keep tab labels short and scannable

- Avoid too many tabs in one notebook (consider grouping or alternative navigation)

- Use `hide(...)` for permission-based tabs

- Use `on_tab_changed(...)` to persist the last selected tab between sessions

---

## Additional resources

### Related widgets

- [PageStack](pagestack.md) - stacked views with history (wizards/flows)

- [Frame](../layout/frame.md) - common tab page container

- [PanedWindow](../layout/panedwindow.md) - split layouts often paired with view switching

### API reference

- [`ttkbootstrap.Notebook`](../../reference/widgets/Notebook.md)