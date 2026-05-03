---
title: Dialog
---

# Dialog

`Dialog` is the **builder-pattern base class** that every modal in
ttkbootstrap is built on. Instead of subclassing, you pass callbacks
that populate the content area and (optionally) the footer, plus a
list of buttons that close the dialog and assign `.result`. Calling
`show()` opens the window, blocks until a button is pressed (or
dismissal), then returns.

Reach for `Dialog` directly when none of the specialized subclasses —
[`MessageDialog`](messagedialog.md), [`QueryDialog`](querydialog.md),
[`FormDialog`](formdialog.md), [`FontDialog`](fontdialog.md),
[`ColorChooserDialog`](colorchooser.md),
[`DateDialog`](datedialog.md),
[`FilterDialog`](filterdialog.md) — cover what you need: a custom
layout, custom button roles, a popover or Cocoa sheet, or a
chromeless frameless window.

---

## Basic usage

Provide a `content_builder` callback that receives a parent `Frame`,
plus a list of button specs. The dialog wires up the layout, packs the
buttons right-to-left, and assigns `.result` from the pressed button.

```python
import ttkbootstrap as ttk

app = ttk.App()

def build(parent):
    ttk.Label(parent, text="Save changes before closing?").pack(
        padx=20, pady=20
    )

dialog = ttk.Dialog(
    title="Unsaved changes",
    content_builder=build,
    buttons=[
        {"text": "Discard", "role": "danger", "result": "discard"},
        {"text": "Cancel",  "role": "cancel", "result": None},
        {"text": "Save",    "role": "primary", "default": True, "result": "save"},
    ],
)
dialog.show()

print(dialog.result)  # "save", "discard", or None
app.mainloop()
```

Buttons are passed as either `DialogButton` instances or plain dicts
with the same fields. Plain strings (`"OK"`, `"Cancel:primary"`) work
on [`MessageDialog`](messagedialog.md), **not** on `Dialog`.

---

## Result value

`dialog.result` is whatever the pressed button's `result=` field was.
It is reset to `None` at the start of every `show()` call, so you can
safely re-show a dialog instance.

```python
dialog.result  # value of the pressed button's `result=`, or None
```

`None` means one of:

- the user closed the window from the title bar,
- the user pressed **Escape** (which destroys the dialog if no
  `cancel`-role button is wired),
- the pressed button had `result=None` (the default).

`Dialog` does **not** fire a `<<DialogResult>>` event and has no
`on_dialog_result` helper — those are added by subclasses
([`MessageDialog`](messagedialog.md), [`QueryDialog`](querydialog.md),
etc.). On the base class, read `.result` after `show()` returns. See
**Events** below if you need to attach a callback.

A button with `closes=False` runs its `command` but does **not**
close the dialog or assign `.result` — useful for "Apply" buttons,
help links, or any non-terminal action.

---

## Common options

| Option | Purpose |
|---|---|
| `master` | Parent widget. Defaults to the application root. |
| `title` | Window title shown in the title bar. Default `"ttkbootstrap"`. |
| `content_builder` | Callable `(frame) -> None`. Builds the content area. The `frame` is a pre-packed `ttk.Frame` you fill with widgets via `pack`/`grid`/`place`. Optional — omit for a footer-only dialog. |
| `footer_builder` | Callable `(frame) -> None`. Replaces the standard button footer entirely. If passed, `buttons` is ignored. |
| `buttons` | Iterable of `DialogButton` or dicts. Packed right-to-left, so the *first* item is the rightmost (and conventionally primary) button. |
| `minsize` / `maxsize` | `(width, height)` window size limits, in pixels. |
| `resizable` | `(width_resizable, height_resizable)`. Defaults to `(False, False)` — dialogs are non-resizable by default. |
| `alert` | If `True`, rings the system bell when the dialog opens. Default `False`. |
| `mode` | `"modal"` (default), `"popover"`, or `"sheet"`. See **Behavior** below. |
| `frameless` | If `True`, removes window decorations and adds an inner border frame. Use for popover-style menus. |
| `window_style` | Windows-only pywinstyles effect (`"mica"`, `"acrylic"`, `"aero"`, `"transparent"`, `"win7"`). Falls back to `AppSettings.window_style` when `None`. |

Each entry in `buttons` is a `DialogButton` (or dict with the same
fields):

| Field | Purpose |
|---|---|
| `text` | Button label. |
| `role` | One of `"primary"`, `"secondary"` (default), `"danger"`, `"cancel"`, `"help"`. Drives default styling and Escape binding (`"cancel"` is wired to Escape). |
| `result` | Value assigned to `dialog.result` when this button is pressed. Default `None`. |
| `closes` | Whether pressing this button destroys the dialog. Default `True`. |
| `default` | If `True`, this button receives focus and is invoked on **Enter**. Only one button should set this. |
| `command` | Callable `(dialog) -> None` invoked when the button is pressed, *before* `result` is assigned and the dialog is destroyed. Receives the `Dialog` instance. |
| `accent` / `variant` | Style tokens that override the role-derived styling (e.g. `accent="info", variant="link"`). |
| `icon` | Icon name or icon spec dict, passed straight to `ttk.Button(icon=...)`. |

