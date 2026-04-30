---
title: Dialogs
---

# Dialogs

A dialog is a short, focused window that interrupts the main flow of the
application — confirming a destructive action, prompting for a value,
picking a date or color, filling out a quick form. ttkbootstrap ships
ready-made dialogs for the common cases plus a base class for building
your own.

This guide covers:

- **Choosing the right dialog** — message, input, picker, form, custom
- **The blocking call shape** — `dialog.show()` and `dialog.result`
- **Convenience facades** — `MessageBox` and `QueryBox`
- **Specialized pickers** — date, font, color, filter
- **Multi-field input** — `FormDialog`
- **Custom dialogs** — subclassing or composing `Dialog`
- **Positioning, modality, and dismissal**

The dialog system is layered. From most convenient to most flexible:

1. **`MessageBox` / `QueryBox` facades** — one call, returns a value.
2. **Dedicated dialog classes** — `MessageDialog`, `QueryDialog`,
   `DateDialog`, `FontDialog`, `ColorChooserDialog`, `FilterDialog`,
   `FormDialog`. Construct, configure, `show()`, read `result`.
3. **`Dialog` base class** — your widgets, your buttons, your result.

You can stop at layer 1 for almost everything. Drop down only when you
need control the layer above doesn't expose.

---

## Choosing a dialog

| You want to… | Use |
|---|---|
| Show a message and have the user acknowledge it | `MessageBox.show_info` / `show_warning` / `show_error` / `show_question` |
| Ask the user to confirm an action | `MessageBox.yesno` / `okcancel` / `yesnocancel` |
| Recover from a recoverable failure | `MessageBox.retrycancel` |
| Prompt for a single string, integer, float, or date | `QueryBox.get_string` / `get_integer` / `get_float` / `get_date` |
| Let the user pick one of a fixed list of values | `QueryBox.get_item` |
| Pick a color or font with a rich picker UI | `QueryBox.get_color` / `get_font` (or `ColorChooserDialog` / `FontDialog`) |
| Choose which items in a long list to keep | `FilterDialog` |
| Collect several related fields at once | `FormDialog` |
| Build something none of the above covers | `Dialog` (compose) or subclass it |

For the first six rows the convenience facades (`MessageBox`, `QueryBox`)
are usually all you need. Drop down to the dialog classes themselves
when you need fine-grained control over buttons, validation, or layout.

