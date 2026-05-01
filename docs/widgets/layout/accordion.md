---
title: Accordion
---

# Accordion

`Accordion` is a vertical stack of [Expander](expander.md) sections
with a built-in mutual-exclusion policy. By default, opening one
section auto-collapses the others; opt out with `allow_multiple=True`
for a multi-open accordion, or `allow_collapse_all=False` to require
at least one section to stay open.

`Accordion` extends [Frame](frame.md), so the same `padding`,
`surface`, `show_border`, and `input_background` tokens shape the
outer container. The sections themselves are [Expander](expander.md)
widgets — `Accordion` owns their lifecycle (creation, ordering,
removal, optional separators) and listens for `<<Toggle>>` to enforce
its policies, then re-emits `<<AccordionChange>>` for the group as a
whole.

<figure markdown>
![accordion](../../assets/dark/widgets-accordion.png#only-dark)
![accordion](../../assets/light/widgets-accordion.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

accordion = ttk.Accordion(app, accent="primary", variant="solid")
accordion.pack(fill="x", padx=10, pady=10)

general = accordion.add(title="General Settings")
ttk.CheckButton(general.content, text="Enable feature").pack(anchor="w")

advanced = accordion.add(title="Advanced Settings")
ttk.Label(advanced.content, text="Advanced options").pack(anchor="w")

about = accordion.add(title="About")
ttk.Label(about.content, text="Version 1.0").pack(anchor="w")

app.mainloop()
```

`add()` returns the [Expander](expander.md), and child widgets go on
its `.content` frame — not on the expander itself. The first call to
`add()` packs the section directly under the accordion; subsequent
sections stack underneath in insertion order.

---

## Layout model

The accordion is a vertical stack — there is no horizontal mode. Each
section is packed `fill='x'` along the top axis of the outer Frame in
the order it was added. Section content height is whatever the
expander reports; the accordion does not impose a maximum height or a
scroll viewport. For a long accordion in a fixed-height region, wrap
it in a [ScrollView](scrollview.md).

**Section identity is keyed.** Every section has a string `key` —
either the explicit `key=` you pass to `add()`, or an auto-generated
`expander_<n>` (the counter increments per call, never reuses).
`expand(key)`, `collapse(key)`, `remove(key)`, `item(key)`, and
`configure_item(key, …)` all address sections by that key.

```python
accordion.add(key="general", title="General")
accordion.add(key="advanced", title="Advanced")

accordion.expand("advanced")
accordion.collapse("general")

for key in accordion.keys():
    print(key, accordion.item(key).cget("title"))
```

**Optional separators.** With `show_separators=True`, a horizontal
[Separator](separator.md) is inserted between each pair of adjacent
expanders. The first section has no leading separator. Reconfiguring
`show_separators` at runtime takes effect on **future** `add()` calls
only — existing sections keep their current separator layout. Plan to
toggle this at construction time, not after expanders are populated.

```python
accordion = ttk.Accordion(app, show_separators=True)
```

**Removing a section** also removes its associated separator. If the
removed section was open and `allow_collapse_all=False`, the first
remaining section is auto-expanded so the accordion never becomes
fully collapsed.

---

## Common options

| Option               | Type         | Default | Notes                                                                          |
| -------------------- | ------------ | ------- | ------------------------------------------------------------------------------ |
| `allow_multiple`     | bool         | `False` | Allow multiple sections open simultaneously                                    |
| `allow_collapse_all` | bool         | `True`  | If `False`, at least one section must stay open; first added is auto-expanded  |
| `show_separators`    | bool         | `False` | Insert horizontal separators between sections (effective at construction time) |
| `accent`             | str          | `None`  | Default accent **forwarded to child Expanders** (see *Accent forwarding* below) |
| `variant`            | str          | `None`  | Default variant **forwarded to child Expanders** (`solid` or `default`)        |

Inherited from [Frame](frame.md):

- `padding`, `width`, `height` — outer-frame geometry. Setting
  `show_border=True` automatically defaults `padding=3` to keep the
  border from clipping the section corners.
- `surface`, `show_border`, `input_background` — themed surface and
  fill tokens for the container. These are independent from the
  per-Expander accent: an `Accordion(surface="card")` paints the
  container, while the inner section headers carry their own colors.

### Accent forwarding

`Accordion`'s `accent` and `variant` are **not** container-surface
tokens — they're stored on the accordion and forwarded as the default
`accent` / `variant` to every Expander created via `add()`. The
container's surface stays at the inherited default (`content`). To
tint the accordion's container, pass `surface="card"` (or another
surface token); to tint the section headers, pass `accent`/`variant`.

```python
ttk.Accordion(app, accent="success", variant="solid")
# all sections render with the solid-success header style;
# the container itself is unstyled
```

!!! warning "Per-call accent collides with accordion accent"

    When the accordion has its own `accent`, passing `accent=` (or
    `variant=`) to a per-call `add(...)` raises
    `TypeError: got multiple values for keyword argument 'accent'`.
    Pick one source: either set the accent on the accordion (and
    every section gets it) or leave the accordion's accent unset and
    pass per-section accents to `add()`. Mixing them is not
    supported.

Existing `Expander` instances passed via `add(expander=existing)` keep
their own accent and variant — the accordion does **not** restyle
them. The only configuration `add()` always applies to an existing
Expander is `highlight=True`, so the open section visually marks
itself.

---

## Behavior

**Mutual exclusion** is enforced by listening on each Expander's
`<<Toggle>>` event. When `allow_multiple=False` (the default) and one
section is opened, every other open section is collapsed. The
internal `_updating` re-entrancy guard prevents the cascading
collapse from re-firing the policy.

**`allow_collapse_all=False` enforcement.** Attempting to close the
last open section — by clicking its header, calling
`accordion.collapse(key)`, or directly calling `expander.collapse()`
— is reverted: the accordion calls `expander.expand()` on the same
section. The first section is also auto-expanded at `add()` time when
no other sections are open.

**`expand_all()` and `collapse_all()` are mode-gated.**
`expand_all()` is a no-op when `allow_multiple=False`;
`collapse_all()` is a no-op when `allow_collapse_all=False`. There is
no exception or warning — they just return.

```python
accordion = ttk.Accordion(app, allow_multiple=True)
accordion.expand_all()    # opens every section
accordion.collapse_all()  # closes every section
```

**Programmatic `expand(key)` / `collapse(key)`** trigger the same
event chain as a header click: the Expander emits `<<Toggle>>`, the
accordion's listener enforces mutual exclusion (collapsing siblings
when `allow_multiple=False`), then `<<AccordionChange>>` fires.

**Keyboard navigation.** Each Expander header takes focus
(`takefocus=True` is set on the inner header frame), so `<Tab>` walks
the section headers in order. `<Return>` and `<space>` toggle the
focused section.

**Reconfiguration.** `allow_multiple`, `allow_collapse_all`, and
`show_separators` are all reconfigurable through `configure(...)` and
queryable through `cget(...)`. Only `show_separators` has a layout
caveat: existing sections keep their current separator state, and
only future `add()` calls react to the new value.

---

## Events

`<<AccordionChange>>` fires whenever the set of expanded sections
changes — on user click, on programmatic `expand` / `collapse`, on
`expand_all` / `collapse_all`, and on `remove(key)` (provided at
least one section remains; removing the last section does **not**
fire the event).

| Event                | Payload (`event.data`)              | Notes                              |
| -------------------- | ----------------------------------- | ---------------------------------- |
| `<<AccordionChange>>` | `{"expanded": list[Expander]}`     | List of currently-expanded sections, in insertion order |

```python
def on_change(event):
    titles = [exp.cget("title") for exp in event.data["expanded"]]
    print("Open sections:", titles)

accordion.on_accordion_changed(on_change)
```

`on_accordion_changed(callback)` registers the listener and returns a
bind id. `off_accordion_changed(bind_id)` unbinds a specific listener;
`off_accordion_changed()` (no argument) unbinds all `<<AccordionChange>>`
handlers.

For per-section toggles, bind on each Expander's `<<Toggle>>` event
directly via `expander.on_toggled(...)`. The accordion's listener
runs first; your handler runs second.

---

## When should I use Accordion?

Use `Accordion` when:

- you have several related sections and only one (or a small set)
  should be visible at a time
- you want a structured stepper-style flow (configure → review →
  confirm) where the user advances through sections
- screen space is limited and mutual-exclusion focus helps users not
  drown in simultaneously-open content

Prefer **multiple [Expander](expander.md) widgets** when each section
should be independently collapsible without the accordion's
mutual-exclusion policy.

Prefer **[Notebook](../views/notebook.md)** when content switching
should be tab-driven and only one section is ever visible — accordions
keep section *headers* visible at all times; notebooks hide everything
but the active tab.

Prefer **[LabelFrame](labelframe.md)** or plain
[Frame](frame.md) sections when no section is ever collapsed — the
accordion's chrome (chevrons, click handlers) adds noise without
benefit.

---

## Related widgets

- **[Expander](expander.md)** — the section primitive Accordion
  manages; usable standalone for a single collapsible region
- **[Notebook](../views/notebook.md)** — tab-driven content switching
  with a similar one-active-at-a-time policy
- **[LabelFrame](labelframe.md)** — titled bordered group when
  sections never collapse
- **[Frame](frame.md)** — parent class; container surface tokens
  behave identically
- **[Separator](separator.md)** — the separator widget Accordion
  inserts between sections when `show_separators=True`
- **[ScrollView](scrollview.md)** — wrap the accordion when its
  combined section height can exceed the available viewport

---

## Reference

- **API reference:** [`ttkbootstrap.Accordion`](../../reference/widgets/Accordion.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
