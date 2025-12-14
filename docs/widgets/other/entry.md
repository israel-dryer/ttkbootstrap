---
title: Entry
icon: fontawesome/solid/i-cursor
---

# Entry

`Entry` is a themed wrapper around `ttk.Entry` that integrates ttkbootstrap’s styling system and reactive text support. It’s the **primitive, low-level text input** used as a building block for higher-level controls like `TextEntry`, `NumericEntry`, `DateEntry`, and others.

<!--
IMAGE: Entry basic states
Suggested: Normal, readonly, and disabled Entry side-by-side
Theme variants: light / dark
-->

---

## Basic usage

Use `Entry` when you need a simple single-line text input.

```python
import ttkbootstrap as ttk

app = ttk.Window()

entry = ttk.Entry(app)
entry.pack(padx=20, pady=20)

app.mainloop()
```

<!--
IMAGE: Basic Entry example
Suggested: A simple Entry with text inserted to demonstrate caret/focus
-->

---

## What problem it solves

Tk’s native `ttk.Entry` provides the core text entry behavior, but it does not provide a consistent, token-driven styling layer across themes or a reactive binding abstraction. ttkbootstrap’s `Entry` adds:

- `bootstyle` support for consistent theming
- `surface_color` integration (when used by the style system)
- `textsignal` for reactive text synchronization

This makes `Entry` a reliable primitive for both direct use and composition.

---

## Core concepts

### Entry vs TextEntry

It’s important to distinguish the primitive `Entry` from the higher-level `TextEntry` control:

**Entry**

  - Single-line text field only
  - Direct ttk options (validate, validatecommand, show, etc.)
  - Best for lightweight or custom compositions

**TextEntry (control)**

  - Label, helper text, validation messages (control-level UX)
  - Standardized events (`on_input`, `on_changed`)
  - Better choice for “form fields” in most apps

!!! tip "Rule of thumb"
    Use **TextEntry** for application forms, and **Entry** when you need a raw primitive."

---

### Reactive text with `textsignal`

`Entry` supports `textsignal`, which is a reactive signal linked to the entry text and auto-synced with `textvariable`.

```python
import ttkbootstrap as ttk

entry = ttk.Entry(app, textsignal=my_signal)
```

This is useful if your application uses signals to drive state and you want the entry to stay in sync without manual variable plumbing.

<!--
IMAGE: Reactive text signal
Suggested: Diagram-style image showing signal -> Entry text synchronization
-->

---

## Common options & patterns

### Masked input (show)

`show` substitutes typed characters with a masking character:

```python
ttk.Entry(app, show="•")
```

!!! note "Password input"
    For a full-featured password field (reveal toggle, validation, messages), prefer `PasswordEntry`.

---

### Validation (validate / validatecommand)

Tk validation is powerful but low-level. Use it when you need immediate, per-keystroke validation.

```python
import ttkbootstrap as ttk

app = ttk.Window()

def validate_text(new_value: str) -> bool:
    return new_value.isdigit() or new_value == ""

vcmd = (app.register(validate_text), "%P")

entry = ttk.Entry(app, validate="key", validatecommand=vcmd)
entry.pack(padx=20, pady=20)

app.mainloop()
```

!!! tip "Prefer control-level validation for forms"
    For most “form field” UX, use the `*Entry` controls (TextEntry, NumericEntry, DateEntry, etc.) which validate on commit and provide consistent messages and events.

---

### Styling with bootstyle

```python
ttk.Entry(app, bootstyle="primary")
ttk.Entry(app, bootstyle="secondary")
```

You can also supply a concrete ttk style name via `style=...` which overrides bootstyle.

---

## Events

`Entry` uses standard Tk/ttk events. Common ones include:

- `<KeyRelease>` for live typing (low-level)
- `<FocusOut>` for commit-style workflows

```python
entry.bind("<KeyRelease>", lambda e: print(entry.get()))
```

!!! tip "If you want standardized Entry events"
    Prefer `TextEntry` and friends when you want consistent `on_input(...)` and `on_changed(...)` semantics across all entry-style controls.

---

## UX guidance

- Use `Entry` for lightweight, embedded, or custom input situations
- Use `readonly` state to prevent editing while still allowing selection
- Avoid per-keystroke validation unless it meaningfully improves UX

---

## When to use / when not to

**Use Entry when:**

- You need a minimal single-line input
- You’re building your own composite widget or custom validation
- You need direct access to ttk validation options

**Avoid Entry when:**

- You want labels, helper text, and consistent events (use `TextEntry`)
- You need specialized input types (use `NumericEntry`, `DateEntry`, `TimeEntry`, etc.)
- You want modern “form field” UX out of the box

---

## Related widgets

- **TextEntry** — form-ready text control (label/messages/events)
- **PasswordEntry** — specialized masked input control
- **NumericEntry** — locale-aware numeric control
- **Combobox** — selection + optional text entry
