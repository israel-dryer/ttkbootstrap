---
title: PathEntry
icon: fontawesome/solid/folder-open
---

# PathEntry

`PathEntry` is a **high-level file and folder path input control** for desktop applications.

It combines:

- a text field (so users can type or paste a path)
- a browse button (so users can pick visually)
- consistent label/message/validation behavior (via the same `Field` patterns as other v2 controls)

Use `PathEntry` whenever you need the user to choose:

- an **existing file**
- an **existing folder**
- a **save location**
- a **path-like value** that benefits from browsing

> _Image placeholder:_  
> `![PathEntry overview](../_img/widgets/pathentry/overview.png)`  
> Suggested shot: file picker mode + folder picker mode + invalid path message.

---

## Basic usage (choose a file)

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

## What problem does PathEntry solve?

Desktop apps frequently need file/folder paths, but a plain `Entry` is awkward:

- users don’t know the exact path
- copy/paste paths are common (and should be allowed)
- validation is inconsistent per screen
- browsing behavior (open/save/folder) repeats everywhere

`PathEntry` standardizes this into one control so path picking is consistent across your app.

---

## Text vs value

Like other entry controls, `PathEntry` separates raw text from committed value.

| Concept | Meaning |
|---|---|
| Text | what the user is typing/pasting |
| Value | committed path value (after validation) |

```python
current = path.value
path.value = r"C:\data\input.csv"
```

To read raw text at any time:

```python
raw = path.get()
```

---

## Choose a folder

If your implementation supports a “directory” mode, use it when you want folder selection.

```python
import ttkbootstrap as ttk

app = ttk.App()

folder = ttk.PathEntry(
    app,
    label="Output folder",
    message="Choose a destination directory",
    select="directory",   # example option
)
folder.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

> _Image placeholder:_  
> `![PathEntry folder](../_img/widgets/pathentry/folder.png)`

---

## Save location (save-as)

Use a save mode when the user is choosing a new file path.

```python
import ttkbootstrap as ttk

app = ttk.App()

out = ttk.PathEntry(
    app,
    label="Save report as",
    select="save",   # example option
    message="Choose a filename and location",
)
out.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

!!! note "Save vs open"
    “Open” selection typically requires the file to exist.  
    “Save” selection typically allows non-existing files and may confirm overwrite.

---

## File type filters

Many desktop apps should filter visible file types.

```python
import ttkbootstrap as ttk

app = ttk.App()

doc = ttk.PathEntry(
    app,
    label="Document",
    select="file",
    filetypes=[
        ("PDF", "*.pdf"),
        ("Word Document", "*.docx"),
        ("All files", "*.*"),
    ],
)
doc.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

> _Image placeholder:_  
> `![PathEntry filters](../_img/widgets/pathentry/filters.png)`  
> Suggested shot: OS picker with file filter dropdown.

---

## Validation patterns

Paths are a common validation hotspot. `PathEntry` supports standard field validation rules.

### Required

```python
p = ttk.PathEntry(app, label="File", required=True)
p.add_validation_rule("required", message="Please choose a file")
```

### Must exist

```python
p.add_validation_rule("path_exists", message="Path does not exist")
```

### Must be a file or folder

```python
p.add_validation_rule("is_file", message="Must be a file")
p.add_validation_rule("is_dir", message="Must be a folder")
```

!!! note "Rule names"
    Use the rule names that exist in your project’s validation registry (the examples above reflect common patterns).

---

## Events

`PathEntry` emits standard field events:

- `<<Input>>` — text editing (typing/paste)
- `<<Changed>>` — committed value changed (blur/Enter, or picker selection)
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

Use `on_*` / `off_*` helpers for all of them.

```python
import ttkbootstrap as ttk

app = ttk.App()

p = ttk.PathEntry(app, label="Input file")
p.pack(fill="x", padx=20, pady=10)

def handle_changed(event):
    print("changed:", event.data)

p.on_changed(handle_changed)

app.mainloop()
```

!!! tip "Live Typing"
    Use `on_input(...)` when you want immediate feedback while typing.  
    Use `on_changed(...)` when you want the committed path (including picker selections).

---

## Add-ons

If you want extra UI (like a “Clear” button), use add-ons.

```python
import ttkbootstrap as ttk

app = ttk.App()

p = ttk.PathEntry(app, label="File")
p.insert_addon(ttk.Button, position="after", text="Clear", command=lambda: setattr(p, "value", ""))
p.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

> _Image placeholder:_  
> `![PathEntry addon](../_img/widgets/pathentry/addon.png)`

---

## Recommended UX patterns

!!! tip "Show the most common path first"
    If your app has a “default folder”, initialize `value=` to that directory so users can browse from there.

!!! tip "Validate on commit"
    Paths often come from paste operations. Prefer validating on commit (`on_changed`) rather than blocking typing mid-edit.

!!! note "Cross-platform paths"
    Users may paste paths with forward slashes or backslashes. Treat path normalization as a feature, not a strictness test.

---

## When should I use PathEntry?

Use `PathEntry` when:

- users choose files/folders often
- you want consistent validation + messaging
- you want both “type/paste” and “browse” workflows

Use `TextEntry` when:

- the value is not actually a filesystem path (e.g., a URL or identifier)

---

## Related widgets

- **TextEntry** — general-purpose field control
- **SelectBox** — choose from known values rather than browsing the filesystem
- **Form** — build complete forms with file/folder fields
- **FileChooserDialog** — use a dialog directly when you don’t need an inline field
