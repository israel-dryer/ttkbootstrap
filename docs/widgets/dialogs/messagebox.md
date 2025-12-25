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

title: MessageBox
---

# MessageBox

`MessageBox` is a **modal feedback dialog** for communicating information and collecting simple user confirmation.

It supports common dialog types like info, warning, error, question/confirm, and can return a result indicating what the user chose.

Use MessageBox for:

- confirmations (Delete? Quit without saving?)

- error reporting (Something failed)

- simple alerts (Action completed)

<!--
IMAGE: MessageBox examples
Suggested: 3 small dialogs (info/warning/error) in light/dark
-->

---

## Basic usage

### Information

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.MessageBox.ok(
    title="Saved",
    message="Your changes have been saved.",
)

app.mainloop()
```

### Confirm / question

```python
result = ttk.MessageBox.yesno(
    title="Delete file?",
    message="This action can't be undone.",
)
print("User chose:", result)  # typically True/False or "Yes"/"No"
```

---

## Value model

Message boxes return a **single committed choice** (or no value if dismissed):

- OK-only dialogs → no decision, just acknowledgement

- Yes/No, OK/Cancel → one decision

- Retry/Cancel → one decision for error recovery

Return values vary by implementation (bool, string token, enum). Treat the result as your source of truth.

---

## Common options

### `title` and `message`

```python
ttk.MessageBox.ok(title="Notice", message="Hello!")
```

### Detail / secondary text (if supported)

Use detail text for stack traces or extra explanation.

```python
ttk.MessageBox.show(
    title="Import failed",
    message="Could not import the file.",
    detail="The file format was not recognized.",
    icon="error",
    buttons=("OK",),
)
```

### Parent / positioning (if supported)

Pass a parent to keep the dialog on top of the correct window.

```python
ttk.MessageBox.ok(parent=app, title="Saved", message="Done.")
```

---

## Common dialog types

Most apps stick to a small set of patterns:

- **Info** — success/neutral notification

- **Warning** — proceed with caution

- **Error** — operation failed

- **Question** — user must choose

Use the highest-level helper that matches your intent (e.g., `ok`, `yesno`, `okcancel`) to keep UI consistent.

---

## Behavior

- Opens as **modal** (blocks interaction until dismissed)

- Escape typically cancels (when cancel is available)

- Enter typically activates the default action (OK/Yes)

Keep messages short, actionable, and avoid putting long text in the main message line.

---

## When should I use MessageBox?

Use `MessageBox` when:

- you need the user to acknowledge or decide something before continuing

- the decision is simple (1–3 buttons)

- the dialog should be modal

Prefer **Toast** when:

- you want non-blocking feedback (Saved!, Copied!)

Prefer **Tooltip** or inline messaging when:

- feedback is contextual and shouldn’t interrupt workflow

---

## Related widgets

- **Toast** — non-blocking notifications

- **Tooltip** — contextual help

- **DateDialog** — modal date selection dialog

---

## Reference

- **API Reference:** `ttkbootstrap.MessageBox`

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

- [`ttkbootstrap.MessageBox`](../../reference/widgets/MessageBox.md)
