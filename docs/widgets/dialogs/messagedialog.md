---
title: MessageDialog
---

# MessageDialog

`MessageDialog` is a modal popup that shows a message and a row of
named buttons. Calling `show()` blocks until the user picks a button;
the chosen button's text is then available on `.result` and is
broadcast as a `<<DialogResult>>` event.

It is the building block underneath
[`MessageBox`](messagebox.md) — when the canned info/warning/error/
yes-no patterns aren't quite right, drop down to `MessageDialog` to
control the icon, the button labels, the default button, and the
accent.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

def confirm():
    dialog = ttk.MessageDialog(
        message="Delete the selected item? This cannot be undone.",
        title="Confirm delete",
        buttons=["Cancel", "Delete:danger"],
        icon="exclamation-triangle-fill",
    )
    dialog.show()
    if dialog.result == "Delete":
        print("deleting…")

ttk.Button(app, text="Delete…", command=confirm).pack(padx=20, pady=20)
app.mainloop()
```

`show()` blocks the caller. Read `.result` after it returns, or
register a callback with `on_dialog_result` if you'd rather react
event-style.

---

## Result value

`.result` is the **text of the button pressed**, with the leading
`text:` portion of the spec stripped:

```python
dialog = ttk.MessageDialog(buttons=["Cancel", "Save:primary"])
dialog.show()

dialog.result  # "Cancel" or "Save", or None
```

`None` means the user dismissed the dialog without choosing a button
— typically by closing the window from the title bar, or by pressing
**Escape** when no `cancel`-role button is present.

The `<<DialogResult>>` event payload also carries a `confirmed`
flag (`True` whenever `result is not None`) — useful when you only
care about "did the user act?" rather than which button was pressed.

For internationalized apps where the button label changes per
locale, prefer reading `confirmed` or distinguish buttons by position
rather than label string.

---

## Common options

| Option | Purpose |
|---|---|
| `message` | The body text. Wrapped to `width` characters per line; newlines are preserved. |
| `title` | Window title shown in the title bar. |
| `buttons` | List of button labels. `"text:accent"` syntax sets a per-button accent (`"Save:primary"`, `"Delete:danger"`). Default is `["button.cancel", "button.ok"]`. |
| `default` | Label of the button to mark as default (Enter target, primary accent, focused). Falls back to the last button in the list. |
| `icon` | A Bootstrap icon name (`"info-circle-fill"`) or a dict `{"name": ..., "size": 32, "color": "danger"}` for a colored or sized icon. |
| `width` | Maximum line length for message wrapping, in characters. Default `50`. |
| `padding` | Inner padding around the message body, as `(x, y)` or a single int. Default `(20, 20)`. |
| `alert` | If `True`, rings the system bell when the dialog opens. Default `False`. |
| `master` | Parent window. Defaults to the application root. |
| `command` | Callable invoked once for *any* button press, before the dialog closes. Receives no arguments. |
| `localize` | Pass via `**kwargs`. When `True`, button labels are resolved through `MessageCatalog.translate` so the default `"button.cancel"` / `"button.ok"` keys render in the active locale. |

```python
ttk.MessageDialog(
    message="Sign in failed.",
    title="Authentication error",
    icon={"name": "x-circle-fill", "size": 40, "color": "danger"},
    buttons=["Close", "Retry:primary"],
    default="Retry",
    alert=True,
).show()
```

!!! note "Localization caveat"
    The default `["button.cancel", "button.ok"]` are translation
    *keys*, not display strings. Without `localize=True`, the user
    sees the literal text `button.cancel` / `button.ok`. Either pass
    `localize=True`, or supply your own button labels.

---

## Behavior

### Modality and lifecycle

Each `MessageDialog` opens a `Toplevel` transient to its parent and
runs in modal mode: the parent window is grabbed, and `show()` does
not return until the user dismisses the dialog. The dialog is
centered on the parent unless an explicit `position` is passed to
`show()`.

`show(position=(x, y))` overrides centering with absolute screen
coordinates. The dialog is destroyed on dismissal — to re-show, build
a new instance.

### Default button (Enter)

The **default button** is wired to **Enter** and gets focus and the
primary accent. Specify it explicitly with `default="OK"`; if
omitted, the *last* button in the list is the default.

The default-button rule has a UX consequence: **list destructive
options first** so the safer choice is the default. With
`buttons=["Delete:danger", "Cancel"]`, **Enter** cancels — exactly
what you want.

### Cancel binding (Escape)

If the *first* button's label contains the word "cancel"
(case-insensitive), it is wired to **Escape** and gets the outline
variant. Any other layout — for example, a custom "Discard" button
that should cancel — needs the underlying [`Dialog`](dialog.md)
class with an explicit `DialogButton(role="cancel")` spec.

### `command` vs button branching

The `command` constructor argument fires *once for every button
press*, before the dialog closes. It receives no arguments and
cannot tell which button was pressed. Use it for side effects
(logging, focus restoration); use `.result` or `<<DialogResult>>`
for branching on the user's choice.

---

## Events

`<<DialogResult>>` is fired once on the dialog's `Toplevel` after the
user picks a button. The payload exposed via `event.data` carries:

| Key | Type | Meaning |
|---|---|---|
| `result` | `str` or `None` | The pressed button's text (or `None`). |
| `confirmed` | `bool` | `result is not None`. |

Use `on_dialog_result(callback)` to register a handler that receives
the payload directly (no `event.data` unwrap needed). The helper
returns a binding identifier you can pass back to `off_dialog_result`
to detach.

```python
def handle(payload):
    if payload["confirmed"]:
        print("user picked:", payload["result"])
    else:
        print("user dismissed the dialog")

