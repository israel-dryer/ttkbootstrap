---
title: Styling
---

# Styling

This guide explains how to work with ttkbootstrap's design system—semantic colors, variants, and consistent styling across widgets.

---

## Design System Thinking

ttkbootstrap styling is **intent-based**, not value-based.

Instead of:

```python
# Don't do this
button.configure(background="#dc3545", foreground="white")
```

Use semantic tokens:

```python
# Do this
ttk.Button(app, text="Delete", accent="danger")
```

The theme resolves `"danger"` to appropriate colors. Change the theme, and all `"danger"` widgets update.

---

## Accent Tokens

The `accent` parameter accepts semantic color tokens:

| Token | Intent |
|-------|--------|
| `primary` | Main action, brand color |
| `secondary` | Supporting action |
| `success` | Positive outcome, confirmation |
| `info` | Informational |
| `warning` | Caution, attention needed |
| `danger` | Destructive action, error |
| `light` | Light background/text |
| `dark` | Dark background/text |

### Basic Usage

```python
ttk.Button(app, text="Save", accent="primary")
ttk.Button(app, text="Cancel", accent="secondary")
ttk.Button(app, text="Delete", accent="danger")
```

### On Any Widget

Most widgets accept `accent`:

```python
ttk.Label(app, text="Success!", accent="success")
ttk.Progressbar(app, accent="info")
ttk.Entry(app, accent="warning")
```

---

## Color Modifiers

Colors support **chained bracket modifiers** for dynamic adjustments:

```python
# Elevation adjustments
"background[+1]"      # One level lighter/elevated
"background[-1]"      # One level darker/recessed
"primary[+2]"         # Two levels lighter

# Shade selection
"primary[100]"        # Lightest shade
"primary[500]"        # Base shade
"primary[900]"        # Darkest shade

# Semantic modifiers
"primary[subtle]"     # Subdued version for backgrounds
"primary[muted]"      # Muted foreground with good contrast

# Chained modifiers (applied left to right)
"primary[100][muted]" # Light primary shade, then muted
"background[+1][subtle]" # Elevated background, then subtle
```

### Elevation

Elevation modifiers adjust lightness relative to the base color:

```python
# Common patterns
"background[+1]"  # Raised surface (cards, dialogs)
"background[+2]"  # Higher elevation (tooltips, menus)
"background[-1]"  # Recessed area (wells, insets)
```

### Shades

Shade modifiers select from the color's palette:

```python
# Primary color shades
"primary[50]"   # Lightest
"primary[100]"
"primary[200]"
"primary[300]"
"primary[400]"
"primary[500]"  # Base color
"primary[600]"
"primary[700]"
"primary[800]"
"primary[900]"  # Darkest
```

### Subtle and Muted

Semantic modifiers for common UI patterns:

| Modifier | Purpose |
|----------|---------|
| `subtle` | Subdued background tint—good for hover states, selection highlights |
| `muted` | Low-contrast foreground—good for secondary text, disabled states |

```python
# Subtle backgrounds
"primary[subtle]"   # Tinted background for primary context
"success[subtle]"   # Light green background for success states
"danger[subtle]"    # Light red background for error states

# Muted text
"foreground[muted]" # Secondary text color
"primary[muted]"    # Subdued primary-colored text
```

### Modifier Pipeline

Modifiers are applied left-to-right as a pipeline:

```python
# Step by step:
"primary[100][muted]"
# 1. Look up primary[100] (light primary shade)
# 2. Apply muted (reduce contrast for text)

"background[+1][subtle]"
# 1. Look up background
# 2. Elevate by +1
# 3. Apply subtle treatment
```

---

## Variants

Widgets support **variant** modifiers to control visual emphasis:

| Variant | Effect |
|---------|--------|
| `solid` | Filled background (default) |
| `outline` | Border only, no fill |
| `ghost` | Minimal chrome, subtle hover |
| `link` | Text-only, like a hyperlink |

Use `accent` and `variant` together:

```python
ttk.Button(app, text="Learn More", accent="info", variant="link")
ttk.Button(app, text="Options", accent="secondary", variant="outline")
ttk.CheckButton(app, text="Enable", accent="success", variant="toggle")
```

### Button Variants

```python
# Solid (default)
ttk.Button(app, text="Primary", accent="primary")

# Outline
ttk.Button(app, text="Primary", accent="primary", variant="outline")

# Link
ttk.Button(app, text="Primary", accent="primary", variant="link")
```

### Toggle Variant

For checkbuttons and radiobuttons:

```python
ttk.CheckButton(app, text="Dark Mode", variant="toggle")
ttk.CheckButton(app, text="Notifications", accent="success", variant="toggle")
```

!!! link "Variants Reference"
    See [Design System → Variants](../design-system/variants.md) for all combinations.

---

## Themes

Themes define **how tokens become colors**. The same `accent="primary"` resolves to different colors depending on the active theme.

```python
# Set theme at startup
app = ttk.App(theme="ocean-dark")

# Switch themes at runtime
from ttkbootstrap import set_theme, toggle_theme
set_theme("forest-light")
toggle_theme()  # Toggle between light and dark
```

