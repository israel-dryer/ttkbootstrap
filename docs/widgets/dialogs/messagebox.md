---
title: MessageBox
---

# MessageBox

`MessageBox` is a thin **facade** over [`MessageDialog`](messagedialog.md):
a handful of static methods (`ok`, `yesno`, `okcancel`, `show_info`,
`show_error`, …) that build a modal `MessageDialog` with a canned
button set and icon, call `show()`, and return the pressed button's
text.

Reach for `MessageBox` when the message fits one of the stock
patterns — info, warning, error, question, yes/no, ok/cancel — and
the few extra lines of `MessageDialog` setup aren't earning their
keep. Drop down to [`MessageDialog`](messagedialog.md) the moment you
need a custom button label, a `:danger` accent, or non-default
modality.

---

## Basic usage

Every method takes `message` first, then `title`, then optional
`master` and `alert` flags, then keyword extras forwarded to the
underlying `MessageDialog`.

```python
import ttkbootstrap as ttk

app = ttk.App()

def confirm_quit():
    answer = ttk.MessageBox.yesno(
        "Quit without saving your changes?",
        title="Unsaved changes",
    )
    if answer == "Yes":
        app.destroy()

ttk.Button(app, text="Quit", command=confirm_quit).pack(padx=20, pady=20)
app.mainloop()
```

Each call **blocks** the caller until the user picks a button (or
dismisses the dialog) and then returns the button's text. There is no
need to instantiate or hold on to anything — the helper builds the
dialog, shows it, and tears it down.

---

## Result value

