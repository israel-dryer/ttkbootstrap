---
title: QueryBox
---

# QueryBox

`QueryBox` is a thin **facade** over the framework's input dialogs:
seven static methods — `get_string`, `get_integer`, `get_float`,
`get_item`, `get_date`, `get_color`, `get_font` — that build a modal
prompt, call `show()`, and return the value the user picked (or
`None` if they cancelled).

Most of the helpers are sugar over [`QueryDialog`](querydialog.md);
`get_date`, `get_color`, and `get_font` delegate to
[`DateDialog`](datedialog.md),
[`ColorChooserDialog`](colorchooser.md), and
[`FontDialog`](fontdialog.md) respectively. Reach for `QueryBox`
when the call shape fits one of the canned helpers and you don't
need a handle on the underlying dialog instance.

---

## Basic usage

Each helper takes the prompt-shaped arguments first, then optional
`master` and helper-specific extras, builds and shows a modal
dialog, and returns the typed value or `None`.

```python
import ttkbootstrap as ttk

app = ttk.App()

def rename():
    new_name = ttk.QueryBox.get_string(
        prompt="Enter a new name",
        title="Rename",
        value="Untitled",
    )
    if new_name is not None:
        print("renamed to:", new_name)

ttk.Button(app, text="Rename…", command=rename).pack(padx=20, pady=20)
app.mainloop()
```

The call **blocks** the caller until the user dismisses the dialog,
so a `print(...)` immediately afterward runs after they've picked.

Test for `result is not None` rather than truthiness — `""` and `0`
are valid answers from the QueryDialog-backed helpers.

---

## Result value

Each helper returns the value the user committed, or `None` if they
cancelled (Cancel button, Escape, or title-bar close).

| Helper | Underlying dialog | Returns |
|---|---|---|
| `get_string(...)` | [`QueryDialog`](querydialog.md) (`TextEntry`) | `str` or `None` |
| `get_integer(...)` | [`QueryDialog`](querydialog.md) (`NumericEntry`, `datatype=int`) | `int` or `None` |
| `get_float(...)` | [`QueryDialog`](querydialog.md) (`NumericEntry`, `datatype=float`) | `float` or `None` |
| `get_item(...)` | [`QueryDialog`](querydialog.md) (filterable `Combobox`) | `str` (the chosen item) or `None` |
| `get_date(...)` | [`DateDialog`](datedialog.md) | `datetime.date` or `None` |
| `get_color(...)` | [`ColorChooserDialog`](colorchooser.md) | color string (`"#rrggbb"` or named) or `None` |
| `get_font(...)` | [`FontDialog`](fontdialog.md) | a font spec object or `None` |

There is no `get_password` helper — for masked input, build a
[`PasswordEntry`](../inputs/passwordentry.md) inside a
[`FormDialog`](formdialog.md) (or a custom [`Dialog`](dialog.md)).

---

## Common options

The QueryDialog-backed helpers (`get_string`, `get_integer`,
`get_float`, `get_item`) share a common shape; `get_date`,
`get_color`, and `get_font` use their underlying dialog's
constructor signature.

| Argument | Used by | Purpose |
|---|---|---|
| `prompt` | string / numeric / item | Prompt text shown above the input. Newlines are preserved. |
| `title` | all | Window title. Default `" "` (no title). |
| `value` | all | Initial value pre-filled into the input (or initial date / color). |
| `master` | all | Parent window. Defaults to the application root. |
| `position` *(kwarg)* | all | Override the centered position with absolute screen coordinates `(x, y)`. |
| `on_result` *(kwarg)* | string / numeric / item / date | Callback receiving the dismissal payload before the helper returns. **Not supported by `get_color` or `get_font`.** |
| `items` | item | List of items shown in the filterable `Combobox`. |
| `minvalue`, `maxvalue` | integer / float | Numeric bounds, enforced before commit. |
| `increment` | integer / float | Step size for the spinner buttons. |
| `value_format` | string / integer / float | ICU format pattern (`"$#,##0.00"`, `"#,##0.##"`, …). |
| `width`, `padding` *(forwarded)* | string / numeric / item | Forwarded to `QueryDialog` via `**kwargs`. |
| `first_weekday` | date | Index of the leftmost calendar column (`0`=Monday, `6`=Sunday). |
| `accent` | date | Accent token for the calendar (`"primary"`, `"success"`, …). |
| `hide_window_chrome` | date | If `True`, removes window decorations (override-redirect). |

