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

title: FormDialog
---

# FormDialog

`FormDialog` is a **modal dialog** that collects multiple related values using a structured form layout.

Use it when a workflow needs a small set of inputs (2–8 fields) with an explicit OK/Cancel outcome.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.FormDialog(
    title="New connection",
    fields=[
        {"key": "host", "label": "Host", "required": True},
        {"key": "port", "label": "Port", "value": 5432},
        {"key": "user", "label": "User"},
    ],
)
result = dlg.show()

print("result:", result)  # dict or None (implementation-dependent)
app.mainloop()
```

---

## Value model

Form dialogs typically return:

- a dict-like result mapping field keys to committed values, or

- `None` when cancelled

---

## Common options

- `title`

- `fields` — form field definitions

- `initial` — initial values (if supported)

- `validate_on_submit` — run validation before accepting (if supported)

---

## Events

Most form dialogs are handled via return value.
If your dialog emits validation lifecycle events, use them for UX only (messages/state), not as the primary result.

---

## Validation and constraints

Use field-level validation:

- required fields

- type parsing (int/float/date)

- cross-field rules (password confirmation, ranges)

For complex “live” forms, prefer an inline **Form** in a normal window or a PageStack flow.

---

## When should I use FormDialog?

Use `FormDialog` when:

- you need several inputs at once

- the user should commit/cancel explicitly

- the inputs are part of a single small task

Prefer **QueryBox** when:

- you only need one value

Prefer **PageStack** when:

- the flow is multi-step or requires navigation

---

## Related widgets

- **Dialog** — base dialog API

- **QueryBox** — single-value prompts

- **Form** — inline multi-field form layouts

- **PageStack** — multi-step workflows

---

## Reference

- **API Reference:** `ttkbootstrap.FormDialog`

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

- [`ttkbootstrap.FormDialog`](../../reference/widgets/FormDialog.md)
