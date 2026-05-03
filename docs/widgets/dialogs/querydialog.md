---
title: QueryDialog
---

# QueryDialog

`QueryDialog` is a modal dialog that prompts the user for **a single
value** — a string, integer, float, date, or pick from a list. It
swaps in the right input widget for the requested `datatype` (a
`TextEntry`, `NumericEntry`, `DateEntry`, or `Combobox`), runs that
widget's validation when the user clicks Submit, and exposes the
typed value on `.result`.

It is the building block underneath
[`QueryBox`](querybox.md) — the canned `get_string` / `get_integer`
/ `get_float` / `get_date` / `get_item` helpers all construct a
`QueryDialog` for you. Drop down to `QueryDialog` directly when you
need to combine options the helpers don't expose together (e.g. an
ICU value format on an integer prompt with min/max bounds).

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

def ask_name():
    dialog = ttk.QueryDialog(prompt="What is your name?", title="Name")
    dialog.show()
    if dialog.result is not None:
        print("Hello,", dialog.result)

ttk.Button(app, text="Ask…", command=ask_name).pack(padx=20, pady=20)
app.mainloop()
```

`show()` blocks the caller. Read `.result` after it returns, or
register a callback with `on_dialog_result` for an event-style flow.

Test for `result is not None` rather than the bare `result` —
`""` and `0` are valid answers.

---

## Result value

`.result` is the **typed value** the user submitted, converted to
the dialog's `datatype`:

| `datatype` | `.result` type |
|---|---|
| `str` (default) | `str` |
| `int` | `int` |
| `float` | `float` |
| `date` | `datetime.date` |
| any, with `items=[...]` | `str` (the chosen item) |

`None` means the user **cancelled** — clicked Cancel, pressed
Escape, or closed the window from the title bar.

The `<<DialogResult>>` event payload also carries a `confirmed`
flag (`True` whenever `result is not None`) — useful when you only
care about "did the user submit?" rather than the value.

---

## Common options

| Option | Purpose |
|---|---|
| `prompt` | Prompt text shown above the input. Newlines are preserved; each line is wrapped to `width` characters. |
| `value` | Initial value pre-filled into the input. Coerced to the widget's expected type. |
| `datatype` | `str` (default), `int`, `float`, or `date`. Selects the input widget and validation. |
| `items` | If non-empty, replaces the entry with a filterable `Combobox`. Overrides `datatype`. |
| `minvalue` / `maxvalue` | Range bounds for `int` / `float`. Ignored for `str`. |
| `increment` | Step size for the `NumericEntry` spinner buttons. |
| `value_format` | ICU pattern (numbers: `"$#,##0.00"`, `"#,##0.##"`) or date preset (`"shortDate"`, `"yyyy-MM-dd"`) used to format and parse the value. |
| `width` | Maximum line length for prompt wrapping, in characters. Default `65`. |
| `padding` | Inner padding around the body, as `(x, y)` or a single int. Default `(20, 20)`. |
| `title` | Window title shown in the title bar. |
| `master` | Parent window. Defaults to the application root. |

```python
from datetime import date

# Numeric input with bounds and currency formatting
ttk.QueryDialog(
    prompt="What's your bid?",
    title="Place bid",
    datatype=float,
    minvalue=0,
    maxvalue=10_000,
    value_format="$#,##0.00",
    increment=10,
).show()

# Date input
ttk.QueryDialog(prompt="Pick a day:", datatype=date).show()

