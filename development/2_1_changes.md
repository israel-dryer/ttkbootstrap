# ttkbootstrap 2.1 — notable changes (running log)

> The consolidated log of 2.1 changes that alter behavior or appearance, each
> with **what** changed and **why**. Same role its 2.0 counterpart
> (`2_0_breaking_changes.md`) played: kept in `development/` so it survives, and
> it is the source for the 2.1 release notes.
>
> Scope is **relative to released 2.0.0**. Regressions introduced *and* fixed
> within the 2.1 cycle never reached a user and are deliberately not logged here
> (they live in the dev log in `CLAUDE.md`).
>
> Legend: **API** = source-level break · **Visual** = appearance-only (no code
> change needed) · **New** = additive · **Fix** = something that did not work
> before now does.

## Index

| Area | Kind | Where |
|---|---|---|
| **Treeview / Tableview row height follows the configured font** | **Visual** | this doc, below |
| **Durable style options — `style.configure()` survives variants & theme switches** | New | this doc, below |
| **Notebook tab `padding` / `bordercolor` are now overridable** | Fix | this doc, below |
| **`DateEntry(value=…)` — a nullable, clearable date field** | New | this doc, below |
| **Scrolling works on Tcl/Tk 9** | Fix | this doc, below |
| **macOS renders at its designed size on Tcl/Tk 9** | Fix | this doc, below |

There are **no API breaks in 2.1**: nothing was removed, and no call that worked
in 2.0.0 fails. One change is visually noticeable without any code change (the
first row) — it is the one to lead the release notes with.

---

## Treeview / Tableview row height follows the configured font  *(Visual)*

**What.** `rowheight` is now derived from the font the treeview style actually
uses. Previously it was computed from `TkDefaultFont` at style-build time, so a
font the application configured was ignored and taller text was clipped.

**Who notices.** An app that sets a global font — the documented
`style.configure(".", font=("Cascadia Code", 24))` technique — and shows a
`Treeview` or `Tableview`. Those rows were clipped in 2.0.0 and now grow to fit,
so **layouts shift**:

| | 2.0.0 | 2.1 |
|---|---|---|
| plain `Treeview`, no configured font | 15px | 15px (unchanged) |
| `Tableview`, no configured font | 21px | 21px (unchanged) |
| plain `Treeview` + `configure(".", font="-size 24")` | 15px (clipped) | **36px** |
| `Tableview` + `configure(".", font="-size 24")` | 21px (clipped) | **50px** |

**Nothing changes for the default case** — an app that never configures a font
sees identical row heights. Only apps that already configured a larger font are
affected, and for those the previous rendering was clipping the text.

**Why.** This is the row-height half of #399; the column-width half was fixed in
#1158. Row height was still font-blind. Fixes #1160 (PR #1281).

**Scope.** Build-time only: a style that already exists is not rebuilt, so a font
set *after* the widget is created does not resize it. Set the font before
creating the widget (or switch themes) for it to take effect.

---

## Durable style options  *(New)*

**What.** Geometry and layout options set with `style.configure(...)` now
**persist**. In 2.0.0 they were silently discarded the moment a `bootstyle`
variant was built or the theme changed, because the style recipes rewrite their
own hardcoded values on every build.

```python
app.style.configure("TEntry", padding=8)

ttk.Entry(app)                      # padded
ttk.Entry(app, bootstyle="danger")  # ALSO padded (2.0.0: reverted to default)
```

Details:

- **Base → variant fan-out.** Set the option once on the base class (`TEntry`)
  and every variant built from it (`danger.TEntry`, …) picks it up. A more
  specific name wins.
- **Retroactive.** Widgets that already exist update too, so the result does not
  depend on whether the override or the widget came first.
- **Survives a theme switch.**
- **Colors are excluded on purpose** — they stay theme-reactive, so a color set
  this way applies immediately but is not replayed after a theme change.
- **`Style.reset_style_options(style=None)`** drops overrides; the shipped value
  returns on the next rebuild.

