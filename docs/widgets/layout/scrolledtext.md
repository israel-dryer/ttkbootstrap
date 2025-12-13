---
title: ScrolledText
icon: fontawesome/solid/align-left
---


# ScrolledText

`ScrolledText` wraps a `tk.Text` widget with configurable scrollbars, mouse-wheel support, and themed scrollbar styling so you can drop a scrollable editor or log viewer into your layouts without wiring canvas boilerplate.

---

## Overview

Key behaviors:

- Scrollbars support four visibility modes (`always`, `never`, `on-hover`, `on-scroll`) plus an `autohide_delay` for the animated modes.
- `direction` chooses vertical, horizontal, or bidirectional scroll; horizontal mode also sets `wrap='none'` unless you override it.
- `scrollbar_style`/`bootstyle` control the thumb/track colors even though the control is canvas-free.
- Mouse-wheel events are propagated to the text widget through dedicated bind tags, keeping touchpad/mouse interactions reliable.
- The widget proxies every `Text` method, so you call `insert()`, `delete()`, `tag_add()`, etc., directly on the ScrolledText instance.

Use `ScrolledText` for notes, code editors, log displays, or any text-rich content that should scroll consistently with the rest of your theme.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

st = ttk.ScrolledText(
    app,
    height=10,
    show_scrollbar="on-scroll",
    scrollbar_style="secondary",
    padding=12,
)
st.pack(fill="both", expand=True, padx=16, pady=16)

for i in range(20):
    st.insert("end", f"Line {i+1}\n")

app.mainloop()
```

---

## Scrollbar & binding modes

- `show_scrollbar='on-scroll'` shows the bars only while dragging or using the wheel; `'on-hover'` reveals them on pointer enter; `'never'` hides them entirely but keeps scrolling working.
- The optional `autohide_delay` configures how long the scrollbars stay visible after activity in the animated modes.
- Horizontal scrolling is accessible via Shift+MouseWheel. Call `xview`/`yview` or `xview_moveto`/`yview_moveto` when you need to sync with other widgets.
- Call `refresh_bindings()` if you dynamically swap many child widgets inside the text frame to keep the wheel bindings current.

---

## When to use ScrolledText

Pick `ScrolledText` over a bare `Text` when you want scrollbars without manual canvas setup, and over `ScrollView` when you primarily need a text editor rather than a general container. If you need more control over scrollbar placement, compose `ScrollView`+`Text` directly.

---

## Related widgets

- **TextEntry** (single-line field)
- **ScrollView**

