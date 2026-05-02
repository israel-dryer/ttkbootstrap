---
title: TimeEntry
---

# TimeEntry

`TimeEntry` is a form-ready time-of-day input. It combines a text
field — for typing or pasting a time — with a searchable dropdown of
time intervals. All of the field chrome that
[`TextEntry`](textentry.md) provides (label, message, validation,
signal/variable binding, accent, density, add-ons) comes along
unchanged.

The committed value is a `datetime.time` object: typed text is parsed
on commit using `value_format` (default `"shortTime"`), and dropdown
selection commits a parsed time directly. `TimeEntry` is built on
[`SelectBox`](../inputs/selectbox.md), so the picker is
type-to-filter and accepts custom values that aren't in the list.

<figure markdown>
![timeentry](../../assets/dark/widgets-timeentry.png#only-dark)
![timeentry](../../assets/light/widgets-timeentry.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

start = ttk.TimeEntry(
    app,
    label="Start time",
    value="08:30",
)
start.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

When `value` is omitted, the field is initialized to the current time.

---

## Value model

`TimeEntry` separates **what is in the field right now** from **the
committed value**:

| Concept | Meaning | How to read it |
|---|---|---|
| Text | The raw editable string in the entry, updated on every keystroke. | `start.get()` |
| Value | The parsed `time` object — produced when the user blurs the field, presses **Enter**, or picks an entry from the dropdown. | `start.value` |

When you set `start.value = "08:30"`, the string is parsed by
`value_format` and stored as `time(8, 30)`; the entry is re-rendered
using the format's display rules. Reading `start.value` always returns
a `time` (or `None` when the field is empty).

```python
start = ttk.TimeEntry(app, value="08:30")
print(type(start.value))   # <class 'datetime.time'>
print(start.value.hour)    # 8
```

You can also assign a `datetime.time` directly.

### Empty values

When the field is empty:

- with `allow_blank=True` (the default), the committed value is `None`.
- with `allow_blank=False`, the previous value is preserved on commit.

Cancelling the dropdown with **Escape** leaves the field unchanged.

### Signals and variables

`start.signal` and `start.variable` are bound to the **raw text**, not
the parsed `time`. Pass your own with `textsignal=` or `textvariable=`
to share the field's text with another widget.

```python
text = ttk.Signal("")
start = ttk.TimeEntry(app, textsignal=text)
```

!!! tip "Commit semantics"
    Parsing, formatting, and `<<Change>>` only run on commit (focus
    out, **Enter**, or dropdown selection), never on every keystroke.
    Bind `<<Input>>` if you need live updates as the user types or
    filters the list.

---

## Common options

| Option | Purpose |
|---|---|
| `value` | Initial time — accepts a string or `datetime.time`. Defaults to the current time. |
| `value_format` | Format spec used to parse and display the time (default `"shortTime"`). Presets: `'shortTime'` (3:30 PM), `'longTime'` (3:30:45 PM PST), `'mediumTime'`, `'hour'`, `'minute'`; or any ICU pattern (e.g. `"HH:mm"`, `"h:mm a"`). |
| `interval` | Minutes between dropdown entries (default `30`). |
| `min_time` | First time in the dropdown (default `00:00`). String or `time`. |
| `max_time` | Last time in the dropdown (default `23:59`). String or `time`. If `max_time < min_time`, the range crosses midnight. |
| `label` | Text shown above the entry. |
| `message` | Helper text shown below; replaced by validation errors. |
| `required` | Adds an asterisk to the label and a `'required'` validation rule. |
| `allow_blank` | Whether an empty input commits as `None` (default) or preserves the previous value. |
| `width` | Width of the entry in characters. |
| `state` | `'normal'`, `'disabled'`, or `'readonly'`. |
| `accent` | Semantic color token for the focus ring (`primary`, `success`, `danger`, …). |
| `density` | `'default'` or `'compact'` for tight forms. |
| `textsignal` / `textvariable` | External signal or Tk variable bound to the raw text. |
| `initial_focus` | Take focus on creation. |

```python
ttk.TimeEntry(app, label="Start time")                     # primary (default)
ttk.TimeEntry(app, label="Start time", accent="success")
ttk.TimeEntry(app, label="Start time", density="compact")
```

!!! link "See [Design System](../../design-system/index.md) for the full set of accent and density tokens."

---

## Behavior

### Time format

`value_format` controls both parsing and display, and resolves through
the active locale. ICU patterns are accepted in addition to the named
presets.

```python
ttk.TimeEntry(app, label="Short time", value_format="shortTime")  # "3:30 PM"
ttk.TimeEntry(app, label="Long time",  value_format="longTime")   # "3:30:45 PM PST"
ttk.TimeEntry(app, label="24-hour",    value_format="HH:mm")      # "15:30"
```

If the locale changes at runtime, the displayed text is reformatted
automatically — the underlying `time` is unchanged.

!!! link "See [Localization](../../capabilities/localization.md) for the full preset list and ICU pattern syntax."

### Dropdown intervals

The dropdown is generated from `min_time`, `max_time`, and `interval`.
The list itself is for convenience; users can always type any time —
including values outside the listed range — because custom values are
allowed.

```python
ttk.TimeEntry(app, label="Slot", interval=15)                            # every 15 minutes
ttk.TimeEntry(app, label="Office hours", min_time="09:00", max_time="17:00")
ttk.TimeEntry(app, label="Overnight",   min_time="22:00", max_time="02:00")  # crosses midnight
```

### Dropdown popup

- Click the clock button or focus the entry — opens the popup.
- Type to filter the list (matches against the formatted time strings).
- Click an entry, or press **Enter** on a highlighted entry — commits the time and closes the popup.
- **Escape** — closes the popup without committing.

If the typed value isn't in the list, it's still accepted on commit
as long as it parses against `value_format`.

### Add-ons

Like other field controls, `TimeEntry` accepts prefix and suffix
add-ons via `insert_addon`. They slot in alongside the dropdown button
and inherit the field's disabled state.

```python
t = ttk.TimeEntry(app, label="Start")
t.insert_addon(ttk.Label, position="before", icon="clock")
```

### Disable, enable, readonly

```python
start.disable()        # not editable, not focusable; dropdown disables too
start.enable()
start.readonly(True)   # focusable, copyable, not editable; dropdown still works
start.readonly(False)
```

---

## Events

`TimeEntry` emits the same events as `SelectBox` and `Field`. Dropdown
selection reuses the standard `<<Change>>` payload — there is no
picker-specific event.

**Input and value events** (callback receives the raw event;
read `event.data`):

| Event | Helper | Fires when… | `event.data` |
|---|---|---|---|
| `<<Input>>` | `on_input` | every keystroke | `{'text': str}` |
| `<<Change>>` | `on_changed` | committed value differs from focus-in value, or a dropdown entry was picked | `{'value', 'prev_value', 'text'}` |
| `<Return>` | `on_enter` | **Enter** pressed in the field | `{'value', 'text'}` |

`event.data["value"]` is a `datetime.time` (or `None`).

```python
def show_committed(event):
    t = event.data["value"]
    if t is not None:
        print("ISO:", t.isoformat(timespec="minutes"))

start.on_changed(show_committed)
```

**Validation events** (callback receives the payload `dict` directly):

| Event | Helper | Fires when… | Payload |
|---|---|---|---|
| `<<Valid>>` | `on_valid` | validation passes | `{'value', 'is_valid': True, 'message': ''}` |
| `<<Invalid>>` | `on_invalid` | validation fails | `{'value', 'is_valid': False, 'message': str}` |
| `<<Validate>>` | `on_validated` | after any validation | `{'value', 'is_valid': bool, 'message': str}` |

!!! tip "Live vs committed"
    Use `on_input` for live feedback (e.g. mirroring the typed string
    elsewhere). Use `on_changed` when you need a parsed `time`.

---

## Validation and constraints

Rules are added with `add_validation_rule(rule_type, **kwargs)` and
run automatically on key release and blur. Built-in rule types are
`'required'`, `'pattern'`, `'stringLength'`, and `'custom'`. There is
no built-in time-bounds rule — `min_time` and `max_time` only
constrain the dropdown list, not what the user can type. Express time
constraints with `'custom'` against the parsed value.

```python
from datetime import time

start = ttk.TimeEntry(app, label="Start time", required=True)

# Within business hours
def in_business_hours(_v):
    v = start.value
    return v is not None and time(9, 0) <= v <= time(17, 0)

start.add_validation_rule(
    "custom",
    func=in_business_hours,
    message="Choose a time between 9:00 AM and 5:00 PM",
)
```

A failed rule replaces the message line with the rule's error text and
emits `<<Invalid>>`. A passing rule restores the original message and
emits `<<Valid>>`. Each rule type has a default trigger (`'always'`,
`'blur'`, or `'manual'`); pass `trigger=...` to override.

`'custom'` rules receive the **string** in the entry, not the parsed
time. Read `field.value` inside the rule (as above) when you need to
compare times — that value is the `time` produced by the most recent
commit.

For cross-field rules (e.g. "end is after start"), wire `on_changed`
on the dependent field and call `field.validation()`:

```python
start = ttk.TimeEntry(app, label="Start")
end   = ttk.TimeEntry(app, label="End")

end.add_validation_rule(
    "custom",
    func=lambda _v: end.value is None or start.value is None or end.value > start.value,
    message="End must be after start",
)
start.on_changed(lambda _e: end.validation())
```

---

## When should I use TimeEntry?

Use `TimeEntry` when:

- the field collects a time of day and the user benefits from a quick interval picker.
- you want a parsed `time` value with locale-aware formatting (no manual `strptime`).
- the field belongs to a form and should share label/message/validation chrome with the other inputs.

Prefer a different control when:

- the field collects a calendar date → use [DateEntry](dateentry.md).
- the field collects a date *and* time together → pair a `DateEntry` with a `TimeEntry`, or use a `TextEntry` with a `longDateLongTime` format.
- the value is "time-like" but not an actual clock time (a duration, a frequency) → use [TextEntry](textentry.md) or [NumericEntry](numericentry.md).
- users should step through values in fixed increments without a list popup → use [SpinnerEntry](spinnerentry.md).

---

## Related widgets

- [DateEntry](dateentry.md) — calendar date input with the same chrome.
- [SelectBox](../inputs/selectbox.md) — base composite that `TimeEntry` extends; useful when you want the same searchable-dropdown UX over an arbitrary list.
- [TextEntry](textentry.md) — base composite text field; `TimeEntry` shares its formatting/validation/signal machinery.
- [SpinnerEntry](spinnerentry.md) — entry that steps through values without a popup.
- [Form](form.md) — assemble a full form from field declarations.

---

## Reference

- **API reference:** [`ttkbootstrap.TimeEntry`](../../reference/widgets/TimeEntry.md)
- **Related guides:**
    - [Forms](../../guides/forms.md)
    - [Formatting](../../guides/formatting.md)
    - [Localization](../../capabilities/localization.md)
    - [Signals](../../capabilities/signals/signals.md)
