# Validation Results

A `ValidationResult` is the return value of
[`ValidationRule.validate(value)`](rules.md). It is a tiny two-field
container — a boolean verdict and an explanation string — built so that
rules never raise and never trigger UI side effects on their own. The
widget event surface and `Form.validate()` consume the result and do
the work.

```python
import ttkbootstrap as ttk

result = ttk.ValidationRule("email").validate("a@b.c")
result.is_valid    # True
result.message     # ''
```

`ValidationResult` is exported from the top-level namespace
(`ttkbootstrap.ValidationResult`); the source lives at
`core/validation/validation_result.py`.

---

## At a glance

| Attribute    | Type   | When it's set | What it means |
|--------------|--------|---------------|---------------|
| `is_valid`   | `bool` | Always        | `True` when the value satisfied the rule, `False` otherwise. |
| `message`    | `str`  | Always        | On failure, the rule's user-supplied `message=` or its built-in default. On success, the empty string. |

That's the entire public surface. There is no severity level, no
multi-message list, no rule reference, and no contextual data — only a
verdict and a string.

---

## Constructing a result

Rules construct results internally; you rarely need to. The two-arg
constructor mirrors the attribute table:

```python
ttk.ValidationResult(True)              # is_valid=True, message=''
ttk.ValidationResult(False, "Nope.")    # is_valid=False, message='Nope.'
```

Both attributes are plain instance attributes — the framework never
mutates a result after returning it, but nothing prevents you from
doing so:

```python
r = ttk.ValidationResult(True)
r.is_valid = False           # legal; nothing watches the field
r.message = "Reconsidered."  # legal
```

