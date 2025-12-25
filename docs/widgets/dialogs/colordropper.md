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

title: ColorDropper
---

# ColorDropper

`ColorDropper` is a **screen color picker** that lets users sample a color from anywhere on the screen.

It’s useful for design tools, theme editors, and workflows where the desired color already exists in the UI.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

color = ttk.ColorDropper().show()
print("color:", color)  # hex / rgb / None

app.mainloop()
```

---

## Value model

A color dropper produces:

- the sampled color value (hex/rgb), or

- `None` if cancelled

---

## Behavior

Common interaction pattern:

- activating the dropper enters “pick mode”

- moving the cursor previews the sampled color (implementation-dependent)

- clicking commits the sample

- Escape cancels

---

## When should I use ColorDropper?

Use `ColorDropper` when:

- users need to match a color already on screen

- sampling is faster than choosing from palettes

Prefer **ColorChooser** when:

- users need to browse/select from a palette with previews

---

## Related widgets

- **ColorChooser** — palette-based color dialog

- **Dialog** — base dialog API

---

## Reference

- **API Reference:** `ttkbootstrap.ColorDropper`

---

## Additional resources

### Related widgets

- [ColorChooser](colorchooser.md)

- [DateDialog](datedialog.md)

- [Dialog](dialog.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.ColorDropper`](../../reference/widgets/ColorDropper.md)
