---
title: RadioGroup
---

# RadioGroup

`RadioGroup` is a composite container that bundles a set of
[RadioButton](radiobutton.md) widgets, an optional group label, and a
shared selection signal into a single widget. The group **owns** the
shared variable — every radio added via `add()` is wired to it
automatically — and exposes a unified `get()` / `set()` / `value` /
`on_changed()` surface so callers don't have to walk individual
radios.

Use `RadioGroup` when the choice belongs together visually and
logically — sort orders, plan tiers, view modes — and when you'd
otherwise be wiring three or more `RadioButton` instances by hand
to the same `signal=`.

<figure markdown>
![radiogroup](../../assets/dark/widgets-radiogroup.png#only-dark)
![radiogroup](../../assets/light/widgets-radiogroup.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

group = ttk.RadioGroup(app, text="Choose a plan", orient="vertical", value="basic")
group.add("Basic", "basic")
group.add("Pro", "pro")
group.add("Enterprise", "enterprise")
group.pack(padx=20, pady=20, fill="x")

app.mainloop()
```

`add(text, value)` creates a child RadioButton and packs it into the
group's button container. The group's internal `StringVar` already
holds `'basic'` from `value=`, so the matching radio paints selected.

---

## Selection model

RadioGroup holds a single string-shaped value and pushes it through
the `RadioButton.variable` of every child it owns.

**Value type.** The group's underlying variable is a `StringVar`
(initial value `''` when no `signal=` / `variable=` / `value=` is
supplied). `get()`, `set(...)`, and the `value` property all read or
write this string. `set()` enforces the type — passing a non-string
raises `TypeError`. `set('')` is the documented "deselect" form.

**Where the variable comes from.** Three constructor paths, mutually
exclusive in priority order:

1. `signal=Signal(...)` — group adopts the signal; `group.signal is
   signal` and `group.variable is signal.var`. `value=` is ignored on
   this path (the signal's pre-existing value wins).
2. `variable=tk.StringVar(...)` — group adopts the variable and
   wraps it in `Signal.from_variable(...)`. `value=` is honored — it
   overwrites the variable's initial value.
3. Neither — group creates its own `StringVar` initialized to
   `value or ''` and a `Signal` over it.

Children added via `add()` always bind to whichever variable the
group ended up with.

**Membership and validation.** `add(text, value, key=...)` requires a
non-`None` `value`; `key` defaults to `value`. Duplicate keys raise
`ValueError`. `set(...)` validates that the requested value is the
key (= value, by default) of one of the child buttons; an unknown
value raises `ValueError`. The empty string is allowed and clears
the selection — no radio paints selected.

```python
g = ttk.RadioGroup(app)
g.add("Yes", "yes")
g.add("No", "no")
g.set("maybe")   # ValueError: Value 'maybe' not found in group...
g.set(123)       # TypeError: RadioGroup requires a string value...
g.set("")        # OK — clears selection
```

**Commit semantics.** Clicking any child radio writes its `value=`
into the shared variable immediately. Programmatic
`group.set(...)` writes through the same path, validated against
known keys.

---

## Common options

| Option | Type | Effect |
| --- | --- | --- |
| `text` | `str` | Group label rendered alongside the buttons. Position controlled by `labelanchor`. Omit to skip the label. |
| `value` | `str` | Initial selected value (must match a child's value/key once buttons are added). Ignored when `signal=` is provided. |
| `signal` | `Signal` | Shared reactive binding. `group.signal` is this signal; `group.variable` is its underlying var. |
| `variable` | `Variable` | Shared Tk variable (typically `StringVar`). Wrapped in `Signal.from_variable(...)` internally. |
| `orient` | `'horizontal'` (default) / `'vertical'` | Layout direction for the radios inside the button container. Reconfigure-safe — re-packs children. |
| `labelanchor` | `'n'` (default) / `'s'` / `'e'` / `'w'` plus combinations like `'nw'`, `'se'` | Placement of the group label relative to the buttons. Compound anchors are normalized to a primary direction (priority `n` > `s` > `w` > `e`). |
| `state` | `'normal'` (default) / `'disabled'` | Applied to every child radio at creation and on configure. |
| `accent` | str | **Forwarded default** for child radios. **See the warning below — currently broken at construction.** |
| `surface` | str | Background surface for the group's frame; usually inherited from parent. |
| `show_border` | bool | Draws a 1px border around the group's frame. |
| `padding` | int / tuple | Frame padding (default `1`). |
| `width` / `height` | int | Frame request size in pixels. |

`bootstyle` is accepted but **deprecated** — use `accent`. RadioGroup
has no variants — the only registered builder for the inner Frame
class (`TFrame`) is `default`, and the per-radio variant axis is
single-valued (see [RadioButton](radiobutton.md)).

`density` is **not** a valid option for RadioGroup or its children
(the radiobutton style builder reads only `accent` and `surface`).

!!! warning "Constructor `accent=` doesn't reach child radios"
    Passing `accent='success'` to the constructor sets the
    instance's `_accent` correctly inside `RadioGroup.__init__` —
    but `super().__init__()` (the Frame init path) then resets
    `self._accent` to `None` before the constructor returns. As a
    result, child radios added via `add()` are constructed with
    `accent=None` and paint with the default style. Confirmed at
    runtime: `RadioGroup(accent='success').add('A', 'a')` yields a
    child whose `style` is `Default.TRadiobutton`, not
    `bs[…].success.TRadiobutton`.

    **Workarounds:**

    - call `group.configure(accent='success')` *after* construction
      and *before* `add(...)` — that path goes through
      `_delegate_accent`, which writes `_accent` and forwards to
      existing children
    - or pass `accent='success'` per-call via `add('A', 'a',
      accent='success')` — the per-call kwarg flows through to the
      RadioButton constructor untouched

### Colors & Styling

Both workarounds in the warning above produce a properly styled
group. The post-construct `configure(accent=...)` form is the
shorter:

```python
g = ttk.RadioGroup(app, text="Plan", orient="vertical")
g.configure(accent="success")
g.add("Basic", "basic")
g.add("Pro", "pro")
g.add("Enterprise", "enterprise")
```

---

## Behavior

**Layout.** RadioGroup is a `Frame` containing two children: an
optional `Label` and an inner `Frame` (the *button container*). The
parent group lays them out via `grid`, with positions decided by
`labelanchor`. The button container internally uses `pack` —
`side='left'` for `orient='horizontal'`, `side='top', anchor='w'`
for `'vertical'`.

**Adding and removing radios.**

- `add(text, value, key=None, **kwargs)` — creates a `RadioButton`
  parented to the button container, wires it to the group's
  variable, applies the group's `state` and `accent` (modulo the bug
  above), and packs it. Any extra kwargs flow to `RadioButton`.
  Returns the created widget. Raises `ValueError` if `value` is
  `None` or if `key` collides.
- `remove(key)` — destroys and removes the named radio. Raises
  `KeyError` on miss.
- `item(key)` / `items()` — lookup helpers; `items()` returns a
  tuple of all child `RadioButton` instances in insertion order.
- `configure_item(key, **kwargs)` — passes kwargs to the named
  child's `configure(...)`; with a single `option=` arg, returns
  `cget(option)` instead.
- `keys()` — tuple of registered keys.

!!! warning "`values()` returns keys, not values"
    The implementation of `RadioGroup.values()` returns
    `tuple(self._buttons.keys())` — the **keys**, not each radio's
    `value=`. When `key` defaults to `value` (the common case),
    that's a tautology. But if you passed `key='foo', value='bar'`,
    `g.keys()` and `g.values()` both return `('foo',)` —
    `g.values()` does not surface `'bar'`. Walk
    `g.items()` and read each radio's `cget('value')` if you need
    the actual values.

**Reconfiguration.** Configure-delegates handle:

- `orient` — repacks every child radio in the new direction
- `accent` — writes through to every child via
  `button.configure(accent=...)` (the working path)
- `state` — propagates to every child
- `labelanchor` — re-grids the label and button container
- `text` — creates / updates / destroys the label as needed
- `value` — equivalent to `set(value)`; validates against the keys

`orient` accepts only `'horizontal'` or `'vertical'`; other values
raise `ValueError`. `state` accepts only `'normal'` or `'disabled'`.

**Keyboard contract.** RadioGroup adds no bindings of its own. The
arrow-key traversal (`<Up>` / `<Down>`) on radios sharing a variable
comes from ttk's stock `TRadiobutton` class binding
(`ttk::button::RadioTraverse`) — it works the same way on standalone
RadioButton siblings. Tab moves focus through children, Space
invokes the focused radio.

**Disabled state.** `state='disabled'` on the group greys every
child and blocks user clicks; the group's variable is still writable
from code via `set(...)`.

---

## Events

Two observation paths:

| Path | Fires when... | Receives |
| --- | --- | --- |
| `group.on_changed(fn)` | The group's variable changes — from any child's user click, from `group.set(...)`, or from a direct write to the underlying signal/variable. | The new value (string). |
| `group.signal.subscribe(fn)` | Identical to `on_changed` (it's a thin wrapper that returns the subscription handle). | The new value. |

`on_changed` returns a subscription handle suitable for
`off_changed(handle)`:

```python
import ttkbootstrap as ttk

app = ttk.App()
group = ttk.RadioGroup(app, text="Plan", orient="vertical", value="basic")
for label, val in [("Basic", "basic"), ("Pro", "pro"), ("Enterprise", "enterprise")]:
    group.add(label, val)
group.pack(padx=20, pady=20)

def on_change(value):
    print("plan now:", value)

sub = group.on_changed(on_change)
# Later: group.off_changed(sub)

app.mainloop()
```

RadioGroup itself emits **no virtual events**. Per-child `command=`
callbacks still work if you pass `command=...` through `add()` —
each child runs its own callback on user invocation in addition to
the group-level subscription firing.

---

## When should I use RadioGroup?

Use RadioGroup when:

- the choice is one-of-N over a fixed list (≤ ~7 items) and the
  group-level surface (single `get()` / `set()` / `on_changed`)
  matches how you want to handle state
- you want a labeled set with consistent layout (vertical stack or
  horizontal row) without hand-wiring every radio's `signal=`
- the group is the unit of disabling / theming / programmatic
  selection

Prefer:

- **[RadioButton](radiobutton.md)** — when you need custom per-row
  layout, mixed widgets in the same row, or finer control than a
  uniform pack/grid pattern
- **[ToggleGroup](togglegroup.md)** — when the choice is a view-mode
  or formatting strip and the buttons should look pressed/unpressed
- **[OptionMenu](optionmenu.md)** — for medium lists (~5–20) where
  vertical space is tight; a button + popup menu
- **[SelectBox](../inputs/selectbox.md)** — for longer lists or when search /
  filtering is needed
- **[CheckButton](checkbutton.md)** group — when **multiple**
  independent options are allowed (RadioGroup is *exactly one*)

---

## Related widgets

- **[RadioButton](radiobutton.md)** — the per-option primitive that
  RadioGroup composes
- **[RadioToggle](radiotoggle.md)** — toolbutton-styled mutually
  exclusive sibling
- **[ToggleGroup](togglegroup.md)** — group container for
  RadioToggle children
- **[CheckButton](checkbutton.md)** / **[Switch](switch.md)** —
  independent boolean siblings (multi-select)
- **[SelectBox](../inputs/selectbox.md)** / **[OptionMenu](optionmenu.md)** —
  dropdown selection alternatives

---

## Reference

- **API reference:** `ttkbootstrap.RadioGroup`
- **Related guides:** [Signals](../../capabilities/signals/signals.md),
  [Localization](../../capabilities/localization.md),
  [Design System](../../design-system/index.md)
