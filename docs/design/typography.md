---
icon: fontawesome/solid/font
---

# Typography

Typography in ttkbootstrap is designed to be **consistent, scalable, and semantic**.

Rather than treating fonts as raw tuples or widget-specific configuration details, ttkbootstrap encourages you to think
in terms of **typographic roles**—such as body text, headings, labels, and UI controls—and apply them consistently
across your application.

This page explains the **design model and intent** behind typography in ttkbootstrap so new users can understand how
text styling is meant to work before applying it in code.

Practical usage examples are covered in the Guides section.

---

## Design Goals

The typography system is built around the following goals:

- **Semantic roles**  
  Text should communicate purpose and hierarchy, not just size.

- **Consistency**  
  The same role should look the same everywhere it appears.

- **Scalability**  
  Typography should adapt to DPI scaling, font changes, and accessibility needs.

- **Theme alignment**  
  Text styling should integrate cleanly with themes and platform conventions.

To support these goals, ttkbootstrap defines typography in terms of **roles**, **scales**, and **modifiers**.

---

## Typographic Roles

A **typographic role** represents how text is used in the interface.

Common roles include:

- body text
- headings
- labels
- captions
- emphasis text

Roles define **hierarchy and intent**, not specific font families or sizes.

For example:

- Body text prioritizes readability.
- Headings establish structure and navigation.
- Labels are compact and functional.
- Captions provide secondary or supporting information.

Each theme maps these roles to concrete font definitions appropriate for the platform.

---

## Typography Scale

Typography follows a **relative scale**, not fixed pixel values.

This allows text to:

- scale with DPI and accessibility settings,
- remain proportional across the interface,
- adapt naturally to different platforms and fonts.

Sizes are defined in relation to each other, creating a predictable hierarchy from small supporting text to large
display text.

The exact size values are theme-defined and may vary between environments.

---

## Modifiers

Modifiers refine typography without changing its underlying role.

Examples include:

- weight adjustments (light, bold)
- style changes (italic, underline)
- emphasis or de-emphasis

Modifiers should be used to **clarify meaning**, not to override hierarchy.

> **Design rule:**  
> If text requires heavy modification to be readable or noticeable, the underlying typographic role is likely incorrect.

Used consistently, modifiers enhance clarity without fragmenting the visual language.

---

## Theme Resolution

Typography is resolved through the active theme.

Themes define:

- font families,
- base sizes,
- line heights,
- weight mappings.

Applications do not hardcode font choices.  
Instead, they rely on roles that themes interpret appropriately for the platform.

Switching themes updates typography automatically while preserving hierarchy and intent.

---

## Platform Considerations

Desktop platforms differ significantly in typography:

- default system fonts,
- font rendering engines,
- spacing and metrics,
- accessibility settings.

The typography system is designed to **respect platform conventions** while maintaining consistent hierarchy and
structure.

This allows ttkbootstrap applications to feel native without sacrificing coherence.

---

## ttkbootstrap’s Role

In v2, ttkbootstrap does not replace Tkinter’s font system.

Instead, it:

- formalizes typographic roles,
- documents consistent hierarchy,
- integrates typography with theming and layout,
- encourages scalable, accessible text usage.

Typography remains fully compatible with Tkinter’s font mechanisms.

---

## What This Section Does Not Cover

This page does not include:

- widget-specific font configuration,
- font tuple construction,
- dynamic font updates,
- code examples.

Those topics are covered in:

- **Guides → Theming & Appearance**
- **Reference → Typography Tokens**
- **Widgets → Text Styling Conventions**

---

## Summary

The ttkbootstrap typography system focuses on **roles over values**.

By applying semantic roles, consistent scales, and restrained modifiers:

- text remains readable and structured,
- interfaces scale across environments,
- and typography reinforces the overall design system.

Understanding this model makes typography easier to apply correctly—and harder to misuse.
