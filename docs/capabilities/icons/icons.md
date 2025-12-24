# Icons

Icons are symbolic visual elements used to communicate actions, states, and
affordances within the user interface.

In ttkbootstrap, icons are treated as a **shared capability** rather than a
per-widget feature, allowing consistent behavior across the framework.

---

## Purpose of icons

Icons are used to:

- reinforce meaning alongside text
- save space in dense interfaces
- provide quick visual recognition

They are most effective when used consistently and sparingly.

---

## Icon usage patterns

Common icon usage patterns include:

- icon-only buttons
- icon + text buttons
- menu item icons
- state indicators (selected, warning, error)

Consistency in these patterns improves usability.

---

## Icons and state

Icons often respond to widget state.

Examples:

- disabled icons appear muted
- active icons appear emphasized
- selected icons reflect current state

ttkbootstrap integrates icon behavior with widget state to ensure visual feedback
matches interaction.

---

## Theming and color

Icons typically derive their color from the active theme.

This allows:

- automatic light/dark adaptation
- consistent semantic coloring
- reduced need for manual styling

Icons should avoid hardcoded colors unless required.

---

## Icon sources

ttkbootstrap supports multiple icon sources, including:

- bundled icon sets
- third-party icon libraries
- custom application icons

All sources are treated uniformly by the icon capability.

---

## Icon sizing

Icon size should be consistent within a context.

Considerations include:

- alignment with text baseline
- touch target size
- visual weight relative to surrounding elements

Avoid mixing icon sizes arbitrarily.

---

## Performance considerations

Icons are reused frequently.

Best practices include:

- caching icon images
- avoiding repeated recoloring
- sharing icon instances where possible

Centralized management improves performance.

---

## ttkbootstrap guidance

ttkbootstrap encourages:

- semantic icon usage
- theme-driven coloring
- reuse over recreation
- documenting icons exposed by widgets

These practices ensure clarity and consistency.

---

## Common pitfalls

- using icons without text where meaning is unclear
- inconsistent icon sizing
- hardcoding icon colors
- recreating icons unnecessarily

Treating icons as a capability avoids these issues.

---

## Next steps

- See **Images** for image lifecycle and caching
- See **Platform → Images & DPI** for rendering behavior
- See **Widgets** for icon usage examples
