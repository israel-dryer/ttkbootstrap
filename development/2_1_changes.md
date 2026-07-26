# ttkbootstrap 2.1 — notable changes (running log)

> The consolidated log of 2.1 changes that alter behavior or appearance, each
> with **what** changed and **why**. Same role its 2.0 counterpart
> (`2_0_breaking_changes.md`) played: kept in `development/` so it survives, and
> it is the source for the 2.1 release notes.
>
> Scope is **relative to the latest released 2.0.x** (currently 2.0.1).
> Regressions introduced *and* fixed within the 2.1 cycle never reached a user
> and are deliberately not logged here (they live in the dev log in
> `CLAUDE.md`) -- and neither does anything already shipped in a 2.0.x patch,
> since the 2.1 notes must not re-announce it. The two Tcl/Tk 9 fixes shipped
> in **2.0.1** for exactly that reason.
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
| **Bootstyle value tokens — raw hex + ramp accents & surfaces** | New | this doc, below |
| **Themed file dialog — a theme-following open/save chooser** | New | this doc, below |

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

## Bootstyle value tokens — raw hex + ramp accents & surfaces  *(New)*

**What.** The `bootstyle` grammar's two color-bearing slots — the color slot and
the `@surface` slot — now accept **value tokens** alongside the closed
vocabulary:

- a **raw hex** color: `bootstyle="#2f2f2f"`, `bootstyle="@#ff0000 #ffffff"`
  (3-digit `#f00` is accepted and normalized to `#ff0000`);
- a **ramp-addressed role**: `bootstyle="primary[300]"`,
  `bootstyle="@background[200] danger"` — `role[stop]`, where `stop` is a
  50–950 ramp step and `role` one of the accent roles or `background`/
  `foreground`, matching Python-side `colors.primary[300]` addressing.

Everything already in the grammar is unchanged; these are two additional
eagerly-validated patterns, so a malformed value token (`#ff00zz`,
`primary[123]`) fails loudly like any unknown token — warn by default, raise
under `set_bootstyle_strict(True)` / `TTKBOOTSTRAP_STRICT=1`. Value tokens are
legal only in the color and surface slots; variants, base-types, and orients
stay a closed vocabulary.

**Reactivity.** A ramp token is semantic and **re-resolves on a theme switch**
(`primary[300]` is "a tint of the current theme's primary" in every theme). A
raw hex is a deliberate **frozen snapshot** — the same trade as a direct color on
a `Label`: it survives theme switches without adapting, and contrast is the
caller's responsibility. A hex accent's *derived* states (hover/pressed/disabled/
on-color) still recompute per theme, so a hex button stays usable in both modes.

**Why.** A one-off color previously required the full custom-style path
(`register_style` / `Style.configure` + `style=`) — the right home for a bespoke
*look*, but heavy ceremony for a single *color*. Value tokens give it a one-line
spelling, the same move Tailwind's arbitrary-value syntax (`bg-[#ff0000]`) makes
on the same kind of closed utility vocabulary.

**Note.** Each distinct hex mints a ttk style that lives for the process (styles
are never unregistered). The closed vocabulary and the ramp tokens are finite, so
their styles plateau; the space of raw hex values is not, so an app that feeds
many distinct hex values through `bootstyle` accumulates styles over its lifetime.

---

## Themed file dialog — a theme-following open/save chooser  *(New)*

**What.** ttkbootstrap now ships an in-library file dialog that follows the active
theme, reproducing the familiar layout of Tk's chooser (a directory bar, a file
listing, a filename field + filetype selector, OK/Cancel) with themed widgets.
The four `Querybox` file wrappers gain a `native` selector to choose it:

```python
# force the themed dialog anywhere (light or dark, it matches your app)
path = ttk.Querybox.get_open_filename(native=False, filetypes=[("Text", "*.txt")])

ttk.Querybox.get_open_filenames(native=False)   # multi-select -> tuple | None
ttk.Querybox.get_save_filename(native=False, defaultextension=".txt")
ttk.Querybox.get_directory(native=False)
```

`native=None` (the default) uses the native OS chooser as before; `native=True`
forces it. The return contracts are unchanged — a path `str`, a `tuple[str, …]`
for multi-select, or `None` on cancel.

**Why.** On Windows and macOS the OS draws a great native chooser, but **X11 has
no native dialog** — Tk falls back to a chooser whose central file list is an
unstyleable white Canvas that ignores the theme (jarring in dark mode). The themed
dialog replaces it. On X11 it will become the **default** (so a dark-themed Linux
app stops flashing a white panel); on Windows/macOS the native chooser stays the
default and the themed one is opt-in via `native=False`. Addresses #1242.

**Scope note.** This first slice ships the dialog and the `native=` opt-in; the
X11-by-default routing lands next in the same 2.1 cycle. Deliberately minimal
(no bookmarks/places sidebar) — matching Tk's chooser; a sidebar is a later
enhancement.
