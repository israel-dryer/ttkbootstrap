---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


---

title: PathEntry
---

# PathEntry

`PathEntry` is a form-ready input control for selecting **files and folders**.

It combines a text field (type/paste paths) with a browse button (pick visually), while keeping the same label/message,
validation, and event model as other v2 field controls. fileciteturn14file2

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

Picker selections commit immediately.

---

## Common options

### Browse mode: `select`

```python
ttk.PathEntry(app, select="file")       # choose existing file
ttk.PathEntry(app, select="directory")  # choose folder
ttk.PathEntry(app, select="save")       # choose save-as path
```

!!! note "Open vs save"
    File selection usually expects an existing path.  
    Save selection may allow non-existing files and can prompt for overwrite.

### File type filters: `filetypes`

```python
ttk.PathEntry(
    app,
    label="Document",
    select="file",
    filetypes=[
        ("PDF", "*.pdf"),
        ("Word Document", "*.docx"),
        ("All files", "*.*"),
    ],
)
```

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

---

## Behavior

- Users can type/paste paths directly.

- Clicking the browse button opens a native file/folder chooser (based on `select`).

- Picker selection commits the value and closes the dialog.

---

## Events

PathEntry emits standard field events:

- `<<Input>>` / `on_input` — typing/pasting

- `<<Changed>>` / `on_changed` — committed value changed (blur/Enter or picker selection)

- validation lifecycle events

```python
def handle_changed(event):
    print("path:", event.data)

path.on_changed(handle_changed)
```

!!! tip "Commit-based logic"
    Prefer `on_changed(...)` for filesystem work (paths should be validated/normalized first).

---

## Validation and constraints

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

## When should I use PathEntry?

Use `PathEntry` when:

- users need to choose files/folders frequently

- you want both typing and browsing

- you want consistent field UX (message + validation)

Prefer **TextEntry** when:

- the value is not a filesystem path (URL, ID)

Prefer a file dialog directly when:

- you need a one-off selection with no persistent field

---

## Related widgets

- **TextEntry** — general-purpose field control

- **SelectBox** — choose from known values instead of browsing

- **Form** — build complete forms with path fields

---

## Reference

- **API Reference:** `ttkbootstrap.PathEntry`

---

## Additional resources

### Related widgets

- [DateEntry](dateentry.md)

- [LabeledScale](labeledscale.md)

- [NumericEntry](numericentry.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.PathEntry`](../../reference/widgets/PathEntry.md)
