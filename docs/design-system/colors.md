---
title: Colors
---

# Colors

Colors in ttkbootstrap are **semantic**, not literal.

Instead of choosing colors by appearance (blue, green, red), applications use
color *intent*—such as *primary*, *success*, or *danger*. The active theme
determines how those intents are rendered.

---

## Semantic color tokens

Common color intents include:

- `primary` — primary actions and focus
- `secondary` — supporting or neutral elements
- `success` — positive or completed states
- `warning` — caution or attention
- `danger` — destructive or critical actions
- `info` — supplemental or informational content

These tokens are consistent across widgets and themes.

---

## Why semantic colors matter

Semantic colors allow:

- automatic theme switching (light / dark)
- consistent meaning across the UI
- centralized visual control
- accessible contrast handling

The same widget code adapts visually without modification.

---

## Using colors in widgets

Widgets reference semantic colors using the `color` parameter.

How colors are *applied* to widgets is covered in:

- [Design System → Variants](variants.md)
- [Widgets → Button](../widgets/actions/button.md)

---

## Custom palettes

Themes map semantic tokens to actual colors.

To customize how colors are rendered, see:

- [Custom Themes](custom-themes.md)

---

## Related concepts

- [Variants](variants.md)
- [Design System → Icons](icons.md)
- [Guides → Styling](../guides/styling.md)