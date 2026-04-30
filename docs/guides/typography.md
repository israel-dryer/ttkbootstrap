---
title: Typography
---

# Typography

This guide is the practical reference for typography in a ttkbootstrap
application: how to choose a font for a widget, how to vary it (bold, italic,
size), and how to keep typography consistent across an app.

For the underlying token vocabulary (the table of token names and their
intended roles) see [Design System → Typography](../design-system/typography.md).
This guide assumes that vocabulary and focuses on what application code does
with it.

---

## The mental model

Don't pick a font family. Pick a **role**.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Settings", font="heading-lg").pack()
ttk.Label(app, text="Configure your preferences below.", font="body").pack()
ttk.Label(app, text="Last saved 2 minutes ago", font="caption").pack()

app.mainloop()
```

Tokens like `body`, `heading-lg`, and `caption` are registered as named Tk
fonts at app startup. They resolve to platform-appropriate families (Segoe UI
on Windows, SF Pro Text on macOS, DejaVu Sans on Linux) and a size scale tuned
for desktop UIs. You write the role; the framework picks the font.

This separation is the entire point. Application code stays platform-neutral
and visually consistent; the typography registry decides how each role looks.

---

## Using tokens

Anywhere a Tk widget accepts a `font=` option, ttkbootstrap accepts a token
name as a string:

```python
ttk.Label(app, text="Title", font="heading-xl")
ttk.Label(app, text="Body text", font="body")
ttk.Label(app, text="def hello(): ...", font="code")
```

The full token table is in
[Design System → Typography](../design-system/typography.md). At a glance:

- **Reading**: `caption`, `body-sm`, `body`, `body-lg`, `body-xl`
- **UI labels**: `label` (bold)
- **Headings**: `heading-sm`, `heading-md`, `heading-lg`, `heading-xl`
- **Display**: `display-lg`, `display-xl`
- **Specialty**: `code` (monospace), `hyperlink` (underlined)

---

## Modifiers: tweaking a token without abandoning it

When you need a slight variation — bold, italic, two points larger — use
modifiers in chained brackets after the token name. The result is still
anchored to the token, so it adapts when the registry's family or scale
changes.

```python
ttk.Label(app, text="Emphasis", font="body[bold]")
ttk.Label(app, text="Quote", font="body[italic]")
ttk.Label(app, text="Bold and italic", font="body[bold][italic]")
ttk.Label(app, text="Strikethrough", font="body[overstrike]")
```

### Sizing

Two ways to set size, with different intent:

```python
# Relative: stays anchored to the token's base size.
# When the registry's base size changes, this tracks it.
"body+1"        # one point larger than body
"caption-1"     # one point smaller than caption

# Absolute: pins a specific size in the bracket.
# Useful when you need a fixed visual size regardless of the token scale.
"body[14]"      # 14 points
"body[16px]"    # 16 pixels
```

Prefer the relative form unless you have a reason to pin an absolute size.
Relative offsets keep the design system in sync; absolute sizes opt out of it.

### Modifier reference

| Modifier | Effect |
|----------|--------|
| `bold` | Bold weight |
| `normal` | Normal weight |
| `italic` | Italic style |
| `roman` | Remove italic |
| `underline` | Underlined text |
| `overstrike` | Strikethrough |
| `N` | Absolute size in points (e.g. `14`) |
| `Npx` | Absolute size in pixels (e.g. `16px`) |

When the same property appears more than once, the last value wins:

```python
"body[bold][normal]"   # normal weight
"body[14][16]"         # 16 points
```

The same chained-bracket syntax also drives color modifiers — see
[Styling → Color Modifiers](styling.md#color-modifiers) for the parallel.

---

## The `Font` class

For fonts you create once and reuse, wrap the string in `Font`. It parses the
expression once, caches the resulting Tk named font, and gives you the same
object to pass everywhere.

```python
import ttkbootstrap as ttk
from ttkbootstrap import Font

app = ttk.App()

heading = Font("heading-lg")
emphasis = Font("body[bold][italic]")

