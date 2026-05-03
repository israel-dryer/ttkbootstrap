---
title: RadioToggle
---

# RadioToggle

`RadioToggle` is a [RadioButton](radiobutton.md) subclass restyled as
a pressed/unpressed button — mutually-exclusive selection drawn as
toolbutton chrome. Like RadioButton, multiple RadioToggles sharing a
`signal=` or `variable=` form a group; clicking one writes its
`value=` to the shared variable and the matching toggle paints
pressed.

The visual is the same toolbutton chrome that backs
[CheckToggle](checktoggle.md), so the two are interchangeable
visually — what differs is the value model. CheckToggle is
independent boolean; RadioToggle is one-of-many. Use RadioToggle for
view-mode strips, formatting alignment (Left / Center / Right /
Justify), or any toolbar pick where exactly one option is active at
a time.

<figure markdown>
![radiotoggle](../../assets/dark/widgets-radiotoggle.png#only-dark)
![radiotoggle](../../assets/light/widgets-radiotoggle.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

view = ttk.Signal("grid")

ttk.RadioToggle(app, text="Grid", signal=view, value="grid").pack(side="left", padx=4, pady=10)
ttk.RadioToggle(app, text="List", signal=view, value="list").pack(side="left", padx=4, pady=10)

app.mainloop()
```

The toggle whose `value=` matches the signal's current value paints
pressed. Clicking the other toggle writes its value to `view`, and
the visual selection follows.

---

## Selection model

RadioToggle holds **no value of its own** — selection is decided by
matching `value=` against the shared variable. The Tk variable lives
on the widget as `widget.variable`; when `signal=` is used, a
reactive `widget.signal` mirrors it. Sibling toggles sharing the
same `signal=` or `variable=` reuse the same underlying object.

**Value type.** Inherits from RadioButton: the default variable is
an **`IntVar`** (initial `0`). Pass non-int `value=` strings to
coerce the variable to a string representation. To pin a known
type, supply your own `tk.StringVar` / `tk.IntVar` via `variable=`
(or a typed `Signal`) and pass it to every toggle in the group.

**Mutually exclusive, by sharing a variable.** Same as RadioButton —
"group" is emergent from sharing `signal=` / `variable=`. Forgetting
to share makes each toggle an independent group of one. For a group
container that owns the shared variable, see
[ToggleGroup](togglegroup.md).

**No tri-state.** The toolbutton style builder maps `selected` /
`pressed` / `focus` / `disabled` / `hover` — but not `alternate`. As
with RadioButton, an indeterminate state would be meaningless for
mutually-exclusive choice.

**`widget.value` reads the shared selection.** Like RadioButton, the
property returns the *current selection*, not the toggle's own
constructor `value=` argument. The constructor `value=` lives at
`widget.cget('value')` — the constant the toggle writes when clicked.

**Commit semantics.** Clicking writes the constructor `value=` into
the shared variable immediately; programmatic `widget.set(...)`
writes through the same path.

---

## Common options

| Option | Type | Effect |
| --- | --- | --- |
| `text` | `str` | Label shown inside the toggle. Localized through `MessageCatalog` when `localize` permits. |
| `value` | `Any` | The constant this toggle writes into the shared variable when clicked. Required for meaningful group behavior. |
| `signal` | `Signal` | Shared reactive binding across the group. Subscribers fire on every change. |
| `variable` | `Variable` | Shared Tk variable to bind directly. Mutually substitutable with `signal=`. |
| `command` | `Callable[[], None]` | Fires on **user invocation only** (click or `.invoke()`). Programmatic `set()` and variable writes do **not** fire it. |
| `state` | `'normal'` / `'disabled'` / `'readonly'` | Disables click input but keeps the variable mutable from code. |
| `accent` | str | Theme token for the pressed / focused fill (default `'primary'`; `'secondary'` for `ghost`). |
| `variant` | `'default'` / `'solid'` / `'outline'` / `'ghost'` | Visual weight (see *Variants* below). `'default'` is an alias of `'solid'`. **No `link` or `text` variants** — those exist on Button but not on Toolbutton. |
| `density` | `'default'` / `'compact'` | Reduces vertical padding and font size. |
| `surface` | str | Background surface; usually inherited from the parent. |
| `width` | int | Label width in characters; widget pads to that width. |
| `padding` | int / tuple | Extra space around the content. |
| `anchor` | str | Content alignment (`'w'`, `'e'`, `'center'`, ...). |
| `compound` | str | Image-vs-text placement when both are set. |
| `icon` | str / dict | Theme-aware icon spec. |
| `icon_only` | bool | Drop the text-reserved padding when no label is shown — typical for icon-only toolbars. |
| `image` | `PhotoImage` | Custom image to render alongside the label. |
| `underline` | int | Index of label character to underline (Alt-shortcut hint). |
| `localize` | `bool` / `'auto'` | How `text` is treated (literal vs translation key). Default `'auto'`. |
| `takefocus` | bool | Whether the widget participates in Tab traversal. |

`bootstyle` is accepted but **deprecated** — use `accent` and
`variant`.

### Variants

```python
ttk.RadioToggle(app, text="Default")                    # solid fill
ttk.RadioToggle(app, text="Outline", variant="outline")
ttk.RadioToggle(app, text="Ghost",   variant="ghost")
```

| Variant | Off appearance | On appearance |
| --- | --- | --- |
| `default` / `solid` | Filled (accent color) | Filled (accent active) |
| `outline` | Outlined ring | Filled (accent color) |
| `ghost` | Transparent (matches surface) | Subtle accent tint |

`ghost` is the typical choice for inline toolbar toggles where the
unpressed state should disappear into the surrounding chrome.

### Colors & Styling

```python
ttk.RadioToggle(app, text="Primary", accent="primary")
ttk.RadioToggle(app, text="Success", accent="success")
ttk.RadioToggle(app, text="Danger",  accent="danger")
```

`accent` colors the pressed / focus fill. The `ghost` variant
defaults to `accent='secondary'`; the others default to `'primary'`.
See [Design System – Variants](../../design-system/variants.md).

---

## Behavior

**User input.** A left-click selects the toggle and writes its
constructor `value=` into the shared variable. The standard Tk
keyboard contract applies: Tab moves focus, Space invokes.
**Up/Down traverse** between toggles sharing the same `variable=` —
RadioToggle uses `ttk_class='Toolbutton'` for *style lookup* but
keeps the `TRadiobutton` bindtag, so ttk's stock `RadioTraverse`
class binding still applies. (CheckToggle does not get arrow
traversal — it changes its actual `class_` and loses the
`TCheckbutton` bindtag.)

**Disabled and readonly.** `state='disabled'` greys the toggle and
blocks clicks; the variable is still writable from code.
`state='readonly'` behaves identically to `disabled` for user input.

**Reconfiguration.** `accent`, `variant`, `text`, `state`, `value`,
`signal`, and `variable` can all be changed via `configure(...)`
after construction. Reconfiguring `value=` changes the **constant
this toggle writes when clicked** — it does *not* re-write the
shared variable. Use `widget.set(new)` (or `signal.set(new)`) to
change the current selection.

**Visual states.** The toolbutton style maps state combinations
across `selected` (pressed), `pressed` (clicking now), `hover`,
`focus`, and `disabled`. Each variant draws these slightly
differently — see the source for full state-spec lists.

---

## Events

Three observation paths, identical in shape to RadioButton:

| Path | Fires when... | Receives |
| --- | --- | --- |
| `command=` callback (per toggle) | The **user** clicks (or `widget.invoke()` is called) **on this specific toggle**. Programmatic `set()` does not fire it. | No arguments. |
| `signal.subscribe(fn)` | The shared variable changes — from any toggle's user click, from `set()` on any toggle, from direct `signal.set(...)`. | The new selected value. |
| `variable.trace_add('write', fn)` | Same as signal: any variable write. | The Tk trace tuple `(name, index, mode)`. |

For group-level handling, subscribe to the shared signal **once** —
one subscription covers selections from every toggle in the group:

```python
import ttkbootstrap as ttk

app = ttk.App()
view = ttk.Signal("grid")

def on_change(new_value):
    print("view mode:", new_value)

view.subscribe(on_change)

ttk.RadioToggle(app, text="Grid", signal=view, value="grid").pack(side="left", padx=4, pady=10)
ttk.RadioToggle(app, text="List", signal=view, value="list").pack(side="left", padx=4, pady=10)
ttk.RadioToggle(app, text="Card", signal=view, value="card").pack(side="left", padx=4, pady=10)

app.mainloop()
```

Use per-toggle `command=` only when you need to know which
**specific** toggle was clicked. RadioToggle emits **no virtual
events** of its own and exposes no `on_*` helpers.

---

## When should I use RadioToggle?

Use RadioToggle when:

- the choice is a view mode, sort order, or formatting axis where
  the user expects pressed/unpressed buttons in a strip
- the toggles live in a toolbar, formatting bar, or compact mode
  picker (Grid / List / Card; Left / Center / Right / Justify)
- you want `density='compact'` (RadioButton itself doesn't accept
  `density=`)

Prefer:

- **[RadioButton](radiobutton.md)** — for forms, settings panels,
  and any case where the user expects a circular radio indicator
- **[ToggleGroup](togglegroup.md)** — when the toggles should be
  managed as a single composite widget with a unified `add()` /
  `set()` / `on_changed` surface
- **[CheckToggle](checktoggle.md)** — when the toggles are
  independent (Bold / Italic / Underline) rather than mutually
  exclusive
- **[Button](../actions/button.md)** — when the action is one-shot
  (no persistent on/off state)

---

## Related widgets

- **[RadioButton](radiobutton.md)** — parent class; classic radio
  with a circular indicator
- **[CheckToggle](checktoggle.md)** — sibling subclass for
  independent boolean toggles
- **[ToggleGroup](togglegroup.md)** — group container that bundles
  RadioToggle children behind a single signal
- **[RadioGroup](radiogroup.md)** — group container for plain
  RadioButton children

---

## Reference

- **API reference:** `ttkbootstrap.RadioToggle`
- **Related guides:** [Signals](../../capabilities/signals/signals.md),
  [Localization](../../capabilities/localization.md),
  [Design System](../../design-system/index.md)
