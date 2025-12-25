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

title: Meter
---

# Meter

`Meter` displays a **single numeric value within a range**, often as a circular or arc-style gauge.

It’s ideal for dashboards, summaries, and status panels where visual emphasis matters more than precision.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

meter = ttk.Meter(app, amountused=65, amounttotal=100)
meter.pack(padx=20, pady=20)

app.mainloop()
```

---

## Value model

Meters display:

- `amountused` relative to `amounttotal`

- optional text/label overlays

---

## Common options

- `amountused`

- `amounttotal`

- `subtext`

- `stripethickness`

- `interactive=False` (if supported)

---

## Styling

Meters are highly visual and often color-coded:

```python
ttk.Meter(app, bootstyle="success")
ttk.Meter(app, bootstyle="danger")
```

---

## When should I use Meter?

Use Meter when:

- showing a snapshot or status

- visual emphasis is important

Prefer **Progressbar** when:

- tracking task progress over time

---

## Related widgets

- **Progressbar**

- **FloodGauge**

---

## Reference

- **API Reference:** `ttkbootstrap.Meter`

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

- [`ttkbootstrap.Meter`](../../reference/widgets/Meter.md)
