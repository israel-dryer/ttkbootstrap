---
title: Variants
---

# Variants

Variants define **visual emphasis and interaction style**, not meaning.

While colors express *intent*, variants express *weight*—how prominent or subtle
a control should appear.

Variants are consistent across widgets.

---

## Common variants

The most common variants are:

- **solid** — highest emphasis (default)
- **outline** — secondary emphasis
- **ghost** — low emphasis, minimal chrome
- **link** — text-like navigation actions
- **text** — lowest emphasis utility actions

Not all widgets support every variant, but supported variants behave consistently.

---

## Emphasis hierarchy

Variants establish a visual hierarchy:

1. Solid (primary actions)
2. Outline (secondary actions)
3. Ghost / Text (contextual or utility actions)

This hierarchy helps users quickly identify what matters most.

---

## Variants across widgets

Variants are *not widget-specific*.

If you understand how a variant behaves here, you understand how it behaves on:

- buttons
- toggles
- segmented controls
- menu actions (where applicable)

See:

- [Widgets → Button](../widgets/actions/button.md)
- [Widgets → ToggleGroup](../widgets/selection/togglegroup.md)

---

## Applying variants

Variants are applied using the `variant` parameter alongside `color`.

```python
ttk.Button(app, text="Save", color="primary")  # solid (default)
ttk.Button(app, text="Cancel", color="secondary", variant="outline")
ttk.Button(app, text="Learn More", color="info", variant="link")
```

How to apply them in real layouts is covered in:

- [Guides → Styling](../guides/styling.md)

---

## Related concepts

- [Colors](colors.md)
- [Icons](icons.md)