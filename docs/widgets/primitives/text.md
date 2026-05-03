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
| `"1.0 + 5 chars"` | Same — full word form is accepted. |
| `"end - 1l"` | One line before the end. |
| `"end - 2 lines"` | Same with the long form. |
| `"insert linestart"` | Start of the cursor's line. |
| `"insert lineend"` | End of the cursor's line. |
| `"insert wordstart"` / `"wordend"` | Word boundary at the cursor. |
| `"insert + 5 display chars"` | Five *visible* characters past — counts elided / hidden text differently from raw chars. |
| `"insert + 1 display lines"` | One wrapped line down (raw `"+1l"` walks logical lines, ignoring wrap). |
| `"@x,y"` | The character under screen pixel `(x, y)` relative to the widget. |

Multiple modifiers chain left-to-right:

```python
text.index("insert wordstart - 1c")          # one before the word's first char
text.index("end - 1c linestart")             # start of the last text line
```

`text.index(spec)` returns the canonical `"line.column"` form for any
of these; use it to normalize before comparing with `==`. For
counting, `text.count(start, end, *units)` returns the number of
units between two indices — `"chars"`, `"displaychars"`, `"lines"`,
`"displaylines"`, `"indices"`, `"displayindices"`, and `"xpixels"` /
`"ypixels"` are all valid units.

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
`tag_raise` / `tag_lower` / `tag_nextrange` / `tag_prevrange`.
Stacking order matters when tags overlap — the most recently raised
tag wins for conflicting style options.

The special tag `"sel"` represents the current selection. Reading
`text.tag_ranges("sel")` returns the selection's `(start, end)`
indices (or `()` when nothing is selected); writing
`text.tag_add("sel", a, b)` extends the selection programmatically;
`text.tag_remove("sel", "1.0", "end")` clears it.

#### Tag styling options

`tag_configure(tag, **options)` accepts the option matrix below. Any
option can be reset by passing the empty string (`""`).

| Option | Effect |
|---|---|
| `font` | Tk font spec or named font. Override the widget-level font for the range. |
| `foreground` / `background` | Per-range text and cell colors. |
| `selectforeground` / `selectbackground` | Override the widget's selection colors when this range is selected. |
| `underline` / `overstrike` | Booleans — add a line under or through the text. |
| `underlinefg` / `overstrikefg` | Color the line independently of `foreground`. |
| `relief` / `borderwidth` | Draw a beveled border around the range (`flat`, `raised`, `sunken`, `ridge`, `groove`, `solid`). |
| `justify` | `left` / `center` / `right` — paragraph alignment. |
| `lmargin1` / `lmargin2` / `rmargin` | Pixel margins — first-line indent, hanging indent, right margin. |
| `lmargincolor` / `rmargincolor` | Margin background colors. |
| `spacing1` / `spacing2` / `spacing3` | Pixels above each paragraph / between wrapped lines / below each paragraph. |
| `wrap` | Per-range wrap mode — overrides the widget's `wrap`. |
| `tabs` / `tabstyle` | Tab stops in screen units; `tabular` / `wordprocessor` style. |
| `elide` | Boolean — hide the range from rendering and from cursor traversal. |
| `bgstipple` / `fgstipple` | Bitmap stipple patterns for shaded rendering. |
| `offset` | Vertical pixel offset (positive = baseline down) — useful for sub/superscript. |

```python
text.tag_configure(
    "code",
    font=("monospace", 10),
    background="#1e1e1e",
    foreground="#d4d4d4",
    relief="flat",
    lmargin1=24,
    lmargin2=24,
    rmargin=24,
    spacing1=4,
    spacing3=4,
)
```

#### Tag range queries

`tag_nextrange(tag, start, stopindex='end')` returns the next
`(start, end)` tuple where `tag` applies, walking forward from
`start`. Useful for iterating every occurrence of a tag without
materializing the full `tag_ranges` tuple:

