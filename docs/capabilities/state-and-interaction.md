---
title: State & Interaction
---

# State & Interaction

ttk widgets carry a small set of *state flags* (`disabled`, `focus`,
`hover`, `selected`, `pressed`, `active`, `alternate`, `invalid`,
`readonly`, `background`, plus arbitrary user states) that style maps
read to choose colors, fonts, and images. ttkbootstrap exposes the
stock ttk `state()` / `instate()` API plus a handful of
framework-specific extensions on top:

- a global keyboard-vs-mouse focus tracker that repurposes the
  `'background'` state flag,
- a `focus_set(visual_focus=True)` switch for showing the focus ring
  on programmatic focus,
- a thin `BusyMixin` and `GrabMixin` for input-blocking and modal
  capture.

For the reactive *value* layer (`Signal`, `<<Change>>`, `command=`),
see [Signals & Events](signals/index.md). This page covers the
*interaction* layer: who has focus, what state flags are set, who
captures pointer events.

---

## At a glance

| Concern | Surface | What it does |
|---|---|---|
| ttk state flags | `widget.state(...)`, `widget.instate(...)` | Read or modify the per-widget visual state set used by style maps |
| Disabled / readonly | `configure(state=...)` and `cget('state')` | The widget *option* — coupled to the state flag in one direction (see below) |
| Focus | `focus_set()`, `focus_force()`, `focus_get()`, `tk_focusNext()` | Move keyboard focus; query the focused widget |
| Visual focus ring | `focus_set(visual_focus=True)` | Show the ring on programmatic focus (default off) |
| Keyboard focus marker | `'background'` ttk state, set on Tab | Lets style maps show the ring only on keyboard navigation |
| Pointer / keyboard grab | `grab_set()`, `grab_release()`, `grab_status()` | Confine events to a window subtree (modal foundation) |
| Input block (busy) | `busy_hold()`, `busy_forget()`, `busy_status()` | Drape an input-only window over a subtree to block clicks |

---

## ttk state flags

`widget.state(spec)` modifies the widget's state set; `widget.state()`
with no argument returns the current set as a tuple.

```python
import ttkbootstrap as ttk

app = ttk.App()
b = ttk.Button(app, text="Save")
b.pack()

b.state()                       # ()
b.state(['disabled'])
b.state()                       # ('disabled',)
b.state(['!disabled', 'focus'])
b.state()                       # ('focus',)

app.mainloop()
```

A spec is a sequence of state names. A bare name *adds* the flag; a
`!`-prefixed name *removes* it. Multiple flags in one call are
applied in order. `widget.state(spec)` returns the *previous* spec
that would undo the change — useful for save-and-restore patterns.

The stock ttk states (Tk 8.6+) are:

| Flag | Meaning |
|---|---|
| `active` | Pointer is over the widget (some themes) |
| `alternate` | Tristate / indeterminate (CheckButton, Progressbar) |
| `background` | Window is inactive — repurposed by ttkbootstrap as the keyboard-focus marker (see below) |
| `disabled` | Widget rejects user input |
| `focus` | Widget has the keyboard focus |
| `hover` | Pointer is over the widget (Tk 8.6+ canonical name) |
| `invalid` | Validation has marked the widget invalid |
| `pressed` | Widget is being pressed/clicked |
| `readonly` | Widget displays a value but rejects user typing |
| `selected` | Widget is selected (CheckButton checked, RadioButton chosen, Tab active) |

Arbitrary additional names (`'user1'`, `'user2'`, or any string)
are accepted and round-trip through `state()` — useful for
custom style-map keys without colliding with the stock vocabulary.

!!! warning "`state()` and `instate()` require an iterable, not a string"

    Despite the type hint suggesting `str | Iterable[str]`, passing a
    bare string causes Tk to join character-by-character. `b.state('disabled')`
    raises `TclError: Invalid state name d` because the implementation
    runs `' '.join('disabled')` → `'d i s a b l e d'`. Always wrap a
    single flag in a list: `b.state(['disabled'])`.

### `instate(...)` — testing state

`widget.instate(spec)` returns `True` if every flag in the spec
matches the widget's current state. The match is conjunctive (AND),
not disjunctive — `instate(['disabled', 'focus'])` is `True` only
when *both* are set.

```python
b.state(['disabled'])
b.instate(['disabled'])             # True
b.instate(['!disabled'])            # False
b.instate(['disabled', 'focus'])    # False — focus not set
```

