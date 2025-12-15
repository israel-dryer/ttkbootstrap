---
title: Button
icon: fontawesome/solid/hand-pointer
---

# Button

Buttons allow users to take actions and make choices with a single click. They communicate available actions and are commonly used throughout an interface—such as in dialogs, forms, and toolbars.

## Basic usage

Typically, a button will show text and handle a button press via the `text` and `command` options.

```python
import ttkbootstrap as ttk

app = ttk.App()


def on_save():
    print("Saved!")


ttk.Button(app, text="Save", command=on_save).pack(padx=20, pady=20)

app.mainloop()
```

---

## Variants

### Solid (default)

Use for the primary, highest-emphasis action on a view (e.g., “Save”, “Submit”, “Continue”).

<figure markdown>
![solid button](../../assets/dark/widgets-button-solid.png#only-dark)
![solid button](../../assets/light/widgets-button-solid.png#only-light)
</figure>

```python
ttk.Button(app, text="Solid")
```

### Outline

Use for secondary actions that should stay visible but clearly defer to the primary button (e.g., “Cancel”, “Back”,
“Learn more”).

<figure markdown>
![outline button](../../assets/dark/widgets-button-outline.png#only-dark)
![outline button](../../assets/light/widgets-button-outline.png#only-light)
</figure>

```python
ttk.Button(app, text="Outline", bootstyle="outline") 
```

### Ghost

Use for low-emphasis, contextual actions embedded in panels, lists, or toolbars where the UI should stay visually quiet
until hover/press.

<figure markdown>
![ghost button](../../assets/dark/widgets-button-ghost.png#only-dark)
![ghost button](../../assets/light/widgets-button-ghost.png#only-light)
</figure>

```python
ttk.Button(app, text="Ghost", bootstyle="ghost")
```

### Link

Use for navigation or “take me somewhere” actions that should read like text and feel lightweight (e.g., “View details”,
“Open settings”).

<figure markdown>
![link button](../../assets/dark/widgets-button-link.png#only-dark)
![link button](../../assets/light/widgets-button-link.png#only-light)
</figure>

```python
ttk.Button(app, text="Link", bootstyle="link")
```

### Text

Use for the lowest-emphasis utility actions—especially in dense UIs—where you want minimal chrome but still want button
semantics (e.g., “Edit”, “Clear”, “Dismiss”).

<figure markdown>
![link button](../../assets/dark/widgets-button-link.png#only-dark)
![link button](../../assets/light/widgets-button-link.png#only-light)
</figure>

```python
ttk.Button(app, text="Text", bootstyle="text")
```

---

## Other common options

Other common options include:

### `state`

Disable a button until the user has completed a step.

```python
btn = ttk.Button(app, text="Continue", bootstyle="primary", state="disabled")
btn.pack()

# later…
btn.configure(state="normal")
```

### `padding`, `width`, `underline`

```python
ttk.Button(app, text="Wide", width=18, padding=(12, 6)).pack(pady=6)
ttk.Button(app, text="Exit", underline=1).pack(pady=6)
```

---

## Colors

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

---

## Icons

Icons are integrated into the button widget and provide theme-aware and state-enabled icons.

<figure markdown>
![icon button](../../assets/dark/widgets-button-icons.png#only-dark)
![icon button](../../assets/light/widgets-button-icons.png#only-light)
</figure>

```python
ttk.Button(
    app,
    text="Settings",
    icon="gear"
).pack(pady=6)
```

!!! note "Default icon position"
    When an icon is used, the default `compound` is set to left. The `compound` option controls where the icon is
    positioned relative to the text. You can use other values: left, right, top, bottom, center.

    Use the `icon_only` option when you are only showing an icon. This will remove the extra padding added for text and will
    make the default icon a bit larger.

!!! tip "Customizing icons"
    You can pass an icon spec instead of a string to customize the color, size, and state of the icon. See iconography for
    details.

---

## Reactive text with `textsignal`

If your v2 app uses signals, you can bind the label text to a signal (so the button text updates automatically).

```python
import ttkbootstrap as ttk

app = ttk.App()

# Example only — use your real signal creation API
label = ttk.Signal("Start")  # pseudo-code

btn = ttk.Button(app, bootstyle="primary", textsignal=label)
btn.pack(padx=20, pady=20)

# later…
label.set("Stop")

app.mainloop()
```

---

## Localization

Localization behavior is controlled by the **global application settings**.

By default, widgets use `localize="auto"`. In this mode, the `text` is treated as a localization
key **when a translation exists**. If the key is not found in the active message catalog, the
widget falls back to using the value as **plain text**.

You can override this behavior per widget if needed.

```python
# uses global app localization settings (default)
ttk.Button(app, text="button.ok", bootstyle="primary").pack()

# explicitly enable localization
ttk.Button(app, text="button.ok", localize=True, bootstyle="primary").pack()

# explicitly disable localization (always treat text as a literal)
ttk.Button(app, text="OK", localize=False, bootstyle="primary").pack()
```

!!! tip "Safe to pass literal text"
    With `localize="auto"`, you can pass either a localization key or a literal label.
    If no translation is found, the label is shown as-is.

---

## Related widgets

- **CheckButton** — boolean toggle (on/off)
- **RadioButton** — single selection in a group
- **MenuButton** / **DropdownButton** — button that opens a menu
- **Dialog** / **MessageDialog** — action buttons inside modal flows
