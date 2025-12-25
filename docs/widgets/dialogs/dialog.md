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

title: Dialog
---

# Dialog

`Dialog` is the base class for building **modal** and **popover** dialogs in ttkbootstrap.

Use dialogs when you need users to **make a decision** or **provide input** before continuing.

---

## Basic usage

Most dialogs follow a pattern like this:

```python
import ttkbootstrap as ttk

app = ttk.App()

dialog = ttk.Dialog(
    title="Dialog title",
    message="Explain what the user needs to do.",
)
result = dialog.show()

print("result:", result)
app.mainloop()
```

---

## Value model

Dialogs produce a **single committed outcome**:

- a result value (string/bool/object), or

- `None` when cancelled/dismissed

---

## Presentation modes

### Modal (default)

Modal dialogs block interaction with the parent window until closed.

Use modal when the user must respond immediately (confirmations, required input).

### Popover

Popover dialogs are lightweight and typically close when focus is lost.

Use popover when the dialog is contextual and low-risk (quick filters, small pickers).

---

## Common options

- `title` — window title

- `message` — primary content text (keep short)

- `parent` — parent window for stacking and focus

- `buttons` — the actions shown (OK/Cancel, Yes/No, etc.)

- `default` — default action activated by Enter (if supported)

---

## Behavior

- **Enter** typically activates the default action.

- **Escape** typically cancels (when cancel is available).

- Closing the window via the title bar is treated like cancel/dismiss.

---

## When should I use Dialog?

Use `Dialog` (or a specialized dialog) when:

- the user must confirm an action

- the user must provide input before continuing

- the flow benefits from an explicit OK/Cancel outcome

Prefer overlays (Toast/Tooltip) when:

- feedback should not block workflow

---

## Related widgets

- **MessageBox** — prebuilt confirmation / alert dialogs

- **QueryBox** — prompt for a single value

- **FormDialog** — prompt for structured multi-field input

- **FilterDialog** — choose filters with confirm/cancel

- **Toast** — non-blocking notification

- **Tooltip** — contextual hover help

---

## Reference

- **API Reference:** `ttkbootstrap.Dialog`

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

- [`ttkbootstrap.Dialog`](../../reference/widgets/Dialog.md)
