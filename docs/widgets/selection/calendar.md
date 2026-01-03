---
title: Calendar
---

# Calendar

`Calendar` is an **inline date selection control** for choosing either a **single date** or a **date range**.

It produces `datetime.date` values and is commonly used for scheduling views, reporting filters, availability selection, and any UI where users benefit from seeing dates in context instead of typing them.

If you want a compact, form-friendly input (typed + popup), prefer **DateEntry**. If you want an always-visible picker embedded in a panel, use **Calendar**.

---

## Quick start

```python
from datetime import date
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.calendar import Calendar

app = ttk.App()

cal = Calendar(app, value=date.today(), accent="primary")
cal.pack(padx=12, pady=12)

def on_select(e):
    # {'date': date, 'range': (start, end|None)}
    print(e.data)

cal.on_date_selected(on_select)

app.mainloop()
```

---

## When to use

Use Calendar when:

* you want an always-visible date picker embedded in a panel

* users benefit from seeing the whole month(s) while selecting

* you want a natural range-selection interaction

### Consider a different control when

* you need a compact form control — use [DateEntry](../inputs/dateentry.md)

* typing or pasted dates are a primary workflow — use [DateEntry](../inputs/dateentry.md)

* screen space is limited — use [DateEntry](../inputs/dateentry.md)

---

## Appearance

### Variants

Calendar supports two selection models:

* **Single** (`selection_mode="single"`): selects exactly one `date`

* **Range** (`selection_mode="range"`): selects a start date, then an end date; dates between are highlighted

Range mode displays **two months side-by-side** to make cross-month selection easier.

#### Single date

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.calendar import Calendar

app = ttk.App()
Calendar(app, value="2025-12-25").pack(padx=12, pady=12)
app.mainloop()
```

#### Date range

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.calendar import Calendar

app = ttk.App()
Calendar(app, selection_mode="range", start_date="2025-12-01", end_date="2025-12-12").pack(padx=12, pady=12)
app.mainloop()
```

### Colors and styling

Use `accent` to set the accent color used for:

* the selected day (single mode)

* the range endpoints and in-range highlight (range mode)

```python
Calendar(app, accent="success")
Calendar(app, selection_mode="range", accent="warning")
```

Calendar also uses internal style names for day/range rendering (e.g. `*-calendar_day-toolbutton`, `*-calendar_date-toolbutton`, `*[subtle]-calendar_range-toolbutton`) so it can visually distinguish:

* normal selectable days

* selected endpoints

* in-range days

!!! link "Design System"
    For a complete overview of theming, colors, and style tokens, see the [Design System](../../design-system/index.md) documentation.

---

## Examples and patterns

### Value API

Calendar provides a standard `get()/set()/.value` API for accessing and modifying the selected date.

**Single mode:**

```python
# Get the selected date
selected = cal.get()        # datetime.date or None
selected = cal.value        # same thing

# Set the selected date programmatically
cal.set(date(2025, 6, 15))
cal.set("2025-06-15")       # ISO string also works
cal.value = date(2025, 6, 15)
```

**Range mode:**

```python
# Get the selected range
start, end = cal.get_range()  # (date|None, date|None)
start, end = cal.range        # same thing

# Set the range programmatically
cal.set_range(date(2025, 1, 10), date(2025, 1, 20))
cal.set_range("2025-01-10", "2025-01-20")  # ISO strings work
cal.range = (date(2025, 1, 10), date(2025, 1, 20))
```

!!! note "Programmatic vs User Updates"
    `set()` and `set_range()` do **not** emit `<<DateSelect>>`. This follows the standard Tk pattern where programmatic updates don't trigger events. User interactions still emit the event.

### How selection works

Calendar maintains:

* a **current date** (`date`) and

* a **range** (`(start_date, end_date | None)`)

Value type:

* single mode: effectively a `date`

* range mode: `start_date` and `end_date` (with `end_date` becoming non-`None` after the second click)

Selection semantics:

* In range mode:

  * first click sets the start

  * second click sets the end (and will reorder if end < start)

  * a third click starts a new range (clearing the previous end)

The value is considered **committed immediately** when a day is clicked (it generates `<<DateSelect>>`).

### Common options

Selection:

* `selection_mode`: `"single"` (default) or `"range"`

* `value`: initial selected date for single mode (`date`, `datetime`, or string)

* `start_date`: range start date (`date`, `datetime`, or string); use `value` for single mode

* `end_date`: range end (range mode only)

Constraints:

* `min_date`: minimum selectable date

* `max_date`: maximum selectable date

* `disabled_dates`: iterable of dates that cannot be selected

Display:

* `show_outside_days`: show adjacent-month days
  Defaults to `True` for single mode and `False` for range mode.

* `show_week_numbers`: show ISO week numbers (default `False`)

* `first_weekday`: `0=Monday` … `6=Sunday`, or `None` for locale default (default `None`)

Style:

* `accent`: accent color used for selection and highlights (default `"primary"`)

Layout:

* `padding`: padding around the widget (standard ttk padding values)

### Binding to signals or variables

Calendar does not expose a `variable=`/`textvariable=` binding for selection.

Use the selection event and query the value:

```python
def on_select(e):
    selected = e.data["date"]
    start, end = e.data["range"]
```

If you need an app-level reactive value, update your own `StringVar`/signal inside the handler.

### Events

Calendar emits:

* `<<DateSelect>>` when the selection changes (including reset)

Use the convenience helpers:

```python
def on_select(e):
    print(e.data)

bind_id = cal.on_date_selected(on_select)

# later:
cal.off_date_selected(bind_id)
```

### Validation and constraints

Calendar enforces constraints at interaction time:

* dates in `disabled_dates` are not selectable

* dates before `min_date` or after `max_date` are not selectable

* month navigation is clamped so you can't navigate entirely outside the allowed min/max month window

---

## Behavior

* Month navigation is provided via chevron buttons.

* In single mode, there is a single header; in range mode, each month has its own header and navigation is mirrored.

* Disabled dates (explicit, or outside min/max) cannot be selected.

* `show_outside_days=False` hides adjacent-month cells and removes them from focus/selection.

Keyboard focus:

* Day cells are focusable `Checkbutton`-style controls (disabled cells are not focusable).

---

## Localization

Calendar localizes:

* weekday headers via `MessageCatalog` tokens (`day.mo`, `day.tu`, …)

* month/year header via Babel date formatting (with a fallback)

It refreshes automatically when `<<LocaleChanged>>` is generated.

!!! link "Localization"
    For complete details on internationalization and locale configuration, see the [Localization](../../capabilities/localization.md) documentation.

---

## Additional resources

### Related widgets

* [DateEntry](../inputs/dateentry.md) — compact typed date input

* DateRangeEntry — compact start/end inputs (if present)

* Popover / Dialog date picker — calendar shown in an overlay (if present)

### Framework concepts

* [Selection](../../capabilities/state-and-interaction.md)

* [Forms](../../guides/forms.md)

* [Localization](../../capabilities/localization.md)

### API reference

- [`ttkbootstrap.Calendar`](../../reference/widgets/Calendar.md)