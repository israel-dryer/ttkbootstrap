---
title: Card
---

# Card

`Card` is a **bordered, elevated container** for grouping related content.

It is a convenience wrapper around `Frame` with `surface='card'` and `show_border=True` by default.

<figure markdown>
![card](../../assets/dark/widgets-card.png#only-dark)
![card](../../assets/light/widgets-card.png#only-light)
</figure>

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

card = ttk.Card(app, padding=20)
card.pack(padx=20, pady=20, fill="x")

ttk.Label(card, text="Card Title", font="heading-md").pack(anchor="w")
ttk.Label(card, text="Card content goes here.").pack(anchor="w", pady=(4, 0))

app.mainloop()
```

---

## When to use

Use `Card` when:

- you want to visually group related content with a border

- you need an elevated container that stands out from the background

Consider a different control when:

- you need a collapsible container - use [Expander](expander.md)

- you need a titled border - use [LabelFrame](labelframe.md)

---

## Examples and patterns

### Basic card

```python
card = ttk.Card(app, padding=20)
card.pack(fill="x", padx=10, pady=10)
ttk.Label(card, text="Hello from a Card!").pack()
```

### Custom padding

```python
card = ttk.Card(app, padding=(16, 24))
```

### Side-by-side cards

```python
row = ttk.Frame(app)
row.pack(fill="x", padx=10)

card1 = ttk.Card(row, padding=16)
card1.pack(side="left", fill="both", expand=True, padx=(0, 5))

card2 = ttk.Card(row, padding=16)
card2.pack(side="left", fill="both", expand=True, padx=(5, 0))
```

---

## Additional resources

### Related widgets

- [Frame](frame.md) - base container without card styling

- [LabelFrame](labelframe.md) - container with a titled border

- [Expander](expander.md) - collapsible container

### API reference

- [`ttkbootstrap.Card`](../../reference/widgets/Card.md)
