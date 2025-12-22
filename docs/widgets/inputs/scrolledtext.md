---
title: ScrolledText
---

# ScrolledText

`ScrolledText` is a multi-line text widget with integrated scrollbars and consistent mouse wheel support.

It wraps a `tkinter.Text` widget inside a themed container and delegates Text methods so you can use it like a normal
Text widget—just with better scrolling behavior and consistent theming. fileciteturn14file5

Use `ScrolledText` for logs, notes, editors, and any situation where **text content** needs to scroll.

<figure markdown>
![scrolledtext states](../../assets/dark/widgets-scrolledtext-states.png#only-dark)
![scrolledtext states](../../assets/light/widgets-scrolledtext-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

st = ttk.ScrolledText(app, height=10, show_scrollbar="on-scroll")
st.pack(fill="both", expand=True, padx=20, pady=20)

st.insert("end", "Insert your text here.\n" * 20)

app.mainloop()
```

---

## Value model

`ScrolledText` is a direct wrapper around `tkinter.Text`:

- content is addressed by Text indices (`"1.0"`, `"end-1c"`, etc.)
- there is no commit-time value model (it’s free-form text)

```python
st.insert("end", "Hello")
text = st.get("1.0", "end-1c")
```

---

## Common options

### Scroll direction: `direction`

- `"vertical"` (default)
- `"horizontal"`
- `"both"`

```python
st = ttk.ScrolledText(app, direction="both")  # wrap defaults to 'none'
```

### Wrapping: `wrap`

When horizontal scrolling is enabled, `wrap` typically should be `"none"`.

```python
code = ttk.ScrolledText(app, direction="both", wrap="none")
```

Horizontal scrolling uses **Shift + Mouse Wheel**.

### Scrollbar visibility: `show_scrollbar`

- `"always"`
- `"never"`
- `"on-hover"`
- `"on-scroll"` (auto-hide after `autohide_delay`)

```python
st = ttk.ScrolledText(app, show_scrollbar="on-hover")
st.configure(show_scrollbar="always")

st = ttk.ScrolledText(app, show_scrollbar="on-scroll", autohide_delay=1200)
```

### Access underlying Text: `text`

```python
text_widget = st.text
```

---

## Behavior

`ScrolledText` is designed specifically for text content (not arbitrary widgets).

- scrolling and mouse wheel behavior are handled internally for cross-platform consistency
- the container and scrollbars participate in ttkbootstrap theming via `bootstyle`

For scrolling arbitrary widgets, use **ScrollView** instead.

---

## Events

`ScrolledText` uses standard `tkinter.Text` events:

```python
st.bind("<KeyRelease>", lambda e: print("changed"))
st.bind("<FocusOut>", lambda e: print("focus out"))
```

---

## Validation and constraints

`ScrolledText` does not provide form-level validation or commit semantics.

If you need validation/messages, use field-based controls like **TextEntry** (single-line) or a dedicated editor component.

---

## When should I use ScrolledText?

Use `ScrolledText` when:

- you need multi-line, scrollable text content (logs, notes, simple editors)
- you want integrated scrollbars and consistent wheel behavior

Prefer **TextEntry** when:

- you need a form-ready, validated single-line field (label/message/events)

Prefer **ScrollView** when:

- you need to scroll arbitrary widgets (forms, panels, composites)

---

## Related widgets

- **TextEntry** — single-line, form-ready text control
- **Entry** — low-level single-line text input
- **ScrollView** — scroll container for arbitrary widgets
- **Scrollbar** — scrollbar primitive used internally

---

## Reference

- **API Reference:** `ttkbootstrap.ScrolledText`
