---
title: FormDialog
---

# FormDialog

`FormDialog` is a modal dialog that wraps a [`Form`](../inputs/form.md)
composite in a `Dialog` shell with an OK/Cancel footer. Calling
`show()` blocks until the user submits or cancels; the form's data —
keyed by field name — is then available on `.result`.

It's the right shape for a small, self-contained data-entry task
(2–8 related fields) that should commit atomically: a "new
connection" prompt, an item editor, a settings group. For richer
workflows that the user will live in for more than a few seconds,
embed a `Form` directly in a [`PageStack`](../views/pagestack.md) or
panel instead.

---

## Basic usage

The simplest form is inferred from a `data` dict — keys become field
names, types become editor choices:

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.FormDialog(
    title="New connection",
    data={"host": "", "port": 5432, "user": ""},
)
dlg.show()

if dlg.result is not None:
    print("submitted:", dlg.result)

app.mainloop()
```

For anything beyond a flat list of inputs, pass `items` explicitly:

```python
dlg = ttk.FormDialog(
    title="New connection",
    data={"host": "", "port": 5432, "user": "", "tls": False},
    items=[
        {"key": "host", "label": "Host"},
        {"key": "port", "label": "Port", "dtype": "int"},
        {"key": "user", "label": "User"},
        {"key": "tls",  "label": "Use TLS"},
    ],
    col_count=2,
)
dlg.show()
```

`show()` blocks the caller. After it returns, branch on `.result is
not None` (an empty form may still legitimately submit `{}` —
checking truthiness can drop valid submissions).

---

## Result value

`.result` is the **form data dict** when the user submitted, or
`None` when the user cancelled or dismissed the window:

```python
dlg.result  # dict[str, Any] or None
```

Values are **coerced by `dtype`** before being returned: a field
declared `dtype="int"` (or with an int default value) is parsed back
to `int` even though the underlying entry stores text. The supported
dtype tokens are `"int"` / `"float"` / `"bool"` / `"date"` /
`"datetime"` / `"password"` / `"str"` (or the corresponding Python
types). When parsing fails, the raw string is returned — validation
rules on the field should catch that case before the dialog closes.

The result dict contains **every key that was in the original
`data`**, plus any keys declared via `items`. Fields the user
didn't touch retain their initial values.

`FormDialog` does **not** fire a `<<DialogResult>>` virtual event
(unlike `MessageDialog` and `QueryDialog`). To react to submission
without blocking, attach a `command` callback to a button (see
[Events](#events)) or read `.result` after `show()` returns.

---

## Common options

| Option | Purpose |
|---|---|
| `title` | Window title. Default `"Form"`. |
| `data` | Initial values; keys become field names when `items` is omitted. |
| `items` | Explicit form layout — a sequence of `FieldItem` / `GroupItem` / `TabsItem` (or equivalent dicts). When omitted, fields are inferred from `data` keys and value types. |
| `col_count` | Number of grid columns at the top level. Default `1`. |
| `min_col_width` | Minimum width per column, in pixels. Default `DEFAULT_MIN_COL_WIDTH`. |
| `on_data_changed` | Callback invoked with the full data dict each time any field's value changes. Use it for live UI updates; it is **not** the submission callback. |
| `buttons` | Footer buttons. Each can be a `DialogButton`, a mapping, or a string. Default is `["Cancel", "OK"]` (cancel + primary roles). The first button appears rightmost. |
| `mode` | `"modal"` (grab + wait) or `"popover"` (no grab + wait). Default `"modal"`. |
| `alert` | If `True`, plays the system alert sound on `show()`. Default `False`. |
| `resizable` | Bool or `(width, height)` tuple of bools. Default `False` (non-resizable). |
| `minsize` / `maxsize` | `(width, height)` tuples. Defaults are auto-calculated from `col_count * min_col_width`. |
| `width` / `height` | Explicit form size; if omitted, the dialog sizes to fit. |
| `scrollview_options` | Mapping forwarded to the internal `ScrollView` (`scrollbar_visibility`, `autohide_delay`). |
| `master` | Parent window. Defaults to the application root. |

```python
dlg = ttk.FormDialog(
    title="Edit profile",
    data={"name": "", "email": "", "newsletter": True},
    items=[
        {"key": "name",       "label": "Display name"},
        {"key": "email",      "label": "Email", "dtype": "str"},
        {"key": "newsletter", "label": "Subscribe to updates",
         "editor": "switch"},
    ],
    buttons=[
        {"text": "Cancel", "role": "cancel"},
        {"text": "Save",   "role": "primary", "default": True},
    ],
    resizable=(True, False),
)
```

!!! note "Localization caveat"
    The default buttons render the literal strings `"button.cancel"`
    and `"button.ok"` — the same translation-key gotcha as
    `MessageDialog`. Pass explicit button labels (or rely on a
    locale catalog that translates those keys) for any user-facing
    dialog.

For richer layouts — labelled groups, tabbed forms, custom editors
per field — see the [`Form` widget](../inputs/form.md), which
documents the full `FieldItem` / `GroupItem` / `TabsItem` shape.
`FormDialog` forwards `items` to it verbatim.

---

## Behavior

### Modality and lifecycle

`FormDialog` opens a `Toplevel` transient to its parent. In `"modal"`
mode the parent is grabbed and `show()` does not return until the
user dismisses the dialog. In `"popover"` mode there is no grab, but
`show()` still waits — useful for a focused-but-not-blocking task.

`show()` accepts the same anchoring options as
[`Dialog.show`](dialog.md): `anchor_to`, `anchor_point`,
`window_point`, `offset`, `auto_flip`. With no `position=` and no
anchor, the dialog centers on its parent.

### Validation on submit

Pressing any non-cancel button runs `Form.validate()` first:

- If every field passes its rules, the dialog stores `form.data` on
  `.result` and closes.
- If any field fails, the dialog **stays open**, the first invalid
  field is focused, and inline validation messages appear on the
  failing fields.

Validation only runs on submission — fields can also have live
("input"-trigger) rules that surface inline errors as the user
types, but those don't block the dialog by themselves. See
[Validation rules](../../capabilities/validation.md) for how to
attach rules to a `Field`.

The cancel button skips validation entirely; cancelling always
closes the dialog and leaves `.result` as `None`.

### Custom button commands

A button's `command` callback receives the **`FormDialog`
instance** (not the underlying `Dialog`). Returning `False` from the
callback aborts the close — useful for extra confirmation steps:

```python
def confirm_overwrite(dlg):
    if dlg.form.data["force"]:
        return  # let the dialog close normally
    if not ttk.MessageBox.yesno("Overwrite existing record?", master=dlg.toplevel):
        return False  # keep the form open

