---
title: Dialog
icon: fontawesome/solid/window-maximize
---

# Dialog

`Dialog` is a flexible, builder-based dialog window for presenting messages, forms, and decisions. It supports **modal and popover modes**, rich button semantics, smart positioning, and a composition-first API that avoids subclassing.

<!--
IMAGE: Dialog overview
Suggested: Modal dialog with title, content area, and primary/cancel buttons
Theme variants: light / dark
-->

---

## Basic usage

Create a simple modal dialog with custom content and buttons:

```python
import ttkbootstrap as ttk

def build_content(parent):
    ttk.Label(parent, text="Are you sure?").pack(padx=20, pady=20)

dialog = ttk.Dialog(
    title="Confirm action",
    content_builder=build_content,
    buttons=[
        ttk.DialogButton(text="Cancel", role="cancel", result=False),
        ttk.DialogButton(text="Confirm", role="primary", result=True, default=True),
    ],
)

dialog.show()

if dialog.result:
    print("User confirmed")
```

<!--
IMAGE: Basic Dialog example
Suggested: Confirmation dialog with Cancel / Confirm buttons
-->

---

## What problem it solves

Dialogs are used when the application needs the user’s attention—confirmation, input, or acknowledgement. `Dialog` solves this by:

- Providing a **single, composable base** for all dialog types
- Supporting modal and non-modal (popover) interaction
- Offering standardized button roles, keyboard behavior, and results
- Handling positioning, focus, and window lifecycle consistently

Unlike fixed dialog subclasses, `Dialog` lets you build exactly what you need without inheritance.

---

## Core concepts

### Builder-based composition

Instead of subclassing, dialogs are composed using builder callbacks:

- `content_builder(parent)` builds the main content
- `footer_builder(parent)` (optional) replaces the standard button footer

```python
def build_content(parent):
    ttk.Label(parent, text="Hello world").pack(padx=20, pady=20)

dialog = ttk.Dialog(content_builder=build_content)
```

This keeps dialog logic simple, explicit, and reusable.

---

### Buttons and results

Dialogs use `DialogButton` specifications to define footer buttons.

```python
ttk.DialogButton(
    text="OK",
    role="primary",
    result="ok",
    default=True,
)
```

Button attributes:

- `role`: visual + semantic role (`primary`, `secondary`, `danger`, `cancel`, `help`)
- `result`: value assigned to `dialog.result`
- `default`: triggered by **Enter**
- `closes`: whether the dialog closes when clicked
- `command(dialog)`: optional callback before close

Buttons are laid out **right-to-left** by convention.

<!--
IMAGE: Dialog button roles
Suggested: Footer showing primary, secondary, and danger buttons
-->

---

### Modal vs popover mode

`mode` controls how the dialog interacts with its parent:

- **modal** (default)
  - Blocks interaction with parent
  - Uses `grab_set` and `wait_window`
- **popover**
  - Closes automatically when focus leaves
  - Useful for lightweight, contextual UI

```python
dialog = ttk.Dialog(mode="popover")
dialog.show()
```

---

### Keyboard behavior

Dialogs handle common keyboard shortcuts automatically:

- **Enter** → activates the default button
- **Escape** → activates the cancel button (or closes the dialog)

This behavior is wired based on button roles—no manual bindings required.

---

## Positioning

Dialogs support explicit and anchor-based positioning via `show(...)`.

### Explicit coordinates

```python
dialog.show(position=(200, 150))
```

### Anchor-based positioning

Anchor dialogs to:

- a widget
- the parent window
- the screen
- the mouse cursor

```python
dialog.show(
    anchor_to="cursor",
    anchor_point="sw",
    window_point="nw",
    offset=(8, 8),
    auto_flip=True,
)
```

<!--
IMAGE: Dialog positioning
Suggested: Popover dialog anchored to a button and to the cursor
-->

---

## Common options & patterns

### Custom footer (no buttons)

Replace the standard footer entirely:

```python
def build_footer(parent):
    ttk.Button(parent, text="Help").pack(side="left")
    ttk.Button(parent, text="OK").pack(side="right")

dialog = ttk.Dialog(
    content_builder=build_content,
    footer_builder=build_footer,
)
```

---

### Dialogs with form input

```python
def build_form(parent):
    ttk.Label(parent, text="Name").grid(row=0, column=0, padx=10, pady=5)
    entry = ttk.Entry(parent)
    entry.grid(row=0, column=1, padx=10, pady=5)
    parent.entry = entry

def on_ok(dialog):
    dialog.result = dialog._content.entry.get()

dialog = ttk.Dialog(
    title="Enter name",
    content_builder=build_form,
    buttons=[
        ttk.DialogButton(text="Cancel", role="cancel"),
        ttk.DialogButton(text="OK", role="primary", command=on_ok, default=True),
    ],
)
dialog.show()
```

---

## UX guidance

- Use dialogs sparingly—only when user attention is required
- Keep content concise and focused
- Always provide a clear cancel/escape path
- Prefer semantic button roles over custom styling

!!! tip "Non-blocking feedback"
    If the user doesn’t need to respond, use a **Toast** instead of a Dialog.

---

## When to use / when not to

**Use Dialog when:**

- Confirmation or decision is required
- You need focused user input
- The workflow must pause until a response is given

**Avoid Dialog when:**

- Feedback is informational only (use Toast)
- Interaction should remain inline
- Frequent interruptions would harm flow

---

## Related widgets

- **Toast** — non-blocking notifications
- **Tooltip** — hover-based hints
- **PageStack** — step-based workflows and wizards
