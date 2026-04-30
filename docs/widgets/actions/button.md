---
title: Button
---

# Button

A button triggers an action when the user clicks it: submit a form,
save a change, open a dialog, run a one-shot operation. Buttons appear
throughout an interface — in dialog footers, toolbars, forms, and
inline within content.

This page covers the `Button` widget. For groups of related buttons,
see [ButtonGroup](buttongroup.md). For a button that opens a menu, see
[DropdownButton](dropdownbutton.md) or [MenuButton](menubutton.md).

---

## Basic usage

A button needs `text` and a `command` callback.

```python
import ttkbootstrap as ttk

app = ttk.App()

def on_save():
    print("Saved!")

ttk.Button(app, text="Save", command=on_save).pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

| Option | Purpose |
|---|---|
| `text` | Label string. Treated as a localization key when localization is enabled. |
| `command` | Callback fired on activation (click, Space, Enter). |
| `accent` | Semantic color: `primary`, `secondary`, `success`, `info`, `warning`, `danger`, `light`, `dark`. |
| `variant` | Visual weight: `solid` (default), `outline`, `ghost`, `link`, `text`. |
| `density` | `default` or `compact` — `compact` reduces internal padding. |
| `icon` | Icon name or spec; theme- and state-aware. |
| `compound` | Icon placement (`left`, `right`, `top`, `bottom`, `center`). Default `left`. |
| `icon_only` | If `True`, strips label-side padding for icon-only buttons. |
| `width` | Width in characters. |
| `padding` | Internal padding as int or `(x, y)` tuple of pixels. |
| `state` | `normal` or `disabled`. |
| `underline` | Index of the character to mark as a keyboard mnemonic (Alt+letter on Windows/Linux). |
| `textsignal` | `Signal[str]` driving a reactive label (see [Localization & reactivity](#localization--reactivity)). |

### Accents

`accent` sets the semantic color. The same accent token reads the same
way across every ttkbootstrap widget, so a `danger` button matches a
`danger` badge or progress bar in the same theme.

<figure markdown>
![button colors](../../assets/dark/widgets-button-colors.png#only-dark)
![button colors](../../assets/light/widgets-button-colors.png#only-light)
</figure>

```python
ttk.Button(app, text="Primary", accent="primary").pack(pady=4)
ttk.Button(app, text="Success", accent="success").pack(pady=4)
ttk.Button(app, text="Danger", accent="danger").pack(pady=4)
```

!!! link "See [Design System → Variants](../../design-system/variants.md) for how accents and variants compose across widgets."

### Variants

`variant` sets the visual weight, expressing how much emphasis the
action carries on the surrounding view.

**Solid** (default) — the primary, highest-emphasis action on a view.
Reach for it for "Save", "Submit", "Continue".

<figure markdown>
![solid button](../../assets/dark/widgets-button-solid.png#only-dark)
![solid button](../../assets/light/widgets-button-solid.png#only-light)
</figure>

```python
ttk.Button(app, text="Solid")
```

**Outline** — secondary actions that should stay visible but defer to
a primary button (e.g., "Cancel", "Back").

<figure markdown>
![outline button](../../assets/dark/widgets-button-outline.png#only-dark)
![outline button](../../assets/light/widgets-button-outline.png#only-light)
</figure>

```python
ttk.Button(app, text="Outline", variant="outline")
```

**Ghost** — low-emphasis, contextual actions in panels, lists, or
toolbars where the UI should stay quiet until hover or press.

<figure markdown>
![ghost button](../../assets/dark/widgets-button-ghost.png#only-dark)
![ghost button](../../assets/light/widgets-button-ghost.png#only-light)
</figure>

```python
ttk.Button(app, text="Ghost", variant="ghost")
```

**Link** — navigation-style actions that should read like text
("View details", "Open settings").

<figure markdown>
![link button](../../assets/dark/widgets-button-link.png#only-dark)
![link button](../../assets/light/widgets-button-link.png#only-light)
</figure>

```python
ttk.Button(app, text="Link", variant="link")
```

**Text** — the lowest-emphasis utility action, with minimal chrome
("Edit", "Clear", "Dismiss"). Useful in dense UIs where a full button
silhouette would be visually noisy.

<figure markdown>
![text button](../../assets/dark/widgets-button-text.png#only-dark)
![text button](../../assets/light/widgets-button-text.png#only-light)
</figure>

```python
ttk.Button(app, text="Text", variant="text")
```

### Density

`density="compact"` reduces internal padding for dense toolbars or
forms. The default is taller and more comfortable for primary content.

```python
ttk.Button(app, text="Compact", density="compact").pack()
```

### Icons

Icons are integrated through the style system, so they pick up the
button's accent and adapt to hover, focus, and disabled states. By
default the icon sits to the left of the label.

<figure markdown>
![icon button](../../assets/dark/widgets-button-icons.png#only-dark)
![icon button](../../assets/light/widgets-button-icons.png#only-light)
</figure>

```python
# label + icon (compound="left" by default)
ttk.Button(app, text="Settings", icon="gear").pack(pady=6)

