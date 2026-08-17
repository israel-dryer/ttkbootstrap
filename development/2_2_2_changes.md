# ttkbootstrap 2.2.2 — notable changes

> The consolidated log of changes that alter behavior or appearance since
> **2.2.1**, each with **what** changed and **why**. Same role its predecessors
> (`2_2_1_changes.md`, `2_2_changes.md`, `2_0_breaking_changes.md`) played: kept
> in `development/` so it survives, and the source for this release's notes.
>
> Scope is **relative to 2.2.1**. A regression introduced *and* fixed inside this
> cycle never reached a user, so it belongs to the dev log in `CLAUDE.md`, not
> here.
>
> Legend: **API** = source-level break · **Visual** = appearance-only (no code
> change needed) · **New** = additive · **Fix** = something that did not work
> before now does.

## Index

Rows mirror the section headings below, in order.

| Area | Kind |
|---|---|
| **Message dialogs accept an icon glyph name** | Fix |

There are **no API breaks**: nothing was removed, and no call that worked in
2.2.1 fails.

---

## Message dialogs accept an icon glyph name  *(Fix)*

**What.** `MessageDialog(icon=...)` and the `Messagebox` methods now accept a
Bootstrap Icons glyph name, which is what the reference pages have always
documented the option to be:

```python
Messagebox.okcancel("Ok or Cancel?", "Choose", icon="question-circle-fill")
```

Previously that warned — *"could not be loaded as an image name, base64 data, or
file path"* — and the dialog opened with no icon at all. The four forms that
already worked (a rendered `ttk.Icon(...)`, a `PhotoImage`, base64 image data, a
file path) are unchanged, and an unusable value still warns and drops the icon
rather than failing to open the dialog.

**Who notices.** Anyone who passed `icon=` to a message dialog and got nothing.
The `show_info` / `show_warning` / `show_error` / `show_question` defaults were
never affected — those render their own glyph internally and only reached the
broken path when a caller overrode `icon=`.

**Why.** The option accepted a `str`, so it type-checked, and `ttk.Icon(...)`
*returns* a `str` — an opaque Tk image name like `"pyimage24"`. Four different
meanings shared one annotation, and the one form the parameter name advertises
was the one that failed. Every other `icon=` in the library already takes a glyph
name (`ttk.Button(icon="gear-fill")`, `ToastNotification(icon="bell-fill")`), so
the dialogs were the sole exception.

A bare glyph name renders at the same size as the built-in alert glyphs, in the
theme foreground — a caller's glyph carries no semantics to map to a color, and
guessing one would be wrong as often as right. `ttk.Icon("gear-fill", 40,
"warning")` remains the way to ask for a specific size or color.
