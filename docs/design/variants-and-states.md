---
icon: fontawesome/solid/sliders
---

# Variants & States

When you style a widget with `bootstyle`, picture the final appearance as a combination of three axes:

- **Color token** (`primary`, `success`, `danger`, etc.) describes the semantic intent.
- **Variant** (`outline`, `ghost`, `link`, `solid`, etc.) controls the treatment, such as fills, borders, or underlined text.
- **Widget suffix** (implicit by default) scopes the variant to a specific class when you need a cross-widget override.

For example, `bootstyle="success-outline"` produces a success-colored outline button using the implicit class. If you include the widget suffix (`success-outline-toolbutton`), the builder still understands the tokens and emits a hashed TTK style name (`bs[2fb014e9].success.Outline.TButton`) that maps back to the combination.

## Choosing a variant

Every widget declares the variants it supports. Common ones include:

- `default`: a filled background that follows the color token.
- `outline`: a transparent surface with colored borders and text.
- `ghost`: a subtle background wash that reads softer than a full fill.
- `link`: no background or border, just accented text.
- `flat` / `solid`: builder-specific tweaks to padding, radius, or border width.

Check the widget reference to see which names are available and how they behave in feedback, data display, or navigation contexts. If you pass a variant the widget does not support, the builder falls back to `default` so the control still renders gracefully.

## States and transitions

Variants define how a widget responds to states (`active`, `disabled`, `hover`, `focus`). The builder translates those rules into the generated style so controls react as expected without extra code. Behind the scenes, `Style.register_style()` remembers the color/variant pairing so switching themes (`ttk.set_theme()` or `ttk.toggle_theme()`) rebuilds the same style with the new palette while preserving the state rules.

## Customizing styles

The style name also includes any extra options you configure through a widget (borders, icons, icons + separators, corner radius). The registry hashes those options into abbreviated names (`bs[2fb014e9].success.Outline.TButton`) so you can keep the API declarative instead of editing generated strings. Prefer semantic color and variant names or the `Style.colors` map for palette reuse, and only rely on hashed styles when you cannot express a combination through the standard Bootstyle segments.