`is_valid=True` is allowed alongside a non-empty `message`, but the
framework never produces that shape — `_default_message()` is consulted
only on failure (see [Validation Rules — Messages](rules.md#messages)).

---

## Reading the result

Two attributes, both public:

```python
result = ttk.ValidationRule("stringLength", min=3).validate("ab")
print(result.is_valid)   # False
print(result.message)    # 'Enter at least 3 characters.'
```

`ValidationRule.validate()` always returns a `ValidationResult` and
never raises. If a rule type has no implementation branch — currently
only `'compare'` — the result is `is_valid=True, message=''`,
regardless of input.

!!! danger "`if result:` is always True"

    There is no `__bool__` override on `ValidationResult`, so the
    object's truthiness is the default for any user-defined class:
    truthy. **`bool(ValidationResult(False))` is `True`.**

    This makes `if rule.validate(value): ...` a silent footgun:

    ```python
    # WRONG — always taken
    if ttk.ValidationRule("required").validate(""):
        save_form()

    # Right — check the field
    if ttk.ValidationRule("required").validate("").is_valid:
        save_form()
    ```

    Either always read `.is_valid`, or wrap the truthiness check
    yourself. The `ValidationRule` itself short-circuits correctly
    inside the framework because it accesses `result.is_valid`
    explicitly.

There is also no `__eq__`, `__repr__`, or `__hash__`.
`ValidationResult(True) == ValidationResult(True)` is `False` (object
identity), and `repr(result)` shows the default
`<...ValidationResult object at 0x...>`. Compare the fields directly
when testing.

---

## Result vs event payload

`ValidationResult` is the return type of `ValidationRule.validate(value)`
— it never reaches a widget event handler. When a widget emits
`<<Valid>>` / `<<Invalid>>` / `<<Validate>>`, the
`event.data` payload is a **`dict`** built from the result plus the
input value:

| Source                           | Type                      | Fields |
|----------------------------------|---------------------------|--------|
| `ValidationRule.validate(value)` | `ValidationResult`        | `is_valid`, `message` |
| `<<Valid>>` / `<<Invalid>>` / `<<Validate>>` event | `dict[str, Any]` | `value`, `is_valid`, `message` |

The conversion happens in `ValidationMixin.validate`
(`widgets/mixins/validation_mixin.py:103-122`):

```python
payload = {"value": value, "is_valid": True, "message": ""}
for rule in self._rules:
    ...
    result = rule.validate(value)
    payload.update(is_valid=result.is_valid, message=result.message)
```

So a handler bound to `<<Validate>>` reads `event.data["is_valid"]`
and `event.data["message"]` from a dict — not from a `ValidationResult`
object. The same payload shape is delivered to the `on_valid` /
`on_invalid` / `on_validated` helpers (see
[Validation overview — Reading the result](index.md#reading-the-result)).

`Form.validate()` follows the same conversion pattern: it reads
`result.is_valid` / `result.message` from each
`ValidationRule.validate()` call and packs them into a dict before
emitting events on the field widget.

---

## Where the result appears

| Surface | What you get |
|---------|--------------|
| `ValidationRule.validate(value)`              | `ValidationResult` — the only place users see the object directly. |
| `widget.validation(value)`                    | `bool`. Returns `True` only when at least one rule ran and all passed. Returns `False` if any rule failed *or* if no rules are registered. |
| `widget.bind('<<Valid>>', cb)` / `<<Invalid>>` / `<<Validate>>` | `event.data` is a `dict`, not a `ValidationResult`. |
| `widget.on_valid(cb)` / `on_invalid(cb)` / `on_validated(cb)` | The callback receives the same payload `dict` directly (no event wrapper — see [Callbacks](../signals/callbacks.md)). |
| `Form.validate()`                             | `bool`. Aggregates per-field results; emits per-field `<<Valid>>` / `<<Invalid>>` / `<<Validate>>` events along the way. |

In other words: `ValidationResult` shows up only when you call
`ValidationRule.validate(value)` directly. The widget API hides it
behind dicts and bools.

!!! warning "`widget.validation()` return value diverges from its docstring"

    `ValidationMixin.validate()`'s docstring at
    `widgets/mixins/validation_mixin.py:99-100` claims the return is
    "`True` if validation was performed (regardless of result)". The
    actual return is `True` only when validation was performed **and**
    every rule passed; it is `False` on the first invalid result and
    on the no-rules case. Treat the return as "did this value pass?"
    and listen to the events for "did validation run?".

---

## What's not here

Concepts the old page implied existed but the implementation does not
support. If you need them, build on top of the two-field result.

- **Severity / warning level.** `ValidationResult` is binary — there
  is no `'warning'` state alongside valid/invalid. Use a `'custom'`
  rule that returns a different message for soft failures, then style
  the field externally on `<<Invalid>>`.
- **Multiple messages.** A result holds at most one message. Multi-rule
  reporting is replaced by short-circuit-on-first-failure inside
  `ValidationRule.validate()` (per-rule) and inside the widget loop
  (per-widget). To collect every failure, walk the rule list yourself:

  ```python
  failures = [
      r.validate(value).message
      for r in widget._rules
      if not r.validate(value).is_valid
  ]
  ```

  `widget._rules` is a private attribute today (no public accessor).
- **Rule provenance.** The result does not record which rule produced
  it. If you need that, capture it in the rule's `message=` (e.g.
  `"required: missing"`) or run rules manually.
- **Equality / comparison.** No `__eq__`. Compare `(r.is_valid,
  r.message)` tuples.
- **Pickling / serialization helpers.** Not implemented; the object's
  state is two fields, so a tuple or dict round-trips trivially.

---

## Standalone use

Like `ValidationRule`, `ValidationResult` has no dependency on any
widget — you can use it as a return type in a non-Tk validator:

```python
def validate_age(raw: str) -> ttk.ValidationResult:
    if not raw.isdigit():
        return ttk.ValidationResult(False, "Age must be a whole number.")
    n = int(raw)
    if not (0 <= n <= 150):
        return ttk.ValidationResult(False, "Age must be between 0 and 150.")
    return ttk.ValidationResult(True)
```

Calls to your own validator return the same object shape that
`ValidationRule.validate()` produces, so downstream code that branches
on `result.is_valid` works identically.

---

## Where to read next

- *What constraint types are built in?* → [Validation Rules](rules.md)
- *How are events wired up around a widget?* → [Validation overview](index.md)
- *How do callbacks deliver the result?* → [Callbacks](../signals/callbacks.md)
- *Which widgets ship the validation surface?* → [TextEntry](../../widgets/inputs/textentry.md), [NumericEntry](../../widgets/inputs/numericentry.md), [DateEntry](../../widgets/inputs/dateentry.md), [SpinnerEntry](../../widgets/inputs/spinnerentry.md), [SelectBox](../../widgets/inputs/selectbox.md)
- *How does form-level submit validation work?* → [FormDialog](../../widgets/dialogs/formdialog.md)