ttk.Label(app, text="Hello", font=heading).pack()
ttk.Label(app, text="Important note", font=emphasis).pack()
ttk.Label(app, text="More with same heading", font=heading).pack()

app.mainloop()
```

Strings and `Font` instances are interchangeable wherever a `font=` argument
is accepted. Use the string form for one-offs; use `Font` when the same
expression appears multiple times or when you want measurement utilities.

### Measurement

`Font` exposes Tk's measurement API on the resolved font:

```python
from ttkbootstrap import Font

body = Font("body")

body.measure("Hello, World!")   # pixel width of the rendered string
body.metrics()                  # {'ascent': ..., 'descent': ..., 'linespace': ..., 'fixed': ...}
body.actual()                   # {'family': ..., 'size': ..., 'weight': ..., ...}
```

These are useful for layout decisions where you need to size a widget around
its text — for example, sizing a column to fit the longest expected value, or
laying out a custom canvas.

---

## Patterns

### A small "design tokens" module

For a real app, the most common pattern is to declare your typography choices
in one place and import them everywhere. This makes the design easier to
adjust later — change one file, the whole app updates.

```python
import ttkbootstrap as ttk
from ttkbootstrap import Font

# fonts.py — design tokens for the app
class AppFonts:
    page_title = Font("display-lg")
    section = Font("heading-lg")
    body = Font("body")
    body_emphasis = Font("body[bold]")
    caption = Font("caption")
    code = Font("code")

app = ttk.App()
ttk.Label(app, text="Welcome", font=AppFonts.page_title).pack()
ttk.Label(app, text="Getting started", font=AppFonts.section).pack()
ttk.Label(app, text="Read the introduction below.", font=AppFonts.body).pack()
ttk.Label(app, text="Updated 2 minutes ago", font=AppFonts.caption).pack()
app.mainloop()
```

### Form labels

The `label` token is intentionally bold and slightly smaller than `body` —
it's the form-field label voice:

```python
import ttkbootstrap as ttk

app = ttk.App()

form = ttk.GridFrame(app, columns=2, gap=10, padding=20)
form.pack()

ttk.Label(form, text="Name", font="label").grid()
ttk.Entry(form).grid()

ttk.Label(form, text="Email", font="label").grid()
ttk.Entry(form).grid()

app.mainloop()
```

### Heading hierarchy

Reach for headings in size order. If you need an extra step you can bridge
with bracket-modified body sizes:

```python
import ttkbootstrap as ttk
from ttkbootstrap import Font

app = ttk.App()

ttk.Label(app, text="Document Title", font=Font("display-lg")).pack()
ttk.Label(app, text="Section", font=Font("heading-lg")).pack()
ttk.Label(app, text="Subsection", font=Font("heading-md")).pack()
ttk.Label(app, text="Minor heading", font=Font("body[bold]")).pack()

app.mainloop()
```

---

## Customizing the typography registry

Most apps don't need to touch the registry — the defaults are tuned for
desktop UIs across all three platforms. If you do need to override family or
size globally, the controls live on `Typography`:

```python
from ttkbootstrap.style.typography import Typography

# Replace the UI font family for every non-monospace token.
Typography.set_global_family("Inter")

# Tweak a single token's size while keeping its family and weight.
Typography.update_font_token("body", size=12)
```

These calls update the registered Tk fonts in place. Widgets that already
reference a token by name (`font="body"`) re-render automatically. Widgets
that hold a derived `Font` object instantiated *before* the change keep their
original metrics — re-create them after global changes if you need them to
follow.

`Typography.set_global_family` deliberately leaves `code` alone so monospace
keeps working when the app font changes.

For the underlying primitives (`FontSpec`, `FontTokens`, `FontTokenNames`,
`build_desktop_tokens`) see the API reference.

---

## Related guides

- [Design System → Typography](../design-system/typography.md) — token
  vocabulary, intent, and scale.
- [Styling](styling.md) — color tokens and the parallel modifier syntax.
- [Layout](layout.md) — composing typography with `PackFrame` and
  `GridFrame`.
