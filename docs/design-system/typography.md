---
title: Typography
---

# Typography

Typography in ttkbootstrap is defined through **font tokens** rather than
individual font selections.

Font tokens describe *intent*—such as body text or headings—while the framework
handles platform-appropriate rendering.

---

## Typography tokens

Common typography tokens include:

- `body` — standard UI text
- `heading` — section and view titles
- `caption` — secondary or supporting text
- `monospace` — code or aligned data

Themes determine the concrete font families and sizes for each token.

---

## Modifiers

Typography tokens can be modified conceptually:

- weight (bold)
- style (italic)
- size adjustments

Modifiers express emphasis without breaking consistency.

---

## Why tokens matter

Using typography tokens ensures:

- consistent text hierarchy
- predictable scaling across platforms
- centralized control
- accessibility-friendly defaults

---

## Using typography in applications

How typography is applied in widgets and layouts is covered in:

- [Guides → Typography](../guides/typography.md)

Typography APIs and implementation details are documented in:

- [API Reference → Font](../reference/utils/Font.md)

---

## Related concepts

- [Design System → Colors](colors.md)
- [Design System → Variants](variants.md)
