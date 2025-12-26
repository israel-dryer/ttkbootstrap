# Validation

Validation capabilities provide a structured way to verify, constrain, and
communicate the correctness of user input and application state.

Rather than embedding validation logic ad hoc in widgets or callbacks,
ttkbootstrap formalizes validation as a shared capability with clear roles and
lifecycles.

---

## What is validation?

Validation is the process of determining whether a value satisfies a set of
rules.

In UI applications, validation is commonly used for:

- form input correctness
- required fields
- type and range constraints
- cross-field consistency

Validation is not only about rejecting input — it is also about **communicating
intent and feedback**.

---

## Validation as a capability

Validation behavior is shared across many widgets and patterns.

By treating validation as a capability:

- rules can be reused
- results are represented consistently
- UI feedback can be standardized

Widgets participate in validation, but do not own the validation logic.

---

## Rules and results

Validation is split into two primary concepts:

- **Rules** — define what conditions must be satisfied
- **Results** — describe the outcome of applying rules

Separating these concerns keeps validation logic composable and testable.

---

## Timing and lifecycle

Validation may occur at different points:

- as the user types
- when a field loses focus
- when a form is submitted
- when dependent values change

Choosing the correct timing is critical for usability.

---

## Relationship to signals and callbacks

Validation integrates with other capabilities:

- callbacks trigger validation
- signals propagate validated state
- widgets update appearance based on results

This allows validation to fit naturally into application workflows.

---

## UI feedback

Validation results often drive UI feedback:

- error messages
- warning indicators
- disabled actions
- focus management

ttkbootstrap encourages consistent feedback patterns rather than ad-hoc styling.

---

## ttkbootstrap guidance

ttkbootstrap promotes:

- reusable validation rules
- explicit validation results
- separation of validation and UI logic
- clear feedback to users

These practices improve correctness and user experience.

---

## Common pitfalls

- validating too aggressively
- mixing validation logic into callbacks
- inconsistent feedback patterns
- unclear ownership of validation state

Understanding validation as a capability helps avoid these issues.

---

## Next steps

- See [Rules](rules.md) for defining validation constraints.
- See [Results](results.md) for interpreting validation outcomes.
- See [Widgets](../../widgets/index.md) for validation in practice.
