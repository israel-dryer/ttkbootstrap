# ttkbootstrap 2.0 — breaking & notable changes (running log)

> The consolidated log of 2.0 changes that alter behavior or appearance, each
> with **what** changed and **why**. Kept in `development/` so it survives the
> docs transition; it is the source for the Workstream-H *Migrating to 2.0* page.
> Dedicated guides hold the deep detail for some areas (linked below); this log
> is the index plus the home for changes without their own guide.
>
> Legend: **API** = source-level break · **Visual** = appearance-only (no code
> change needed) · **New** = additive.

## Index

| Area | Kind | Where |
|---|---|---|
| Theme model, `Theme`, default theme, ramp addressing | API | `development/2_0_theme_migration.md` |
| **Legacy theme names auto-register on use (no hard-stop)** | Fix/Deprecated | this doc, below (Slice 1) |
| **`App` (canonical) / `Window` alias; `theme` / `themename` alias** | New | this doc, below (Slice 2) |
| **`utils/` package; `utility`/`colorutils` → warn-and-forward shims** | Deprecated | this doc, below (Slice 0) |
| Canonical `bootstyle` grammar (closed vocab, strict mode) | API | `development/2_0_bootstyle_grammar_design.md` |
| Character-based icons removed (`ttkbootstrap.icons`) | API | `development/2_0_icon_drop_design.md` (PR #1094) |
| Delivery API (mixins, no import-time monkey-patch) | API | handoff / PR #1075 |
| **Fluent geometry (`pack`/`grid`/`place` return the widget)** | New | this doc, below |
| **`TkLabel` blessed tk.Label + ColorChooser default-mode fix** | New/Fix | this doc, below |
| **`neutral` color** | New | this doc, below |
| **`ghost` button variant** | New | this doc, below |
| **`thin` scrollbar variant** | New | this doc, below |
| **Scrollbar restyle (visible trough, square default)** | Visual | this doc, below |
| **Button-family visual restyle (flat + hairline border)** | Visual | this doc, below |
| **Bare buttons default to `neutral`** | Visual/API | this doc, below |
| **Dialog API normalization (Messagebox/Querybox)** | API | `development/2_0_shipped_widget_api_design.md` (PR A) |
| **Meter: snake_case options, DoubleVar, `value`** | Breaking/additive | this doc, below (PR 2 / #1110) |
| **DateEntry: snake_case (cross-layer), live-text read, string `state`** | Breaking/additive | this doc, below (PR 3 / #1111) |
| **Floodgauge: DoubleVar value, `start(interval)`, live mode/orient** | Breaking/additive | this doc, below (PR 4) |
| **Scrolled: Canvas-viewport rewrite, `auto_hide`, keyword-only** | Breaking/additive | this doc, below (PR 5) |
| **LabeledScale + ToolTip: DoubleVar, lifecycle, `configure`/`cget`** | Breaking/additive | this doc, below (PR 6) |
| **ToastNotification: glyph icon, stack manager, keyword-only** | Breaking/additive | this doc, below (PR 7) |
| **Borderless popups get native macOS chrome (no titlebar)** | Visual | this doc, below |
| **`card` / `highlight` frame variants** | New | this doc, below |
| **`Text` border left to tk default (not themed)** | Visual | this doc, below |
| **ScrolledText: card border, focus ring, auto-hide fixes** | Visual | this doc, below |
| **Scrollbar: no trough channel, darker light-mode thumb** | Visual | this doc, below |
| **Inputs: focus color on focus only (not hover)** | Visual | this doc, below |
| **`card` / `highlight` frames: hairline border (`RAISED`, no bevel)** | Visual | this doc, below |
| **Control-height parity + check/radio/menubutton focus rings** | Visual | this doc, below |

---

## Legacy (pre-2.0) theme names auto-register on use  *(Fix / Deprecated)*

**What.** `ttk.Window(themename="darkly")` (and any `theme_use("<legacy>")`)
works again. In 2.0 the curated semantic-anchor catalog replaced the pre-2.0
theme names, and those old names were opt-in only via
`ttk.install_legacy_themes()` — so `theme_use("darkly")` on a legacy name raised
`TclError` with no ordering that fixed it from user code (the first line of
~every existing app broke). Now, when a name is in `STANDARD_THEMES` but not yet
registered, `theme_use` **lazily adapts + registers just that one theme**
(`theme_from_legacy_dict` → `register_theme`), emits a one-time
`DeprecationWarning`, and builds it normally. `darkly` still looks like darkly
(only its buggy plumbing is regenerated). `install_legacy_themes()` stays as the
explicit **bulk** register so `theme_names()`/ttkcreator can enumerate the full
legacy set.

**Why.** Prefer deprecation over a hard break. There is no 1:1 legacy→2.0 theme
mapping (`darkly` ≠ `bootstrap-dark`, different palettes), so forcing migration
would change every app's colors *and* its code. This intentionally reverses
Workstream E's "opt-in only" decision — that decision is what created the wall —
while keeping its deprecation nudge (a per-name `DeprecationWarning`).

**Not changed.** The default theme: `ttk.Window()` with no name still renders
`bootstrap-light` — a documented *visual* change, not a crash.

---

## Utilities reorganized into a `utils/` package  *(Deprecated old paths — no break)*

**What.** The public utility helpers now live in a first-class **`ttkbootstrap.utils`**
package instead of the pre-2.0 scatter (`ttkbootstrap.utility` grab-bag +
`ttkbootstrap.colorutils`):

- `utils/color.py` — `color_to_rgb`/`color_to_hex`/`color_to_hsl`/
  `update_hsl_value`/`contrast_color`/`conform_color_model` (was `colorutils`).
- `utils/scaling.py` — `enable_high_dpi_awareness`, `scale_size` (from `utility`).
- `utils/platform.py` — `windowing_system` (from `utility`).
- `utils/__init__.py` re-exports the whole surface, so `from ttkbootstrap.utils
  import ...` reaches everything from one namespace.

The old module paths **still work** as thin **warn-and-forward shims** (same
pattern as `ttkbootstrap.publisher`): importing `ttkbootstrap.utility` or
`ttkbootstrap.colorutils` emits a one-time `DeprecationWarning` and re-exports the
moved names (including the `colorutils` model constants and the two
already-internal `utility` forwards). Removed in 3.0. Everything also stays
re-exported at the **top level** (`ttk.scale_size`, `ttk.contrast_color`, …) — the
primary discovery path — unchanged.

**Migration.** `from ttkbootstrap.utility import scale_size` →
`from ttkbootstrap.utils import scale_size` (or keep using `ttk.scale_size`);
`from ttkbootstrap import colorutils` → `from ttkbootstrap import utils`. No
behavior changed — the functions are the same objects.

**Why.** Utilities are a first-class concern in ttkbootstrap (a styling
extension) in a way they aren't in a widget library, so they get a deliberate,
discoverable home instead of a `utility.py` grab-bag plus a separate
`colorutils.py`. This also gives the later 2.0 slices (typography, deferred-config)
a place to be *born* rather than bolted onto the grab-bag. The old paths shim
rather than break, matching "prefer deprecation over hard breaks." (The shims are
source-only back-compat and are not documented; docs present `utils/` as the home.)

---

## `App`/`Window` and `theme`/`themename` naming aliases  *(New — no break)*

**What.** Two disambiguating renames, both delivered as **additive permanent
aliases** — nothing existing breaks, and **no deprecation warnings** (these are
the most-typed identifiers in every app).

- **`App` is now the canonical application-root class; `Window` is a permanent,
  fully-supported alias** (`Window = App`, the same class object). So
  `type(app).__name__`, `repr`, and tracebacks read `App`, while `ttk.Window(...)`,
  `isinstance(x, Window)`, and existing `class MyApp(ttk.Window)` subclasses keep
  working unchanged. `Toplevel` is untouched (already unambiguous).
- **`theme` is now the canonical constructor argument on `App`/`Window`/`Style`;
  `themename` is a permanent, non-deprecated alias.** `Style` already used
  `theme`; only the window classes were out of step. `theme` is the second
  positional on `App`/`Window` (so `App("Title", "darkly")` still means theme),
  and both `theme=` and `themename=` are accepted (canonical `theme` wins if both
  are given).

**Unchanged (deliberately).** `Style.theme_use(themename)` and
`Style.theme_create(themename)` **keep the `themename` parameter** — they override
`ttk.Style` methods whose tkinter parameter is literally `themename`, so they keep
Tk's spelling for drop-in compatibility (and are almost always called
positionally). This sharpens the 2.0 naming convention rather than breaking it:
`theme` on the authored constructors, Tk spelling on the ttk.Style method
overrides.

**Why.** `Window` is ambiguous — a `Toplevel` is also a window. `App` (the one
root, paired with the singleton `Style`) vs `Toplevel` (many) is the clearer
split and mirrors tkinter's `Tk`/`Toplevel`. And `Style` already spelled it
`theme`, so accepting `theme` on the window constructors removes a needless
inconsistency. Both are aliases (not deprecations) because a warning on `Window`
or `themename` would fire in ~100% of existing apps for a pure naming preference.
Docs lead with `App`/`theme`; `Window`/`themename` are documented as the aliases.

---

## `neutral` — a new semantic color  *(New)*

**What.** A new bootstyle color, `neutral` (e.g. `bootstyle="neutral"`,
`bootstyle="neutral-outline"`), for a low-emphasis, unaccented button. Additive —
nothing existing changes; the default button is still `primary`.

**Why.** There was no calm, theme-adaptive "just a button." `secondary` is a
medium-emphasis gray *fill*; `light` is a fixed pale tone with no border, so it
vanishes on a light surface. People reached for `light` to fake a quiet button,
which then became a *bright* button in dark themes. `neutral` fills the gap
correctly: it is **derived from the theme surface** (a mode-aware raise — darker
than the page in light themes, lighter in dark), always low-emphasis, and it
follows the theme. Ported from bootstack's neutral (its default button =
`elevate(surface, 1)` + a derived border) — mechanism borrowed, not API.

**`neutral` vs `light`/`dark`.** They are not redundant. `light`/`dark` are
**fixed tones** (always pale / always dark, regardless of mode) and are full
palette colors usable on every widget; `neutral` is **theme-adaptive, always
quiet**, and is scoped to buttons. Use `light`/`dark` for a deliberate tone (e.g.
a light button on a colored header); use `neutral` for "no emphasis, follow the
theme."

**Scope.** Buttons (and the extending button-family widgets — see below).
`NEUTRAL_FAMILIES` in `constants.py` gates where it is advertised.

**Migration.** None required. Optionally replace `bootstyle="light"` buttons that
were standing in for a quiet/subtle button with `bootstyle="neutral"` — it will
stay quiet in dark mode where `light` would turn bright.

Design: `development/2_0_neutral_color_design.md`.

## Scrollbar restyle — visible trough, inset thumb, square default  *(Visual)*

**What.** The standard (`default`) and `round` scrollbars were reworked:
- a **visible trough** (a subtle track shade of the surface) so the thumb reads
  as sliding in a channel rather than floating on the surface;
- the thumb is **inset** ~1px from the trough walls (a transparent margin baked
  into the thumb image), so there is a track of space around it;
- the thumb has a **minimum length** (a 9-slice end region), so a long list can't
  shrink it to a microscopic sliver;
- `default` is now a **flat square** thumb and `round` a **pill** (they used to be
  nearly identical rounded thumbs);
- **no arrows** (the previous `arrowsize` was already dead layout config).

The `thin` variant is unchanged. The combobox popdown uses `thin`; the font dialog
lists use the square `default`.

**Why.** The 2.0 scrollbars had an invisible trough (= surface) and a thumb that
floated with no track and could collapse to nothing on a long list. Restoring a
visible trough + inset thumb + min size makes them read as real scrollbars (closer
to 1.0), and splitting square/round gives a genuine choice. Ports the visible-trough
idea from 1.0; thumb margin/min-size are implemented via the image + 9-slice border.

**Migration.** None (appearance only). `bootstyle="round"` is still the pill;
the default is now square.

## `thin` — a new scrollbar variant  *(New)*

**What.** A thin scrollbar (`bootstyle="thin"`, `primary-thin`, …): a few-pixel
flat thumb on a surface-matched track, **no arrows**. Neutral by default (thumb =
`border(surface)`), or the accent when a color is given; darkens/lightens on
hover/press. It is now the scrollbar used in the **Combobox popdown** and the
**font dialog** lists — narrow spaces where the bar is a scroll *indicator* more
than a drag handle. Additive; the standard (`default`) and `round` scrollbars are
unchanged.

**Why.** The standard scrollbar (with arrows, an 18×8 rounded thumb) is heavy in a
cramped dropdown. bootstack's thin bar reads as a clean sliver. Ported from
bootstack (mechanism, not API) — the thumb is a solid box from the `rect` toolkit,
so no new PNG asset was added.

**Migration.** None (additive). Opt in with `bootstyle="thin"` on any `Scrollbar`.

## `ghost` — a new button variant  *(New)*

**What.** A new button modifier, `ghost` (e.g. `bootstyle="ghost"`,
`bootstyle="primary-ghost"`). A ghost button is **transparent at rest** — no fill,
no border, just its label — and gains a **subtle wash** on hover/press: a light
tint of the accent for a colored ghost (`primary-ghost` → a faint blue wash), or a
neutral surface raise for the default/neutral ghost. Additive.

**Why.** It fills the gap between `link` (text-only, hyperlink feel) and `outline`
(bordered): more button-like than a link (it has a hover surface), quieter than an
outline. Common for toolbar/icon buttons and low-emphasis actions. Ported from
bootstack's ghost button (derivation, not API). Button family only.

**Migration.** None (additive).

## Button-family visual restyle — flat fill + 1px hairline border  *(Visual)*

**What.** Solid buttons changed from a flat fill with **no border** to a flat
fill with a subtle **1px hairline border** derived from the fill. Applies to the
solid `ttk.Button` and (as it lands) the other button-family widgets
(`Menubutton`, `Toolbutton`, the DateEntry button). No API change — existing
`bootstyle` values are unchanged; only the rendered appearance differs.

**Why.**
- **Definition on any surface.** A borderless fill has no edge where it meets a
  same-ish background (a `light`/`neutral` button on a white page effectively
  disappeared). A hairline border gives every button a defined shape.
- **Consistency.** With `neutral` introduced (which *needs* a border to read),
  bordering only neutral would make it a different species from the accent
  buttons. One border rule keeps the family uniform.
- **Still flat.** The border is not a bevel. clam ties "border" to a two-tone 3D
  bevel; to keep the button flat we set `darkcolor`/`lightcolor` to track the
  fill at rest so only a single-color 1px edge shows (the resting edge sharpens
  slightly to the border color on hover/press). The border color is
  **fill-derived** (same hue), never a gray outline.

**Details that were deliberately chosen (and why):**
- **`borderwidth=1`, unscaled.** A hairline stays one physical pixel at every DPI;
  scaling it makes it read as a thick 2px+ edge on hi-DPI displays. (A narrow
  exception in the scaling guard permits the literal `borderwidth=1`.)
- **clam limits, acknowledged.** clam cannot draw a flat, bevel-free, *rounded*
  border — rounded/consistent corners would require image-based (9-slice) border
  elements (bootstack's approach; the recolor pipeline from #1081 exists but no
  button template was added for 2.0). 2.0 ships the flat clam border; image-based
  rounded buttons remain a possible later change.

**Migration.** None required. Apps will simply look slightly more defined. If you
had custom `TButton` styles that assumed no `bordercolor`, note that the built-in
solid recipe now sets one.

Design/rationale trail: `development/2_0_neutral_color_design.md` §3a.

## Toolbutton & switch state colors — bootstack on/off model  *(Visual)*

**What.** The unselected/selected ("off"/"on") colors for the solid **Toolbutton**
and the "off" track of the **switch** (round/square toggle) were re-derived to
bootstack's model:
- **Toolbutton OFF** was a fairly heavy gray fill (`colors.border` in light /
  `colors.selectbg` in dark) with a full-contrast label. It is now a **quiet
  raised surface** (`neutral_fill` = a mode-aware ~6% elevation of the surface)
  with a **muted** label (`mute(fg)`). **ON** is unchanged (the accent).
- **Switch OFF** track was `mute(fg)` (a mid-gray from the text); it is now
  `border(surface)` — the derived neutral border color, a lighter/quieter off
  state.
- **Neutral toolbutton** (new — `bootstyle="neutral-toolbutton"`) has no accent to
  latch to, so "on" is shown by a **stronger** surface raise (`neutral_fill`
  level 2, ~12%) versus the level-1 "off" fill.
- **Toolbuttons are now pure toggles**: only ON (selected) vs OFF (unselected)
  change the appearance. The previous hover/active "preview the on state" and the
  pressed state were removed -- a toggle has two states, and previewing the
  selected look on hover was misleading. (Outline toolbuttons also gained the
  solid toolbutton's `focusthickness`, so both variants are the same height and a
  toolbutton no longer nudges its neighbors when it takes keyboard focus.)

**Why.** The old toolbutton off state was visually loud (a solid gray chip),
competing with the selected accent. bootstack's model reads better: off is a calm,
barely-there surface with de-emphasized text, so the *selected* segment clearly
carries the emphasis. The switch off track likewise reads quieter. All derived
(no new authored colors), mode-aware, via existing helpers (`neutral_fill`/`mute`/
`border`), ported from bootstack's `toolbutton`/`switch` builders (mechanism, not
API). `neutral_fill` gained a `level` argument for the level-1/level-2 raise.

