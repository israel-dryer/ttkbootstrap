---
title: ScrolledText
icon: fontawesome/solid/file-lines
---

# ScrolledText

`ScrolledText` is a text widget with configurable scrollbars and full mouse wheel support. It wraps a standard `tkinter.Text` inside a themed container and delegates Text methods so you can use it like a normal `Text` widget—just with better scrolling behavior.

<!--
IMAGE: ScrolledText with content and scrollbars
Suggested: ScrolledText showing multi-line text, vertical scrollbar visible (on-scroll mode)
Theme variants: light / dark
-->

---

## Basic usage

Create a scrollable text area and insert content:

```python
import ttkbootstrap as ttk

app = ttk.Window()

st = ttk.ScrolledText(app, height=10, show_scrollbar="on-scroll")
st.pack(fill="both", expand=True, padx=20, pady=20)

st.insert("end", "Insert your text here.\n" * 20)

app.mainloop()
```

<!--
IMAGE: Basic ScrolledText example
Suggested: Multi-line text with scrollbar appearing while scrolling
-->

---

## What problem it solves

A plain `tkinter.Text` widget does not include scrollbars or consistent mouse wheel behavior by default. `ScrolledText` solves this by:

- Providing integrated vertical/horizontal scrollbars
- Supporting scrollbar visibility modes: `always`, `never`, `on-hover`, `on-scroll`
- Enabling mouse wheel scrolling regardless of platform (Windows/macOS/Linux)
- Delegating Text methods so it “feels” like a normal `Text` widget

---

## Core concepts

### This is for text, not arbitrary widgets

Use `ScrolledText` when your content is text (logs, notes, editors). For scrolling arbitrary widgets (forms, panels), use `ScrollView`.

---

### Direction and wrapping

`direction` controls which scrollbars are enabled:

- `"vertical"` (default)
- `"horizontal"`
- `"both"`

When horizontal scrolling is enabled (`horizontal` or `both`), `ScrolledText` defaults `wrap="none"` unless you explicitly set `wrap`.

```python
st = ttk.ScrolledText(app, direction="both")  # wrap defaults to 'none'
```

Horizontal scrolling uses **Shift+MouseWheel**.

<!--
IMAGE: Wrap vs no-wrap
Suggested: Two ScrolledText widgets: wrap='word' vs wrap='none' + horizontal scrolling
-->

---

### Scrollbar visibility modes

`show_scrollbar` controls when scrollbars appear:

- `"always"` — always visible
- `"never"` — hidden (scrolling still works)
- `"on-hover"` — visible while hovering the widget
- `"on-scroll"` — visible while scrolling, auto-hide after `autohide_delay`

```python
st = ttk.ScrolledText(app, show_scrollbar="on-hover")
st.configure(show_scrollbar="always")
```

`autohide_delay` is only used for `on-scroll` mode.

```python
st = ttk.ScrolledText(app, show_scrollbar="on-scroll", autohide_delay=1200)
```

<!--
IMAGE GROUP: Scrollbar modes
- Always
- On-hover
- On-scroll
-->

---

### Delegation: use it like a Text widget

`ScrolledText` delegates most `tkinter.Text` methods to the internal Text instance, so this works exactly as you expect:

```python
st.insert("end", "Hello")
st.delete("1.0", "end")
st.get("1.0", "end-1c")
st.configure(font=("Consolas", 10))
```

If you need direct access to the underlying Text widget:

```python
text_widget = st.text
```

---

## Common options & patterns

### Styling the scrollbars

Use `scrollbar_style` to apply a bootstyle to both scrollbars:

```python
st = ttk.ScrolledText(app, scrollbar_style="primary")
```

---

### Creating a read-only text area

To make a read-only viewer (log output, preview), disable editing:

```python
st = ttk.ScrolledText(app, height=10)
st.insert("end", "Read-only content...")
st.configure(state="disabled")
```

!!! tip "Editable vs readonly"
    Use `state="disabled"` for a read-only viewer. For “copyable but not editable” text, you can use `state="disabled"` and provide a Copy button or context menu.

---

### Backwards-compatible parameters

Legacy parameters like `autohide`, `vbar`, and `hbar` are supported but deprecated. Prefer `direction` and `show_scrollbar` for new code.

---

## Events

`ScrolledText` is a text widget, so you can bind typical Text events:

- `<KeyRelease>` for live typing
- `<Control-a>` for select all, etc.
- Custom key bindings for editors

Scrolling is handled internally using platform-appropriate wheel bindings.

---

## UX guidance

- Use `on-scroll` scrollbars for cleaner layouts (especially logs/notes panes)
- Prefer vertical scrolling for most text widgets
- Enable horizontal scrolling (`direction="both"`) for code or logs where line-wrapping is undesirable

!!! tip "Logs and code"
    For logs, set `wrap="none"` and enable horizontal scrolling so long lines remain intact.

---

## When to use / when not to

**Use ScrolledText when:**

- Your content is text (notes, logs, editor-like views)
- You want scrollbars without manual wiring
- You want consistent wheel behavior across platforms

**Avoid ScrolledText when:**

- You need to scroll arbitrary widgets (use `ScrollView`)
- You need virtualization for huge data (use a data view / grid)
- You need rich text rendering beyond Tk Text capabilities

---

## Related widgets

- **ScrollView** — scroll container for arbitrary widgets
- **Scrollbar** — scrollbar primitive used internally
- **TextEntry** — single-line, form-ready text control