ttk.FormDialog(
    data={"name": "", "force": False},
    buttons=[
        {"text": "Cancel", "role": "cancel"},
        {"text": "Save", "role": "primary", "default": True,
         "command": confirm_overwrite},
    ],
).show()
```

### Default and Escape bindings

Mark a button with `default=True` to make it the **Enter** target
(it also receives focus and the primary accent). Any button with
`role="cancel"` is wired to **Escape**; if no cancel-role button is
present, Escape destroys the dialog with `.result = None`.

### Scrolling

The internal layout always wraps the form in a vertical
`ScrollView`. The scrollbar is visible at all times by default (to
prevent layout jumps when content fits and then doesn't); pass
`scrollview_options={"scrollbar_visibility": "auto"}` to hide it
when not needed.

---

## Events

`FormDialog` doesn't fire a result-style virtual event. The hooks
available are:

| Hook | Fires |
|---|---|
| `on_data_changed(data_dict)` | Each time a field's value changes (live), with the full updated dict. Set via the constructor argument. |
| Button `command(dlg)` | Once per button press, before the dialog closes. Receives the `FormDialog` instance. Return `False` to keep the dialog open. |

For an event-style submission hook, attach a `command` to the
primary button instead of polling `.result`:

```python
def on_submit(dlg):
    save_record(dlg.form.data)

ttk.FormDialog(
    data={"name": "", "email": ""},
    buttons=[
        {"text": "Cancel", "role": "cancel"},
        {"text": "Save", "role": "primary", "default": True,
         "command": on_submit},
    ],
).show()
```

The form widget itself fires field-level validation events
(`<<Valid>>`, `<<Invalid>>`, `<<Validated>>`) on each `Field` — bind
those on `dlg.form.field(key)` if you want to react to validation
state without waiting for submit.

---

## UX guidance

- **Keep the field count small.** Two to eight related inputs is
  the sweet spot. Beyond that, the modal feels like a barrier — split
  into a wizard ([`PageStack`](../views/pagestack.md)) or move the
  form inline onto a page.
- **Label primary buttons with the action**, not "OK". "Save",
  "Create", "Connect" tell the user what will happen when they hit
  Enter; "OK" doesn't.
- **Group related fields** with a `GroupItem` (visible label) when
  the form has more than one logical section. A flat eight-field
  form reads as a wall; the same fields under two labelled groups
  reads as structured.
- **Don't open another modal from a FormDialog button.** If the
  primary action needs a confirmation, use the button's `command`
  callback to inline a [`MessageBox.yesno`](messagebox.md) and abort
  the close on rejection — don't push a second `FormDialog` on top.
- **Reserve `alert=True`** for forms that interrupt the user
  (validation errors needing attention). Routine "new item" prompts
  shouldn't ring the system bell.

---

## When should I use FormDialog?

Use FormDialog when:

- you need 2–8 related inputs collected together with an explicit
  commit/cancel choice.
- the inputs are part of a single, atomic task (creating a record,
  editing settings, configuring a connection).
- the workflow is naturally modal — the user shouldn't continue
  with the parent window until they've answered.

Prefer a different control when:

- you need exactly one value → use [`QueryDialog`](querydialog.md)
  or [`QueryBox`](querybox.md).
- you need a yes/no/confirmation, not data entry → use
  [`MessageBox`](messagebox.md) or [`MessageDialog`](messagedialog.md).
- the form is large, multi-step, or the user will spend more than a
  minute in it → embed a [`Form`](../inputs/form.md) directly in a
  page or [`PageStack`](../views/pagestack.md) flow.
- you need full control of the layout and footer (custom widgets
  beside the buttons, non-form content) → drop down to
  [`Dialog`](dialog.md).

---

## Additional resources

**Related widgets**

- [`Form`](../inputs/form.md) — the inline composite that powers
  `FormDialog`. Use it directly when the form lives in a page, not a
  modal.
- [`Dialog`](dialog.md) — the generic builder underneath; reach for
  it when `FormDialog`'s OK/Cancel footer doesn't fit.
- [`QueryDialog`](querydialog.md) — single-value modal prompt.
- [`MessageDialog`](messagedialog.md) — message + button-row modal.
- [`PageStack`](../views/pagestack.md) — multi-step / wizard
  alternative for larger workflows.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)
- [Validation rules](../../capabilities/validation.md)

**API reference**

- **API reference:** [`ttkbootstrap.FormDialog`](../../reference/dialogs/FormDialog.md)
- **Related guides:** Dialogs, Forms, Validation
