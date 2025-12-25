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

title: Label
---

# Label

`Label` displays **read-only text or images**.

It’s a fundamental building block used for headings, captions, instructions, and status text throughout an interface.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Hello world").pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

- `text`

- `image`

- `compound`

- `anchor`

- `justify`

- `wraplength`

---

## Styling

Labels participate fully in ttkbootstrap theming:

```python
ttk.Label(app, text="Info", bootstyle="info")
ttk.Label(app, text="Muted", bootstyle="secondary")
```

---

## When should I use Label?

Use Label when:

- displaying static text or images

- providing context or instructions

Prefer **Entry / TextEntry** when:

- user input is required

---

## Related widgets

- **Button**

- **Badge**

- **Tooltip**

---

## Reference

- **API Reference:** `ttkbootstrap.Label`

---

## Additional resources

### Related widgets

- [Badge](badge.md)

- [FloodGauge](floodgauge.md)

- [ListView](listview.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.Label`](../../reference/widgets/Label.md)