```python
pos = "1.0"
while True:
    rng = text.tag_nextrange("hit", pos)
    if not rng:
        break
    do_something_with(*rng)
    pos = rng[1]
```

`tag_prevrange` walks backward. Both return `()` when no further
range exists.

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
it. The default for user-created marks is `"right"` — newly inserted
text shifts the mark to its right edge, so the mark stays anchored
to the position after the insertion.

| Method | Use |
|---|---|
| `mark_set(name, index)` | Create a mark or move an existing one. |
| `mark_unset(*names)` | Delete marks. The internal `insert` / `current` / `anchor` marks cannot be unset. |
| `mark_gravity(name, direction=None)` | Read (no `direction`) or write the mark's gravity. |
| `mark_names()` | Tuple of all mark names. |
| `mark_next(index)` / `mark_previous(index)` | Walk marks in document order. |

Names with a leading `tk::` prefix are conventional for internal /
private marks — use a project-specific prefix on your own marks to
keep the namespace tidy.

### Embedded objects

Use `text.window_create(index, window=widget)` to embed a child
widget at an index, and `text.image_create(index, image=photo)` to
embed an image. Both behave like single characters for indexing and
selection. Embedded objects are useful for inline buttons, mini
forms, and richtext-style decorations.

`window_create` accepts `align=` (`baseline` / `top` / `center` /
`bottom`), `padx=` / `pady=` (pixel padding around the widget), and
`stretch=` (boolean — when true, the widget's height is stretched to
match the line height). Pass `create=callable` to defer instantiation
until the embed is first scrolled into view — the callable returns
the widget when invoked. The embedded widget must be parented to the
Text or one of its ancestors.

`image_create` accepts `align=`, `padx=` / `pady=`, and `name=`
(string — when provided, becomes the embed's identifier so you can
reconfigure it later via `image_configure(name, …)` or remove it via
`delete(name)`). The image reference must be retained by Python —
stash it on a long-lived object (e.g. `text.image_ref = img`) so the
GC doesn't reclaim it.

```python
button = ttk.Button(text, text="Run", accent="primary")
text.window_create("end", window=button, padx=4, pady=4)

img = ImageTk.PhotoImage(Image.open("icon.png"))
text.image_ref = img
text.image_create("end", image=img, padx=4)
```

To find every embedded object: `text.dump("1.0", "end",
window=True)` returns a list of `(kind, value, index)` triples for
the kinds you ask for (`window`, `image`, `mark`, `tag`, `text`).

### Selection

The selection is the special `"sel"` tag. Read it as a tag range, mutate
it as a tag, observe changes via the `<<Selection>>` virtual event:

```python
rng = text.tag_ranges("sel")            # () or (start_idx, end_idx)
text.tag_add("sel", "1.0", "1.end")     # select the first line
text.tag_remove("sel", "1.0", "end")    # clear the selection
text.see("sel.first")                   # scroll to selection start
```

The cursor (caret) is the `"insert"` mark — moving it does not change
the selection unless `<Shift>` is held during the keypress. To move
both at once:

```python
text.mark_set("insert", "1.0")
text.tag_remove("sel", "1.0", "end")
```

`text.see(index)` scrolls the view as little as needed to make
`index` visible. Pair with `mark_set("insert", …)` to implement
"jump to line" affordances.

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

The undo / edit method surface (only meaningful when `undo=True`):