**Why.** Long-standing request (discussion #536): there was no supported way to
set a general property on a base style class and have it stick. Closes #1238 and
#1161 (PR #1279). Documented in *Custom styles → Change an option everywhere*.

**Caveat worth repeating in the release notes.** Persistence cannot make a widget
honor an option it never reads. `font` on an entry/combobox/spinbox comes from the
widget or the named `TkTextFont`, not the style; `sashthickness` works only on the
global `"Sash"` style. Both are Tk behaviors, unchanged by 2.1, and are documented
under *Options a widget doesn't read*.

---

## Notebook tab `padding` / `bordercolor` are now overridable  *(Fix)*

**What.** `style.configure("TNotebook.Tab", padding=…)` had no effect in 2.0.0.
It does now.

**Why.** The notebook recipe mapped `padding` (and `bordercolor`) to the *same*
value for both `selected` and `!selected`. Because those two states cover every
state, `lookup` always resolved through the map and silently masked the
`configure` value. Vanilla ttk honors the same call, so this was ours, not Tk's.
The redundant map entries were removed; `bordercolor` moved into `configure`
(it had no `configure` value, only the map).

**Appearance is unchanged** — the mapped and configured values were identical,
verified across every state (`selected`, `!selected`, `active`, `disabled`).
Found while reviewing the durable-options work (PR #1282).

---

## `DateEntry(value=…)` — a nullable, clearable date field  *(New)*

**What.** `DateEntry` gains a keyword-only `value=` parameter and a `clear()`
method, so a date field can be genuinely empty:

```python
picker = ttk.DateEntry(app, value=None)   # starts blank

picker.get_date()   # -> None
picker.clear()      # back to empty; set_date(None) and value = None are equivalent
```

**No change to existing code.** Omitting `value` keeps the 2.0.0 behavior exactly:
the field starts on today (or `start_date`), and `get_date()` never returns
`None`. Passing `value` — including `value=None` — opts into the nullable model,
where an empty field reads as `None` instead of falling back to `start_date`.

**Why.** An optional date is a normal form requirement (discussion #476) and had
no supported spelling. The additive half of #1253 (PR #1277); making
`value=None` the *default* is a breaking change deferred to 3.0 (#1276).

---

## Scrolling works on Tcl/Tk 9  *(Fix)*

**What.** `ScrolledFrame` (and the color dropper's zoom) scrolls correctly on a
Tk 9 interpreter. In 2.0.0, on Tk 9:

- a **trackpad, Magic Mouse or Magic Trackpad did nothing at all** — those
  devices fire `<TouchpadScroll>`, which nothing was listening for;
- **one wheel notch jumped to the end of the content** on macOS;
- **wheel scrolling was dead on Linux**, where `<Button-4>`/`<Button-5>` are no
  longer delivered to scripts.

**Who notices.** Anyone on an interpreter linked against Tk 9 — a Homebrew,
conda or pyenv build. The python.org installers still ship Tk 8.6, where nothing
changes. Check with:

```
python -c "import tkinter; print(tkinter.Tcl().eval('info patchlevel'))"
```

**Why.** Tk 9 changed the scroll-event contract: precise-delta devices report
through `<TouchpadScroll>` instead of `<MouseWheel>`, wheel deltas are normalized
to multiples of 120 on every platform (macOS previously reported 1 per notch),
and X11 wheel buttons are translated to `<MouseWheel>` internally (TIP 474). The
widgets were written against Tk 8.6 and read every one of those the old way.

One notch now moves one unit on every platform and Tk version, and a trackpad
gesture scrolls smoothly — pixel deltas are accumulated and spent as whole canvas
units, following Tk's own convention for units-based widgets.

Widgets that rely on Tk's class bindings (`Treeview`, `Listbox`, `Text`, and so
`ScrolledText`) were never affected: Tk 9 binds `<TouchpadScroll>` on those
classes itself. Fixes #1290.

---

## macOS renders at its designed size on Tcl/Tk 9  *(Fix)*

**What.** On a Tk 9 interpreter, every asset and every pixel-valued piece of
geometry rendered **33% larger than designed** on macOS — while the text inside
it stayed the same size. Padding, borders, indicators and icons inflated around
unchanged type:

| widget | Tk 8.6 | Tk 9 in 2.0.0 | Tk 9 in 2.1 |
|---|---|---|---|
| `Button` | 56 x 30 | 62 x 32 | 56 x 30 |
| `Entry` | 194 x 30 | 198 x 34 | 194 x 30 |
| `Checkbutton` | 44 x 18 | 52 x 24 | 44 x 18 |
| `Label` (text only, no scaled padding) | 34 x 20 | 34 x 20 | 34 x 20 |

That last row is the tell: a plain label was identical throughout, because it is
pure text. Only the parts ttkbootstrap scales moved.

**Who notices.** macOS users on an interpreter linked against Tk 9 — Homebrew,
conda or pyenv. Windows and Linux were never affected, and the python.org
installers still ship Tk 8.6.

**Why.** ttkbootstrap converts logical UI units to pixels against a baseline for
what "100% scaling" reports. Aqua assumed **72 dpi** (`tk scaling` 1.0), while
every other platform assumed 96 (4/3). Tk 9 aligned aqua with the rest at 96, so
the same unchanged screen now reports 1.333 — and reading it against the old
baseline yielded a 4/3 factor where the answer should be 1.0. The baseline is now
gated on the Tk version as well as the platform.

**Fonts were never the problem, which is what makes it subtle.** Tk 9 restates
`TkDefaultFont` as size 10 where Tk 8.6 called it 13, but both render at a 16px
linespace — the nominal number changed with the dpi assumption, the rendered text
did not. Had the text actually grown, scaling the assets to match would have been
correct.
