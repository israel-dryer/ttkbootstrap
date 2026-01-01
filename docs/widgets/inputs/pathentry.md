---
title: PathEntry
---

# PathEntry

`PathEntry` is a form-ready input control for selecting **files and folders**.

It combines a text field (type/paste paths) with a browse button (pick visually), while keeping the same label/message,
validation, and event model as other v2 field controls.

---

## Quick start

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

## When to use

Use `PathEntry` when:

- users need to choose files/folders frequently
- you want both typing and browsing
- you want consistent field UX (message + validation)

### Consider a different control when...

- the value is not a filesystem path (URL, ID) -> use [TextEntry](textentry.md)
- you need a one-off selection with no persistent field -> use a file dialog directly

---

## Examples and patterns

### Value model

PathEntry separates **raw text** from the **committed path value**.

| Concept | Meaning |
|---|---|
| Text | Raw text while editing |
| Value | Committed path after validation/commit |

```python
current = path.value
raw = path.get()

path.value = r"C:\data\input.csv"
```

Picker selections commit immediately. The raw dialog result (which may be a tuple for
multi-file selections) is available via `path.dialog_result`.

### Dialog type: `dialog`

```python
ttk.PathEntry(app, dialog="openfilename")   # choose existing file (default)
ttk.PathEntry(app, dialog="directory")      # choose folder
ttk.PathEntry(app, dialog="saveasfilename") # choose save-as path
ttk.PathEntry(app, dialog="openfilenames")  # choose multiple files
```

Available dialog types:

- `openfilename` / `openfile`: Single file selection
- `openfilenames` / `openfiles`: Multiple file selection
- `directory`: Directory selection
- `saveasfilename` / `saveasfile`: Save file dialog

!!! note "Open vs save"
    File selection usually expects an existing path.
    Save selection may allow non-existing files and can prompt for overwrite.

### File type filters: `dialog_options`

```python
ttk.PathEntry(
    app,
    label="Document",
    dialog="openfilename",
    dialog_options={
        "filetypes": [
            ("PDF", "*.pdf"),
            ("Word Document", "*.docx"),
            ("All files", "*.*"),
        ],
        "title": "Select a document",
    },
)
```

Common `dialog_options` keys: `title`, `initialdir`, `initialfile`, `filetypes`, `defaultextension`.

### Button text: `button_text`

```python
ttk.PathEntry(app, label="File", button_text="Choose...")
ttk.PathEntry(app, label="Folder", dialog="directory", button_text="Select Folder")
```

The button text can be changed at runtime via `configure(button_text=...)`.

### Add-ons

```python
p = ttk.PathEntry(app, label="File")
p.insert_addon(
    ttk.Button,
    position="after",
    text="Clear",
    command=lambda: setattr(p, "value", ""),
)
```

### Events

PathEntry emits standard field events:

- `<<Input>>` / `on_input` — typing/pasting
- `<<Change>>` / `on_changed` — committed value changed (blur/Enter or picker selection)
- validation lifecycle events

The `<<Change>>` event provides `event.data` with:

- `value`: The new path value (display string)
- `prev_value`: The previous path value
- `text`: Same as value (display string)
- `dialog_result`: Raw dialog result (may be tuple for multi-select)

```python
def handle_changed(event):
    print("path:", event.data["value"])
    print("raw result:", event.data["dialog_result"])

path.on_changed(handle_changed)
```

!!! tip "Commit-based logic"
    Prefer `on_changed(...)` for filesystem work (paths should be validated/normalized first).

### Validation and constraints

Common validation patterns include:

- required
- path exists
- is file / is directory

```python
p = ttk.PathEntry(app, label="File", required=True)
p.add_validation_rule("required", message="Please choose a file")
p.add_validation_rule("path_exists", message="Path does not exist")
```

---

## Behavior

- Users can type/paste paths directly.
- Clicking the browse button opens a native file/folder chooser (based on `dialog`).
- Picker selection commits the value and closes the dialog.
- For multi-file selection, paths are joined with ", " for display; raw result is available via `dialog_result`.

---

## Additional resources

### Related widgets

- [TextEntry](textentry.md) - general-purpose field control
- [SelectBox](../selection/selectbox.md) - choose from known values instead of browsing
- [Form](../forms/form.md) - build complete forms with path fields

### API reference

- [`ttkbootstrap.PathEntry`](../../reference/widgets/PathEntry.md)