---
title: PageStack
---

# PageStack

`PageStack` is a **stacked view container** that manages multiple "pages" where only one page is visible at a time.

It provides **history-based navigation** (push, back, forward), similar to a web browser, making it ideal for wizards,
multi-step workflows, and task-based navigation inside a single window.

<!--
IMAGE: PageStack navigation flow
Suggested: Three pages with forward/back navigation arrows and a visible history stack
Theme variants: light / dark
-->

---

## Quick start

Create a PageStack, add pages, and navigate between them:

```python
import ttkbootstrap as ttk

app = ttk.App()

stack = ttk.PageStack(app, padding=10)
stack.pack(fill="both", expand=True)

page1 = stack.add("start", padding=10)
page2 = stack.add("details", padding=10)
page3 = stack.add("confirm", padding=10)

ttk.Label(page1, text="Start page").pack()
ttk.Button(page1, text="Next", command=lambda: stack.navigate("details")).pack()

ttk.Label(page2, text="Details page").pack()
ttk.Button(page2, text="Next", command=lambda: stack.navigate("confirm")).pack()
ttk.Button(page2, text="Back", command=stack.back).pack()

ttk.Label(page3, text="Confirm page").pack()
ttk.Button(page3, text="Back", command=stack.back).pack()

app.mainloop()
```

---

## When to use

Use `PageStack` when:

- navigation is sequential or flow-based

- back/forward behavior improves usability

- only one view should be visible at a time

Consider a different control when:

- users need random access to views - use [Notebook](notebook.md) instead

- the interaction model is "switch categories" - use [Notebook](notebook.md) instead

- multiple views must be visible simultaneously - use [PanedWindow](../layout/panedwindow.md) instead

---

## Appearance

### Styling

PageStack itself is a container without visual styling. Style the individual pages and navigation controls as needed.

!!! link "Design System"
    See [Colors & Themes](../../design-system/colors.md) for styling page content and navigation buttons.

---

## Examples and patterns

### Pages are keyed

Each page is identified by a unique string key:

```python
stack.add("settings")
stack.navigate("settings")
```

Keys are stable and preferable to index-based navigation.

### Adding pages

Use `add()` to get a page frame for placing widgets.

```python
page = stack.add("profile", padding=10)
```

Frame options (padding, color, etc.) can be passed directly:

```python
page = stack.add("settings", padding=10, accent="primary")
```

Or add an existing widget as a page:

```python
frame = ttk.Frame(stack, padding=10)
stack.add("custom", frame)
```

### Navigation and history

Navigate to a page (push):

```python
stack.navigate("details")
```

Move through history:

```python
stack.back()
stack.forward()
```

Check availability:

```python
stack.can_back()
stack.can_forward()
```

Redirect (replace current history entry):

```python
stack.navigate("login", replace=True)
```

### Passing data between pages

Pass a dict when navigating:

```python
stack.navigate("confirm", data={"user": user_id})
```

That data is included in lifecycle event payloads so pages can react to it.

### Full-bleed pages

When adding pages, control how they fill the stack:

```python
stack.add("full", sticky="nsew")
```

### Removing pages

Remove a page entirely:

```python
stack.remove("details")
```

If the removed page is active, the stack becomes empty until you navigate elsewhere.

### Events

`PageStack` emits a navigation lifecycle you can hook into:

- `<<PageUnmount>>` - current page is being hidden

- `<<PageWillMount>>` - new page will be shown

- `<<PageMount>>` - new page is now visible

- `<<PageChange>>` - navigation completed

```python
def on_page_changed(event):
    data = event.data
    print(data["page"], data["nav"])

funcid = stack.on_page_changed(on_page_changed)
# stack.off_page_changed(funcid)
```

### Event payload

Navigation events include:

- `page` - current page key

- `prev_page` - previous page key

- `prev_data` - data passed to the previous page

- `nav` - `"push"`, `"back"`, or `"forward"`

- `index` - current history index

- `length` - total history length

- `can_back` - whether back navigation is possible

- `can_forward` - whether forward navigation is possible

---

## Behavior

### UX guidance

- Use PageStack for **linear or stateful navigation**

- Provide clear Back/Next controls when history is involved

- Avoid mixing PageStack flow navigation with tabs (`Notebook`) in the same region

!!! tip "Think like a flow"
    PageStack works best when users think in terms of steps or screens, not categories.

---

## Additional resources

### Related widgets

- [Notebook](notebook.md) - tabbed views without history

- [Frame](../layout/frame.md) - typical page container

- [PanedWindow](../layout/panedwindow.md) - resizable multi-view layouts

### API reference

- [`ttkbootstrap.PageStack`](../../reference/widgets/PageStack.md)