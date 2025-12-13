---
icon: fontawesome/solid/font
---

# Typography

ttkbootstrap 2 defines named font tokens (for example `body`, `heading-md`, `display-xl`, `code`) so you can assign a shared font via `font="body"` and keep widgets, dialogs, and tables in sync. Every widget that supports the `font` option includes the `FontMixin`, which understands modifier syntax and applies updates without creating new Tk `Font` objects.

## Named font tokens

The tokens correspond to familiar text roles (body copy, headings, badges, code) and reuse the configured font families and sizes:

- Body text: `body-xl`, `body-lg`, `body`, `body-sm`.
- Headings: `heading-xl`, `heading-lg`, `heading-md` plus the display tokens `display-xl` and `display-lg` for emphasis.
- Auxiliary text: `label`, `caption`, `code`, and `hyperlink` cover badges, annotations, monospaced snippets, and link-style underlines.

## FontMixin and modifiers

FontMixin lets you tweak the current token in the constructor by appending bracketed modifiers. Examples:

- `Label(..., font="body[bold]")` makes the token bold for that widget only.
- `Button(..., font="heading-lg[italic]")` combines a heading token with italic styling.
- `Entry(..., font="[14][underline]")` keeps the widget's current family while adjusting size and decoration.

Modifier strings can chain (`"heading-lg[italic][overstrike]"`), use size aliases (`xs`, `sm`, `md`, `lg`, `xl`, `xxl`), or set explicit pixel values (`[12px]`). Missing components inherit from the current font, so you only override the attributes you care about.

## Updating tokens at runtime

Call `Typography.update_font_token("body", weight="bold")` or `Typography.set_global_family("Inter")` to adjust tokens across the app. The change propagates to every widget that references the token, keeping typography consistent without touching each widget individually.

## Quick reference card

| Token | Usage | Notes |
| --- | --- | --- |
| `body-xl` | `Label(..., font="body-xl")` | Larger base text for cards or callouts. |
| `body-lg` | `Label(..., font="body-lg")` | Slightly bigger paragraphs or section text. |
| `body` | `Label(..., font="body")` | Default paragraphs and entry text. |
| `body-sm` | `Label(..., font="body-sm")` | Metadata, helper text, or tertiary copy. |
| `heading-xl` | `Label(..., font="heading-xl")` | Main section titles and hero headings. |
| `heading-lg` | `Dialog(..., font="heading-lg")` | Panel titles and card headers. |
| `heading-md` | `Frame(..., font="heading-md")` | Secondary headings and emphasis text. |
| `display-xl` | `Label(..., font="display-xl")` | Showcase or hero typography. |
| `display-lg` | `Label(..., font="display-lg")` | Prominent labels or stats. |
| `label` | `Badge(..., font="label")` | Small emphasis text, badges, or chip labels. |
| `caption` | `Label(..., font="caption")` | Tiny annotations, helper copy, or captions. |
| `code` | `Text(..., font="code")` | Monospaced snippets and console-style output. |
| `hyperlink` | `Label(..., font="hyperlink")` | Underlined link text with accent decoration. |

| Modifier | Example | Effect |
| --- | --- | --- |
| Size alias | `font="[lg]"` | Switches to a preset size (lg = 14pt) without touching the token. |
| Weight | `font="[bold]"` | Applies bold weight. |
| Slant | `font="[italic]"` | Applies italic styling. |
| Decorations | `font="[underline,overstrike]"` | Adds underline and overstrike. |
| Pixel size | `font="[16px]"` | Locks the font height to the given pixel size. |

Combining shared tokens with FontMixin modifiers keeps text aligned with the design system while allowing case-by-case tweaks right where widgets are constructed.
