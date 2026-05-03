---
title: Form
---

# Form

`Form` is a spec-driven, multi-field input. You hand it a list of field
declarations (or a `data` dict) and it builds a labeled grid of input
widgets that share a single value-dict, a single `on_data_changed`
callback, and a single `validate()` entry point.

Unlike a single input widget, `Form`'s value is a `dict[str, Any]`
keyed by field name. Read it with `form.data` (or `form.value`); set
it with `form.set(...)` (or `form.value = ...`). Use `Form` when the
shape is "edit a record" and the page count is one.

<figure markdown>
![form](../../assets/dark/widgets-form.png#only-dark)
![form](../../assets/light/widgets-form.png#only-light)
</figure>

---

## Basic usage

Define fields with a list of dicts, read the committed data after
validation:

```python
import ttkbootstrap as ttk

app = ttk.App()

form = ttk.Form(
    app,
    items=[
        {"key": "name", "label": "Name", "editor": "textentry"},
        {"key": "age", "label": "Age", "editor": "numericentry", "dtype": "int"},
        {"key": "status", "label": "Status", "editor": "selectbox",
         "editor_options": {"items": ["New", "In Progress", "Done"]}},
    ],
)
form.pack(fill="both", expand=True, padx=20, pady=20)

def submit():
    if form.validate():
        print(form.data)

ttk.Button(app, text="Submit", command=submit).pack(pady=(0, 20))

app.mainloop()
```

The fastest path skips `items=` entirely — pass a `data` dict and
`Form` infers fields from the value types:

```python
form = ttk.Form(app, data={"name": "Alice", "age": 34, "active": True})
# Builds: TextEntry, NumericEntry, CheckButton — keys preserved.
```

---

## Value model

The form's value is a `dict[str, Any]`. Field keys map to widget
values; reading and writing happen at two layers (per-field via
`form.field(key)`, or whole-dict via `form.data` / `form.set(...)`).

### Spec item shapes

`items=` accepts three item shapes (as `dataclass` instances or plain
dicts):

| Shape | Type tag | Purpose |
|---|---|---|
| `FieldItem` | `"field"` (default) | One field with `key` / `label` / `editor` / `dtype` |
| `GroupItem` | `"group"` | Nested grid of items; `label` makes it a `LabelFrame`, otherwise a plain `Frame` |
| `TabsItem` | `"tabs"` | Notebook hosting one or more `TabItem`s of items |

Top-level items are placed into a grid driven by `col_count` (default
`1`). When a `FieldItem` omits both `row` and `column`, it auto-flows
left-to-right with wrapping; when both are set, it lands at that
explicit cell.

### Field-item keys

A `FieldItem` (or its dict equivalent) accepts only these keys:

- `key` (required) — dict key in `form.data`
- `label` — display label; defaults to `key.replace("_", " ").title()`
- `dtype` — `'int' | 'float' | 'bool' | 'date' | 'datetime' | 'password' | 'str'` or a Python type. Drives both editor inference (when `editor` is omitted) and read-time coercion.
- `editor` — explicit editor (see table below). Overrides dtype-driven inference.
- `editor_options` — dict forwarded to the editor's constructor (e.g. `{"items": [...]}` for SelectBox, `{"min": 0, "max": 100}` for NumericEntry)
- `readonly` — `True` calls `state(['readonly'])` on Field-based editors; `state(['disabled'])` on the rest
- `visible` — `False` skips widget construction entirely (the key still appears in `form.data` if seeded from `data=` or written via `set_field_value`)
- `column`, `row`, `columnspan`, `rowspan` — explicit grid placement

!!! warning "Spec keys outside this list are silently dropped"
    `_normalize_items` only reads the fields above. Common spec
    additions like `value=`, `required=True`, `validate="email"`,
    `help=...`, `message=...` are accepted by the dict literal but
    never reach the widget. Use `data=` for initial values and
    `form.field(key).add_validation_rule(...)` for rules — see
    Validation and constraints below.

### Editor inference

When `editor` is omitted, the dtype picks the widget:

| `dtype` | Editor |
|---|---|
| `'int'`, `int`, `'float'`, `float` | `NumericEntry` |
| `'bool'`, `bool` | `CheckButton` |
| `'date'`, `'datetime'`, `date`, `datetime` | `DateEntry` |
| `'password'` | `PasswordEntry` |
| `'str'`, `None`, anything else | `TextEntry` |

When `data=` is passed without `items=`, dtypes are inferred from the
value of each key (`bool` is checked before `int` to avoid the
`True is int` trap).

The full editor vocabulary recognized by `editor=`:

| Editor | Widget |
|---|---|
| `'textentry'` | `TextEntry` (single-line, default fallback) |
| `'numericentry'` | `NumericEntry` |
| `'passwordentry'` | `PasswordEntry` |
| `'dateentry'` | `DateEntry` |
| `'selectbox'`, `'combobox'` | `SelectBox` |
| `'spinbox'` | `Spinbox` (raw `ttk.Spinbox` primitive) |
| `'text'` | `tk.Text` (multi-line; **not** `TextEntry`) |
| `'checkbutton'` | `CheckButton` |
| `'switch'`, `'toggle'` | `Switch` |
| `'scale'` | `Scale` |

!!! warning "Unknown editor names fall back silently"
    A misspelled editor name (`'select'`, `'int'`, `'bogus'`) hits
    the fallback branch and builds a `TextEntry` with no warning.
    Verify editor names against the table above.

### Reading and writing data

Four equivalent reads of the whole dict:

```python
data = form.data         # property; equivalent to form.get()
data = form.value        # property; same dict
data = form.get()        # method; same dict
data = form.cget("data") # configure-delegate read
```

Two equivalent writes:

```python
form.set({"name": "Alice", "age": 34})
form.value = {"name": "Alice", "age": 34}
# form.configure(data=...) also works
```

Single-field accessors:

```python
form.get_field_value("email")       # raises KeyError on missing key
form.set_field_value("email", "x")  # raises KeyError on missing key
```

`form.data` always reflects current widget values (including unsaved
edits), not just what was last `set()`. Reads pass through
`_coerce_value` per-field — but only when `dtype` is set. A
`NumericEntry` without `dtype='int'` round-trips strings:

```python
form = ttk.Form(app, items=[{"key": "n", "editor": "numericentry"}])
form.set({"n": 7})
form.data["n"]  # → '7' (str, not int!)
```

Always pair `numericentry` with an explicit `dtype` (`'int'` or
`'float'`) when the value's Python type matters.

### Hidden-but-trackable fields

`visible=False` skips widget construction but keeps the key
addressable via `set_field_value` and `get_field_value`:

```python
form = ttk.Form(app, items=[
    {"key": "id", "visible": False},
    {"key": "name", "editor": "textentry"},
])
form.set_field_value("id", 42)
form.data       # → {"id": 42, "name": ""}
form.field("id")  # raises KeyError — no widget exists
```

Useful for IDs you want to round-trip without showing the user.

---

## Common options

| Option | Default | Effect |
|---|---|---|
| `data` | `{}` | Initial value dict; also drives item inference when `items=None` |
| `items` | inferred from `data` | Explicit field / group / tab spec |
| `col_count` | `1` | Top-level column count for auto-flow |
| `min_col_width` | `DEFAULT_MIN_COL_WIDTH` | Minimum width per column (px) |
| `on_data_changed` | `None` | Callback fired with the full dict on any field change |
| `width`, `height` | `None` | When set, propagation is disabled and the form keeps these dimensions |
| `accent` | `None` | Forwarded to the outer `Frame` (container surface tinting) |
| `buttons` | `None` | Optional footer buttons (`DialogButton`, mapping, or string) |

!!! note "`columns=` is accepted as an alias for `col_count=`"
    Both spellings work. `col_count` is the canonical argument name.

`editor_options` flows verbatim into the editor's constructor, so
options live where the editor expects them:

```python
{"key": "status", "editor": "selectbox",
 "editor_options": {"items": ["A", "B"], "allow_custom_values": True}}

{"key": "level", "editor": "numericentry", "dtype": "int",
 "editor_options": {"min": 0, "max": 10, "step": 1}}

{"key": "due", "editor": "dateentry",
 "editor_options": {"min_date": date.today()}}
```

Three keys passed in `editor_options` (`show_message`, `required`,
`validator`) are filtered out before reaching non-Field editors
(`Spinbox`, `Text`, `Switch`, `CheckButton`, `Scale`) — those don't
accept `ValidationMixin` kwargs. They reach Field-based editors
(`TextEntry`, `NumericEntry`, `PasswordEntry`, `DateEntry`,
`SelectBox`) unchanged.

---

## Behavior

### Layout and grouping

Use `GroupItem` (`type="group"`) for visual sections. With a
`label`, the group renders as a `LabelFrame`; without, a plain
`Frame`:

```python
form = ttk.Form(app, items=[
    {"type": "group", "label": "Account",
     "items": [
         {"key": "user", "editor": "textentry"},
         {"key": "role", "editor": "selectbox",
          "editor_options": {"items": ["Admin", "User"]}},
     ]},
    {"type": "group",  # no label — bare Frame
     "items": [
         {"key": "notes", "editor": "text"},
     ]},
])
```

Use `TabsItem` (`type="tabs"`) to split a wide form into pages.
Each `TabItem` carries its own `label` and item list:

```python
form = ttk.Form(app, items=[{
    "type": "tabs",
    "tabs": [
        {"label": "General", "items": [
            {"key": "name", "editor": "textentry"},
        ]},
        {"label": "Advanced", "items": [
            {"key": "verbose", "editor": "checkbutton"},
        ]},
    ],
}])
```

!!! note "`TabsItem.label` is reserved but not rendered"
    The dataclass accepts a top-level `label` on a `TabsItem`, but
    nothing in the build path renders it. The `label` on each
    individual `TabItem` is the one that becomes the tab caption.

### Live data sync

Variable traces on every editor's variable feed
`_sync_value_from_widget`, which writes back to `form._data` and (if
set) calls `on_data_changed(dict_copy)`:

```python
def changed(data):
    print("changed:", data)

form = ttk.Form(app, on_data_changed=changed,
                items=[{"key": "n", "editor": "textentry"}])
form.field("n").value = "x"
# changed: {'n': 'x'}
```

`form.set(...)` suppresses the trace re-entry by setting
`_suspend_sync = True` for the duration of the bulk write — so a
single `set()` of N keys produces no `on_data_changed` calls (the
suspend flag is only released after every key is written).

### Field access and reactive bindings

Widget access by key:

```python
field = form.field("email")     # → Field instance; KeyError on miss
fields = form.fields()          # → tuple of Field instances
keys = form.keys()              # → tuple of key strings
```

Variables and signals (per-field):

```python
var = form.field_variable("name")  # → tk.Variable; None on miss
sig = form.field("name").signal    # → Signal or Variable on the inner editor
```

`field_signal(key)` and `field_textsignal(key)` work for all editor
types — both the Field-based editors (`TextEntry`, `NumericEntry`,
`SelectBox`, `DateEntry`, `PasswordEntry`) and the raw SignalMixin
subclasses (`CheckButton`, `Switch`, `Scale`). `form.field(key).signal`
is the equivalent direct path when you already have the Field widget.

### Footer buttons

Pass a sequence of strings, mappings, or `DialogButton` instances to
`buttons=`:

```python
form = ttk.Form(app, items=[...], buttons=["Cancel", "Save"])
# Or with explicit roles:
form = ttk.Form(app, items=[...], buttons=[
    {"text": "Cancel", "role": "cancel"},
    {"text": "Save",   "role": "primary",   "result": "saved"},
    {"text": "Delete", "role": "danger",    "result": "deleted"},
])
```

Plain strings are wrapped in `DialogButton` with the first becoming
`role="primary"` and the rest `"secondary"`. Buttons render
right-to-left in `pack(side="right")` order — the conventional
primary action lands on the right edge.

`role` resolves to `(accent, variant)`:

| Role | Accent | Variant |
|---|---|---|
| `"primary"` | `"primary"` | `None` |
| `"secondary"` | `"secondary"` | `None` |
| `"danger"` | `"danger"` | `None` |
| `"cancel"` | `"secondary"` | `"outline"` |
| `"help"` | `"info"` | `"link"` |

Footer-button commands receive the form as their single argument:

```python
def save(form):
    if form.validate():
        print(form.data)

form = ttk.Form(app, items=[...],
                buttons=[{"text": "Save", "command": save}])
```

After a button click, `form.result` becomes the button's `result`
field — or, if `result` is not set on the button, falls back to
`form.data`. Useful for embedding a `Form` inside a custom dialog
flow that reads `form.result` after the dialog closes.

### Readonly fields

`readonly=True` on a `FieldItem` calls `state(['readonly'])` on
Field-based editors (typing blocked, selection still works) and
`state(['disabled'])` on the rest:

```python
{"key": "id", "label": "User ID", "editor": "textentry", "readonly": True}
```

Reconfiguring readonly state at runtime needs a manual
`form.field(key).readonly(True/False)` call — there is no
configure-delegate for the spec-level flag.

---

## Events

`Form` itself emits no virtual events. The reactive surface is
distributed across the inner editors and the `on_data_changed`
callback:

| Surface | What it carries |
|---|---|
| `on_data_changed=cb` | Callback `cb(data: dict)` fires on every per-field change. Receives a fresh copy of the full dict. |
| `form.field(key).bind('<<Change>>', ...)` | Per-field commit event from the inner editor. Payload depends on the editor — see the editor's own page. |
| `form.field(key).bind('<<Valid>>', ...)` etc. | `ValidationMixin` events (see Validation below). Payload is `{"value": ..., "is_valid": bool, "message": str}`. |
| Footer button `command=cb` | `cb(form)` fires on click; `form.result` is set immediately after. |

```python
form.field("email").bind("<<Invalid>>",
    lambda e: print("invalid:", e.data["message"]))
```

Form has no `<<Submit>>` or `<<Cancel>>` event of its own — derive
those from a button's `command=` callback.

---

## Validation and constraints

### Attaching rules

Rules attach per-field after construction. The form spec doesn't
carry rules:

```python
form = ttk.Form(app, items=[
    {"key": "email", "editor": "textentry"},
    {"key": "age",   "editor": "numericentry", "dtype": "int"},
])

form.field("email")._entry.add_validation_rule("required")
form.field("email")._entry.add_validation_rule("email")
form.field("age")._entry.add_validation_rule(
    "custom", validator=lambda v: 0 <= v <= 150)
```

Field-based editors expose the underlying `ValidationMixin` part as
`._entry` (the `TextEntryPart` / `NumericEntryPart` / `DateEntryPart`
/ etc.). That is where `add_validation_rule` lives. See
[Validation rules](../../capabilities/validation/rules.md) for
the full rule vocabulary.

### `Form.validate()` semantics

`form.validate()` walks every Field child, runs its rules, and
returns `True` only if **every** rule passes. On the first invalid
field it stops walking that field and continues with the next; the
first invalid widget gets `focus_set()` called on it.

Two important details:

- **Trigger gating.** `Form.validate()` runs only rules whose
  `trigger` is `"always"` or `"manual"` — blur-triggered and
  input-triggered rules are skipped. The default trigger from
  `add_validation_rule(...)` is `"always"`, so most rules run; if
  you explicitly pass `trigger="blur"`, the rule will not fire
  from `Form.validate()`.
- **Synthetic events.** For each rule that runs, the form emits
  `<<Valid>>` / `<<Invalid>>` plus `<<Validate>>` on the inner
  editor — so any handler bound on the field sees the result. The
  validation event payload is the dict
  `{"value": ..., "is_valid": bool, "message": str}`.

```python
form.field("email").bind("<<Invalid>>", lambda e: ...)

if not form.validate():
    show_error("Please fix the highlighted fields")
```

### Inherent constraints

`dtype` is the only spec-level constraint enforced by Form itself —
on `_read_value_from_widget`, the value is coerced to the dtype
(failing silently and returning the raw string if coercion raises).
Pair it with `editor_options={"min": ..., "max": ...}` for editors
that support it (`NumericEntry`, `Scale`, `Spinbox`).

---

## When should I use Form?

Use `Form` when:

- the UI is "edit a record" — many fields sharing one value-dict,
  one validation pass, one submit
- the field set is data-driven (feature flags, schema, metadata) and
  hand-laid-out widgets would mean a lot of repetitive plumbing
- you want consistent label / message / readonly / signal behavior
  across every field for free

Prefer building widgets manually when:

- the form has 1–3 fields and any layout you'd write by hand is
  simpler than writing the spec
- the layout is highly custom (artistic alignment, mixed widget
  sizes, non-grid composition)
- the row-by-row layout needs widgets that aren't in the editor
  vocabulary

For a modal flow, prefer [`FormDialog`](../dialogs/formdialog.md):
it wraps a `Form` in a `Dialog` and returns the result through the
dialog's `<<DialogResult>>` event.

---

## Related widgets

- **[FormDialog](../dialogs/formdialog.md)** — modal dialog wrapping a `Form`, with submit / cancel buttons and a return value
- **[TextEntry](textentry.md), [NumericEntry](numericentry.md), [DateEntry](dateentry.md), [SelectBox](selectbox.md), [PasswordEntry](passwordentry.md), [TimeEntry](timeentry.md), [SpinnerEntry](spinnerentry.md)** — Field-based editors a `Form` composes
- **[CheckButton](../selection/checkbutton.md), [Switch](../selection/switch.md), [Scale](scale.md)** — non-Field editors a `Form` composes
- **[GridFrame](../layout/gridframe.md)** — when an ad-hoc layout for a small form is simpler than writing a spec
- **[PageStack](../views/pagestack.md)** — wizard-style multi-step forms that go beyond a single `Form`

---

## Reference

- **API reference:** [`ttkbootstrap.Form`](../../reference/widgets/Form.md)
- **Related guides:** [Forms](../../guides/forms.md), [Validation](../../capabilities/validation/index.md), [Layout](../../guides/layout.md)