**Open (visual gate):** the neutral toolbutton distinguishes on/off by elevation
only (~6% vs ~12%); confirm on a light↔dark spot-check that the selected state
reads clearly enough (the level-2 weight is the knob).

**Migration.** None (appearance only). `toolbutton` joins `NEUTRAL_FAMILIES`, so
`neutral-toolbutton` / `neutral-outline-toolbutton` are now valid bootstyles.

## Bare buttons default to `neutral`  *(Visual / small API)*

**What.** A bare `ttk.Button()` / `ttk.Menubutton()` (no `bootstyle`) now renders
**neutral** instead of **primary**. Opt into an accent explicitly
(`bootstyle="primary"`). A new construction-time setting restores the old default:
`Window(default_button="primary")` (or `Style(theme, default_button="primary")`).

**Why.** A plain button is not a call-to-action — it should be quiet by default,
and you opt into emphasis (the Bootstrap/bootstack model). This suits
ttkbootstrap's utility/scientific audience, who generally want a calm default over
a blue CTA.

**Scope.** `Button` and `Menubutton` only. **Not** Toolbutton / Toggle /
Checkbutton / Radiobutton — their default accent is the *selection* signal, and
they are already neutral *at rest* (OFF = the quiet surface, ON = accent), so
flipping their ON state would only remove the selection color. The DateEntry
button (an internal affordance) also stays primary.

