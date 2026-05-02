# Events & Bindings

Tk delivers user input and system notifications through a binding
system. A **binding** associates an event sequence (`<Button-1>`,
`<KeyPress>`, `<<Selected>>`) with a callback. When the event fires,
Tk walks the receiving widget's **bindtag list** and invokes every
matching binding it finds along the way.

This page is the mechanics: the bindtag walk, the three binding
scopes, the `event` object, modifier and virtual-event syntax, and the
most common ways binding code goes wrong.

For the higher-level "subscribe to a value, react to a change" model,
see [Capabilities → Signals](../capabilities/signals/index.md).

---

## What an event sequence is

An event sequence is a string in angle brackets describing the input
or notification to match:

| Sequence | What it matches |
|---|---|
| `<Button-1>` | Mouse button 1 (left) pressed |
| `<ButtonRelease-1>` | Mouse button 1 released |
| `<Motion>` | Pointer moved while inside the widget |
| `<KeyPress>` (or `<Key>`) | Any key pressed while widget has focus |
| `<KeyPress-Return>` (or `<Return>`) | Return/Enter pressed |
| `<Configure>` | Widget geometry changed (resize, move) |
| `<Enter>`, `<Leave>` | Pointer entered or left widget bounds |
| `<FocusIn>`, `<FocusOut>` | Widget gained or lost focus |
| `<<MyEvent>>` | A *virtual event* named `MyEvent` (double angle brackets) |

Tk parses the sequence into a normalized form, so `<Button-1>`,
`<1>`, and `<ButtonPress-1>` all match the same event. Modifier keys
are prepended with hyphens — `<Shift-Button-1>`,
`<Control-KeyPress-c>`, `<Alt-F4>`. See **Modifier keys**, below.

---

## The bindtag walk

Every widget carries an ordered list of bindtags. When an event
arrives, Tk walks the list and runs **all** bindings registered for
that event sequence on each tag, in order.

The default list for any widget is:

```python
import ttkbootstrap as ttk
app = ttk.App()
btn = ttk.Button(app, text="OK")
btn.bindtags()
# ('.!button', 'TButton', '.', 'all')
```

| Position | Tag | Scope |
|---|---|---|
| 1 | Widget path (e.g. `'.!button'`) | This widget instance only |
| 2 | Class name (e.g. `'TButton'`) | Every widget of this class — Tk's stock behavior lives here |
| 3 | Toplevel path (e.g. `'.'`) | Every widget under the root or any toplevel |
| 4 | `'all'` | Every widget in the application |

Tk runs every matching binding it finds at each tag, then moves to the
next tag. A handler can return the string `"break"` to stop the walk;
otherwise all four tags are visited.

You can rearrange or extend the list with `widget.bindtags((...))`.
Custom bindtags are useful when you want to share a binding across an
ad-hoc group of widgets that don't share a class — give them a custom
tag like `"DraftMode"` and bind once with `widget.bind_class("DraftMode",
event, fn)`.

---

## The three binding scopes

| Call | Tag affected | Use when |
|---|---|---|
| `widget.bind(event, fn)` | Widget instance (tag 1) | One specific widget needs a handler |
| `widget.bind_class("TButton", event, fn)` | Class (tag 2) | Modify the default behavior of every widget of a class — rare; usually bad practice |
| `widget.bind_all(event, fn)` | The `"all"` tag (tag 4) | App-wide shortcut handlers, debugging, focus tracing |

`bind_class` is dangerous because it changes Tk's stock behavior for
every instance of that class — including widgets in third-party code.
Reach for a custom bindtag instead if you need to share behavior.

`bind_all` is the canonical way to register an app-wide keyboard
shortcut. ttkbootstrap's `Shortcuts` service builds on it; see
**Modifier keys**, below.

---

## Replace or append: the `add` argument

`bind`, `bind_class`, and `bind_all` all take an optional third
argument that controls what happens when a binding already exists for
the same event sequence on the same tag:

| `add` value | Behavior |
|---|---|
| omitted, `None`, or `""` (default) | **Replace** the existing binding |
| `"+"` or `True` | **Append** — both bindings fire, in registration order |

The default is *replace*. This is the most common source of "my
handler stopped firing" bugs — a later piece of code (a tooltip
attachment, a debug instrumentation, a third-party library) silently
overwrites your binding. Use `add="+"` whenever you mean "in addition
to anything that's already there":

```python
# Adds a new handler without disturbing existing binds
widget.bind("<Enter>", on_enter, add="+")
```

The `bind` call returns a *funcid* string. Pass it to `unbind` to
remove just that one handler when multiple are stacked:

```python
funcid = widget.bind("<Enter>", on_enter, add="+")
# ...later...
widget.unbind("<Enter>", funcid)
```

Calling `unbind("<Enter>")` with no funcid removes **every** binding
for that event on the widget — easy to do by accident.

---

## Stopping propagation

A handler can return the string `"break"` to stop the bindtag walk
mid-way:

```python
def on_click(event):
    handle_locally()
    return "break"
```

This is the canonical way to override Tk's class-level default
behavior from a widget-level handler. For example, a `Text` widget's
`<Tab>` defaults (insert a tab character) can be replaced with focus
traversal:

```python
def focus_next(event):
    event.widget.tk_focusNext().focus()
    return "break"

text.bind("<Tab>", focus_next)
```

Without `"break"`, both your handler and the class-level default fire,
and the user gets focus traversal *and* an inserted tab.

Use `"break"` deliberately. Returning it from a binding on the `"all"`
tag, for example, can suppress framework behavior in surprising ways.

---

## The event object

Every callback receives a single `event` argument with these
attributes (omitted attributes are `??`):

| Attribute | Meaning |
|---|---|
| `event.widget` | The widget that received the event (always set) |
| `event.x`, `event.y` | Pointer position, widget-relative pixels |
| `event.x_root`, `event.y_root` | Pointer position, screen-relative pixels |
| `event.num` | Mouse button number (1=left, 2=middle, 3=right; macOS may differ) |
| `event.keysym` | Symbolic key name (`"Return"`, `"BackSpace"`, `"a"`) |
| `event.keysym_num` | Numeric keysym |
| `event.char` | The character produced by the keypress, or `""` |
| `event.state` | Bitmask of active modifiers and mouse buttons |
| `event.delta` | Mouse wheel delta (sign and magnitude vary by platform) |
| `event.width`, `event.height` | Widget size (set on `<Configure>`) |
| `event.data` | Payload of a virtual event (see **Virtual events**) |
| `event.type` | The event type as a `tk.EventType` enum |

Not every attribute is meaningful for every event. `event.x` on a
`<<ItemSelected>>` virtual event, for instance, is `0`.

---

## Modifier keys

Modifiers are prepended to the event sequence with hyphens:

```python
widget.bind("<Shift-Button-1>", shift_click)
widget.bind("<Control-c>", copy)
widget.bind("<Alt-F4>", quit_app)
```

The case-sensitive single-letter form (`<Control-c>`) matches lowercase
'c'; `<Control-C>` matches Shift-Ctrl-C. For control characters, the
`<Control-...>` form is the modern syntax — `<Control-Key-c>` and
`<Control-c>` are equivalent.

**Cross-platform "primary modifier".** Cmd on macOS, Ctrl on Windows
and Linux. Tk has no built-in symbol for "the primary modifier"; you'd
otherwise need to register `<Command-s>` on macOS and `<Control-s>`
elsewhere by hand. ttkbootstrap's `Shortcuts` service does this for
you:

