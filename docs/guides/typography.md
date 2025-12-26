---
title: Typography
---

# Typography

This guide shows how to use ttkbootstrap's typography system—font tokens, modifiers, and the `Font` class for creating reusable named fonts.

---

## Font Tokens

ttkbootstrap defines **semantic font tokens** rather than raw font tuples. Tokens represent typographic roles:

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

### Using Tokens Directly

Tokens are registered as named Tk fonts, so you can use them directly:

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Body text", font="body").pack()
ttk.Label(app, text="Large heading", font="heading-lg").pack()
ttk.Label(app, text="Code snippet", font="code").pack()

app.mainloop()
```

Tokens adapt to the platform—using Segoe UI on Windows, SF Pro on macOS, and DejaVu Sans on Linux.

---

## The Font Class

The `Font` class provides a powerful way to create fonts with modifiers:

```python
from ttkbootstrap import Font

# Create a font from a token
body_font = Font("body")

# Create a font with modifiers
bold_body = Font("body[bold]")

# Use in widgets
ttk.Label(app, text="Bold text", font=bold_body)
```

The `Font` class:

- Parses a string syntax for tokens and modifiers
- Creates and caches named Tk fonts
- Can be passed directly to any widget's `font` parameter

---

## Modifier Syntax

Modifiers are specified in **chained brackets** after the token name:

!!! note "Consistent Syntax"
    Font modifiers use the same chained bracket syntax as [color modifiers](styling.md#color-modifiers). This consistency makes both systems easy to learn together.

```python
# Single modifier
Font("body[bold]")
Font("body[italic]")
Font("body[underline]")

# Multiple modifiers (chained brackets)
Font("body[bold][italic]")
Font("body[14][bold][underline]")
Font("heading-lg[18][bold][italic]")
```

Available modifiers:

| Modifier | Effect |
|----------|--------|
| `bold` | Bold weight |
| `normal` | Normal weight |
| `italic` | Italic style |
| `roman` | Remove italic |
| `underline` | Underlined text |
| `overstrike` | Strikethrough text |
| `14` | Absolute size (14pt) |
| `16px` | Absolute size in pixels |

### Size in Brackets

Specify absolute size as a bracketed modifier:

```python
Font("body[14]")              # Force 14pt
Font("body[16][bold]")        # 16pt bold
Font("body[16px]")            # Force 16 pixels
Font("heading-lg[24][italic]") # 24pt italic heading
```

### Size Delta with +/-

Adjust size relative to the token's base size using `+` or `-` before the brackets:

```python
Font("body+1")              # 1 point larger than body
Font("body-2")              # 2 points smaller than body
Font("heading-lg+2[bold]")  # 2 points larger than heading-lg, bold
Font("caption-1[italic]")   # 1 point smaller than caption, italic
```

### Modifier Pipeline

Modifiers are applied left-to-right as a pipeline. For the same property, later values override earlier ones:

```python
Font("body[bold][normal]")   # Results in normal weight
Font("body[14][16]")         # Results in 16pt
```

### Complete Examples

```python
from ttkbootstrap import Font

# Common patterns
title_font = Font("heading-xl")
subtitle_font = Font("heading-lg[normal]")  # Heading size, normal weight
body_font = Font("body")
emphasis_font = Font("body[bold][italic]")
code_font = Font("code")
small_caption = Font("caption[italic]")

# Size variations using +/-
large_body = Font("body+2")
compact_label = Font("body-1")

# Size with modifiers
large_bold = Font("body+2[bold]")
custom_heading = Font("heading-lg[18][italic]")

# Decoration
link_text = Font("body[underline]")
deleted_text = Font("body[overstrike]")
emphasized_link = Font("body[bold][underline]")
```

---

## Using Fonts in Widgets

Pass `Font` objects directly to widgets:

```python
import ttkbootstrap as ttk
from ttkbootstrap import Font

app = ttk.App()

# Define fonts
title = Font("heading-xl")
body = Font("body")
code = Font("code")

# Apply to widgets
ttk.Label(app, text="Welcome", font=title).pack(pady=10)
ttk.Label(app, text="This is body text.", font=body).pack()
ttk.Label(app, text="print('Hello')", font=code).pack(pady=10)

app.mainloop()
```

### Inline Font Strings

Many widgets also accept the font string directly:

```python
ttk.Label(app, text="Bold heading", font="heading-lg[bold]")
ttk.Label(app, text="Italic caption", font="caption[italic]")
```

---

## Creating Named Fonts

For fonts you'll reuse across your application, create them once and reference by name:

```python
from ttkbootstrap import Font

