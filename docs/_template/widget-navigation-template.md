---
title: NavigationWidgetName
---

# NavigationWidgetName

1–2 paragraphs describing:

- what kind of navigation this widget provides (tabs, stacked pages, views)
- how users move between views (random access vs sequential flow)
- whether navigation is stateful (history) or stateless

Mention common use cases (tabs, wizards, inspectors, dashboards).

---

## Framework integration

**Application structure**

- How views/pages are created and managed
- Whether navigation preserves state/history

**Signals & Events**

- How navigation changes are observed (events/callbacks/signals)
- Recommended patterns for coordinating navigation with app state

**Layout Properties**

- Expected container usage
- Sticky/expansion conventions for navigation + content regions

---

## Basic usage

Show the simplest runnable example that demonstrates navigation between views.

```python
# minimal, copy/paste runnable
```

---

## What problem it solves

Explain why this navigation widget exists, such as:

- switching between related views without new windows
- managing multi-step workflows
- providing persistent navigation within a region

Contrast briefly with other navigation patterns.

---

## Core concepts

Explain how to think about the navigation model.

Typical subsections:

- pages or views are keyed
- how navigation targets are referenced
- random-access vs sequential navigation
- history and state (if applicable)

---

## Pages and views

Explain how pages/views are created and managed:

- creating new pages automatically
- adding existing widgets as pages
- lifecycle of pages (created, shown, hidden, destroyed)

Include a concise example.

---

## Navigation behavior

Describe how navigation works:

- switching pages
- back/forward behavior (if supported)
- replace vs push semantics
- passing data during navigation (if supported)

---

## Events

Document navigation lifecycle events.

Explain:

- what events fire
- when they fire
- what data is included in the payload

```python
def on_changed(event):
    ...

nav.on_changed(on_changed)
```

---

## Common options & patterns

Curated options and patterns, such as:

- layout and sticky behavior
- enabling/disabling navigation targets
- lazy loading or conditional navigation
- integrating with buttons or menus

---

## UX guidance

Prescriptive advice:

- when to use tabs vs stacked navigation
- avoiding mixed navigation metaphors
- keeping navigation predictable and discoverable

---

## When to use / when not to

**Use NavigationWidgetName when:**

- …

**Avoid NavigationWidgetName when:**

- …

---

## See also

**Related widgets**

- **OtherNavigationWidget** — alternative navigation pattern
- **Layout widget** — for arranging navigation + content
- **Action widgets** — triggers for navigation

**Framework concepts**

- [Signals & Events](../../capabilities/signals/index.md)
- [Layout Properties](../../capabilities/layout-props.md)

**API reference**

- **API Reference:** `ttkbootstrap.NavigationWidgetName`
- **Related guides:** Navigation, Layout, UX Patterns
