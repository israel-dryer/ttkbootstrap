---
title: SelectionWidgetName
---

# SelectionWidgetName

1–2 paragraphs describing:

- what kind of selection this control represents (single, multiple, tri-state, from-a-list)

- what value it produces and how it is typically used (settings, filters, preferences)

If relevant, briefly contrast it with closely related selection controls.

---

## Framework integration

**Value model**

- Whether choices are independent or mutually exclusive

- What value type is produced (`bool`, `str`, `set`, etc.)

- When the value is considered committed

**Signals & Events**

- Preferred binding (`signal=...`) when supported

- Change events and virtual events

**Design System**

- Variant expectations (checkbox vs toggle, radio vs button-style radio)

- How states are represented visually (selected, active, disabled)

**Localization**

- How labels and option text participate in localization

---

## Overview

Explain the selection model in plain terms:

- whether choices are **independent** or **mutually exclusive**

- how many values can be selected

- whether the control represents a boolean, enum, set, or list-based choice

---

## Basic usage

Show a minimal, runnable example demonstrating:

- creating the widget

- setting an initial selection (`value`, `default`, etc.)

- packing or gridding it

```python
# minimal, copy/paste runnable
```

---

## Variants

If the widget supports visual or behavioral variants, document them here.

Examples:

- checkbox vs toggle

- radio vs button-style radio

- dropdown vs inline list

Use a short example per variant.

---

## How the value works

Describe the value model clearly:

- what the value represents

- its type (`bool`, `str`, `set`, etc.)

- default value semantics

- special values (e.g., `None` for indeterminate)

Explain when the value is considered committed.

---

## Binding to signals or variables

Explain state binding options:

- preferred reactive binding (`signal=...`)

- Tk variables (`variable=...`, `textvariable=...`) as alternatives

Show a concise two-way binding example.

---

## Common options

Curated options only, such as:

- `items` (for list-based selection)

- `value` / `default`

- `state` / `readonly`

- `command`

- widget-specific options (search, allow_custom_values, onvalue/offvalue)

---

## Behavior

Describe interaction behavior:

- mouse and keyboard interaction

- how selection changes are triggered

- popup open/close behavior for dropdown-style controls

- group behavior (for radio groups)

---

## Events

Document selection-related events:

- committed change (`on_changed`, `<<Changed>>`)

- live input (`on_input`, `<<Input>>`) when applicable

```python
def on_changed(e):
    ...

w.on_changed(on_changed)
```

---

## Validation and constraints

Describe common constraints:

- enforcing valid options

- tri-state or mixed-selection semantics

- dynamic option lists

- cross-field selection rules

---

## Colors and styling

If supported, document `color` and `variant` usage and variant combinations.

Show a few representative examples rather than an exhaustive list.

---

## Localization

Explain how labels and option text participate in localization:

- default behavior

- explicitly enabling/disabling localization

- recommended key conventions

---

## When should I use SelectionWidgetName?

Use it when:

- …

Prefer OtherWidget when:

- …

---

## Additional resources

**Related widgets**

- **OtherSelectionWidget** — how it differs

- **AnotherWidget** — complementary behavior

**Framework concepts**

- [Signals & Events](../../capabilities/signals/index.md)

- [Localization](../../capabilities/localization.md)

- [Validation](../../capabilities/validation.md)

**API reference**

- **API Reference:** `ttkbootstrap.SelectionWidgetName`

- **Related guides:** Selection, Forms, Localization
