---
title: Reactivity
---

# Reactivity

This guide explains how to connect widgets and application state using signals, callbacks, and events.

---

## Three Mechanisms

ttkbootstrap provides three ways to respond to changes:

| Mechanism | Purpose | Use For |
|-----------|---------|---------|
| **Signals** | Reactive state | Values that multiple widgets share |
| **Callbacks** | Direct actions | Button clicks, menu selections |
| **Events** | Low-level input | Keyboard, mouse, focus |

Each has its place. Understanding when to use each makes applications cleaner.

---

## Signals

Signals represent **state that can be observed**.

```python
import ttkbootstrap as ttk

app = ttk.App()

# Create a signal
name = ttk.Signal("")

# Connect an entry to the signal
entry = ttk.TextEntry(app, signal=name)
entry.pack(padx=20, pady=10)

# React to signal changes
def on_name_changed(value):
    print(f"Name changed to: {value}")

name.subscribe(on_name_changed)

app.mainloop()
```

Key characteristics:

- Signals hold a value that changes over time
- Multiple widgets can share the same signal
- Subscribers are notified when the value changes
- Widgets don't know about each other—they only know the signal

### Creating Signals

```python
# String signal
name = ttk.Signal("")

# Boolean signal
enabled = ttk.Signal(False)

# Numeric signal
count = ttk.Signal(0)

# Any type
selection = ttk.Signal(None)
```

### Reading and Writing

```python
# Get current value
current = name.get()

# Set value (notifies subscribers)
name.set("Alice")

# Alternative property access
current = name.value
name.value = "Alice"
```

### Subscribing

```python
def on_changed(value):
    print(f"New value: {value}")

# Subscribe
name.subscribe(on_changed)

# Unsubscribe
name.unsubscribe(on_changed)
```

Subscribers receive the new value whenever it changes.

### Connecting Widgets

Many widgets accept a `signal` parameter:

```python
name = ttk.Signal("")

# Entry updates the signal
entry = ttk.TextEntry(app, signal=name)

# Label displays the signal
label = ttk.Label(app, textvariable=name)
```

When the entry changes, the label updates automatically.

### Mapping and Transforming

Create **derived signals** by mapping a source signal through a transform function:

```python
import ttkbootstrap as ttk

app = ttk.App()

# Source signal
celsius = ttk.Signal(0)

# Derived signal: transforms celsius to fahrenheit
fahrenheit = celsius.map(lambda c: c * 9/5 + 32)

# UI
ttk.Label(app, text="Celsius:").pack()
ttk.Scale(app, from_=0, to=100, variable=celsius).pack(fill="x", padx=20)

ttk.Label(app, text="Fahrenheit:").pack(pady=(20, 0))
ttk.Label(app, textvariable=fahrenheit).pack()

app.mainloop()
```

When `celsius` changes, `fahrenheit` updates automatically with the transformed value.

#### Common Mapping Patterns

**Formatting for display:**

```python
price = ttk.Signal(29.99)

# Format as currency
display_price = price.map(lambda p: f"${p:.2f}")

ttk.Label(app, textvariable=display_price)  # Shows "$29.99"
```

**Boolean to text:**

```python
is_enabled = ttk.Signal(True)

# Map boolean to descriptive text
status_text = is_enabled.map(lambda v: "Enabled" if v else "Disabled")

ttk.Label(app, textvariable=status_text)
```

**Validation state:**

```python
username = ttk.Signal("")

# Derive validity
is_valid = username.map(lambda u: len(u) >= 3)

# Derive message
validation_msg = username.map(
    lambda u: "" if len(u) >= 3 else "Username must be at least 3 characters"
)
```

**Chaining transforms:**

```python
raw_input = ttk.Signal("  hello world  ")

# Chain multiple transforms
cleaned = raw_input.map(str.strip).map(str.title)

# cleaned.get() returns "Hello World"
```

#### Combining Multiple Signals

For transformations that depend on multiple signals, use `subscribe` with manual updates:

```python
width = ttk.Signal(10)
height = ttk.Signal(20)
area = ttk.Signal(0)

def update_area(*_):
    area.set(width.get() * height.get())

width.subscribe(update_area)
height.subscribe(update_area)
update_area()  # Initialize
```

Or create a helper for common cases:

