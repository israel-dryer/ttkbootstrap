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
ttk.Button(app, text="Delete", bootstyle="danger")
```

The theme resolves `"danger"` to appropriate colors. Change the theme, and all `"danger"` widgets update.

---

## Bootstyle Tokens

The `bootstyle` parameter accepts semantic color tokens:

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
ttk.Button(app, text="Save", bootstyle="primary")
ttk.Button(app, text="Cancel", bootstyle="secondary")
ttk.Button(app, text="Delete", bootstyle="danger")
```

### On Any Widget

Most widgets accept `bootstyle`:

```python
ttk.Label(app, text="Success!", bootstyle="success")
ttk.Progressbar(app, bootstyle="info")
ttk.Entry(app, bootstyle="warning")
```

---

## Variants

Some widgets support **variant** modifiers:

| Variant | Effect |
|---------|--------|
| `outline` | Border only, no fill |
| `link` | Text-only, like a hyperlink |
| `toggle` | Switch-style for checkbuttons |

Combine color and variant:

```python
ttk.Button(app, text="Learn More", bootstyle="info-link")
ttk.Button(app, text="Options", bootstyle="secondary-outline")
ttk.CheckButton(app, text="Enable", bootstyle="success-toggle")
```

### Button Variants

```python
# Solid (default)
ttk.Button(app, text="Primary", bootstyle="primary")

# Outline
ttk.Button(app, text="Primary", bootstyle="primary-outline")

# Link
ttk.Button(app, text="Primary", bootstyle="primary-link")
```

### Toggle Variant

For checkbuttons and radiobuttons:

```python
ttk.CheckButton(app, text="Dark Mode", bootstyle="toggle")
ttk.CheckButton(app, text="Notifications", bootstyle="success-toggle")
```

!!! link "Variants Reference"
    See [Design System → Variants](../design-system/variants.md) for all combinations.

---

## Themes

Themes define **how tokens become colors**.

### Built-in Themes

ttkbootstrap includes many themes:

**Light themes:** `cosmo`, `flatly`, `journal`, `litera`, `lumen`, `minty`, `pulse`, `sandstone`, `united`, `yeti`

**Dark themes:** `cyborg`, `darkly`, `solar`, `superhero`, `vapor`

### Setting a Theme

```python
app = ttk.App(theme="darkly")
```

### Changing at Runtime

```python
from ttkbootstrap import set_theme, toggle_theme

# Set specific theme
set_theme("superhero")

# Toggle between light and dark variants
toggle_theme()
```

All widgets update automatically.

### Theme-Aware Styling

Semantic tokens adapt to the theme:

```python
# "primary" is blue in cosmo, teal in minty
ttk.Button(app, text="Go", bootstyle="primary")
```

Same code, different appearance per theme.

!!! link "Custom Themes"
    See [Design System → Custom Themes](../design-system/custom-themes.md) for creating themes.

---

## Consistent Patterns

### Color Coding by Intent

```python
# Actions
ttk.Button(form, text="Submit", bootstyle="primary")
ttk.Button(form, text="Cancel", bootstyle="secondary")
ttk.Button(form, text="Delete", bootstyle="danger")

# Status
ttk.Label(status_bar, text="Connected", bootstyle="success")
ttk.Label(status_bar, text="Warning: Low disk", bootstyle="warning")
ttk.Label(status_bar, text="Error", bootstyle="danger")
```

### Progress Indicators

```python
# Normal progress
ttk.Progressbar(app, value=50, bootstyle="primary")

# Success state
ttk.Progressbar(app, value=100, bootstyle="success")

# Warning state
ttk.Progressbar(app, value=90, bootstyle="warning")
```

### Form Validation

```python
# Normal state
entry = ttk.Entry(app)

# Error state
entry.configure(bootstyle="danger")

# Success state
entry.configure(bootstyle="success")
```

---

## Typography

ttkbootstrap uses semantic typography where supported:

```python
# Heading style
ttk.Label(app, text="Settings", font=("Helvetica", 16, "bold"))

# Body text (default)
ttk.Label(app, text="Configure your preferences below.")

# Caption/small text
ttk.Label(app, text="Last updated: Today", font=("Helvetica", 10))
```

Font choices should come from the design system, not hardcoded values.

!!! link "Typography"
    See [Design System → Typography](../design-system/typography.md) for guidelines.

---

## Icons

Icons reinforce meaning alongside color:

```python
ttk.Button(app, text="Save", bootstyle="primary", image=save_icon, compound="left")
ttk.Button(app, text="Delete", bootstyle="danger", image=trash_icon, compound="left")
```

Icons and bootstyle work together—use `danger` styling with a warning/delete icon.

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
grid.add(ttk.Label(grid, text="Username:"))
grid.add(ttk.Entry(grid), sticky="ew")

grid.add(ttk.Label(grid, text="Email:"))
grid.add(ttk.Entry(grid), sticky="ew")

grid.add(ttk.Label(grid, text="Role:"))
grid.add(ttk.OptionMenu(grid, values=["User", "Admin", "Guest"]), sticky="ew")

# Toggles
toggles = ttk.PackFrame(form, direction="vertical", gap=5)
toggles.pack(fill="x", pady=(15, 0))

toggles.add(ttk.CheckButton(toggles, text="Email notifications", bootstyle="toggle"))
toggles.add(ttk.CheckButton(toggles, text="Two-factor auth", bootstyle="success-toggle"))

# Actions
actions = ttk.PackFrame(form, direction="horizontal", gap=10)
actions.pack(anchor="e", pady=(20, 0))

actions.add(ttk.Button(actions, text="Cancel", bootstyle="secondary-outline"))
actions.add(ttk.Button(actions, text="Save Changes", bootstyle="primary"))

app.mainloop()
```

---

## Common Mistakes

### Avoid Hardcoded Colors

```python
# Bad
label.configure(foreground="#ff0000")

# Good
label.configure(bootstyle="danger")
```

### Don't Mix Semantic and Literal

```python
# Bad: inconsistent
ttk.Button(app, text="OK", bootstyle="success")
ttk.Button(app, text="Cancel", background="gray")  # Won't work with ttk

# Good: consistent
ttk.Button(app, text="OK", bootstyle="success")
ttk.Button(app, text="Cancel", bootstyle="secondary")
```

### Use Appropriate Tokens

```python
# Bad: using "danger" for non-destructive action
ttk.Button(app, text="Next", bootstyle="danger")

# Good: using appropriate token
ttk.Button(app, text="Next", bootstyle="primary")
```

---

## Summary

- Use **bootstyle tokens** for semantic coloring
- Use **variants** (outline, link, toggle) for style modifications
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
