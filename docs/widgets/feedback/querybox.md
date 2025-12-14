---
title: QueryBox
icon: fontawesome/solid/circle-question
---

# QueryBox

`QueryBox` is a set of convenience helpers for collecting a single value from the user—string, number, date, item selection, font, or color—using consistent ttkbootstrap dialogs. It is built on top of `QueryDialog` (for text/number/date/item inputs) and the specialized picker dialogs (`DateDialog`, `FontDialog`, `ColorChooserDialog`).

Use `QueryBox` when you want a **one-line API** for common “ask the user” workflows without building a custom `Dialog` or `FormDialog`.

<!--
IMAGE: QueryBox gallery
Suggested: A small grid showing 4 dialog types: get_string, get_integer, get_item, get_date
Theme variants: light / dark
-->

---

## Basic usage

Ask for a string:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryBox

app = ttk.App()

name = QueryBox.get_string("What is your name?", title="Name", master=app)
print(name)

app.mainloop()
```

Ask for a number with bounds:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryBox

app = ttk.App()

qty = QueryBox.get_integer(
    "Quantity?",
    title="Order",
    value=1,
    minvalue=1,
    maxvalue=99,
    master=app,
)
print(qty)

app.mainloop()
```

Pick from a list:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryBox

app = ttk.App()

color = QueryBox.get_item(
    "Choose a color",
    title="Color",
    items=["Red", "Green", "Blue"],
    master=app,
)
print(color)

app.mainloop()
```

---

## What problem it solves

Applications frequently need “single value” user input:

- quick prompts (“Name?”, “Search?”, “Reason?”)
- small numeric inputs (quantity, threshold, percentage)
- small selections (one item from a list)
- date picks (calendar popover)
- utility pickers (font, color)

`QueryBox` solves this by standardizing:

- button sets (Cancel + Submit)
- return semantics (`result` or `None`)
- basic validation for numbers and item selection
- localization-ready button text keys
- optional formatting via `value_format`

---

## Core concepts

### QueryBox vs QueryDialog vs Dialog

- **QueryBox**: static helper methods, fastest to use
- **QueryDialog**: the underlying single-input dialog (string / number / date / item)
- **Dialog**: generic builder for custom dialog layouts and workflows

If you just need a single value, **QueryBox** is usually the right tool.

---

### Return value

All QueryBox methods return:

- the selected/entered value (typed to the requested datatype), or
- `None` if the user cancels/closes without confirming.

Examples:

```python
QueryBox.get_string(...)   # -> str | None
QueryBox.get_integer(...)  # -> int | None
QueryBox.get_float(...)    # -> float | None
QueryBox.get_item(...)     # -> str | None
QueryBox.get_date(...)     # -> datetime.date | None
QueryBox.get_font(...)     # -> tkinter.font.Font | None
QueryBox.get_color(...)    # -> color string | None (implementation-defined)
```

---

### Prompt wrapping and multiline prompts

`prompt` supports multiline strings. Each line is wrapped to a character width for readability.

```python
QueryBox.get_string(
    "Line 1\nThis is a longer line that will wrap automatically.",
    width=65,
    master=app,
)
```

---

### `value_format` selects specialized field controls

When you provide `value_format`, `QueryDialog` uses the form-ready `*Entry` controls so parsing/formatting is consistent with your locale and formatting rules:

- `TextEntry` for strings
- `NumericEntry` for int/float
- `DateEntry` for dates

Examples:

```python
# Currency formatting (NumericEntry)
price = QueryBox.get_float(
    "Price",
    value=19.99,
    value_format="$#,##0.00",
    master=app,
)
```

```python
# Date formatting (DateEntry)
from datetime import date