```python
def combine(signals, transform):
    """Create a signal that combines multiple source signals."""
    result = ttk.Signal(transform(*[s.get() for s in signals]))

    def update(*_):
        result.set(transform(*[s.get() for s in signals]))

    for s in signals:
        s.subscribe(update)

    return result

# Usage
width = ttk.Signal(10)
height = ttk.Signal(20)
area = combine([width, height], lambda w, h: w * h)
```

!!! link "Signal API"
    See [`ttkbootstrap.Signal`](../reference/utils/Signal.md) for all methods.

---

## Callbacks

Callbacks handle **discrete actions**.

```python
import ttkbootstrap as ttk

app = ttk.App()

def on_submit():
    print("Form submitted!")

ttk.Button(app, text="Submit", command=on_submit).pack(pady=20)

app.mainloop()
```

Callbacks are:

- fired once per action
- tied to a specific widget
- good for commands, not ongoing state

### Common Callback Patterns

#### Button Click

```python
def save_file():
    # ... save logic ...
    pass

ttk.Button(app, text="Save", command=save_file)
```

#### With Arguments

```python
def delete_item(item_id):
    print(f"Deleting {item_id}")

# Use lambda to pass arguments
ttk.Button(app, text="Delete", command=lambda: delete_item(42))
```

#### Reading State in Callbacks

```python
name = ttk.Signal("")

def on_submit():
    current_name = name.get()
    print(f"Submitting: {current_name}")

entry = ttk.TextEntry(app, signal=name)
button = ttk.Button(app, text="Submit", command=on_submit)
```

The callback reads the signal's current value when invoked.

---

## Events

Events handle **low-level input** like keyboard and mouse.

```python
import ttkbootstrap as ttk

app = ttk.App()

entry = ttk.Entry(app)
entry.pack(padx=20, pady=20)

def on_key(event):
    print(f"Key pressed: {event.keysym}")

entry.bind("<Key>", on_key)

app.mainloop()
```

Events are:

- tied to Tk's event system
- useful for keyboard shortcuts, mouse gestures
- more complex than signals or callbacks

### Common Events

```python
# Keyboard
widget.bind("<Return>", on_enter)
widget.bind("<Escape>", on_escape)
widget.bind("<Control-s>", on_save)

# Mouse
widget.bind("<Button-1>", on_left_click)
widget.bind("<Double-Button-1>", on_double_click)
widget.bind("<Enter>", on_mouse_enter)  # Hover
widget.bind("<Leave>", on_mouse_leave)

# Focus
widget.bind("<FocusIn>", on_focus)
widget.bind("<FocusOut>", on_blur)
```

### Virtual Events

Some widgets emit virtual events for semantic actions:

```python
def on_selection_changed(event):
    print("Selection changed")

listview.bind("<<SelectionChange>>", on_selection_changed)
```

#### Convenience Methods

Many ttkbootstrap widgets provide `on_*` and `off_*` methods that abstract common event bindings. **Prefer these over manual binding when available**:

```python
# Preferred: use convenience methods
def handle_change(event):
    print("Value changed:", event.data)

# on_* returns a bind_id for later removal
bind_id = entry.on_changed(handle_change)

# Later, to remove the binding, pass the bind_id
entry.off_changed(bind_id)
```

This is cleaner than manual binding:

```python
# Manual binding (works, but prefer on_* methods)
bind_id = entry.bind("<<Changed>>", handle_change)
entry.unbind("<<Changed>>", bind_id)
```

#### Generating Virtual Events

Use `event_generate` to programmatically emit a virtual event:

```python
# Emit an event on a widget
widget.event_generate("<<MyCustomEvent>>")
```

**Event scope**: Virtual events propagate up the widget hierarchy. A binding on a parent widget will receive events generated by its children:

```python
# Parent binds to event
app.bind("<<FormSubmitted>>", on_form_submitted)

# Child generates event — parent receives it
submit_button.event_generate("<<FormSubmitted>>")
```

This enables loose coupling: children emit events, parents handle them.

#### Enhanced Virtual Events with Data

ttkbootstrap extends Tk's virtual events to support **passing data** through the event object:

```python
# Generate event with data
widget.event_generate("<<ItemSelected>>", data={"id": 42, "name": "Alice"})

# Handler receives data in event.data
def on_item_selected(event):
    print(f"Selected: {event.data['name']} (ID: {event.data['id']})")

widget.bind("<<ItemSelected>>", on_item_selected)
```

