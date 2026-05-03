---
title: DateEntry
---

# DateEntry

`DateEntry` is a form-ready calendar date input. It combines a text
field — for typing or pasting a date — with a calendar button that
opens a [`DateDialog`](../dialogs/datedialog.md) popup. All of the
field chrome that [`TextEntry`](textentry.md) provides (label, message,
validation, signal/variable binding, accent, density, add-ons) comes
along unchanged.

The committed value is a `date` object, not a string: text is parsed
on commit using `value_format` (default `"longDate"`), and the picker
hands back a `date` directly. Locale-aware formatting and parsing
share the same engine used by `TextEntry` and `NumericEntry`.

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

## Value model

`DateEntry` separates **what is in the field right now** from **the
committed value**:

| Concept | Meaning | How to read it |
|---|---|---|
| Text | The raw editable string in the entry, updated on every keystroke. | `due.get()` |
| Value | The parsed `date` object — produced when the user blurs the field, presses **Enter**, or picks a date from the calendar. | `due.value` |

When you set `due.value = "March 14, 1981"`, the string is parsed by
`value_format` and stored as `date(1981, 3, 14)`; the entry is
re-rendered using the format's display rules. Reading `due.value`
always returns a `date` (or `None` when the field is empty).

```python
due = ttk.DateEntry(app, value="2025-12-31")
print(type(due.value))   # <class 'datetime.date'>
print(due.value.year)    # 2025
```

You can also assign a `date` or `datetime` directly — `datetime`
values are normalized to their date component for display.

### Empty values

When the field is empty:

- with `allow_blank=True` (the default), the committed value is `None`.
- with `allow_blank=False`, the previous value is preserved on commit.

Cancelling the calendar popup leaves the field unchanged.

### Signals and variables

`due.signal` and `due.variable` are bound to the **raw text**, not the
parsed `date`. Pass your own with `textsignal=` or `textvariable=` to
share the field's text with another widget.

```python
text = ttk.Signal("")
due = ttk.DateEntry(app, textsignal=text)
```

!!! tip "Commit semantics"
    Parsing, formatting, and `<<Change>>` only run on commit (focus
    out, **Enter**, or picker selection), never on every keystroke.
    Bind `<<Input>>` if you need live updates as the user types.

---

## Common options

| Option | Purpose |
|---|---|
| `value` | Initial date — accepts a string, `date`, or `datetime`. |
| `value_format` | Format spec used to parse and display the date (default `"longDate"`). Presets include `'longDate'`, `'shortDate'`, `'monthAndDay'`, `'monthAndYear'`, `'quarterAndYear'`, `'dayOfWeek'`, `'year'`, …; or any ICU pattern (e.g. `"yyyy-MM-dd"`). |
| `label` | Text shown above the entry. |
| `message` | Helper text shown below; replaced by validation errors. |
| `required` | Adds an asterisk to the label and a `'required'` validation rule. |
| `show_picker_button` | Show or hide the calendar button (default `True`). |
| `picker_title` | Title of the calendar popup (default `"Select new date"`). |
| `picker_first_weekday` | First column of the calendar grid; `0` = Monday, `6` = Sunday (default `6`). |
| `allow_blank` | Whether an empty input commits as `None` (default) or preserves the previous value. |
| `width` | Width of the entry in characters. |
| `state` | `'normal'`, `'disabled'`, or `'readonly'`. |
| `accent` | Semantic color token for the focus ring (`primary`, `success`, `danger`, …). |
| `density` | `'default'` or `'compact'` for tight forms. |
| `textsignal` / `textvariable` | External signal or Tk variable bound to the raw text. |
| `initial_focus` | Take focus on creation. |

```python
ttk.DateEntry(app, label="Due date")                     # primary (default)
ttk.DateEntry(app, label="Due date", accent="success")
ttk.DateEntry(app, label="Due date", density="compact")
```

!!! link "See [Design System](../../design-system/index.md) for the full set of accent and density tokens."

---

## Behavior

### Date format

`value_format` controls both parsing and display, and resolves through
the active locale. ICU patterns (e.g. `"yyyy-MM-dd"`) are accepted in
addition to the named presets.

```python
ttk.DateEntry(app, label="Long date",  value="March 14, 1981", value_format="longDate").pack()
ttk.DateEntry(app, label="Short date", value="3/14/81",        value_format="shortDate").pack()
ttk.DateEntry(app, label="ISO date",   value="2025-01-15",     value_format="yyyy-MM-dd").pack()
```