# Filterable list pick
ttk.QueryDialog(
    prompt="Choose a colour:",
    items=["Red", "Green", "Blue"],
    value="Green",
).show()
```

When `items=` is set the `datatype` is ignored — the dialog renders
a `Combobox` whose dropdown filters as the user types.

---

## Behavior

### Modality and lifecycle

The dialog opens a `Toplevel` transient to its parent and runs in
modal mode: the parent window is grabbed, and `show()` does not
return until the user dismisses the dialog. The dialog is centered
on the parent unless an explicit `position` is passed:

```python
dialog.show(position=(200, 150))
```

The `Toplevel` is destroyed on dismissal — to re-prompt, build a
new `QueryDialog`.

### Buttons

The button row is fixed: a **Cancel** button (cancel role; bound to
**Escape**, returns `None`) and a **Submit** button (primary,
default; bound to **Enter**, runs validation). They cannot be
relabelled or reordered through `QueryDialog` itself — use
[`Dialog`](dialog.md) directly if you need different button text or
roles.

### Submit and validation

Clicking Submit (or pressing Enter inside the input) runs the
underlying input widget's validation:

- For **`str` input** (`TextEntry`), any value is accepted.
- For **`int` / `float` input** (`NumericEntry`), the value must
  parse as the requested type and fall within `minvalue` /
  `maxvalue`.
- For **`date` input** (`DateEntry`), the value must parse as a
  date in the current locale or `value_format`.
- For **`items` mode** (`Combobox`), the typed value must match an
  entry in `items` (case-sensitive, exact match).

Validation outcomes differ by widget. The `Combobox` and old-style
numeric paths show a translated error in a child `MessageBox.ok` and
keep the dialog open. The `Field`-based widgets (`TextEntry`,
`NumericEntry`, `DateEntry`) raise their own inline validation
feedback under the input — if the value is invalid the dialog stays
open silently, with the field's error message visible.

### Focus

The input field receives focus when the dialog opens (re-applied via
`after_idle` so the buttons' own focus calls don't steal it).

---

## Events

`<<DialogResult>>` fires once on the dialog's `Toplevel` after
dismissal. The payload exposed via `event.data` carries:

| Key | Type | Meaning |
|---|---|---|
| `result` | the typed value, or `None` | The submitted value (or `None` if cancelled). |
| `confirmed` | `bool` | `result is not None`. |

Use `on_dialog_result(callback)` to register a handler that receives
the payload directly (no `event.data` unwrap needed). The helper
returns a binding identifier you can pass back to
`off_dialog_result` to detach.

```python
def handle(payload):
    if payload["confirmed"]:
        print("submitted:", payload["result"])
    else:
        print("cancelled")

dialog = ttk.QueryDialog(prompt="Enter your age:", datatype=int, master=app)
dialog.on_dialog_result(handle)
dialog.show()
```

Pass `master=` so the binding has somewhere to live before the
`Toplevel` is created (`on_dialog_result` binds to
`self._dialog.toplevel or self._master`, and the toplevel does not
exist until `show()` runs).

---

## When should I use QueryDialog?

Use `QueryDialog` when:

- you need a single value with bounds, formatting, or list-pick
  behavior, and the [`QueryBox`](querybox.md) helpers don't quite
  fit (e.g. you want both `minvalue` *and* a custom ICU format).
- you want the typed result and the `<<DialogResult>>` lifecycle
  hook on the same object (`QueryBox` returns the value directly
  but doesn't expose the dialog).

Prefer a different control when:

- the call shape is one of the canned patterns
  (`get_string` / `get_integer` / `get_float` / `get_date` /
  `get_item`) — use [`QueryBox`](querybox.md) for a one-line call.
- you need more than one input field — use
  [`FormDialog`](formdialog.md).
- you only need to show a message or get a button choice — use
  [`MessageDialog`](messagedialog.md) or
  [`MessageBox`](messagebox.md).
- you need full control over button labels, roles, or footer
  layout — drop down to [`Dialog`](dialog.md).

---

## Additional resources

**Related widgets**

- [`QueryBox`](querybox.md) — static `get_string` / `get_integer`
  / `get_float` / `get_date` / `get_item` helpers that build a
  `QueryDialog` for you.
- [`MessageDialog`](messagedialog.md) — message + button choice,
  no input field.
- [`FormDialog`](formdialog.md) — multi-field modal form.
- [`Dialog`](dialog.md) — the generic builder underneath
  `QueryDialog`; use it when you need custom buttons or layout.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)

**API reference**

- **API reference:** [`ttkbootstrap.QueryDialog`](../../reference/dialogs/QueryDialog.md)
- **Related guides:** Dialogs, Localization
