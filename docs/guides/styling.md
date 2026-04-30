---
title: Styling
---

# Styling

This guide explains how to control the appearance of widgets in
ttkbootstrap. The framework is built around a small set of semantic
tokens — `accent`, `variant`, `surface`, and `density` — that every
themable widget understands. Compose those tokens at construction time
and the active theme decides how they render.

This page is a tour of the styling vocabulary. For deeper references,
see:

- [Design System → Colors](../design-system/colors.md) — what the
  semantic colors mean.
- [Design System → Variants](../design-system/variants.md) — emphasis
  hierarchy.
- [Theming](theming.md) — themes, palettes, and runtime switching.
- [Custom Themes](../design-system/custom-themes.md) — full theme
  vocabulary.

---

## Style by intent, not by value

ttkbootstrap styling is **intent-based**. Widgets express what they
*mean* (a primary action, a danger state, an informational status),
and the active theme decides how that intent renders.

```python
# Don't do this
button.configure(background="#dc3545", foreground="white")

# Do this
ttk.Button(app, text="Delete", accent="danger")
```

The advantages compound:

- The same widget code works in light and dark themes.
- Switching themes restyles every widget at once — no recoloring.
- Meaning is declared at the call site, not buried in literal hex.

---

## The four tokens

Every themable widget in ttkbootstrap accepts up to four styling
tokens. Most pages only mention the ones they support, but the
vocabulary is consistent across the framework.

| Token | Controls | Example values |
|-------|----------|----------------|
| `accent` | Semantic color (intent) | `"primary"`, `"success"`, `"danger"` |
| `variant` | Visual emphasis | `"solid"`, `"outline"`, `"ghost"`, `"link"` |
| `surface` | Container background | `"content"`, `"chrome"`, `"card"`, `"overlay"` |
| `density` | Spacing tightness | `"default"`, `"compact"` |

Combine them as constructor keyword arguments:

```python
ttk.Button(app, text="Save", accent="primary")                            # solid is default
ttk.Button(app, text="Cancel", accent="secondary", variant="outline")
ttk.Button(app, text="Compact", accent="primary", density="compact")
ttk.Frame(app, surface="card", padding=20)
```

---

## Accent

The `accent` parameter sets the semantic color. Every theme defines
the same set of intents:

| Token | Intent |
|-------|--------|
| `primary` | Main action, brand color |
| `secondary` | Supporting action |
| `success` | Positive outcome, confirmation |
| `info` | Informational |
| `warning` | Caution, attention needed |
| `danger` | Destructive action, error |
| `light` | Light surface or text |
| `dark` | Dark surface or text |

Accent applies to almost every widget — buttons, labels, progress
bars, entries, frames:

```python
ttk.Button(app, text="Save", accent="primary")
ttk.Label(app, text="Connected", accent="success")
ttk.Progressbar(app, accent="info", value=60)
ttk.Entry(app, accent="warning")
```

For the meaning behind each token and how themes resolve them, see
[Design System → Colors](../design-system/colors.md).

---

## Variant

`variant` controls visual emphasis — how prominent a widget appears
relative to others. Variants are widget-specific because not every
emphasis level makes sense for every control.

### Button variants

`Button` (and any widget that inherits its styling, like
`MenuButton`) supports:

| Variant | Effect |
|---------|--------|
| `solid` | Filled background (the default). |
| `outline` | Border only, transparent fill. |
| `ghost` | No border or fill until hover. |
| `link` | Text-only with link affordances. |
| `text` | Lowest-emphasis flat text button. |

```python
ttk.Button(app, text="Primary", accent="primary")                        # solid
ttk.Button(app, text="Outline", accent="primary", variant="outline")
ttk.Button(app, text="Ghost",   accent="primary", variant="ghost")
ttk.Button(app, text="Link",    accent="primary", variant="link")
```

### Other widgets

Several widget families have their own variant vocabulary:

| Widget | Variants |
|--------|----------|
| `Badge` | `square`, `pill` |
| `CheckButton` | `default`, `round`, `square` |
| `Progressbar` | `default`, `striped`, `thin` |
| `Tabs`, `TabView` | `pill`, `bar` |
| `ToggleGroup` | `outline`, `ghost` |

See each widget's reference page for its full list.

### Toggles and switches are separate widgets

`CheckButton` does **not** have a `"toggle"` variant. Toggle-style
controls are dedicated widgets:

```python
# Toggle button (looks like a button, behaves like a checkbox)
ttk.CheckToggle(app, text="Notifications", accent="success")

# iOS-style switch
ttk.Switch(app, text="Dark mode")
```

For the design rationale and emphasis hierarchy across variants, see
[Design System → Variants](../design-system/variants.md).

---

## Surface