d = QueryBox.get_string(
    "Enter a date",
    value=date.today().isoformat(),
    value_format="yyyy-MM-dd",
    master=app,
)
```

!!! tip "Prefer value_format for user-facing numbers/dates"
    If the user will type values in their locale (thousands separators, decimal symbol, date formats), use `value_format` so input behaves like the rest of your app.

---

## Common QueryBox helpers

### `get_string(...)`

Shows a single-line text input dialog.

Key parameters:
- `prompt`, `title`, `value`
- `value_format` (optional)
- `position=(x, y)` (optional, via kwargs)
- `on_result` callback (optional)

```python
s = QueryBox.get_string("Search", value="widgets", master=app)
```

---

### `get_item(...)`

Shows a dropdown selection dialog using a `Combobox`.

Key parameters:
- `items` (required for dropdown behavior)
- `value` (optional initial selection)

Typing filters the dropdown list by substring match.

```python
item = QueryBox.get_item("Pick one", items=["A", "B", "C"], master=app)
```

---

### `get_integer(...)` and `get_float(...)`

Shows a numeric input dialog with validation.

Key parameters:
- `minvalue`, `maxvalue` (optional bounds)
- `increment` (optional step size; applied when using `NumericEntry`)
- `value_format` (optional parsing/formatting)

```python
n = QueryBox.get_integer("Age", minvalue=0, maxvalue=120, master=app)
x = QueryBox.get_float("Threshold", minvalue=0.0, maxvalue=1.0, master=app)
```

Validation behavior:
- invalid type → shows a MessageBox error
- out of range → shows a MessageBox error
- invalid item (when using `items`) → shows a MessageBox error

---

### `get_date(...)`

Shows a calendar date picker dialog (`DateDialog`).

Key parameters:
- `first_weekday` (0=Monday … 6=Sunday)
- `value` (initial date)
- `bootstyle`
- `hide_window_chrome` (popover-style date picker)
- `on_result` callback

```python
from datetime import date

picked = QueryBox.get_date(
    title="Pick a date",
    value=date.today(),
    first_weekday=6,
    hide_window_chrome=True,
    master=app,
)
```

---

### `get_font(...)` and `get_color(...)`

Utility pickers:
- `get_font(...)` uses `FontDialog`
- `get_color(...)` uses `ColorChooserDialog`

```python
font = QueryBox.get_font(master=app, title="Choose font")
color = QueryBox.get_color(master=app, title="Choose color")
```

---

## Events

### `<<DialogResult>>`

`QueryDialog` emits `<<DialogResult>>` on the dialog toplevel (or the provided `master`) after the dialog closes.

Payload (when available):

```python
event.data = {"result": <value>, "confirmed": True/False}
```

You can subscribe using `on_result` on the QueryBox methods, or bind manually.

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryBox

app = ttk.App()

def on_result(payload):
    print("payload:", payload)

QueryBox.get_integer("Number?", master=app, on_result=on_result)

app.mainloop()
```

!!! note "Submit button uses localization keys"
    The default QueryDialog buttons use semantic keys like `button.cancel` and `button.submit`, so they participate in localization automatically.

---

## UX guidance

- Use QueryBox for quick prompts and confirmations that return a single value
- Provide bounds (`minvalue`/`maxvalue`) for numeric inputs to prevent invalid states
- Use `get_item(...)` for short lists; for long lists, prefer `FilterDialog` or a dedicated page
- For multi-field edits, use `FormDialog`

!!! tip "Don’t overuse modal prompts"
    If a value can be edited inline or in a dedicated settings page, that often provides a smoother workflow than repeated prompts.

---

## When to use / when not to

**Use QueryBox when:**

- You need one value (string/number/date/item/font/color)
- You want a consistent, localized OK/Cancel pattern
- You want to avoid building a custom dialog

**Avoid QueryBox when:**

- You need multiple fields with layout and validation (use `FormDialog`)
- The workflow is multi-step (use `PageStack`)
- Feedback is informational only (use `Toast`)

---

## Related widgets

- **QueryDialog** — underlying single-input dialog
- **Dialog** — generic dialog builder
- **FormDialog** — structured multi-field dialog
- **DateDialog / FontDialog / FilterDialog** — specialized dialogs
- **MessageBox** — validation and alert feedback
