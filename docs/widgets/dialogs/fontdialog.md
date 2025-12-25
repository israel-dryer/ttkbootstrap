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

title: FontDialog
---

# FontDialog

`FontDialog` is a **modal font picker** that lets users choose a font family, size, and style, then confirm or cancel.

Use it for editor-like features (rich text, labels, code editors) where users need a standard font selection experience.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.FontDialog(title="Choose a font")
result = dlg.show()

print("font:", result)  # font string/object or None
app.mainloop()
```

---

## Value model

Font dialogs typically return:

- a committed font spec (string, tuple, or object), or

- `None` when cancelled

---

## Common options

- `title`

- `initial_font` (if supported)

- preview sample text (if supported)

---

## Behavior

- OK commits the selected font

- Cancel closes without committing

- Enter confirms, Escape cancels (typical)

---

## When should I use FontDialog?

Use `FontDialog` when:

- font choice is part of a user customization workflow

- you want a standard modal picker

Prefer inline font controls when:

- font selection is a frequent, always-visible control (toolbars)

---

## Related widgets

- **Dialog** — base dialog API

- **FormDialog** — structured multi-field input

- **MessageBox** — confirmations/alerts

---

## Reference

- **API Reference:** `ttkbootstrap.FontDialog`

---

## Additional resources

### Related widgets

- [ColorChooser](colorchooser.md)

- [ColorDropper](colordropper.md)

- [DateDialog](datedialog.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.FontDialog`](../../reference/widgets/FontDialog.md)
