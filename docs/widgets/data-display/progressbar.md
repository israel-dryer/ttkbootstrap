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

title: Progressbar
---

# Progressbar

`Progressbar` displays **task progress over time**.

It communicates how much work has completed (determinate) or that work is ongoing (indeterminate), without requiring user interaction.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

pb = ttk.Progressbar(app, maximum=100, value=40)
pb.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

---

## Value model

- **Determinate**: shows progress between `0` and `maximum`

- **Indeterminate**: animates continuously to indicate ongoing work

```python
pb.configure(mode="indeterminate")
pb.start()
```

---

## Common options

- `value`

- `maximum`

- `mode="determinate" | "indeterminate"`

- `length`

- `orient="horizontal" | "vertical"`

---

## Behavior

- Determinate mode updates visually as `value` changes

- Indeterminate mode runs an animation until stopped

---

## Styling

Use `bootstyle` to indicate intent or severity:

```python
ttk.Progressbar(app, bootstyle="success")
ttk.Progressbar(app, bootstyle="warning")
```

---

## When should I use Progressbar?

Use Progressbar when:

- progress is linear and measurable

- users benefit from seeing completion percentage

Prefer **Meter** when:

- you want a more expressive, dashboard-style indicator

---

## Related widgets

- **Meter**

- **FloodGauge**

- **Spinner / BusyIndicator** (if available)

---

## Reference

- **API Reference:** `ttkbootstrap.Progressbar`

---

## Additional resources

### Related widgets

- [Badge](badge.md)

- [FloodGauge](floodgauge.md)

- [Label](label.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.Progressbar`](../../reference/widgets/Progressbar.md)
