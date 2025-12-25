---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


---

title: Notebook
---

# Notebook

`Notebook` is a **tabbed view container** that shows one page at a time and lets users switch views by clicking tabs.

ttkbootstrap’s `Notebook` extends `ttk.Notebook` with:

- **key-based tab references** (stable, human-friendly)

- optional **auto-generated keys**

- helpers for **hide/show/remove** while keeping the tab registry consistent

- **enriched tab lifecycle events** that describe *what changed* and *why* fileciteturn17file0

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

You can also add an existing widget as a tab:

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

## Core concepts

### Tab references

Most notebook APIs accept a “tab reference” that can be:

- **key** (`str`) — recommended (stable)

- **index** (`int`) — 0-based position

- **widget** — the tab’s content widget

```python
nb.select("settings")    # by key
nb.select(0)             # by index
nb.select(settings)      # by widget
```

!!! tip "Prefer keys"
    Indices change when tabs are inserted, removed, or reordered. Keys remain stable.

### Creating tabs with `add_frame` and `insert_frame`

`add_frame(...)` creates a new `Frame` tab and returns it:

```python
page = nb.add_frame(label="Logs", key="logs", frame_options=dict(padding=10))
```

Use `insert_frame(...)` to insert at a specific position:

```python
page = nb.insert_frame(0, label="Start", key="start", frame_options=dict(padding=10))
```

### Localized tab labels

`Notebook` supports translation-aware tab text (tokens retranslate on locale changes). You can also provide formatting args:

```python
nb.add(page, key="recent", text="tabs.recent", fmtargs=("Today",))
```

---

## Common patterns

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

---

## Events

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

- `via`: `"click" | "key" | "programmatic" | "unknown"` fileciteturn17file0

!!! tip "Track navigation state"
    Use `reason` and `via` to distinguish user clicks from programmatic navigation (wizards, validation redirects).

---

## UX guidance

- Keep tab labels short and scannable

- Avoid too many tabs in one notebook (consider grouping or alternative navigation)

- Use `hide(...)` for permission-based tabs

- Use `on_tab_changed(...)` to persist the last selected tab between sessions

---

## When should I use Notebook?

Use `Notebook` when:

- you have multiple related views sharing the same window area

- switching views should be fast and non-destructive

- you want a familiar desktop “tabs” model

Prefer `PageStack` when:

- the workflow is sequential (wizard/flow)

- back/forward history matters

Avoid tabs when:

- you have many sections that don’t fit well as tabs (consider a side navigation pattern)

---

## Related widgets

- **PageStack** — stacked views with history (wizards/flows)

- **Frame** — common tab page container

- **PanedWindow** — split layouts often paired with view switching

---

## Reference

- **API Reference:** `ttkbootstrap.Notebook`

---

## Additional resources

### Related widgets

- [PageStack](pagestack.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.Notebook`](../../reference/widgets/Notebook.md)
