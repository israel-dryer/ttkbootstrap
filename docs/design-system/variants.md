---
title: Variants
---

# Variants

Variants describe **visual emphasis** — how loud or quiet a control
should appear — and pair with `accent` to produce the rendered look.
Where `accent` answers *which color*, `variant` answers *how much
chrome*.

A solid primary button shouts; an outline primary button asks; a ghost
or link primary button whispers. Same accent, three emphasis levels:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Variants")
for variant in ("solid", "outline", "ghost", "link"):
    ttk.Button(app, text=f"Save ({variant})", accent="primary",
               variant=variant).pack(padx=20, pady=4, fill="x")
app.mainloop()
```

## Per-widget variant catalog

Each ttk widget class registers its own set of variants. Passing an
unregistered variant raises `BootstyleBuilderError: Builder '<name>'
not found for widget class '<class>'` at construction time.

| Widget | Variants | Default | Notes |
|---|---|---|---|
| `Button` | `solid`, `outline`, `ghost`, `link`, `text` | `solid` (alias `default`) | The full emphasis ladder. |
| `MenuButton` | `solid`, `outline`, `ghost`, `text` | `solid` (alias `default`) | No `link` variant. |
| `CheckToggle`, `RadioToggle` | `solid`, `outline`, `ghost` | `solid` (alias `default`) | Toolbutton chrome — no `link` or `text`. |
| `ButtonGroup` | `solid`, `outline`, `ghost` | `solid` (alias `default`) | Variant cascades to children that don't pin their own. |
| `CheckButton` | `default` (the standard checkbox) | `default` | The `switch` variant is for `Switch`, not user-facing here. |
| `Switch` | `switch` | `switch` (auto-set) | A `CheckButton` subclass that hard-codes `variant='switch'`. |
| `RadioButton`, `RadioGroup` | `default` | `default` | No emphasis axis — radios are radios. |
| `Notebook` | `default`, `bar`, `pill`, `tab` | `default` | `default` and `tab` share the chrome; `bar` and `pill` are visually distinct. |
| `Tabs` (TabItem) | `default`, `bar` | `default` | `pill` is in the docstring/signature but not registered — see below. |
| `Badge` | `square`, `pill` | `square` | The shape of the chip. |
| `Progressbar` | `default`, `striped`, `thin` | `default` | `striped` adds a moving stripe pattern; `thin` is half-height. |
| `Scrollbar` | `default`, `round`, `rounded`, `square` | `default` (image-based rounded thumb) | `round` and `rounded` are aliases for the default; `square` is the flat solid path. |
| Everything else | `default` | `default` | Frame, Label, Card, Entry, Combobox, Spinbox, Treeview, ListView, ScrollView, etc. |

The "everything else" row covers the bulk of the widget catalog. Most
widgets aren't visually variant-axed — their look is shaped by `accent`
and `surface` alone, and passing `variant=` at all raises
`BootstyleBuilderError`. If a widget isn't listed above, assume
`default` is the only valid value.

!!! warning "`Tabs(variant='pill')` raises at the first `add()` call"
    The `Tabs` constructor signature lists `'pill'` as a supported
    variant alongside `'bar'`, but no `pill` builder is registered for
    `TabItem.TFrame`. Construction succeeds, then the first `add()`
    raises `BootstyleBuilderError: Builder 'pill' not found for widget
    class 'TabItem.TFrame'. Available variants: default, bar`.

## What each variant does

The intent ladder is the same across widget classes; the rendered
chrome differs by class.

| Variant | Intent | Typical chrome |
|---|---|---|
| `solid` (`default`) | Highest emphasis — primary action of the screen. | Filled background in the accent color; high-contrast foreground. |
| `outline` | Medium emphasis — secondary action. | Transparent background; accent-colored 1 px border and foreground. |
| `ghost` | Low emphasis — tertiary or context action. | Transparent background; accent-colored foreground only. Hover/active produce a faint accent-tinted background. |
| `link` | Inline action that reads as text. | Underlined accent-colored text on a transparent background; no padding/border treatment. |
| `text` | Lowest emphasis — quiet utility action. | Plain accent-colored text without underline; minimum chrome. |
| `bar` (Notebook, Tabs) | Tab strip rendered as a horizontal underline-style bar. | Selected tab is underlined in accent; inactive tabs are muted. |
| `pill` (Notebook) | Tab strip rendered as fully-rounded pills. | Selected pill filled in accent. |
| `striped` (Progressbar) | Animated diagonal stripes. | Visually emphasizes activity vs. a flat fill. |
| `thin` (Progressbar) | Half-height bar. | Lower visual weight in dense layouts. |
| `square` / `pill` (Badge) | Chip shape. | Sharp vs. fully-rounded corners. |
| `square` / `round` (Scrollbar) | Thumb shape. | Solid flat thumb vs. image-based rounded thumb. |

The `solid` variant is the implicit default for most action-emphasis
widgets — passing `variant="default"` and passing `variant="solid"`
produce identical resolved styles. The `outline`/`ghost`/`link`/`text`
ladder is consistent across `Button`, `MenuButton`, and `Toolbutton`
where supported.

## Composition with `accent`

Variants work in combination with `accent`. The same variant on a
different accent produces a different color but the same chrome
treatment:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Accent + variant")
for accent in ("primary", "danger", "success", "secondary"):
    ttk.Button(app, text=f"{accent} outline", accent=accent,
               variant="outline").pack(padx=20, pady=4, fill="x")
app.mainloop()
```

Both axes are construction-time options that end up baked into a
unique resolved style name (`bs[<hash>].<accent>.<variant>.T<Class>`).
Reconfiguring `accent=` after construction works through the standard
`_delegate_accent` path on most widgets and rebuilds the style;
reconfiguring `variant=` is widget-specific and frequently
construction-only — most widgets pin `variant` at construction and
reject runtime changes. See the per-widget pages under
[Widgets](../widgets/index.md) for the configure-time behavior of each
widget's variant.

## When variants are too coarse

Variants are intentionally narrow — they're a five-rung emphasis
ladder, not a full styling vocabulary. If a project needs:

- A specific font weight or size on a button → use `font=` with a
  [typography token](typography.md), not a new variant.
- A custom border color or thickness → use `style_options=` to pin
  builder kwargs (`{'show_border': True}`, `{'border_color': 'stroke'}`),
  not a new variant.
- A different visual identity for one screen → switch the active theme
  for that screen, not the variant.
- A genuinely new control type → register a custom builder. See
  [Platform → Styling Internals](../platform/ttk-styles-elements.md)
  for the registration API.

The deprecated `bootstyle="success-outline"` syntax is decomposed at
construction into `accent="success", variant="outline"` and emits a
`DeprecationWarning`. New code should pass the two kwargs directly.

## Where to read next

- The kwarg that pairs with `variant`: [Colors](colors.md).
- Type-related styling that doesn't fit the variant axis:
  [Typography](typography.md).
- The widget-by-widget surface for variant kwargs:
  [Widgets → Button](../widgets/actions/button.md),
  [Widgets → Tabs](../widgets/navigation/tabs.md),
  [Widgets → Progressbar](../widgets/data-display/progressbar.md).
- How variants are translated into ttk style elements:
  [Platform → Styling Internals](../platform/ttk-styles-elements.md).