**Mechanism.** `default_button` is a **color name** (default `"neutral"`) stored on
the `Style` and read once when the base `TButton`/`TMenubutton` builds — a
construction-time choice, **not** a runtime toggle. Explicit styles
(`primary.TButton`, etc.) are unchanged. Dialogs set `bootstyle` explicitly, so
their CTA emphasis is unaffected.

**Migration.** Add `bootstyle="primary"` to buttons that should be call-to-action,
or set `Window(default_button="primary")` to restore the pre-2.0 default globally.

Design: `development/2_0_neutral_default_design.md`.

## Dialog API normalization — Messagebox/Querybox signatures & returns  *(API)*

Shipped-widget API pass, **PR A** (design: `development/2_0_shipped_widget_api_design.md`).

**What.**
- **`Messagebox` signatures are uniform and `parent`/`alert` are keyword-only.**
  Every method is now `method(message, title, *, parent=None, alert=False,
  position=None, buttons=None, icon=None, localize=True)`. Previously some methods
  ordered the positional args `parent, alert` and others `alert, parent`, so a
  positional third argument was ambiguous. The formerly hidden `**kwargs` options
  (`position`, `buttons`, `icon`, `localize`) are now discoverable named params.
- **`Querybox.get_date` returns `None` when cancelled** (closed without picking a
  day). Previously it *always* returned a `date`, silently falling back to
  `startdate`/today, so cancellation was indistinguishable from a selection.
  `get_date` also gained a `position=` argument.
- **All `Querybox.get_*` methods return via the `Dialog.result` property**, not
  the private `._result`, so the modal grab is released consistently. `get_string`
  / `get_item` still return `""` on submit-of-empty vs `None` on cancel (now
  documented, not accidental).
- **`MessageDialog.command` accepts a plain zero-argument callable.** The legacy
  `(callable, label)` tuple form (the label was never used) is deprecated and
  normalized with a `DeprecationWarning` (removed in 3.0).
- **`Messagebox`/`Querybox` and the dialog classes are re-exported at top level**
  (`ttk.Messagebox`, `ttk.Querybox`, `ttk.MessageDialog`, …), matching how widgets
  are exposed. `ttkbootstrap.dialogs.*` import paths remain valid.
- Internal: `DatePickerDialog` gained an `autoshow=False` path + a `show()` method
  + a `result` property so `get_date` can position the popup and detect
  cancellation without blocking in the constructor (the default `autoshow=True`
  keeps the old blocking-in-`__init__` behavior for direct users). The duplicate
  `ColorChoice` namedtuple in `colorchooser.py` now imports the one in
  `colordropper.py` (single type).

**Why.** These were the shipped-widget inconsistencies flagged by the 2.0 API
survey: an ambiguous positional order, an un-signalable cancel, four different
result-access conventions, and a vestigial tuple param. Normalizing them now (API
pass before the Workstream-H docs) means the docs get written against final
signatures.

**Migration.**
- Pass `parent=`/`alert=` by keyword to `Messagebox.*` (positional no longer
  accepted). Almost all existing code already does.
- If you called `Querybox.get_date(...)` and used the result unconditionally,
  guard for `None` (a cancel). E.g. `d = Querybox.get_date(); if d: ...`.
- Replace any `MessageDialog(command=(fn, "label"))` with
  `MessageDialog(command=fn)`.

**Not breaking.** `message` (Messagebox) vs `prompt` (Querybox) is kept — it is a
real told-vs-asked distinction. `parent` stays the owner-argument name across the
dialog surface (the embeddable `ColorChooser` frame keeps `master`).

## Window/Toplevel API normalization — snake_case, keyword-only, positioning  *(API)*

**What.** `Window` and `Toplevel` now share a private `_BaseWindow` mixin and a
normalized constructor surface (shipped-widget API pass, PR B).

- **Raw-Tk-mirroring kwargs are snake_cased** with warn-and-normalize aliases
  (removed in 3.0): `hdpi`→`high_dpi`, `overrideredirect`→`override_redirect`,
  `windowtype`→`window_type`, `toolwindow`→`tool_window`. The old spellings still
  work through 2.x but emit a `DeprecationWarning`.
- **Constructors are keyword-only after the leading positional(s)**: `Window(title,
  themename, *, ...)` and `Toplevel(title, *, ...)`. Everything past those (e.g.
  `size`, `iconphoto`, `alpha`, `default_button`) must be passed by keyword. This
  cannot be shimmed (positional args carry no name) — documented breaking change,
  low real-world incidence.
- **`Toplevel.iconify` is a real keyword-only parameter** (default `False`), no
  longer smuggled through `**kwargs`.
- **`iconphoto` semantics are unified** across both classes via one `_setup_icon`
  helper: `None` skips (leave untouched), `''` uses the default (brand icon on
  `Window`, inherit on `Toplevel`), a path loads with fallback. This fixes the old
  `Toplevel(iconphoto=None)` crash (it fell into `PhotoImage(file=None)`), and a
  bad icon path now emits a `UserWarning` instead of `print()`ing to stdout. A
  `.ico` path is applied via `wm_iconbitmap` on Windows.
- **`position` accepts negative (edge-relative) offsets** — it now emits
  `f"{x:+d}{y:+d}"`, so `position=(-10, -10)` places the window relative to the
  bottom-right edge; `size`+`position` apply as one combined `geometry()` call.