| Method | Use |
|---|---|
| `edit_undo()` | Undo the most recent edit set; raises `TclError` if nothing to undo. |
| `edit_redo()` | Redo the most recently undone edit set; raises if nothing to redo. |
| `edit_separator()` | Force a separator into the undo stack — the next `edit_undo()` stops here. |
| `edit_reset()` | Discard all undo / redo history. |
| `edit_modified(flag=None)` | Read or set the modification flag — see [Events](#events). |
| `edit("undo")` / `edit("redo")` | Same as the helpers; raw access for arg-form variations. |

With `autoseparators=True` (the default when `undo=True`), Tk inserts
separators heuristically — typically when the input source changes
(typing → paste → typing creates two separators). For finer control,
set `autoseparators=False` and place separators manually around
logical edit boundaries (e.g. after every line break, after every
paste).

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
| `autostyle` | `bool` | Default `True`. Pass `False` to skip the theme-color paint and the `<<ThemeChanged>>` registration entirely. The `_surface` attribute is still captured. |
| `inherit_surface` | `bool` | Default from `AppSettings.inherit_surface_color`. When true, the new widget's `_surface` is taken from the parent — the explicit `surface=` argument is overridden. |
| `surface` | `str` | Surface token to record on the widget. Honored only when `inherit_surface=False` (or when there is no parent surface to inherit). |

`inherit_surface=True` (the default) is the opt-in behavior for legacy
Tk widgets: the widget blends with its container rather than forcing a
specific surface. If you want to pin a surface regardless of the parent,
pass `inherit_surface=False` alongside your explicit `surface=`:

```python
ttk.Text(parent, surface='card', inherit_surface=False)
```

!!! warning "`_surface` does not tint the Text widget"
    Even when `_surface` is set on the widget (via inheritance or
    explicit `surface=`), the registered Text builder paints the
    widget with the theme's `background` token — the page-level
    background — and ignores `_surface` entirely. So a `Text`
    inside a `Frame(surface="card")` paints with the page
    background, not the card background; this is by design so that
    input chrome stays visually distinct from container chrome. To
    paint a custom background color, configure `background=`
    directly (and accept that the next `<<ThemeChanged>>` will
    revert it — see *Behavior*).

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

**Default font is `TkDefaultFont`.** The root-window `Tk` builder
calls `option_add('*Text*Font', 'TkDefaultFont')` once at app
construction, so every Text widget picks up the framework's default
text font instead of Tk's stock `TkFixedFont`. The per-Text builder
does not touch `font`. Pass `font=...` to override per widget; the
override survives theme changes.

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

Tag bindings sit *behind* widget-level bindings — a class-level
`<Button-1>` (the default, which moves the cursor) still fires when
you bind one to a tag. Return `"break"` from the tag handler to
suppress the class binding for that event.

---

## Search

`text.search(pattern, start, stopindex=None, **options)` returns the
first index where `pattern` matches, walking forward from `start`
(or backward when `forwards=False`). Returns `""` on no match.

| Option | Default | Effect |
|---|---|---|
| `forwards` | `True` | Walk forward (`True`) or backward (`False`) from `start`. |
| `backwards` | inverse | Convenience inverse of `forwards`. |
| `exact` | `True` | Match the pattern literally. |
| `regexp` | `False` | Treat `pattern` as a Tcl regex. |
| `nocase` | `False` | Case-insensitive matching. |
| `elide` | `False` | Match through ranges tagged with `elide=True`. |
| `count` | `None` | Pass an `IntVar` / `StringVar` to receive the matched length (in chars), useful for variable-length regex matches. |
| `stopindex` | `None` (whole doc) | Stop searching at this index. |

```python
counter = ttk.IntVar(value=0)
pos = text.search(r"^\s*def\s+\w+",
                  "1.0", stopindex="end",
                  regexp=True, count=counter)
if pos:
    end = f"{pos}+{counter.get()}c"
    text.tag_add("def", pos, end)
```

For "find every match" loops, advance `start` past the previous
match to avoid infinite recursion on zero-width regex matches:

```python
def find_all(pattern, *, regexp=False) -> list[tuple[str, str]]:
    hits = []
    start = "1.0"
    counter = ttk.IntVar()
    while True:
        pos = text.search(pattern, start, stopindex="end",
                          regexp=regexp, count=counter)
        if not pos:
            return hits
        length = counter.get() if regexp else len(pattern)
        if length == 0:
            start = f"{pos}+1c"
            continue
        end = f"{pos}+{length}c"
        hits.append((pos, end))
        start = end
```

---

## Scrolling

Text wires to scrollbars via the `xscrollcommand` / `yscrollcommand`
options on the widget and `xview` / `yview` methods on the bound
scrollbar.

| Method / Option | Purpose |
|---|---|
| `xview` / `yview` | Read the current view as `(first, last)` fractions, or scroll via arg forms. |
| `xview_moveto(fraction)` / `yview_moveto(fraction)` | Scroll so the given fraction is the leftmost / topmost visible position. |
| `xview_scroll(n, what)` / `yview_scroll(n, what)` | Scroll `n` units (`"units"` or `"pages"`). |
| `see(index)` | Scroll just enough to make `index` visible. The cheapest "jump to" primitive. |
| `scan_mark(x, y)` / `scan_dragto(x, y, gain=10)` | Implement middle-click drag-scrolling — `mark` records the start, `dragto` moves the view by the delta scaled by `gain`. |

The scrollbar pairing is symmetric:

```python
sb = ttk.Scrollbar(parent, orient="vertical", command=text.yview)
text.configure(yscrollcommand=sb.set)
```

Without `yscrollcommand=sb.set`, scrolling the Text by other means
(arrow keys, `see()`, programmatic changes) won't update the
scrollbar's thumb position.

For a "text plus scrollbar" composite that handles this wiring (and
adds hover / always / never visibility modes),
[`ScrolledText`](../inputs/scrolledtext.md) is the prebuilt option.

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

### Line-numbers gutter

A second Text widget alongside the main one acts as a gutter. Wire
both yviews together so they scroll in lockstep:

```python
container = ttk.Frame(app)
container.pack(fill="both", expand=True)

gutter = ttk.Text(container, width=4, padx=4,
                  state="disabled", takefocus=False)
gutter.pack(side="left", fill="y")

text = ttk.Text(container, wrap="word")
text.pack(side="left", fill="both", expand=True)

def refresh_gutter(_=None):
    gutter.configure(state="normal")
    gutter.delete("1.0", "end")
    line_count = int(text.index("end-1c").split(".")[0])
    gutter.insert("1.0", "\n".join(str(n) for n in range(1, line_count + 1)))
    gutter.configure(state="disabled")
    gutter.yview_moveto(text.yview()[0])

def sync_yview(*args):
    gutter.yview_moveto(text.yview()[0])

text.bind("<<Modified>>",
          lambda e: (refresh_gutter(), text.edit_modified(False)))
text.bind("<Configure>", sync_yview)
text.bind("<MouseWheel>", lambda e: text.after_idle(sync_yview))
text.edit_modified(False)
refresh_gutter()
```

For tighter sync (every keystroke, every paste), bind `<KeyRelease>`
in addition to `<<Modified>>`.

### Syntax highlighting

Define a tag per token kind, then walk the buffer with a regex pass
on every `<<Modified>>`. For small documents this is fast enough; for
large ones, scope the rescan to the changed paragraph(s):

```python
text.tag_configure("kw", foreground="#0d6efd")
text.tag_configure("str", foreground="#198754")
text.tag_configure("comment", foreground="#6c757d", font=("italic", 10))

PATTERNS = [
    (r"\#[^\n]*",                           "comment"),
    (r"\".*?\"|'.*?'",                       "str"),
    (r"\b(def|class|return|if|else|for)\b", "kw"),
]

def rehighlight():
    for _, tag in PATTERNS:
        text.tag_remove(tag, "1.0", "end")
    counter = ttk.IntVar()
    for pattern, tag in PATTERNS:
        start = "1.0"
        while True:
            pos = text.search(pattern, start, stopindex="end",
                              regexp=True, count=counter)
            if not pos:
                break
            end = f"{pos}+{counter.get()}c"
            text.tag_add(tag, pos, end)
            start = end

text.bind("<<Modified>>",
          lambda e: (rehighlight(), text.edit_modified(False)))
text.edit_modified(False)
```

For incremental highlighting, replace the global `1.0`/`end` range
with the bounds of the changed lines (track via the `<<Modified>>`
handler plus comparing `text.index("insert linestart")` /
`"insert lineend"` from before and after the edit).

### Find and replace

Walk every match with `search`, mutate inside a single `text.edit_separator()`
boundary so the whole batch undoes as one operation:

```python
def replace_all(needle: str, repl: str) -> int:
    count = 0
    text.edit_separator()
    start = "1.0"
    while True:
        pos = text.search(needle, start, stopindex="end")
        if not pos:
            break
        end = f"{pos}+{len(needle)}c"
        text.delete(pos, end)
        text.insert(pos, repl)
        start = f"{pos}+{len(repl)}c"
        count += 1
    text.edit_separator()
    return count
```

### Embed an inline widget

```python
text.insert("end", "Run task: ")
btn = ttk.Button(text, text="Go", accent="primary",
                 command=lambda: print("clicked"))
text.window_create("end", window=btn, padx=4, pady=2)
text.insert("end", "\n")
```

The embedded button moves with surrounding text edits, participates
in selection (highlighted as a "character" if the selection covers
its position), and can be removed via `text.delete(index)` on the
embed's character position.

### Save and restore selection

```python
def save_selection() -> tuple[str, str] | None:
    rng = text.tag_ranges("sel")
    return (str(rng[0]), str(rng[1])) if rng else None

def restore_selection(saved):
    text.tag_remove("sel", "1.0", "end")
    if saved:
        text.tag_add("sel", *saved)
```

Useful around bulk operations (find/replace, tag rebuilds) that
clear or move the selection mid-run.

---

## Performance

Most apps don't need to think about Text performance — Tk's storage
is a balanced B-tree of lines, and the common operations are sub-
linear. The notes below cover the cases where you can hit a wall.

- **Batch inserts.** A single `insert("end", big_string)` is far
  faster than ten thousand `insert("end", line + "\n")` calls.
  When streaming data in (a log tail, a network feed), accumulate
  in a Python `list` and flush every few hundred ms.
- **Wrap mutation in a single redraw window.** Tk redraws at idle,
  so a sequence of `insert` / `delete` / `tag_add` calls in one
  handler costs roughly the same as a single call. *Don't* call
  `update()` in the middle — it forces a redraw and tanks throughput.
- **Tag-once, configure many.** `tag_configure(name, …)` re-styles
  every range that already has the tag — much cheaper than removing
  and reapplying the tag. For animated highlights, mutate the tag's
  options rather than repainting per-character.
- **Tag stacking matters.** When two tags both set `background`,
  the most recently *raised* one wins (`tag_raise(later, earlier)`).
  Keep the high-priority tags at the top of the stacking order
  rather than constantly removing and re-adding lower ones.
- **`<<Modified>>` is once per transition.** Don't put expensive
  rescans in the handler without re-arming via
  `text.edit_modified(False)`. The flag stays set after the first
  call, so subsequent edits don't fire — the handler runs forever
  and silently misses every later edit.
- **Cap the buffer for log views.** A 10MB Text widget paints
  fine, but `count("1.0", "end", "chars")` becomes O(buffer)
  and visible at 100MB. The "trim long logs" pattern above keeps
  long-running viewers responsive.
- **Use `see` over `yview_moveto` for "follow tail" UIs.**
  `see("end")` is one call and a bounded scroll; `yview_moveto`
  with a computed fraction needs an `update_idletasks` to reflect
  the new bottom.
- **Use `dump` for inspection, not for normal reads.** `dump` is
  designed for serialization tools and is much heavier than
  `get` / `index` / `tag_ranges` for everyday queries.

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
