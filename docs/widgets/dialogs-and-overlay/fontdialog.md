---
title: FontDialog
icon: fontawesome/solid/font
---

# FontDialog

`FontDialog` is a ready-to-use font selector dialog that lets users pick a **font family**, **size**, **weight**, **slant**, and optional effects (**underline**, **overstrike**) with a live preview. It returns the selected value as a `tkinter.font.Font` object, or `None` if the user cancels.

<!--
IMAGE: FontDialog overview
Suggested: FontDialog showing family list (left), size list (right), style options (bold/italic/effects), and preview text
Theme variants: light / dark
-->

---

## Basic usage

Show the dialog and apply the selected font:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import FontDialog

app = ttk.App()

dlg = FontDialog(master=app, title="Select Font")
dlg.show()

if dlg.result:
    ttk.Label(app, text="Sample Text", font=dlg.result).pack(padx=20, pady=20)

app.mainloop()
```

---

## What problem it solves

Font selection is a common “utility” workflow (editors, reports, printing, design tools), but wiring up a complete picker UI is repetitive. `FontDialog` provides:

- A complete font selection UI (family, size, weight, slant, effects)
- A live preview area so users can confirm the look before committing
- A simple `result` API (`tkinter.font.Font` or `None`)
- Built-in localization keys for the UI labels and preview text

---

## Core concepts

### Result value

After `.show()`, the selected font is available as:

```python
selected = dlg.result  # tkinter.font.Font | None
```

- `tkinter.font.Font` when the user presses **OK**
- `None` when the user presses **Cancel** (or closes the dialog)

---

### Live preview

The dialog maintains a preview font that updates as the user changes:

- family
- size
- weight (normal/bold)
- slant (roman/italic)
- underline / overstrike

The preview text updates immediately, so users can see changes without closing the dialog.

<!--
IMAGE: Live preview updates
Suggested: Two screenshots of the same dialog before/after toggling Bold + Italic
-->

---

### Localization keys

The dialog uses semantic keys for labels and preview text (e.g., `font.family`, `font.size`, `font.preview`). If you have localization enabled, these keys will be translated automatically.

!!! tip "Localize the title"
    The default `title` is a semantic key (for example `font.selector`). Pass a literal string if you don’t want localization.

---

## Common options & patterns

### Start from a specific default font

Use `default_font` to set the initial selection. It can be any Tk named font (or your custom font name).

```python
from ttkbootstrap.dialogs import FontDialog

dlg = FontDialog(master=app, default_font="TkTextFont")
dlg.show()
```

Common Tk named fonts include:

- `TkDefaultFont`
- `TkTextFont`
- `TkFixedFont`
- `TkHeadingFont`

---

### Use the dialog as a “popover-like” tool

`FontDialog` wraps the generic `Dialog` internally, so you can pass any standard dialog show options to `show(...)`.

Example: show it non-centered (screen-anchored by default):

```python
dlg = FontDialog(master=app)
dlg.show(anchor_to="screen")
```

<!--
IMAGE: FontDialog positioning
Suggested: FontDialog centered vs positioned near screen corner
-->

---

## Events

`FontDialog` exposes a simple imperative API:

- Call `show(...)` to display it.
- Read `result` afterward.

If you need richer dialog lifecycle events, use `Dialog` directly and build a custom font picker in `content_builder`.

---

## UX guidance

- Prefer `FontDialog` when users need both **choice** and **confirmation** (preview)
- Keep font selection as a secondary workflow (toolbar button, settings panel link)
- Apply fonts immediately after selection so users get feedback

!!! tip "Preview-first UX"
    A live preview reduces “trial and error” and helps users confidently choose fonts.

---

## When to use / when not to

**Use FontDialog when:**

- You need a complete font picker with preview
- Users must choose family + size + style (not just one attribute)
- You want a consistent, localized dialog UI

**Avoid FontDialog when:**

- You only need a size selector (use `Spinbox` / `SpinnerEntry`)
- You only need a family list (use `TreeView` or `Combobox`)
- Font choice is part of a larger form step (embed controls on a page or custom `Dialog`)

---

## Related widgets

- **Dialog** — generic dialog builder for custom workflows
- **DateDialog** — specialized picker dialog pattern
- **Combobox / Spinbox** — primitives often used in custom pickers
