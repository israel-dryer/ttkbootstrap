---
title: Text
---

# Text

`Text` is the multi-line text-editor primitive in ttkbootstrap. It is
not a custom subclass — `ttkbootstrap.Text` is `tkinter.Text`
re-exported from the top-level namespace. The integration ttkbootstrap
adds is an install-time wrapper around `tk.Text.__init__` that paints
theme colors (background, foreground, caret, selection, focus border)
on construction and re-applies them on `<<ThemeChanged>>`. Beyond that,
every option, method, and event behaves exactly like the underlying
`tk.Text` widget.

For the standard "text plus scrollbar" composite, prefer
[`ScrolledText`](../inputs/scrolledtext.md) — it wires the scrollbar
for you and handles visibility modes. For single-line input, prefer
[`TextEntry`](../inputs/textentry.md) (or one of the typed Field
inputs). Reach for `Text` directly when you need multi-line editing
with tag styling, embedded widgets/images, search, or undo/redo, and
want full access to the raw Tk option surface.

<figure markdown>
![text](../../assets/dark/widgets-text.png#only-dark)
![text](../../assets/light/widgets-text.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

text = ttk.Text(app, width=60, height=12, wrap="word")
text.pack(fill="both", expand=True, padx=20, pady=20)

text.insert("end", "Hello from Text\n")
text.insert("end", "This is a multi-line widget.")

print(text.get("1.0", "end-1c"))  # all text without trailing newline

app.mainloop()
```

---

## Content model

`Text` does not hold a single string. Its content is a sequence of
characters, addressed by **index strings**, with three orthogonal
overlays: **tags** (named ranges), **marks** (named indices that move
with edits), and **embedded objects** (widgets and images). There is
no `textvariable` and no reactive signal — observers either bind to
events or read the widget directly.

### Indices

A character position is a string of the form `"line.column"`,
1-indexed for lines and 0-indexed for columns:

| Index | Meaning |
|---|---|
| `"1.0"` | Start of content (line 1, column 0). |
| `"end"` | End of content (always one position past the last newline). |
| `"end-1c"` | Last real character — the form to use for "all text". |
| `"insert"` | Current caret position. |
| `"current"` | Position under the mouse. |
| `"sel.first"` / `"sel.last"` | Selection range, when a selection exists. |
| `"<line>.<col>"` | Explicit numeric position. |

Indices accept arithmetic and modifier suffixes:

| Form | Meaning |
|---|---|
| `"1.0 + 5c"` | Five characters past start. |
| `"end - 1l"` | One line before the end. |
| `"insert linestart"` | Start of the cursor's line. |
| `"insert lineend"` | End of the cursor's line. |
| `"insert wordstart"` / `"wordend"` | Word boundary at the cursor. |

### Tags

Tags are named ranges with style and event bindings. The same tag can
cover multiple disjoint ranges; styling and bindings apply to all of
them. Tags are the primary tool for syntax highlighting, link
behavior, error markers, and any visual or interactive overlay.

```python
# style a range
text.tag_add("warn", "2.0", "2.end")
text.tag_configure("warn", background="#fff3cd", foreground="#665")

# event-bind a range (link-like behavior)
text.tag_bind("warn", "<Button-1>", lambda e: print("clicked warn"))
```

Useful tag methods: `tag_add` / `tag_remove` / `tag_delete` /
`tag_configure` / `tag_bind` / `tag_ranges` / `tag_names` /
`tag_raise` / `tag_lower`. Stacking order matters when tags overlap —
the most recently raised tag wins for conflicting style options.

### Marks

A mark is a named index that moves with surrounding edits, so the
position you stored stays anchored to *content* even as text is
inserted or deleted before it. The widget keeps three special marks
internally — `"insert"` (caret), `"current"` (mouse), and
`"anchor"` (selection origin) — and you can add your own.

```python
text.mark_set("checkpoint", "insert")
text.insert("1.0", "prepended text\n")
print(text.index("checkpoint"))   # still points to the original spot
```

Marks have a `gravity` (`"left"` or `"right"`) controlling which side
text inserted *at* the mark goes on; `mark_gravity()` reads or sets
it.

### Embedded objects

Use `text.window_create(index, window=widget)` to embed a child
widget at an index, and `text.image_create(index, image=photo)` to
embed an image. Both behave like single characters for indexing and
selection. Embedded objects are useful for inline buttons, mini
forms, and richtext-style decorations.

---

## Common options

`tk.Text` exposes a large option surface; the most-used options are
below. The autostyle wrapper adds three additional construction
keywords on top — `surface`, `inherit_surface`, and `autostyle` — but
none of them produces a per-widget surface tint (see *Behavior*).

### Layout and editing

| Option | Type | Description |
|---|---|---|
| `width` | `int` | Width in **characters** of the configured font. |
| `height` | `int` | Height in **lines**. |
| `wrap` | `'none' \| 'char' \| 'word'` | Line-wrap mode. `'none'` enables horizontal scrolling. |
| `state` | `'normal' \| 'disabled'` | `'disabled'` blocks both user typing and programmatic `insert`/`delete` — see *Behavior*. |
| `padx` / `pady` | `int` | Internal padding on each side. The autostyle wrapper sets `padx=5, pady=5` by default. |
| `spacing1` / `spacing2` / `spacing3` | `int` | Pixel spacing above each paragraph / between wrapped lines / below each paragraph. |
| `cursor` | `str` | Mouse-cursor name (e.g. `"hand2"`). |
| `font` | `str \| Font` | Display font; defaults to `TkDefaultFont`. |

### Undo and editing model

| Option | Type | Description |
|---|---|---|
| `undo` | `bool` | Enable the undo/redo stack. Off by default. |
| `maxundo` | `int` | Cap on undo entries; `-1` for unlimited. |
| `autoseparators` | `bool` | Auto-insert undo separators between independent edits. |

When `undo=True`, the methods `edit_undo()` / `edit_redo()` /
`edit_separator()` / `edit_reset()` become useful. `edit_modified()`
reads or sets the modification flag — see [Events](#events).

### Theme-critical colors

| Option | Description |
|---|---|
| `background`, `foreground` | Page background and main text color. |
| `insertbackground` | Caret color. |
| `selectbackground`, `selectforeground` | Active selection. |
| `inactiveselectbackground` | Selection color when widget loses focus. |
| `highlightbackground`, `highlightcolor` | Border color when unfocused / focused. |
| `highlightthickness` | Border thickness; the autostyle builder sets this to `0` by default. |

The autostyle wrapper sets every entry in this group from the active
theme tokens at construction and on every `<<ThemeChanged>>`. If you
override one of them manually, the override sticks until the next
theme change, which then resets it. Pass `autostyle=False` if you
want a Text widget that the framework leaves alone — see *Behavior*.

### Autostyle keywords

The install-time wrapper around `tk.Text.__init__` accepts three
additional kwargs that are not real Tk options:

| Option | Type | Description |
|---|---|---|
| `autostyle` | `bool` | Default `True`. Pass `False` to skip the theme-color paint and the `<<ThemeChanged>>` registration entirely. |
| `inherit_surface` | `bool` | Default `True`. Captures the parent's `_surface` token onto the new widget, mirroring how container widgets cascade `surface`. |
| `surface` | `str` | Override the inherited surface token on this widget. |

!!! warning "`surface=` does not tint the Text widget"
    Both `surface=` and `inherit_surface=` write `_surface` on the
    widget, but the registered Text builder paints the widget with
    the theme's `background` token (the page-level background),
    ignoring the surface argument. So a `Text` inside a
    `Frame(surface="card")` paints with the page background, not
    the card background — by design, so input chrome is visually
    distinct from container chrome. To paint a custom background
    color, configure `background=` directly.

`accent`, `variant`, and `density` are **not** valid kwargs on
`Text` — passing any of them raises
`TclError: unknown option "-accent"` (or `-variant` / `-density`).

---

## Behavior

**`state="disabled"` blocks programmatic edits too, silently.** Unlike
ttk Entry — where `state="readonly"` blocks user typing but
`insert()`/`delete()` still work — Tk Text's `disabled` state rejects
both user input *and* programmatic mutation, with no exception. The
canonical read-only-with-occasional-update idiom is to flip back to
`"normal"` for the duration of the write:

```python
def append_line(s: str) -> None:
    text.configure(state="normal")
    text.insert("end", s + "\n")
    text.see("end")
    text.configure(state="disabled")
```

`<<Modified>>` does not fire while disabled because nothing changed —
the silent no-op extends to event emission as well.

**Default font is `TkDefaultFont`.** The autostyle wrapper sets
`option_add('*Text*Font', 'TkDefaultFont')` on the root window so
every Text widget picks up the framework's default text font. Pass
`font=...` to override per widget; the override survives theme
changes since the Text builder does not reconfigure `font`.

**Theme reapplication.** The widget is registered with the global
style on construction; on `<<ThemeChanged>>` the builder runs again
and resets every theme-driven option (background, foreground, caret,
selection colors, padx/pady, relief, highlightthickness). User
overrides on those options revert at the theme switch.

**Theme tokens vs. parent surface.** As noted under *Common options*,
the painted `background` always resolves to the theme's `background`
token, regardless of the parent's surface. The widget's `_surface`
attribute is set (so child layout queries can read it) but never
applied. If you need the Text to match a tinted container, set
`background=` explicitly with the matching theme color and accept
that it will reset across theme changes (or pass `autostyle=False`
and own the styling yourself).

---

## Events

`Text` does **not** emit any framework virtual events
(`<<Change>>`, `<<Input>>`, `<<Changed>>`) and exposes no `on_*`
helpers. There is no `textvariable` and no reactive `signal=`
channel. To observe edits, use one of the patterns below:

### `<<Modified>>` — Tk's edit flag

`tk.Text` maintains a one-shot **modification flag**. The widget
fires `<<Modified>>` exactly once when the flag transitions from
clear to set; subsequent edits do not fire the event again until the
flag is reset. The intended pattern is to reset the flag inside the
handler so each subsequent edit re-arms it:

```python
def on_modified(event):
    text.edit_modified(False)   # re-arm
    print("text changed")

text.bind("<<Modified>>", on_modified)
text.edit_modified(False)       # initial arm
```

This event covers programmatic and user edits, but does **not** fire
while `state="disabled"` (because edits are no-ops in that state).

### Direct key/mouse bindings

For keystroke-level reactivity (autocomplete, live previews,
character counters), bind the underlying input events:

```python
text.bind("<KeyRelease>", lambda e: count.set(text.count("1.0", "end", "chars")))
text.bind("<<Selection>>", lambda e: print(text.tag_ranges("sel")))
```

`<<Selection>>` fires when the selection changes (including on
deselection).

### Tag-bound events

`tag_bind(tag, sequence, callback)` attaches handlers that fire when
the matching event happens *inside* a tagged range. This is the
canonical way to implement clickable text:

```python
text.tag_configure("link", underline=True, foreground="#0d6efd")
text.tag_bind("link", "<Button-1>", lambda e: open_url())
text.tag_bind("link", "<Enter>",    lambda e: text.configure(cursor="hand2"))
text.tag_bind("link", "<Leave>",    lambda e: text.configure(cursor="xterm"))
```

---

## Patterns

### Read-only viewer

```python
text = ttk.Text(app, width=80, height=20, wrap="word")
text.pack(fill="both", expand=True)
text.insert("1.0", load_log())
text.configure(state="disabled")
```

Wrap any later append in a `state="normal"` / `state="disabled"`
flip — see *Behavior*.

### Search and highlight

```python
def highlight(term: str) -> None:
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
    text.tag_configure("hit", background="#fff3cd")
```

`text.search(...)` accepts `regexp=True`, `count=ttk.IntVar()` for
match length capture, and `forwards=False` for reverse search.

### Pair with a scrollbar

```python
container = ttk.Frame(app)
container.pack(fill="both", expand=True)

text = ttk.Text(container, wrap="word")
text.pack(side="left", fill="both", expand=True)

bar = ttk.Scrollbar(container, orient="vertical", command=text.yview)
bar.pack(side="right", fill="y")

text.configure(yscrollcommand=bar.set)
```

For the same effect with one widget, use
[`ScrolledText`](../inputs/scrolledtext.md).

### Trim long logs

```python
MAX_CHARS = 200_000

def trim() -> None:
    n = text.count("1.0", "end", "chars")
    chars = n[0] if isinstance(n, (tuple, list)) else int(n)
    if chars > MAX_CHARS:
        text.delete("1.0", f"1.0+{chars - MAX_CHARS}c")
```

Performance note: prefer batched inserts (one big chunk) over many
small inserts, and prefer tags for visual styling over rebuilding
the widget contents.

---

## When should I use Text?

Reach for `Text` when:

- you need **multi-line editing or display**, with wrapping,
  selection, undo, and the full Tk Text option surface;
- you need **tags** for styling, search highlighting, link behavior,
  syntax coloring, or error markers;
- you need to **embed widgets or images** inline with text;
- you are building a custom log viewer, code editor, or richtext
  surface and want raw access to indices, marks, and tag bindings.

For the standard "text plus scrollbar" composite, use
[`ScrolledText`](../inputs/scrolledtext.md). For form-style
single-line input, use [`TextEntry`](../inputs/textentry.md) (or a
typed Field input). For free-form drawing or virtualization, use
[`Canvas`](canvas.md).

## Related widgets

- [ScrolledText](../inputs/scrolledtext.md) — Text wired to a
  scrollbar with hover / always / never visibility modes.
- [TextEntry](../inputs/textentry.md) — single-line form input with
  label, helper text, validation messages, and `on_input` /
  `on_changed` events.
- [Entry](entry.md) — sibling primitive for raw single-line input.
- [Scrollbar](../layout/scrollbar.md) /
  [ScrollView](../layout/scrollview.md) — scrolling primitives.
- [Canvas](canvas.md) — drawing primitive for custom rendering.

## Reference

- The [Tk text manual](https://www.tcl.tk/man/tcl/TkCmd/text.htm) —
  authoritative for every option, method, and index syntax.
- Python's [`tkinter.Text`](https://docs.python.org/3/library/tkinter.html#tkinter.Text)
  bindings.