- **`place_window_center`/`position_center` use the new positioning utility**
  (`internal/positioning.py`, a subset of bootstack's `WindowPositioning`):
  monitor-aware centering (via optional `screeninfo`, graceful single-screen
  fallback) + on-screen clamping. Previously it ignored the titlebar and was not
  multi-monitor aware.
- Internal/polish: the `style` property returns the singleton consistently on both
  classes; `overrideredirect(True)` is a silent no-op on macOS (aqua) where it
  destabilizes Tk; on win32 an explicit AppUserModelID is set so the taskbar shows
  the app icon, not `python.exe`.

**Why.** `Window`/`Toplevel` were the last shipped surfaces with un-normalized
signatures: raw Tk attribute names, a ~14-param all-positional constructor, a
smuggled `iconify`, two diverging `iconphoto` implementations (one crashing on
`None`), a `+{x}+{y}` position that couldn't express edge offsets, and a
titlebar-ignorant single-screen centering. bootstack had already solved the
cross-platform quirks; we borrow the mechanisms (not the API).

**Migration.**
- Rename kwargs: `hdpi=`→`high_dpi=`, `overrideredirect=`→`override_redirect=`,
  `windowtype=`→`window_type=`, `toolwindow=`→`tool_window=`.
- Pass window options by keyword (they already usually are): `Window("Title",
  size=(800,600))`, not `Window("Title", "theme", "primary", ...)` positionally.

**Not breaking.** `minsize`/`maxsize` are kept (they mirror the Tk method names the
tuple wraps — consistency-with-Tk wins over bootstack's `min_size`/`max_size`).
`screeninfo` is an *optional* import; without it centering falls back to Tk's
single-screen metrics (no new hard dependency — Pillow stays the only one).

## Tableview re-export + bug fixes  *(API + behavior)*

**What.** `Tableview` normalization (shipped-widget API pass, PR C — fixes only;
the method-verb rename is a deferred later slice).

- **`Tableview`, `TableColumn`, and `TableRow` are re-exported at top level**
  (`ttk.Tableview`, matching every other widget) and from
  `ttkbootstrap.widgets`. The `ttkbootstrap.widgets.tableview.*` import path stays
  valid.
- **`insert_row(values=[])` now raises `ValueError`** instead of `print()`ing
  `"[TableView] Cannot insert. No values found."` to stdout and returning `None`.
  This also surfaces in the batch paths (`insert_rows`, and the constructor's
  `rowdata`) — a row with no values is now a loud error, not a silent skip.
- **Two latent bugs fixed** (were dead-on-call): `delete_column(cid=...)` used
  `self.cidmap(int(cid))` (calling a dict → `TypeError`) — now
  `self.cidmap.get(int(cid))`, matching the sibling column methods; the header
  right-click menu's `self.master = self.master` self-assignment now sets
  `self.master` from the constructor argument.
- **Dead code removed**: the `reset_row_sort` `...` stub (`reset_column_sort` +
  `reset_table` cover the need), the unused private `_build_table_rows`/
  `_build_table_columns` builders, and the commented-out `_select_pagesize`. The
  `coldata` docstring drops the never-implemented `maxwidth` setting.

**Why.** `Tableview` was the only shipped widget not reachable as `ttk.<Name>`,
and it carried two methods that could never succeed plus a stdout `print` in
library code. These are cheap, unambiguous fixes; the larger method-verb
normalization is intentionally deferred so names and docs move together.

**Migration.**
- `delete_column(cid=...)` and `Tableview` header right-click "delete column" now
  work where they previously raised — no caller change needed.
- If you relied on `insert_row([])` silently no-op'ing, guard the empty case
  yourself or stop calling it with empty values.

**Not breaking.** All established `Tableview` method names are unchanged. The
`get_date`-style verb rename (`move_row_down`→`move_selected_row_down`,
`hide/unhide`→`show/hide`, `coldata`/`rowdata` aliases) is a separate, later slice
with deprecated aliases.

## Theme-aware widget icons: `apply_icon` + `icon=`/`icon_size=`  *(additive)*

**What.** New public surface for putting a theme-aware Bootstrap Icons glyph on a
widget (design `development/2_0_icon_theme_awareness_design.md`):

- `ttk.apply_icon(widget, name, *, size=14, states=None, compound=None)` — renders
  the glyph following the widget's style `foreground` (so it inverts on
  outline/toggle, mutes when disabled) and re-renders on `<<ThemeChanged>>`.
- `icon=`/`icon_size=` keyword sugar on every blessed ttk widget (`BootMixin`) —
  routes to `apply_icon` after the base style resolves.
- Supported on label-image widgets (`Button`/`Label`/`Menubutton`/`Checkbutton`/
  `Radiobutton`); other classes raise `TypeError`.

**Why.** A bare `Icon(...)` used as `image=` bakes its color once and goes stale on
a theme switch — style-delivered icons (builder recipes) were theme-aware, inline
ones were not. This completes the `Icon` feature's theme story.

**The one thing to know (implicit style generation).** `icon=`/`apply_icon`
*augments the widget's style*: it gives the widget a derived, content-hashed style
`Icon<hash>.<your style>` that **inherits** your `bootstyle`/`style` (config, map,
and layout) and adds the glyph. So **`widget.cget("style")` changes** to the
derived name. `bootstyle` and `icon` compose and re-derive together; `icon=None`
restores the base style. The static `Icon(...)` escape hatch is unchanged (a raw
`-image`, no style, not themed).

**Not breaking.** Purely additive; no existing signature changed. First-party: the
datepicker header carets were migrated onto `apply_icon` (internal, no API change).

## Tableview pagination: glyph nav buttons + boundary-disable  *(behavior)*

**What.** The five `Tableview` pagination controls (first/prev/next/last + reset)
change from character symbols (`« ‹ › » ⎌`, styled `symbol.Link.TButton`) to
Bootstrap Icons glyphs on a `ghost` base via the `icon=` sugar
(`chevron-bar-left`/`chevron-left`/`chevron-right`/`chevron-bar-right` +
`arrow-counterclockwise`). The four **nav** buttons now **disable at the page
boundaries** — first/prev on page one, next/last on the last page — driven from
`load_table_data` (the single funnel that refreshes the page index/limit). The
searchable-but-unpaginated reset button gets the same glyph for consistency.

**Why.** The character symbols were font-dependent and visually inconsistent with
the rest of the 2.0 glyph-based indicators; the nav buttons previously stayed
enabled at the boundaries (a click there was a silent no-op), so there was no
affordance for "no further pages." Ghost + disabled foreground mutes the glyph, so
the boundary state now reads.

**Not breaking (API).** No public signature changed; `goto_first_page`/
`goto_last_page`/`goto_next_page`/`goto_prev_page` are unchanged. A programmatic
caller can still invoke them at a boundary (they were already guarded no-ops); only
the button's interactive `state` reflects the boundary now.

## Meter: snake_case options, DoubleVar values, `value` property  *(breaking + additive)*

**What.** The `Meter` widget's API was normalized (widget-review PR 2):
- **All 18 authored options renamed to snake_case** — `amountused`→`amount_used`,
  `metersize`→`meter_size`, `metertype`→`meter_type`, `meterthickness`→
  `meter_thickness`, `amountmin`/`amounttotal`→`amount_min`/`amount_total`,
  `amountformat`→`amount_format`, `arcrange`/`arcoffset`→`arc_range`/`arc_offset`,
  `wedgesize`→`wedge_size`, `showtext`→`show_text`, `stripethickness`→
  `stripe_thickness`, `textleft`/`textright`→`text_left`/`text_right`,
  `textfont`→`text_font`, `subtextstyle`→`subtext_style`, `subtextfont`→
  `subtext_font`, `stepsize`→`step_size`. (`subtext`, `interactive`, `bootstyle`
  unchanged.) Applies to constructor kwargs **and** `configure`/`cget`/item access.
- **Public attributes renamed**: `amountusedvar`→`amount_used_var`,
  `amounttotalvar`→`amount_total_var`, `amountminvar`→`amount_min_var`,
  `amountuseddisplayvar`→`amount_used_display_var`, `labelvar`→`label_var`,
  `meterframe`→`meter_frame`, `textframe`→`text_frame`.
- **Constructor is keyword-only** after `master`.
- **Values are `DoubleVar`-backed** (was `IntVar`): fractional `amount_used` and
  fractional `amount_format` (e.g. `"{:.1f}"`) are now honored instead of truncated.
- New canonical **`value`** property (get/set) as the uniform value handle
  (`amount_used` remains a synonym).

**Migration.** All old option and attribute spellings are accepted through 2.x with
a `DeprecationWarning` naming the new form (via `style/_compat.py`), removed in 3.0.
The keyword-only constructor and the `IntVar`→`DoubleVar` change cannot be shimmed:
pass options by keyword (already the norm), and expect floats back from
`amount_used`/`value` where you previously got ints.

**Fixes bundled.** `cget(...)` now works for every option (was absent);
`amount_format` is reconfigurable (was construction-only); `configure(meter_size=…)`
no longer double-scales on a round-trip; a `subtext_style` change now recolors the
left/right labels too; the dead `<<Configure>>` bind was removed.

---

## DateEntry: snake_case (cross-layer), live-text read, string `state`  *(breaking + additive)*

**What.** The `DateEntry` widget's API was normalized (widget-review PR 3), and the
rename was coordinated across the date-picker dialog layer:
- **Authored options renamed to snake_case** — `dateformat`→`date_format`,
  `firstweekday`→`first_weekday`, `startdate`→`start_date`. Applies to constructor
  kwargs **and** `configure`/`cget`/item access. The **same rename lands on
  `Querybox.get_date` and `DatePickerDialog`**, which carried the old
  `firstweekday`/`startdate` keyword names.
- **Constructor is keyword-only** after `master`.
- **`configure(cnf="state")` / `cget("state")` now return a plain state string**
  (the entry's state), not the old `{"Entry": …, "Button": …}` dict. Setting
  `state=` still fans out to the entry (and the button for `normal`/`disabled`).
- **`get_date()` / the new `value` property read the live entry text**, so typed
  keyboard edits are honored (previously the stored shadow date was returned and
  manual edits were silently ignored). Empty/unparseable text falls back to the last
  set date. `get_date` return type is now `Optional[datetime]`.
- The read-only **`dateformat` property was removed** — the format is an option, read
  it via `cget("date_format")` (the legacy `dateformat` spelling still resolves there
  with a warning). New canonical **`value`** property (get/set); `get_date`/`set_date`
  remain as date-typed synonyms.
- On unparseable text the entry is flagged **`invalid`** on blur (`<FocusOut>`).
- New **`position=`** passthrough to the picker popup.

**Migration.** The old `dateformat`/`firstweekday`/`startdate` spellings are accepted
through 2.x with a `DeprecationWarning` naming the new form (via `style/_compat.py`),
on the widget **and** the dialog layer; removed in 3.0. The keyword-only constructor,
the `state` dict→string change, and the removed `dateformat` property cannot be
shimmed: pass options by keyword; read `state`/format via `cget(...)`; and if you
relied on `get_date()` returning the shadow, note it now reflects the live text.

**Fixes bundled.** `cget(...)` works for every custom option (via the shared
`ConfigureDelegationMixin`); `width` is applied to the entry only (was double-applied
to the frame and entry); `date_format` reconfigure now re-validates and re-renders;
a picker re-entrancy guard prevents a second popup while one is open; unknown keyword
arguments to `Querybox.get_date`/`DatePickerDialog` now raise `TypeError` (typos fail
loudly instead of being swallowed).

---

## Floodgauge: DoubleVar value, `start(interval)`, live mode/orient  *(breaking + additive)*

**What.** The canvas-based `Floodgauge` widget was normalized (widget-review PR 4).
Its options mirror `ttk.Progressbar` and are **not** renamed; the changes are
contract/behavior:

*Breaking:*
- **Value backing is now `DoubleVar`** (was `IntVar`), matching `ttk.Progressbar`.
  `value` / `cget("value")` / the new `value` property return **float**, and
  `configure(value=33.3)` is honored instead of truncated. An externally supplied
  `variable=IntVar(...)` still binds.
- **`start()` realigned to `ttk.Progressbar.start(interval)`.** The canonical
  signature is now `start(interval=None)`; a single positional is the *interval*
  (previously it was the step size). The per-mode step size is now an internal
  default. Unknown keyword arguments raise `TypeError`.

*Deprecated (works through 2.x, removed in 3.0):*
- The pre-2.0 **`start(step_size, interval)`** call shape — two positionals, or a
  `step_size=` keyword — is accepted with a `DeprecationWarning` (via
  `style/_compat.normalize_floodgauge_start_args`).

*Additive:*
- New canonical **`value`** property (get/set).

**Migration.** Expect `float` back from `value`/`cget("value")` where you previously
got `int`. Update `start(step, interval)` calls to `start(interval)` (set the step
via the mode default); the old form keeps working with a warning through 2.x. A bare
`start(20)` now means *interval=20*, not *step_size=20* — this positional-meaning
change cannot be shimmed.

**Fixes bundled.** `mode` and `orient` are now **live** `configure`/`cget` options
(they were construction-only and raised `TclError`; `orient` now also swaps the
canvas width/height); `configure(opt)` returns a proper **5-tuple** spec (was a
malformed 4-tuple); `maximum=0` no longer raises `ZeroDivisionError`; a `mask` no
longer clobbers the user's `textvariable`, so **`cget("text")` returns the user's
text** rather than the masked string. `FloodgaugeLegacy` (unchanged API, 3.0-removal)
gained a `destroy()` that detaches its value/text write traces (leak parity with the
#1070 fix).

**Follow-up (property-consistency pass) — *deprecated*, not breaking.** Floodgauge's
option backing fields (`maximum`, `mode`, `orient`, `mask`, `font`, `length`,
`thickness`) are now **private**; they were bare public attributes that paralleled the
`configure`/`cget` surface (and `fg.maximum = 50` bypassed the redraw). The canonical
surface is `configure`/`cget`/item-access (or `fg.value`), but the old bare-attribute
**read and write still work through 2.x with a `DeprecationWarning`** (via `__getattr__`
/`__setattr__` — a write now routes through `configure`, so it takes effect instead of
silently shadowing). The `variable`/`textvariable` handles stay public. This aligns
Floodgauge with Meter/DateEntry — the rule is: options through `configure`/`cget` only,
properties only for the canonical `value` and genuinely-computed state.

## Scrolled: Canvas-viewport rewrite, `auto_hide`, keyword-only  *(breaking + additive)*

**What.** `ScrolledText` and `ScrolledFrame` (widget-review PR 5) were normalized,
and `ScrolledFrame` was rebuilt on a Canvas viewport.

*Breaking:*
- **Constructors are keyword-only** after `master`.
- **Options renamed to snake_case**: `autohide` → `auto_hide` (both classes),
  `scrollheight` → `scroll_height` (`ScrolledFrame`).
- **`ScrolledFrame` is internally restructured** — the content frame is now a child
  of a `Canvas` viewport inside `self.container` (grid: canvas + scrollbar). The
  public contract is preserved (`ttk.Checkbutton(sf, …)` still parents to the
  content; `sf.pack()/grid()/place()` still lay out the whole assembly;
  `sf.container` is still the outer frame for `notebook.add(...)`), but code that
  reached into the old `place()`-based internals or relied on `sf` itself being the
  Canvas-less frame may need updating.
- **`autohide_scrollbar()` now has one meaning on both classes** — it *toggles*
  auto-hide on/off (previously it *bound* enter/leave on `ScrolledText` but *toggled
  a flag* on `ScrolledFrame`).
- **`yview()` returns `(first, last)`** (delegated to the Canvas); it previously
  returned `None`.

*Deprecated (works through 2.x, removed in 3.0):*
- `autohide=` / `scrollheight=` are accepted with a `DeprecationWarning` (via
  `style/_compat.normalize_scrolled_kwargs`).
- **`ScrolledFrame.vscroll`** stays as the attribute for the scrollbar; the unified
  accessor is now `vbar` (`sf.vbar is sf.vscroll`). `ScrolledText` also exposes
  `vbar`/`hbar`.

*Additive:*
- `auto_hide` is exposed as a read-only bool **property** on both classes.

**Migration.** Rename `autohide`→`auto_hide` and `scrollheight`→`scroll_height`
(old spellings warn through 2.x). Pass options by keyword. If you read a `yview()`
result, it is now a 2-tuple.

**Fixes bundled.** The old `ScrolledFrame.destroy()` was a no-op that **leaked** the
outer container + scrollbar — `destroy()` now tears down the whole assembly (native
Canvas cascade, re-entrancy-guarded so an ancestor teardown is clean). The Canvas
supplies **native scroll fractions**, removing the `_measures` **div-by-zero** before
realize. Mousewheel scrolling moved to a **per-instance bind-tag** seam (enable/
disable by toggling the tag in `bindtags`), fixing the O(subtree) per-hover rebind and
the clobbering of app-level wheel handlers, and giving location-independent teardown
(`unbind_class` in `destroy()`); `disable_scrolling()` still survives a later hover
(regression #1064). `ScrolledText` moved to a **grid** layout, deleting `_on_configure`
and its `hbar=True, vbar=False` **AttributeError** outright; its `configure`/`cget`
and unknown-method access now delegate to the inner `Text` (via the shared
`ConfigureDelegationMixin` target hook), so `st.configure(font=…)` / `st.cget("wrap")`
round-trip. Four bare `except:` clauses were narrowed to `except tkinter.TclError`.

---

## LabeledScale + ToolTip: DoubleVar, lifecycle, `configure`/`cget`  *(breaking + additive)*

**What.** `LabeledScale` and `ToolTip` (widget-review PR 6) were normalized. No
option *renames* (both widgets' option names were already clean).

- **Constructors are keyword-only** after the first positional
  (`LabeledScale(master, *, …)`, `ToolTip(widget, *, …)`), and `compound` is now a
  real named `LabeledScale` parameter (it was only read from `**kwargs`).
- **`LabeledScale` value backing `IntVar` → `DoubleVar`** (matches Meter /
  ttk.Progressbar): fractional scales are honored, so `value` / the value label can
  now be a float. The value label is rendered with `:g` formatting, so an integer
  scale still reads as integers (`4`, not `4.0`).
- **`ToolTip` gained `configure`/`cget`** (and `tip["text"]` item access) over its
  options (`text`, `bootstyle`, `position`, `delay`, `wraplength`, `justify`,
  `image`, `padding`); a currently-visible popup is reconfigured in place. Previously
  these were only reachable by poking undocumented attributes.

**Migration.** The keyword-only constructors and the `IntVar`→`DoubleVar` change
cannot be shimmed: pass `LabeledScale`/`ToolTip` options by keyword (already the
norm), and expect a float back from `LabeledScale.value` where you previously got an
int. Nothing warns — these are source-level breaks, not deprecations.

**Fixes bundled.**
- `LabeledScale(compound="bottom")` no longer raises `TclError` (the `compound`
  option was forwarded to `ttk.Frame` before being popped) and the Frame is
  initialized **once** (was twice — an orphaned frame leaked per instance).
- `LabeledScale.destroy()` cancels its pending `after_idle` label-adjust, fixing a
  use-after-destroy `AttributeError` when the idle callback fired into a
  half-torn-down widget.
- `ToolTip` binds with `add="+"` (a second tooltip, or the user's own `<Enter>`
  handler, is no longer silently clobbered), gained a `destroy()` that unbinds those
  handlers + cancels the pending timer + drops a live popup, and **self-releases when
  its target widget is destroyed** (`<Destroy>`), fixing the orphaned-timer-into-a-
  dead-widget leak. Placement now measures the real popup size and routes through
  `internal/positioning.ensure_on_screen` (multi-monitor clamping) instead of a bare
  `except:` 200×50 guess. The embedded `__main__` demo was removed from the package
  source and a bare `except:` narrowed to `except tkinter.TclError`.

## ToastNotification: glyph icon, stack manager, keyword-only  *(breaking + additive)*

**What.** `ToastNotification` (widget-review PR 7) was normalized.

*Breaking.*
- **The `icon` parameter is now a Bootstrap-Icons glyph name** (e.g.
  `"bell-fill"`, `"info-circle-fill"`), not a raw Unicode/PUA character. It is
  rendered from the built-in icon font (theme-matched, recolorable), so it
  follows the theme instead of depending on an OS symbol font. Default is a bell
  glyph; pass `icon=""` to suppress it. The old PUA defaults (``/`◰`) are gone.
- **`iconfont` (and `icon_font`) is removed** — it was dead (the constructor
  overwrote it before it could render). Passing either is accepted through 2.x
  with a `DeprecationWarning` and ignored (removed in 3.0).
- **The constructor is keyword-only** after `title, message`.
- **A bad `position` anchor now raises `ValueError`** (was silently dropped to
  the OS default). `position` stays a 3-tuple `(x, y, anchor)`.
- **`set_geometry()` is now private (`_set_geometry` internals)** — it was public
  but always internal. `titlefont` internal attribute → `title_font`.

*Additive.*
- **Concurrent toasts no longer overlap.** Toasts anchored to the same screen
  corner are **stacked** and offset so each is fully visible; dismissing one
  **reflows** the rest to close the gap.
- **`show_toast()` returns the toast** as a dismiss handle, and a new idempotent
  **`hide()`** dismisses it programmatically (safe to call twice / before shown).
  `hide_toast()` remains as an alias.

*Fixed.*
- Every `show_toast()` used to emit a `DeprecationWarning` (it force-injected the
  legacy `overrideredirect` kwarg) — now uses the internal `override_redirect`.
- The duration timer and fade loop `after` ids are stored and cancelled on
  dismiss (they could double-fire); `self.toplevel` is reset to `None` after
  destroy; the bare `except:` in the fade is narrowed to `tkinter.TclError`.
- The withdrawn-window mismeasure (`winfo_height()==1`) is fixed by measuring the
  requested size before placing. The embedded `__main__` demo was removed and the
  `"ne = top-left"` docstring corrected (`ne` is top-**right**).

**Migration.** Replace a Unicode `icon="◰"` with a glyph name
(`icon="bell-fill"`); drop any `iconfont=`. Pass toast options by keyword. If you
called `set_geometry()` directly, don't (it is internal). Capture the return of
`show_toast()` if you want to dismiss a toast early: `t = toast.show_toast(); t.hide()`.

## Property/accessor consistency pass  *(mostly deprecated, not breaking)*

A cross-widget sweep so options live only on `configure`/`cget`/item-access and the
attribute surface stays minimal (widget/Variable handles + `value`/computed state).
Old spellings keep working through 2.x with a `DeprecationWarning` (removed in 3.0):

- **Floodgauge** — the option backing fields (`maximum`, `mode`, `orient`, `mask`,
  `font`, `length`, `thickness`) are private; the old bare-attribute read/write still
  works (deprecated) — a write now routes through `configure` (see the Floodgauge
  section above).
- **Meter** — the subtext/text-position Label handles gained collision-free names
  (`subtext_label`, `text_left_label`, `text_right_label`, `text_center_label`); the
  old `subtext`/`textleft`/`textright`/`textcenter` attributes are deprecated aliases.
  (The bare `subtext` name is now unambiguously the *option*: `cget("subtext")` →
  string; `meter.subtext_label` → the Label.)
- **DateEntry** — the pre-2.0 `dateformat` attribute is a deprecated read alias for
  `cget("date_format")`.
- **Scrolled** — `ScrolledFrame.vbar` is the vertical-scrollbar handle (matching
  `ScrolledText`); the old `vscroll` attribute is a deprecated alias.

## Tableview: method-verb rename  *(deprecated, not breaking)*

Targeted fixes to the inconsistent method verbs flagged in the API review; the old
names keep working through 2.x with a `DeprecationWarning` (removed in 3.0):

- **`move_row_down` → `move_selected_row_down`** — the other row-moves are
  `move_selected_row_up`/`move_selected_rows_to_top`/`move_selected_rows_to_bottom`;
  this one had dropped `selected`.
- **`unhide_selected_column` → `show_selected_column`** — drops the odd `unhide`
  verb (row/column objects already use `show`/`hide`).
- **`get_columns()` → the `tablecolumns` property** — `get_columns` was a documented
  duplicate of the property. (`get_column`/`get_row`/`get_rows` stay — they take
  arguments and are real accessors.)

Left as-is: the `coldata`/`rowdata` constructor params (fine as data-input names),
`configure(cnf=)` vs the objects' `configure(opt=)`, and the plural/singular split
in `move_selected_rows_to_top` vs `move_selected_row_up`.

## Tableview: glyph sort indicator  *(Visual)*

The sorted-column header now shows a Bootstrap-Icons `sort-up`/`sort-down` glyph
(rendered from the built-in icon font in the heading color, re-tinted on a theme
switch) via the heading `image=`, instead of an appended `⬆`/`⬇` ASCII character.
No API change. The glyph is drawn after the header label (ttk heading image
placement), with a small leading gap baked into the image so it doesn't butt
against the text.

## Sizegrip: recolor raster asset instead of a font glyph  *(Visual)*

The `Sizegrip` grip is now drawn from a recolorable raster asset
(`assets/elements/sizegrip.png` + the `sizegrip` manifest entry) via
`Assets.recolor`, replacing the `grip-horizontal` font glyph. The default grip
color is derived from the surface (`border(colors.bg)`). No API change.

## Tableview: header/body border + row-height restyle  *(Visual)*

The `Table.Treeview` styling was refined: **row spacing is restored to match 1.0**
— a 2.0 Treeview styling change had shrunk the effective row height to just the
text `linespace`, so `rowheight = linespace + ascent` brings the vertical space
back (it is not taller than 1.0). The header border derives from the heading
background (`border(background)`) and follows the hover color on the active
heading, and the body border derives from `inputbg` at a 1px (was 2px) width.
No API change.

## Tableview: right-click menus follow the theme  *(Visual)*

The Tableview's top-level cell/header right-click menus subclassed raw `tk.Menu`,
so they rendered in the OS palette (`SystemMenu` background, `SystemHighlight`
selection) while their own cascade submenus — built with `ttk.Menu` — were
theme-styled, giving the outer menu a mismatched look. Both menu classes now
subclass `ttk.Menu`, so background/foreground/selection match the cascades and the
active theme. No API change.

## Tableview: plain-text context-menu labels  *(Visual)*

The cell/header right-click menu labels dropped their leading decorative Unicode
symbols (`⬆`/`↑`/`🞨`/`⧨`/`⎌`/… — sort/move/align/delete markers). Those glyphs
aren't guaranteed in the platform menu font (they render as missing-box tofu on
some Linux/macOS setups), and `tk.Menu` command entries have no hover-aware image,
so a rendered icon can't track the active-row highlight. Labels are now the plain,
translatable text. No API change.

## Borderless popups get native macOS chrome  *(Visual)*

Borderless `Toplevel` popups (tooltips, and any `window_type` popup) were drawn
with a full titlebar on macOS. On aqua, `override_redirect` is a no-op — it breaks
Cocoa click handling and can crash Tk — so the borderless request had no effect and
the OS drew default window chrome, leaving a titlebar over every tooltip.

On aqua the borderless `window_type` values (`tooltip`, `splash`, `utility`,
`dock`) now map to a native macOS window class via
`::tk::unsupported::MacWindowStyle` (e.g. `tooltip` → `help`), so the popup gets a
real system shadow and rounded corners with no titlebar. The call is applied on the
freshly-created, never-mapped window (Tk ignores it after the first event-loop
trip) and, living in Tk's `unsupported` namespace, is wrapped in `try/except` and
falls back to the previous default chrome when unavailable. Windows/Linux behavior
is unchanged (`window_type` still resolves to `-type` on X11). Mechanism ported
from bootstack (`_runtime/toplevel.py`); no API change. No effect off macOS.

## `card` / `highlight` frame variants  *(New)*

**What.** Two new frame style variants (internal `bootstyle` modifiers, so they
route through the resolver but are not advertised in the public reference):
`card` — a simple inert 1px-bordered surface — and `highlight` — the same border
but state-mapped so it brightens to the accent while the frame is in the `focus`
state (a focus ring). Apply `highlight` once and toggle `frame.state(["focus"])`.

**Why.** Composite widgets need a container that owns a single border so their
contents sit inside one frame instead of each child drawing its own edge, and a
focus-tracked version so the whole box can light up when its content is focused.
ScrolledText is the first consumer. Border drawn with `relief=SOLID` +
`bordercolor` (bootstack's card idiom); a ttk frame reserves inset space from its
*widget* `padding`, not the style's, so consumers give the frame a little padding
so children don't paint over the border.

## `Text` border left to the tk default  *(Visual)*

**What.** `StyleBuilderTK.update_text_style` no longer imposes a border on `tk.Text`
(the `highlightthickness`/`highlightbackground`/`highlightcolor`/`relief` settings
were removed); only the colors + `insertwidth`/`padx`/`pady` are themed. A standalone
`Text` now shows tk's native border; set `highlightthickness`/`highlightbackground`
yourself for a themed one.

**Why.** So a surrounding container can own the border (see ScrolledText below).
Leaving the border to the tk default also means a one-off per-widget override is no
longer stomped by the theme walk re-imposing a border on every theme switch.

## ScrolledText: card border, focus ring, auto-hide fixes  *(Visual)*

**What.** The text and scrollbars now sit inside a single bordered `highlight`
"card" frame (the inner `Text` is kept borderless), instead of the scrollbar
sitting in a gutter outside the text's own edge. The border tracks focus (accent
ring while the text is focused, via the child's focus forwarded to the container
with `state(["focus"])`). Auto-hide was also fixed: it no longer flickers (a
`winfo_containing` guard ignores the inferior `<Leave>` crossings onto the text /
scrollbar) and no longer grows the window on hover (each scrollbar's lane is
reserved with a fixed `minsize`, so showing/hiding the bar neither resizes the
frame nor reflows the text). Scrollbars get a 1px pad at both long-axis ends so
they don't touch the container edge.

**Why.** In 1.x the scrollbar floated *inside* the text's border via `place()`; the
2.0 grid rewrite moved it to a gutter outside the border, and auto-hide toggled the
scrollbar's own grid column (flicker + window growth). Owning the border on the
container restores the "scrollbar inside the frame" look while keeping the grid
robustness. No public API change.

## Scrollbar: no trough channel, darker light-mode thumb  *(Visual)*

**What.** The default/round scrollbar trough is again the surface color (no visible
channel around the thumb), and the neutral thumb reads darker in light themes
(`shade(border, 0.25)` instead of the pale `border`), so it is clearly visible
against the near-white trough. The `thin` variant shares the same thumb color.
The unused `scrollbar_thumb` recolor asset (`scrollbar-thumb.png` + its manifest
entry) was removed — the thumb is drawn procedurally, so the asset was dead.

**Why.** The faint `border`-colored thumb on a barely-off-white trough was hard to
see in light mode; dropping the trough tint and darkening the thumb fixes the
contrast without changing the bar's size.

## Inputs: focus color shows on focus only, not hover  *(Visual)*

**What.** `Entry`, `Combobox`, and `Spinbox` no longer tint their border with the
focus color on *hover*. The `("hover !disabled", ...)` mapping was dropped from
each widget's `bordercolor` state map; the border now brightens to the focus color
(`primary`, or the colored variant) only while the widget actually holds focus.
Invalid (danger) and readonly states are unchanged.

**Why.** Lighting the focus ring on mere hover is non-standard — the ring should
signal *where keyboard input goes*, not where the pointer happens to be. Reserving
it for the real `focus` state matches conventional input behavior and removes a
distracting hover flicker when the pointer sweeps across a form.

## `card` / `highlight` frames: single hairline border (`RAISED`, bevel suppressed)  *(Visual)*

**What.** The `card` and `highlight` frame variants now draw their border with
`relief=RAISED` and `lightcolor`/`darkcolor` set to the frame background (instead
of `relief=SOLID`). Suppressing the clam bevel leaves only the `bordercolor`
hairline, at the same 1px weight the inputs draw. `highlight` additionally
state-maps `lightcolor`/`darkcolor` (not just `bordercolor`) to the accent on
`focus`, so the whole ring brightens uniformly. (Supersedes the `relief=SOLID`
mechanism noted in the `card`/`highlight` entry above.)

**Why.** The `SOLID` border read slightly heavier than the input borders it sits
next to; matching the inputs' `RAISED`-with-neutralized-bevel technique gives cards
and inputs one consistent hairline weight across the theme.

## DatePickerDialog: frameless popover; dismisses on outside click / Escape  *(Behavioral)*

**What.** `DatePickerDialog` (and therefore `Querybox.get_date` and the
`DateEntry` calendar button) now shows as a **frameless** window
(`override_redirect=True`; a no-op on macOS/aqua, where Tk keeps the chrome).
It no longer takes a modal grab: clicking anywhere outside the popup, or pressing
`Escape`, cancels the selection and closes it — in addition to the existing
"click a day to select and close". Because there is no grab, the parent window
stays interactive while the popup is open (clicking it dismisses the popup).
`show(wait_for_result=True)` still blocks the caller until the popup closes, so
`get_date` returns synchronously as before. The old titlebar `X`-to-cancel
affordance is gone (there is no titlebar); outside-click / `Escape` replace it.

**Why.** The popup was a chrome'd modal window that could open partly off-screen
and could only be cancelled via the window-manager `X`. A frameless popover that
closes on outside click is the conventional date-picker interaction and mirrors
bootstack's popover date dialog.

u## Popups: dropdown placement + on-screen clamping  *(Behavioral / bugfix)*

**What.** The date-picker popup now drops **directly below its target widget,
left-aligned** (standard dropdown placement) instead of anchoring to the target's
bottom-*right* corner. Because `DateEntry` targets its entry field, the calendar
now appears beneath the **input** rather than under the calendar button. When
there isn't room below the target on its monitor, the popup **flips to sit above**
the target (new `internal.positioning.below_widget` helper). Every placement path
— the date picker's, and the base dialog's explicit-`position` path used by
`Messagebox`/`Querybox` — is routed through `ensure_on_screen`, so a popup near a
screen edge is clamped to stay fully on its monitor instead of overflowing. The
date picker centers via `center_on_screen` (monitor under the cursor) when it has
no parent.

**Why.** Previously the date picker anchored to the parent's bottom-right corner
with a raw `+x+y` geometry and no bounds check: it dropped under the button rather
than the input, and routinely spilled past the screen edge (a target near the
bottom had nowhere to go). `Messagebox`/`Querybox` had the same off-screen gap on
an explicit `position`. Dropping below-left with an above-flip and a hard on-screen
clamp is the conventional, robust dropdown behavior (mirrors bootstack).

## DatePickerDialog: no longer mutates the global `LC_TIME` locale  *(Behavioral / bugfix)*

**What.** `DatePickerDialog.__init__` no longer calls
`locale.setlocale(locale.LC_TIME, "")`. Opening the calendar (directly, or via
`Querybox.get_date` / a `DateEntry` button) previously switched the process-wide
time locale from the ambient/C locale to the OS default as a side effect. That
desynced `DateEntry`'s `%x` round-trip — the field's text is written with
`strftime` at construction (C-locale `%x`, e.g. `07/09/26`) but was then parsed
with `strptime` under the freshly-changed OS locale (`%x` now expects a 4-digit
year), so the next button click logged a spurious *"Date entry text does not match
with date format: %x"* `UserWarning`. The date display format is now stable for
the whole session instead of flipping after the first picker open.

**Why.** The `setlocale` was both the source of that mismatch and counterproductive
for the dialog's own i18n: the calendar localizes month/weekday names through
`MessageCatalog`, keyed on the **English** `strftime("%B")` output, so it relies on
the ambient (C) locale returning English names — exactly what setting the OS locale
broke. Removing the global mutation fixes the warning and makes the calendar's month
titles localize consistently with its (already `MessageCatalog`-based) weekday
headers.

## DateEntry / DatePickerDialog: `show_outside_days` option  *(New)*

**What.** `DatePickerDialog`, `Querybox.get_date`, and `DateEntry` gained a
`show_outside_days: bool = True` option. When True (default, current behavior),
the calendar shows the leading/trailing days of the adjacent months as muted,
non-selectable labels. When False, those cells are blank so only the current
month's days are visible. On `DateEntry` it is a configure option
(`cget`/`configure("show_outside_days")`); it applies to the popup the next time
it opens.

**Why.** Additive parity with bootstack's `Calendar.show_outside_days` — some
layouts prefer a calendar that only shows the current month.

## DateEntry: `button_icon` option  *(New)*

**What.** `DateEntry` gained a `button_icon: str = "calendar-week"` option to
choose the glyph shown on the calendar button (any Bootstrap-icon name the icon
engine renders). It is a full `configure`/`cget` option: setting it live
re-renders the button glyph (theme/state-aware, via `apply_icon`).

**Why.** Additive — lets callers pick a different calendar/date glyph without
subclassing.

## DatePickerDialog / DateEntry: popup title no longer displayed  *(Behavioral)*

**What.** The calendar popup is now a frameless (override-redirect) window, so it
has no titlebar — the `DatePickerDialog(title=...)` / `Querybox.get_date(title=...)`
/ `DateEntry(popup_title=...)` text is **no longer displayed** anywhere. The
parameters are retained (accepted, stored) for API compatibility but have no
visible effect.

**Why.** Consequence of the frameless-popover redesign (see the *DatePickerDialog:
frameless popover* entry above). A borderless popup has no window chrome to render
the title in; the calendar's own month/year header remains the visible heading.

## Removed the dead `Date.TButton` calendar-button style (`date` internal modifier)  *(Internal cleanup)*

**What.** The bespoke date-button style recipe (`@register_builder("date", "button")`
→ `Date.TButton`, a button with a baked-in `calendar3` glyph image) and the
`"date"` token in `BOOTSTYLE_INTERNAL_MODIFIERS` were removed. `DateEntry`'s
button no longer uses `bootstyle="…-date"`; it is a normal button styled with the
widget's `bootstyle` and its glyph supplied by the icon engine
(`Button(icon=button_icon)`), so the dedicated style became dead code.

**Why.** The icon engine (Workstream I) now renders the calendar glyph on an
ordinary button, making a separate image-baking button recipe redundant. `"date"`
was an internal-only modifier (undocumented, never in the public `BootStyle`
Literal), so its removal is not a public-grammar change and needed no reference
regeneration.

**Impact.** Internal only. `bootstyle="date"` / `"…-date"` was never a documented
form; it now tokenizes as an unknown token (warns by default, raises under strict
mode) like any other retired keyword.

## App icon: multi-resolution `.ico` on Windows, PNG on macOS/Linux  *(New / behavioral)*

**What.** The default `Window` brand icon is now applied per-platform, mirroring
bootstack: **Windows** uses a multi-resolution `assets/app_icons/ttkbootstrap.ico`
via `wm_iconbitmap`; **macOS/Linux** use `assets/app_icons/ttkbootstrap.png` (the
512px render) via `iconphoto`. It falls back to the embedded base64
`_DEFAULT_ICON_DATA` if the packaged asset can't be found, so the icon is always
set. New build script `tools/make_app_ico.py` reads the per-size source PNGs from
the repo-root `assets/app_icons/` (`16x16.png`..`512x512.png`) and writes the two
shipped runtime assets into `src/ttkbootstrap/assets/app_icons/`: `ttkbootstrap.ico`
(Pillow `save(format="ICO", sizes=..., append_images=...)`) and `ttkbootstrap.png`.
Only those two are packaged; the source PNGs are build inputs, not shipped.

**Why.** The previous default was a single low-resolution embedded PNG, so the
titlebar/taskbar icon looked soft at larger sizes. A packed `.ico` lets Windows
pick the crisp frame per DPI/context; macOS/Linux take a full-size PNG. Rebuild
the `.ico` with `python tools/make_app_ico.py` after changing the source PNGs.

---

## Fluent geometry — `pack`/`grid`/`place` return the widget  *(New)*

**What.** On ttkbootstrap's widgets the geometry managers now return the widget
instead of `None`, so a widget can be created and placed in one expression:

```python
btn = ttk.Button(root, text="Save", bootstyle="success").pack(padx=10, pady=10)
```

Both the short names (`pack`/`grid`/`place`) and the `*_configure` spellings
return `self`. Additive and backwards compatible — tkinter's managers returned
`None`, which nothing consumed, so returning `self` only *adds* a usable value;
existing `w.pack()` calls are unaffected.

**Why.** The common construct-then-place pattern otherwise costs two statements
(and a name binding) even for throwaway widgets. Returning `self` collapses it
to one line without changing semantics.

**Scope.** Delivered by a new `FluentGeometryMixin` shared by `BootMixin` (ttk)
and `AutoStyleMixin` (tk), so every shipped widget and anything wrapped with
`bootify()` gets it by default. A raw `tk`/`ttk` widget constructed directly
does not — same scoping as the rest of the `bootstyle` API. `FluentGeometryMixin`
is re-exported from `ttkbootstrap` and `ttkbootstrap.style` for custom subclasses.

**Global opt-in.** `enable_global_api()` now also patches tkinter's shared
`Pack`/`Grid`/`Place` mixins, so `pack`/`grid`/`place` return the widget on
*stock, native, and third-party* widgets too — consistent with how the global
`bootstyle` patch already works. Importing ttkbootstrap stays side-effect-free;
the geometry patch only happens when you explicitly opt in.

---

## `TkLabel` blessed tk.Label + ColorChooser default-mode fix  *(New / Fix)*

**What.** Added `ttk.TkLabel` — a blessed `AutoStyleMixin` subclass of
`tkinter.Label` (mirroring the existing `TkFrame`), re-exported from
`ttkbootstrap`. Like the other blessed tk widgets it accepts `autostyle=` and,
with `autostyle=False`, opts out of theming entirely (keeps its explicit
colors). Used it to fix a **ColorChooser** crash.

**Why (the bug).** `ColorChooser` built its color swatches and preview panels
from *native* `tkinter.Frame`/`tkinter.Label` passed `autostyle=False`. But
`autostyle` is a ttkbootstrap concept — stock tkinter rejects `-autostyle`
unless `enable_global_api()` has patched the tk constructors. Since 2.0 no
longer monkey-patches at import (PR 3), opening the color chooser in the default
configuration raised `TclError: unknown option "-autostyle"`. The swatches use
`autostyle=False` deliberately (they must show literal colors the theme must not
repaint), so the fix is to build them from the blessed `TkFrame`/`TkLabel`,
which honor `autostyle=` in both modes. A second latent break in the same dialog
was fixed too: `create_buttonbox` called `ToolTip(widget, text)` positionally,
but `ToolTip` became keyword-only in the #1114 normalization.

**Migration.** None. `ColorChooser`/`ColorChooserDialog` (and `Querybox.get_color`)
now work without `enable_global_api()`. `ttk.TkLabel` is available for any tk
label that must carry explicit, un-themed colors.

---

## Public utilities re-exported at the top level + `windowing_system`  *(New)*

**What.** The public utility helpers are now reachable directly on the package,
the same way widgets and dialogs are (`ttk.<name>`), instead of only via their
submodules:

- from `ttkbootstrap.utility`: `enable_high_dpi_awareness`, `scale_size`, and a
  **new** `windowing_system(widget)` helper (returns `'win32'`/`'aqua'`/`'x11'`).
- from `ttkbootstrap.colorutils`: `color_to_rgb`, `color_to_hex`, `color_to_hsl`,
  `update_hsl_value`, `contrast_color`, `conform_color_model`.

`windowing_system(widget)` wraps `widget.tk.call('tk', 'windowingsystem')` and
now backs the ~8 first-party sites that previously repeated that raw Tcl call
(`window.py`, `dialogs/base.py`, `dialogs/datepicker.py`, `widgets/toast.py`,
`widgets/tableview.py`, `widgets/scrolled.py`). `style/scaling.py` keeps its own
leaf `windowing_system` property (it sits in the early style-init path, so it
stays free of a cross-package import).

**Why.** These are documented public helpers, but reaching them meant knowing the
submodule path (`from ttkbootstrap.utility import scale_size`). Surfacing them on
the top-level namespace matches how the rest of the public API is exposed and
makes `ttk.scale_size(...)` / `ttk.contrast_color(...)` "just work". The
`windowing_system` helper also gives platform checks one spelling instead of a
scattered raw Tcl call. `colorutils` gained an `__all__` so its public surface is
explicit.

**Migration.** None — purely additive. The `ttkbootstrap.utility` /
`ttkbootstrap.colorutils` import paths remain valid.

---

## Control-height parity + check/radio/menubutton focus rings  *(Visual)*

**What.** Two related visual fixes to the interactive controls:

- **Height parity.** Buttons, toolbuttons, and menubuttons rendered 2px taller
  than the text inputs (31 vs 29px at 100%). The button/toolbutton/menubutton
  vertical padding is trimmed by 1px per side so every control — `Button`,
  `Menubutton`, `Toolbutton`, `Entry`, `Combobox`, `Spinbox` — is the same
  height again, matching 1.x (where they were all ~29).
- **Focus rings everywhere in the button family.** `Checkbutton`, `Radiobutton`,
  `Menubutton`, and the toggle/switch styles (`toggle`/`round-toggle`/
  `square-toggle`) had **no** keyboard-focus ring; `Button`/`Toolbutton` already
  did. They now all draw the same 1px `focuscolor` ring on focus (the ring hugs
  the label and does not change the indicator-driven check/radio/switch height).

**Why.** The +2px on buttons was an unintended side effect of the 2.0 button
restyle adding a `focusthickness=1` focus ring (which reserves 1px per side) on
top of the existing padding; nothing compensated for it, so buttons grew. The
fix keeps the accessibility win (a visible focus ring) and restores the height by
absorbing the ring into the padding. Adding the missing rings to
check/radio/menubutton makes keyboard focus visible and consistent across the
whole family.

**Scope.** `style/builders/{button,toolbutton,menubutton}.py` (padding
`(…,5,…)` → `(…,4,…)`; menubutton `focusthickness` 0 → 1) and
`style/builders/{checkbutton,radiobutton,toggle}.py` (add
`focuscolor`/`focusthickness` + a disabled `focuscolor` map; the toggle layouts
also gain a `Toolbutton.focus` wrapper around the label, which they lacked).
Inputs are unchanged (they signal focus with a border-color highlight, not a
ring — see "Inputs: focus color on focus only").

**Migration.** None (appearance only).