# icon-only button — strips label padding
ttk.Button(app, icon="gear", icon_only=True).pack(pady=6)
```

!!! tip "Custom icon specs"
    Pass a dict instead of a name to override color, size, or per-state
    appearance. See [Design System → Icons](../../design-system/icons.md).

!!! link "See [Icons & Imagery](../../capabilities/icons/index.md) for sizing, DPI handling, and recoloring behavior."

### Sizing

`width` is measured in characters; `padding` accepts an int or `(x, y)`
tuple of pixels. Use them to align buttons to a grid or pad icon-only
buttons.

```python
ttk.Button(app, text="Wide", width=18, padding=(12, 6)).pack(pady=6)
```

### Keyboard mnemonic

`underline` marks one character as a mnemonic (zero-indexed) and draws
it underlined. On Windows and Linux, **Alt+letter** activates the
button; on macOS the underline is rendered but the activation
shortcut is platform-dependent.

```python
ttk.Button(app, text="Exit", underline=1).pack()
```

---

## Behavior

- **Tab / Shift+Tab** moves keyboard focus.
- **Space / Enter** activates the focused button (fires `command`).
- A disabled button is skipped during focus traversal and does not
  fire `command` or click-related events.
- Hover, focus, and pressed visuals are produced by the active theme;
  no extra wiring is required.

### Disable until ready

Disable a button until a precondition is met, then re-enable it.

```python
btn = ttk.Button(app, text="Continue", accent="primary", state="disabled")
btn.pack()

# later, after validation succeeds…
btn.configure(state="normal")
```

!!! link "See [State & Interaction](../../capabilities/state-and-interaction.md) for focus, hover, and disabled behavior across widgets."

---

## Events

`Button` exposes a single primary hook, the **`command`** callback,
fired on every activation (click, Space, or Enter):

```python
def on_save():
    ...

ttk.Button(app, text="Save", command=on_save)
```

For lower-level interactions — distinguishing single vs double-click,
right-click, or modifier keys — bind Tk events directly:

```python
btn = ttk.Button(app, text="Open")
btn.bind("<Double-Button-1>", lambda e: open_in_new_window())
btn.bind("<Control-Button-1>", lambda e: open_with_modifier())
```

---

## Localization & reactivity

### Localized labels

When localization is enabled, the value passed to `text=` is treated as
a message key and resolved through the active catalog. The label
updates automatically when the locale changes at runtime. If the key
has no translation, the literal string is shown — so `text="Save"`
works whether or not localization is on.

```python
ttk.Button(app, text="button.save").pack()
```

### Reactive labels

Bind a `Signal[str]` via `textsignal` when the label needs to update
dynamically — Start/Stop toggles, counters, status indicators.

```python
label = ttk.Signal("Start")
ttk.Button(app, textsignal=label).pack()

label.set("Stop")
```

!!! link "See [Signals](../../capabilities/signals/index.md) for reactive bindings, and [Localization](../../capabilities/localization.md) for catalogs and locale switching."

---

## When should I use Button?

Use `Button` when the user needs to **trigger an action immediately** —
submitting a form, saving a change, opening a dialog, navigating to a
new view.

Prefer a different control when:

- the action toggles persistent state → use [CheckButton](../selection/checkbutton.md), [CheckToggle](../selection/checktoggle.md), or [Switch](../selection/switch.md).
- the user picks one option from a small set → use [RadioButton](../selection/radiobutton.md), [RadioGroup](../selection/radiogroup.md), or [ToggleGroup](../selection/togglegroup.md).
- the action reveals a menu of choices → use [DropdownButton](dropdownbutton.md) or [MenuButton](menubutton.md).
- you want a connected row of related actions → use [ButtonGroup](buttongroup.md).

---

## Related widgets

- [ButtonGroup](buttongroup.md) — connected row of related buttons.
- [MenuButton](menubutton.md) — opens a Tk menu.
- [DropdownButton](dropdownbutton.md) — a primary action plus a dropdown of choices.
- [CheckButton](../selection/checkbutton.md), [Switch](../selection/switch.md) — persistent on/off state.
- [RadioButton](../selection/radiobutton.md), [ToggleGroup](../selection/togglegroup.md) — single-choice selection.

---

## Reference

- **API reference:** [`ttkbootstrap.Button`](../../reference/widgets/Button.md)
- **Related guides:**
    - [Design System → Variants](../../design-system/variants.md)
    - [Design System → Icons](../../design-system/icons.md)
    - [Icons & Imagery](../../capabilities/icons/index.md)
    - [Signals](../../capabilities/signals/index.md)
    - [Localization](../../capabilities/localization.md)
    - [State & Interaction](../../capabilities/state-and-interaction.md)