```python
from datetime import date

# Numeric input with bounds and currency formatting
amount = ttk.QueryBox.get_float(
    prompt="What's your bid?",
    title="Place bid",
    minvalue=0,
    maxvalue=10_000,
    value_format="$#,##0.00",
    increment=10,
)

# Filterable list pick
colour = ttk.QueryBox.get_item(
    prompt="Choose a colour:",
    items=["Red", "Green", "Blue"],
    value="Green",
)

# Date input
when = ttk.QueryBox.get_date(value=date.today(), accent="primary")
```

The argument list is **fixed per method** — `QueryBox` does not let
you swap the button labels, change the dialog modality, or attach
multiple result handlers. If you need that, instantiate the
underlying dialog directly.

---

## Behavior

Each helper builds a fresh modal dialog transient to `master`,
calls `show()`, reads `.result` off the dialog, and tears it down.
The helper does not return until the user dismisses the dialog.

For the QueryDialog-backed helpers:

- **Submit / Enter** runs the input widget's validation. For
  `get_string` any value is accepted; for `get_integer` /
  `get_float` the value must parse and fall within `minvalue` /
  `maxvalue`; for `get_item` the typed value must match an entry
  in `items` (case-sensitive, exact). See
  [`QueryDialog`](querydialog.md) for the full validation rules.
- **Cancel / Escape** returns `None`.
- Invalid input keeps the dialog open: the Field-based helpers
  (`get_string`, `get_integer`, `get_float`) show inline error
  feedback under the input; `get_item` shows a child `MessageBox`.

For `get_date`, `get_color`, and `get_font`, modality and
button-binding rules come from the underlying dialog — see
[`DateDialog`](datedialog.md), [`ColorChooserDialog`](colorchooser.md),
and [`FontDialog`](fontdialog.md).

---

## Events

`QueryBox` is a thin facade — there's no instance to bind to. The
QueryDialog-backed helpers and `get_date` accept an **`on_result`
keyword** that registers a callback fired before the helper
returns.

```python
def log_choice(payload):
    if payload["confirmed"]:
        print("submitted:", payload["result"])
    else:
        print("cancelled")

ttk.QueryBox.get_integer(
    prompt="Enter your age:",
    title="Age",
    minvalue=0,
    on_result=log_choice,
)
```

The payload shape comes from the underlying dialog:

- `get_string` / `get_integer` / `get_float` / `get_item` →
  `QueryDialog`'s `<<DialogResult>>` payload
  (`{"result": ..., "confirmed": bool}`).
- `get_date` → `DateDialog`'s on-result payload (see
  [`DateDialog`](datedialog.md)).
- `get_color` and `get_font` accept no `on_result` callback —
  their helper signatures don't expose it.

If you need a longer-lived hook, multiple subscribers, or
inspection of the dialog instance, build the underlying dialog
yourself and call its result-binding method
(`QueryDialog.on_dialog_result`, `DateDialog.on_result`, …).

---

## When should I use QueryBox?

Use `QueryBox` when:

- the call shape fits one of the canned helpers (`get_string`,
  `get_integer`, `get_float`, `get_item`, `get_date`, `get_color`,
  `get_font`).
- you want one line of code instead of three.
- you don't need to hold on to the dialog instance.

Prefer a different control when:

- you need to combine options the helper doesn't expose (e.g.
  `minvalue` *and* a custom ICU format on a string prompt) — use
  [`QueryDialog`](querydialog.md) directly.
- you need multiple input fields — use
  [`FormDialog`](formdialog.md).
- you only need to show a message or get a button choice — use
  [`MessageBox`](messagebox.md).
- you need full control over button labels, roles, or footer
  layout — drop down to [`Dialog`](dialog.md).

---

## Additional resources

**Related widgets**

- [`QueryDialog`](querydialog.md) — the underlying modal for
  `get_string`, `get_integer`, `get_float`, and `get_item`.
- [`DateDialog`](datedialog.md) — backs `get_date`.
- [`ColorChooserDialog`](colorchooser.md) — backs `get_color`.
- [`FontDialog`](fontdialog.md) — backs `get_font`.
- [`MessageBox`](messagebox.md) — the same facade pattern, for
  showing messages and collecting button choices.
- [`FormDialog`](formdialog.md) — multi-field modal form.
- [`Dialog`](dialog.md) — generic dialog builder underneath
  everything.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)

**API reference**

- **API reference:** [`ttkbootstrap.QueryBox`](../../reference/dialogs/QueryBox.md)
- **Related guides:** Dialogs, Localization
