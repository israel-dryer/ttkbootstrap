---
title: OptionMenu
---

# OptionMenu

`OptionMenu` is a single-selection control rendered as a
[MenuButton](../actions/menubutton.md) with a chevron — clicking the
button (or pressing Return) opens a popup [ContextMenu](../actions/contextmenu.md)
containing the configured options as radiobutton items, all
sharing one `StringVar`. Selecting an item updates the displayed
text and fires `<<Change>>` with `event.data = {'value': value}`.

It is intentionally simpler than [SelectBox](../inputs/selectbox.md): no
search, no custom values, no inline filtering. Use OptionMenu for
short, well-known option sets where a compact button-plus-popup
beats showing every option inline as radio indicators.

<figure markdown>
![optionmenu](../../assets/dark/widgets-optionmenu.png#only-dark)
![optionmenu](../../assets/light/widgets-optionmenu.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

menu = ttk.OptionMenu(
    app,
    value="Medium",
    options=["Low", "Medium", "High"],
)
menu.pack(padx=20, pady=20)

app.mainloop()
```

The button shows the current value as its text. Clicking it opens
the menu; selecting an item commits the new value and closes the
popup.

---

## Selection model

OptionMenu stores its current value in a `StringVar` exposed as
`widget._textvariable` (and reachable through `widget.textsignal`,
the reactive wrapper). All paths — user click, `widget.set(...)`,
`configure(value=...)`, `widget.value = ...`, or a direct write to
the bound signal/variable — write through this single variable.

**Value type.** Always `str`. `set(...)` calls `str(value)` and
writes the result, so passing `set(123)` stores `'123'`. There is
no type discrimination, no auto-conversion back to the source type
on read — `widget.value` returns the string the variable holds.

**Options list.** `options=` accepts any iterable; each item is
rendered as a radiobutton menu entry. Items are coerced to strings
via `str(item)` for display. Reconfigure-safe — `configure(options=
[...])` rebuilds the underlying ContextMenu in place.

!!! warning "`set(...)` does not validate against `options=`"
    OptionMenu's `set(value)` writes the stringified value to the
    underlying variable unconditionally. There is no membership
    check against `options`. Verified at runtime: `m =
    OptionMenu(app, value='A', options=['A','B'])`,
    `m.set('not_in_list')` succeeds — `m.value == 'not_in_list'`,
    no menu radiobutton paints selected, and `<<Change>>` still
    fires with the orphan value. Either validate against `options`
    and raise on miss (matching RadioGroup's behavior), or document
    the permissive contract loudly. (Surfaced 2026-05-01.)

**Initial value.** Three constructor paths to determine the starting
value:

1. `value="Medium"` — the constructor creates an internal `StringVar`
   holding `"Medium"`.
2. `textvariable=tk.StringVar(value="Medium")` — your variable wins;
   `value=` (if also passed) overrides it via the variable's stored
   contents.
3. `textsignal=Signal("Medium")` — the signal's underlying variable
   is adopted; `value=` (if also passed) overrides it.

!!! note "`value=` takes precedence over signal/variable"
    When both `value=` and `textsignal=` (or `textvariable=`) are
    passed, the constructor's `value=` arg **wins** and is written
    into the bound variable, clobbering the signal's pre-existing
    value. To honor an existing signal, omit `value=`. Verified:
    `OptionMenu(value='A', options=[...], textsignal=Signal('B'))`
    yields `m.value == 'A'`, and the signal's value is now `'A'`
    too (the signal's underlying var was replaced).

**Commit semantics.** Any user click commits immediately; there is
no "open menu, dismiss without choosing" recovery — closing the
popup without picking just leaves the original value in place.

---

## Common options

| Option | Type | Effect |
| --- | --- | --- |
| `value` | `Any` (coerced to `str`) | Initial selected value. Passed as `text=` to the underlying MenuButton. |
| `options` | `list[Any]` | The available choices. Coerced to strings for display via `str(item)`. Reconfigure-safe. |
| `command` | `Callable[[str], None]` | Fires after selection commits. Receives the new value (string), **not** the event. **See the warning under Events — currently fires twice per change.** |
| `textsignal` | `Signal[str]` | Reactive binding. Subscribers fire on every change. |
| `textvariable` | `StringVar` | Tk variable to bind directly. Mutually substitutable with `textsignal=`. |
| `state` | `'normal'` / `'disabled'` / `'readonly'` | Disabled / readonly states block menu opening (`show_menu` checks `instate(("!disabled", "!readonly"))`). |
| `accent` | str | Theme token for the button chrome. |
| `variant` | `'solid'` (default) / `'outline'` / `'ghost'` / `'text'` | Visual weight on the underlying MenuButton. **No `link` or `pill` variants** — those exist on Button but not on Menubutton. |
| `surface` | str | Background surface; usually inherited. |
| `width` | int | Button width in characters. |
| `padding` | int / tuple | Extra padding around the content. |
| `compound` | str | Image-vs-text placement when both are set. |
| `icon` | str / dict | Theme-aware icon spec for the leading icon. |
| `icon_only` | bool | Drop text-reserved padding when no label is shown. |
| `show_dropdown_button` | bool | Toggle visibility of the chevron. |
| `dropdown_button_icon` | str / dict | Icon name for the chevron (default `'caret-down-fill'`). |
| `image` | `PhotoImage` | Custom image. *Won't auto-recolor on theme changes — prefer `icon=`.* |
| `underline` | int | Index of label character to underline. |
| `localize` | `bool` / `'auto'` | How `value` text is treated (literal vs translation key). Default `'auto'`. |
| `takefocus` | bool | Whether the widget participates in Tab traversal. |

`bootstyle` is accepted but **deprecated** — use `accent` and
`variant`.

OptionMenu has only the variant axis listed above (inherited from
MenuButton); there's no widget-specific variant. `density` is **not**
exposed at the OptionMenu level (the underlying MenuButton accepts
it, but OptionMenu doesn't capture it from kwargs — a future
enhancement).

### Colors & Styling

```python
ttk.OptionMenu(app, value="A", options=["A", "B"], accent="primary")
ttk.OptionMenu(app, value="A", options=["A", "B"], accent="primary", variant="outline")
ttk.OptionMenu(app, value="A", options=["A", "B"], accent="primary", variant="ghost")
ttk.OptionMenu(app, value="A", options=["A", "B"], variant="text")
```

`accent` colors the button chrome (fill for `solid`/`text`, ring for
`outline`, hover tint for `ghost`). The popup menu inherits density
from the button via `configure_style_options('density')` and
positions itself at the button's southwest corner with a small
offset to align with the visible button border.

See [Design System – Variants](../../design-system/variants.md).

---

## Behavior

**User input.** Left-click, `<Return>`, and `<KP_Enter>` open the
popup menu (`show_menu()`). Selecting any item commits its value via
the shared variable; the menu auto-dismisses. Clicking elsewhere
without picking dismisses the popup without committing.

**Disabled and readonly.** `state='disabled'` and `state='readonly'`
both block menu opening (`show_menu` returns silently). The
underlying variable is still writable from code, so
`menu.set('value')` works in any state.

**Reconfiguration.** Configure delegates handle:

- `value` — equivalent to `widget.set(...)`
- `options` — destroys and rebuilds the popup menu
- `textsignal` — rewrites the variable binding (re-subscribes the
  change-event emitter)
- `show_dropdown_button` — toggles chevron visibility (rebuilds
  style)
- `dropdown_button_icon` — changes chevron icon (rebuilds style)

`command=` and `state` flow through the parent MenuButton
configure paths.

**Popup positioning.** The popup attaches to the button's south-west
corner (`anchor='nw', attach='sw'`) with a small horizontal offset
(`scale_from_source(10)`) so the menu's left edge lines up with the
button's visible border. `show_menu()` also bumps the menu's
`minwidth` to match the button width — the dropdown never renders
narrower than its trigger.

**Keyboard contract.** Tab moves focus to the button. Return /
KP_Enter open the menu. Once the menu is open, arrow keys navigate
items, Return commits, Escape dismisses without committing — those
bindings live on the underlying ContextMenu / Tk Menu.

---

## Events

Two observation paths:

| Path | Fires when... | Receives |
| --- | --- | --- |
| `widget.on_changed(callback)` | Underlying variable changes — user click, `set()`, `configure(value=...)`, signal write, `textvariable.set(...)`. | Tk event with `event.data = {'value': value}`. |
| `widget.textsignal.subscribe(fn)` | Same trigger as above (it's the same subscription chain `on_changed` rides). | The new value (string). |

`on_changed(callback)` returns a bind id suitable for
`off_changed(bind_id)`.

```python
def on_changed(event):
    print("Selected:", event.data["value"])

bind_id = menu.on_changed(on_changed)
# Later: menu.off_changed(bind_id)
```

A `command=` callback (passed at construction) is wired to
`<<Change>>` internally and receives the **value**, not the event:
`command=lambda v: print(v)`.

!!! warning "`<<Change>>` fires twice per write"
    The OptionMenu constructor calls `_bind_change_event()` twice
    during `__init__` — once indirectly via `self.configure(
    textvariable=self._textvariable)` (which routes through
    `_delegate_textsignal`) and once explicitly at the end of
    `__init__`. Each call subscribes a fresh `<<Change>>`-emitting
    lambda to `textsignal` without unsubscribing the previous one
    (the `if self._bind_id is not None` guard runs against
    `self._bind_id`, but only the second call assigns to it). Net
    effect: every variable write fires `<<Change>>` **twice**, and
    any `command=` callback runs **twice** per change. Verified at
    runtime: `len(m.textsignal._subscribers) == 2` immediately
    after construction. `on_changed` listeners and `command=`
    callbacks must be idempotent until this is fixed. (Surfaced
    2026-05-01.)

---

## When should I use OptionMenu?

Use OptionMenu when:

- the option list is short to medium (~3–15 items) and well-known
  to users (license tiers, sort orders, time zones)
- the control should remain compact (a button, not an inline list
  of radios)
- search and rich rendering aren't needed

Prefer:

- **[SelectBox](../inputs/selectbox.md)** — for longer lists, when search /
  filtering is needed, or when users may need to type a custom
  value
- **[RadioButton](radiobutton.md)** / **[RadioGroup](radiogroup.md)**
  — when there are very few options (≤ ~5) and showing them inline
  improves discoverability
- **[ToggleGroup](togglegroup.md)** — when a segmented button strip
  is a better fit than a popup menu (view modes, formatting
  selectors)
- **[MenuButton](../actions/menubutton.md)** + a custom
  [ContextMenu](../actions/contextmenu.md) — when items need
  individual commands, separators, submenus, or a heterogeneous mix
  rather than a uniform option list

---

## Related widgets

- **[MenuButton](../actions/menubutton.md)** — base widget OptionMenu
  extends; use for menus that aren't single-selection lists
- **[ContextMenu](../actions/contextmenu.md)** — the underlying menu
  primitive that drives the popup
- **[SelectBox](../inputs/selectbox.md)** — combobox-style alternative with
  search and custom values
- **[RadioGroup](radiogroup.md)** — inline radio alternative for
  small lists
- **[ToggleGroup](togglegroup.md)** — segmented strip alternative

---

## Reference

- **API reference:** `ttkbootstrap.OptionMenu`
- **Related guides:** [Signals](../../capabilities/signals/signals.md),
  [Localization](../../capabilities/localization.md),
  [Design System](../../design-system/index.md)
