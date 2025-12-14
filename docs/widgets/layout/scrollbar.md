---
title: Scrollbar
icon: fontawesome/solid/grip-lines-vertical
---

# Scrollbar

`Scrollbar` is a themed wrapper around `ttk.Scrollbar` that integrates ttkbootstrap’s styling system. It’s a **primitive UI component** used to scroll other widgets (Text, Canvas, Listbox, TreeView, etc.) and is also used internally by higher-level widgets like `ScrollView` and `ScrolledText`.

<!--
IMAGE: Scrollbar variants
Suggested: Vertical and horizontal Scrollbar examples, plus a themed bootstyle variant
Theme variants: light / dark
-->

---

## Basic usage

Attach a scrollbar to a scrollable widget by wiring the widget’s `xview`/`yview` and the scrollbar’s `command` together.

### Vertical scrollbar

```python
import ttkbootstrap as ttk

app = ttk.Window()

text = ttk.Text(app, height=8, width=40)
text.grid(row=0, column=0, sticky="nsew")

vbar = ttk.Scrollbar(app, orient="vertical", command=text.yview)
vbar.grid(row=0, column=1, sticky="ns")

text.configure(yscrollcommand=vbar.set)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

app.mainloop()
```

### Horizontal scrollbar

```python
import ttkbootstrap as ttk

app = ttk.Window()

text = ttk.Text(app, wrap="none", height=8, width=40)
text.grid(row=0, column=0, sticky="nsew")

hbar = ttk.Scrollbar(app, orient="horizontal", command=text.xview)
hbar.grid(row=1, column=0, sticky="ew")

text.configure(xscrollcommand=hbar.set)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

app.mainloop()
```

<!--
IMAGE: Scrollbar wired to Text
Suggested: Text widget with visible vertical + horizontal scrollbars
-->

---

## What problem it solves

Many widgets expose `xview`/`yview` scrolling APIs but don’t include scrollbars automatically. `Scrollbar` solves this by:

- Providing a standard scrolling control for any compatible widget
- Supporting vertical and horizontal orientation
- Integrating ttkbootstrap `bootstyle` tokens for consistent theme styling

For most use cases, higher-level widgets (`ScrollView`, `ScrolledText`) handle scrollbars automatically. Use `Scrollbar` directly when you’re wiring scrolling manually or building custom composites.

---

## Core concepts

### The scroll contract: `command` and `*scrollcommand`

A scrollbar needs two-way wiring:

1. **Scrollbar → Widget**: scrollbar calls the widget’s view method (`xview`/`yview`) via `command`.
2. **Widget → Scrollbar**: widget reports its viewport using `xscrollcommand`/`yscrollcommand` calling the scrollbar’s `set`.

This is the standard Tk pattern:

```text
Scrollbar(command=widget.yview)
Widget(yscrollcommand=scrollbar.set)
```

---

### Orientation

Use `orient="vertical"` or `orient="horizontal"`:

```python
ttk.Scrollbar(app, orient="vertical")
ttk.Scrollbar(app, orient="horizontal")
```

---

## Common options & patterns

### Styling with bootstyle

Apply a semantic style token:

```python
ttk.Scrollbar(app, bootstyle="primary")
ttk.Scrollbar(app, bootstyle="secondary")
```

You can also use more specific style tokens depending on what your theme exposes (for example, square variants).

If you provide an explicit ttk style name via `style=...`, it overrides `bootstyle`.

<!--
IMAGE: Scrollbar bootstyle variants
Suggested: Several scrollbars using different bootstyles stacked together
-->

---

### Focus behavior

Scrollbars are usually not part of normal keyboard traversal. Keep `takefocus` disabled unless you have a specific accessibility requirement:

```python
ttk.Scrollbar(app, takefocus=False)
```

---

## Events

Scrollbars are typically driven through the scroll contract rather than event binding. When needed, you can bind low-level events like:

- `<ButtonPress-1>` / `<B1-Motion>` (dragging)
- `<Enter>` / `<Leave>` (hover styling, if desired)

Most applications don’t need these bindings directly.

---

## UX guidance

- Prefer `ScrollView` for scrolling arbitrary widgets (forms, panels)
- Prefer `ScrolledText` for scrolling text content
- Use a direct `Scrollbar` only when you need custom wiring (Canvas, Text, custom widgets)

!!! tip "Keep scrollbars subtle"
    Most modern UIs benefit from scrollbars that appear on hover or on scroll. Use `ScrollView` / `ScrolledText` if you want those behaviors without manual logic.

---

## When to use / when not to

**Use Scrollbar when:**

- You are wiring scrolling for `Text`, `Canvas`, `TreeView`, or a custom widget
- You need manual control over placement, layout, or styling
- You’re building a composite widget that manages its own scrolling

**Avoid Scrollbar when:**

- You want a “scrollable frame” (use `ScrollView`)
- You want a scrollable text area (use `ScrolledText`)
- You want auto-hide scrollbar behaviors (use higher-level widgets that implement it)

---

## Related widgets

- **ScrollView** — scroll container for arbitrary widgets
- **ScrolledText** — scrollable text widget
- **TreeView / TableView** — data views that often pair with scrollbars
