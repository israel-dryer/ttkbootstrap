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

title: FloodGauge
---

# FloodGauge

`FloodGauge` is a **filled-level indicator** that visualizes how full a value is within a range.

It’s especially useful for capacity, utilization, or threshold-based indicators.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

fg = ttk.FloodGauge(app, value=75)
fg.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

---

## Value model

- `value` represents fill level (commonly 0–100)

- optional thresholds can alter styling

---

## Common options

- `value`

- `maximum`

- `text`

- `orient`

---

## Styling

Flood gauges often change color as thresholds are crossed:

```python
ttk.FloodGauge(app, bootstyle="warning")
```

---

## When should I use FloodGauge?

Use FloodGauge when:

- capacity or fullness matters

- thresholds are more important than exact numbers

---

## Related widgets

- **Progressbar**

- **Meter**

---

## Reference

- **API Reference:** `ttkbootstrap.FloodGauge`

---

## Additional resources

### Related widgets

- [Badge](badge.md)

- [Label](label.md)

- [ListView](listview.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.FloodGauge`](../../reference/widgets/FloodGauge.md)
