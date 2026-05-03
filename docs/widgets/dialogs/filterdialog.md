---
title: FilterDialog
---

# FilterDialog

`FilterDialog` is a modal **multi-select picker** built on top of
[`Dialog`](dialog.md). It displays a list of items as checkboxes —
optionally with a top search box and a Select All toggle — and returns
the values of the checked items as a list when the user clicks OK.

It's the right shape for filter UIs where the option set is too dense
to expose inline (a dozen status tags, two dozen categories) and where
an explicit Apply/Cancel commit is preferable to live filtering. The
`frameless=True` variant gives you a borderless dialog with outside-
click dismissal — useful for the "open this from a filter button"
pattern, anchored to the trigger.

Unlike most dialogs in the framework, `FilterDialog` is itself a
`Frame` subclass that *composes* a `Dialog` on `show()` rather than
extending it — that has implications for the events surface and where
you bind handlers. See [Events](#events).

---

## Basic usage

Construct, `show()`, read the list of selected values:

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.FilterDialog(
    master=app,
    title="Filter by status",
    items=[
        {"text": "New", "value": "new"},
        {"text": "In progress", "value": "in_progress", "selected": True},
        {"text": "Done", "value": "done"},
    ],
    enable_search=True,
    enable_select_all=True,
)
dlg.show()

if dlg.result is not None:
    print("active filters:", dlg.result)   # list[Any]; may be []

app.mainloop()
```

`show()` blocks until the user clicks **OK** or dismisses the dialog
(Cancel, Escape, window-close, or — in `frameless=True` mode — an
outside click). The dialog's `.result` is set before `show()` returns;
`show()` itself also returns that same value, so `selected = dlg.show()`
is equivalent to reading `dlg.result` afterwards.

---

## Result value

`.result` is a list of the `value` field for every checked item when
the user clicked **OK**, or `None` on every cancel path:

```python
dlg.result  # list[Any], or None
```

A few non-obvious points:

- **Empty list (`[]`) is a valid OK outcome** — distinct from `None`.
  An empty list means the user clicked OK with nothing checked
  (intentionally clearing filters). Branch on `result is not None`,
  not on truthiness.
- The list contains the items' `value` field (not the display `text`).
  String items (`items=["A", "B"]`) use `text` as `value`, so the two
  fields coincide.
- Order in the result reflects **the order the user clicked the
  checkboxes**, not the order of the items in the source list. If
  you need stable ordering, sort the result yourself.
- `.result` is set by the OK button's command callback before the
  dialog destroys. Cancel paths leave it untouched.

!!! warning "Stale result on re-`show()`"

    `FilterDialog.show()` does **not** reset `.result` to `None` at
    the start of each call (only the underlying `Dialog`'s own
    `result` is reset). If you call `show()` once, the user clicks
    OK, then you call `show()` again and the user cancels, the
    second call returns the **previous** OK result rather than
    `None`. Always set `dlg.result = None` before re-showing, or
    construct a fresh `FilterDialog` per opening.

---

## Common options

| Option | Purpose |
|---|---|
| `master` | Parent widget. `FilterDialog` is itself a `Frame` and is initialized as a child of this master; the underlying `Dialog` is also transient against it. Defaults to the application root. |
| `title` | Window title. Default `"Filter"` — a literal string, **not** a translation key (unlike most dialogs). Pass an explicit translated string if you ship localized builds. |
| `items` | List of items to display as checkboxes. Each item is either a **string** (used as both display text and value) or a **dict** with `text` (required), `value` (defaults to `text`), and `selected` (defaults to `False`). |
| `enable_search` | If `True`, adds a search `TextEntry` with a leading magnifying-glass icon at the top of the dialog. The search is a case-insensitive substring match against each item's `text`. Default `False`. |
| `enable_select_all` | If `True`, adds a "Select All" checkbox above the item list. Default `False`. The checkbox label is resolved through `MessageCatalog.translate("edit.select_all")`. |
| `frameless` | If `True`, the dialog is rendered without window decorations and dismisses when the user clicks outside it. Default `False`. |

Item shape:

```python
items = [
    "Plain string",                               # text and value both = "Plain string"
    {"text": "With value", "value": 42},          # value can be any hashable
    {"text": "Pre-checked", "selected": True},    # starts checked
]
```

!!! note "Localization"
    Default button labels (`"button.ok"` / `"button.cancel"`) and the
    Select All checkbox label (`"edit.select_all"`) are resolved
    through `MessageCatalog.translate` so they render in the active
    locale. Item `text` is shown verbatim — translate it yourself
    before passing. The default `title="Filter"` is an English
    literal; pass an explicit translated string if you ship localized
    builds.

---

## Behavior

### Modality and window sizing

`FilterDialog` is **modal-only**. The underlying `Dialog` is
constructed with `mode="modal"` hard-coded; the modality grabs focus
on the parent application until the dialog closes.

The window has fixed-width sizing constraints: `minsize=(250, 200)`,
`maxsize=(250, 380)`, `resizable=(False, True)`. Width is locked at
250 pixels; height resizes vertically between 200 and 380 to
accommodate longer item lists. The list itself sits in a 230-pixel
scrollable container — items past that height scroll.

`show()` accepts the standard `Dialog.show()` positioning kwargs
(`position=`, `anchor_to=`, `anchor_point=`, `window_point=`,
`offset=`, `auto_flip=`). The default is to center on the parent.

### Default and cancel bindings

Both buttons are wired correctly for keyboard accelerators:

- **OK** has `default=True` and `role="primary"` — pressing **Enter**
  invokes it. The OK callback stashes the selected values into
  `self.result` and emits `<<SelectionChange>>`.
- **Cancel** has `role="cancel"` — pressing **Escape** invokes it
  cleanly, and `.result` stays `None`.

The window-close (`X`) button destroys the toplevel without invoking
the Cancel command, but `.result` still ends up `None` because the
underlying `Dialog.show()` resets its own `result` to `None` at start
and the `_on_ok` callback never ran.

### Search filtering

When `enable_search=True`, every keystroke in the search box re-runs
`text.lower() in item['text'].lower()` against each item and
shows/hides the corresponding checkbox via `pack_forget()`. The
filter is purely visual — checked items that scroll off due to a
filter remain checked and remain in the result if the user clicks OK.

The search field uses `on_input` (live, per-keystroke), not
`on_changed` — there is no debouncing.

### Select All

The Select All toggle iterates **all** checkbox items, not just the
ones currently visible under a search filter. If the user types a
search term and then clicks Select All, every item in the underlying
list — including ones not currently visible — is selected.

The Select All checkbox does **not** auto-update its own state in
response to individual checkbox toggles. If the user manually checks
all items one-by-one, the Select All box stays in whatever state the
user last left it. This is a known UX quirk.

### Frameless mode and outside-click dismiss

`frameless=True` does two things:

1. The toplevel is rendered without window decorations
   (override-redirect on most platforms).
2. A `<Button-1>` binding is installed on the root window that
   destroys the dialog when the click lands outside its bounds.
   `.result` stays `None` (the dismiss bypasses the OK path).

Frameless mode is the framework's "popover" shape for FilterDialog —
combine it with `anchor_to=trigger_button` to get a filter panel
that opens beneath a toolbar button:

```python
dlg = ttk.FilterDialog(
    master=app, items=[...], frameless=True,
    enable_search=True, enable_select_all=True,
)
dlg.show(anchor_to=filter_button, anchor_point="sw", window_point="nw")
```

The outside-click dismissal is global — clicks anywhere outside the
dialog dismiss it, including clicks on other widgets in the
application. Don't rely on it for partial-overlay scenarios.

### Items with duplicate text

The internal checkbox registry is keyed by item `text`, not `value`.
If two items share the same `text`, the second silently overwrites
the first in the registry — the second checkbox renders, but Select
All and search will only act on the second one's binding. Make `text`
fields unique within an item list; if the user-facing label must be
duplicated, distinguish them in `value` and consider rendering them
through a different selection control.

---

## Events

`FilterDialog` exposes a single virtual event,
`<<SelectionChange>>`, that fires when the user clicks **OK**:

```python
def handle(event):
    print(event.data["selected"])    # list[Any] of selected values

dlg = ttk.FilterDialog(master=app, items=[...])
dlg.on_selection_changed(handle)
dlg.show()
```

Differences from the rest of the dialogs sweep:

- The event name is **`<<SelectionChange>>`**, not the
  `<<DialogResult>>` used by `MessageDialog`, `QueryDialog`,
  `DateDialog`, and `ColorChooserDialog`.
- The payload key is **`"selected"`**, not `"result"`. The shape is
  `{"selected": list[Any]}` — there is no `confirmed` flag (the
  event only fires on commit, so it's implicit).
- The event is generated on **the `FilterDialog` frame instance**
  (`self.event_generate(...)`), not on the dialog's toplevel. Bind
  via the `on_selection_changed` helper rather than reaching into
  `dlg._dialog.toplevel`.
- There is **no** `on_dialog_result` helper, and the dialog does
  **not** fire `<<DialogResult>>` — the underlying `Dialog` sets its
  own `result` (which is the OK button's `result=True` sentinel, not
  the selected list), but that's an internal value and isn't surfaced.
- The event **only fires on OK**. Cancel, Escape, window-close, and
  outside-click (frameless) all leave `.result` as `None` and emit
  no event.

`on_selection_changed(callback)` returns a binding identifier. Use
`off_selection_changed(bind_id)` to unbind a single subscriber, or
call it with no argument to clear all `<<SelectionChange>>` bindings:

```python
bid = dlg.on_selection_changed(handle)
# ...
dlg.off_selection_changed(bid)
```

Because the event is on the FilterDialog frame (not the dialog's
toplevel), subscriptions registered before `show()` survive across
multiple `show()` calls — unlike `DateDialog` / `QueryDialog` /
`ColorChooserDialog`, where pre-`show()` registration silently
no-ops if no `master` is set.

---

## UX guidance

- **Pre-select sensible defaults** via `selected: True` per item,
  rather than expecting the user to start from an empty selection.
  Common patterns: pre-select the user's last-saved filter, or
  pre-select all items with `enable_select_all=True` for an
  exclusive-filter UI.
- **Use `frameless=True` with `anchor_to=`** to open the filter
  off a toolbar button. The borderless look + outside-click dismiss
  matches the popover-filter UX users expect from web apps. For a
  full modal dialog look, leave `frameless=False`.
- **Pair `enable_search=True` with longer lists** (>10 items).
  For shorter lists the search box is wasted space; render the
  checkboxes directly (or use inline
  [`CheckButton`](../selection/checkbutton.md)) instead.
- **Don't mix Select All with a search filter as the primary UX.**
  Because Select All ignores the search filter, users who search
  "active" and click Select All will get a surprising amount of
  collateral selection. Consider hiding Select All when search is
  active, or replacing this dialog with a custom multi-step UI for
  large lists.
- **Don't reach for `FilterDialog` for single-select.** The widget
  is exclusively multi-select; a single-select picker is better
  served by [`Combobox`](../primitives/combobox.md) or
  [`SelectBox`](../inputs/selectbox.md).

---

## When should I use FilterDialog?

Use `FilterDialog` when:

- the user picks **multiple** values from a list of >5 options, and
  inline checkboxes would crowd the UI.
- explicit **Apply/Cancel commit** is desirable — the user reviews
  their changes and confirms in one step rather than the result
  changing as they click.
- you want a **searchable** option list without writing the search
  plumbing yourself.
- you want a **popover-style filter panel** off a toolbar trigger
  (combine with `frameless=True` and `anchor_to=`).

Prefer a different control when:

- the option set is **small (≤5 items)** → render
  [`CheckButton`](../selection/checkbutton.md) widgets inline.
- the user picks **exactly one value** → use
  [`Combobox`](../primitives/combobox.md), 
  [`SelectBox`](../inputs/selectbox.md), or
  [`QueryDialog`](querydialog.md) with `items=`.
- you need **live filtering as the user toggles** (no Apply
  button) → render checkboxes inline and react to each
  `<<Changed>>`.
- you need **structured multi-field input** (filters across
  several axes) → use [`FormDialog`](formdialog.md).
- you need a fully **custom layout** (grouped sections, mixed
  controls) → drop down to [`Dialog`](dialog.md) with a
  `content_builder` and lay out the primitives directly.

---

## Additional resources

**Related widgets**

- [`Dialog`](dialog.md) — the generic builder underneath; reach
  for it directly for custom multi-section pickers.
- [`FormDialog`](formdialog.md) — multi-field structured input,
  for filters that span several typed axes rather than a single
  multi-select.
- [`QueryDialog`](querydialog.md) — single-value picker; supports
  filterable `Combobox` mode via `items=`.
- [`SelectBox`](../inputs/selectbox.md) — inline single-select
  control.
- [`CheckButton`](../selection/checkbutton.md) — inline filter
  primitive for short option sets.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)

**API reference**

- **API reference:** [`ttkbootstrap.FilterDialog`](../../reference/dialogs/FilterDialog.md)
- **Related guides:** Dialogs, UX Patterns, Localization
