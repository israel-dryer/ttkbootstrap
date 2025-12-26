---
title: QueryDialog
---

# QueryDialog

`QueryDialog` is a **modal dialog** for collecting user input with built-in validation.

Use `QueryDialog` when you need to prompt the user for a single value (text, number, date, or item selection). For common patterns, prefer the convenience methods in [QueryBox](querybox.md).

---

## Quick start

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryDialog

app = ttk.App()

dialog = QueryDialog(
    prompt="Enter your name:",
    title="Name Input",
    value="",
)
dialog.show()

if dialog.result:
    print("User entered:", dialog.result)

app.mainloop()
```

---

## When to use

Use `QueryDialog` when:

- you need custom validation (min/max values)
- you want control over the input widget type
- you need programmatic access to dialog events

### Consider a different control when...

- you want a simple string/integer/float prompt -> use [QueryBox](querybox.md) static methods
- you just need to show a message -> use [MessageDialog](messagedialog.md)
- you need a complex multi-field form -> use [FormDialog](formdialog.md)

---

## Common options

### `prompt`

The prompt text to display above the input field. Supports multiline strings.

### `value`

The initial value to populate in the input field.

### `datatype`

Expected data type for validation: `str`, `int`, `float`, or `date`.

```python
from datetime import date

# Integer input
QueryDialog(prompt="Enter age:", datatype=int, minvalue=0, maxvalue=150)

# Date input
QueryDialog(prompt="Select date:", datatype=date)
```

### `minvalue` / `maxvalue`

Range constraints for numeric data types.

### `items`

Optional list of items for dropdown selection. Shows a Combobox instead of Entry.

```python
QueryDialog(
    prompt="Select a color:",
    items=["Red", "Green", "Blue"],
    value="Green",
)
```

### `value_format`

ICU format pattern for formatting/parsing values.

```python
QueryDialog(prompt="Enter amount:", datatype=float, value_format="$#,##0.00")
```

---

## Behavior

- The dialog is modal - blocks interaction with the parent until closed.
- Submit validates the input before closing.
- Invalid input shows an error message and keeps the dialog open.
- Cancel closes without setting a result.

---

## Events

`QueryDialog` emits `<<DialogResult>>` when closed.

```python
def on_result(payload):
    if payload["confirmed"]:
        print("User entered:", payload["result"])
    else:
        print("User canceled")

dialog.on_dialog_result(on_result)
dialog.show()
```

---

## Additional resources

### Related widgets

- [QueryBox](querybox.md) - static convenience methods for common input patterns
- [MessageDialog](messagedialog.md) - message-only dialogs
- [FormDialog](formdialog.md) - multi-field form dialogs
- [Dialog](dialog.md) - base dialog class

### API reference

- [`ttkbootstrap.dialogs.QueryDialog`](../../reference/dialogs/QueryDialog.md)