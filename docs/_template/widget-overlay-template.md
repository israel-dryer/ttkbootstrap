---
title: OverlayWidgetName
---

# OverlayWidgetName

1–2 paragraphs describing:

- what kind of overlay or feedback this widget provides (tooltip, toast, banner, popover)
- whether it is **blocking or non-blocking**
- how it appears and disappears (hover, time-based, user action)

Keep this focused on *feedback and guidance*, not data entry.

---

## Framework integration

**Application behavior**

- Trigger model (hover/click/programmatic)
- Safety behavior (auto-dismiss, outside click, focus rules)

**Design System**

- How the overlay uses theme tokens (surface, borders, typography)
- How emphasis/intent is communicated (colors, icons)

**Signals & Events**

- Lifecycle hooks (shown, dismissed, action selected)
- Recommended patterns for integrating with app state

---

## Basic usage

Show the simplest, most common usage.

```python
# minimal, copy/paste runnable
```

If the widget has multiple trigger styles (hover vs programmatic), show only the primary one here.

---

## What problem it solves

Explain why this overlay exists, such as:

- providing contextual help without clutter
- giving feedback without interrupting flow
- surfacing transient information
- reducing the need for modal dialogs

Contrast briefly with dialogs or persistent UI elements.

---

## Core concepts

Explain how to think about this overlay.

Common subsections include:

- trigger model (hover, click, automatic)
- blocking vs non-blocking behavior
- lifecycle (show, update, dismiss)
- safety behavior (auto-dismiss, outside click, focus rules)

---

## Content and presentation

Describe what content can appear:

- title vs message
- icons or imagery
- action buttons (if supported)
- text wrapping and layout rules

Provide short examples if helpful.

---

## Positioning

Explain where the overlay appears:

- relative to a widget (anchored)
- relative to cursor
- relative to screen edges

Include auto-flip or screen-safe behavior if supported.

---

## Behavior and lifecycle

Describe interaction behavior:

- how it is shown
- how it is dismissed
- what happens on user interaction
- how long it remains visible

If the widget is fully automatic, state that clearly.

---

## Events and callbacks

Document lifecycle events or callbacks, such as:

- dismissed
- clicked
- action selected

```python
def on_dismissed(data):
    ...

widget.on_dismissed(on_dismissed)
```

---

## UX guidance

Prescriptive advice:

- when to prefer overlays vs dialogs
- recommended text length and tone
- accessibility considerations
- avoiding notification fatigue

---

## When to use / when not to

**Use OverlayWidgetName when:**

- …

**Avoid OverlayWidgetName when:**

- …

---

## See also

**Related widgets**

- **Dialog** — blocking decisions
- **Action widgets** — triggers for overlays
- **OtherOverlayWidget** — alternative feedback patterns

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Signals & Events](../../capabilities/signals/index.md)

**API reference**

- **API Reference:** `ttkbootstrap.OverlayWidgetName`
- **Related guides:** Feedback, UX Patterns, Accessibility
