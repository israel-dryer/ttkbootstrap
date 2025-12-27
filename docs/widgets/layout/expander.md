---
title: Expander
---

# Expander

`Expander` is a **collapsible container** with a clickable header (title + chevron) and expandable content area.

It provides a way to show/hide content sections, reducing visual clutter while keeping related controls accessible.

<!--
IMAGE: Collapsible section with chevron
Suggested: Expander titled "Settings" with checkboxes inside, shown expanded and collapsed
Theme variants: light / dark
-->

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

exp = ttk.Expander(app, title="Settings")
exp.pack(fill="x", padx=10, pady=5)

content = exp.add()
ttk.CheckButton(content, text="Enable notifications").pack(anchor="w")
ttk.CheckButton(content, text="Dark mode").pack(anchor="w")
ttk.CheckButton(content, text="Auto-save").pack(anchor="w")

app.mainloop()
```

---

## When to use

Use `Expander` when:

- you want to hide optional or advanced settings by default

- screen space is limited and content can be revealed on demand

- grouping related controls under a collapsible header improves scanability

**Consider a different control when:**

- content should always be visible -- use [LabelFrame](labelframe.md) or [Frame](frame.md)

- you need multiple exclusive sections (only one open at a time) -- consider building an Accordion from multiple Expanders

- you need tabbed navigation -- use [Notebook](../views/notebook.md)

---

## Appearance

### Styling

The chevron button uses `foreground-ghost` by default for a subtle appearance.
When `bootstyle` is provided, the chevron inherits that style.

```python
ttk.Expander(app, title="Primary Section", bootstyle="primary")
```

### Border

Use `show_border=True` to add a visible border around the expander.

```python
ttk.Expander(app, title="Bordered", show_border=True)
```

### Custom icons

Override the default chevron icons with custom ones.

```python
ttk.Expander(
    app,
    title="Custom Icons",
    icon_expanded={'name': 'dash', 'size': 16},
    icon_collapsed={'name': 'plus', 'size': 16},
)
```

### Icon position

Place the chevron before or after the title.

```python
ttk.Expander(app, title="Icon Before", icon_position="before")
ttk.Expander(app, title="Icon After", icon_position="after")  # default
```

---

## Examples & patterns

### Adding content

Use `add()` to get a content frame for placing widgets.

```python
exp = ttk.Expander(app, title="Options")
exp.pack(fill="x", padx=10, pady=5)

content = exp.add()  # Returns a Frame
ttk.Label(content, text="Option 1").pack()
ttk.Entry(content).pack(fill="x")
```

Calling `add()` multiple times returns the same frame (idempotent).

### Starting collapsed

Set `expanded=False` to start in collapsed state.

```python
exp = ttk.Expander(app, title="Advanced", expanded=False)
```

### Non-collapsible section

Set `collapsible=False` to create a section that cannot be toggled (always visible, no chevron).

```python
exp = ttk.Expander(app, title="Always Visible", collapsible=False)
```

### Programmatic control

```python
exp.expand()    # Expand the content
exp.collapse()  # Collapse the content
exp.toggle()    # Toggle current state

# Property access
if exp.expanded:
    print("Currently expanded")

exp.expanded = False  # Collapse via property
```

### Responding to toggle events

```python
def on_toggle(event):
    print(f"Expanded: {event.data['expanded']}")

exp.on_toggle(on_toggle)
```

Or bind directly:

```python
exp.bind('<<Toggle>>', lambda e: print(e.data))
```

### Expand/Collapse all

```python
expanders = [exp1, exp2, exp3]

def expand_all():
    for e in expanders:
        e.expand()

def collapse_all():
    for e in expanders:
        e.collapse()
```

---

## Behavior

- Clicking anywhere on the header toggles the content (not just the chevron).

- Keyboard accessible: focus the header, then press `Enter` or `Space` to toggle.

- The `<<Toggle>>` event fires with `event.data = {'expanded': bool}`.

- Content uses `pack_forget()`/`pack()` for show/hide, so layout reflows automatically.

---

## Configuration

### Dynamic configuration

```python
exp.configure(title="New Title")
exp.configure(collapsible=False)
exp.configure(icon_expanded={'name': 'caret-up', 'size': 14})
```

---

## Additional resources

### Related widgets

- [LabelFrame](labelframe.md) -- always-visible labeled container

- [Frame](frame.md) -- general-purpose container

- [Notebook](../views/notebook.md) -- tabbed content switching

- [PanedWindow](panedwindow.md) -- resizable split panes

### Framework concepts

- [Layout Properties](../../capabilities/layout-props.md)

- [Layout](../../platform/geometry-and-layout.md)

### API reference

- [`ttkbootstrap.Expander`](../../reference/widgets/Expander.md)
