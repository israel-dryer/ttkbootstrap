---
title: Label
---

# Label

`Label` is a themed wrapper over `tkinter.ttk.Label` that displays
**read-only text or an image** — headings, captions, instructions,
form-field labels, status text. It's the foundational display widget
in the framework: `Badge`, `Field` labels, and several composite
widgets are built on top of it.

Unlike `Button`, it doesn't fire `command` and doesn't take focus by
default. Unlike `Entry`, it doesn't carry a value model — it
displays whatever is bound to its `text` (or `textvariable` /
`textsignal`).

<figure markdown>
![label](../../assets/dark/widgets-label.png#only-dark)
![label](../../assets/light/widgets-label.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Hello world").pack(padx=20, pady=20)

app.mainloop()
```

Label is one of the few widgets you can construct with no
arguments — `ttk.Label(app)` produces an empty label that you can
populate later via `widget.configure(text=...)` or by binding a
signal.

---

## Common options

Label accepts the standard `ttk.Label` options plus the framework's
theming, icon, and signal extensions. The everyday surface:

| Option           | Purpose                                                          |
| ---------------- | ---------------------------------------------------------------- |
| `text`           | The displayed string. Accepts a literal, `Signal`, or `tk.Variable`. |
| `image`          | A `PhotoImage` to display. Combined with `text` via `compound`.   |
| `icon`           | Theme-aware icon spec resolved through the style system.          |
| `icon_only`      | Removes the extra padding reserved for label text.                |
| `compound`       | Where the image/icon sits relative to text (`"left"`, `"top"`, …). |
| `anchor`         | Where the content sits inside the label box (`"w"`, `"center"`, …). |
| `justify`        | Multi-line alignment (`"left"`, `"center"`, `"right"`).           |
| `wraplength`     | Maximum line width before wrapping.                               |
| `accent`         | Theme color token applied to the **foreground**.                  |
| `surface`        | Theme background token (defaults to the inherited surface).       |
| `font`           | Font name, size, or `tkinter.font.Font` instance.                 |
| `padding`        | Internal padding around the content.                              |
| `localize`       | Whether `text` is treated as a translation key.                   |
| `value_format`   | ICU format spec for non-string values (e.g. `"currency"`, `"decimal"`). |
| `textvariable`   | Tk `StringVar` bound to the displayed text.                       |
| `textsignal`     | Reactive `Signal[str]` bound to the displayed text.               |
| `state`          | `"normal"`, `"disabled"`, `"readonly"` (see Behavior).            |

**Colors & Styling.** `accent` controls the foreground color, not a pill or
chip background — a Label is text on the inherited surface. To get
a high-contrast colored chip, use [Badge](badge.md) instead.

```python
ttk.Label(app, text="Saved", accent="success")
ttk.Label(app, text="Heads up", accent="warning")
```

**Icons.** `icon` accepts a string name or a dict spec. Combine
with `text` via `compound`, or render the icon alone with
`icon_only=True`:

```python
ttk.Label(app, text="Verified", icon="check", compound="left")
ttk.Label(app, icon="info-circle", icon_only=True, accent="info")
```

**Reactive text.** `textsignal` (and `textvariable`) keep the label
synchronized without manual `configure()` calls:

```python
status = ttk.Signal("Connecting…")
ttk.Label(app, textsignal=status).pack()

status.set("Online")  # label updates automatically
```

If you pass `text=signal`, the framework normalizes it into the
`textsignal` slot; both forms are equivalent.

---

## Behavior

`Label` is a static display widget — it has no `command`, no focus
ring, and `takefocus` is `False` by default.

**State.** Through the `TtkStateMixin`, Label honors the standard
ttk states (`normal`, `disabled`, `active`, `readonly`). The
visible effect depends on the theme:

- `"disabled"` typically dims the text via the `!disabled`/`disabled`
  state map.
- `"active"` and `"readonly"` are accepted but rarely have a
  distinct visual on a label.

**Wrap and anchor.** Without `wraplength`, Label is a single line
and the parent's width determines whether the text is clipped. Set
`wraplength` when you need multi-line wrapping inside a fixed
width.

**Locale-aware text.** When `localize=True`, the `text` argument
is treated as a key against the active `MessageCatalog` and the
label re-translates automatically on `<<LocaleChanged>>`. With
`value_format`, non-string values (numbers, dates, currencies) are
formatted through `IntlFormatter` according to the active locale.

```python
ttk.Label(app, text="greeting.hello", localize=True)
ttk.Label(app, text=1234.5, value_format="currency")
```

---

## Events

Label does not emit virtual events and does not expose `on_*`
helpers — it's a pure display widget. Reactivity goes the other
direction: bind a `Signal` or `Variable` to `text` and update the
binding from your code.

If you need click handling on label-shaped content, either bind
manually:

```python
def clicked(event):
    ...

label = ttk.Label(app, text="Click me")
label.bind("<Button-1>", clicked)
```

…or use [Button](../actions/button.md) (with a borderless variant
when you want a label-like appearance).

---

## When should I use Label?

Use `Label` when:

- you need to display read-only text or an image
- you want the text to participate in theming (accent colors, dark
  mode) and locale changes
- you need a reactive display that updates from a `Signal`

Prefer:

- [Badge](badge.md) — for compact, high-contrast pill-style
  status/count chips
- [Field label slot](../forms/field.md) — when labelling a form
  control (handles sizing, alignment, and required-marker
  conventions)
- [Button](../actions/button.md) — when the text is interactive

---

## Related widgets

- **[Badge](badge.md)** — compact status indicator built on Label
- **[Button](../actions/button.md)** — interactive text/icon trigger
- **[Tooltip](../overlays/tooltip.md)** — hover-only contextual text
- **[Progressbar](progressbar.md)** — when the message is "how far"

---

## Reference

- **API reference:** `ttkbootstrap.Label`
- **Related guides:** [Design System](../../design-system/index.md),
  [Localization](../../capabilities/localization.md),
  [Signals](../../capabilities/signals/signals.md)
