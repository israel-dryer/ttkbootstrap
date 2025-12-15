---
title: DateEntry
icon: fontawesome/solid/calendar-days
---

# DateEntry

`DateEntry` is a fully featured date input control including a label, input field, and message text.

It combines a familiar text field with a calendar picker popup, built on ttkbootstrap’s field foundation—so it behaves like
your other entry controls (messages, validation, localization, events), while making date entry fast and consistent.

If you are building forms, dialogs, or data-driven UIs, `DateEntry` should usually be your **default calendar date input**.

<figure markdown>
![dateentry states](../../assets/dark/widgets-dateentry-states.png#only-dark)
![dateentry states](../../assets/light/widgets-dateentry-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

due = ttk.DateEntry(
    app,
    label="Due date",
    value="2025-12-31",
    message="Pick a date or type one",
)
due.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Text vs value

All Entry-based controls separate **what the user is typing** from the **committed value**.

| Concept | Meaning |
|---|---|
| Text | Raw, editable string while the field is focused |
| Value | Parsed, validated value committed on blur or Enter |

```python
# get committed value
current = field.value

# set committed value programmatically
field.value = ...
```

If you need the raw text at any time:

```python
raw = field.get()
```

!!! tip "Commit semantics"
    Parsing, validation, and `value_format` are applied **only when the value is committed**
    (blur or Enter), never on every keystroke.

For date controls, the committed `value` is typically a date-like value (or a normalized string),
after parsing and validation.

---

## Picker behavior

`DateEntry` includes a calendar popup that opens from the suffix button.

Common behaviors:

- Click the calendar button → opens the picker
- Click a day → commits the date and closes the popup
- Escape → closes the popup without changing the committed value

<figure markdown>
![dateentry picker](../../assets/dark/widgets-dateentry-popup.png#only-dark)
![dateentry picker](../../assets/dark/widgets-dateentry-popup.png#only-light)
</figure>

---

## Formatting with `value_format`

`DateEntry` supports the same **commit-time formatting** model as `TextEntry` and `NumericEntry`.

Formatting is applied when the value is committed (blur or Enter), allowing users to type naturally while editing.

`value_format` uses the app’s active locale/format settings (configured globally in `AppSettings`),
unless you override formatting behavior at the widget level.

### Named date formats

```python
import ttkbootstrap as ttk

app = ttk.App()

row = ttk.Frame(app, padding=10)
row.pack(fill="x")

ttk.DateEntry(
    row,
    label="Short Date",
    value="March 14, 1981",
    value_format="shortDate",
).pack(side="left", padx=10)

ttk.DateEntry(
    row,
    label="Long Date",
    value="1981-03-14",
    value_format="longDate",
).pack(side="left", padx=10)

app.mainloop()
```

!!! tip "Stable storage, friendly display"
    Keep your **storage format** stable (e.g., ISO strings) and let the control handle display formatting.

<figure markdown>
![dateentry picker](../../assets/dark/widgets-dateentry-formats.png#only-dark)
![dateentry picker](../../assets/dark/widgets-dateentry-formats.png#only-light)
</figure>

---

## Validation

Because `DateEntry` is field-based, you can use the same validation patterns as other entry controls.

```python
import ttkbootstrap as ttk

app = ttk.App()

d = ttk.DateEntry(app, label="Date", required=True)
d.add_validation_rule("required", message="A date is required")
d.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

Common validation patterns:

- required date
- not in the past
- within a business window (e.g., next 90 days)

---

## Events

`DateEntry` emits standard field events:

- `<<Input>>` — text editing
- `<<Changed>>` — committed value changed (typing + Enter/blur, or picker selection)
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

In addition to `widget.bind(...)`, ttkbootstrap provides convenience methods for **all events** in this family:

- `on_*` to attach a handler
- `off_*` to remove a handler

Example: reacting to committed value changes

```python
import ttkbootstrap as ttk

app = ttk.App()

d = ttk.DateEntry(app, label="Due date")
d.pack(fill="x", padx=20, pady=10)

def handle_changed(event):
    print("changed:", event.data)

d.on_changed(handle_changed)

app.mainloop()
```

!!! tip "Live Typing"
    Use `on_input(...)` when you want “live typing” behavior, and `on_changed(...)` when you want the committed value.

---

## Add-ons

Like other field controls, you can insert prefix/suffix add-ons.

```python
import ttkbootstrap as ttk

app = ttk.App()

d = ttk.DateEntry(app, label="Birthday")
d.insert_addon(ttk.Label, position="before", icon='cake-fill')
d.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

<figure markdown>
![dateentry picker](../../assets/dark/widgets-dateentry-addons.png#only-dark)
![dateentry picker](../../assets/dark/widgets-dateentry-addons.png#only-light)
</figure>

---

## Localization

Localization behavior is controlled by the **global application settings**.

By default, widgets use `localize="auto"`. In this mode, `label`, `message`, and `text`
are treated as localization keys **when a translation exists**.
If no translation is found, the value is shown as **plain text**.

You can override this behavior per widget if needed.

```python
# global app localization (default)
ttk.DateEntry(app, label="order.due_date", message="order.due_date.help").pack(fill="x")

# explicitly enable localization
ttk.DateEntry(app, label="order.due_date", localize=True).pack(fill="x")

# explicitly disable localization
ttk.DateEntry(app, label="Due date", message="Pick a date", localize=False).pack(fill="x")
```

!!! tip "Safe to pass literal text"
    With `localize="auto"`, you may pass either localization keys or literal strings.

---

## When should I use DateEntry?

Use `DateEntry` when:

- users need to enter dates reliably
- you want a picker popup and parsing support
- you want consistent label/message/validation behavior

Prefer `TextEntry` when:

- the value is “date-like” but not a calendar date (e.g., “Q4 2025”, “ASAP”, “Next week”)

---

## Related widgets

- **TimeEntry** — time input control
- **TextEntry** — general field control with validation and formatting
- **NumericEntry** — numeric field with bounds and stepping
- **DateDialog** — date selection in a modal dialog
