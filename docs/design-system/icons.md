---
title: Icons
---

# Icons

Icons in ttkbootstrap are treated as **semantic UI elements**, not decorative images.

They are used to:

- reinforce meaning,
- improve scanability,
- communicate state,
- and support common desktop interaction patterns.

This page explains the **design intent and architectural role** of iconography in ttkbootstrap so new users understand
how icons are meant to be used before applying them in code.

Practical usage examples and APIs are covered in the Guides and Reference sections.

---

## Design Goals

The iconography system is guided by a small set of principles:

- **Semantic clarity**  
  Icons should convey meaning consistently, not style arbitrarily.

- **Consistency**  
  The same icon should represent the same concept everywhere.

- **State awareness**  
  Icons should clearly reflect interaction and application state.

- **Theme integration**  
  Icons should adapt naturally to light/dark themes and color schemes.

- **Scalability**  
  Icons must scale cleanly across DPI settings and screen densities.

To support these goals, ttkbootstrap treats icons as **first-class UI resources** rather than static images.

---

## Semantic Usage

Icons are most effective when they **reinforce an existing concept**, rather than introducing new meaning.

Common semantic roles include:

- actions (save, delete, search),
- navigation (back, forward, expand),
- status (success, warning, error),
- affordances (dropdown, close, more options).

Icons should complement text, not replace it, unless the meaning is universally understood.

> **Design rule:**  
> If an icon requires a tooltip to explain its meaning, it may not be appropriate on its own.

---

## Icon Sets

ttkbootstrap does not mandate a single icon set.

Instead, it supports working with **icon providers**, allowing applications to choose icon families that match their
brand and platform expectations.

Common characteristics of a good icon set:

- complete coverage of common UI actions,
- consistent stroke weight and visual style,
- availability at multiple sizes,
- compatibility with recoloring.

Icon sets should be chosen **once per application** and used consistently.

---

## Size & Alignment

Icons are typically displayed at discrete, intentional sizes.

Rather than arbitrary scaling, icons should:

- align visually with surrounding text,
- match control height and density,
- preserve pixel alignment where possible.

Consistent sizing helps maintain visual rhythm and prevents icons from drawing unintended attention.

---

## Color & State

Icons participate fully in the application’s color system.

They may reflect:

- default state,
- hover and active states,
- disabled state,
- semantic intent (e.g., danger, success).

Icon color should always derive from **semantic color tokens**, not hardcoded values.

This ensures icons remain legible and appropriate across themes.

---

## Interactive Icons

In desktop applications, icons are often interactive.

Common patterns include:

- icon buttons,
- disclosure indicators,
- contextual menus,
- status toggles.

Interactive icons should:

- provide clear affordance,
- respond visually to interaction,
- respect accessibility and focus behavior.

Icons should never be the *only* indicator of critical state or action.

---

## Platform Considerations

Desktop platforms differ in icon conventions:

- icon metaphors,
- default sizes,
- visual density,
- contrast expectations.

The iconography system is designed to:

- respect platform norms,
- allow platform-specific icon choices when necessary,
- maintain consistent meaning across environments.

A visually native feel is often more important than strict visual uniformity.

---

## ttkbootstrap’s Role

In v2, ttkbootstrap does not invent new icon standards.

Instead, it:

- provides infrastructure for managing icons as reusable resources,
- integrates icons with theming and state,
- encourages semantic and consistent usage,
- avoids hardcoding icon imagery into widget logic.

Icon selection and visual style remain application-level decisions.

---

## What This Section Does Not Cover

This page does not include:

- icon loading APIs,
- provider-specific configuration,
- widget-level icon examples,
- asset packaging instructions.

Those topics are covered in:

- **Guides → Icon Usage**
- **Reference → Icon Providers**
- **Widgets → Icon Support**

---

## Summary

The ttkbootstrap iconography system emphasizes **meaning, consistency, and adaptability**.

By treating icons as semantic UI elements rather than decoration:

- interfaces become easier to scan,
- interaction states are clearer,
- and visual language remains cohesive.

Understanding this model will help you use icons effectively across your application.
