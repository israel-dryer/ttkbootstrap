---
title: ScrolledText
---

# ScrolledText

`ScrolledText` is a multi-line text widget with integrated scrollbars and consistent mouse wheel support.

It wraps a `tkinter.Text` widget inside a themed container and delegates Text methods so you can use it like a normal
Text widget—just with better scrolling behavior and consistent theming.

Use `ScrolledText` for logs, notes, editors, and any situation where **text content** needs to scroll.

<figure markdown>
![scrolledtext states](../../assets/dark/widgets-scrolledtext-states.png#only-dark)
![scrolledtext states](../../assets/light/widgets-scrolledtext-states.png#only-light)
</figure>

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

st = ttk.ScrolledText(app, height=10, scrollbar_visibility="scroll")
st.pack(fill="both", expand=True, padx=20, pady=20)

st.insert("end", "Insert your text here.\n" * 20)

app.mainloop()
```

---

## When to use

Use `ScrolledText` when:

- you need multi-line, scrollable text content (logs, notes, simple editors)
- you want integrated scrollbars and consistent wheel behavior

### Consider a different control when...

- you need a form-ready, validated single-line field (label/message/events) -> use [TextEntry](textentry.md)
- you need to scroll arbitrary widgets (forms, panels, composites) -> use [ScrollView](../layout/scrollview.md)

---

## Examples and patterns

### Value model

`ScrolledText` is a direct wrapper around `tkinter.Text`:

- content is addressed by Text indices (`"1.0"`, `"end-1c"`, etc.)
- there is no commit-time value model (it's free-form text)

```python
st.insert("end", "Hello")
text = st.get("1.0", "end-1c")
```

### Scroll direction: `scroll_direction`

- `"vertical"` (default)
- `"horizontal"`
- `"both"`

```python
st = ttk.ScrolledText(app, scroll_direction="both")  # wrap defaults to 'none'
```

### Wrapping: `wrap`

When horizontal scrolling is enabled, `wrap` typically should be `"none"`.

```python
code = ttk.ScrolledText(app, scroll_direction="both", wrap="none")
```

Horizontal scrolling uses **Shift + Mouse Wheel**.

### Scrollbar visibility: `scrollbar_visibility`

- `"always"`
- `"never"`
- `"hover"`
- `"scroll"` (auto-hide after `autohide_delay`)

```python
st = ttk.ScrolledText(app, scrollbar_visibility="hover")
st.configure(scrollbar_visibility="always")

st = ttk.ScrolledText(app, scrollbar_visibility="scroll", autohide_delay=1200)
```

### Access underlying Text: `text`

```python
text_widget = st.text
```

### Events

`ScrolledText` uses standard `tkinter.Text` events:

```python
st.bind("<KeyRelease>", lambda e: print("changed"))
st.bind("<FocusOut>", lambda e: print("focus out"))
```

### Validation and constraints

`ScrolledText` does not provide form-level validation or commit semantics.

If you need validation/messages, use field-based controls like **TextEntry** (single-line) or a dedicated editor component.

---

## Behavior

`ScrolledText` is designed specifically for text content (not arbitrary widgets).

- scrolling and mouse wheel behavior are handled internally for cross-platform consistency
- the container and scrollbars participate in ttkbootstrap theming via `color`

For scrolling arbitrary widgets, use **ScrollView** instead.

---

## Additional resources

### Related widgets

- [TextEntry](textentry.md) - single-line, form-ready text control
- [Entry](../primitives/entry.md) - low-level single-line text input
- [ScrollView](../layout/scrollview.md) - scroll container for arbitrary widgets
- [Scrollbar](../layout/scrollbar.md) - scrollbar primitive used internally

### API reference

- [`ttkbootstrap.ScrolledText`](../../reference/widgets/ScrolledText.md)