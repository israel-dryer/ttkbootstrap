# Validation Rules

Validation rules define the conditions that input values must satisfy.
They encapsulate validation logic in a reusable, composable form.

This page explains how validation rules work conceptually in ttkbootstrap
and how they are intended to be used.

---

## What is a validation rule?

A validation rule represents a single, focused constraint.

Examples:

- value must not be empty
- value must be numeric
- value must fall within a range
- value must match a pattern

Rules answer the question: *Is this value acceptable?*

---

## Single responsibility

Each rule should do one thing.

Good rules:

- check a single condition
- return a clear outcome
- avoid side effects

Combining multiple checks into one rule makes validation harder to reason about.

---

## Composing rules

Complex validation is achieved by combining simple rules.

Composition allows:

- reuse of common constraints
- clearer intent
- easier testing

Rules may be applied sequentially or as a group, depending on context.

---

## Stateless design

Validation rules should be stateless.

They should:

- depend only on the provided value
- not modify application state
- not rely on widget internals

This makes rules reusable across widgets and contexts.

---

## Context-aware rules

Some rules require additional context.

Examples:

- comparing values across fields
- validating against application state
- enforcing conditional requirements

Context should be passed explicitly rather than captured implicitly.

---

## Error messaging

Rules often provide descriptive messages when validation fails.

Good messages:

- explain what went wrong
- suggest corrective action
- avoid technical jargon

Clear messages improve user experience.

---

## Timing considerations

Rules may be evaluated:

- continuously
- on focus change
- on submission

Choosing the right timing avoids user frustration.

---

## ttkbootstrap guidance

ttkbootstrap encourages:

- small, focused rules
- explicit composition
- separation from UI logic
- consistent messaging

These practices improve clarity and maintainability.

---

## Common pitfalls

- overly complex rules
- mixing UI concerns into rules
- hardcoding context
- duplicating logic across widgets

Understanding rule design avoids these problems.

---

## Next steps

- See **Results** for interpreting validation outcomes
- See **Validation Overview** for lifecycle context
- See **Widgets → Forms** for practical examples
