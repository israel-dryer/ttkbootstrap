---
title: Theming
---

# Theming

This guide explains how ttkbootstrap's theming system works—palettes, color generation, and creating custom themes.

---

## How Themes Work

A theme defines the **complete color system** for your application. Instead of hardcoding colors, you work with semantic tokens (`primary`, `danger`, etc.) that resolve to actual colors based on the active theme.

```python
import ttkbootstrap as ttk

# Theme determines what "primary" means
app = ttk.App(theme="ocean-light")

# Same code, different colors per theme
ttk.Button(app, text="Submit", color="primary")
```

---

## Theme Structure

Every theme defines:

| Property | Purpose |
|----------|---------|
| `name` | Unique identifier (e.g., `"ocean-light"`) |
| `display_name` | Human-readable name (e.g., `"Ocean Light"`) |
| `mode` | `"light"` or `"dark"` |
| `foreground` | Default text color |
| `background` | Default surface color |
| `shades` | Base color palette (blue, red, green, etc.) |
| `semantic` | Role mappings (primary → cyan[600]) |

### Shades: The Color Palette

Shades define the raw colors available to the theme:

```json
{
  "shades": {
    "blue": "#0d6efd",
    "red": "#dc3545",
    "green": "#198754",
    "yellow": "#ffc107",
    "cyan": "#0dcaf0",
    "teal": "#20c997",
    "orange": "#fd7e14",
    "purple": "#6f42c1",
    "pink": "#d63384",
    "indigo": "#6610f2",
    "gray": "#adb5bd"
  }
}
```

From each shade, ttkbootstrap generates a **full spectrum** of 9 variants:

```
blue[100] → lightest tint
blue[200]
blue[300]
blue[400]
blue[500] → base color
blue[600]
blue[700]
blue[800]
blue[900] → darkest shade
```

### Semantic: Role Mappings

Semantic tokens map abstract roles to specific shades:

```json
{
  "semantic": {
    "primary": "cyan[600]",
    "secondary": "blue[600]",
    "success": "teal[600]",
    "info": "blue[600]",
    "warning": "yellow[600]",
    "danger": "red[600]",
    "light": "gray[100]",
    "dark": "gray[900]"
  }
}
```

This indirection is powerful:

- Light themes typically use `[600]` shades for contrast
- Dark themes typically use `[400]` shades for visibility
- Changing `"primary": "cyan[600]"` to `"primary": "blue[600]"` rebrands the entire app

---

## Built-in Themes

ttkbootstrap includes paired light/dark themes:

| Theme Family | Light | Dark |
|--------------|-------|------|
| Bootstrap | `bootstrap-light` | `bootstrap-dark` |
| Ocean | `ocean-light` | `ocean-dark` |
| Forest | `forest-light` | `forest-dark` |
| Rose | `rose-light` | `rose-dark` |
| Amber | `amber-light` | `amber-dark` |
| Aurora | `aurora-light` | `aurora-dark` |
| Classic | `classic-light` | `classic-dark` |

### Listing Available Themes

```python
import ttkbootstrap as ttk

app = ttk.App()

# Get all registered themes
themes = ttk.get_themes()
for theme in themes:
    print(f"{theme['name']}: {theme['display_name']}")
```

---

## Switching Themes

### At Startup

```python
app = ttk.App(theme="ocean-dark")
```

### At Runtime

```python
from ttkbootstrap import set_theme, toggle_theme, get_theme

# Switch to a specific theme
set_theme("forest-light")

# Toggle between light and dark
toggle_theme()

# Check current theme
current = get_theme()
print(f"Current theme: {current}")
```

### Theme Toggle Button

```python
import ttkbootstrap as ttk

app = ttk.App(theme="ocean-light")

def on_toggle():
    ttk.toggle_theme()

ttk.Button(app, text="Toggle Dark Mode", command=on_toggle).pack(pady=20)

app.mainloop()
```

---

## Light and Dark Aliases

ttkbootstrap provides `"light"` and `"dark"` aliases that resolve to configured themes:

```python
# These are equivalent when ocean-light is configured as the light theme
app = ttk.App(theme="light")
app = ttk.App(theme="ocean-light")
```

