---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


---

title: Badge
---

# Badge

`Badge` is a compact **status indicator** built on top of `Label`.

It’s designed for short, scannable values like **counts**, **statuses**, and **tags** — for example: “New”, “Beta”, “3”, “Offline”.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Badge(app, text="New").pack(padx=20, pady=10)
ttk.Badge(app, text="3", bootstyle="primary").pack(padx=20, pady=10)

app.mainloop()
```

---

## Styling with `bootstyle`

`Badge` defaults to `bootstyle="badge"` and will **coerce** your bootstyle to include the `-badge` suffix.

That means these are equivalent:

```python
ttk.Badge(app, text="Beta")                  # uses "badge"
ttk.Badge(app, text="Beta", bootstyle="badge")
ttk.Badge(app, text="Beta", bootstyle="primary")        # coerced to "primary-badge"
ttk.Badge(app, text="Beta", bootstyle="primary-badge")  # explicit
```

!!! note "Bootstyle coercion"
    If the provided `bootstyle` does not include `"badge"`, it is automatically rewritten as `"{bootstyle}-badge"`.

---

## Icon badges

Because `Badge` subclasses `Label`, you can use icons the same way:

```python
ttk.Badge(app, text="Verified", icon="check").pack(pady=6)
ttk.Badge(app, icon="bell", icon_only=True, bootstyle="info").pack(pady=6)
```

---

## Common options

Badge accepts the standard `Label` options, including:

- `text`

- `icon`, `image`, `compound`

- `icon_only`

- `padding`, `width`, `wraplength`

- `font`, `foreground`, `background`

- `localize`, `value_format`

---

## When should I use Badge?

Use `Badge` when:

- you need a small, high-contrast label for status or counts

- the value is short (typically 1–12 characters)

- you want a consistent visual “pill” across the UI

Prefer `Label` when:

- text is long or multi-line

- content should blend into the surrounding layout (not pop)

Prefer `Toast` when:

- you need transient feedback that should disappear automatically

---

## Related widgets

- **Label** — general-purpose read-only text

- **Toast** — non-blocking feedback

- **Progressbar / Meter / FloodGauge** — continuous indicators

---

## Reference

- **API Reference:** `ttkbootstrap.Badge`

---

## Additional resources

### Related widgets

- [FloodGauge](floodgauge.md)

- [Label](label.md)

- [ListView](listview.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.Badge`](../../reference/widgets/Badge.md)
