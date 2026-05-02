---
title: Typography
---

# Typography

Typography tokens are named Tk fonts that ship pre-registered on every
`App`. You write `font="body"` or `font="heading-lg[italic]"`; the
framework resolves the token through the active theme to a
platform-appropriate family and size.

The token system has two layers:

1. **A registry of 14 named font tokens** — base sizes for body text,
   labels, headings, displays, code, and hyperlinks. Each token
   is a real Tk named font, so `font="body"` works directly anywhere
   Tk accepts a font.
2. **An inline modifier syntax** that adjusts size, weight, and style
   without forking a new token. `body[bold]`, `heading-lg[italic]`,
   `caption[14][underline]` are all valid widget kwargs.

## Token catalog

Each token is registered as a Tk named font when the App initializes.
Sizes are in points; weights are `normal` or `bold`.

| Token | Default size (relative to base) | Weight | Purpose |
|---|---|---|---|
| `caption` | base − 2 | normal | Small supporting text |
| `label` | base − 2 | bold | Form labels, field labels |
| `body-sm` | base − 1 | normal | Compact body text |
| `body` | base | normal | Default body text |
| `body-lg` | base + 1 | normal | Slightly larger body text |
| `body-xl` | base + 2 | normal | Larger body text |
| `heading-sm` | base − 1 | bold | Smallest heading |
| `heading-md` | base | bold | Medium heading |
| `heading-lg` | base + 1 | bold | Large heading |
| `heading-xl` | base + 2 | bold | Extra large heading |
| `display-lg` | base + 4 | bold | Large display text |
| `display-xl` | base + 5 | bold | Extra large display text |
| `code` | base | normal | Monospace (uses the mono family) |
| `hyperlink` | base | normal, underlined | Underlined link text |

The `base` size is platform-dependent: 13 pt on macOS (HIG-aligned),
11 pt elsewhere. The font *family* is also platform-tuned —
`Segoe UI` on Windows, `SF Pro Text` on macOS, `DejaVu Sans` on Linux,
with `Cascadia Mono` / `SF Mono` / `DejaVu Sans Mono` as the
monospace counterpart for `code`.

Tk's standard named fonts are also remapped to the token system at App
init: `TkDefaultFont` and `TkTextFont` resolve to `body`,
`TkHeadingFont` to `heading-md`, `TkCaptionFont` to `caption`, and
`TkFixedFont` to `code`. Existing code that uses `font='TkDefaultFont'`
keeps working and picks up the token-based theme font automatically.

## Inline modifier syntax

You can attach modifiers to any token (or to no token at all) via
square-bracket notation. The framework parses `font='<token>[mods]'`
at the widget kwarg boundary and substitutes the resolved Tk font
tuple before passing it to Tk.

