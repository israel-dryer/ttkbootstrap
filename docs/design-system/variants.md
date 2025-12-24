---
title: Variants & States
---

# Variants & States

Variants and states define **how widgets communicate intent and interaction** in a ttkbootstrap application.

Rather than styling widgets ad hoc, ttkbootstrap encourages expressing *what a widget represents* (its variant) and *how
it is currently being interacted with* (its state). The visual system resolves these concepts consistently through
theming.

This page explains the **design model and intent** behind variants and states so new users understand how interaction
styling is meant to work before applying it in code.

Practical usage and APIs are covered in the Guides and Reference sections.

---

## Design Goals

The variants and states system is guided by the following goals:

- **Semantic clarity**  
  Visual differences should communicate meaning, not decoration.

- **Consistency**  
  The same variant or state should look and behave consistently across widgets.

- **Predictability**  
  Users should be able to anticipate how widgets will respond to interaction.

- **Theme integration**  
  Variants and states should resolve through the active theme.

- **Accessibility**  
  Interaction states must remain perceivable across contrast levels and input methods.

Together, variants and states form the **interaction language** of the interface.

---

## Variants: Meaning & Emphasis

A **variant** expresses the *semantic intent* or *emphasis level* of a widget.

Common variant concepts include:

- primary actions,
- secondary actions,
- destructive actions,
- subtle or de-emphasized actions,
- informational presentation.

Variants answer the question:
> *What kind of action or information is this?*

They do not describe interaction or transient behavior.

---

## Variants Are Stable

Variants are **stable over time**.

A widget’s variant typically:

- does not change during interaction,
- represents its role within the interface,
- remains consistent across states.

For example, a destructive action remains destructive whether hovered, focused, or disabled.

This stability helps users build trust and familiarity.

---

## States: Interaction & Context

A **state** represents a widget’s current interaction or context.

Common states include:

- default (idle),
- hover,
- active or pressed,
- focused,
- disabled,
- selected,
- invalid or error.

States answer the question:
> *What is happening to this widget right now?*

States are transient and change in response to user input or application logic.

---

## States Are Dynamic

Unlike variants, states are **dynamic**.

They:

- change frequently,
- reflect real-time interaction,
- provide feedback to user actions.

Clear state feedback is essential for usability and accessibility.

---

## Variant + State Resolution

Variants and states work **together**.

A widget’s appearance is resolved by combining:

- its semantic variant,
- its current state,
- the active theme.

For example:

- a primary button looks different when hovered than when idle,
- a disabled destructive action remains visually destructive but muted,
- a selected navigation item reflects both role and state.

This resolution is handled centrally by the theming system.

---

## Interaction Feedback

States provide immediate visual feedback to user actions, including:

- pointer interaction,
- keyboard navigation,
- focus changes,
- validation feedback.

Feedback should be:

- timely,
- clearly perceivable,
- consistent across widgets.

> **Design rule:**  
> If a state change is not visually apparent, the interaction is incomplete.

---

## Accessibility Considerations

Variants and states must remain perceivable for all users.

This includes:

- sufficient contrast in all states,
- visible focus indicators,
- non-color cues where appropriate,
- keyboard-only interaction support.

Accessibility is not an optional layer—it is a core requirement of state design.

---

## ttkbootstrap’s Role

In v2, ttkbootstrap does not redefine interaction states.

Instead, it:

- formalizes variant and state semantics,
- documents consistent interaction patterns,
- integrates state resolution with themes,
- avoids widget-specific ad hoc styling.

This ensures interaction behavior remains predictable and scalable.

---

## What This Section Does Not Cover

This page does not include:

- widget-specific variant lists,
- state APIs or configuration,
- animation or timing details,
- code examples.

Those topics are covered in:

- **Guides → Interaction Patterns**
- **Reference → Variants & States**
- **Widgets → Individual Widget Behavior**

---

## Summary

Variants define **what a widget is**.  
States define **what is happening to it**.

By separating meaning from interaction:

- interfaces remain consistent,
- behavior becomes predictable,
- and theming scales cleanly across widgets.

Understanding this model makes it easier to design interfaces that feel responsive, intentional, and accessible.