A second argument can be a callback invoked when the test passes:

```python
b.instate(['disabled'], lambda: print("user can't click"))
# When True, the callback runs and instate returns its return value.
# When False, instate returns False without calling the callback.
```

---

## State flag vs `state` widget option

ttk widgets carry **two** independent representations of the
disabled / readonly / normal axis:

- The `state` *option* — read with `cget('state')`, written with
  `configure(state='normal' | 'disabled' | 'readonly')`. This is the
  Tk-side widget option.
- The `disabled` and `readonly` *state flags* — read with `state()`,
  written with `state(['disabled'])` / `state(['readonly'])`.

`configure(state=...)` writes both: the option and the matching state
flag. The reverse is **not symmetric** — clearing a flag with
`state(['!disabled'])` leaves the option untouched.

```python
e = ttk.Entry(app)

e.configure(state='disabled')
e.cget('state')          # 'disabled'   — option set
e.state()                # ('disabled',) — flag set
e.state(['!disabled'])
e.cget('state')          # 'disabled'   — option still set!
e.state()                # ()           — flag cleared
```

The flag is what style maps consult, so the visual will look enabled
after the second call — but `cget('state')` (and any code that
queries it) will still report `disabled`. Use `configure(state=...)`
on either side of the round trip for consistency, or read state via
`instate(['disabled'])` when in doubt.

`'readonly'` is supported by `Entry`, `Combobox`, and `Spinbox` only
on the option side. The state flag is set freely on any ttk widget
but only those three honor it as input-rejection behavior.

### Tk widgets have only the option

`Text`, `Canvas`, `Listbox`, and the other classic Tk widgets do not
have a `state()` method — only `configure(state='normal' |
'disabled')`:

```python
text = ttk.Text(app)
text.state(...)                    # AttributeError
text.configure(state='disabled')   # OK
text.cget('state')                 # 'disabled'
```

For a `Text` widget, `state='disabled'` blocks user typing *and*
silently no-ops programmatic `insert()` / `delete()` — see
[Primitives → Text](../widgets/primitives/text.md).

---

## Focus

`focus_set()` requests keyboard focus for a widget. `focus_get()`
returns the widget that currently holds it (or `None` if no widget
in this application has focus).

```python
e = ttk.Entry(app)
e.pack()
e.focus_set()              # request focus
app.focus_get()            # → <Entry .!entry>
```

Tk remembers the most recent focused descendant for each toplevel.
When the window manager hands focus back to a toplevel, Tk redirects
it to that remembered widget — `focus_lastfor()` returns who that
would be.

`focus_force()` overrides the window manager and steals focus
unconditionally; reserve it for first-launch setup or recovery from
a wedged state. For ordinary "focus this field after validation
failure" use `focus_set()`.

