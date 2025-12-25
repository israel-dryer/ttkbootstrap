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

title: PasswordEntry
---

# PasswordEntry

`PasswordEntry` is a secure, form-ready text input control for passwords, PINs, and other sensitive values.

It builds on `TextEntry`, adding masking, optional reveal behavior, and password-specific validation patterns—while preserving
the same label/message, localization, and event model used throughout ttkbootstrap v2. fileciteturn14file1

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

pwd = ttk.PasswordEntry(
    app,
    label="Password",
    required=True,
    message="Must be at least 8 characters",
)
pwd.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

PasswordEntry separates **what is displayed** from **what is stored**.

| Concept | Meaning |
|---|---|
| Text | Masked display text |
| Value | Actual committed password value |

```python
secret = pwd.value   # committed value
raw = pwd.get()      # raw internal text
```

The reveal toggle changes only the display, never the underlying value.

---

## Common options

### `required`, `message`, `bootstyle`

```python
ttk.PasswordEntry(app, label="Password", required=True, message="Minimum 8 characters")
```

### Reveal toggle: `show_visible_toggle`

```python
pwd = ttk.PasswordEntry(app, label="Password", show_visible_toggle=False)
```

### Add-ons

```python
pwd.insert_addon(ttk.Label, position="before", icon="lock", icon_only=True)
```

---

## Behavior

- Characters are masked while typing.

- A reveal button is shown by default (configurable).

- Commit semantics match other field controls (blur or Enter).

---

## Events

PasswordEntry emits the standard field events:

- `<<Input>>` / `on_input` — editing

- `<<Changed>>` / `on_changed` — committed value changed

- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

```python
def handle_changed(event):
    print("Password updated")

pwd.on_changed(handle_changed)
```

!!! tip "Event usage"
    Use `on_input(...)` for live UX feedback (e.g., strength meters).  
    Use `on_changed(...)` for authentication or submission logic.

---

## Validation and constraints

Password validation is typically applied **on commit**, not per keystroke.

```python
pwd = ttk.PasswordEntry(app, label="Password", required=True)
pwd.add_validation_rule("min_length", 8, message="Minimum 8 characters")
```

Common patterns include:

- required

- minimum length

- character class rules

- confirmation match (cross-field rule)

---

## When should I use PasswordEntry?

Use `PasswordEntry` when:

- the input should not be displayed in clear text

- you want consistent form UX (label/message/validation/events)

Prefer **TextEntry** when:

- masking is not required

Prefer **NumericEntry** when:

- the input is numeric-only (PINs with numeric constraints)

---

## Related widgets

- **TextEntry** — general text field

- **NumericEntry** — numeric input with validation

- **Form** — structured field layout and submission

---

## Reference

- **API Reference:** `ttkbootstrap.PasswordEntry`

---

## Additional resources

### Related widgets

- [DateEntry](dateentry.md)

- [LabeledScale](labeledscale.md)

- [NumericEntry](numericentry.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.PasswordEntry`](../../reference/widgets/PasswordEntry.md)
