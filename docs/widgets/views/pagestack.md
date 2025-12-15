---
title: PageStack
icon: fontawesome/solid/layer-group
---

# PageStack

`PageStack` is a navigation container that manages multiple “pages” where only one page is visible at a time. It provides **stack-based navigation with history**, similar to a web browser, making it ideal for wizards, multi-step workflows, and view-based navigation inside a single window.

<!--
IMAGE: PageStack navigation flow
Suggested: Three pages with forward/back navigation arrows and a visible history stack
Theme variants: light / dark
-->

---

## Basic usage

Create a PageStack, add pages, and navigate between them:

```python
import ttkbootstrap as ttk

app = ttk.App()

stack = ttk.PageStack(app, padding=10)
stack.pack(fill="both", expand=True)

page1 = stack.add_page("start", padding=10)
page2 = stack.add_page("details", padding=10)
page3 = stack.add_page("confirm", padding=10)

ttk.Label(page1, text="Start page").pack()
ttk.Button(page1, text="Next", command=lambda: stack.navigate("details")).pack()

ttk.Label(page2, text="Details page").pack()
ttk.Button(page2, text="Next", command=lambda: stack.navigate("confirm")).pack()
ttk.Button(page2, text="Back", command=stack.back).pack()

ttk.Label(page3, text="Confirm page").pack()
ttk.Button(page3, text="Back", command=stack.back).pack()

app.mainloop()
```

<!--
IMAGE: Basic PageStack example
Suggested: Wizard-style layout with Next / Back buttons
-->

---

## What problem it solves

Many desktop workflows are **sequential or stateful**, where users move forward and backward through views rather than switching arbitrarily. `PageStack` solves this by:

- Showing exactly one page at a time
- Maintaining a navigation history
- Supporting back and forward navigation
- Emitting rich lifecycle events for page transitions
- Allowing data to be passed between pages during navigation

This makes it well-suited for wizards, setup flows, inspectors, and task-based navigation.

---

## Core concepts

### Pages are keyed

Each page is identified by a **unique string key**:

```python
stack.add_page("settings")
stack.navigate("settings")
```

Keys are stable and human-readable, making them preferable to index-based navigation.

---

### Adding pages

You can add pages in two ways:

**Create a new page automatically**:

```python
page = stack.add_page("profile", padding=10)
```

**Add an existing widget as a page**:

```python
frame = ttk.Frame(stack, padding=10)
stack.add("custom", frame)
```

Pages are internally managed and hidden until navigated to.

---

### Navigation and history

Navigate to a page with:

```python
stack.navigate("details")
```

Move backward or forward through history:

```python
stack.back()
stack.forward()
```

Check navigation availability:

```python
stack.can_back()
stack.can_forward()
```

You can replace the current history entry (useful for redirects):

```python
stack.navigate("login", replace=True)
```

---

### Passing data between pages

You can pass a data dictionary when navigating:

```python
stack.navigate("confirm", data={"user": user_id})
```

This data is included in lifecycle event payloads so pages can react to it.

---

## Lifecycle events

`PageStack` emits a rich set of events during navigation:

- `<<PageUnmounted>>` — current page is being hidden
- `<<PageWillMount>>` — new page will be shown
- `<<PageMounted>>` — new page is now visible
- `<<PageChanged>>` — navigation completed

### Event payload

Navigation events include a data dictionary with:

- `page` — current page key
- `prev_page` — previous page key
- `prev_data` — data passed to the previous page
- `nav` — `"push"`, `"back"`, or `"forward"`
- `index` — current history index
- `length` — total history length
- `can_back` — whether back navigation is possible
- `can_forward` — whether forward navigation is possible

```python
def on_page_changed(event):
    data = event.data
    print(data["page"], data["nav"])

stack.on_page_changed(on_page_changed)
```

To remove the handler:

```python
funcid = stack.on_page_changed(on_page_changed)
stack.off_page_changed(funcid)
```

<!--
IMAGE: PageStack event lifecycle
Suggested: Timeline diagram showing unmount → will mount → mounted → changed
-->

---

## Common options & patterns

### Sticky and layout control

When adding pages, you can control how the page fills the stack:

```python
stack.add_page("full", sticky="nsew")
```

This is useful when pages need to stretch to fill available space.

---

### Removing pages

Remove a page entirely:

```python
stack.remove("details")
```

If the removed page is currently active, the stack becomes empty until you navigate elsewhere.

---

## UX guidance

- Use PageStack for **linear or stateful navigation**
- Provide clear Back/Next controls when history is involved
- Avoid mixing PageStack navigation with tabbed navigation (`Notebook`) in the same area

!!! tip "Think like a flow"
    PageStack works best when users think in terms of “steps” or “screens,” not categories.

---

## When to use / when not to

**Use PageStack when:**

- Navigation is sequential or flow-based
- You want browser-like back/forward behavior
- Only one view should be visible at a time

**Avoid PageStack when:**

- Users need random access to views (use `Notebook`)
- Multiple views should be visible simultaneously (use `PanedWindow`)
- Navigation is purely structural, not stateful

---

## Related widgets

- **Notebook** — tabbed navigation without history
- **Frame** — page container primitive
- **PanedWindow** — resizable multi-view layouts
