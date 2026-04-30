---
title: PathEntry
---

# PathEntry

`PathEntry` is a form-ready input for choosing **files and folders**. It
combines a text field — for typing or pasting paths — with a Browse
button that opens a native file or directory chooser. All of the field
chrome that [`TextEntry`](textentry.md) provides (label, message,
validation, signal/variable binding, accent, density, add-ons) comes
along unchanged.

The committed value is a **display string** of the selected path or
paths. For multi-file selections, the raw tuple from the dialog is
preserved separately on `path.dialog_result`, so you never have to
parse it back out of the joined display text.

<figure markdown>
![pathentry](../../assets/dark/widgets-pathentry.png#only-dark)
![pathentry](../../assets/light/widgets-pathentry.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

path = ttk.PathEntry(
    app,
    label="Input file",
    message="Select a CSV file to import",
)
path.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

`PathEntry` separates **what is shown in the field** from **what came
back from the picker**:

| Concept | Meaning | How to read it |
|---|---|---|
| Text | The raw editable string in the entry, updated on every keystroke. | `path.get()` |
| Value | The committed display string — the path the user typed and committed, or the path(s) returned by the picker. | `path.value` |
| Dialog result | The raw object the file dialog returned — a string for single selection, a tuple for `openfilenames`/`openfiles`. | `path.dialog_result` |

When the user picks a single file or folder, `value` is the path
string. When they pick multiple files (`dialog="openfilenames"`), the
paths are joined with `", "` for display, while `path.dialog_result`
holds the original tuple. Use the dialog result whenever you need to
iterate paths reliably — splitting on `", "` is unsafe.

```python
current = path.value          # display string
raw = path.get()              # current text in the entry
selection = path.dialog_result  # raw dialog return (str or tuple)

path.value = "/data/input.csv"  # set programmatically
```

### Empty values

When the field is empty:

- with `allow_blank=True` (the default), the committed value is `None`.
- with `allow_blank=False`, the previous value is preserved on commit.

A cancelled picker leaves the field unchanged — the dialog only
commits when the user actually selects something.

### Signals and variables

`path.signal` and `path.variable` are bound to the **raw text**, just
like other field controls. Pass your own with `textsignal=` or
`textvariable=` to share the path with another widget or to drive it
from elsewhere.

```python
selected = ttk.Signal("")
path = ttk.PathEntry(app, textsignal=selected)
```

---

## Common options

| Option | Purpose |
|---|---|
| `value` | Initial path value to display. |
| `dialog` | Which file dialog to open (`'openfilename'`, `'directory'`, `'saveasfilename'`, `'openfilenames'`, …). Default `'openfilename'`. |
| `dialog_options` | Dict of options passed to the dialog (`title`, `initialdir`, `initialfile`, `filetypes`, `defaultextension`). |
| `button_text` | Label on the browse button. Default `"Browse"`. |
| `label` | Text shown above the entry. |
| `message` | Helper text shown below; replaced by validation errors. |
| `required` | Adds an asterisk to the label and a `'required'` validation rule. |
| `allow_blank` | Whether an empty input commits as `None` (default) or preserves the previous value. |
| `width` | Width of the entry in characters. |
| `state` | `'normal'`, `'disabled'`, or `'readonly'`. |
| `accent` | Semantic color token for the focus ring (`primary`, `success`, `danger`, …). |
| `density` | `'default'` or `'compact'` for tight forms. |
| `textsignal` / `textvariable` | External signal or Tk variable bound to the raw text. |
| `initial_focus` | Take focus on creation. |

```python
ttk.PathEntry(app, label="File")                         # primary (default)
ttk.PathEntry(app, label="File", accent="success")
ttk.PathEntry(app, label="File", density="compact")
```

!!! link "See [Design System](../../design-system/index.md) for the full set of accent and density tokens."

---

## Behavior

### Dialog type

`dialog` selects which native chooser opens when the browse button is
clicked. Each value maps to a `tkinter.filedialog.ask*` function:

| `dialog=` | Opens | Returns |
|---|---|---|
| `'openfilename'` *(default)* | Open-file dialog | path string |
| `'openfile'` | Open-file dialog | open file object |
| `'openfilenames'` | Multi-file open | tuple of path strings |
| `'openfiles'` | Multi-file open | tuple of file objects |
| `'directory'` | Folder chooser | path string |
| `'saveasfilename'` | Save-as dialog | path string |
| `'saveasfile'` | Save-as dialog | open file object |

```python
ttk.PathEntry(app, dialog="openfilename")    # choose existing file
ttk.PathEntry(app, dialog="directory")       # choose folder
ttk.PathEntry(app, dialog="saveasfilename")  # choose save-as path
ttk.PathEntry(app, dialog="openfilenames")   # choose multiple files
```

!!! note "Open vs save"
    Open dialogs expect an existing path. Save dialogs may allow a
    non-existent file and can prompt for overwrite. Pick the variant
    that matches your downstream code path.

### Dialog options

`dialog_options` is forwarded as keyword arguments to the underlying
`filedialog.ask*` call. The most useful keys:

| Key | Effect |
|---|---|
| `title` | Window title for the dialog. |
| `initialdir` | Directory the dialog opens in. |
| `initialfile` | Pre-selected filename (save dialogs). |
| `filetypes` | List of `(label, pattern)` tuples for the file-type dropdown. |
| `defaultextension` | Extension appended if the user omits one. |

```python
ttk.PathEntry(
    app,
    label="Document",
    dialog="openfilename",
    dialog_options={
        "title": "Select a document",
        "filetypes": [
            ("PDF", "*.pdf"),
            ("Word document", "*.docx"),
            ("All files", "*.*"),
        ],
    },
)
```

### Browse button text

```python
ttk.PathEntry(app, label="File", button_text="Choose...")
ttk.PathEntry(app, label="Folder", dialog="directory", button_text="Select folder")
```

The button label can be changed at runtime with
`path.configure(button_text=...)`.

### Add-ons

Like other field controls, `PathEntry` accepts prefix and suffix
add-ons via `insert_addon` — they slot in alongside the browse button
and inherit the field's disabled state.

```python
path = ttk.PathEntry(app, label="File")
path.insert_addon(
    ttk.Button,
    position="after",
    text="Clear",
    command=lambda: setattr(path, "value", ""),
)
```

### Disable, enable, readonly

```python
path.disable()        # not editable, not focusable; browse button disables too
path.enable()
path.readonly(True)   # focusable, copyable, not editable; browse still works
path.readonly(False)
```

---

## Events

`PathEntry` emits the same events as `Field`, plus an enriched
`<<Change>>` payload when the change came from the picker.

**Input and value events** (callback receives the raw event;
read `event.data`):

| Event | Helper | Fires when… | `event.data` |
|---|---|---|---|
| `<<Input>>` | `on_input` | every keystroke | `{'text': str}` |
| `<<Change>>` | `on_changed` | committed value changed (blur/Enter or picker selection) | `{'value', 'prev_value', 'text'[, 'dialog_result']}` |
| `<Return>` | `on_enter` | **Enter** pressed in the field | `{'value', 'text'}` |

When the change comes from the picker, `event.data` includes a
`'dialog_result'` key holding the raw dialog return (a string, or a
tuple for multi-select). When the user typed the change, that key is
absent — read it with `event.data.get('dialog_result')`.

```python
def handle_changed(event):
    print("path:", event.data["value"])
    raw = event.data.get("dialog_result")
    if isinstance(raw, tuple):
        for p in raw:
            print(" -", p)

path.on_changed(handle_changed)
```

**Validation events** (callback receives the payload `dict` directly):

| Event | Helper | Fires when… | Payload |
|---|---|---|---|
| `<<Valid>>` | `on_valid` | validation passes | `{'value', 'is_valid': True, 'message': ''}` |
| `<<Invalid>>` | `on_invalid` | validation fails | `{'value', 'is_valid': False, 'message': str}` |
| `<<Validate>>` | `on_validated` | after any validation | `{'value', 'is_valid': bool, 'message': str}` |

!!! tip "Commit-based logic"
    Prefer `on_changed` for filesystem work. By the time it fires, the
    path is the one the user committed — either by picking it or by
    leaving the field after typing it.

---

## Validation and constraints

Rules are added with `add_validation_rule(rule_type, **kwargs)` and
run automatically on key release and blur. Built-in rule types are
`'required'`, `'pattern'`, `'stringLength'`, and `'custom'`. There is
no built-in "path exists" rule — use `'custom'` with `os.path` checks.

```python
import os

path = ttk.PathEntry(app, label="Input file", required=True)

# Path must exist on disk
path.add_validation_rule(
    "custom",
    func=lambda v: bool(v) and os.path.exists(v),
    message="Path does not exist",
)

# Must be a directory
folder = ttk.PathEntry(app, label="Output folder", dialog="directory")
folder.add_validation_rule(
    "custom",
    func=lambda v: bool(v) and os.path.isdir(v),
    message="Choose an existing folder",
)

# Restrict by extension when typing
csv_path = ttk.PathEntry(app, label="CSV")
csv_path.add_validation_rule(
    "pattern",
    pattern=r".+\.csv$",
    message="File must end in .csv",
)
```

A failed rule replaces the message line with the rule's error text and
emits `<<Invalid>>`. A passing rule restores the original message and
emits `<<Valid>>`. Each rule type has a default trigger (`'always'`,
`'blur'`, or `'manual'`); pass `trigger=...` to override.

For multi-file selections, the committed value is the joined display
string and a `'pattern'` rule will not match cleanly — validate
against `path.dialog_result` directly inside an `on_changed` handler
instead.

If you need per-keystroke filtering — blocking characters as the user
types — use Tk's low-level `validate` / `validatecommand` on the
underlying [`Entry`](../primitives/entry.md). `PathEntry`'s rule
system is designed around commit-time validation.

---

## When should I use PathEntry?

Use `PathEntry` when:

- the field collects a filesystem path and the user benefits from both typing and a native chooser.
- you want consistent form chrome (label, message, validation) across the inputs in a form.
- you need access to the raw multi-file tuple, not just a flattened string.

Prefer a different control when:

- the field collects free-form text or a URL → use [TextEntry](textentry.md).
- the value comes from a fixed list of known paths → use [SelectBox](../selection/selectbox.md).
- you only need a single one-off file pick with no persistent input → call `tkinter.filedialog.askopenfilename` directly.

---

## Related widgets

- [TextEntry](textentry.md) — base composite text field; `PathEntry` shares its label/message/validation/signal machinery.
- [SelectBox](../selection/selectbox.md) — pick from a known set of paths instead of browsing the filesystem.
- [Form](../forms/form.md) — assemble a full form from field declarations.

---

## Reference

- **API reference:** [`ttkbootstrap.PathEntry`](../../reference/widgets/PathEntry.md)
- **Related guides:**
    - [Forms](../../guides/forms.md)
    - [Signals](../../capabilities/signals/signals.md)
