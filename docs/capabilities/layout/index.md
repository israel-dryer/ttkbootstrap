# Layout Capabilities

Layout capabilities describe how widgets participate in layout, spacing, and
scrolling behavior.

Rather than documenting geometry behavior repeatedly on individual widgets,
ttkbootstrap formalizes layout concerns as shared capabilities that apply
consistently across the framework.

This section explains layout behavior conceptually and how ttkbootstrap guides
layout usage.

---

## Layout as a capability

Layout is not a property of a widget alone — it is a **relationship between a
widget and its container**.

Layout capabilities describe:

- how widgets are placed inside containers
- how space is allocated and resized
- how scrolling regions are managed

These behaviors are shared across many widgets.

---

## Geometry managers

Tk provides three geometry managers:

- `pack`
- `grid`
- `place`

Each manager has different trade-offs.

ttkbootstrap does not replace these managers, but provides structure and
conventions around their use.

---

## Container responsibility

Containers own layout decisions.

Widgets:

- request size
- expose layout options
- respond to resizing

Containers:

- determine spacing
- control expansion
- define scrolling behavior

ttkbootstrap encourages composing layouts from containers rather than tuning
individual widgets.

---

## Declarative intent

Layout bugs often come from implicit behavior.

ttkbootstrap promotes:

- explicit spacing
- clear expansion rules
- predictable container hierarchies

This makes layout behavior easier to reason about and debug.

---

## Scrolling as layout

Scrolling is a layout concern, not a widget feature.

Scrollable containers:

- manage viewport and content size
- synchronize scrollbars
- adapt to dynamic content

ttkbootstrap provides standardized scrolling patterns to avoid ad-hoc solutions.

---

## Relationship to widget lifecycle

Layout resolution depends on widget lifecycle.

Size and position:

- are not final during construction
- are resolved after the event loop runs

Layout capabilities should be used with lifecycle timing in mind.

---

## Common pitfalls

- mixing geometry managers in the same container
- querying size before layout resolution
- relying on implicit spacing
- implementing scrolling manually

Understanding layout as a capability helps avoid these issues.

---

## Next steps

- See **Containers** for layout composition patterns
- See **Spacing** for padding and margins
- See **Scrolling** for scrollable layout behavior
