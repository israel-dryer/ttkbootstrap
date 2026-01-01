---
title: Tabs
---

# Tabs

`Tabs` is a **tab bar container** that groups `TabItem` widgets into a horizontal or vertical navigation strip.

It manages tab layout, selection state, and optional features like close buttons and an "add" button
for dynamic tab creation.

<!--
IMAGE: Tabs variants
Suggested: Horizontal bar tabs, pill tabs, vertical tabs
Theme variants: light / dark
-->

---

## Quick start

Create a tab bar with selectable tabs:

```python
import ttkbootstrap as ttk

app = ttk.App()

tabs = ttk.Tabs(app)
tabs.pack(fill="x", padx=10, pady=10)

tabs.add(text="Home", icon="house")
tabs.add(text="Files", icon="folder2")
tabs.add(text="Settings", icon="gear")

def on_tab_changed(value):
    print(f"Selected: {value}")

tabs.on_tab_changed(on_tab_changed)

app.mainloop()
```

---

## When to use

Use `Tabs` when:

- you need a standalone tab bar without content switching

- you're building custom navigation where tabs control external content

- you want fine-grained control over tab behavior

Consider a different control when:

- you need tabs with integrated content panels - use [TabView](../views/tabview.md) instead

- navigation is sequential/flow-based - use [PageStack](../views/pagestack.md) instead

---

## Appearance

### Variants

Tabs supports two visual variants:

| Variant | Description |
|---------|-------------|
| `bar` | Default style with underline indicator and divider |
| `pill` | Rounded pill-style tabs without divider |

```python
# Bar variant (default)
tabs = ttk.Tabs(app, variant="bar")

# Pill variant
tabs = ttk.Tabs(app, variant="pill")
```

### Orientation

Tabs can be horizontal or vertical:

```python
# Horizontal (default)
tabs = ttk.Tabs(app, orient="horizontal")

# Vertical
tabs = ttk.Tabs(app, orient="vertical")
```

### Tab width

Control how tabs size themselves:

```python
# Auto-size to content (default)
tabs = ttk.Tabs(app, tab_width=None)

# Fixed character width
tabs = ttk.Tabs(app, tab_width=12)

# Stretch to fill available space
tabs = ttk.Tabs(app, tab_width="stretch")
```

!!! link "Design System"
    See [Colors & Themes](../../design-system/colors.md) for color customization.

---

## Examples and patterns

### Adding tabs

Use `add()` to create tabs:

```python
tabs.add(text="Documents", icon="file-text")
tabs.add(text="Settings", icon="gear")
```

For advanced use cases like programmatic lookups or removal, supply an explicit `key`:

```python
tabs.add(key="docs", text="Documents", icon="file-text")
tabs.add(key="settings", text="Settings", icon="gear")

# Later: lookup, configure, or remove by key
tabs.item("docs").configure(text="My Documents")
tabs.configure_item("settings", state="disabled")
tabs.remove("docs")
```

### Selection state

Track selection via the `on_tab_changed` callback:

```python
def handle_change(value):
    print(f"Now selected: {value}")

tabs.on_tab_changed(handle_change)
```

Or use the Signal API:

```python
tabs.signal.subscribe(lambda v: print(v))
```

Get/set selection programmatically:

```python
current = tabs.get()
tabs.set("settings")
```

### Closable tabs

Enable close buttons on tabs:

```python
# Always visible close buttons
tabs = ttk.Tabs(app, enable_closing=True)

# Close buttons visible on hover only
tabs = ttk.Tabs(app, enable_closing="hover")
```

Handle close events:

```python
def on_close():
    print("Tab closed")

tabs.add(text="Document", close_command=on_close)
```

### Add button

Show an "add" button for dynamic tab creation:

```python
tabs = ttk.Tabs(app, enable_adding=True)

def on_add(event):
    tabs.add(text="New Tab")

tabs.on_tab_added(on_add)
```

### Events

Tabs emits virtual events:

- `<<TabSelect>>` - when a tab is selected
- `<<TabClose>>` - when a tab's close button is clicked
- `<<TabAdd>>` - when the add button is clicked

```python
tabs.bind("<<TabSelect>>", lambda e: print("Tab selected"))
```

---

## Behavior

### UX guidance

- Use consistent tab styling within a region

- Limit horizontal tabs to 5-7 items for scannability

- Use icons with text for better recognition

- Vertical tabs work well for settings-style navigation

!!! tip "Pair with content"
    For tabs that switch content, use [TabView](../views/tabview.md) which combines
    Tabs with a PageStack automatically.

---

## Additional resources

### Related widgets

- [TabView](../views/tabview.md) - tabs with integrated content switching

- [PageStack](../views/pagestack.md) - stack-based navigation

- [Notebook](../views/notebook.md) - traditional tabbed container

- [SideNav](sidenav.md) - vertical navigation list

### API reference

- [`ttkbootstrap.Tabs`](../../reference/widgets/Tabs.md)