!!! link "Theming Guide"
    See [Theming](theming.md) for theme structure, built-in themes, and creating custom themes.

---

## Consistent Patterns

### Accent Coding by Intent

```python
# Actions
ttk.Button(form, text="Submit", accent="primary")
ttk.Button(form, text="Cancel", accent="secondary")
ttk.Button(form, text="Delete", accent="danger")

# Status
ttk.Label(status_bar, text="Connected", accent="success")
ttk.Label(status_bar, text="Warning: Low disk", accent="warning")
ttk.Label(status_bar, text="Error", accent="danger")
```

### Progress Indicators

```python
# Normal progress
ttk.Progressbar(app, value=50, accent="primary")

# Success state
ttk.Progressbar(app, value=100, accent="success")

# Warning state
ttk.Progressbar(app, value=90, accent="warning")
```

### Form Validation

```python
# Normal state
entry = ttk.Entry(app)

# Error state
entry.configure(accent="danger")

# Success state
entry.configure(accent="success")
```

---

## Typography

ttkbootstrap uses semantic typography where supported:

```python
# Heading style
ttk.Label(app, text="Settings", font="heading-xl")

# Body text (default)
ttk.Label(app, text="Configure your preferences below.")

# Caption/small text
ttk.Label(app, text="Last updated: Today", font="caption")
```

Font choices should come from the design system, not hardcoded values.

!!! link "Typography"
    See [Typography](typography.md) to learn how to use ttkbootstrap typography.

---

## Icons

Icons reinforce meaning alongside color:

```python
ttk.Button(app, text="Save", accent="primary", image=save_icon, compound="left")
ttk.Button(app, text="Delete", accent="danger", image=trash_icon, compound="left")
```

Icons and color work together—use `danger` styling with a warning/delete icon.

!!! link "Icons"
    See [Design System → Icons](../design-system/icons.md) for icon usage.

---

## Padding and Spacing

### Widget Padding

```python
ttk.Button(app, text="Compact", padding=(5, 2))
ttk.Button(app, text="Roomy", padding=(20, 10))
```

### Container Padding

```python
ttk.Frame(app, padding=20)
ttk.PackFrame(app, padding=(20, 10), gap=15)
```

### Consistent Spacing

Use consistent values throughout:

```python
SPACING_SM = 5
SPACING_MD = 10
SPACING_LG = 20

ttk.PackFrame(app, gap=SPACING_MD, padding=SPACING_LG)
```

---

## Example: Styled Form

```python
import ttkbootstrap as ttk

app = ttk.App(theme="flatly")

# Form container
form = ttk.LabelFrame(app, text="User Settings", padding=20)
form.pack(padx=20, pady=20, fill="x")

# Form grid
grid = ttk.GridFrame(form, columns=["auto", 1], gap=(10, 8))
grid.pack(fill="x")

# Fields
ttk.Label(grid, text="Username:").grid()
ttk.Entry(grid).grid(sticky="ew")

ttk.Label(grid, text="Email:").grid()
ttk.Entry(grid).grid(sticky="ew")

ttk.Label(grid, text="Role:").grid()
ttk.OptionMenu(grid, values=["User", "Admin", "Guest"]).grid(sticky="ew")

# Toggles
toggles = ttk.PackFrame(form, direction="vertical", gap=5)
toggles.pack(fill="x", pady=(15, 0))

ttk.CheckButton(toggles, text="Email notifications", variant="toggle").pack()
ttk.CheckButton(toggles, text="Two-factor auth", accent="success", variant="toggle").pack()

# Actions
actions = ttk.PackFrame(form, direction="horizontal", gap=10)
actions.pack(anchor="e", pady=(20, 0))

ttk.Button(actions, text="Cancel", accent="secondary", variant="outline").pack()
ttk.Button(actions, text="Save Changes", accent="primary").pack()

app.mainloop()
```

---

## Common Mistakes

### Avoid Hardcoded Colors

```python
# Bad
label.configure(foreground="#ff0000")

# Good
label.configure(accent="danger")
```

### Don't Mix Semantic and Literal

```python
# Bad: inconsistent
ttk.Button(app, text="OK", accent="success")
ttk.Button(app, text="Cancel", background="gray")  # Won't work with ttk

# Good: consistent
ttk.Button(app, text="OK", accent="success")
ttk.Button(app, text="Cancel", accent="secondary")
```

### Use Appropriate Tokens

```python
# Bad: using "danger" for non-destructive action
ttk.Button(app, text="Next", accent="danger")

# Good: using appropriate token
ttk.Button(app, text="Next", accent="primary")
```

---

## Summary

- Use **accent tokens** for semantic coloring
- Use **variant** (outline, link, ghost) for style modifications
- Change **themes** to update all widgets at once
- Maintain **consistency** with reusable spacing constants
- Let the **design system** handle the details

!!! link "Design System"
    See [Design System](../design-system/index.md) for the complete reference.

---

## Next Steps

- [App Structure](app-structure.md) — how applications are organized
- [Layout](layout.md) — building layouts with containers
- [Reactivity](reactivity.md) — signals and reactive updates