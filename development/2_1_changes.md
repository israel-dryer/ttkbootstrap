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
