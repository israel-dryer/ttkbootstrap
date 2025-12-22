---
title: Text
---

# Text

`Text` is Tkinter’s **multi-line text editor** widget (`tk.Text`).

It supports rich behavior that typical entry widgets don’t:

- multiple lines with wrapping and indentation
- **tags** for styling and interaction (links, highlights, code blocks)
- embedded **images** and **widgets**
- undo/redo, search, marks, and selections

ttkbootstrap exposes `Text` as a first-class widget so you can build editors, logs, and rich text UIs with a consistent theme and a clear set of usage patterns.

!!! tip "Prefer Field-based inputs when possible"
    For most form input, prefer **TextEntry**, **PasswordEntry**, **NumericEntry**, etc.  
    Use `Text` when you need **multi-line editing** or **tag-based formatting**.

---

## Basic usage

Create a text widget, insert content, and read it back:

```python
import ttkbootstrap as ttk

app = ttk.App()

text = ttk.Text(app, width=60, height=12, wrap="word")
text.pack(fill="both", expand=True, padx=20, pady=20)

text.insert("end", "Hello from Text\n")
text.insert("end", "This is a multi-line widget.")

print(text.get("1.0", "end-1c"))  # get all text, excluding trailing newline

app.mainloop()
```

---

## Key options

`Text` has a large option surface. These are the ones you’ll use most.

### Size and wrapping

- `width` — number of **characters** (int)
- `height` — number of **lines** (int)
- `wrap` — `"none"`, `"char"`, `"word"`

```python
ttk.Text(app, width=80, height=24, wrap="word")
```

!!! note "Width/height are character/line counts"
    Some type stubs allow “screen units” for `height`, but Tk’s Text widget is documented in terms of
    **characters (width)** and **lines (height)**. Prefer integers for portable behavior.

### Editing and undo

- `state` — `"normal"` or `"disabled"`
- `undo` — enable undo/redo
- `maxundo` — undo stack limit
- `autoseparators` — automatically insert undo separators

```python
text = ttk.Text(app, undo=True, maxundo=200, autoseparators=True)
```

### Padding and paragraph spacing

- `padx`, `pady` — internal padding
- `spacing1`, `spacing2`, `spacing3` — spacing above/between/below lines

```python
ttk.Text(app, padx=10, pady=8, spacing1=2, spacing2=2, spacing3=2)
```

### Theme-critical colors

These options matter most for light/dark theme consistency:

- `background`, `foreground`
- `insertbackground` (caret)
- `selectbackground`, `selectforeground`
- `inactiveselectbackground`

If ttkbootstrap applies defaults, you can usually rely on them. If you manually override, set the full set so the control stays readable in both themes.

---

## The Text index model

Many `Text` methods use **indices** instead of numeric positions.

Common indices:

- `"1.0"` — line 1, character 0 (start of content)
- `"end"` — end of content (includes the trailing newline)
- `"end-1c"` — end minus 1 character (commonly “real end”)
- `"insert"` — current cursor position
- `"sel.first"` / `"sel.last"` — selection range (when selection exists)

Examples:

```python
# insert at cursor
text.insert("insert", "typed here")

# delete current selection (if any)
if text.tag_ranges("sel"):
    text.delete("sel.first", "sel.last")

# ensure a specific index is visible
text.see("end")
```

---

## Common patterns

### Read-only text (log viewer)

`Text` doesn’t have a “readonly” state like ttk entries. Use `state="disabled"` and temporarily enable when updating:

```python
def append_line(s: str):
    text.configure(state="normal")
    text.insert("end", s + "\n")
    text.see("end")
    text.configure(state="disabled")
```

### Clear content

```python
text.delete("1.0", "end")
```

### Search and highlight

```python
def highlight(term: str):
    text.tag_remove("hit", "1.0", "end")
    if not term:
        return

    start = "1.0"
    while True:
        pos = text.search(term, start, stopindex="end", nocase=True)
        if not pos:
            break
        end = f"{pos}+{len(term)}c"
        text.tag_add("hit", pos, end)
        start = end

    text.tag_configure("hit", background="#fff3cd")  # example highlight
```

---

## Tags

Tags are the most powerful feature of `Text`. They let you style and interact with *ranges* of text.

### Style a range

```python
text.insert("end", "Normal\n")
start = text.index("end-1c linestart")
text.insert("end", "Bold line\n")

text.tag_add("bold", start, "end-1c")
text.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
```

### Link-like text

```python
def open_link(_):
    print("clicked")

text.insert("end", "Open settings")
start = "1.0"
end = "1.0 lineend"

text.tag_add("link", start, end)
text.tag_configure("link", underline=True)
text.tag_bind("link", "<Button-1>", open_link)
text.tag_bind("link", "<Enter>", lambda e: text.configure(cursor="hand2"))
text.tag_bind("link", "<Leave>", lambda e: text.configure(cursor="xterm"))
```

!!! tip "Tag names are your API"
    Use stable tag names like `"error"`, `"warning"`, `"link"`, `"code"` so your app can update styling globally.

---

## Scrolling

Text uses `yscrollcommand` / `yview` to connect a scrollbar.

```python
import ttkbootstrap as ttk

app = ttk.App()

frame = ttk.Frame(app)
frame.pack(fill="both", expand=True, padx=20, pady=20)

text = ttk.Text(frame, wrap="word")
text.pack(side="left", fill="both", expand=True)

sb = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
sb.pack(side="right", fill="y")

text.configure(yscrollcommand=sb.set)

app.mainloop()
```

---

## Events and change detection

A common “gotcha” is that `Text` does not emit a simple `<<Changed>>` event like your Field-based widgets.

Two common approaches:

- Bind key/mouse events (simple, but noisy)
- Use the modified flag (`edit_modified`) and `<<Modified>>` pattern (more controlled)

Example pattern:

```python
def on_modified(_):
    # Reset the modified flag so the event can fire again
    text.edit_modified(False)
    print("text changed")

text.bind("<<Modified>>", on_modified)
text.edit_modified(False)
```

---

## Performance tips

- Prefer **batch inserts** (insert a full chunk) over many tiny inserts.
- Use tags to style ranges rather than rebuilding the widget contents.
- For very large logs, consider truncating older content:

```python
MAX_CHARS = 200_000

def trim():
    # Tk < 3.13 returns a tuple from count()
    n = text.count("1.0", "end", "chars")
    chars = n[0] if isinstance(n, (tuple, list)) else int(n)
    if chars > MAX_CHARS:
        text.delete("1.0", "1.0+20000c")
```

---

## When should I use Text?

Use `Text` when:

- you need multi-line editing or display
- you need tags (highlighting, link-like behavior, syntax coloring)
- you need embedded images/widgets

Prefer **ScrolledText** when:

- you want the standard “Text + scrollbar” composite with less wiring

Prefer **TextEntry** (and other Field widgets) when:

- input is part of a form and you want label/message/validation and `on_input/on_changed`

---

## Related widgets

- **ScrolledText** — Text with built-in scrolling
- **TextEntry** — Field-based single-line input
- **Form** — spec-driven form builder (usually uses Field-based inputs)
- **Scrollbar / ScrollView** — scrolling primitives
- **Canvas** — drawing/virtualization primitive (often used for custom editors)

---

## Reference

- **API Reference:** `ttkbootstrap.Text` (Tkinter `tk.Text`)