`surface` sets a frame's background using a semantic surface token.
Each token is a flat name — the theme decides the actual color and
adjusts it for light vs. dark mode.

| Token | Use for |
|-------|---------|
| `content` | The main page or canvas background (default). |
| `chrome` | Application chrome — sidebars, toolbars, navigation. |
| `card` | Slightly elevated surface — cards, panels. |
| `overlay` | Floating UI — menus, dialogs, popups. |
| `input` | Recessed input fields. |

```python
ttk.Frame(app, surface="content")    # main content area
ttk.Frame(app, surface="chrome")     # sidebar / toolbar
ttk.Frame(app, surface="card", padding=20, show_border=True)
```

Children of a surface inherit the surface's foreground colors
automatically. Setting `surface=` on a parent frame is enough to
restyle nested labels, buttons, and inputs to match.

### Frame borders

Frames support `show_border=True` for a theme-aware rounded outline.
The border color is derived from the active theme so it adapts to
light and dark modes:

```python
card = ttk.Frame(app, surface="card", show_border=True, padding=20)
card.pack(padx=20, pady=20)
```

---

## Density

`density` sets the spacing tightness for widgets that support it
(buttons, entries, fields, tables, toolbars, menu items). Two values:

| Value | Effect |
|-------|--------|
| `default` | Comfortable spacing tuned for desktop UI (default). |
| `compact` | Tighter padding and slightly smaller fonts. |

```python
# Roomy default
ttk.Button(app, text="Save", accent="primary")

# Compact for dense forms or toolbars
ttk.Button(app, text="Save", accent="primary", density="compact")
ttk.Toolbar(app, density="compact")
```

Use `compact` selectively — typically for toolbars, data tables, and
inspector panes — not as a global setting. Mixing densities in a
single visual region looks inconsistent.

---

## Per-instance overrides

The same tokens accepted at construction can be applied later with
`configure()`:

```python
entry = ttk.Entry(app)

# Show validation feedback without rebuilding the widget
entry.configure(accent="danger")    # error
entry.configure(accent="success")   # valid
entry.configure(accent=None)        # reset to neutral
```

This is the recommended pattern for reactive styling — switching
emphasis in response to user input, async results, or signal
updates.

---

## Themes and runtime switching

Themes are what map every token to a concrete color. The same
`accent="primary"` resolves to a different hex value under each
theme. Set the theme at startup, or switch it at runtime:

```python
import ttkbootstrap as ttk

# Set at startup
app = ttk.App(theme="ocean-dark")

# Switch at runtime
ttk.set_theme("forest-light")

# Toggle between configured light and dark themes
ttk.toggle_theme()

# Read the active theme
current = ttk.get_theme()
```

For theme structure, the built-in themes, and creating custom themes,
see [Theming](theming.md).

---

## Going beyond the four tokens

For most UI work, `accent`, `variant`, `surface`, and `density` are
all you need. When you need a specific shade of a color — for custom
chart palettes, annotation strips, or data-visualization layers — the
theme provider exposes the full color spectrum.

### Color tokens with modifiers

Color tokens accept chained bracket modifiers:

```python
"primary"                # base accent color
"primary[100]"           # specific shade (50–950 in 50-step increments)
"primary[subtle]"        # tinted for backgrounds
"primary[muted]"         # reduced contrast for text
"foreground[muted]"      # secondary text
"primary[100][muted]"    # chained: light shade, then muted
```

| Modifier | Purpose |
|----------|---------|
| `[N]` (numeric) | Pick a specific shade in the 50–950 spectrum. |
| `[+N]` / `[-N]` | Lighten or darken relative to the base. |
| `[subtle]` | Subdued tint for backgrounds and selection. |
| `[muted]` | Reduced-contrast foreground for secondary text. |

These tokens can be passed to any widget parameter that accepts a
color (e.g. a `font` color override, or a custom drawing canvas):

```python
from ttkbootstrap import get_theme_color

bg = get_theme_color("primary[subtle]")
fg = get_theme_color("foreground[muted]")
```

For the full color system, see
[Design System → Colors](../design-system/colors.md) and
[Theming](theming.md).

---

## Custom ttk styles

When the token system isn't expressive enough — typically because
you need to override a specific ttk option that doesn't have a
corresponding token — drop down to `ttk.Style`. This is the standard
Tkinter API, exposed through ttkbootstrap's singleton:

```python
import ttkbootstrap as ttk

app = ttk.App()
style = ttk.Style()

# Configure a custom ttk style name
style.configure(
    "Custom.TButton",
    padding=(20, 10),
    font="heading-md",
)

# Map state-dependent options
style.map(
    "Custom.TButton",
    foreground=[("active", "white")],
)

# Apply by ttk style name
ttk.Button(app, text="Custom", style="Custom.TButton").pack()

# Inspect resolved options
padding = style.lookup("Custom.TButton", "padding")

app.mainloop()
```

