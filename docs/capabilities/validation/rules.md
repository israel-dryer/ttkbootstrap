# Validation Rules

A `ValidationRule` is one constraint plus a trigger policy. It wraps a
single check (`is_valid` / `message`) over a string value, so a widget's
rule list can be read top-to-bottom and stops at the first failure.

```python
import ttkbootstrap as ttk

rule = ttk.ValidationRule("stringLength", min=3, max=20)
result = rule.validate("ab")
# ValidationResult(is_valid=False, message='Enter between 3 and 20 characters.')
```

`rule.validate(value)` always returns a [`ValidationResult`](results.md);
it never raises and has no side effects. Widgets call it for you on
`<KeyRelease>` and `<FocusOut>` (debounced 50 ms) and emit virtual
events with the result — see [Validation overview](index.md) for the
event surface.

---

## At a glance

| `rule_type`      | Default trigger | Required params | What it checks |
|------------------|-----------------|-----------------|----------------|
| `'required'`     | `always`        | —               | value is not `None` and (if a string) is not empty / whitespace-only |
| `'email'`        | `always`        | —               | value matches `[^@]+@[^@]+\.[^@]+` (anchored at start, not end) |
| `'pattern'`      | `always`        | `pattern=str`   | `re.match(pattern, value)` succeeds (anchored at start, not end) |
| `'stringLength'` | `blur`          | `min=int` and/or `max=int` | `min ≤ len(value) ≤ max` |
| `'custom'`       | `manual`        | `func=callable` | `func(value)` returns truthy |
| `'compare'`      | `blur`          | —               | **Not implemented.** Always returns `is_valid=True` regardless of input. |

All six are exposed through the `RuleType` literal at
`core/validation/types.py:4`. The first five have implementation branches
in `ValidationRule.validate()`; `'compare'` is a silent no-op.

---

## `'required'`

Fails on `None` and on string values that are empty or whitespace-only.
Every other value type — numbers, dates, lists, booleans — passes
through as valid.

```python
r = ttk.ValidationRule("required")
r.validate(None).is_valid       # False
r.validate("").is_valid         # False
r.validate("   ").is_valid      # False
r.validate("abc").is_valid      # True
r.validate(0).is_valid          # True (not a string)
```

The fast path on a widget is the `required=True` constructor flag,
which calls `add_validation_rule("required")` for you:

```python
ttk.TextEntry(app, label="Name", required=True)
```

Default message: `"This field is required."`

---

## `'email'`

Matches the value against `[^@]+@[^@]+\.[^@]+`. The regex is
deliberately permissive — it confirms there is *some* `@` and *some*
`.` after it — and is not RFC-compliant. It is a reasonable client-side
sanity check, not a verification.

Two contract details worth knowing:

1. **`re.match`, not `re.fullmatch`.** The pattern is anchored at the
   start of the string but **not** at the end, so `"  a@b.c"` passes
   (the leading whitespace is consumed by `[^@]+`). If you need to
   reject leading or trailing junk, follow up with a `'pattern'` rule
   that uses `\Z`.
2. **No deliverability check.** `'a@b.c'` is valid by this rule; the
   domain doesn't have to resolve.

```python
r = ttk.ValidationRule("email")
r.validate("a@b.c").is_valid          # True
r.validate("foo").is_valid            # False
r.validate("  a@b.c").is_valid        # True (leading whitespace tolerated)
```

Default message: `"Enter a valid email address."`

---

## `'pattern'`

Runs `re.match(self.params['pattern'], value)`. Like `'email'`, the
match anchors at the start of the string only — append `\Z` (or `$` on
single-line input) if you require a full match.

```python
r = ttk.ValidationRule("pattern", pattern=r"\d{3}-\d{4}")
r.validate("123-4567").is_valid          # True
r.validate("abc").is_valid               # False
r.validate("123-4567 extra").is_valid    # True (re.match isn't fullmatch)

r = ttk.ValidationRule("pattern", pattern=r"\d{3}-\d{4}\Z")
r.validate("123-4567 extra").is_valid    # False
```

If `pattern` is omitted, the rule matches the empty string at
position 0 of any input — i.e., it always passes. There is no warning;
construct rules with care.

Default message: `"Value does not match the required pattern."`

---

## `'stringLength'`

Reads `min` and `max` from `params`. Defaults are `min=0` and
`max=∞`, so omitting both makes the rule a no-op.

```python
r = ttk.ValidationRule("stringLength", min=3, max=20)
r.validate("ab").is_valid                 # False
r.validate("hello").is_valid              # True
r.validate("a" * 21).is_valid             # False
```

!!! warning "Use `min` / `max`, not `min_length` / `max_length`"
    `ValidationRule.validate()` reads `params.get("min")` and
    `params.get("max")` (`core/validation/validation_rules.py:73-74`).
    Passing `min_length=` / `max_length=` (the names used in the
    `ValidationMixin.add_validation_rule` example docstring at
    `widgets/mixins/validation_mixin.py:78`) silently writes them
    into `params` but never reads them — the rule falls back to its
    `min=0` / `max=∞` defaults and accepts every string.

Default messages depend on which bound is set:

- `stringLength(min=5)` → `"Enter at least 5 characters."`
- `stringLength(min=5, max=20)` → `"Enter between 5 and 20 characters."`
- `stringLength(max=20)` → `"Enter between 0 and 20 characters."`
- `stringLength()` → `"Enter at least 0 characters."` *(non-sensical;
  pair with a `min` or write a custom `message=`)*

---

## `'custom'`

Calls `params['func'](value)` and treats a falsy return as failure.
The default trigger is `'manual'`, so a custom rule never auto-runs
on key release or focus loss — call `widget.validation(value)` (or
let `Form.validate()` drive it) explicitly.