# Create reusable fonts at app startup
class AppFonts:
    title = Font("heading-xl")
    subtitle = Font("heading-lg[normal]")
    body = Font("body")
    body_bold = Font("body[bold]")
    caption = Font("caption[italic]")
    code = Font("code")

# Use throughout the application
ttk.Label(app, text="Title", font=AppFonts.title)
ttk.Label(app, text="Description", font=AppFonts.body)
```

### Accessing the Underlying Tk Font

The `Font` class wraps a Tk named font:

```python
font = Font("body[bold]")

# Get the Tk font object
tk_font = font.tkfont

# Get the registered font name
name = font.name  # e.g., "ttkbootstrap.font.abc123"

# Font can be used as a string (returns name)
str(font)  # Same as font.name
```

---

## Font Measurement

The `Font` class provides measurement utilities:

```python
from ttkbootstrap import Font

font = Font("body")

# Measure text width in pixels
width = font.measure("Hello, World!")

# Get font metrics
metrics = font.metrics()
# Returns: {'ascent': 12, 'descent': 3, 'linespace': 15, 'fixed': 0}

# Get actual font properties
actual = font.actual()
# Returns: {'family': 'Segoe UI', 'size': 11, 'weight': 'normal', ...}
```

### Practical Uses

```python
# Calculate required widget width
text = "This is a long label"
font = Font("body")
required_width = font.measure(text) + 20  # Add padding

ttk.Label(app, text=text, font=font, width=required_width)

# Get line height for layout calculations
line_height = font.metrics()["linespace"]
```

---

## Typography Registry

For advanced use, access the typography system directly:

```python
from ttkbootstrap.style.typography import Typography, FontSpec

# Get a token's specification
spec = Typography.get_token("heading-lg")
print(spec.font, spec.size, spec.weight)

# Update a token globally
Typography.update_font_token("body", size=12)

# Change the global font family
Typography.set_global_family("Arial")
```

### Available Token Names

```python
from ttkbootstrap.style.typography import FontTokenNames

# Access token name constants
FontTokenNames.body       # "body"
FontTokenNames.heading_lg # "heading-lg"
FontTokenNames.code       # "code"
```

---

## Common Patterns

### Consistent Headings

```python
from ttkbootstrap import Font

# Define heading hierarchy
h1 = Font("heading-xl")
h2 = Font("heading-lg")
h3 = Font("heading-md")
h4 = Font("body-lg[bold]")

ttk.Label(app, text="Main Title", font=h1).pack()
ttk.Label(app, text="Section", font=h2).pack()
ttk.Label(app, text="Subsection", font=h3).pack()
ttk.Label(app, text="Minor Heading", font=h4).pack()
```

### Form Labels and Values

```python
label_font = Font("body[bold]")
value_font = Font("body")

grid = ttk.GridFrame(app, columns=2, gap=10, padding=20)

grid.add(ttk.Label(grid, text="Name:", font=label_font))
grid.add(ttk.Label(grid, text="Alice", font=value_font))

grid.add(ttk.Label(grid, text="Email:", font=label_font))
grid.add(ttk.Label(grid, text="alice@example.com", font=value_font))
```

### Code Display

```python
code_font = Font("code")
line_number_font = Font("code[bold]")

# Code editor style
ttk.Label(app, text="1", font=line_number_font)
ttk.Label(app, text="def hello():", font=code_font)
```

### Status Messages

```python
normal_status = Font("caption")
error_status = Font("caption[bold]")
success_status = Font("caption[italic]")

def show_status(message, level="normal"):
    fonts = {
        "normal": normal_status,
        "error": error_status,
        "success": success_status,
    }
    status_label.configure(text=message, font=fonts[level])
```

---

## Summary

- Use **font tokens** (`body`, `heading-lg`, `code`) for semantic typography
- Use the **`Font` class** to create fonts with modifiers
- Specify **modifiers in brackets**: `Font("body[bold][italic]")`
- Adjust **size with +/-**: `Font("body+2")` or `Font("body[14]")`
- **Reuse fonts** by creating them once and referencing throughout
- Use **`measure()`** and **`metrics()`** for layout calculations

!!! link "Design System"
    See [Design System → Typography](../design-system/typography.md) for the design philosophy.

---

## Next Steps

- [Styling](styling.md) — working with the design system
- [Layout](layout.md) — building layouts with containers
- [App Structure](app-structure.md) — how applications are organized
