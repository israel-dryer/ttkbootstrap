---
title: WidgetName
---

# WidgetName

1–2 paragraphs that say:

- what kind of dialog this is (confirmation, picking, configuration…)
- whether it's modal, popover-like, or hybrid
- what it's built on, if relevant (e.g. `Dialog`, `FormDialog`, `Calendar`)

The intro carries the "what is this and why does it exist" framing.
There's no separate `What problem it solves` / `Core concepts` /
`Framework integration` section — those collapse into the intro plus
the sections below.

---

## Basic usage

The most common usage pattern: construct, `.show()`, read the result.

```python
import ttkbootstrap as ttk

dlg = WidgetName(...)
dlg.show()

print(dlg.result)
```

If the dialog supports an alternate presentation (popover, anchored),
show one short example here.

---

## Result value

The dialog's central concern: what comes out of it.

Document:

- what `.result` contains and its type
- what `None` means (and when it occurs)
- when `.result` is set (after `.show()` returns? on button click?)

```python
dlg.result  # <type> or None
```

For dialogs whose result is a structured value (form data, color
spec, font choice), describe the shape here. For dialogs that don't
have a `.result` (static-method facades like `MessageBox`), this
section becomes the "what the call returns" section instead.

---

## Common options

Curated — the options users actually configure. Avoid full API dumps.

Typical:

- title
- initial value / message
- bounds, constraints
- buttons / defaults
- icons or window chrome
- modality flags

Show one or two compact examples. Theme tokens (`accent`, `variant`)
go here when relevant; localization callouts can be a `!!! note`
inline rather than a separate section.

---

## Behavior

Modality, focus, and lifecycle rules:

- modal / popover / sheet behavior
- default-button binding (Enter)
- cancel binding (Escape)
- focus and grab semantics
- transient relationship to parent
- `alert=True` and any side effects of `.show()`

If the dialog has a non-blocking variant or auto-dismiss, document
it here.

---

## Events

The lifecycle hooks the dialog exposes.

Common patterns:

- `<<DialogResult>>` virtual event
- `on_result(...)` / `on_dismissed(...)` helpers
- payload shape (`{"result": ..., "confirmed": bool}`)

```python
def handle(payload):
    ...

dlg.on_dialog_result(handle)
```

If the dialog has no events (facades, static methods), state that
explicitly and link to the underlying class instead.

---

## UX guidance

*Optional — include only when there's prescriptive advice the reader
won't derive from the API.*

Examples:

- when to use modal vs popover
- how to label buttons (verbs > "OK"/"Cancel")
- destructive-button placement and default-button rules
- when to ring the system bell
- focus and accessibility considerations

Skip this section for base classes, builders, or specialty interactions
where UX advice doesn't apply.

---

## When should I use WidgetName?

Use WidgetName when:

- …

Prefer OtherDialog when:

- …

Always point to a concrete alternative (`MessageBox` / `QueryDialog`
/ `FormDialog` / inline widget / non-modal toast).

---

## Additional resources

**Related widgets**

- **OtherDialog** — how it differs
- **Dialog** — generic dialog builder
- **FormDialog** — multi-input dialogs

**Framework concepts**

- [Windows](../platform/windows.md)
- [Localization](../capabilities/localization.md)

**API reference**

- **API reference:** `ttkbootstrap.WidgetName`
- **Related guides:** Dialogs, UX Patterns, Localization
