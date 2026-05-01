---
title: ToggleGroup
---

# ToggleGroup

`ToggleGroup` is a composite container that bundles a strip of
toolbutton-styled toggles into a single segmented control. Unlike
[RadioGroup](radiogroup.md) (which always produces single-selection
radios), ToggleGroup picks its child class based on `mode=`:
`'single'` builds [RadioToggle](radiotoggle.md) children sharing a
`StringVar` (one selection at a time); `'multi'` builds
[CheckToggle](checktoggle.md) children sharing a `SetVar` (any
subset selected). Either way, the children render as a connected
button strip with rounded outer corners — the position-aware
styling treats the buttons as one segmented unit.

Use ToggleGroup for view-mode pickers (Grid / List / Card),
formatting strips (Bold / Italic / Underline), filter chips, or
toolbar segments — anywhere the choices belong together visually.

<figure markdown>
![togglegroup](../../assets/dark/widgets-togglegroup.png#only-dark)
![togglegroup](../../assets/light/widgets-togglegroup.png#only-light)
</figure>

---

## Basic usage

Single-selection (the default mode):

```python
import ttkbootstrap as ttk

app = ttk.App()

group = ttk.ToggleGroup(app, mode="single", value="grid")
group.add("Grid", value="grid")
group.add("List", value="list")
group.add("Cards", value="cards")
group.pack(padx=20, pady=20)

app.mainloop()
```

Multi-selection:

```python
group = ttk.ToggleGroup(app, mode="multi", value={"bold"})
group.add("Bold", value="bold")
group.add("Italic", value="italic")
group.add("Underline", value="underline")
group.pack(padx=20, pady=20)
```

---

## Selection model

ToggleGroup's value type depends on `mode=`:

| Mode | Value type | Default variable | Children |
| --- | --- | --- | --- |
| `'single'` (default) | `str` | `StringVar` (`""`) | `RadioToggle` |
| `'multi'` | `set[str]` | `SetVar` (`set()`) | `CheckToggle` |

`get()` returns the current value (string or set). `set(...)`
enforces the type — single mode requires `str`, multi mode requires
`set` — and writes through to the underlying variable. The `value`
property mirrors `get()` / `set()`.

**Where the variable comes from.** Three constructor paths, in
priority order:

1. `signal=Signal(...)` — group adopts the signal; `group.signal is
   signal`. `value=` is ignored on this path (the signal's
   pre-existing value wins).
2. `variable=tk.StringVar(...)` (single) or `SetVar(...)` (multi) —
   group adopts the variable, wraps it in `Signal.from_variable(...)`,
   and applies `value=` if provided.
3. Neither — group creates an internal variable matching the mode,
   initialized to `value or ''` (single) or `value or set()` (multi).

**Membership and validation.** `add(text, value, key=...)` requires
a non-`None` `value`; `key` defaults to `value`; duplicate keys
raise `ValueError`.

!!! warning "`set(...)` does NOT validate against known keys"
    ToggleGroup's `set(value)` enforces only the type (str for
    single, set for multi); it does not check that `value` matches
    a registered key. Verified at runtime:
    `g = ttk.ToggleGroup(app); g.add('A', 'a'); g.set('unknown')`
    succeeds — `g.value == 'unknown'` afterwards, and no child
    paints selected because no matching toggle exists. This is
    inconsistent with [RadioGroup](radiogroup.md), where
    `set('unknown')` raises `ValueError`. Either validate against
    `keys()` to match RadioGroup's behavior, or document the
    permissive contract loudly. (Surfaced 2026-05-01.)

**Multi-mode click semantics.** In multi mode, `_on_multi_toggle`
runs on every child click — it reads the current `set`, toggles
inclusion of the clicked toggle's `value`, and writes the new set
back. Each `CheckToggle`'s own variable is also flipped to match.

```python
g = ttk.ToggleGroup(app, mode="multi")
g.add("A", "a"); g.add("B", "b"); g.add("C", "c")
g.item("a").invoke()  # value = {'a'}
g.item("b").invoke()  # value = {'a', 'b'}
g.item("a").invoke()  # value = {'b'}  (re-clicking removes)
```

**Commit semantics.** Single-mode clicks write through immediately
via the shared variable. Multi-mode clicks go through the
`_on_multi_toggle` shim, which then writes the updated set. Both
fire `<<Change>>` on the underlying signal.

---

## Common options

| Option | Type | Effect |
| --- | --- | --- |
| `mode` | `'single'` (default) / `'multi'` | Selects child class (RadioToggle vs CheckToggle) and variable type (`StringVar` vs `SetVar`). **Construction-only** — there's no configure delegate that swaps mode at runtime. |
| `value` | `str` (single) / `set[str]` (multi) | Initial selected value. Ignored when `signal=` is provided. |
| `signal` | `Signal` | Shared reactive binding. `group.signal` is this signal. |
| `variable` | `Variable` | Shared Tk variable (`StringVar` for single, `SetVar` for multi). Wrapped in `Signal.from_variable(...)` internally. |
| `orient` | `'horizontal'` (default) / `'vertical'` | Layout direction for the strip. Reconfigure-safe — re-packs and re-styles children. |
| `accent` | str | **Forwarded to all child toggles** at creation and on configure (default `'primary'`). |
| `variant` | `None` (default — solid) / `'outline'` / `'ghost'` | Visual weight applied to every child. `None` is the only registered "default" name on `ButtonGroup`; `'solid'` works as an alias too. **No `pill` or `link`/`text` variants** — those exist on Button but not on ButtonGroup. |
| `surface` | str | Background surface for the group's frame; usually inherited from parent. |
| `show_border` | bool | Draws a 1px border around the group's frame. |
| `padding` | int / tuple | Frame padding (default `1`). |
| `width` / `height` | int | Frame request size in pixels. |

`bootstyle` is accepted but **deprecated** — use `accent` and
`variant`.

ToggleGroup has **no group-label option** — unlike RadioGroup, it
doesn't expose `text=` / `labelanchor=`. Passing `text=...` raises
`TclError: unknown option "-text"`. If you need a label, place a
[Label](../data-display/label.md) next to the group manually.

It also has **no `state=` configure option** — disable individual
children via `configure_item(key, state='disabled')`.

`density` is not exposed at the group level, but per-toggle
`density='compact'` works through `add(...)` (it propagates to the
toolbutton style builder via `style_options`).

### Colors & Styling

```python
ttk.ToggleGroup(app, accent="primary")    # default
ttk.ToggleGroup(app, accent="success")
ttk.ToggleGroup(app, accent="danger", variant="outline")
ttk.ToggleGroup(app, accent="primary", variant="ghost")
```

Per-button accent overrides also work — pass `accent='...'` to
`add()`:

```python
g = ttk.ToggleGroup(app, accent="primary")
g.add("OK", "ok")
g.add("Delete", "delete", accent="danger")  # this one only
```

Unlike RadioGroup, ToggleGroup's constructor **correctly forwards**
`accent` to children. The implementation explicitly restores
`self._accent` after `super().__init__()` (`composites/togglegroup.py:
96-98`) — RadioGroup doesn't have that fix today.

---

## Behavior

**Layout.** ToggleGroup is a `Frame` containing the toggles directly
(no inner button container; there's no group label to lay out
around). `orient='horizontal'` packs children with `side='left'`;
`orient='vertical'` packs with `side='top', fill='x'`.

**Position-aware styling.** Children get `ttk_class='ButtonGroup'`
and a position style option (`before` for the first, `center` for
middle children, `after` for the last). The result is rounded outer
corners on the strip and square inner edges between buttons. Each
`add(...)` and `remove(...)` call invokes
`_update_button_positions()` to recompute and rebuild the styles
for every existing child, so the strip stays correctly segmented as
the group grows or shrinks.

**Adding and removing toggles.**

- `add(text, value, key=None, **kwargs)` — creates a child
  (RadioToggle or CheckToggle depending on `mode`) wired to the
  group's variable, applies the group's `accent` / `variant`, packs
  it according to `orient`, and updates segment positions. Per-call
  `accent=` / `variant=` overrides are honored. Returns the created
  widget.
- `remove(key)` — destroys the named toggle and re-segments the
  remaining children. Silent on miss (unlike RadioGroup, which
  raises `KeyError`).
- `item(key)` / `items()` / `keys()` — lookup helpers.
- `configure_item(key, **kwargs)` — passes kwargs to a single
  child's `configure(...)`; `option=` form returns `cget(option)`.
- ToggleGroup does NOT define a `values()` method (RadioGroup does,
  though that one returns keys not values — see RadioGroup's bug
  list).

**Reconfiguration.** Configure delegates handle `accent`, `orient`,
and `value`. `mode=` is captured at construction and **not
reconfigurable** — there's no `_delegate_mode` and the variable type
is fixed once chosen.

**Keyboard contract.** Same as RadioToggle / CheckToggle — Tab moves
focus between children, Space invokes the focused toggle. In single
mode (`RadioToggle` children), `<Up>` / `<Down>` traverse via the
stock `TRadiobutton` class binding (`RadioTraverse`). In multi mode
(`CheckToggle` children), arrow keys are NOT bound at the class
level (CheckToggle's bindtag is `Toolbutton`, not `TCheckbutton`).

**Disabled state.** ToggleGroup itself has no `state=` configure
option; disable individual toggles with
`group.configure_item(key, state='disabled')` (or pass
`state='disabled'` to `add(...)`).

---

## Events

Two observation paths:

| Path | Fires when... | Receives |
| --- | --- | --- |
| `group.on_changed(fn)` | The shared variable changes — from any child's user click, from `group.set(...)`, or from a direct write to the underlying signal/variable. | The new value (string in single mode; **a `set` instance** in multi mode). |
| `group.signal.subscribe(fn)` | Identical to `on_changed` (it's a thin wrapper that returns the subscription handle). | The new value. |

```python
import ttkbootstrap as ttk

app = ttk.App()
group = ttk.ToggleGroup(app, mode="multi")
for label, val in [("Bold", "bold"), ("Italic", "italic"), ("Underline", "underline")]:
    group.add(label, value=val)
group.pack(padx=20, pady=20)

def on_change(value):
    print("formatting:", value)  # value is a set[str] in multi mode

sub = group.on_changed(on_change)
# Later: group.off_changed(sub)

app.mainloop()
```

ToggleGroup itself emits **no virtual events**. Per-child `command=`
callbacks still work if you pass `command=...` through `add()` — in
multi mode, the user-supplied command runs *after* the SetVar
update via `_on_multi_toggle`.

---

## When should I use ToggleGroup?

Use ToggleGroup when:

- the choice is a view mode, sort order, formatting axis, or
  filter strip and the controls should read as one segmented unit
- single OR multi-selection both fit (the same widget supports
  either via `mode=`)
- buttons should look pressed/unpressed instead of using check or
  radio indicators

Prefer:

- **[RadioGroup](radiogroup.md)** — when the choice belongs in a
  form or settings panel and a circular radio indicator is the right
  affordance, or when you need a group label
- **[ButtonGroup](../actions/buttongroup.md)** — when the children
  are one-shot actions (Save / Cancel / Apply), not persistent
  toggles
- **[RadioToggle](radiotoggle.md)** / **[CheckToggle](checktoggle.md)**
  — when you want a single toolbutton-styled toggle, or when you
  need free-form (non-segmented) layout
- **[OptionMenu](optionmenu.md)** / **[SelectBox](selectbox.md)** —
  for medium-to-long lists where a strip would overflow

---

## Related widgets

- **[RadioToggle](radiotoggle.md)** — the per-option primitive used
  by single-mode ToggleGroup
- **[CheckToggle](checktoggle.md)** — the per-option primitive used
  by multi-mode ToggleGroup
- **[RadioGroup](radiogroup.md)** — group container with classic
  radio indicators and an optional group label
- **[ButtonGroup](../actions/buttongroup.md)** — segmented action
  buttons (no persistent selection)

---

## Reference

- **API reference:** `ttkbootstrap.ToggleGroup`
- **Related guides:** [Signals](../../capabilities/signals/signals.md),
  [Localization](../../capabilities/localization.md),
  [Design System](../../design-system/index.md)
