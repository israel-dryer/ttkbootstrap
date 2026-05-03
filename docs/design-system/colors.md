---
title: Colors
---

# Colors

Color tokens are how widget code talks about color without naming a hex
value. You write `accent="primary"` or `surface="card"`; the active theme
maps the token to a concrete color, and the same widget code adapts when
the theme changes.

This page lists every token the framework defines, the two kwarg axes
that consume them (`accent` and `surface`), and the modifier syntax for
deriving variants of an existing token.

## Token catalog

| Family | Tokens | What they mean |
|---|---|---|
| Brand semantics | `primary`, `secondary`, `success`, `info`, `warning`, `danger`, `light`, `dark` | Action-color intent. Themes map each to a shade. |
| Surface tokens | `chrome`, `content`, `card`, `overlay`, `input` | Container backgrounds at five elevations. Derived per-theme from `background`. |
| On-surface foregrounds | `on_chrome`, `on_content`, `on_card`, `on_overlay`, `on_input` | High-contrast text color for each surface. Computed by `best_foreground`. |
| Muted foregrounds | `on_chrome_secondary`, `on_content_secondary`, `on_card_secondary`, `on_overlay_secondary`, `on_input_secondary` | Lower-contrast secondary text on each surface. |
| Stroke tokens | `stroke`, `stroke_subtle` | Border and divider colors. Derived from `background`. |
| Literals | `foreground`, `background`, `white`, `black` | Theme-defined or absolute. |
| Shades | `blue`, `red`, `green`, `yellow`, `orange`, `cyan`, `teal`, `purple`, `pink`, `indigo`, `gray` | Base color names. Combine with a shade step (`blue[100]`–`blue[900]`) to pull a specific tint. |

A theme JSON file declares the literals (`foreground`, `background`, `white`, `black`),
the shade base values, and the brand-semantic mappings (e.g.
`"primary": "blue[600]"`). Everything else — the surface tokens, the
on-surface foregrounds, the strokes, the 9-step shade spectrum — is
derived automatically from those inputs. See
[Custom Themes](custom-themes.md) for the JSON schema.

## The `accent` and `surface` axes

Most widgets accept color tokens through two distinct kwargs that play
different roles:

| Kwarg | Question it answers | Token family it consumes |
|---|---|---|
| `accent=` | What color is this widget? | Brand semantics (typically `primary` / `success` / `danger`); also any shade or hex |
| `surface=` | What background does this widget sit on? | Surface tokens (`chrome` / `content` / `card` / `overlay` / `input`) |

Action widgets (Button, Toolbutton, MenuButton, CheckButton, RadioButton)
take `accent`. Container widgets (Frame, LabelFrame, Card, Toolbar,
ScrollView) take `surface`. Inputs (TextEntry, NumericEntry, Spinbox,
Combobox) take `surface` for the field background and inherit `accent`
through their built-in chrome.

```python
import ttkbootstrap as ttk

app = ttk.App(title="Tokens")

# accent = the widget's action color
ttk.Button(app, text="Save", accent="primary").pack(pady=5, padx=20)
ttk.Button(app, text="Delete", accent="danger").pack(pady=5, padx=20)

# surface = the container's background elevation
shell = ttk.Frame(app, surface="chrome", padding=10)
shell.pack(fill="x")
ttk.Label(shell, text="Shell chrome").pack()

card = ttk.Card(app, padding=10)  # Card defaults to surface="card"
card.pack(fill="x", padx=20, pady=10)
ttk.Label(card, text="Card content").pack()

app.mainloop()
```

Container widgets are also in `CONTAINER_CLASSES`, which means the
bootstyle wrapper rewrites `accent="primary"` on a `Frame` as
`surface="primary"` — the two kwargs become interchangeable on
containers. On non-container widgets they remain distinct: `accent` is
captured into the resolved style key, `surface` describes the parent
backdrop the widget renders against.

## Modifier syntax

Tokens accept chained modifiers in square brackets. Modifiers apply
left to right as a pipeline:

| Form | Meaning | Example |
|---|---|---|
| `[NNN]` | Shade lookup (digits 100–900). Only meaningful on shade base names. | `blue[300]`, `red[700]` |
| `[+N]` / `[-N]` | Step the color up/down N elevation levels (subtle lighten/darken). | `card[+1]`, `background[+2]` |
| `[subtle]` | Tinted variant for backgrounds or borders. | `primary[subtle]` |
| `[muted]` | Muted foreground at lower contrast (passes the WCAG 4.5:1 minimum). | `primary[muted]` |

Modifiers chain. `background[+1][muted]` elevates the background one
step and then computes a muted foreground against the result; the order
matters because each modifier transforms the running color.

The `[NNN]` shade form only works on **base shade names**
(`blue`, `red`, etc.). It does **not** work on semantic tokens —
`primary[100]` raises `ValueError: Invalid color token`. To pull a
specific tint of a brand color, use the underlying shade
(`blue[300]`) or use a modifier that does work on semantics
(`primary[subtle]`, `primary[+1]`).

## Hex strings pass through

Any token that starts with `#` is returned unchanged:

```python
b = ttk.Style().style_builder
print(b.color("#ff6600"))  # → '#ff6600'
print(b.color("primary"))  # → '#0d6efd' (or whatever the active theme maps it to)
```

Use a hex literal when you need a one-off color that doesn't justify a
new theme token. Hex values do **not** adapt across themes — they
render the same on light and dark, which is occasionally what you want
(brand logo backgrounds, fixed legend colors) but usually isn't.

## Reading the active palette

Every resolved token comes from `Style().style_builder.color(token)`:

```python
import ttkbootstrap as ttk
app = ttk.App(title="probe")
b = ttk.Style().style_builder

print(b.color("primary"))            # the brand primary
print(b.color("card"))               # the card surface
print(b.color("on_card"))            # readable foreground on card
print(b.color("blue[300]"))          # specific shade
print(b.color("background[+1]"))     # one step elevated
```

`color()` raises `ValueError: Invalid color token: '<name>'` for unknown
tokens, with a brief list of valid token families. It accepts hex
strings as a passthrough (anything beginning with `#`).

There is no `border` or `border_subtle` token — use `stroke` and
`stroke_subtle` instead. The error message lists only the brand
semantics; the surface, on-surface, stroke, and shade tokens are valid
but not listed in the error text.

## Theme switching

Token resolution happens at style-build time, and styles invalidate on
`<<ThemeChanged>>`. Switching themes at runtime cascades automatically
through every widget that consumes tokens — no per-widget reconfiguration
required.

```python
import ttkbootstrap as ttk
app = ttk.App(title="Theme switch")
ttk.Button(app, text="Save", accent="primary").pack(padx=20, pady=20)

def to_dark():
    ttk.Style().theme_use("bootstrap-dark")

ttk.Button(app, text="Dark mode", command=to_dark, variant="outline").pack(pady=5)
app.mainloop()
```

The button's `accent="primary"` re-resolves through the dark theme's
`primary` shade automatically. Hex literals embedded directly in widget
code do not — they stay the same across themes by design.

## Theme tokens and icons

Theme tokens (`"primary"`, `"success"`, etc.) in `IconSpec.color` and
per-state color overrides are resolved through the style engine before
reaching PIL. Hex strings and PIL named colors also work directly.

```python
# All three forms are equivalent and correct
ttk.Button(app, icon={"name": "star", "color": "primary"})
ttk.Button(app, icon={"name": "star", "color": "#4D76F6"})
ttk.Button(app, icon={"name": "star"})  # inherits widget foreground
```

See [Capabilities → Icons & Imagery](../capabilities/icons/index.md)
for the full per-state icon override surface.

## Where to read next

- The visual-emphasis axis that composes with `accent`:
  [Variants](variants.md).
- How tokens become ttk styles internally:
  [Platform → Styling Internals](../platform/ttk-styles-elements.md).
- The widget-level kwargs that consume `accent` and `surface`:
  [Widgets → Button](../widgets/actions/button.md),
  [Widgets → Frame](../widgets/layout/frame.md).
- Defining your own palette: [Custom Themes](custom-themes.md).
- Theme switching at the application level:
  [Guides → Theming](../guides/theming.md).
