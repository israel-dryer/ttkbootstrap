---
title: Entry
---

# Entry

`Entry` is the single-line text input primitive in ttkbootstrap. It is
a thin themed wrapper over `tkinter.ttk.Entry` that adds the
ttkbootstrap styling tokens (`accent`, `density`, `surface`) and a
reactive `textsignal` channel alongside the standard `textvariable`.

Entry is the building block that the input composites
([`TextEntry`](../inputs/textentry.md),
[`NumericEntry`](../inputs/numericentry.md),
[`DateEntry`](../inputs/dateentry.md),
[`PasswordEntry`](../inputs/passwordentry.md), and friends) wrap. For
form UX you almost always want one of those — they add labels, helper
text, commit-time parsing, validation messages, and the framework's
standard `on_input` / `on_changed` event surface. Reach for `Entry`
directly when you are building a custom composite of your own or need
the raw ttk-Entry surface.

<figure markdown>
![entry](../../assets/dark/widgets-entry.png#only-dark)
![entry](../../assets/light/widgets-entry.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

entry = ttk.Entry(app)
entry.pack(padx=20, pady=20)

app.mainloop()
```

To pre-fill the entry, write through the bound variable or call
`insert()` directly:

```python
ttk.Entry(app, textvariable=ttk.StringVar(value="Ada")).pack()

# or imperatively
e = ttk.Entry(app)
e.insert(0, "Ada")
e.pack()
```

---

## Value model

`Entry` holds a single string. The current text is reachable in three
equivalent ways:

- **Tk method**: `entry.get()` / `entry.delete(0, "end")` /
  `entry.insert(0, ...)` — the standard `ttk.Entry` API.
- **Tk variable**: pass `textvariable=tk.StringVar(...)` and
  read/write through the variable.
- **Reactive signal**: pass `textsignal=ttk.Signal("")` and subscribe
  via `signal.subscribe(...)`.

`textvariable` and `textsignal` are kept in sync automatically through
the `TextSignalMixin`. If you don't pass either, accessing
`entry.textsignal` (or `entry.textvariable`) lazily creates and binds
one. If both are passed, `textsignal` wins.

Unlike the input composites, `Entry` has **no commit-vs-input
distinction**. Every keystroke is a value change — there is no
"commit" event, no parsing, no validation messages. If you need that
distinction, use [`TextEntry`](../inputs/textentry.md).

---

## Common options

| Option | Type | Description |
|---|---|---|
| `textvariable` | `tk.Variable` | Tk variable bound to the entry text. |
| `textsignal` | `Signal[str]` | Reactive signal bound to the entry text. Wins over `textvariable` when both are passed. |
| `show` | `str` | Substitute character displayed for each typed character (e.g. `"*"` for masked input). |
| `width` | `int` | Width in **characters**, not pixels. |
| `justify` | `str` | Text alignment: `"left"`, `"center"`, `"right"`. |
| `state` | `str` | `"normal"` (default), `"readonly"` (uneditable but selectable), or `"disabled"` (uneditable, dimmed, not focusable). |
| `validate` | `str` | Tk validation mode — see *Validation and constraints*. |
| `validatecommand` | tuple | Tk validation callback. |
| `accent` | `str` | Theme token for the focus ring (`"primary"`, `"success"`, `"danger"`, …). Defaults to `"primary"`. |
| `surface` | `str` | Surface token of the parent container; affects the focus-ring blend. Inherited from parent if not set. **Construction-only** — see *Behavior*. |
| `density` | `'default'` \| `'compact'` | Visual size. `compact` uses the smaller `caption` font and shorter row image. **Reconfigure is partially broken** — see *Behavior*. |
| `font` | `str \| Font` | Override the entry text font. Forced to `caption` when `density='compact'`. |
| `style_options` | `dict` | Escape hatch for additional builder keys (e.g. `{'input_background': 'background'}`). |

The `accent` and `surface` tokens flow into the entry's style builder,
which renders the field background, border, focus ring, and selection
highlight. Only the `default` variant is registered — passing any other
`variant` value raises `BootstyleBuilderError`.

!!! note "Background tokens"
    The field's fill color resolves to the `input_background` style
    option (defaults to `content`). The constructor doesn't expose
    `input_background` directly — pass it via
    `style_options={'input_background': 'background'}`, or set it on
    the parent `Frame` so it cascades. Inside a
    `Frame(input_background='...')`, every descendant Entry inherits
    the value automatically.

---

## Behavior

**Standard ttk.Entry behavior.** Focus, caret navigation, copy/cut/
paste shortcuts, selection (`Shift-Home`, double-click, etc.), and the
`<KeyPress>` / `<KeyRelease>` / `<FocusIn>` / `<FocusOut>` events are
all inherited unchanged from ttk.

**State semantics:**

- `state="normal"` — editable, focusable.
- `state="readonly"` — selection and cursor work, typing does not.
  Readonly entries still receive focus.
- `state="disabled"` — uneditable, dimmed, removed from focus
  traversal.

The shorthand `entry.state(["readonly"])` / `entry.state(["disabled"])`
also works (provided by `TtkStateMixin`) and is the form to prefer when
toggling the same state on and off.

**Reconfiguration caveats.**

- `entry.configure(accent=...)` rebuilds the resolved style and works
  as expected.
- `entry.configure(surface=...)` raises
  `TclError: unknown option "-surface"`. The `surface` constructor
  argument has no matching configure delegate. Set surface at
  construction time, or fall through to the escape hatch:
  `entry.configure_style_options(surface='primary')`. Either way, the
  parent frame's surface is the better channel for surface
  inheritance.
- `entry.configure(density=...)` updates only the entry's **font**.
  The resolved ttk style is not rebuilt, so the underlying image
  element and padding from the construction-time density persist.
  Default-density Entries reconfigured to `compact` keep their
  default-height row but get the smaller caption font — visually
  inconsistent. Set `density` at construction time.

---

## Events

`Entry` does not emit any framework virtual events and ships no `on_*`
helpers — it is a passthrough to `ttk.Entry`. To observe value changes,
subscribe through the binding channel:

```python
entry = ttk.Entry(app, textsignal=ttk.Signal(""))
entry.textsignal.subscribe(lambda value: print("text:", value))
```

Or bind directly to the Tk events the underlying widget produces:

```python
entry.bind("<KeyRelease>", lambda e: print(entry.get()))
entry.bind("<FocusOut>", lambda e: print("committed:", entry.get()))
entry.bind("<Return>",   lambda e: print("submit:",    entry.get()))
```

For framework-standard `on_input` (every keystroke) and `on_changed`
(commit boundary) helpers, use [`TextEntry`](../inputs/textentry.md).

---

## Validation and constraints

`Entry` exposes Tk's native `validate` / `validatecommand` /
`invalidcommand` machinery directly. Use it when you need
per-keystroke gating that physically rejects input:

```python
def is_digits(new_value: str) -> bool:
    return new_value.isdigit() or new_value == ""

vcmd = (app.register(is_digits), "%P")
ttk.Entry(app, validate="key", validatecommand=vcmd).pack()
```

Tk's substitution codes (`%P` for the proposed value, `%S` for the
inserted text, `%V` for the validation phase, etc.) are documented in
the [Tk docs for ttk::entry](https://www.tcl.tk/man/tcl/TkCmd/ttk_entry.htm).

This kind of validation is "hard" — invalid input is silently
discarded, with no visible feedback to the user. For form UX where
invalid input should be **shown** with a validation message, use
[`TextEntry`](../inputs/textentry.md) (or
[`NumericEntry`](../inputs/numericentry.md) /
[`DateEntry`](../inputs/dateentry.md)) — those expose
`on_valid` / `on_invalid` plus a built-in message line.

---

## When should I use Entry?

Reach for `Entry` directly when:

- you are **building your own composite** and need a raw input that
  you'll wrap with your own labels, messages, or layout;
- you specifically want **Tk-native key validation** with the
  `validate` / `validatecommand` machinery;
- you need to drop down to a `ttk.Entry` option (`xscrollcommand`,
  `exportselection`, `invalidcommand`) that the input composites
  don't surface.

For everything else — forms, dialogs, settings panes, anything a user
will see — prefer one of the input composites. They are cheap to
adopt, integrate with the framework's signal/event surface, and ship
with the visual affordances (label, message, prefix/suffix, etc.) that
real apps need.

## Related widgets

- [TextEntry](../inputs/textentry.md) — form-ready text field with
  label, helper text, validation messages, and `on_input` /
  `on_changed` events.
- [PasswordEntry](../inputs/passwordentry.md) — masked input with a
  reveal toggle and validation hooks.
- [NumericEntry](../inputs/numericentry.md) — numeric input with
  bounds, stepping, and locale-aware formatting.
- [DateEntry](../inputs/dateentry.md) /
  [TimeEntry](../inputs/timeentry.md) — structured date/time inputs.
- [SpinnerEntry](../inputs/spinnerentry.md) — generic incremental
  input with up/down arrows.
- [Combobox](combobox.md) / [Spinbox](spinbox.md) — sibling
  primitives wrapping `ttk.Combobox` / `ttk.Spinbox`.

## Reference

- [`ttkbootstrap.Entry`](../../reference/widgets/Entry.md)
