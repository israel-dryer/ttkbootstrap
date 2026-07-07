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
| **Button-family visual restyle (flat + hairline border)** | Visual | this doc, below |
| **Bare buttons default to `neutral`** | Visual/API | this doc, below |

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