The Style instance is a singleton — calling `ttk.Style()` always
returns the same object — so configuration applied anywhere is
visible everywhere. The convenience helper `ttk.get_style()` returns
the same instance.

Use this only as an escape hatch. Token-driven styling stays in sync
with theme changes automatically; raw `Style.configure()` calls do
not, and you'll have to re-apply them on a `<<ThemeChanged>>` event
if you need them to follow the theme.

---

## Typography and icons

Font and icon styling have their own dedicated tokens. They follow
the same intent-based model — pick a token like `body`, `heading-lg`,
or `caption`, and the theme handles the rest:

```python
ttk.Label(app, text="Settings", font="heading-xl")
ttk.Label(app, text="Last updated: today", font="caption")
ttk.Button(app, text="Save", accent="primary", icon="save")
```

For details, see:

- [Typography](typography.md) — font tokens, modifiers, custom fonts.
- [Design System → Icons](../design-system/icons.md) — icon usage.

---

## Padding and spacing

Padding is a Tk option, not a ttkbootstrap-specific token, but it
plays into the visual rhythm of styled widgets. Define spacing
constants once and reuse them so the rhythm stays consistent:

```python
SPACING_SM = 5
SPACING_MD = 10
SPACING_LG = 20

ttk.Button(app, text="Compact", padding=(SPACING_SM, 2))
ttk.Frame(app, padding=SPACING_LG)
ttk.PackFrame(app, gap=SPACING_MD, padding=SPACING_LG)
```

For layout-level spacing primitives (`gap`, `padx`/`pady`), see
[Layout](layout.md) and
[Spacing and Alignment](spacing-and-alignment.md).

---

## A styled form

A short example bringing the tokens together:

```python
import ttkbootstrap as ttk

app = ttk.App(theme="flatly")

form = ttk.LabelFrame(app, text="User Settings", padding=20)
form.pack(padx=20, pady=20, fill="x")

grid = ttk.GridFrame(form, columns=["auto", 1], gap=(10, 8))
grid.pack(fill="x")

ttk.Label(grid, text="Username:").grid()
ttk.Entry(grid).grid(sticky="ew")

ttk.Label(grid, text="Email:").grid()
ttk.Entry(grid).grid(sticky="ew")

ttk.Label(grid, text="Role:").grid()
ttk.OptionMenu(grid, options=["User", "Admin", "Guest"]).grid(sticky="ew")

toggles = ttk.PackFrame(form, direction="vertical", gap=5)
toggles.pack(fill="x", pady=(15, 0))

ttk.CheckToggle(toggles, text="Email notifications").pack()
ttk.CheckToggle(toggles, text="Two-factor auth", accent="success").pack()

actions = ttk.PackFrame(form, direction="horizontal", gap=10)
actions.pack(anchor="e", pady=(20, 0))

ttk.Button(actions, text="Cancel", accent="secondary", variant="outline").pack()
ttk.Button(actions, text="Save Changes", accent="primary").pack()

app.mainloop()
```

---

## What not to do

### Don't hardcode colors

```python
# Bad
label.configure(foreground="#ff0000")

# Good
label.configure(accent="danger")
```

Hardcoded hex values bypass the theme entirely — they don't switch
with the theme, don't adapt to dark mode, and don't compose with
other styled widgets.

### Don't reach for raw Tk options on ttk widgets

```python
# Bad — has no effect on most ttk widgets
ttk.Button(app, text="Cancel", background="gray")

# Good — token-driven
ttk.Button(app, text="Cancel", accent="secondary", variant="outline")
```

ttk widgets ignore most direct color options (`background`,
`foreground`). Use tokens, or `ttk.Style().configure()` for true
ttk-level overrides.

### Don't misuse semantic intents

```python
# Bad — "danger" reads as destructive, not "next step"
ttk.Button(app, text="Next", accent="danger")

# Good
ttk.Button(app, text="Next", accent="primary")
```

Pick the token that matches what the widget *means*. Misusing
`danger` or `success` for visual variety undermines accessibility and
breaks the meaning every other widget in the app is establishing.

### Don't use `bootstyle=`

The legacy `bootstyle` parameter is deprecated. New code should use
`accent` and `variant` directly. Existing `bootstyle="primary-outline"`
still works for migration, but emits a deprecation warning.

---

## Next steps

- [Theming](theming.md) — palettes, built-in themes, custom themes.
- [Typography](typography.md) — font tokens.
- [Layout](layout.md) — building layouts with containers.
- [Reactivity](reactivity.md) — signals and reactive updates.
