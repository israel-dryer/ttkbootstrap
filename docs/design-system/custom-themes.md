---
title: Custom Themes
---

# Custom Themes

Custom themes redefine how the design system is rendered without changing
application code. A theme maps semantic tokens to concrete visual values that
all widgets consume.

---

## Theme properties

Every theme is defined by the following properties:

| Property | Purpose |
|----------|---------|
| `name` | Unique identifier used in code (e.g. `"ocean-light"`) |
| `display_name` | Human-readable label (e.g. `"Ocean Light"`) |
| `mode` | `"light"` or `"dark"` |
| `foreground` | Default text color |
| `background` | Default surface color |
| `white` | Pure white reference |
| `black` | Pure black reference |
| `shades` | Base color palette |
| `semantic` | Role mappings from semantic tokens to palette values |

---

## Shades

Shades define the raw color palette available to a theme.

Each shade is a named base color (e.g. `"blue"`, `"red"`). From each base,
ttkbootstrap generates a **9-step spectrum** of tints and shades:

| Step | Meaning |
|------|---------|
| `[100]` | Lightest tint |
| `[200]–[400]` | Progressively darker tints |
| `[500]` | Base color |
| `[600]–[800]` | Progressively darker shades |
| `[900]` | Darkest shade |

A theme defines 11 base colors and the system produces 99 usable palette
values automatically.

Standard shade names: `blue`, `red`, `green`, `yellow`, `cyan`, `teal`,
`orange`, `purple`, `pink`, `indigo`, `gray`.

---

## Semantic tokens

Semantic tokens map abstract color roles to palette values.

| Token | Conventional role |
|-------|-------------------|
| `primary` | Brand color and main actions |
| `secondary` | Supporting actions |
| `success` | Positive outcomes |
| `info` | Informational |
| `warning` | Caution |
| `danger` | Destructive actions |
| `light` | Light surface accent |
| `dark` | Dark surface accent |

Each token maps to a shade step, e.g. `"primary": "cyan[600]"`. Light themes
typically use `[500]`–`[600]` steps for foreground contrast; dark themes
typically use `[400]` steps for visibility on dark backgrounds.

---

## Built-in themes

ttkbootstrap ships paired light/dark themes:

| Family | Light | Dark |
|--------|-------|------|
| Bootstrap | `bootstrap-light` | `bootstrap-dark` |
| Ocean | `ocean-light` | `ocean-dark` |
| Forest | `forest-light` | `forest-dark` |
| Rose | `rose-light` | `rose-dark` |
| Amber | `amber-light` | `amber-dark` |
| Aurora | `aurora-light` | `aurora-dark` |
| Classic | `classic-light` | `classic-dark` |

---

## Creating and using custom themes

For the JSON format, how to register themes, runtime switching, and
theme-aware patterns, see:

- [Guides → Theming](../guides/theming.md)

For styling widgets with semantic tokens, see:

- [Guides → Styling](../guides/styling.md)

---

## Related concepts

- [Design System → Colors](colors.md)
- [Design System → Typography](typography.md)
- [Design System → Icons](icons.md)
- [API Reference → Style](../reference/style/index.md)
