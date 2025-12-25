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

title: RadioButton
---

# RadioButton

`RadioButton` is a **selection control** that lets users choose **exactly one option** from a set of mutually exclusive choices.

Use `RadioButton` when all options are short and should be visible at once (settings, modes, priority levels).

<figure markdown>
![radiobutton states](../../assets/dark/widgets-radiobutton-states.png#only-dark)
![radiobutton states](../../assets/light/widgets-radiobutton-states.png#only-light)
</figure>

---

## Overview

A radio selection is defined by a **shared value** plus a distinct `value=` for each option:

- each `RadioButton` represents one possible value

- the selected option is the one whose `value` matches the shared **signal** or **variable**

- only one option can be selected at a time

---

## Basic usage

In ttkbootstrap v2, the shared value is typically managed using a `signal`.

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.Signal("medium")

ttk.RadioButton(app, text="Low", signal=choice, value="low").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="Medium", signal=choice, value="medium").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="High", signal=choice, value="high").pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

---

## Variants

### RadioButton (default)

The standard radio indicator + label.

```python
ttk.RadioButton(app, text="Option", signal=choice, value="opt")
```

### RadioToggle

If you want a button-like “badge” look for mutually exclusive choices, use `RadioToggle`.

```python
ttk.RadioToggle(app, text="Grid", signal=view, value="grid")
ttk.RadioToggle(app, text="List", signal=view, value="list")
```

---

## How the value works

`RadioButton` uses a **single shared value** to represent the selected option.

- each `RadioButton` defines its own `value`

- selection is the option whose `value` matches the shared signal or variable

```python
choice = ttk.Signal("low")

ttk.RadioButton(app, text="Low", signal=choice, value="low")
ttk.RadioButton(app, text="High", signal=choice, value="high")
```

Updating the shared state changes the selected option:

```python
choice.set("high")
```

!!! note "Single source of truth"
    The shared signal or variable is the source of truth.
    Individual radio buttons do not store state independently.

---

## Binding to signals or variables

Signals are generally preferred in v2 applications, but Tk variables are fully supported.

### Using a Tk variable

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.StringVar(value="medium")

ttk.RadioButton(app, text="Low", variable=choice, value="low").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="Medium", variable=choice, value="medium").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="High", variable=choice, value="high").pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

---

## Common options

### `command`

Use `command=` to react when the selection changes.

```python
choice = ttk.Signal("low")

def on_change():
    print("selected:", choice.get())

ttk.RadioButton(app, text="Low", signal=choice, value="low", command=on_change)
ttk.RadioButton(app, text="High", signal=choice, value="high", command=on_change)
```

### `state`

Disable individual options when they are not available.

```python
choice = ttk.Signal("basic")

ttk.RadioButton(app, text="Basic", signal=choice, value="basic")
ttk.RadioButton(app, text="Pro (unavailable)", signal=choice, value="pro", state="disabled")
```

---

## Behavior

- Selecting an option sets the shared signal/variable to that option’s `value`.

- Only one option may be selected at a time.

- Keyboard navigation follows standard ttk radiobutton behavior (focus + Space to select).

---

## Events

Use `command=` for per-button callbacks, or subscribe to the shared signal for group-level changes.

```python
choice = ttk.Signal("low")

def on_selected(value):
    print("selected:", value)

bind_id = choice.subscribe(on_selected)
# Later: choice.unsubscribe(bind_id)
```

---

## Validation and constraints

Radio selections are inherently constrained to the set of options you provide.

Validation is most useful when:

- a selection is required before submitting a form

- certain options become unavailable based on other inputs

---

## Colors and styling

RadioButtons support standard ttkbootstrap color tokens.

```python
ttk.RadioButton(app)  # primary is default
ttk.RadioButton(app, bootstyle="secondary")
ttk.RadioButton(app, bootstyle="success")
ttk.RadioButton(app, bootstyle="info")
ttk.RadioButton(app, bootstyle="warning")
ttk.RadioButton(app, bootstyle="danger")
```

<figure markdown>
![colors](../../assets/dark/widgets-radiobutton-colors.png#only-dark)
![colors](../../assets/light/widgets-radiobutton-colors.png#only-light)
</figure>

---

## Localization

Localization behavior is controlled by the global application settings.

By default, widgets use `localize="auto"`: if a translation exists for `text`, it is used;
otherwise `text` is treated as a literal label.

```python
ttk.RadioButton(app, text="settings.mode.basic")
ttk.RadioButton(app, text="settings.mode.basic", localize=True)
ttk.RadioButton(app, text="Basic", localize=False)
```

!!! tip "Safe to pass literal text"
    With `localize="auto"`, passing literal text is safe when no translation exists.

---

## When should I use RadioButton?

Use `RadioButton` when:

- exactly **one option must be selected**

- all options are short and visible

Prefer **CheckButton** when:

- multiple selections are allowed

Prefer **SelectBox / OptionMenu** when:

- the list is long

- screen space is limited

- search or filtering is needed

---

## Related widgets

- **CheckButton** — multiple independent selections

- **SelectBox** — dropdown selection, optional search

- **OptionMenu** — simple menu-based selection

- **RadioGroup** — composite control for managing radio options as one widget

- **RadioToggle** — button-like radio styling

---

## Reference

- **API Reference:** `ttkbootstrap.RadioButton`

---

## Additional resources

### Related widgets

- [Calendar](calendar.md)

- [CheckButton](checkbutton.md)

- [CheckToggle](checktoggle.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.RadioButton`](../../reference/widgets/RadioButton.md)
