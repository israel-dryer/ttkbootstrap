---
title: Calendar
---

# Calendar

`Calendar` is an inline date-picker that shows one or two months of
day cells and produces a `datetime.date` value (or a
`(start, end)` tuple in range mode). Selection is driven entirely by
clicking day cells in the displayed month(s); there is no `signal=`
or `variable=` channel — observers either bind `<<DateSelect>>` or
read `cal.value` / `cal.range` directly.

Unlike [DateEntry](../inputs/dateentry.md), Calendar is intended to
sit visibly in a panel rather than open as a popup. Use DateEntry
when typing or paste-in flows are primary; use Calendar when users
benefit from seeing the whole month while choosing.

<figure markdown>
![calendar](../../assets/dark/widgets-calendar.png#only-dark)
![calendar](../../assets/light/widgets-calendar.png#only-light)
</figure>

---

## Basic usage

```python
from datetime import date
import ttkbootstrap as ttk

app = ttk.App()

cal = ttk.Calendar(app, value=date(2025, 6, 15), accent="primary")
cal.pack(padx=12, pady=12)

cal.on_date_selected(lambda e: print(e.data))

app.mainloop()
```

In single mode (the default) `cal.value` returns a `date`; in range
mode `cal.range` returns the `(start, end)` tuple.

---

## Selection model

Calendar holds two pieces of state that the public API exposes
separately:

| Mode | What `cal.value` returns | What `cal.range` returns |
|---|---|---|
| `selection_mode="single"` (default) | the selected `date` | `(date, None)` (start mirrors value) |
| `selection_mode="range"` | the most-recently-clicked `date` | `(start, end \| None)` |

**Value type.** Always `datetime.date`. ISO-format strings
(`"2025-12-25"`), `MM/DD/YYYY` strings, and `datetime` objects are
coerced through `_coerce_date` at every public entry point —
`value=`, `start_date=`, `end_date=`, `set()`, `set_range()`, and
the `value` / `range` property setters. Strings that don't match
either format are silently ignored.

**Independent.** Calendar does not participate in any group. There
is no shared-variable mechanism, no `signal=`, no `variable=`. To
react to changes, bind `<<DateSelect>>` (see Events).

**Initial state.** In single mode pass `value=`. In range mode pass
`start_date=` and `end_date=` (`value=` is treated as an alias for
`start_date=`). When both bounds are given and `end_date < start_date`,
the constructor swaps them. If nothing is passed, the display opens
on today's month and `_selected_date` is set to `date.today()` but
`range` is `(None, None)`.

**No-selection.** In range mode the range can be `(None, None)`
(after `cal.range = None` or `cal.set_range(None, None)`). In single
mode there is no "cleared" state — `value=None` is silently ignored
by `set()` and the property setter.

**Commit semantics.** A user click on a day cell commits immediately
and emits `<<DateSelect>>`. Programmatic `set()`, `set_range()`, the
`value` / `range` property setters, and `configure(date=...)`
**do not emit the event** — they are silent state writes, matching
the standard Tk pattern for programmatic updates.

```python
cal = ttk.Calendar(app, selection_mode="range")
cal.set_range(date(2025, 1, 10), date(2025, 1, 20))   # silent
print(cal.range)                                        # (2025-01-10, 2025-01-20)
print(cal.value)                                        # 2025-01-20 (the end date)
```

!!! warning "Range mode: prefer `range` over `value`"
    In range mode `cal.value` returns whichever end of the range was
    set most recently — and after `cal.range = None` it can return a
    *stale* date even though the range tuple is `(None, None)` (the
    underlying `_selected_date` is not cleared by range setters).
    Use `cal.range` for range-mode reads.

!!! warning "`set()` and `set_range()` bypass constraints"
    The interactive paths refuse clicks on dates that are in
    `disabled_dates` or outside `[min_date, max_date]`. The
    programmatic setters (`set`, `set_range`, the property setters,
    and `configure(date=...)`) **do not** — they accept any
    coercible date. If your code routes user input through `set()`,
    re-validate before calling.

---

## Common options

| Option | Type | Default | Notes |
|---|---|---|---|
| `selection_mode` | `"single"` \| `"range"` | `"single"` | Range mode displays two months side-by-side. Construction-only. |
| `value` | `date` \| `datetime` \| `str` \| `None` | `None` | Initial date for single mode; in range mode aliases `start_date`. |
| `start_date` | `date` \| `datetime` \| `str` \| `None` | `None` | Range start. |
| `end_date` | `date` \| `datetime` \| `str` \| `None` | `None` | Range end. Auto-swapped with `start_date` if `end < start`. |
| `min_date` | `date` \| `datetime` \| `str` \| `None` | `None` | Earliest selectable date and earliest navigable month. |
| `max_date` | `date` \| `datetime` \| `str` \| `None` | `None` | Latest selectable date and latest navigable month. |
| `disabled_dates` | `Iterable[date \| datetime \| str]` | `None` | Specific dates that cannot be selected. |
| `show_outside_days` | `bool` \| `None` | `None` | Renders days from neighboring months as muted cells. Defaults to `True` in single mode and `False` in range mode. |
| `show_week_numbers` | `bool` | `False` | Adds a leftmost ISO-week-number column. |
| `first_weekday` | `int` \| `None` | `None` | `0=Monday` … `6=Sunday`. `None` reads the first day of the week from the current locale via Babel; falls back to Monday on failure. |
| `accent` | str | `"primary"` | Tints the selected day, range endpoints, and the in-range fill. |
| `bootstyle` | str | `None` | Deprecated. `accent` wins when both are passed. |
| `padding` | int \| tuple \| str | `None` | Outer ttk padding. |

`accent`, `value`, and `range` are reconfigurable via the property
setters. `selection_mode`, `show_outside_days`,
`show_week_numbers`, `first_weekday`, `min_date`, `max_date`, and
`disabled_dates` are construction-only — `configure(...)` does not
re-run `_build_ui`.

```python
cal = ttk.Calendar(
    app,
    accent="success",
    selection_mode="range",
    start_date="2025-12-01",
    end_date="2025-12-12",
    show_week_numbers=True,
)
```

### Colors & Styling

`accent` drives every selection-related surface. Internally Calendar
constructs day cells as `CheckToggle` widgets registered against
four custom Toolbutton style variants:

- `calendar-day` — selectable in-month days (default cell).
- `calendar-date` — start and end of a selected range, and the
  single-mode selected day.
- `calendar-range` — interior in-range days (uses a subtler tint).
- `calendar-outside` — neighboring-month "outside days" (rendered
  with the `ghost` look and disabled).

These are not user-overridable through public options; they exist so
the four cell states render distinctly under the same accent.

!!! link "Design System"
    For the full theming model and color tokens, see the
    [Design System](../../design-system/index.md) documentation.

---

## Behavior

**Header layout.** Single mode shows one header
(`«` `‹` `Month Year` `›` `»`) above the grid. Range mode replaces
it with two per-month headers — the left header keeps the back
chevrons, the right header keeps the forward chevrons, and the
inner chevrons are swapped out for invisible spacers so the column
widths stay aligned across both months.

**Click the title to reset.** Clicking the centered `Month Year`
label snaps the display back to the constructor's initial month,
restores the initial selection, and fires `<<DateSelect>>`. This is
an undocumented feature of the original page, but it is part of the
shipped behavior. The right-click bindings on the year chevrons
(`«`, `»`) are aliases for left-click — same handler.

**Navigation clamp.** The four chevron buttons walk
`_display_date` by one month or one year. `_is_month_allowed`
rejects any candidate whose first-of-month falls outside
`[min_date, max_date]` (using `replace(day=1)` for the bounds
check), so the user can never scroll past a configured edge.

!!! warning "min/max + no `value=` can lock navigation"
    When you pass `min_date` / `max_date` but omit `value=` /
    `start_date=`, the display opens on today's month — and if today
    is outside the configured window, both chevrons are blocked
    immediately because every candidate fails the clamp. The user
    sees an unselectable view with no way to navigate.
    Always pair `min_date` / `max_date` with an in-range `value=`
    (or `start_date=`).

**Click rules in range mode.**

1. With no range in progress, the first click sets `start_date` and
   leaves `end_date` as `None`.
2. The second click sets `end_date`; if the click is earlier than
   the existing start, start and end are swapped before commit.
3. A third click discards the previous range and sets a new
   `start_date`, with `end_date` reset to `None`.

**Disabled rendering.** Cells in `disabled_dates`, before
`min_date`, or after `max_date` render with the `disabled` ttk
state, lose `takefocus`, and refuse clicks. Outside-month cells
(when `show_outside_days=True`) are also disabled and use the
`calendar-outside` variant; when `show_outside_days=False` they
render as empty cells (and entire empty rows are removed via
`grid_remove`).

**Keyboard contract.** Day cells are focusable Toolbutton-shaped
`CheckToggle` widgets. Tab walks through the in-month, non-disabled
cells in row-major order; `<space>` and `<Return>` invoke the cell.
There is no arrow-key grid navigation today — Tab/Shift-Tab is the
only keyboard path through the grid.

**Locale refresh.** Calendar binds `<<LocaleChanged>>` and
re-renders weekday headers (via `MessageCatalog.translate` over
`day.mo` … `day.su` tokens) and month/year titles (via
`babel.dates.format_skeleton('yMMMM', ...)`) when the locale
changes. `first_weekday=None` is resolved once at construction
through Babel's `Locale.parse(...).first_week_day`.

---

## Events

Calendar emits a single virtual event:

| Event | Payload (`event.data`) | Fires on |
|---|---|---|
| `<<DateSelect>>` | `{"date": date, "range": (date, date \| None)}` | User click on a day cell, and the title-click reset. |

The event does **not** fire on any programmatic state change —
`set()`, `set_range()`, `value` / `range` property setters, and
`configure(date=...)` are all silent.

```python
def on_select(event):
    selected_date = event.data["date"]
    start, end = event.data["range"]
    print(selected_date, start, end)

bind_id = cal.on_date_selected(on_select)

# later
cal.off_date_selected(bind_id)
```

`on_date_selected` is `bind('<<DateSelect>>', cb, add=True)`, so
multiple subscribers coexist. If you need to react to programmatic
writes too, hook the call sites in your application code — there is
no internal observability channel for the silent paths.

---

## When should I use Calendar?

Use Calendar when:

- the picker should always be visible on screen (a sidebar, a
  scheduling panel, a reporting filter strip)
- the surrounding UI benefits from showing a whole month or two
  months at a glance
- range selection is a primary interaction and you want the
  endpoint highlighting and span fill on a real grid

Prefer [DateEntry](../inputs/dateentry.md) when:

- the picker should live inside a form alongside other inputs
- typing or pasting an ISO date is a primary path
- screen real estate is scarce — DateEntry is a single line until
  the user opens its popup

For range entry as two compact form inputs, look at
[DateRangeEntry](../inputs/dateentry.md) (if your app already uses
the DateEntry stack) instead of pairing two Calendars.

---

## Related widgets

- **[DateEntry](../inputs/dateentry.md)** — compact entry-style
  date input with a popup calendar.
- **DateDialog** — modal date picker built on Calendar.

---

## Reference

- **API reference:** [`ttkbootstrap.Calendar`](../../reference/widgets/Calendar.md)
- **Related guides:** [Forms](../../guides/forms.md),
  [Localization](../../capabilities/localization.md)
