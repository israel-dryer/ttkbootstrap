# ttkbootstrap 2.1.1 — notable changes

> The consolidated log of changes that alter behavior or appearance since
> **2.1.0**, each with **what** changed and **why**. Same role its predecessors
> (`2_1_changes.md`, `2_0_breaking_changes.md`) played: kept in `development/`
> so it survives, and the source for this release's notes.
>
> **A typing- and docs-only patch.** No runtime behavior changes: the shipped
> stub is inert at import, and the one library file touched is a reference page.
>
> Scope is **relative to 2.1.0**. A regression introduced *and* fixed inside
> this cycle never reached a user, so it belongs to the dev log in `CLAUDE.md`,
> not here.
>
> Legend: **API** = source-level break · **Visual** = appearance-only (no code
> change needed) · **New** = additive · **Fix** = something that did not work
> before now does.

## Index

Rows mirror the section headings below, in order.

| Area | Kind |
|---|---|
| **Widget constructor parameters are back in editors** | Fix |

There are **no API breaks**: nothing was removed, and no call that worked in
2.1.0 fails.

---

## Widget constructor parameters are back in editors  *(Fix)*

**What.** Hovering a widget constructor in an editor — `ttk.Button(`,
`ttk.Frame(`, any of the 26 native widgets — shows that widget's parameters
again, with a description for each, and autocomplete offers them. Type checkers
(mypy, pyright/Pylance) also flag a misspelled keyword instead of accepting it
silently.

**Who notices.** Anyone writing ttkbootstrap code in PyCharm, VS Code or any
editor with a language server — most acutely someone learning tkinter, who was
relying on the parameter list to discover what a widget can do.

**Why it broke.** 1.x shipped a hand-written `__init__.pyi` type stub that
spelled out every widget's keyword arguments. 2.0 replaced the import-time
monkey-patch with real subclasses (`class Button(BootMixin, ttk.Button)`) and
deleted the stub, on the reasoning that inheritance would carry the signatures
through. It doesn't: `BootMixin` precedes the ttk class in the MRO and its
constructor is `(*args, **kwargs)`, so that generic signature is what an editor
resolves — and the one-line class docstring is all it has left to show. Because
`py.typed` still shipped, type checkers read the same `**kwargs` and stopped
checking widget keywords altogether.

**What changed.** `ttkbootstrap/__init__.pyi` is back, now **generated** rather
than hand-written (`python tools/generate_widget_stubs.py`). It takes each
widget's options *and* its description from the per-widget reference pages under
`docs/reference/api/`, so what your editor shows is the same text as the
documentation — the tooltip opens with what the widget actually is ("Frame is
the native ttk rectangular container for grouping and laying out other
widgets"), not a note that it is themed. A `tests/test_widget_stubs.py` sync
test keeps the two from drifting apart.

**What it accepts.** The documented options, plus the spellings that work
without being part of the documented surface: Tk's `bd`/`bg`/`fg`
abbreviations, `name`, ttk's raw `style=`/`class_=`, and the entry family's
`background`. Value types are deliberately wide, because Tk takes more than one
spelling of most of them and a stub that rejects working code is worse than one
that misses a wrong value — `font=("Helvetica", 12)` as well as a string or a
`Font`, `values=`/`columns=` as a tuple or a list, and `image=` as a tkinter
image, a Pillow `ImageTk.PhotoImage`, or a Tk image name.

Where the constructor and `configure()` differ, the stub follows what actually
works. Options a widget only accepts at construction — `autostyle`, and the root
window's `screen`/`container`/`visual`/`colormap` — are absent from
`configure()`. `OptionMenu` is the reverse and the sharpest case: its
constructor takes only `command`, `direction`, `style` and `name` and raises
`TclError: unknown option` for the rest, so the menubutton options it inherits
are offered on `configure()` only. Its reference page now documents `command`,
which was missing, and no longer claims every option works in both places.

**Note for the reporter's case:** nothing about `import ttkbootstrap as tb` and
`tb.Frame(self)` was ever wrong; the parameters were simply no longer visible.
