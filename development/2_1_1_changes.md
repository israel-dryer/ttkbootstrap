# ttkbootstrap 2.1.1 — notable changes

> The consolidated log of changes that alter behavior or appearance since
> **2.1.0**, each with **what** changed and **why**. Same role its predecessors
> (`2_1_changes.md`, `2_0_breaking_changes.md`) played: kept in `development/`
> so it survives, and the source for the release notes when this ships.
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
abbreviations, `name`/`class_`, ttk's raw `style=`, and the entry family's
`background`. Options a widget only accepts at construction — `autostyle`,
`class_`, and the root window's `screen`/`container`/`visual`/`colormap` — are
absent from `configure()`, matching what Tk does at runtime.

**Note for the reporter's case:** nothing about `import ttkbootstrap as tb` and
`tb.Frame(self)` was ever wrong; the parameters were simply no longer visible.