```python
import ttkbootstrap as ttk
from ttkbootstrap import get_shortcuts

shortcuts = get_shortcuts()
shortcuts.register("save", "Mod+S", save_file)
shortcuts.register("quit", "Mod+Q", lambda: app.destroy())
shortcuts.bind_to(app)              # binds all registered shortcuts
shortcuts.binding("save")           # '<Command-s>' on macOS, '<Control-s>' elsewhere
```

`Mod` resolves to `Command` on macOS and `Control` everywhere else.
The `Shortcut.display` property formats the same shortcut for display
in menus (`"⌘S"` on macOS, `"Ctrl+S"` elsewhere).

---

## Virtual events

Virtual events are application-defined names in double angle brackets.
They decouple *what changed* from *what input triggered the change*:

```python
# Subscribe
widget.bind("<<Selected>>", on_selected)

# Emit
widget.event_generate("<<Selected>>", data={"item_id": 42})
```

The `data=` keyword is passed through Tk's `-data` attribute and
arrives on the receiver as `event.data`. In current Tk versions the
data is passed through unchanged when the value is a Python object
(dict, list, etc.); older Tk required string-only values.

**Virtual events do not bubble.** This is the most common source of
"I bound the event but my handler never runs" bugs in framework code.
A virtual event emitted on a child widget does *not* propagate to its
parent — the only way the parent receives it is if you re-emit on the
parent:

```python
def on_child_selected(event):
    parent.event_generate("<<Selected>>", data=event.data)
```

Several ttkbootstrap composites currently document virtual events as
"bubbled from child" but don't actually re-emit. See the bug list in
the docs review plan for the specific cases (`Tabs.<<TabSelect>>`,
`SideNav.<<ItemInvoked>>`, `PageStack.<<PageWillMount>>` /
`<<PageUnmount>>`). Bind directly on the emitting child until the
framework forwards them.

---

## Posting events from code

Use `event_generate` to inject any event — physical or virtual — into
the queue:

```python
# Simulate a click for testing
btn.event_generate("<Button-1>", x=5, y=5)

# Fire a virtual event with payload
view.event_generate("<<DataChanged>>", data={"rows": 12})
```

The event is appended to the event queue and dispatched the next time
the event loop drains it. See [Event Loop](event-loop.md) for the
queue model.

---

## Common pitfalls

**Silent overwrite without `add="+"`.** A second `bind` call replaces
the first. The framework's `ToolTip` constructor uses hard binds for
`<Enter>` / `<Leave>` / `<Motion>` and clobbers any pre-existing
handlers — pre-bind your own `<Enter>` *first*, attach the tooltip
*after*, and use `add="+"` for any handler that should coexist.

**Class binds change every widget.** `bind_class("TButton", ...)`
affects every Button in the app, including third-party ones. Use a
custom bindtag instead.

**Returning `"break"` accidentally.** Any non-`None` return value
counts as "stop propagation" if it stringifies to `"break"`. A handler
that returns a Python literal `"break"` for an unrelated reason
silently disables every later binding.

**Modifier case in keysyms.** `<Control-A>` matches Shift-Ctrl-A, not
Ctrl-A. For ASCII letters, write `<Control-a>` (or use `Shortcuts`).

**Forgotten unbind on destroy.** Bindings on `bind_all` or
`bind_class` outlive the destroyed widget unless you clean up with
`unbind_all` / `unbind_class`. Plain `widget.bind` is reaped
automatically with the widget.

**Reading `event.x` on virtual events.** Virtual events carry only
`event.data` (and `event.widget` / `event.type`). Geometry attributes
default to `0`.

---

## Next steps

- [Event Loop](event-loop.md) — how dispatched events fit into the
  queue model and how `event_generate` interacts with `after`.
- [Capabilities → Virtual Events](../capabilities/signals/virtual-events.md)
  — the framework's conventions for naming and using virtual events.
- [Capabilities → Signals](../capabilities/signals/index.md) — the
  reactive layer most app-level state should live in.
- [Widget Lifecycle](widget-lifecycle.md) — when bindings should be
  registered and torn down.
