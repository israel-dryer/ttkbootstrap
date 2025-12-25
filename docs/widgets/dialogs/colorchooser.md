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

title: ColorChooser
---

# ColorChooser

`ColorChooser` is a **color picker dialog** for selecting a color and returning the chosen value.

Use it when you want a standard “pick a color → OK/Cancel” flow for theming, drawing tools, labels, or settings.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

color = ttk.ColorChooser(
    title="Choose a color",
    initial="#3b82f6",
).show()

print("color:", color)  # hex / rgb / None
app.mainloop()
```

---

## Value model

Color chooser dialogs typically return:

- a committed color value (hex string or rgb tuple), or

- `None` when cancelled

---

## Common options

- `title`

- `initial` (starting color)

- `format` (hex/rgb) if supported

---

## Behavior

- OK commits the color

- Cancel closes without committing

- Enter confirms, Escape cancels (typical)

---

## When should I use ColorChooser?

Use `ColorChooser` when:

- users pick a color occasionally

- an explicit confirm/cancel flow is appropriate

Prefer **ColorDropper** when:

- users need to pick a color from the screen

Prefer inline color swatches when:

- users frequently change colors and need immediate feedback

---

## Related widgets

- **ColorDropper** — pick a color from the screen

- **Dialog** — base dialog API

- **MessageBox** — confirmations/alerts

---

## Reference

- **API Reference:** `ttkbootstrap.ColorChooser`

---

## Additional resources

### Related widgets

- [ColorDropper](colordropper.md)

- [DateDialog](datedialog.md)

- [Dialog](dialog.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.ColorChooser`](../../reference/widgets/ColorChooser.md)
