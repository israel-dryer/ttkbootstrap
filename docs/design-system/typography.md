---
title: Typography
---

# Typography

Typography in ttkbootstrap is defined through **font tokens** rather than
individual font selections.

Font tokens describe *intent* — such as body text or headings — while the
framework handles platform-appropriate rendering.

---

## Font tokens

Tokens are registered as named Tk fonts. Use them directly as a `font`
parameter value:

| Token | Purpose |
|-------|---------|
| `caption` | Small supporting text |
| `label` | Bold label text (form labels, field labels) |
| `body-sm` | Compact body text |
| `body` | Default body text |
| `body-lg` | Larger body text |
| `body-xl` | Extra large body text |
| `heading-md` | Medium heading |
| `heading-lg` | Large heading |
| `heading-xl` | Extra large heading |
| `display-lg` | Large display text |
| `display-xl` | Extra large display text |
| `code` | Monospace code text |
| `hyperlink` | Underlined link text |

Themes map each token to a concrete font family, size, and weight. Tokens
adapt automatically to the platform (Segoe UI on Windows, SF Pro on macOS,
DejaVu Sans on Linux).

---

## Modifiers

Tokens can be modified without breaking consistency. Modifiers are expressed
in chained brackets after the token name:

| Modifier | Effect |
|----------|--------|
| `bold` | Bold weight |
| `normal` | Normal weight |
| `italic` | Italic style |
| `roman` | Remove italic |
| `underline` | Underlined |
| `overstrike` | Strikethrough |
| `N` | Absolute size in points (e.g. `14`) |
| `Npx` | Absolute size in pixels (e.g. `16px`) |

Size can also be adjusted relative to the token's base using `+N` or `-N`
before the brackets (e.g. `body+2`, `caption-1`).

---

## Using typography in applications

How font tokens and the `Font` class are applied in widgets and layouts:

- [Guides → Typography](../guides/typography.md)

Font API documentation:

- [API Reference → Font](../reference/utils/Font.md)

---

## Related concepts

- [Design System → Colors](colors.md)
- [Design System → Variants](variants.md)