Every helper returns a `str` (the pressed button's text) or `None`
when the dialog is dismissed without a button press (close box,
Escape on cancel-bearing dialogs).

| Helper | Buttons (left → right) | Possible return values |
|---|---|---|
| `ok(...)` | `OK` | `"OK"` or `None` |
| `okcancel(...)` | `Cancel`, `OK` | `"OK"`, `"Cancel"`, or `None` |
| `yesno(...)` | `No`, `Yes` | `"Yes"`, `"No"`, or `None` |
| `yesnocancel(...)` | `Cancel`, `No`, `Yes` | `"Yes"`, `"No"`, `"Cancel"`, or `None` |
| `retrycancel(...)` | `Cancel`, `Retry` | `"Retry"`, `"Cancel"`, or `None` |
| `show_info(...)` | `OK` (info icon) | `"OK"` or `None` |
| `show_warning(...)` | `OK` (warning icon, `alert=True`) | `"OK"` or `None` |
| `show_error(...)` | `OK` (error icon, `alert=True`) | `"OK"` or `None` |
| `show_question(...)` | `OK` (question icon) | `"OK"` or `None` |

```python
result = ttk.MessageBox.okcancel("Replace existing file?")
if result == "OK":
    write_file()
elif result == "Cancel":
    log("user cancelled")
else:
    log("user dismissed dialog")  # closed via title bar
```

Button labels are passed through `MessageCatalog.translate`
(`localize=True` is always on inside the facade), so the returned
string reflects the **active locale** when a translation exists. Code
that branches on `result == "Yes"` will break under translation —
prefer comparing against a known constant captured at call time, or
drop down to `MessageDialog` and read the `<<DialogResult>>`
`confirmed` flag.

---

## Common options

| Argument | Purpose |
|---|---|
| `message` | Body text. Positional or keyword. Wrapped to `width` characters per line. |
| `title` | Window title. Defaults to a single space (no title). |
| `master` | Parent window. Defaults to the application root. |
| `alert` | If `True`, rings the system bell when the dialog opens. `show_warning` and `show_error` default to `True`; everything else defaults to `False`. |
| `icon` *(kwarg)* | Override the icon. Bootstrap icon name (`"info-circle-fill"`) or a dict (`{"name": ..., "size": 32, "color": "danger"}`). The semantic helpers (`show_info`, `show_warning`, …) set this for you. |
| `width` *(kwarg)* | Maximum line length for message wrapping. Default `50`. |
| `padding` *(kwarg)* | Inner padding around the message body. Default `(20, 20)`. |
| `position` *(kwarg)* | Override the centered position with absolute screen coordinates `(x, y)`. |
| `on_result` *(kwarg)* | Callback receiving the `<<DialogResult>>` payload (`{"result": ..., "confirmed": ...}`). Fires before the helper returns. |

```python
ttk.MessageBox.show_error(
    "Could not connect to the server.",
    title="Connection failed",
    master=app,
    width=60,
    padding=(24, 16),
)
```

The button labels themselves are **fixed per method** — `MessageBox`
won't let you swap `Yes`/`No` for `Keep`/`Discard`. If you need verb
labels (or a `:danger` accent on a destructive button), instantiate
[`MessageDialog`](messagedialog.md) directly.

---

## Behavior

### Modality and lifecycle

Each call builds a fresh modal `MessageDialog` transient to `master`,
shows it, and destroys it on dismissal. The helper does not return
until the user dismisses the dialog. Calling code therefore behaves
like a synchronous prompt — a `print(...)` immediately after the
helper runs after the user has clicked.

### Default button (Enter)

The **last button** in each canned set is the default — the one
focused, accented as primary, and bound to **Enter**. So:

- `okcancel` → **OK** is default
- `yesno` → **Yes** is default
- `yesnocancel` → **Yes** is default
- `retrycancel` → **Retry** is default

This matches conventional modal UX: Enter performs the affirmative
action.

### Cancel binding (Escape)

The **first** button is wired to **Escape** *only when its label
contains "cancel"* (case-insensitive). That covers `okcancel`,
`yesnocancel`, and `retrycancel`. **`yesno` has no Escape binding** —
neither button is "cancel", so closing the dialog from the keyboard
requires the title-bar close box. Use `yesnocancel` if you want
keyboard dismissal.

### Localization

`MessageBox` always passes `localize=True` to the underlying dialog,
so canonical labels (`"OK"`, `"Cancel"`, `"Yes"`, `"No"`, `"Retry"`)
are looked up in the active `MessageCatalog` before being shown and
returned. When a translation exists, the returned string is the
translated label.

---

## Events

`MessageBox` is a thin facade — there is no instance to bind to. Use
the **`on_result` keyword** to react to the dismissal payload:

```python
def log_choice(payload):
    print("confirmed:", payload["confirmed"], "result:", payload["result"])

ttk.MessageBox.yesnocancel(
    "Save changes before quitting?",
    title="Unsaved changes",
    on_result=log_choice,
)
```

If you need a longer-lived hook (multiple subscribers, off-binding,
inspection of the dialog instance), build a `MessageDialog` yourself
and call `on_dialog_result` on it.

---

## When should I use MessageBox?

Use `MessageBox` when:

- the message fits one of the stock patterns: info / warning / error
  / yes-no / ok-cancel / retry-cancel.
- you want one line of code instead of three.
- the canned button labels are acceptable for your locale and tone.

Prefer a different control when:

- you need custom button labels or a `:danger` accent → use
  [`MessageDialog`](messagedialog.md).
- you need to collect a value, not just a button choice → use
  [`QueryBox`](querybox.md) or [`QueryDialog`](querydialog.md).
- you need multiple inputs → use [`FormDialog`](formdialog.md).
- you want non-blocking feedback ("Saved", "Copied") → use
  [`Toast`](../overlays/toast.md).

---

## Additional resources

**Related widgets**

- [`MessageDialog`](messagedialog.md) — the underlying modal; use it
  directly for custom buttons, accents, or default-button overrides.
- [`QueryBox`](querybox.md) — the same facade pattern, but for
  collecting a single text/numeric value.
- [`Toast`](../overlays/toast.md) — non-blocking inline notification
  for transient feedback.
- [`Dialog`](dialog.md) — the generic builder underneath everything.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)

**API reference**

- **API reference:** [`ttkbootstrap.MessageBox`](../../reference/dialogs/MessageBox.md)
- **Related guides:** Dialogs, Localization
