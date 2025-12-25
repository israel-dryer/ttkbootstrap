---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


---

title: ButtonGroup
---

# ButtonGroup

`ButtonGroup` visually groups multiple buttons (or button-like widgets) into a single connected cluster. It provides **automatic positioning and styling** for the first, middle, and last items—without tracking selection state.

Use it for toolbars, compact action clusters, and “related actions” groups where you want the controls to look connected.

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

group = ttk.ButtonGroup(app, bootstyle="primary")
group.add("Save", command=lambda: print("Save"))
group.add("Load", command=lambda: print("Load"))
group.add("Delete", command=lambda: print("Delete"))
group.pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use ButtonGroup when you want **visual grouping** of actions, but you *don’t* want the container to manage any “selected” value.

### Consider a different control when…

- You need single or multi selection state → use **ToggleGroup**

- You need classic radio semantics → use **RadioGroup**

- You need an overflow / menu of actions → use **DropdownButton**

- You need a structured navigation pattern → use **Notebook** or **PageStack**

---

## Appearance

ButtonGroup applies a `-buttongroup` style suffix to its children and automatically updates each child’s **position**:

- `before` (first)

- `center` (middle)

- `after` (last)

This enables connected borders and shared separators without manually styling each widget.

### Bootstyle

The group’s `bootstyle` becomes the base for all child widgets.

```python
group = ttk.ButtonGroup(app, bootstyle="success-outline")
group.add("Apply")
group.add("Cancel")
```

If a child widget explicitly sets `bootstyle`, ButtonGroup will still append `-buttongroup` so it participates in grouping.

### Orientation

Use `orient="horizontal"` (default) for toolbar-style groups, or `orient="vertical"` for stacked action lists.

```python
group = ttk.ButtonGroup(app, orient="vertical", bootstyle="secondary")
group.add("Up")
group.add("Down")
group.add("Remove")
```

---

## Examples & patterns

### Disabling the entire group

Set `state` on the group to apply to all children (unless overridden per child).

```python
group = ttk.ButtonGroup(app, bootstyle="primary", state="disabled")
group.add("Save")
group.add("Load")
```

Later:

```python
group.configure(state="normal")
```

### Using keys to configure a specific widget

If you provide a `key`, you can retrieve/configure/remove that widget later.

```python
group = ttk.ButtonGroup(app)
group.add("New", key="new_btn", command=lambda: print("New"))
group.add("Open", key="open_btn", command=lambda: print("Open"))

group.configure_widget("new_btn", state="disabled")
```

### Mixing widget types

By default, ButtonGroup creates `ttkbootstrap.Button` children. You can provide a `widget_type` for mixed groups.

```python
from ttkbootstrap import MenuButton

group = ttk.ButtonGroup(app, bootstyle="primary")
group.add("Run", command=lambda: print("Run"))
group.add("Options", widget_type=MenuButton, key="menu")
```

!!! note "Stateful widget types"
    ButtonGroup is often used with buttons and menu triggers. If you use radio/check widgets, they keep their own state and variables.

### Removing widgets

```python
group.remove("open_btn")  # remove by key
```

### Clearing the group

```python
group.clear()
```

---

## Behavior

- ButtonGroup **does not track selection**. It only manages layout and visual grouping.

- Child order is the order widgets were added (insertion order).

- When widgets are added/removed, ButtonGroup recomputes each widget’s position (`before/center/after`).

- Changing `orient` repacks children (`left` for horizontal, `top` for vertical) and updates grouping styles.

---

## Localization & reactivity

ButtonGroup itself has no text to localize; localization and reactive text behavior come from the **child widgets** you add (e.g., `Button`, `MenuButton`).

See **Guides → Internationalization → Localization** and **Guides → Events & Signals → Signals** for app-wide behavior.

---

## Related widgets

- **ToggleGroup** — grouped controls that also manage a selected value (single or multi)

- **RadioGroup** — single selection, radio semantics

- **DropdownButton** — compact action launcher with a menu

- **ContextMenu** — widget-backed popup menu (often used with toolbars)

---

## Reference

- **API Reference:** `ttkbootstrap.ButtonGroup`

- **Related guides:** Design System → Variants, Patterns → Toolbars

---

## Additional resources

### Related widgets

- [Button](button.md)

- [ContextMenu](contextmenu.md)

- [DropdownButton](dropdownbutton.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.ButtonGroup`](../../reference/widgets/ButtonGroup.md)
