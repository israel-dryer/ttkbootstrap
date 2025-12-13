---
title: PasswordEntry
icon: fontawesome/solid/lock
---


# PasswordEntry

`PasswordEntry` is a **Field-based password control** that automatically masks characters and adds a visibility toggle so users can verify their input without compromising security.

It layers the label/message/validation infrastructure of `Field` with a press-and-hold eye icon that reveals the password temporarily, making it a secure option for login forms, vaults, or credential prompts.

---

## Overview

`PasswordEntry` gives you:

- **Masking** via the `show` option (default `●`), hiding characters as they are typed.
- **Visibility toggle button** (eye icon) that temporarily reveals the password while held.
- **Full `Field` behavior**, including labels, messages, validation hooks, bootstyles, and addon slots.
- **Custom mask characters** if you prefer `•`, `*`, or another glyph.
- **Optional toggle hiding** via `show_visible_toggle=False` when no reveal button is desired.

The widget is built for forms where security and usability must coexist.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(title="Password Entry Demo", theme="cosmo")

password = ttk.PasswordEntry(
    app,
    label="Password",
    message="Must be at least 8 characters",
    required=True
)
password.pack(fill="x", padx=16, pady=8)

pin = ttk.PasswordEntry(
    app,
    label="PIN",
    show="*",
    message="Numeric PIN only",
    show_visible_toggle=False
)
pin.pack(fill="x", padx=16, pady=8)

app.mainloop()
```

---

## Masking, toggle, & validation

- The `show` option controls the mask character (`'●'` by default). Pass `show="*"` for a traditional look.
- The eye icon (visibility toggle) reveals the password only while pressed, preserving privacy when focus leaves the field.
- Toggle visibility can be hidden with `show_visible_toggle=False` for stricter workflows.
- Inherited `Field` validation rules (`required`, `add_validation_rule`, etc.) keep the control ready for secure forms.
- Message labels display hints or validation feedback, and the field emits `<<Valid>>` / `<<Invalid>>` events like any other `Field` widget.

---

## Events & interaction

`PasswordEntry` forwards the standard `Field` events:

- `<<Input>>`: fires on every keystroke (useful for live strength meters or feedback).
- `<<Changed>>`: fires when a new value commits (Enter, blur, etc.).
- `<<Valid>>` / `<<Invalid>>`: report validation state changes triggered by `Field` rules.
- `<<Validated>>`: also available through the inherited `Field` implementation.

The visibility button itself emits `<ButtonPress>`/`<ButtonRelease>` internally to toggle masking, but you rarely need to interact with those bindings directly.

---

## When to use PasswordEntry

Choose `PasswordEntry` for login screens, password creation flows, and any form where secret text needs both masking and optional verification. It guarantees consistent messaging, validation, and bootstyle treatment across your app.

If you only need plain text input, use `TextEntry`. For general-purpose `Entry` fields without labels/messages, prefer `Entry` from `ttkbootstrap.widgets.primitives`.

---

## Related widgets

- `TextEntry`
- `Entry`
- `Form`

