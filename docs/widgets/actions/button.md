---
title: Button
---

# Button

Buttons allow users to take actions with a single click. They communicate available actions and are commonly used throughout an interface—such as in dialogs, forms, and toolbars.

## Quick start

Create a button by providing `text` and a `command` callback.

```python
import ttkbootstrap as ttk

app = ttk.App()

def on_save():
    print("Saved!")

ttk.Button(app, text="Save", command=on_save).pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use a button when the user needs to **trigger an action immediately**, such as submitting a form, saving a change, or opening a dialog.

### Consider a different control when…

- Use **CheckButton / CheckToggle** for persistent on/off state.
- Use **RadioButton / RadioGroup** for choosing one option from a set.
- Use **ToggleGroup** for compact single or multi selection (segmented control).
- Use **MenuButton / DropdownButton** when the action reveals a menu of choices.

---

## Appearance

Buttons are styled using **semantic colors** and **variant** tokens. Variants describe visual weight and interaction style, not meaning.

!!! link "See [Design System → Variants](../../design-system/variants.md) for how variants map consistently across widgets."

### Colors

The `bootstyle` accepts color tokens that are typically combined with the button variant:

<figure markdown>
![button colors](../../assets/dark/widgets-button-colors.png#only-dark)
![button colors](../../assets/light/widgets-button-colors.png#only-light)
</figure>

```python
ttk.Button(app, text="Primary", bootstyle="primary").pack(pady=4)
ttk.Button(app, text="Outline", bootstyle="primary-outline").pack(pady=4)
ttk.Button(app, text="Ghost", bootstyle="primary-ghost").pack(pady=4)
ttk.Button(app, text="Link", bootstyle="primary-link").pack(pady=4)
ttk.Button(app, text="Text", bootstyle="secondary-text").pack(pady=4)
```

### Variants

The supported variants for Button are: **solid** (default), **outline**, **ghost**, **link**, and **text**.

**Solid (default)**  
Use for the primary, highest-emphasis action on a view (e.g., “Save”, “Submit”, “Continue”).

<figure markdown>
![solid button](../../assets/dark/widgets-button-solid.png#only-dark)
![solid button](../../assets/light/widgets-button-solid.png#only-light)
</figure>

```python
ttk.Button(app, text="Solid")
```

**Outline**  
Use for secondary actions that should stay visible but clearly defer to the primary button (e.g., “Cancel”, “Back”).

<figure markdown>
![outline button](../../assets/dark/widgets-button-outline.png#only-dark)
![outline button](../../assets/light/widgets-button-outline.png#only-light)
</figure>

```python
ttk.Button(app, text="Outline", bootstyle="outline")
```

**Ghost**  
Use for low-emphasis, contextual actions embedded in panels, lists, or toolbars where the UI should stay visually quiet until hover or press.

<figure markdown>
![ghost button](../../assets/dark/widgets-button-ghost.png#only-dark)
![ghost button](../../assets/light/widgets-button-ghost.png#only-light)
</figure>

```python
ttk.Button(app, text="Ghost", bootstyle="ghost")
```

**Link**  
Use for navigation or “take me somewhere” actions that should read like text (e.g., “View details”, “Open settings”).

<figure markdown>
![link button](../../assets/dark/widgets-button-link.png#only-dark)
![link button](../../assets/light/widgets-button-link.png#only-light)
</figure>

```python
ttk.Button(app, text="Link", bootstyle="link")
```

**Text**  
Use for the lowest-emphasis utility actions—especially in dense UIs—where you want minimal chrome but still want button semantics (e.g., “Edit”, “Clear”, “Dismiss”).

<figure markdown>
![text button](../../assets/dark/widgets-button-text.png#only-dark)
![text button](../../assets/light/widgets-button-text.png#only-light)
</figure>

```python
ttk.Button(app, text="Text", bootstyle="text")
```

---

## Examples & patterns

### Using icons

Icons are integrated into the button widget and provide theme-aware and state-enabled icons. The `compound` controls
where the icon/image is positioned relative to the label, and this is `"left"` by default.

<figure markdown>
![icon button](../../assets/dark/widgets-button-icons.png#only-dark)
![icon button](../../assets/light/widgets-button-icons.png#only-light)
</figure>

```python
# button with label & icon
ttk.Button(app, text="Settings", icon="gear").pack(pady=6)

# icon-only button
ttk.Button(app, icon="gear", icon_only=True).pack(pady=6)
```

!!! link "See [Icons & Images](../../capabilities/icons.md) for icon sizing, DPI handling, and recoloring behavior."


!!! tip "Custom Icons"
    You can pass an icon spec instead of a string to customize the color, size, and state of the icon.
    See [Design System → Icons](../../design-system/icons.md).

### Disable until ready (`state`)

Disable a button until the user has completed a step.

```python
btn = ttk.Button(app, text="Continue", bootstyle="primary", state="disabled")
btn.pack()

# later…
btn.configure(state="normal")
```

### Size and emphasis (`padding`, `width`, `underline`)

```python
ttk.Button(app, text="Wide", width=18, padding=(12, 6)).pack(pady=6)
ttk.Button(app, text="Exit", underline=1).pack(pady=6)
```

---

## Behavior

Buttons support keyboard focus and activation.

- **Tab / Shift+Tab** moves focus.
- **Space / Enter** activates the button.
- Disabled buttons do not receive focus or emit events.

!!! link "See [State & Interaction](../../capabilities/state-and-interaction.md) for focus, hover, and disabled behavior across widgets."

---

## Localization

If your application localization is enabled, you can pass a **message token** as `text`. The displayed label is resolved
through the active message catalog.

```python
ttk.Button(app, text="button.save").pack()
```

!!! link "See [Localization](../../capabilities/localization.md) for how message tokens are resolved and how language switching works."

---

## Reactivity

Use a signal when the label should update dynamically at runtime (for example, Start/Stop, Connect/Disconnect).

```python
label = ttk.Signal("Start")
ttk.Button(app, textsignal=label).pack()

label.set("Stop")
```

!!! link "See [Signals](../../capabilities/signals.md) for how signal-backed widget values and text updates work."

---

## Additional resources

### Related widgets

- [CheckButton](../selection/checkbutton.md)
- [RadioButton](../selection/radiobutton.md)
- [ToggleGroup](../selection/togglegroup.md)
- [MenuButton](menubutton.md)
- [DropdownButton](dropdownbutton.md)
- [Dialog](../dialogs/dialog.md)
- [MessageDialog](../dialogs/messagedialog.md)

### Framework concepts

- [Design System → Variants](../../design-system/variants.md)
- [Design System → Icons](../../design-system/icons.md)
- [Icons & Imagery](../../capabilities/icons-and-imagery.md)
- [Signals](../../capabilities/signals.md)
- [Localization](../../capabilities/localization.md)
- [State & Interaction](../../capabilities/state-and-interaction.md)

### API reference

- [`ttkbootstrap.Button`](../../reference/widgets/Button.md)