Configure aliases in your app settings (see [App Settings](#configuring-theme-preferences)).

---

## Creating Custom Themes

### Theme JSON Format

Create a JSON file with the theme structure:

```json
{
  "name": "my-theme-light",
  "display_name": "My Theme Light",
  "mode": "light",
  "foreground": "#212529",
  "background": "#f8f9fa",
  "white": "#ffffff",
  "black": "#000000",
  "shades": {
    "blue": "#0066cc",
    "red": "#cc3333",
    "green": "#339933",
    "yellow": "#ffcc00",
    "cyan": "#00cccc",
    "teal": "#009999",
    "orange": "#ff9900",
    "purple": "#9933cc",
    "pink": "#cc3399",
    "indigo": "#6633cc",
    "gray": "#999999"
  },
  "semantic": {
    "primary": "blue[500]",
    "secondary": "gray[600]",
    "success": "green[500]",
    "info": "cyan[500]",
    "warning": "yellow[500]",
    "danger": "red[500]",
    "light": "gray[100]",
    "dark": "gray[900]"
  }
}
```

### Paired Light and Dark Themes

For a complete theme, create both variants. The key differences:

**Light theme:**

- `mode`: `"light"`
- `foreground`: dark color (e.g., `"#212529"`)
- `background`: light color (e.g., `"#f8f9fa"`)
- `semantic` uses `[500]` or `[600]` shades

**Dark theme:**

- `mode`: `"dark"`
- `foreground`: light color (e.g., `"#f8f9fa"`)
- `background`: dark color (e.g., `"#1a1a1a"`)
- `semantic` uses `[400]` shades for visibility

### Example: Corporate Brand Theme

```json
{
  "name": "acme-light",
  "display_name": "Acme Light",
  "mode": "light",
  "foreground": "#1a1a2e",
  "background": "#fafafa",
  "white": "#ffffff",
  "black": "#000000",
  "shades": {
    "blue": "#0066ff",
    "red": "#e63946",
    "green": "#2a9d8f",
    "yellow": "#e9c46a",
    "cyan": "#00b4d8",
    "teal": "#14b8a6",
    "orange": "#f4a261",
    "purple": "#7c3aed",
    "pink": "#ec4899",
    "indigo": "#4f46e5",
    "gray": "#6b7280"
  },
  "semantic": {
    "primary": "blue[500]",
    "secondary": "gray[500]",
    "success": "green[500]",
    "info": "cyan[500]",
    "warning": "orange[500]",
    "danger": "red[500]",
    "light": "gray[100]",
    "dark": "gray[900]"
  }
}
```

---

## Registering Custom Themes

```python
from ttkbootstrap.style.theme_provider import register_user_theme

# Register before creating the App
register_user_theme("acme-light", "path/to/acme-light.json")
register_user_theme("acme-dark", "path/to/acme-dark.json")

# Now use the theme
app = ttk.App(theme="acme-light")
```

---

## Configuring Theme Preferences

Configure default themes when creating the App:

```python
app = ttk.App(
    theme="light",  # Start with light theme
    light_theme="ocean-light",  # "light" alias resolves to this
    dark_theme="ocean-dark",    # "dark" alias resolves to this
)
```

With this configuration:

- `theme="light"` uses `ocean-light`
- `theme="dark"` uses `ocean-dark`
- `toggle_theme()` switches between them

---

## Color Spectrum Generation

When you define a shade like `"blue": "#0d6efd"`, ttkbootstrap generates the full spectrum:

```
blue[100] ← 80% tint (lightest)
blue[200] ← 60% tint
blue[300] ← 40% tint
blue[400] ← 25% tint
blue[500] ← base color
blue[600] ← 25% shade
blue[700] ← 40% shade
blue[800] ← 60% shade
blue[900] ← 85% shade (darkest)
```

This means you only define 11 base colors, and the system generates 99 usable shades.

### Accessing Generated Colors

```python
from ttkbootstrap import get_theme_provider

provider = get_theme_provider()

# Access any generated color
primary_500 = provider.colors["primary[500]"]
blue_300 = provider.colors["blue[300]"]
```

---

## Theme-Aware Code

### Checking Theme Mode

```python
from ttkbootstrap import get_theme_provider

provider = get_theme_provider()

if provider.mode == "dark":
    # Dark mode specific logic
    pass
else:
    # Light mode specific logic
    pass
```

### Responding to Theme Changes

```python
import ttkbootstrap as ttk

app = ttk.App()

def on_theme_changed():
    current = ttk.get_theme()
    print(f"Theme changed to: {current}")
    # Update any theme-dependent state

# Listen for theme changes
app.bind("<<ThemeChanged>>", lambda e: on_theme_changed())
```

---

## Best Practices

### 1. Always Create Paired Themes

If you create `my-theme-light`, also create `my-theme-dark`. Users expect dark mode.

### 2. Use Semantic Tokens

Don't hardcode colors. Use `color="primary"` so themes work correctly:

```python
# Good
ttk.Button(app, text="Submit", color="primary")

# Bad - ignores theming
ttk.Button(app, text="Submit", background="#0066cc")
```

### 3. Test Both Modes

Always test your UI in both light and dark modes. Some designs that work in light mode may have contrast issues in dark mode.

### 4. Respect System Preferences

Consider detecting the system's dark mode preference at startup:

```python
import darkdetect

# Start with system preference
initial_theme = "dark" if darkdetect.isDark() else "light"
app = ttk.App(theme=initial_theme)
```

### 5. Keep Semantic Mappings Logical

- `primary` → brand color, main actions
- `secondary` → supporting actions
- `success` → positive outcomes (green family)
- `danger` → destructive actions (red family)
- `warning` → caution (yellow/orange family)
- `info` → informational (blue family)

---

## Summary

- Themes define **shades** (raw colors) and **semantic** mappings (role → shade)
- Each shade generates a **9-step spectrum** automatically
- Use `set_theme()` and `toggle_theme()` for runtime switching
- Create custom themes as **JSON files** with paired light/dark variants
- Always use **semantic tokens** (`color` and `variant`) instead of hardcoded colors

!!! link "Styling Guide"
    See [Styling](styling.md) for using color and variant tokens in widgets.

!!! link "Color Modifiers"
    See [Styling → Color Modifiers](styling.md#color-modifiers) for adjusting colors dynamically.

---

## Next Steps

- [Styling](styling.md) — using color and variant tokens
- [Typography](typography.md) — font tokens and modifiers
- [App Structure](app-structure.md) — application organization
