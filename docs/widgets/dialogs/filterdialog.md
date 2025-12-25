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

title: FilterDialog
---

# FilterDialog

`FilterDialog` is a **dialog for selecting filters** (often multi-select) with an explicit Apply/Cancel outcome.

Use it when filtering options are too dense for inline controls, or when you want users to review and apply changes all at once.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.FilterDialog(
    title="Filters",
    filters=[
        {"key": "status", "label": "Status", "options": ["New", "In Progress", "Done"]},
        {"key": "priority", "label": "Priority", "options": ["Low", "Medium", "High"]},
    ],
)
result = dlg.show()

print("filters:", result)  # dict-like or None
app.mainloop()
```

---

## Value model

Filter dialogs typically return:

- a dict-like filter state (selected values), or

- `None` when cancelled

---

## Common patterns

- multi-select groups (checkbox lists)

- single-select groups (radio)

- clear/reset actions inside the dialog

---

## Behavior

- Apply commits and closes

- Cancel closes without committing

- Escape cancels (typical)

Popover mode (if supported) works well for quick filter panels.

---

## When should I use FilterDialog?

Use `FilterDialog` when:

- you have many filters and limited space

- apply/cancel is clearer than live filtering

Prefer inline filter controls when:

- there are only a few filters

- live filtering is expected

---

## Related widgets

- **Dialog** — base dialog API

- **FormDialog** — general multi-field input

- **SelectBox** / **CheckButton** — common inline filter controls

---

## Reference

- **API Reference:** `ttkbootstrap.FilterDialog`

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

- [`ttkbootstrap.FilterDialog`](../../reference/widgets/FilterDialog.md)
