# Validation

Validation in ttkbootstrap is a small, explicit surface: a rule class
(`ValidationRule`), a result class (`ValidationResult`), and a per-widget
mixin (`ValidationMixin`) that auto-runs rules on key release and focus
loss and emits virtual events. The text-entry composites
(`TextEntry`, `NumericEntry`, `DateEntry`, `TimeEntry`,
`PasswordEntry`, `PathEntry`, `SpinnerEntry`) and `SelectBox` ship the
mixin already wired up; `Form` aggregates field-level rules into a
single submit-time check.

Validation is always **per-value, string-only, and synchronous** — there
is no per-form rule registry, no async hook, and no built-in
cross-field rule. Compose those out of `'custom'` rules.

---

## At a glance

| Piece | Where it lives | What it does |
|---|---|---|
| [`ValidationRule`](rules.md) | `ttkbootstrap.ValidationRule` | One rule = one constraint + a trigger policy. Five built-in types (`required`, `email`, `pattern`, `stringLength`, `custom`); call `rule.validate(value)` to apply. |
| [`ValidationResult`](results.md) | `ttkbootstrap.ValidationResult` | A `(is_valid, message)` pair returned by `rule.validate(...)` and carried inside the virtual-event payload. |
| `ValidationMixin` | `widgets/mixins/validation_mixin.py` (internal) | Owns the rule list on the widget, debounces auto-validation on `<KeyRelease>` / `<FocusOut>`, emits `<<Valid>>` / `<<Invalid>>` / `<<Validate>>`. Mixed into every text-entry composite. |
| [`Form.validate()`](../../widgets/dialogs/formdialog.md) | `ttkbootstrap.Form` | Walks every field, runs its rules with trigger `'manual'`, focuses the first invalid field, returns a single bool. |

---

## Adding a rule to a widget

```python
import ttkbootstrap as ttk

app = ttk.App()
entry = ttk.TextEntry(app, label="Email")
entry.pack()

entry.add_validation_rule("required")
entry.add_validation_rule("email", message="Please enter a valid email address.")

app.mainloop()
```

`add_validation_rule(rule_type, **opts)` constructs a `ValidationRule`
and appends it to the widget's internal list. The fast path for
"required" is a constructor flag:

```python
ttk.TextEntry(app, label="Email", required=True)
```

which is equivalent to calling `add_validation_rule("required")` after
construction. Field composites (every `TextEntry`-family widget plus
`SelectBox`) forward both `add_validation_rule` and `add_validation_rules`
to their inner part.

To replace the entire rule list at once, hand `add_validation_rules`
a list of pre-built rules:

```python
entry.add_validation_rules([
    ttk.ValidationRule("required"),
    ttk.ValidationRule("stringLength", min=3, max=20),
])
```

---

## When rules fire

Each rule carries a `trigger` policy that gates auto-validation. The
defaults match the rule type:

| Rule type     | Default trigger | Fires on                                              |
|---------------|-----------------|-------------------------------------------------------|
| `required`    | `always`        | every key release **and** focus loss                  |
| `email`       | `always`        | every key release **and** focus loss                  |
| `pattern`     | `always`        | every key release **and** focus loss                  |
| `stringLength`| `blur`          | focus loss only                                       |
| `custom`      | `manual`        | never auto — call `widget.validation(value)` yourself |

Override the default by passing `trigger=` at construction:

```python
ttk.ValidationRule("email", trigger="blur")  # only on focus loss
```

Auto-validation is debounced 50 ms on both `<KeyRelease>` and
`<FocusOut>`, so a fast typist gets at most one validation pass per
50 ms.

`'manual'` is the escape hatch. `Form.validate()` runs every rule with
trigger `'manual'`, so even rules tagged `'always'` or `'blur'` fire on
form submit. A rule tagged `'manual'` that you never call by hand
will appear configured but never report a problem.

---

## Reading the result

Three virtual events are emitted on the widget after each
auto-validation pass and after every `widget.validation(value)` call:

| Event          | Fires when                          | `event.data`                                         |
|----------------|-------------------------------------|------------------------------------------------------|
| `<<Invalid>>`  | a rule fails                        | `{'value': ..., 'is_valid': False, 'message': str}`  |
| `<<Valid>>`    | every rule passes                   | `{'value': ..., 'is_valid': True,  'message': ''}`   |
| `<<Validate>>` | always — after `<<Invalid>>` or `<<Valid>>` | same payload as above                       |

Note the event name is `<<Validate>>` (singular, present tense), but
the helper method that wraps it is `on_validated` (past tense).

The on/off helper pairs deliver the **payload dict directly**, not the
Tk event:

```python
entry.on_invalid(lambda data: print("nope:", data["message"]))
entry.on_valid(lambda data: print("ok:", data["value"]))
entry.on_validated(lambda data: print("done:", data["is_valid"]))
```

This is a deliberate divergence from the rest of the framework's `on_*`
helpers, which take a Tk event and read `event.data` for the payload.
See [Callbacks](../signals/callbacks.md) for the broader catalog of
callback shapes.

If you bind directly with `widget.bind("<<Invalid>>", cb)`, you get
the conventional Tk event (`event.data` carries the dict).

---

## Form-level validation

`Form` aggregates field rules into a one-shot check used at submit
time:

```python
form = ttk.Form(app)
form.add_field("name", label="Name", required=True)
form.add_field("email", label="Email", validation_rules=[
    ttk.ValidationRule("email"),
])

if form.validate():
    save(form.data)
```

`Form.validate()` walks every field, runs rules with trigger
`'manual'` (which matches `'always'` and `'manual'` rules but skips
`'key'`/`'blur'`-only rules), emits `<<Valid>>` / `<<Invalid>>` on each
field's underlying entry, focuses the first invalid field, and returns
a single bool. `FormDialog` calls this on its OK button before
returning a result.

---

## What's not here

- **No async rules.** `'custom'` runs synchronously; if you need a
  network check, drive it from a focus-out handler and call
  `widget.validation(value)` only when the result is in.
- **No cross-field rules.** Compose with `'custom'`: capture the other
  widget in the closure and read its value inside the predicate.
- **No `'compare'` rule.** Use a `'custom'` rule that captures the
  reference value or peer widget in the closure.

---

## Where to read next

- *How do I write a rule?* → [Rules](rules.md)
- *What does a result look like?* → [Results](results.md)
- *How do I bind to validation events?* → [Callbacks](../signals/callbacks.md)
- *How does form-level validation work?* → [FormDialog](../../widgets/dialogs/formdialog.md)
- *Which widgets carry the validation surface?* → [TextEntry](../../widgets/inputs/textentry.md), [NumericEntry](../../widgets/inputs/numericentry.md), [DateEntry](../../widgets/inputs/dateentry.md), [SpinnerEntry](../../widgets/inputs/spinnerentry.md)
