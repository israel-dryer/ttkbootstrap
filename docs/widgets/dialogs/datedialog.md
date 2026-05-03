---
title: DateDialog
---

# DateDialog

`DateDialog` is a modal calendar picker. It wraps the
[`Calendar`](../selection/calendar.md) widget in a chrome-capable
dialog: open it, the user clicks a day, and the dialog **commits and
closes on that click** — there is no OK/Cancel footer. The selected
date is then available on `.result`.

It's the right shape for a one-shot pick-a-date task that doesn't
need to live inline (a "due date" prompt, a report range start, an
"open to" calendar). For inline keyboard-typeable input, prefer
[`DateEntry`](../inputs/dateentry.md). For a calendar embedded in a
page (no dialog at all), use [`Calendar`](../selection/calendar.md)
directly.

---

## Basic usage

Construct, `show()`, read `.result`:

```python
import ttkbootstrap as ttk
from datetime import date

app = ttk.App()

dlg = ttk.DateDialog(
    title="Choose a date",
    initial_date=date(2026, 1, 15),
)
dlg.show()

print("selected:", dlg.result)  # datetime.date or None

app.mainloop()
```

`show()` blocks until the user clicks a day or dismisses the dialog.
Branch on `.result is not None` rather than truthiness — every
`datetime.date` is truthy, but the explicit `is not None` check makes
the cancel branch unambiguous.

For a popover-style picker that closes when the user clicks
elsewhere (no modal grab), pass `close_on_click_outside=True`:

```python
dlg = ttk.DateDialog(
    initial_date=date.today(),
    close_on_click_outside=True,
    hide_window_chrome=True,
)
dlg.show(anchor_to=button, anchor_point="sw", window_point="nw")
```

---

## Result value

`.result` is the selected `datetime.date`, or `None` when the user
dismissed the dialog without picking a day:

```python
dlg.result  # datetime.date or None
```

`.result` is set the moment the user clicks a non-disabled day in
the embedded calendar — that same click commits and destroys the
toplevel. `show()` returns immediately afterward. Cancel paths
(Escape, the window close button, an outside click in popover mode)
leave `.result` as `None` and do **not** fire any result event.

Navigation actions inside the calendar — clicking the previous /
next month arrows, or pressing the "Today" reset — do **not**
commit. Only an explicit day-cell click counts as a selection.

---

## Common options

| Option | Purpose |
|---|---|
| `title` | Window title text. Default `" "` (single space). |
| `initial_date` | Date shown when the dialog opens. Default `date.today()`. Accepts a `date`, `datetime`, or ISO date string. |
| `first_weekday` | First weekday in the grid: `0=Monday … 6=Sunday`. Default `6` (Sunday). |
| `min_date` / `max_date` | Inclusive bounds on selectable days. Days outside are rendered but disabled. |
| `disabled_dates` | Iterable of `date` / `datetime` / ISO strings to render disabled. |
| `show_outside_days` | Whether days from the previous/next month fill the grid edges. Defaults to the `Calendar` default (`True`). |
| `show_week_numbers` | Render an ISO week-number column on the left. Default `False`. |
| `accent` | Calendar accent token (`primary`, `success`, …). Themes the selected-day chip and today indicator. |
| `hide_window_chrome` | Removes the window decorations via override-redirect. macOS silently falls back to a normal toplevel (Tk/Cocoa limitation). |
| `close_on_click_outside` | Switches the dialog to popover mode (no grab; closes on outside click). |
| `master` | Parent widget. Defaults to the application root. |

```python
ttk.DateDialog(
    title="Pick a delivery date",
    initial_date=date.today(),
    min_date=date.today(),
    max_date=date.today() + timedelta(days=60),
    disabled_dates=public_holidays,
    accent="success",
    show_week_numbers=True,
)
```

For a fuller list of calendar-side options (selection mode, range
selection, week starts, etc.), see [`Calendar`](../selection/calendar.md)
— `DateDialog` forwards the listed options through to the embedded
calendar verbatim.

---

## Behavior

### Modal vs popover

The default mode is `modal`: the parent window is grabbed and the
calendar is centered (or anchored, see below). `show()` waits for
the dialog to close.

Setting `close_on_click_outside=True` switches to `popover` mode —
no grab is taken, and the dialog closes when the user clicks any
widget outside the toplevel hierarchy. The picker still commits on
day-cell click; the only difference is the cancel path. Pair this
with `hide_window_chrome=True` and an `anchor_to=` widget for an
inline-popup effect.

### No buttons, click-to-commit

`DateDialog` builds with `buttons=[]` — there is **no OK or Cancel
button** in the footer (and no footer at all). The dialog commits
the moment the user clicks a non-disabled day. To dismiss without
a selection the user presses Escape, closes the window, or (in
popover mode) clicks outside.

If you need an explicit confirm step or "Today / Clear" actions,
build your own `Dialog` around a `Calendar` directly rather than
trying to bolt buttons onto `DateDialog`.

### Default positioning

If you don't pass `position=` and don't pass `anchor_to=`, `show()`
defaults to the **bottom-right corner of the parent window** (using
`master.winfo_rootx() + master.winfo_width()`). When the dialog has
no usable parent, it falls back to centering on screen.

`show()` also accepts the same anchoring options as
[`Dialog.show`](dialog.md): `anchor_to`, `anchor_point`,
`window_point`, `offset`, `auto_flip`. The most common shape is
anchoring to the trigger widget:

```python
button = ttk.Button(parent, text="Pick…", command=open_picker)

def open_picker():
    dlg = ttk.DateDialog(close_on_click_outside=True,
                         hide_window_chrome=True)
    dlg.show(anchor_to=button, anchor_point="sw", window_point="nw")
    if dlg.result is not None:
        button.configure(text=dlg.result.isoformat())
```

### Bounds, disabled dates, and validation

`min_date` / `max_date` and `disabled_dates` are enforced by the
embedded calendar — disabled cells render greyed and cannot be
clicked, so they cannot be committed. There is no validation
callback or "force resubmit" path; if the user couldn't pick the
date, `.result` is `None`.

For business rules beyond bounds and explicit blocklists ("only
weekdays", "only the 1st and 15th of each month"), pre-compute the
disabled set and pass it as `disabled_dates`.

### Default and Escape bindings

There is no Enter binding (no default button to press). Escape
destroys the toplevel with `.result = None`. The window-manager
close button does the same.

---

## Events

| Hook | Fires |
|---|---|
| `on_result(callback)` → `funcid` | Once per successful selection, after `.result` has been set and before the toplevel is destroyed. |
| `<<DialogResult>>` | Same moment as `on_result`. Bind directly on the dialog's toplevel (or pre-bind on `master`) to receive `event.data = {"result": date, "confirmed": True}`. |

`on_result` returns a Tk binding ID that can be passed to
`off_result` to unregister:

```python
def picked(payload):
    print("picked:", payload["result"])

funcid = dlg.on_result(picked)
dlg.show()
dlg.off_result(funcid)
```

!!! note "Callback payload"
    The handler invokes `callback(event.data)` — passing the full
    payload dict, **not** the unwrapped date. Read `payload["result"]`
    inside the callback. (The class docstring claims the callback
    receives the bare `datetime.date`; in current source it receives
    the dict.)

`on_result` binds against `dlg._dialog.toplevel or self._master`. If
you call it **before** `show()` and the dialog has no `master=`
parent, there is no target to bind on and the call silently no-ops
(returns `None`). Pass `master=` in that case, or call `on_result`
after `show()` returns (which works as a one-shot post-mortem hook).

Cancel paths do **not** fire `<<DialogResult>>` — there is no
`{"confirmed": False}` event. Detect cancel by checking
`dlg.result is None` after `show()` returns, or by binding
`<Destroy>` on the toplevel for a popover-style flow.

---

## UX guidance

- **Anchor popovers to their trigger.** A `close_on_click_outside`
  popover with `hide_window_chrome=True` reads as a dropdown; pair
  it with `anchor_to=trigger_button, anchor_point="sw",
  window_point="nw"` so it appears flush below the button. A free-
  floating popover looks like a stray window.
- **Constrain when you know the answer is constrained.** If the
  date must be in the future, set `min_date=date.today()` rather
  than letting the user pick a past date and showing an error
  afterward. The calendar disables impossible cells in place.
- **Set `first_weekday` from the locale.** For European/ISO
  audiences pass `first_weekday=0` (Monday); for US audiences,
  `first_weekday=6` (the default). The Calendar widget can resolve
  this from Babel — but `DateDialog` always passes through the
  argument, so wire it from your locale settings if you want it
  automatic.
- **Don't use `DateDialog` for ranges.** It commits on the first
  click. For start/end pickers, embed `Calendar(selectmode="range")`
  in a custom `FormDialog` or `Dialog`.
- **Skip `hide_window_chrome` on macOS** when it matters — Tk auto-
  disables override-redirect there (Cocoa rejects it for grabbed
  toplevels), so the option only changes appearance on Windows /
  Linux. Don't build a UI that depends on the chrome being gone.

---

## When should I use DateDialog?

Use `DateDialog` when:

- the user picks a single date as a discrete action, with the
  calendar grid as the primary affordance (not a typed entry).
- you want a popover-style date picker anchored to a button or
  cell, distinct from a form field.
- the date is the only thing being collected — no other inputs
  belong in the same dialog.

Prefer a different control when:

- the date lives in a form alongside other fields → use
  [`DateEntry`](../inputs/dateentry.md), which combines typed input
  with a popup picker.
- the calendar is part of the page layout (always visible) → embed
  [`Calendar`](../selection/calendar.md) directly.
- you need a date **range** (start + end) → use
  `Calendar(selectmode="range")` inside a custom `Dialog`, since
  `DateDialog` commits on the first click.
- you want explicit OK / Cancel / Today buttons → build a
  [`Dialog`](dialog.md) around a `Calendar` rather than re-skinning
  `DateDialog`.

---

## Additional resources

**Related widgets**

- [`DateEntry`](../inputs/dateentry.md) — inline date field with a
  popup calendar; the right shape inside forms.
- [`Calendar`](../selection/calendar.md) — the inline calendar
  composite that powers `DateDialog`. Use it when the calendar is
  part of the page, not a modal.
- [`TimeEntry`](../inputs/timeentry.md) — time-of-day input.
- [`QueryBox.get_date`](querybox.md) — one-line facade that opens
  a `DateDialog` and returns its `.result`.
- [`Dialog`](dialog.md) — the generic builder; reach for it when
  you need confirm/cancel buttons or a custom footer.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)

**API reference**

- **API reference:** [`ttkbootstrap.DateDialog`](../../reference/dialogs/DateDialog.md)
- **Related guides:** Dialogs, Calendars, Localization
