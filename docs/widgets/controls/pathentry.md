---
title: PathEntry
icon: fontawesome/solid/folder-open
---


# PathEntry

`PathEntry` is a **Field-based path picker** that combines an entry field with a button that opens native file/directory dialogs, ensuring users select valid paths without leaving your form.

It remembers the dialog result, supports multiple file selection, and keeps the usual `Field` guarantees (labels, validation, messages, addons).

---

## Overview

PathEntry wraps `Field` so you get:

- A dialog button (`Choose File` by default) that launches a native `filedialog` type (open file, directory, save, etc.).
- Automatic path rendering in the field, even for multiple selections (`openfilenames` returns comma-separated values by default).
- Preservation of the raw dialog result via the `dialog_result` property for downstream processing.
- Configurable dialog types (`openfilename`, `directory`, `saveasfilename`, etc.) and dialog options (`filetypes`, `initialdir`, `defaultextension`, etc.).
- All Field comforts: labels, messages, validation rules, bootstyles, addons, and signal events.

The control is ideal for upload/download interfaces, configuration screens, and forms that require precise file system input.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(title="Path Entry Demo", themename="cosmo")

file_entry = ttk.PathEntry(
    app,
    label="Document",
    dialog="openfilename",
    dialog_options={
        "title": "Select a document",
        "filetypes": [("Text files", "*.txt"), ("All files", "*.*")]
    }
)
file_entry.pack(fill="x", padx=16, pady=8)

dir_entry = ttk.PathEntry(
    app,
    label="Install Folder",
    dialog="directory",
    dialog_options={"title": "Choose an install directory"}
)
dir_entry.pack(fill="x", padx=16, pady=8)

app.mainloop()
```

---

## Dialog types & options

Control the behavior via the `dialog` argument (default `openfilename`):

- `openfilename`: Single file path string.
- `openfile`: File object.
- `directory`: Directory path.
- `openfilenames` / `openfiles`: Multiple file paths or file objects.
- `saveasfilename` / `saveasfile`: Save dialog results.

Pass `dialog_options` to configure the native dialog (`title`, `initialdir`, `filetypes`, `defaultextension`, etc.). Multiple results (from `openfilenames` or `openfiles`) are joined with `", "` for display, while the raw list is still available on `dialog_result`.

Use `label` to change the button text and `dialog_options['multiple']=True` when you need to allow multiple picks even in file dialogs that support it.

---

## Validation & events

PathEntry inherits all `Field` signals:

- `<<Changed>>`: fires after a dialog selection or manual input commits.
- `<<Input>>`: fires on each keystroke (for manual typing).
- `<<Valid>>` / `<<Invalid>>`: support validation rules such as `required=True`.

You can extend with `add_validation_rule` or `allow_blank=True` depending on whether empty paths are acceptable. The `message` area communicates hints or validation errors.

---

## When to use PathEntry

Use PathEntry when you need users to pick files or folders but still want consistent field styling and validation. It keeps filesystem interactions native while integrating with your bootstyle-themed form layout.

For manual text input without dialogs, prefer `TextEntry`. When you need both date/time and file input, combine PathEntry with other `Field` widgets in a `Form`.

---

## Related widgets

- `TextEntry`
- `Field`
- `Form`