`tk_focusNext()` and `tk_focusPrev()` walk the Tab traversal order
(see [Platform → Accessibility](../platform/accessibility.md) for
the rules that govern who's in the chain).

### Visual focus — the `'background'` state trick

ttkbootstrap installs a global Tab-key tracker on import
(`runtime/visual_focus.py`) that flips the `'background'` ttk state
on whichever widget receives focus *via the Tab key*, and clears it
on `<FocusOut>`. The flag is normally used to indicate an inactive
window — rarely styled in practice — so the framework reuses it as
a "this focus came from the keyboard" marker.

Style maps then key off the combined state:

```text
('background focus', focus_ring_color),  # keyboard focus → show ring
('focus', ''),                           # mouse focus → no ring
```

This is the Tk equivalent of CSS `:focus-visible`: clicking a button
focuses it but does not draw a ring; tabbing to the same button
does. Mouse focus produces only the bare `'focus'` flag; keyboard
focus produces both `'focus'` and `'background'`.

Programmatic focus defaults to the no-ring path. Pass
`visual_focus=True` to `focus_set` (or `focus_force`) when you want
the ring drawn — typically after validation failure when you want to
draw the user's eye to the field:

```python
def submit():
    if not entry.get().strip():
        entry.focus_set(visual_focus=True)
        return
    # ... save data
```

The helper `is_keyboard_focus(widget)` from
`ttkbootstrap.runtime.visual_focus` returns `True` when both flags
are set — useful for code that needs to react to keyboard-focused
state rather than any focused state.

---

## Pointer / keyboard grabs

A grab confines pointer and keyboard events to a window subtree —
the foundation for modal interaction. While a grab is held, clicks
outside the grab subtree are ignored (or rerouted to the grab
window, depending on the platform).

| Method | What it does |
|---|---|
| `grab_set()` | Set a *local* grab — events confined within this Tk application |
| `grab_set_global()` | Set a *global* grab — events confined at the window-system level |
| `grab_release()` | Release the grab (always pair with the set in a `try` / `finally`) |
| `grab_status()` | `'local'`, `'global'`, or `None` |
| `grab_current()` | The widget holding the grab in this application, or `None` |

```python
top = ttk.Toplevel(master=app, title="Confirm")
top.grab_set()
top.grab_status()      # 'local'
top.grab_current()     # <Toplevel .!toplevel>

top.grab_release()
top.grab_status()      # None
```

A grab does **not** make a window modal on its own. The full modal
recipe is `transient(parent)` + `grab_set()` + `wait_window(top)` —
this is what the framework's [`Dialog`](../widgets/dialogs/dialog.md)
base class assembles. See `dialogs/dialog.py` for the canonical
shape.

Avoid `grab_set_global()` outside narrow cases (color-picker
dropper, modal system overlays); a global grab can make the entire
desktop feel stuck if the application crashes before releasing it.

---

## Busy — blocking input on a subtree

`busy_hold()` drapes an input-only Tk window over a widget (and its
descendants), intercepting pointer events. Use it during long-
running synchronous work that you can't move off the main thread —
file I/O on small files, schema migrations, single-pass renders.

| Method | What it does |
|---|---|
| `busy_hold(**opts)` | Activate busy mode; common option is `cursor='watch'` |
| `busy_forget()` | Deactivate busy mode |
| `busy_status()` | `True` if busy mode is active |
| `busy_configure(**opts)` | Query or update busy options without toggling |
| `busy_cget(option)` | Read a single busy option |

```python
content = ttk.Frame(app)
content.pack()

content.busy_hold(cursor="watch")
try:
    # ... long synchronous work
    pass
finally:
    content.busy_forget()
```

Caveats:

- Busy blocks pointer events only. Keyboard events may still reach
  focused widgets — pair with `focus_set()` on a non-busy area if
  full input lockout matters.
- Always release in a `finally` block. If the application crashes
  with busy held, the subtree stays unresponsive until the
  application restarts.
- For genuinely long work, prefer moving off the main thread — see
  [Platform → Threading & Async](../platform/threading-and-async.md).
  Busy is a UX patch for short blocking work, not a substitute for
  background execution.

---

## Where state and interaction meet other capabilities

- **Signals** carry the *value* a widget displays; *state* describes
  how the widget is rendering it (enabled, focused, hovered). A
  signal write doesn't touch state; a state change doesn't touch the
  signal. See [Signals & Events](signals/index.md).
- **Validation** writes the `'invalid'` state flag (and
  `'!invalid'` to clear it) — that's what marks a field with the
  error treatment. See [Validation](validation/index.md).
- **Selection** widgets (`CheckButton`, `RadioButton`, `Tabs`) use
  the `'selected'` state flag; the framework toggles it when the
  bound variable changes. See
  [Selection widgets](../widgets/selection/checkbutton.md).
- **Dialog modality** combines `transient`, `grab_set`, and
  `wait_window` — see [Platform → Windows](../platform/windows.md).
- **Configuration** pins the *initial* state (`state='disabled'`
  in widget kwargs); state and interaction describe how it changes
  afterwards. See [Configuration](configuration.md).

---

## Where to read next

- *"How do I render a focus ring only on keyboard navigation?"* —
  this page above; the `'background focus'` state-map key.
- *"How do I disable a widget so it ignores clicks?"* —
  `widget.configure(state='disabled')`. Use this rather than
  `state(['disabled'])` so `cget('state')` stays in sync.
- *"How do I show that a field failed validation?"* — set the
  `'invalid'` state flag (the framework does this for you when a
  `ValidationRule` fails); see [Validation → Results](validation/results.md).
- *"How do I block input during a long operation?"* —
  `widget.busy_hold(cursor='watch')` for short work;
  [Threading & Async](../platform/threading-and-async.md) for long
  work.
- *"How do I make a dialog modal?"* — `transient` + `grab_set` +
  `wait_window`. See the [Dialog](../widgets/dialogs/dialog.md)
  base class for the canonical shape.
