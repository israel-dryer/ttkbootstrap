# Button

A `Button` initiates an action in response to user interaction.

In ttkbootstrap, `Button` is a **first-class framework component** that participates in the design
system, reactive model, and application architecture—rather than a thin wrapper around
`ttk.Button`.

---

## Framework integration

`Button` integrates with multiple ttkbootstrap framework layers automatically.

### Design System

- Uses typography tokens defined by the active theme
- Supports semantic colors (`primary`, `secondary`, `success`, etc.)
- Supports visual variants (`solid`, `outline`, `ghost`, `link`)
- Responds consistently to hover, focus, pressed, and disabled states

### Signals & Events

- Can trigger imperative callbacks (`command`)
- Can participate in reactive workflows using
  [signals](../../capabilities/signals/index.md)
- Emits meaningful interaction events rather than requiring manual binding

### Icons & Images

- Supports themed, DPI-aware icons
- Icons participate in image caching and recoloring
- Icon-only and icon+text buttons are first-class patterns

### Localization

- Button text may be localized using message catalogs
- Text updates automatically when the active language changes

### Layout Properties

- Respects declarative layout intent (padding, alignment, expansion)
- Integrates cleanly with container-driven layout systems

In most cases, you do not need to configure these integrations explicitly.

---

## Basic usage

```python
import ttkbootstrap as ttk

def on_submit():
    print("Submitted")

app = ttk.App()

ttk.Button(
    app,
    text="Submit",
    command=on_submit,
).pack(padx=20, pady=20)

app.mainloop()
```

---

## Styling buttons

Buttons are styled using **semantic color** and **variant** tokens rather than raw colors.

```python
ttk.Button(
    app,
    text="Save",
    bootstyle="primary",
)
```

Variants describe *visual weight*, not meaning:

```python
ttk.Button(app, text="Primary", bootstyle="primary")
ttk.Button(app, text="Outline", bootstyle="primary-outline")
ttk.Button(app, text="Ghost", bootstyle="primary-ghost")
ttk.Button(app, text="Link", bootstyle="link")
```

These styles are theme-aware and consistent across the application.

---

## Buttons with icons

Icons integrate directly with the framework’s image system.

```python
ttk.Button(
    app,
    text="Save",
    icon="save",
)
```

Icon-only buttons are also supported:

```python
ttk.Button(
    app,
    icon="trash",
    icon_only=True,
)
```

Icons automatically scale with DPI and respond to theme changes.

---

## Reactive patterns with signals

Buttons can participate in reactive workflows by interacting with signals.

```python
from ttkbootstrap import Signal

enabled = Signal(True)

def on_click():
    print("Clicked")

btn = ttk.Button(
    app,
    text="Action",
    command=on_click,
)

enabled.subscribe(
    lambda value: btn.configure(
        state="normal" if value else "disabled"
    )
)
```

This allows application state—not widget wiring—to drive behavior.

---

## Accessibility and interaction

Buttons follow consistent accessibility expectations:

- Keyboard activation via Enter/Space
- Focus and hover state visibility
- Disabled state propagation
- Predictable interaction feedback

These behaviors are handled by the framework.

---

## When to use ButtonGroup instead

If you need:

- Grouped actions
- Mutually exclusive choices
- Toggle-style behavior
- Toolbar-style layouts

Consider using **ButtonGroup** or **ToggleGroup** instead of managing multiple buttons manually.

---

## Relationship to ttk

Internally, `Button` builds on ttk primitives—but those details are intentionally abstracted.

You should not need to:

- Manage ttk state flags directly
- Adjust element layouts manually
- Compensate for platform styling differences

Those concerns are handled by ttkbootstrap.

---

## See also

**Related widgets**

- [ButtonGroup](buttongroup.md)
- [ToggleGroup](../selection/togglegroup.md)

**Framework concepts**

- [Signals & Events](../../capabilities/signals/index.md)
- [Icons & Images](../../capabilities/icons/index.md)
- [Layout Properties](../../capabilities/layout-props.md)

**API reference**

- [`Button`](../../reference/widgets/Button.md)