| Modifier | What it does | Example |
|---|---|---|
| `bold` | Sets weight bold | `body[bold]` |
| `normal` | Sets weight normal (cancel inherited bold) | `heading-md[normal]` |
| `italic` | Sets slant italic | `body[italic]` |
| `roman` | Sets slant roman (cancel italic) | `body[roman]` |
| `underline` | Underlines | `body[underline]` |
| `overstrike` | Strikethrough (aliases: `strike`, `strikethrough`) | `body[overstrike]` |
| `N` (digits) | Absolute point size | `body[16]` |
| `Npx` | Absolute pixel size (Tk's negative-size convention) | `body[16px]` |
| `xs`, `sm`, `md`, `lg`, `xl`, `xxl` | Size tokens (8 / 10 / 12 / 14 / 16 / 18 pt) | `body[lg]` |
| `+N` / `-N` (before brackets) | Relative size delta on the token's base | `body+2`, `caption-1` |

Multiple modifiers chain inside one or more bracket groups, and a
single bracket can contain a comma- or space-separated list:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Typography")
ttk.Label(app, text="Default body").pack(padx=20, pady=4)
ttk.Label(app, text="Bold body", font="body[bold]").pack(padx=20, pady=4)
ttk.Label(app, text="Italic body", font="body[italic]").pack(padx=20, pady=4)
ttk.Label(app, text="Bold italic", font="body[bold,italic]").pack(padx=20, pady=4)
ttk.Label(app, text="Underlined link", font="hyperlink").pack(padx=20, pady=4)
ttk.Label(app, text="Larger body", font="body+2").pack(padx=20, pady=4)
ttk.Label(app, text="Heading, italic", font="heading-lg[italic]").pack(padx=20, pady=4)
app.mainloop()
```

The bracket head is optional. `font="[14][bold]"` defaults to the
`body` token and overrides only the size and weight. The full grammar
also accepts a literal family name in place of a token —
`font="Helvetica[16][bold]"` skips the token system and renders with
the named family directly.

!!! note "Unknown tokens fall through silently"
    `font="not-a-real-token"` does **not** raise — Tk receives the
    string verbatim, fails to find a matching named font, and falls
    back to its default font with no warning. If a label silently
    renders in the wrong font, double-check the token spelling. The
    framework intercepts and validates only when modifiers are
    present (i.e. `font="not-a-real-token[bold]"` parses through the
    modifier path and resolves correctly to a `body[bold]`-style
    fallback).

## The `Font` class

For programmatic font construction or measurement, use `ttk.Font`:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Font class")
f = ttk.Font("body[bold]")

print(f.name)               # the resolved Tk font name string
print(f.measure("Hello"))   # pixel width of "Hello" in this font
print(f.actual())           # full Tk font dict

# Pass to widgets directly
ttk.Label(app, text="Bold body", font=f).pack(padx=20, pady=20)
app.mainloop()
```

`Font` accepts the same modifier syntax as the inline `font="..."`
kwarg. The resolved Tk font is cached per spec, so reusing the same
expression doesn't repeatedly re-create the underlying named font.

`Font.measure(text)`, `Font.metrics(...)`, and `Font.actual(...)`
forward to the underlying Tk font, useful for layout calculations
that need exact pixel widths (custom canvas labels, dynamic column
widths in TreeView, etc.).

## Per-app font customization

`Typography.set_global_family(family)` swaps every UI token to a
single family without touching the monospace `code` token:

```python
import ttkbootstrap as ttk
from ttkbootstrap.style.typography import Typography

app = ttk.App(title="Custom family")
Typography.set_global_family("Inter")
ttk.Label(app, text="Now in Inter", font="body").pack(padx=20, pady=20)
app.mainloop()
```

`Typography.update_font_token(name, **kwargs)` adjusts a single token
in place — change `body` to use a larger base size while keeping
everything else at its default scale.

For full theming integration (changing fonts as part of a custom
theme), see [Custom Themes](custom-themes.md).

## When to use a token vs a literal

Use a **token** (`body`, `heading-lg`, etc.) when the text is part
of the application UI — labels, headings, body copy, status messages.
Tokens adapt to the platform and respect any per-app font
customization.

Use the **modifier syntax** when you need a quick variant of a token
— a bold `body`, an italic `caption`, an underlined link. The
result is still a derived named Tk font, so you keep platform
adaptation.

Use a **literal family** (`"Helvetica[16]"`) only when you need a
specific font that doesn't fit the token system — typically display
typography, branded marketing text, or a deliberate one-off in a
diagram or chart. Literal families bypass theming.

Avoid raw Tk font tuples (`("Helvetica", 16, "bold")`) outside of
custom widget code. The string-based syntax is the canonical
interface — it's parseable, theme-aware, and round-trips through
`cget('font')` in a stable form.

## Where to read next

- The token vocabulary that pairs with `font`:
  [Colors](colors.md).
- The `Font` class API: [API Reference → Font](../reference/utils/Font.md).
- Application-level font workflows:
  [Guides → Typography](../guides/typography.md).
- Defining custom fonts in a theme: [Custom Themes](custom-themes.md).