```python
def must_start_with_x(value: str) -> bool:
    return value.startswith("X")

r = ttk.ValidationRule("custom", func=must_start_with_x, trigger="always")
r.validate("Xfoo").is_valid    # True
r.validate("foo").is_valid     # False
```

!!! warning "A `'custom'` rule with no `func=` silently passes everything"
    The validate branch is `if func and not func(value)`, so a missing
    callable short-circuits to `is_valid=True`. There is no error at
    construction or validation time.

Default message: `"Invalid value."` Override with `message="..."` (or
return a tuple from `func` and post-process the result yourself).

This is the escape hatch for everything not covered above — async
checks driven from focus-out, cross-field checks that capture the
peer widget in the closure, or composite checks that combine library
rules manually.

---

## `'compare'` (not implemented)

Listed in the `RuleType` literal but has no branch in
`ValidationRule.validate()` (`core/validation/validation_rules.py:48-86`).
Every input returns `is_valid=True`:

```python
r = ttk.ValidationRule("compare")
r.validate("anything").is_valid    # True (always)
r.validate(None).is_valid          # True (always)
```

Use a `'custom'` rule that captures the reference value or peer widget
in the closure until this is either implemented or removed from the
literal.

---

## Triggers

Each rule carries a `trigger` policy that gates **auto**-validation.
The defaults are listed in the at-a-glance table; override at
construction:

```python
ttk.ValidationRule("email", trigger="blur")
ttk.ValidationRule("stringLength", min=3, trigger="always")
```

`trigger=` is pulled out of `**kwargs` at construction
(`ValidationRule.__init__:45`); the remaining keys go into `params`.
Stored values are accessible as `rule.trigger` (string) and
`rule.params` (dict).

The widget's auto-validation passes a trigger string (`'key'` or
`'blur'`) into `validate(value, trigger)`. The filter inside
`ValidationMixin.validate` is:

```python
for rule in rules:
    if trigger != "manual" and rule.trigger not in ("always", trigger):
        continue
    # ... apply rule
```

Read it as:

| Caller's trigger | Rules that run                                   |
|------------------|--------------------------------------------------|
| `'manual'`       | every rule, regardless of its own trigger        |
| `'key'`          | rules whose trigger is `'always'` or `'key'`     |
| `'blur'`         | rules whose trigger is `'always'` or `'blur'`    |

Auto-validation always passes `'key'` or `'blur'`, so a rule tagged
`'manual'` is invisible to typing and focus changes. `Form.validate()`
runs its own loop with a different filter (`'always'` or `'manual'`
only — skips `'key'`/`'blur'`-only rules); see
[FormDialog](../../widgets/dialogs/formdialog.md) for the form-level
contract.

---

## Messages

Three layers, in priority order:

1. **`message=` argument at construction.** Wins always when non-empty.
2. **`_default_message()` for the rule type.** Generated lazily from
   `params` (see the per-rule sections above).
3. **`"Invalid input."`** — fallback for unknown rule types (currently
   only `'compare'`).

```python
ttk.ValidationRule("required", "Please enter your name.")
ttk.ValidationRule("email")  # → "Enter a valid email address."
```

The empty string `message=""` falls back to the default — only a
truthy message overrides:

```python
ttk.ValidationRule("required", "").validate("").message
# → "This field is required."  (default kicks in)
```

The selected message is carried in `ValidationResult.message` and in
the `<<Invalid>>` / `<<Validate>>` event payload's `message` key.

---

## Composing rules on a widget

Add multiple rules in order; the first failure short-circuits the
chain.

```python
entry = ttk.TextEntry(app, label="Username")
entry.add_validation_rule("required")
entry.add_validation_rule("stringLength", min=3, max=20, trigger="always")
entry.add_validation_rule("pattern", pattern=r"^[a-zA-Z0-9_]+$")
```

If the user types `""`, the `'required'` rule fails immediately and
`<<Invalid>>` fires with that message; the length and pattern checks
never run. The chain re-evaluates from the top on every key release
(50 ms-debounced), so as soon as the value passes `'required'` the
next rule takes over and the message updates.

Ordering matters: put cheap, broadly-applicable rules first (typically
`'required'`), then format checks, then business-rule `'custom'`s.

Replace the entire chain in one call:

```python
entry.add_validation_rules([
    ttk.ValidationRule("required"),
    ttk.ValidationRule("email"),
])
```

---

## Standalone use

`ValidationRule` is independent of any widget — it is a pure data
object. You can use it as a building block in a non-Tk validator,
or write tests against the rules without instantiating the framework.

```python
r = ttk.ValidationRule("email")
result = r.validate(form_field_value)
if not result.is_valid:
    print(result.message)
```

The rule object holds three pieces of state: `type` (the literal),
`message` (the user-supplied override), `trigger` (the policy), and
`params` (everything else from `**kwargs`). All four are public.

---

## Where to read next

- *What does the result object look like?* → [Results](results.md)
- *How are events wired up around a widget?* → [Validation overview](index.md)
- *How does form-level submit validation work?* → [FormDialog](../../widgets/dialogs/formdialog.md)
- *Which widgets ship the validation surface?* → [TextEntry](../../widgets/inputs/textentry.md), [NumericEntry](../../widgets/inputs/numericentry.md), [DateEntry](../../widgets/inputs/dateentry.md), [SpinnerEntry](../../widgets/inputs/spinnerentry.md), [SelectBox](../../widgets/inputs/selectbox.md)
- *How do callbacks deliver the result?* → [Callbacks](../signals/callbacks.md)
