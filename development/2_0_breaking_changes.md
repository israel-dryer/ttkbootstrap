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
| Canonical `bootstyle` grammar (closed vocab, strict mode) | API | `development/2_0_bootstyle_grammar_design.md` |
| Character-based icons removed (`ttkbootstrap.icons`) | API | `development/2_0_icon_drop_design.md` (PR #1094) |
| Delivery API (mixins, no import-time monkey-patch) | API | handoff / PR #1075 |
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

## Sizegrip: recolor raster asset instead of a font glyph  *(Visual)*

The `Sizegrip` grip is now drawn from a recolorable raster asset
(`assets/elements/sizegrip.png` + the `sizegrip` manifest entry) via
`Assets.recolor`, replacing the `grip-horizontal` font glyph. The default grip
color is derived from the surface (`border(colors.bg)`). No API change.
