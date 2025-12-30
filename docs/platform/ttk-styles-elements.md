# ttk Styles & Elements

ttk widgets separate **behavior** from **appearance**.
This separation is implemented through ttk’s **style and element system**.

Understanding how styles and elements work is essential for understanding how
ttkbootstrap themes, color tokens, and variants function.

This page explains the ttk styling model at a conceptual level and how
ttkbootstrap builds on top of it.

---

## Styles vs widgets

In ttk, widgets do not directly control most aspects of their appearance.

Instead:

- widgets reference a **style name**
- the style defines how the widget is drawn
- styles are resolved dynamically at runtime

This allows the same widget to appear differently under different themes.

---

## What a style is

A ttk style is a named collection of options.

Styles define:

- layout (which elements are drawn and in what order)
- visual properties (colors, borders, padding)
- state-specific behavior (hover, active, disabled)

Styles are identified by hierarchical names, such as:

```
Primary.TButton
Outline.Secondary.TButton
```

Styles are resolved by name, not by widget instance.

---

## Elements

Elements are the lowest-level building blocks of ttk widgets.

An element:

- draws a specific visual component
- may be image-based or primitive-based
- reacts to widget state

Common elements include:

- borders
- backgrounds
- labels
- indicators

Widgets are composed of multiple elements arranged by a layout.

---

## Layouts

A style layout defines how elements are combined to form a widget.

Layouts:
- specify which elements are used
- define how elements are nested
- control alignment and stretching

Changing a layout can radically alter a widget’s appearance without changing its behavior.

---

## Widget states

ttk widgets have a well-defined state model.

Common states include:
- `normal`
- `active`
- `disabled`
- `focus`
- `selected`
- `pressed`

Styles may define different visuals for different states.

ttkbootstrap uses this state model extensively to implement variants and interactions.

---

## How ttkbootstrap uses styles

ttkbootstrap builds on ttk’s styling system rather than replacing it.

The framework:

- generates style names programmatically
- maps semantic concepts (color, variant) to styles
- creates reusable element layouts
- applies consistent state behavior

This allows ttkbootstrap to offer expressive styling while remaining compatible
with ttk’s underlying engine.

---

## Color and variant as style abstractions

The `color` and `variant` parameters provide a high-level description of a widget's visual intent.

Instead of working directly with style names, users specify:

- semantic color (via `color` parameter)
- visual variant (via `variant` parameter)

ttkbootstrap resolves these into concrete ttk style names and layouts.

This keeps styling declarative and consistent:

- See [Design System → Variants](../design-system/variants.md) for semantic styling options.
- See [Guides → Styling](../guides/styling.md) for how to apply styles in practice.

---

## Common pitfalls

- attempting to configure ttk widgets like Tk widgets
- modifying styles without understanding layout implications
- relying on implicit style inheritance
- mixing Tk and ttk styling approaches

Understanding the style and element system helps avoid these issues.

---

## Next steps

- See [Design System](../design-system/index.md) for tokens and visual semantics.
- See [Design System → Typography](../design-system/typography.md) for font styling.
- See [Widgets](../widgets/index.md) to see how styles are applied in practice.
