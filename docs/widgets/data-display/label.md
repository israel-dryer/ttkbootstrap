---
title: Label
---

# Label

`Label` displays **read-only text or images**.

It’s a fundamental building block used for headings, captions, instructions, and status text throughout an interface.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Hello world").pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

- `text`
- `image`
- `compound`
- `anchor`
- `justify`
- `wraplength`

---

## Styling

Labels participate fully in ttkbootstrap theming:

```python
ttk.Label(app, text="Info", bootstyle="info")
ttk.Label(app, text="Muted", bootstyle="secondary")
```

---

## When should I use Label?

Use Label when:

- displaying static text or images
- providing context or instructions

Prefer **Entry / TextEntry** when:

- user input is required

---

## Related widgets

- **Button**
- **Badge**
- **Tooltip**

---

## Reference

- **API Reference:** `ttkbootstrap.Label`