<figure markdown>
![dateentry formats](../../assets/dark/widgets-dateentry-formats.png#only-dark)
![dateentry formats](../../assets/light/widgets-dateentry-formats.png#only-light)
</figure>

If the locale changes at runtime, the displayed text is reformatted
automatically — the underlying `date` is unchanged.

!!! link "See [Localization](../../capabilities/localization.md) for the full preset list and ICU pattern syntax."

### Calendar popup

- Click the calendar button — opens the picker, seeded with the current value (or today if empty/invalid).
- Click a day — commits the date and closes the popup.
- Escape — closes the popup without committing.

Hide the picker button with `show_picker_button=False` if the field
should accept typing only. `picker_first_weekday` controls which day
heads the grid (`0` Monday … `6` Sunday).

```python
ttk.DateEntry(app, label="Date", show_picker_button=False)
ttk.DateEntry(app, label="Date", picker_first_weekday=0)   # Monday-first
```

<figure markdown>
![dateentry picker](../../assets/dark/widgets-dateentry-popup.png#only-dark)
![dateentry picker](../../assets/light/widgets-dateentry-popup.png#only-light)
</figure>

### Add-ons

Like other field controls, `DateEntry` accepts prefix and suffix
add-ons via `insert_addon`. They slot in alongside the calendar button
and inherit the field's disabled state.

```python
d = ttk.DateEntry(app, label="Birthday")
d.insert_addon(ttk.Label, position="before", icon="cake-fill")
```

<figure markdown>
![dateentry addons](../../assets/dark/widgets-dateentry-addons.png#only-dark)
![dateentry addons](../../assets/light/widgets-dateentry-addons.png#only-light)
</figure>

### Disable, enable, readonly

```python
due.disable()        # not editable, not focusable; calendar button disables too
due.enable()
due.readonly(True)   # focusable, copyable, not editable; picker still works
due.readonly(False)
```

---

## Events

`DateEntry` emits the same events as `Field`. The picker reuses the
standard `<<Change>>` payload — there is no picker-specific event.

**Input and value events** (callback receives the raw event;
read `event.data`):

| Event | Helper | Fires when… | `event.data` |
|---|---|---|---|
| `<<Input>>` | `on_input` | every keystroke | `{'text': str}` |
| `<<Change>>` | `on_changed` | committed value differs from focus-in value, or a date was picked | `{'value', 'prev_value', 'text'}` |
| `<Return>` | `on_enter` | **Enter** pressed in the field | `{'value', 'text'}` |

`event.data["value"]` is a `date` object (or `None`).

```python
def show_committed(event):
    d = event.data["value"]
    if d is not None:
        print("ISO:", d.isoformat())

due.on_changed(show_committed)
```

**Validation events** (callback receives the payload `dict` directly):

| Event | Helper | Fires when… | Payload |
|---|---|---|---|
| `<<Valid>>` | `on_valid` | validation passes | `{'value', 'is_valid': True, 'message': ''}` |
| `<<Invalid>>` | `on_invalid` | validation fails | `{'value', 'is_valid': False, 'message': str}` |
| `<<Validate>>` | `on_validated` | after any validation | `{'value', 'is_valid': bool, 'message': str}` |

!!! tip "Live vs committed"
    Use `on_input` for live feedback (e.g. mirroring the typed string
    elsewhere). Use `on_changed` when you need a parsed `date`.

---

## Validation and constraints

Rules are added with `add_validation_rule(rule_type, **kwargs)` and
run automatically on key release and blur. Built-in rule types are
`'required'`, `'pattern'`, `'stringLength'`, and `'custom'`. There is
no built-in calendar-bounds rule — express date constraints with
`'custom'` against the parsed value.

```python
from datetime import date, timedelta

due = ttk.DateEntry(app, label="Due date", required=True)

# Must be today or later
due.add_validation_rule(
    "custom",
    func=lambda _v: due.value is not None and due.value >= date.today(),
    message="Date cannot be in the past",
)

# Within the next 90 days
window_end = date.today() + timedelta(days=90)
due.add_validation_rule(
    "custom",
    func=lambda _v: due.value is not None and due.value <= window_end,
    message="Date must be within 90 days",
)
```

A failed rule replaces the message line with the rule's error text and
emits `<<Invalid>>`. A passing rule restores the original message and
emits `<<Valid>>`. Each rule type has a default trigger (`'always'`,
`'blur'`, or `'manual'`); pass `trigger=...` to override.

`'custom'` rules receive the **string** in the entry, not the parsed
date. Read `due.value` inside the rule (as above) when you need to
compare dates — that value is the `date` produced by the most recent
commit.

For cross-field rules (e.g. "end is after start"), wire `on_changed`
on the dependent field and call `field.validate()`:

```python
start = ttk.DateEntry(app, label="Start")
end   = ttk.DateEntry(app, label="End")

end.add_validation_rule(
    "custom",
    func=lambda _v: end.value is None or start.value is None or end.value >= start.value,
    message="End must be on or after start",
)
start.on_changed(lambda _e: end.validation())
```

---

## When should I use DateEntry?

Use `DateEntry` when:

- the field collects a calendar date and you want both typing and a picker UI.
- you want a parsed `date` value with locale-aware formatting (no manual `strptime`).
- the field belongs to a form and should share label/message/validation chrome with the other inputs.

Prefer a different control when:

- the field collects a time of day → use [TimeEntry](timeentry.md).
- the field collects a date *and* time together → use a `DateEntry` plus a `TimeEntry`, or a `TextEntry` with a `longDateLongTime` format.
- the value is "date-like" but not an actual calendar date (a fiscal period code, a free-form string) → use [TextEntry](textentry.md).
- you only need a one-off modal date pick with no persistent input → use [DateDialog](../dialogs/datedialog.md).

---

## Related widgets

- [TimeEntry](timeentry.md) — time-of-day input with the same chrome.
- [TextEntry](textentry.md) — base composite text field; `DateEntry` shares its formatting/validation/signal machinery.
- [DateDialog](../dialogs/datedialog.md) — the calendar popup used by the picker, also usable directly as a modal date prompt.
- [Calendar](../selection/calendar.md) — standalone calendar widget for inline use.
- [Form](form.md) — assemble a full form from field declarations.

---

## Reference

- **API reference:** [`ttkbootstrap.DateEntry`](../../reference/widgets/DateEntry.md)
- **Related guides:**
    - [Forms](../../guides/forms.md)
    - [Formatting](../../guides/formatting.md)
    - [Localization](../../capabilities/localization.md)
    - [Signals](../../capabilities/signals/signals.md)
