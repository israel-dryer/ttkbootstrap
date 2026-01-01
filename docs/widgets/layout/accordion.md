---
title: Accordion
---

# Accordion

`Accordion` is a **container of collapsible sections** where expanding one section can automatically collapse the others.

It manages a group of [Expander](expander.md) widgets, providing mutual exclusion behavior and optional constraints like requiring at least one section to remain open.

<!--
IMAGE: Accordion with multiple sections, one expanded
Suggested: Three sections labeled "General", "Advanced", "About" with "General" expanded
Theme variants: light / dark
-->

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

accordion = ttk.Accordion(app, color="primary", variant="solid")
accordion.pack(fill="x", padx=10, pady=10)

section1 = accordion.add(title="General Settings")
ttk.CheckButton(section1.content, text="Enable feature").pack(anchor="w")

section2 = accordion.add(title="Advanced Settings")
ttk.Label(section2.content, text="Advanced options here").pack()

section3 = accordion.add(title="About")
ttk.Label(section3.content, text="Version 1.0").pack()

app.mainloop()
```

---

## When to use

Use `Accordion` when:

- you have multiple related sections and want only one visible at a time

- screen space is limited and mutual exclusion helps focus attention

- you want a structured, step-by-step flow (e.g., wizard-like forms)

**Consider a different control when:**

- sections should be independently collapsible -- use multiple [Expander](expander.md) widgets

- content switching should use tabs -- use [Notebook](../views/notebook.md)

- all sections should always be visible -- use [LabelFrame](labelframe.md) or [Frame](frame.md)

---

## Appearance

### Styling

Pass `color` and `variant` to apply a consistent style to all managed expanders.

```python
ttk.Accordion(app, color="success", variant="solid")
```

### Border

Use `show_border=True` to add a visible border around the accordion container.

```python
ttk.Accordion(app, show_border=True)
```

### Separators

Use `show_separators=True` to add horizontal separators between sections.

```python
ttk.Accordion(app, show_separators=True)
```

---

## Examples & patterns

### Adding sections

Use `add()` to create new expander sections. It returns the `Expander` widget.

```python
accordion = ttk.Accordion(app)
accordion.pack(fill="x")

section = accordion.add(title="Section Title", icon={'name': 'gear', 'size': 16})
ttk.Label(section.content, text="Section content").pack()
```

### Adding existing expanders

You can add pre-created `Expander` widgets:

```python
exp = ttk.Expander(accordion, title="Custom Expander")
accordion.add(exp)
```

### Removing sections

Use `remove()` to remove a section by its key:

```python
# Add with explicit key
section = accordion.add(key="temp", title="Temporary")

# Remove by key
accordion.remove("temp")

# Get all keys
for key in accordion.keys():
    print(key)
```

### Multiple selection mode

By default, only one section can be open at a time. Set `allow_multiple=True` to allow multiple sections to be open simultaneously.

```python
accordion = ttk.Accordion(app, allow_multiple=True)
```

### Non-collapsible mode

Set `allow_collapse_all=False` to require at least one section to remain open. The first section is automatically expanded.

```python
accordion = ttk.Accordion(app, allow_collapse_all=False)
```

### Starting with a section expanded

```python
section1 = accordion.add(title="First", expanded=True)
section2 = accordion.add(title="Second")  # collapsed by default
```

### Programmatic control

```python
accordion.expand("section1")   # Expand by key
accordion.collapse("section2") # Collapse by key

# With allow_multiple=True only:
accordion.expand_all()
accordion.collapse_all()

# Access expanders
for exp in accordion.items():
    print(exp.cget('title'))

# Get currently expanded sections
for exp in accordion.expanded:
    print(f"Open: {exp.cget('title')}")

# Query configuration
if accordion.cget('allow_multiple'):
    print("Multiple selection enabled")
```

### Responding to changes

```python
def on_accordion_changed(event):
    expanded = event.data['expanded']
    titles = [exp.cget('title') for exp in expanded]
    print(f"Open sections: {titles}")

accordion.on_accordion_changed(on_accordion_changed)
```

---

## Behavior

- When `allow_multiple=False` (default), opening one section closes all others.

- When `allow_collapse_all=False`, attempting to close the last open section is prevented.

- The `<<AccordionChange>>` event fires with `event.data = {'expanded': list[Expander]}`.

- All managed expanders automatically have `highlight=True` set to show selection state.

- Keyboard accessible: Tab to navigate between sections, Enter/Space to toggle.

---

## Configuration

### Construction options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `allow_multiple` | bool | `False` | Allow multiple sections open at once |
| `allow_collapse_all` | bool | `True` | Allow all sections to be closed |
| `show_separators` | bool | `False` | Show separators between sections |
| `color` | str | `None` | Color applied to all expanders |
| `variant` | str | `None` | Variant applied to all expanders |

---

## Additional resources

### Related widgets

- [Expander](expander.md) -- individual collapsible section

- [Notebook](../views/notebook.md) -- tabbed content switching

- [LabelFrame](labelframe.md) -- always-visible labeled container

- [Frame](frame.md) -- general-purpose container

### Framework concepts

- [Layout Properties](../../capabilities/layout-props.md)

- [Layout](../../platform/geometry-and-layout.md)

### API reference

- [`ttkbootstrap.Accordion`](../../reference/widgets/Accordion.md)