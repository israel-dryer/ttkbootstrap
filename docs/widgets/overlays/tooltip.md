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

title: Tooltip
---

# Tooltip

`Tooltip` is a **contextual overlay** that appears on hover (or focus) to provide brief help or explanations.

Use tooltips for:

- icon-only buttons

- dense toolbars

- exposing extra detail without cluttering the UI

Tooltips should be short, readable, and optional.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

btn = ttk.Button(app, text="Refresh")
btn.pack(padx=20, pady=20)

ttk.Tooltip(btn, text="Reload the current view")
app.mainloop()
```

---

## Behavior

- Appears on hover (and optionally focus)

- Disappears on leave or after a delay

- Should not steal focus or block interaction

---

## Common options

- `text`

- `delay` (time before showing)

- `wraplength` (max line width)

- `bootstyle` (if supported)

---

## When should I use Tooltip?

Use Tooltip when:

- the control meaning isn’t obvious (especially icon-only UI)

- you want “learnable” UI without permanent labels

Avoid tooltips when:

- the text is essential to completing the task (use labels or inline help)

---

## Related widgets

- **Toast** — non-blocking notifications

- **MessageBox** — blocking alerts and confirmations

---

## Reference

- **API Reference:** `ttkbootstrap.Tooltip`

---

## Additional resources

### Related widgets

- [Toast](toast.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.ToolTip`](../../reference/widgets/ToolTip.md)