This is particularly useful for:

- Passing selected items from lists or tables
- Communicating form values on submission
- Custom widget-to-parent communication

```python
# Real-world example: custom list widget
class ItemList(ttk.Frame):
    def select_item(self, item):
        self._selected = item
        # Emit event with the selected item as data
        self.event_generate("<<ItemSelected>>", data=item)

# Parent handles the event
def on_selected(event):
    item = event.data
    print(f"User selected: {item}")

item_list = ItemList(app)
item_list.bind("<<ItemSelected>>", on_selected)
```

!!! link "Events & Bindings"
    See [Platform → Events & Bindings](../platform/events-and-bindings.md) for the full event system.

---

## Choosing the Right Mechanism

### Use Signals When

- Multiple widgets need the same value
- State should persist across interactions
- You want reactive updates

```python
# Good: shared username across form
username = ttk.Signal("")
entry = ttk.TextEntry(app, signal=username)
preview = ttk.Label(app, textvariable=username)
```

### Use Callbacks When

- A button or action triggers something
- The action happens once, not continuously
- There's a clear "do this" moment

```python
# Good: button submits form
ttk.Button(app, text="Submit", command=submit_form)
```

### Use Events When

- You need keyboard shortcuts
- You need mouse interaction details
- You're handling focus or hover

```python
# Good: keyboard shortcut
app.bind("<Control-s>", lambda e: save_file())
```

---

## Combined Patterns

### Form with Submit

```python
import ttkbootstrap as ttk

app = ttk.App()

# State
username = ttk.Signal("")
password = ttk.Signal("")

# UI
form = ttk.PackFrame(app, direction="vertical", gap=10, padding=20)
form.pack(fill="both", expand=True)

form.add(ttk.Label(form, text="Username:"))
form.add(ttk.TextEntry(form, signal=username))

form.add(ttk.Label(form, text="Password:"))
form.add(ttk.PasswordEntry(form, signal=password))

# Submit reads current signal values
def on_submit():
    print(f"Login: {username.get()} / {password.get()}")

form.add(ttk.Button(form, text="Login", command=on_submit))

app.mainloop()
```

### Live Preview

```python
import ttkbootstrap as ttk

app = ttk.App()

# Signal for shared state
content = ttk.Signal("Type here...")

main = ttk.PackFrame(app, direction="horizontal", gap=20, padding=20)
main.pack(fill="both", expand=True)

# Editor
editor = ttk.ScrolledText(main, width=40, height=10)
main.add(editor, fill="both", expand=True)

# Preview updates reactively
preview = ttk.Label(main, wraplength=200)
main.add(preview)

# Connect editor changes to preview
def sync_to_preview(event=None):
    preview.configure(text=editor.get("1.0", "end-1c"))

editor.bind("<KeyRelease>", sync_to_preview)

app.mainloop()
```

### Keyboard Shortcuts

```python
import ttkbootstrap as ttk

app = ttk.App()

def save():
    print("Saving...")

def quit_app():
    app.destroy()

# Global shortcuts
app.bind("<Control-s>", lambda e: save())
app.bind("<Control-q>", lambda e: quit_app())

ttk.Label(app, text="Press Ctrl+S to save, Ctrl+Q to quit").pack(pady=20)

app.mainloop()
```

---

## What Signals Are Built On

Signals are implemented using Tk variables (`StringVar`, `IntVar`, etc.) with traces.

This means:

- Signals work with any Tk widget
- They integrate with Tk's event loop
- They're not a separate system—they're Tk-native

The Signal API provides a cleaner interface:

| Tk Variables | Signals |
|--------------|---------|
| `var.trace_add()` | `signal.subscribe()` |
| `var.get()` | `signal.get()` / `signal.value` |
| `var.set()` | `signal.set()` / `signal.value = ...` |

!!! link "Signals Capability"
    See [Capabilities → Signals](../capabilities/signals/signals.md) for implementation details.

---

## Summary

- **Signals** for shared state and reactive updates
- **Callbacks** for discrete actions (button clicks)
- **Events** for low-level input (keyboard, mouse)

Use signals when state is shared. Use callbacks when an action happens. Use events when you need input details.

---

## Next Steps

- [App Structure](app-structure.md) — how applications are organized
- [Layout](layout.md) — building layouts with containers
- [Styling](styling.md) — applying consistent styling