!!! note "Themed, not native"
    ttkbootstrap dialogs are styled Tk windows — they look the same on
    every platform but do **not** match the OS file or color picker. For
    native behavior (file pickers, system color/font dialogs) use
    Python's `tkinter.filedialog`, `tkinter.colorchooser`, or
    `tkinter.font` modules. See
    [Native vs custom dialogs](../widgets/dialogs/index.md#native-vs-custom-dialogs).

---

## The dialog call shape

Every dialog class in ttkbootstrap follows the same pattern:

```python
import ttkbootstrap as ttk

dialog = ttk.MessageDialog(message="Save changes?", buttons=["Cancel", "Save:primary"])
dialog.show()              # blocks until the user closes it
print(dialog.result)       # "Save", "Cancel", or None
```

`show()` is **modal and blocking** — it waits for the user to respond
before returning. After it returns, read `dialog.result` to find out
what happened.

`result` is `None` when the user dismisses the window without choosing
anything (clicking the close button, pressing `Escape`, or for
`popover` mode clicking outside the dialog). Always handle that case
first:

```python
dialog.show()
if dialog.result is None:
    return                 # user dismissed the dialog — do nothing
if dialog.result == "Save":
    save_document()
```

The `MessageBox` and `QueryBox` facades wrap this pattern into one-line
calls that just return the value (or `None`):

```python
import ttkbootstrap as ttk

name = ttk.QueryBox.get_string(prompt="Project name:", title="New Project")
if name is None:
    return
print(f"Creating {name}")
```

### What `result` contains

The type of `result` depends on the dialog:

| Dialog | `result` on confirm | `result` on cancel |
|---|---|---|
| `MessageDialog` / `MessageBox.*` | button text (`str`) | `None` |
| `QueryDialog` / `QueryBox.get_string` / `get_item` | `str` | `None` |
| `QueryBox.get_integer` / `get_float` | `int` / `float` | `None` |
| `DateDialog` / `QueryBox.get_date` | `datetime.date` | `None` |
| `FontDialog` / `QueryBox.get_font` | `tkinter.font.Font` | `None` |
| `ColorChooserDialog` / `QueryBox.get_color` | `ColorChoice` (`rgb`, `hsl`, `hex`) | `None` |
| `FilterDialog` | `list[Any]` of selected values | `None` |
| `FormDialog` | `dict[str, Any]` of field values | `None` |
| `Dialog` (custom) | whatever you assign — defaults to the clicked button's `result` | `None` |

---

## Message dialogs

Use a message dialog when you need to **tell** or **ask** the user
something.

### One-line confirmations and notifications

`MessageBox` is a static facade with one method per common pattern:

```python
import ttkbootstrap as ttk

# Acknowledgement (single OK button + icon)
ttk.MessageBox.show_info("Settings saved.")
ttk.MessageBox.show_warning("This will reset your preferences.")
ttk.MessageBox.show_error("Could not connect to server.")
ttk.MessageBox.show_question("Continue with the current selection?")

# Plain OK (no icon)
ttk.MessageBox.ok("Build complete.")

# Action choices (no icon)
choice = ttk.MessageBox.yesno("Delete this file?")
if choice == "Yes":
    print("delete")

choice = ttk.MessageBox.okcancel("Apply changes?")
choice = ttk.MessageBox.yesnocancel("Save before closing?")
choice = ttk.MessageBox.retrycancel("Connection failed.")
```

Each method returns the **text of the button pressed** (`"OK"`,
`"Yes"`, `"No"`, `"Cancel"`, `"Retry"`) or `None` if the user dismissed
the dialog. Always test against the actual button text.

The `show_warning` and `show_error` variants ring the system bell by
default; the others don't. Pass `alert=True` (or `alert=False`) on any
of them to override.

### Custom buttons and styling

For non-standard button sets, drop down to `MessageDialog` directly.
Button labels accept a `"text:accent"` syntax that styles the button
with a named accent token:

```python
import ttkbootstrap as ttk

dialog = ttk.MessageDialog(
    message="This will permanently delete 12 files.",
    title="Confirm delete",
    buttons=["Cancel", "Delete:danger"],
)
dialog.show()
if dialog.result == "Delete":
    print("delete")
```

Common accent tokens after the colon: `primary`, `secondary`, `success`,
`info`, `warning`, `danger`. They use the same accent vocabulary as
buttons elsewhere in the library. The last button in the list is the
default (focused, triggered by Enter) unless a `default=` label is
specified explicitly.

`MessageDialog` accepts an `icon=` argument for a Bootstrap icon name
(or a dict with `name`/`size`/`color`) when you want an icon without
using one of the preset variants.

---

## Input prompts

Use an input prompt when you need **a single value** from the user.

### Strings, numbers, and dates

`QueryBox` covers the common cases:

```python
import ttkbootstrap as ttk
from datetime import date

name = ttk.QueryBox.get_string(prompt="New name:", value="Untitled")
count = ttk.QueryBox.get_integer(prompt="How many?", minvalue=1, maxvalue=99)
ratio = ttk.QueryBox.get_float(prompt="Scale factor:", value=1.0)
day = ttk.QueryBox.get_date(value=date.today())
```

Each returns the typed value or `None` on cancel — `get_integer`
returns an `int`, `get_float` returns a `float`, `get_date` returns a
`datetime.date`.

### Picking from a list

`get_item` shows a filterable combobox and returns the chosen string:

```python
import ttkbootstrap as ttk

choice = ttk.QueryBox.get_item(
    prompt="Pick a theme:",
    items=["light", "dark", "system"],
    value="system",
)
```

The user can type to filter the list or pick directly from the
dropdown. The result is the string they confirmed — validated to be
one of `items`, or `None` on cancel.

### Validation, bounds, and formatting

`QueryBox.get_integer` and `get_float` already accept `minvalue` and
`maxvalue`. For tighter control — formatted display (currency, ICU
patterns), an explicit increment, multiline prompts — use `QueryDialog`
directly:

```python
import ttkbootstrap as ttk

dialog = ttk.QueryDialog(
    prompt="Port number:",
    title="Server settings",
    value="8080",
    datatype=int,
    minvalue=1024,
    maxvalue=65535,
)
dialog.show()
port = dialog.result
```

`QueryDialog` swaps in the right field widget for the `datatype`
(`TextEntry`, `NumericEntry`, or `DateEntry`), so out-of-range or
malformed input is rejected before `result` is set.

---

## Specialized pickers

When the value being chosen has a rich UI (a calendar, a color
spectrum, a font preview), use the dedicated picker dialog. The
`QueryBox` one-liners wrap them; the dialog classes are for when you
need extra options (date bounds, custom palettes).

| Picker | Class | One-liner |
|---|---|---|
| Date | `DateDialog` | `QueryBox.get_date(...)` |
| Font | `FontDialog` | `QueryBox.get_font(...)` |
| Color | `ColorChooserDialog` | `QueryBox.get_color(...)` |
| Multi-select filter | `FilterDialog` | — |

```python
import ttkbootstrap as ttk
from datetime import date

color = ttk.QueryBox.get_color(value="#3498db")        # ColorChoice or None
font = ttk.QueryBox.get_font()                          # font.Font or None

picker = ttk.DateDialog(
    initial_date=date.today(),
    min_date=date(2026, 1, 1),
    max_date=date(2026, 12, 31),
)
picker.show()
selected_date = picker.result                           # date or None
```

`get_color` returns a `ColorChoice` named tuple with `.rgb`, `.hsl`,
and `.hex` fields — use `chosen.hex` if you only need the hex string.

`ColorChooserDialog` includes spectrum, themed-palette, and
standard-palette tabs, plus an optional screen "dropper" (Windows /
Linux only) for sampling pixels from anywhere on screen.

`FilterDialog` is the right fit for "let the user pick which of these
items to keep" — a list of checkboxes with optional search and
select-all:

```python
import ttkbootstrap as ttk

columns = ["Name", "Email", "Department", "Hire date", "Manager"]
dialog = ttk.FilterDialog(items=columns, enable_search=True, enable_select_all=True)
dialog.show()
visible = dialog.result   # list of selected items, or None
```

---

## Multi-field input

`FormDialog` embeds a [Form](../widgets/forms/form.md) inside a modal
dialog. Use it when you need **several related fields** in one step:

```python
import ttkbootstrap as ttk

dialog = ttk.FormDialog(
    title="New connection",
    data={"host": "localhost", "port": 5432, "ssl": True},
)
dialog.show()
if dialog.result:
    print(dialog.result)   # dict of field values
```

`result` is the form's data dict on success, `None` on cancel. The form
runs its own validation when the OK/primary button is clicked — the
dialog stays open if validation fails.

When inferred fields aren't enough, pass an `items` spec for explicit
layout (groups, tabs, custom editors, validation rules) — see the
[Forms guide](forms.md) for the field grammar. You can also override
the footer with the `buttons=` parameter using the same button specs as
the base `Dialog` (covered below).

---

## Building custom dialogs

When none of the built-in dialogs fit, instantiate `Dialog` directly
with a content builder, or subclass it for stateful dialogs.

### The composition shape

Two callbacks plus a button list, in plain function form:

```python
import ttkbootstrap as ttk

def build_content(parent):
    label = ttk.Label(parent, text="Pick the columns to export:")
    label.pack(anchor="w", padx=12, pady=(12, 4))
    box = ttk.Frame(parent, padding=12)
    box.pack(fill="both", expand=True)

dialog = ttk.Dialog(
    title="Export",
    content_builder=build_content,
    buttons=[
        {"text": "Cancel", "role": "cancel"},
        {"text": "Export", "role": "primary", "result": "export"},
    ],
)
dialog.show()
if dialog.result == "export":
    print("exporting")
```

The base `Dialog` does not take a `message=` shorthand — content always
comes from `content_builder`, a function that receives an empty `Frame`
and packs/grids widgets into it. (The `MessageDialog` subclass exposes
`message=` because it builds its own content.)

### Button specs

Each entry in `buttons=` is either a `DialogButton` instance or a dict
with the same fields. The fields you'll use most often:

- **`text`** — label text.
- **`role`** — one of `"primary"`, `"secondary"`, `"danger"`,
  `"cancel"`, `"help"`. Drives both styling and keyboard behavior:
  `primary` (or any button with `default=True`) is the Enter-key
  default; `cancel` is the Escape-key default.
- **`result`** — value assigned to `dialog.result` when this button is
  clicked. Set this for the buttons whose outcome you care about; leave
  it `None` for cancel-style buttons. **If you don't set `result`,
  `dialog.result` stays `None` even after the user clicks** — so always
  set it on the buttons you want to detect.
- **`default`** — make this the Enter-key default and give it focus on
  open. The first `primary` button gets this implicitly.
- **`closes`** — `False` to keep the dialog open after click (e.g. for
  validation that sometimes fails). Default `True`.
- **`command`** — callback that receives the `Dialog` instance. Run
  validation here, then either set `dialog.result` and let `closes=True`
  destroy the window, or leave `closes=False` and destroy it manually
  on success.

Buttons in the list are packed right-to-left, so **the first entry
appears rightmost** — this matches the macOS convention where the
primary action sits at the right.

### Result propagation

There are three ways the result gets set:

1. **Per-button `result=`** — easiest. Click sets `dialog.result` to
   that value, and (with `closes=True`) closes the window.
2. **Per-button `command=`** — the callback receives the `Dialog`
   instance and can write `dialog.result = ...` directly. Use this when
   the result depends on widget state, not the button itself.
3. **Read widget state after `show()`** — for stateful subclasses, keep
   references to your widgets on `self` and read them in
   `dialog.result` getters or after `show()` returns.

For a fuller reference, see the
[Dialog widget page](../widgets/dialogs/dialog.md).

---

## Modality and positioning

`Dialog` and its subclasses support three modes via the `mode=`
parameter:

- **`"modal"`** (default) — grabs input from the parent window and
  blocks until closed. The standard application dialog.
- **`"popover"`** — does not grab input; closes automatically when
  focus leaves the dialog. Right for menu-like or transient pickers
  attached to a button. Still blocks the calling code until closed.
- **`"sheet"`** — on macOS, applies the Cocoa sheet window class for a
  chromeless, parent-attached dialog. Falls back to plain modal on
  Windows and Linux.

You can override modality at call time with `show(modal=True/False)`,
independent of the mode.

### Positioning

By default, `show()` centers the dialog on its parent. For
popover-style dialogs anchored to a widget — opening below a button,
to the right of a row, near the cursor — `show()` accepts anchor
arguments:

```python
import ttkbootstrap as ttk

def open_dialog(button):
    picker = ttk.DateDialog()
    picker.show(
        anchor_to=button,
        anchor_point="sw",   # bottom-left corner of the button
        window_point="nw",   # top-left of the dialog meets it
        offset=(0, 4),       # 4px gap below the button
        auto_flip=True,      # flip if it would go off-screen
    )

app = ttk.Window()
btn = ttk.Button(app, text="Pick date", command=lambda: open_dialog(btn))
btn.pack(padx=20, pady=20)

app.after(50, app.destroy)
app.mainloop()
```

`anchor_to` also accepts the strings `"screen"`, `"cursor"`, or
`"parent"`. See the [Dialog widget page](../widgets/dialogs/dialog.md)
for the full positioning vocabulary.

### `alert=True`

Pass `alert=True` to ring the system bell when the dialog opens —
useful for genuinely interruptive errors. `MessageBox.show_warning` and
`show_error` set this implicitly.

---

## Patterns and tips

### Always parent your dialogs

Pass `master=` so the dialog inherits the right window for centering,
modality, and theme. Without it, the dialog falls back to the default
root, which is fine for top-level prompts but wrong for dialogs
launched from a secondary `Toplevel`:

```python
import ttkbootstrap as ttk

class MyWindow(ttk.Toplevel):
    def confirm(self):
        ttk.MessageBox.show_info("Done.", master=self)
```

### Keep the main thread responsive

`show()` blocks the calling thread. That's fine inside a button
command — the Tk event loop owns the call stack — but **do not** call
`show()` from a worker thread. Marshal the result back to the main
thread first. See [Threading & async](../platform/threading-and-async.md).

### Confirm destructive actions

For destructive flows, use `MessageDialog` with a `:danger` accent on
the primary button so the consequence is visible:

```python
import ttkbootstrap as ttk

def delete_item(name):
    dialog = ttk.MessageDialog(
        message=f"Permanently delete '{name}'?",
        buttons=["Cancel", "Delete:danger"],
    )
    dialog.show()
    if dialog.result == "Delete":
        print(f"deleting {name}")
```

### Nest dialogs sparingly

A dialog launched from another dialog works — the nested one becomes
modal to the outer dialog — but the resulting interaction is heavy. If
the outer dialog needs a confirmation step (e.g. "really delete?"),
prefer a single dialog with a `:danger` button over a chained pair.

### Localize button text

Standard button labels (`OK`, `Cancel`, `Yes`, `No`, `Retry`) flow
through the message catalog when the dialog is built with
`localize=True` — `MessageBox` and `QueryBox` do this for you. For your
own dialogs, wrap labels with `L("Save")` so they translate. See the
[Localization guide](localization.md).

---

## Additional resources

- [Dialogs widget index](../widgets/dialogs/index.md) — per-dialog reference
- [MessageBox](../widgets/dialogs/messagebox.md) /
  [MessageDialog](../widgets/dialogs/messagedialog.md)
- [QueryBox](../widgets/dialogs/querybox.md) /
  [QueryDialog](../widgets/dialogs/querydialog.md)
- [FormDialog](../widgets/dialogs/formdialog.md) — see also the
  [Forms guide](forms.md)
- [DateDialog](../widgets/dialogs/datedialog.md),
  [FontDialog](../widgets/dialogs/fontdialog.md),
  [ColorChooser](../widgets/dialogs/colorchooser.md),
  [FilterDialog](../widgets/dialogs/filterdialog.md)
- [Dialog](../widgets/dialogs/dialog.md) — base class for custom dialogs
