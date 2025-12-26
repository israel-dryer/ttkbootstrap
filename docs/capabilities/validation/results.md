# Validation Results

Validation results represent the **outcome** of applying one or more validation
rules to a value.

Rather than returning raw booleans, ttkbootstrap models validation outcomes
explicitly so that applications can react consistently and provide meaningful
user feedback.

---

## What is a validation result?

A validation result answers the question:

> *Is this value valid, and if not, why?*

A result typically contains:

- validity state (valid / invalid / warning)
- one or more messages
- optional contextual data

This structure allows validation to drive UI behavior beyond simple acceptance
or rejection.

---

## Valid vs invalid vs warning

Validation results may represent different severities:

- **Valid** — the value satisfies all rules
- **Invalid** — the value violates one or more rules
- **Warning** — the value is acceptable but noteworthy

Distinguishing these states allows more nuanced UX.

---

## Aggregating results

When multiple rules are applied, results must be combined.

Aggregation may:

- stop on first failure
- collect all failures
- prioritize certain rules

The chosen strategy affects both performance and user feedback.

---

## Driving UI feedback

Validation results often control:

- error messages
- visual indicators
- disabled or enabled actions
- focus behavior

By modeling results explicitly, these effects can be applied consistently.

---

## Relationship to widgets

Widgets typically:

- trigger validation
- receive validation results
- update their appearance accordingly

Widgets should not interpret validation logic themselves — they react to results.

---

## Integration with signals

Validation results integrate naturally with signals.

A signal may:

- represent the current validation state
- propagate changes to dependent UI elements
- coordinate form-level validity

This enables declarative, reactive validation flows.

---

## Timing and user experience

When results are presented matters.

Consider:

- delaying error messages until focus loss
- showing warnings non-intrusively
- avoiding constant error churn while typing

Good timing improves usability.

---

## ttkbootstrap guidance

ttkbootstrap promotes:

- explicit result objects
- consistent severity levels
- separation of validation and presentation
- clear, user-focused messaging

These practices lead to predictable behavior.

---

## Common pitfalls

- treating validation as binary only
- leaking rule logic into UI code
- inconsistent severity handling
- unclear feedback messaging

Explicit results help avoid these issues.

---

## Next steps

- See [Validation Rules](rules.md) for defining constraints.
- See [Widgets](../../widgets/index.md) for validation in practice.
- See [Signals](../signals/signals.md) for propagating validation state.
