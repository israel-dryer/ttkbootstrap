---
title: DialogName
---

# DialogName

1–2 paragraphs describing:

- what kind of dialog this is

- what task it supports (confirmation, picking, configuration, etc.)

- whether it is modal, popover-like, or hybrid

Mention what it is built on if relevant (e.g., `Dialog`, `FormDialog`, `Calendar`).

---

## Framework integration

**Application & Windows**

- Modality expectations (local grab, focus behavior, parent/child relationship)

- Window behaviors (transient, always-on-top, resize rules)

**Design System**

- How the dialog uses theme tokens (surface, borders, typography)

- Button variants and semantic emphasis

**Signals & Events**

- How results are surfaced (`.result`, virtual events, callbacks)

- Reactive usage patterns (optional)

**Localization**

- How labels and messages participate in localization

- Formatting of values (dates/numbers) if applicable

Keep this section about *expected behavior*, not a full list of options.

---

## Basic usage

Show the most common usage pattern.

This usually includes:

- creating the dialog

- calling `.show()`

- reading the result

```python
dlg = DialogName(app, ...)
dlg.show()

print(dlg.result)
```

If the dialog supports alternate presentation (popover / anchored), show one short example.

---

## What problem it solves

Explain why this dialog exists instead of:

- building a fully custom dialog

- embedding the widget inline

- using a simpler `MessageBox`

Focus on developer ergonomics and UX benefits.

---

## Core concepts

Explain the dialog’s mental model.

Examples:

- modal vs popover behavior

- blocking vs non-blocking flow

- select vs confirm vs cancel semantics

- safety guarantees (what closes the dialog, what doesn’t)

Use subsections if needed:

### Modal vs popover

### Confirming vs cancelling

---

## Result value

Explain clearly:

- what `.result` contains

- its type

- what `None` means

- when it is set

```python
dlg.result  # <type> or None
```

!!! note
    The dialog only produces a result when the user explicitly confirms.

---

## Common options

Document the options most users will configure, such as:

- title

- initial value

- bounds / constraints

- buttons / defaults

- visual flags (icons, window chrome, modality)

Avoid dumping the full API.

---

## Events

Explain dialog-level events.

Common patterns:

- `<<DialogResult>>`

- `on_result(...)`

- payload structure (`confirmed`, `result`)

```python
def on_result(payload):
    ...

dlg.on_result(on_result)
```

---

## UX guidance

Prescriptive advice:

- when to use modal vs popover

- how to label buttons

- how to avoid interrupting users

- accessibility and focus considerations

This section is design guidance, not API documentation.

---

## When to use / when not to

**Use DialogName when:**

- …

**Avoid DialogName when:**

- …

Always point to another concrete widget as the alternative.

---

## Additional resources

**Related widgets**

- **OtherDialog** — how it differs

- **Dialog** — generic dialog builder

- **Toast** — non-blocking alternative

- **FormDialog** — multi-input dialogs

**Framework concepts**

- [Windows](../../platform/windows.md)

- [Signals & Events](../../capabilities/signals/index.md)

- [Localization](../../capabilities/localization.md)

**API reference**

- **API Reference:** `ttkbootstrap.DialogName`

- **Related guides:** Dialogs, UX Patterns, Localization
