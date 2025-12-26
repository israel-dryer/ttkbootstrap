---
title: Label
---

# Label

`Label` displays **read-only text or images**.

It's a fundamental building block used for headings, captions, instructions, and status text throughout an interface.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Hello world").pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use Label when:

- displaying static text or images

- providing context or instructions

- showing status information that doesn't require user interaction

### Consider a different control when...

- **User input is required** — use [Entry](../primitives/entry.md) or [TextEntry](../inputs/textentry.md) instead

- **You need a compact status indicator** — use [Badge](badge.md) for high-contrast pill-style labels

- **You need interactive text** — use [Button](../actions/button.md) for clickable elements

---

## Appearance

### Styling with `bootstyle`

Labels participate fully in ttkbootstrap theming:

```python
ttk.Label(app, text="Info", bootstyle="info")
ttk.Label(app, text="Muted", bootstyle="secondary")
ttk.Label(app, text="Warning", bootstyle="warning")
```

!!! link "Design System"
    See [Design System](../../design-system/index.md) for color tokens and theming guidelines.

---

## Examples & patterns

### Common options

- `text` — the text content to display

- `image` — an image to display

- `compound` — how to combine text and image (`"top"`, `"bottom"`, `"left"`, `"right"`, `"center"`)

- `anchor` — where to position content within the label

- `justify` — text alignment (`"left"`, `"center"`, `"right"`)

- `wraplength` — maximum line width before wrapping

### Text alignment

```python
ttk.Label(app, text="Left aligned", anchor="w").pack(fill="x")
ttk.Label(app, text="Centered", anchor="center").pack(fill="x")
ttk.Label(app, text="Right aligned", anchor="e").pack(fill="x")
```

### Image with text

```python
ttk.Label(app, text="Status", image=icon, compound="left").pack()
```

---

## Behavior

Label is a static display widget. It does not respond to user interaction by default, but can be updated programmatically.

---

## Localization

Label supports localization through the `localize` parameter:

```python
ttk.Label(app, text="greeting.hello", localize=True)
```

!!! link "Localization"
    See [Localization](../../capabilities/localization.md) for translation setup.

---

## Reactivity

Label can be updated dynamically by binding to signals:

```python
message = ttk.Signal("Initial text")
label = ttk.Label(app, text=message)
message.set("Updated text")  # Label updates automatically
```

!!! link "Signals"
    See [Signals](../../capabilities/signals/signals.md) for reactive programming patterns.

---

## Additional resources

### Related widgets

- [Button](../actions/button.md) — interactive clickable element

- [Badge](badge.md) — compact status indicator

- [Tooltip](../overlays/tooltip.md) — contextual hover information

### Framework concepts

- [Design System](../../design-system/index.md) — colors, typography, and theming

- [Signals](../../capabilities/signals/signals.md) — reactive data binding

- [Localization](../../capabilities/localization.md) — translation support

### API reference

- [`ttkbootstrap.Label`](../../reference/widgets/Label.md)