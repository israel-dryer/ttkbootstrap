---
title: Badge
---

# Badge

`Badge` is a compact, accent-colored chip built on top of `Label`. It's
intended for short, scannable values — counts, statuses, tags — like
`"New"`, `"Beta"`, `"3"`, or `"Offline"`. Unlike a plain Label, where
`accent` only tints the foreground, a Badge renders as a filled
shape: the chip background takes the accent color, the text takes
the auto-contrast `on_color`.

By default Badge is a `square`-cornered chip in the `primary` accent
at `-size 8` font with centered content. Switch to a rounded pill via
`variant="pill"`, or to any other accent via `accent="success"`,
`"danger"`, etc.

<figure markdown>
![badge](../../assets/dark/widgets-badge.png#only-dark)
![badge](../../assets/light/widgets-badge.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Badge(app, text="New").pack(padx=20, pady=10)
ttk.Badge(app, text="3", accent="success", variant="pill").pack(padx=20, pady=10)

app.mainloop()
```

Badge inherits the full Label construction surface, so anything you
can set on a Label (icon, image, signal-bound text, formatting) you
can set on a Badge.

---

## Common options

Badge accepts every `Label` option plus a `variant` knob for chip
shape. Defaults differ from Label in a few places — Badge centers
its content, uses a smaller font, and resolves to the `primary`
accent fill if none is supplied.

| Option           | Purpose                                                            |
| ---------------- | ------------------------------------------------------------------ |
| `text`           | The displayed string. Accepts a literal, `Signal`, or `tk.Variable`. |
| `image`          | A `PhotoImage` to display. Combined with `text` via `compound`.    |
| `icon`           | Theme-aware icon spec resolved through the style system.           |
| `icon_only`      | Removes the extra padding reserved for label text.                 |
| `compound`       | Where the image/icon sits relative to text (`"left"`, `"top"`, …). |
| `accent`         | Chip fill color (`"primary"` by default). Foreground auto-contrasts. |
| `variant`        | `"square"` (default) or `"pill"` — chip silhouette.                |
| `surface`        | Surface token used outside the chip outline. Inherited by default. |
| `anchor`         | Content position inside the chip (`"center"` by default).          |
| `padding`        | Internal padding around the chip content.                          |
| `width`          | Width of the badge in characters.                                  |
| `wraplength`     | Maximum line width before wrapping. Rare on a badge.               |
| `font`           | Font name, size, or `tkinter.font.Font` (`-size 8` by default).    |
| `localize`       | Whether `text` is treated as a translation key.                    |
| `value_format`   | ICU format spec for non-string values (`"decimal"`, `"currency"`, …). |
| `textvariable`   | Tk `StringVar` bound to the displayed text.                        |
| `textsignal`     | Reactive `Signal[str]` bound to the displayed text.                |
| `state`          | `"normal"`, `"disabled"`, `"readonly"` (see Behavior).             |

**Accent and variant.** `accent` drives the chip's fill; the
text foreground is selected by the framework as the readable
contrast color (`on_color(accent)`), so you don't set foreground
manually:

```python
ttk.Badge(app, text="Beta", accent="primary")
ttk.Badge(app, text="Saved", accent="success", variant="pill")
ttk.Badge(app, text="Failed", accent="danger")
```

**Icons and counts.** Because Badge is a Label, icon-only and
text-plus-icon chips work the same way:

```python
ttk.Badge(app, text="Verified", icon="check", compound="left", accent="success")
ttk.Badge(app, icon="bell", icon_only=True, accent="info")
ttk.Badge(app, text="12", variant="pill", accent="danger")
```

**Reactive text.** Bind a `Signal` (or `Variable`) to keep the
chip live:

```python
unread = ttk.Signal(0)
ttk.Badge(app, textsignal=unread, accent="danger", variant="pill").pack()

unread.set(5)  # badge updates automatically
```

If you pass `text=signal`, the framework normalizes it into
`textsignal`; both forms are equivalent.

---

## Behavior

Badge is a static display widget — it doesn't take focus, fire
`command`, or carry a value model.

**State.** Through the `TtkStateMixin`, Badge accepts the standard
ttk states (`normal`, `disabled`, `active`, `readonly`). The
`disabled` state typically dims the chip; the other states are
accepted but rarely have a distinct visual on a badge.

**Sizing and wrapping.** Badge is a single-line chip by default.
The chip grows to fit its text content plus the built-in `(6, 0)`
horizontal padding. Use `width` to fix a character width; use
`wraplength` only when you actually want a multi-line chip.

**Locale-aware text.** With `localize=True`, `text` is treated
as a translation key against the active `MessageCatalog`, and the
badge re-translates on `<<LocaleChanged>>`. With `value_format`,
non-string values are formatted through `IntlFormatter`:

```python
ttk.Badge(app, text="status.new", localize=True, accent="info")
ttk.Badge(app, text=1234, value_format="decimal", variant="pill")
```

---

## Events

Badge does not emit virtual events and does not expose any `on_*`
helpers — it's a pure display widget. Reactivity goes the other
direction: bind a `Signal` or `Variable` to `text` and update the
binding from your code.

If you need click handling on a chip, either `bind("<Button-1>", …)`
manually, or use a [Button](../actions/button.md) styled to look
like a chip.

---

## When should I use Badge?

Use `Badge` when:

- you need a small, high-contrast pill or square chip for status,
  counts, or tags
- the value is short (typically 1–12 characters)
- you want consistent chip styling across the UI

Prefer:

- [Label](label.md) — for plain text without a colored background,
  for multi-line content, or for headings/captions
- [Progressbar](progressbar.md) / [Floodgauge](floodgauge.md) /
  [Meter](meter.md) — when the message is "how much" or "how far"
- [Toast](../overlays/toast.md) — when feedback should appear,
  linger, and dismiss itself

---

## Related widgets

- **[Label](label.md)** — the foundational read-only widget Badge
  extends
- **[Progressbar](progressbar.md)** — continuous progress indicator
- **[Meter](meter.md)** — dashboard-style gauge
- **[Floodgauge](floodgauge.md)** — capacity indicator with a label

---

## Reference

- **API reference:** `ttkbootstrap.Badge`
- **Related guides:** [Design System](../../design-system/index.md),
  [Localization](../../capabilities/localization.md),
  [Signals](../../capabilities/signals/signals.md)