```python
ttk.Dialog(
    title="Restart required",
    content_builder=lambda f: ttk.Label(
        f, text="Restart now to apply updates?"
    ).pack(padx=20, pady=20),
    buttons=[
        ttk.DialogButton(text="Later",   role="cancel"),
        ttk.DialogButton(text="Restart", role="primary",
                         default=True, result=True),
    ],
).show()
```

---

## Behavior

### Modes

| Mode | Modal | Closes on focus loss | Notes |
|---|---|---|---|
| `"modal"` (default) | Yes | No | Grabs the parent window; `show()` blocks until dismissal. |
| `"popover"` | No grab | Yes | `show()` still blocks (uses `wait_window`), but the dialog destroys itself when focus leaves. Useful for transient pickers anchored to a widget. |
| `"sheet"` | Yes | No | On macOS, applies the Cocoa **sheet** window class for a chromeless slide-down dialog tied to its parent. On Windows/Linux, falls back to plain `"modal"`. |

`show(modal=True/False)` overrides the mode's default modality for a
single call.

### Default button (Enter)

A button with `default=True` is focused on open and bound to
**Enter**. Unlike [`MessageDialog`](messagedialog.md), `Dialog` does
**not** auto-promote the last button to default — you must set
`default=True` explicitly, or the dialog will have no Enter binding.

### Cancel button (Escape)

A button with `role="cancel"` is bound to **Escape** and gets the
outline variant. If no such button exists, **Escape** destroys the
dialog directly (with `result=None`).

### Positioning via `show()`

`show()` accepts positioning keywords that are evaluated in this
order:

1. `position=(x, y)` — absolute screen coordinates.
2. `anchor_to=...` plus `anchor_point` / `window_point` / `offset` /
   `auto_flip` — anchor to a widget, the cursor, the parent, or the
   screen. See [Windows](../../platform/windows.md) for the full
   anchor model.
3. Default — centered on the parent window.

`auto_flip` keeps the dialog on-screen by flipping its position when
it would overflow a screen edge.

### Frameless dialogs

`frameless=True` removes the OS title bar and resize border, then adds
an internal `ttk.Frame(show_border=True, padding=2)` around the
content. This is the recommended shape for popover-anchored menus or
custom dropdown surfaces. Frameless windows have no system close
button — make sure the footer or content area provides a way out.

---

## Events

`Dialog` itself does **not** fire any events. The standard
`<<DialogResult>>` virtual event and the `on_dialog_result` /
`off_dialog_result` helpers live on the specialized subclasses
([`MessageDialog`](messagedialog.md),
[`QueryDialog`](querydialog.md), [`DateDialog`](datedialog.md),
[`ColorChooserDialog`](colorchooser.md),
[`ColorDropperDialog`](colordropper.md)) — they generate the event
themselves after `show()` finishes.

If you need an event-style hook on a base `Dialog`, use a button
`command` callback. It receives the `Dialog` instance and runs before
the dialog is destroyed:

```python
def on_save(dlg):
    persist(dlg)

ttk.Dialog(
    content_builder=...,
    buttons=[
        {"text": "Cancel", "role": "cancel"},
        {"text": "Save",   "role": "primary", "default": True,
         "command": on_save, "result": "saved"},
    ],
).show()
```

For long-lived listeners, bind `<<DialogResult>>` (or any custom
virtual event) on the dialog's `Toplevel` directly via the
`dialog.toplevel` property — but you'll need to call
`event_generate` yourself from a button `command`.

---

## When should I use Dialog?

Use `Dialog` when:

- you need a layout the canned subclasses don't offer (multi-column,
  tabbed, embedded charts, custom footer).
- you need a popover or Cocoa sheet — none of the subclasses expose
  the `mode` argument.
- you need a frameless dropdown anchored to a widget.
- you need button roles outside the message/yes-no patterns
  (`"help"`, multiple `"primary"` actions, an "Apply" with
  `closes=False`).

Prefer a different control when:

- the dialog is "show a message and pick a button" → use
  [`MessageDialog`](messagedialog.md) or
  [`MessageBox`](messagebox.md).
- the dialog is "ask for one value" → use
  [`QueryDialog`](querydialog.md) or [`QueryBox`](querybox.md).
- the dialog is "edit a structured form" → use
  [`FormDialog`](formdialog.md).
- the dialog picks a date, color, or font → use
  [`DateDialog`](datedialog.md),
  [`ColorChooserDialog`](colorchooser.md), or
  [`FontDialog`](fontdialog.md).
- the message is non-blocking → build a non-modal `Toplevel` with
  auto-dismiss; there is no built-in toast.

---

## Additional resources

**Related widgets**

- [`MessageDialog`](messagedialog.md) — confirm/notify with a fixed
  layout (icon + message + buttons).
- [`QueryDialog`](querydialog.md) — single-value input dialog.
- [`FormDialog`](formdialog.md) — multi-field form in a dialog shell.
- [`DateDialog`](datedialog.md) /
  [`ColorChooserDialog`](colorchooser.md) /
  [`FontDialog`](fontdialog.md) — domain-specific pickers.
- [`FilterDialog`](filterdialog.md) — column-filter editor for
  ListView / TreeView.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)

**API reference**

- **API reference:** [`ttkbootstrap.Dialog`](../../reference/dialogs/Dialog.md),
  [`ttkbootstrap.DialogButton`](../../reference/dialogs/DialogButton.md)
- **Related guides:** Dialogs, UX Patterns
