---
icon: fontawesome/solid/droplet
---

# Color System

The ttkbootstrap color system is designed to help you style desktop interfaces using **semantic intent**, not raw
colors.

Instead of assigning hex values or referencing low-level TTK style names, you describe *what a color means* in the
interface—such as “primary action”, “warning state”, or “background surface”—and ttkbootstrap resolves the actual colors
based on the active theme.

This approach allows applications to remain:

- visually consistent,
- theme-aware,
- adaptable to light and dark modes,
- and resilient to future design changes.

This page explains **how the color system is structured and how it is meant to be used conceptually**. Practical
examples and recipes are covered in the Guides section.

---

## Design Goals

The color system is built around a few core goals:

- **Semantic clarity**  
  Colors communicate meaning, not just appearance.

- **Theme independence**  
  Applications should not depend on specific color values.

- **Consistency across widgets**  
  The same intent should look consistent everywhere.

- **Adaptability**  
  Colors should respond automatically to theme changes, contrast modes, and platform differences.

To support these goals, ttkbootstrap organizes colors into **tokens**, **variants**, and **modifiers**.

---

## Color Tokens

A **color token** represents a semantic role in the interface.

Examples include:

- `primary`
- `secondary`
- `success`
- `warning`
- `danger`
- `info`
- `background`
- `foreground`

Tokens do not describe how a color looks.  
They describe **what the color represents**.

For example:

- `primary` represents the main action or emphasis color.
- `background` represents surfaces behind content.
- `danger` represents destructive or error-related actions.

Each theme defines how these tokens are rendered visually.

---

## Variants

Variants describe **how a color is applied** to a widget.

Common variants include:

- `solid`
- `outline`
- `link`
- `ghost`

Variants affect:

- fill vs border usage,
- emphasis level,
- interaction affordances.

For example, a `primary-outline` button communicates the same intent as `primary`, but with reduced visual weight.

Variants allow consistent styling choices without redefining color meaning.

---

## Bootstyle Strings

Colors are typically applied using **bootstyle strings**, which combine intent and variant into a single declarative
value.

A bootstyle string is composed of:

```
<color token>-<variant>
```

Examples:

- `primary`
- `secondary-outline`
- `danger-link`
- `success-ghost`

Bootstyle strings allow widgets to be styled consistently without referencing raw TTK style names or color values.

---

## Modifiers

Modifiers refine a color’s appearance while preserving its semantic meaning.

Examples include:

- subtle emphasis
- elevated or recessed surfaces
- hover or active state adjustments

Modifiers are intended to make **small visual adjustments**, not to redefine the meaning of a color.

> **Design rule:**  
> If a color requires extensive modification to “look right,” the underlying token choice is likely incorrect.

Modifiers should be used sparingly and consistently to maintain a coherent visual language.

---

## Theme Resolution

Each theme defines a complete color palette for all supported tokens.

When a theme is active:

- tokens are resolved to concrete color values,
- variants are rendered appropriately,
- modifiers are applied consistently.

Applications do not need to know—or care—about the actual color values being used.

Switching themes updates the entire interface automatically.

---

## Hashed Style Names

Internally, ttkbootstrap generates hashed TTK style names to ensure:

- uniqueness,
- isolation between widgets,
- compatibility with TTK’s style engine.

These hashed names are an **implementation detail**.

> **Important:**  
> Hashed style names are not part of the public API and are not guaranteed to remain stable across versions.  
> Application code should never reference them directly.

All styling should be expressed through tokens, variants, and bootstyle strings.

---

## ttkbootstrap’s Role

In v2, ttkbootstrap does not invent a new color model.

Instead, it:

- formalizes semantic color usage,
- documents consistent styling patterns,
- centralizes theme-defined palettes,
- and integrates color behavior cleanly with widgets, layout, and application structure.

This allows developers to focus on **design intent**, while ttkbootstrap handles resolution and consistency.

---

## What This Section Does Not Cover

This page does not include:

- widget-specific styling examples,
- complete token lists,
- theme creation tutorials,
- or application code.

Those topics are covered in:

- **Guides → Theming & Appearance**
- **Reference → Color Tokens**
- **Widgets → Styling Conventions**

---

## Summary

The ttkbootstrap color system encourages you to think in terms of **meaning**, not values.

By using semantic tokens, variants, and modifiers:

- your UI remains consistent,
- your application adapts naturally to different themes,
- and your styling decisions scale as the project grows.

Understanding this model will make the rest of ttkbootstrap easier to use—and harder to misuse.