dialog = ttk.MessageDialog(message="Continue?", buttons=["No", "Yes"])
dialog.on_dialog_result(handle)
dialog.show()
```

---

## UX guidance

- **Keep the message short.** `MessageDialog` is for a single
  question or notice. If you need a paragraph of explanation, a form,
  or a list of options, use [`FormDialog`](formdialog.md) or build
  your own with [`Dialog`](dialog.md).
- **Label buttons with verbs**, not "OK" / "Cancel", whenever the
  action has a name. "Delete", "Discard changes", "Replace file" tell
  the user what will happen; "OK" doesn't.
- **Put the destructive option first** with the `:danger` accent and
  the safe option second. The default-button rule (last button is the
  default) then makes the safe choice the **Enter** target.
- **Reserve `alert=True` for genuinely urgent dialogs.** The bell is
  a hard interrupt; use it for errors that require attention, not for
  routine confirmations.
- **Don't chain dialogs.** If a dialog's button opens another dialog,
  the user has to dismiss two levels of modal before they can keep
  working. Restructure into a single dialog or a non-modal flow.

---

## When should I use MessageDialog?

Use MessageDialog when:

- you need a confirmation, notice, or two-/three-way decision with
  custom button labels.
- you want an icon or a per-button accent (`:danger`, `:primary`).
- the canned [`MessageBox`](messagebox.md) shortcuts don't fit.

Prefer a different control when:

- the message fits a stock pattern (info / warning / error / yes-no /
  ok-cancel) → use [`MessageBox`](messagebox.md) for less code.
- you need to collect a value, not just a button choice → use
  [`QueryDialog`](querydialog.md) or [`QueryBox`](querybox.md).
- you need multiple inputs → use [`FormDialog`](formdialog.md).
- you want a non-blocking notification → there is no built-in toast;
  build a non-modal `Toplevel` with auto-dismiss.

---

## Additional resources

**Related widgets**

- [`MessageBox`](messagebox.md) — static `show_info` / `yesno` /
  etc. shortcuts that build a `MessageDialog` for you.
- [`QueryDialog`](querydialog.md) — modal dialog with a single text
  input.
- [`FormDialog`](formdialog.md) — multi-field modal form.
- [`Dialog`](dialog.md) — the generic builder underneath
  `MessageDialog`; use it directly when you need full control of
  layout, footer, or button roles.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)

**API reference**

- **API reference:** [`ttkbootstrap.MessageDialog`](../../reference/dialogs/MessageDialog.md)
- **Related guides:** Dialogs, Localization
