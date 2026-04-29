---
title: Accessibility
---

# Accessibility

This page describes what ttkbootstrap provides for keyboard navigation and visual accessibility, and is honest about the limitations of the underlying Tk toolkit for screen reader support.

---

## Keyboard navigation

Tk's Tab traversal is active in all ttkbootstrap applications without any setup. Pressing Tab moves focus forward through interactive widgets; Shift+Tab moves it backward.

The traversal order follows widget creation order within each container. Nested containers are traversed depth-first.

### Controlling tab order

The `takefocus` option controls whether a widget participates in Tab traversal:

```python
# Exclude a widget from tab order
label = ttk.Label(app, text="Read-only", takefocus=False)

# Include a normally non-focusable widget
canvas = ttk.Canvas(app, takefocus=True)
```

Most interactive widgets (`Button`, `Entry`, `CheckButton`, etc.) include themselves in the tab order by default. Purely decorative widgets (`Label`, `Separator`, `Frame`) do not.

### Traversal helpers

Any widget exposes helpers for inspecting and moving focus programmatically:

```python
# Move to next/previous widget in tab order
next_widget = widget.tk_focusNext()
prev_widget = widget.tk_focusPrev()

# Query current focus
focused = app.focus_get()
```

---

## Focus rings

ttkbootstrap installs a focus-ring system on import that mirrors CSS `:focus-visible` behavior:

- **Tab navigation** — a visible focus ring appears on the focused widget.
- **Mouse clicks** — no focus ring is shown, even though the widget has focus.

This distinction avoids the visual noise of rings appearing after every click while still giving keyboard users a clear focus indicator.

### Programmatic focus with a ring

When your code moves focus (for example, to a validation error field), pass `visual_focus=True` to show the ring:

```python
# Normal programmatic focus — no ring
entry.focus_set()

# Programmatic focus with ring — useful after validation failure
entry.focus_set(visual_focus=True)
```

`focus_force` accepts the same parameter for cases where you need to pull focus from another window.

### Checking keyboard focus

```python
from ttkbootstrap.runtime.visual_focus import is_keyboard_focus

if is_keyboard_focus(widget):
    # Widget has focus AND was focused via keyboard
    ...
```

---

## Contrast and color

ttkbootstrap themes are designed with WCAG contrast ratios in mind for their default states. The semantic token system (`accent`, `surface`, `foreground`) ensures that color choices made by the theme are applied consistently across the widget tree.

When creating custom themes or using the color modifier system, verify that foreground-on-background combinations meet WCAG AA (4.5:1 for normal text, 3:1 for large text). The `primary[muted]` and `foreground[muted]` modifiers reduce contrast intentionally — use them only for supplementary text, not primary content.

Avoid expressing state exclusively through color. Pair color changes with text, icons, or shape changes so that colorblind users receive the same information.

---

## Screen reader support

!!! note "Tk accessibility limitation"
    Tk does not expose a native accessibility API on any platform. Screen readers (VoiceOver on macOS, NVDA/JAWS on Windows, Orca on Linux) cannot read widget labels or roles from ttkbootstrap windows in the same way they can from native toolkit applications.

The practical consequences:

| Platform | Screen reader | Tk behavior |
|---|---|---|
| macOS | VoiceOver | Window title is announced. Widget content is generally not accessible. |
| Windows | NVDA, JAWS | Limited. Focus changes may be detected, but labels and roles are not exposed. |
| Linux | Orca | Largely inaccessible via AT-SPI. |

For applications where screen reader accessibility is a hard requirement, Tk-based toolkits are not the right foundation. Native-toolkit frameworks (PyQt6/PySide6 expose Qt Accessibility, wxPython exposes platform accessibility APIs) provide full screen reader integration.

---

## Practical checklist

For applications where keyboard accessibility matters:

- [ ] All interactive widgets are reachable by Tab and operable by keyboard (Enter/Space for buttons, arrow keys for lists and menus).
- [ ] Focus is never trapped in a section with no way out by keyboard.
- [ ] Modal dialogs return focus to the triggering element on close.
- [ ] Validation errors call `focus_set(visual_focus=True)` on the offending field.
- [ ] `takefocus=False` is set on decorative widgets that serve no interactive purpose.
- [ ] Color is not the only indicator of state (pair with text or iconography).
- [ ] Custom colors are checked against WCAG contrast ratios.

---

## Next steps

- [Platform Differences](platform-differences.md) — how focus and keyboard behavior vary by OS
- [Events & Bindings](events-and-bindings.md) — wiring keyboard events to widget actions
- [Capabilities → Focus](../reference/capabilities/focus.md) — `focus_set`, `focus_get`, and traversal API
