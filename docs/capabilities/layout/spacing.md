# Spacing

Spacing controls the visual separation between widgets and layout regions.
Consistent spacing is critical for readable, professional user interfaces.

This page explains how spacing works in Tk and how ttkbootstrap promotes
clear and consistent spacing practices.

---

## Types of spacing

Spacing generally falls into three categories:

- **Padding** — space inside a container around its contents
- **Margins** — space outside a widget (managed by the container)
- **Gaps** — uniform spacing between sibling widgets

Tk exposes spacing through geometry manager options rather than a dedicated
layout system.

---

## Padding vs margins

Tk does not explicitly distinguish between padding and margins.

Instead:
- padding is usually applied via container options
- external spacing is controlled by geometry manager parameters

ttkbootstrap adopts a conceptual distinction even when the underlying mechanism
is the same.

---

## Consistent spacing

Inconsistent spacing is a common UI problem.

ttkbootstrap encourages:
- using container-level spacing
- defining spacing once per layout region
- avoiding per-widget spacing tweaks

Consistency improves both appearance and maintainability.

---

## Spacing and resizing

Spacing affects how layouts resize.

Excessive spacing:
- wastes screen space
- exaggerates resizing artifacts

Insufficient spacing:
- makes interfaces feel cramped
- reduces readability

Balance is essential.

---

## Vertical vs horizontal spacing

Spacing needs differ by direction.

Common patterns:
- tighter vertical spacing in forms
- looser spacing between sections
- consistent horizontal alignment

Containers help enforce these patterns.

---

## Responsive considerations

As window size changes:
- spacing may appear larger or smaller
- layout density changes

Avoid absolute assumptions about spacing in resizable layouts.

---

## ttkbootstrap guidance

ttkbootstrap promotes:

- spacing as a layout concern
- container-managed spacing
- reuse of spacing patterns
- avoidance of ad-hoc values

These practices lead to predictable layouts.

---

## Common pitfalls

- mixing multiple spacing strategies
- hardcoding spacing values everywhere
- compensating for layout bugs with padding

Most spacing issues stem from unclear layout intent.

---

## Next steps

- See **Scrolling** for how spacing interacts with scroll regions
- See **Containers** for layout composition
- See **Platform → Geometry & Layout** for layout mechanics
