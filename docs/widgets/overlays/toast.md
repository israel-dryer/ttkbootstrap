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

title: Toast
---

# Toast

`Toast` is a **non-blocking notification overlay** used to show brief feedback without interrupting the workflow.

Use Toast for messages like “Saved”, “Copied”, or “Connected”. Toasts should disappear automatically and should not require user action.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Toast(
    app,
    title="Saved",
    message="Your changes were saved successfully.",
).show()

app.mainloop()
```

---

## Behavior

- Non-modal (does not block)

- Auto-dismiss after a short duration (typically configurable)

- Usually stacks if multiple toasts are shown

- Click-to-dismiss is common (if supported)

---

## Common options

- `title`

- `message`

- `duration` (auto-hide delay)

- `bootstyle` / intent (info/success/warning/error)

---

## When should I use Toast?

Use Toast when:

- feedback is helpful but not critical

- the user should not be interrupted

Prefer **MessageBox** when:

- the user must confirm or decide something

Prefer inline messaging when:

- the feedback is tied to a specific control (validation, helper text)

---

## Related widgets

- **Tooltip** — contextual hover help

- **MessageBox** — modal alerts and confirmations

---

## Reference

- **API Reference:** `ttkbootstrap.Toast`

---

## Additional resources

### Related widgets

- [ToolTip](tooltip.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.Toast`](../../reference/widgets/Toast.md)
