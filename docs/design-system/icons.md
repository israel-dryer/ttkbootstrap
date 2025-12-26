---
title: Icons
---

# Icons

Icons in ttkbootstrap are **symbolic UI elements**, not static image files.

They are part of the design system and behave consistently across themes,
widgets, and screen densities.

---

## Icon model

An icon in ttkbootstrap is:

- referenced by name (not file path)
- resolved through an icon provider
- recolored automatically by theme
- DPI-aware and cached by the framework

Icons participate in widget state (hover, disabled, active) automatically.

---

## Why icons are symbolic

By treating icons symbolically:

- the same icon works in light and dark themes
- color and contrast are handled centrally
- scaling is automatic
- widgets remain declarative

Applications express *intent*, not rendering details.

---

## Icon providers

Icon providers supply named icons to the framework.

Which providers are available depends on the environment and configuration.

---

## Using icons in applications

How icons are applied to widgets and patterns is covered in:

- [Guides → Icons](../guides/icons.md)

Widget-specific icon usage examples appear in:

- [Widgets → Button](../widgets/actions/button.md)
- [Widgets → ContextMenu](../widgets/actions/contextmenu.md)

---

## Related concepts

- [Design System → Colors](colors.md)
- [Capabilities → Icons & Imagery](../capabilities/icons-and-imagery.md)
