---
title: ScrolledText
---

# ScrolledText

`ScrolledText` is a multi-line text editor that wraps a `tkinter.Text`
widget inside a themed container, adds vertical and horizontal
scrollbars with configurable visibility, and normalizes mouse wheel
scrolling across platforms.

The widget delegates Text methods (`insert`, `get`, `delete`, `see`,
`tag_*`, `mark_*`, `search`, …) so you can drive it like a normal
`tkinter.Text`. There is no committed `value` model — content lives in
the text buffer and is addressed by Tk indices.

<figure markdown>
![scrolledtext states](../../assets/dark/widgets-scrolledtext-states.png#only-dark)
![scrolledtext states](../../assets/light/widgets-scrolledtext-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

st = ttk.ScrolledText(app, height=10)
st.pack(fill="both", expand=True, padx=20, pady=20)

st.insert("end", "Insert your text here.\n" * 20)

app.mainloop()
```

---

## Value model

`ScrolledText` is a thin wrapper around `tkinter.Text`. Unlike the form
field widgets (`TextEntry`, `NumericEntry`, …) it has **no `value`
property, no commit semantics, and no signal/variable** for the buffer
contents. Content is addressed and manipulated by Tk text indices:

| Concept | How to read or write it |
|---|---|
| Insert text | `st.insert("end", "hello")` |
| Read all text | `st.get("1.0", "end-1c")` |
| Replace a range | `st.replace("1.0", "end", new_text)` |
| Delete a range | `st.delete("1.0", "end")` |
| Scroll to an index | `st.see("end")` |

Indices are strings like `"1.0"` (line 1, column 0), `"end"`,
`"end-1c"` (one character before end, dropping the trailing newline Tk
adds), or `"insert"` (the cursor position). See the Tk
[Text documentation](https://www.tcl-lang.org/man/tcl/TkCmd/text.htm#M125)
for the full index grammar.

If you need a typed, validated, single-line value, use
[`TextEntry`](textentry.md) instead.

---

## Common options

| Option | Purpose |
|---|---|
| `scroll_direction` | `'vertical'` (default), `'horizontal'`, or `'both'`. |
| `scrollbar_visibility` | `'always'` (default), `'never'`, `'hover'`, or `'scroll'`. |
| `autohide_delay` | Milliseconds before scrollbars hide in `'scroll'` mode (default `1000`). |
| `scrollbar_style` | Accent token applied to the scrollbars (`'primary'`, `'success'`, `'danger'`, …). |
| `wrap` | `'word'` (default), `'char'`, or `'none'`. Forced to `'none'` when `scroll_direction` is `'horizontal'` or `'both'` and `wrap` is unset. |
| `height` / `width` | Buffer size in rows and columns (passed to the underlying `Text`). |
| `state` | `'normal'` or `'disabled'`. Passed through to the `Text` at construction; change at runtime via `st.text.configure(state=…)`. |
| `padding` | Padding around the container `Frame`. |

Any other keyword argument is forwarded to the underlying
`tkinter.Text` — `font`, `tabs`, `undo`, `spacing1`/`spacing2`/
`spacing3`, `selectbackground`, etc.

---

## Behavior

### Scrollbar visibility modes

- **`always`** — both relevant scrollbars stay visible.
- **`never`** — scrollbars are hidden but wheel scrolling still works.
- **`hover`** — scrollbars appear while the pointer is inside the
  widget and disappear on leave.
- **`scroll`** — scrollbars appear when the user scrolls and fade out
  after `autohide_delay` ms of inactivity.

```python
ttk.ScrolledText(app, scrollbar_visibility="hover")
ttk.ScrolledText(app, scrollbar_visibility="scroll", autohide_delay=1500)
```

### Horizontal scrolling

When `scroll_direction` is `'horizontal'` or `'both'`, `wrap` defaults
to `'none'` so long lines extend off-screen instead of wrapping.
Horizontal scrolling is driven by **Shift + Mouse Wheel**.

```python
code = ttk.ScrolledText(app, scroll_direction="both")  # wrap='none' implied
```

### Mouse wheel handling

`ScrolledText` installs platform-aware wheel bindings on a private
bind tag so wheel events scroll the text widget regardless of which
child has focus. Windows, macOS, and X11 deltas are normalized
internally.

### Accessing the underlying widgets

```python
st.text                   # the inner tkinter.Text
st.vertical_scrollbar     # ttkbootstrap.Scrollbar
st.horizontal_scrollbar   # ttkbootstrap.Scrollbar
```

Reach for `st.text` when you need to call methods that aren't
delegated — most notably `configure(...)` for runtime option changes
on the buffer (e.g. `st.text.configure(state="disabled")`).

### Text method delegation

At construction time, `ScrolledText` copies non-geometry methods from
`tkinter.Text` onto itself. You can call `insert`, `delete`,
`replace`, `get`, `see`, `index`, `compare`, `search`, `tag_add`,
`tag_configure`, `mark_set`, `edit_undo`, `edit_redo`,
`window_create`, `image_create`, and so on directly on the
`ScrolledText` instance. Pack, grid, and place methods are not
delegated — those manage the container.

---

## Events

`ScrolledText` does not add framework-level events. Use the standard
`tkinter.Text` virtual events on either the widget itself or
`st.text`:

| Event | Fires when… |
|---|---|
| `<<Modified>>` | The buffer's modified flag transitions. Reset with `st.edit_modified(False)`. |
| `<<Selection>>` | The selection changes. |
| `<KeyRelease>` | After every keystroke (live changes). |
| `<FocusIn>` / `<FocusOut>` | The text widget gains or loses focus. |

```python
def on_change(event):
    if st.edit_modified():
        print("buffer changed")
        st.edit_modified(False)

st.bind("<<Modified>>", on_change)
```

For commit-style semantics (fire only on blur or **Enter**), bind
`<FocusOut>` and `<Return>` and read `st.get("1.0", "end-1c")`.

---

## Validation and constraints

`ScrolledText` does not provide form-level validation, error messages,
or rule-based validation. Tk's `validate` / `validatecommand` only
applies to `Entry` and `Spinbox` widgets — not to `Text` — so
character-level filtering must be implemented manually:

```python
def cap_length(event):
    text = st.get("1.0", "end-1c")
    if len(text) > 500:
        st.delete("1.0 + 500c", "end-1c")

st.bind("<KeyRelease>", cap_length)
```

For form-ready, validated input use [`TextEntry`](textentry.md)
(single-line) or compose `ScrolledText` with your own commit handler.

---

## When should I use ScrolledText?

Use `ScrolledText` when:

- you need a multi-line, scrollable text buffer (logs, notes, simple
  editors, code views).
- you want consistent scrollbar visibility modes and cross-platform
  wheel behavior without wiring scrollbars yourself.
- you want full access to Tk's `Text` API — tags, marks, undo/redo,
  embedded images and widgets.

Prefer a different control when:

- you need a single-line, validated form field → use
  [`TextEntry`](textentry.md).
- you need to scroll arbitrary widgets (forms, panels, composites)
  rather than text → use [`ScrollView`](../layout/scrollview.md).
- you only need a bare `tk.Text` and will provide your own
  scrollbars → use [`Text`](../primitives/text.md).

---

## Related widgets

- [`TextEntry`](textentry.md) — single-line, form-ready text input
  with label, message, and validation.
- [`Text`](../primitives/text.md) — the unwrapped multi-line text
  primitive.
- [`Entry`](../primitives/entry.md) — single-line text primitive.
- [`ScrollView`](../layout/scrollview.md) — scroll container for
  arbitrary widgets.
- [`Scrollbar`](../layout/scrollbar.md) — scrollbar primitive used
  internally.

---

## Reference

- **API reference:** [`ttkbootstrap.ScrolledText`](../../reference/widgets/ScrolledText.md)
- **Related guides:**
    - [Forms](../../guides/forms.md)
