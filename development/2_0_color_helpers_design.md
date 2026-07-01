# ttkbootstrap 2.0 — private color ramps and builder helpers

**Status:** implemented; automated gates pass, human visual gate pending  
**Branch:** `refactor/2.0-color-helpers`, from `2.0` at `c1f9ed73`  
**Date:** 2026-06-30

## Decision summary

Take a focused first slice of Workstream E without introducing the full
semantic-anchor `Theme` API. Add a bounded, module-private RGB ramp generator
and exactly five helpers to the private `StyleBuilderTTK` coordinator:

```python
builder.active(color)
builder.pressed(color)
builder.border(color)
builder.disabled(role='background', surface=None)
builder.on_color(color)
```

These replace repeated builder-local state, disabled, border, and foreground
calculations by porting bootstack's current derivation policy. They are not
public toolkit functions, do not change `Colors` construction or lookup, and do
not expose ramp indexing. Existing public color utilities remain compatible.

This is a visual normalization, not a behavior-exact refactor. Interaction
states will follow the same tint/shade direction across themes, and unsafe
accent foregrounds may change to meet a 3:1 UI-text contrast floor. Those
changes require a representative human theme sweep before merge.

## Scope and invariants

In scope:

- private Bootstrap-weight RGB ramps generated from any Tk/Pillow color;
- the five coordinator helpers above;
- migration of ttk recipes where existing math expresses those concepts;
- focused unit, style-map, cache-bound, and structural tests;
- a manual preview across representative built-in themes.

Out of scope:

- the public semantic-anchor `Theme` family API or public ramp addressing;
- conversion of the 16-key built-in theme dictionaries;
- deriving/removing the existing `Colors` fields;
- bootstyle grammar changes or public Tier-2 `state_colors()` helpers;
- removal/deprecation of existing public color utilities;
- a general color-token parser, a new dependency, or legacy `tk.*` migration.

Public imports/signatures, generated ttk style names, lazy construction,
warning-free import, image-cache purity, and the single-root test discipline
remain invariant. No ramp is stored on `Style`, `Colors`, or the Tk root.

## Current-state findings

The builders contain 29 `Colors.update_hsv` calls, 22 ttk
`Colors.make_transparent` calls, 14 ttk `Colors.get_foreground` calls, repeated
light/dark border branches, and several meanings for hover/active/pressed.

Solid buttons blend the fill into the window background at 90% for hover and
80% for pressed. That lightens states on white but darkens the same accent on a
dark surface. Date buttons and scales adjust HSV value; scrollbars use smaller
±5% changes. Warning/info fills often keep authored `selectfg` even when it is
not readable.

Not every calculation is state plumbing. Stripe highlights, floodgauge and
progress/scale trough washes, unselected check/radio/toggle muting,
theme-authored selection colors, and icon knockout colors remain explicit.

## Private ramp model

Add implementation-detail functions in `style/theme.py`:

```python
_color_ramp(color) -> mapping[int, str]
_mix(color, target, weight) -> str
_relative_luminance(color) -> float
_contrast_ratio(foreground, background) -> float
```

`_color_ramp` normalizes through `PIL.ImageColor`, treats the input as the 500
anchor, and generates 50–950 stops. It ports bootstack's current
Bootstrap-compatible RGB weights:

| Stops | Target | Target fraction |
|---|---|---:|
| 50, 100, …, 450 | white | 90%, 80%, …, 10% |
| 500 | — | anchor |
| 550, 600, …, 950 | black | 10%, 20%, …, 90% |

Mix with per-channel rounding and return lowercase `#rrggbb`. The 100-step
stops match Bootstrap 5.3; the 50-step stops are linear half steps.

Use `lru_cache(maxsize=256)` keyed by normalized anchor. Built-ins repeatedly
use a small set, while the bound prevents arbitrary custom colors from causing
process-lifetime growth. The later semantic-theme design may expose a wrapper,
but must preserve these values rather than create a second ramp engine. The five
helpers use bootstack's focused derivations; active/pressed and border are not
artificially quantized to ramp stops.

## Helper contracts

### `active(color)` and `pressed(color)`

Port bootstack's `_state_color` mechanism. Compute WCAG relative luminance;
colors below 0.5 lighten in HLS space and colors at or above 0.5 darken. Active
uses an 8% lightness delta and pressed uses 12%. These helpers are intentionally
color-luminance-aware rather than branching on theme mode: a bright fill needs
to darken and a dark fill needs to lighten in either mode.

`active` supplies hover/active ttk states. `pressed` is the stronger step for
nonterminal colors.

### `on_color(color)`

Return a readable filled-surface foreground, **white-preferred and
saturation-aware**, via `_accent_on_color(surface)`. The rule:

1. white wins whenever it clears the bold-text floor
   (`_ON_COLOR_MIN_CONTRAST = 3.0`);
2. otherwise, for a **vivid, non-warm** accent — saturation
   `>= _ON_COLOR_SAT_FLOOR` (45), hue outside the warm band (20–100°), white
   still `>= _ON_COLOR_WHITE_FLOOR` (2.3) — white is *still* chosen, because
   WCAG contrast understates white's readability there;
3. otherwise black.

The choice depends only on the fill, so it is **identical in light and dark
themes** — no mode branch.

Design note — why saturation, not just contrast: WCAG relative luminance is
**not perceptual**. It weights green ~0.72, red ~0.21, blue ~0.07, so vivid
reds/greens/blues compute as "dark" and a raw max-contrast (or plain
white-floor) rule picks *black* on them even though white reads far better —
e.g. sandstone `info` #29abe0 scores black 8.0 vs white 2.6, yet black is hard
to read on it. Saturation separates a vivid accent (white) from a light gray
(black); the warm-hue band keeps perceptually-light yellow/orange/lime
(`warning`) on black. Validated across the built-ins: exactly the vivid
cool/red accents flip to white (14 roles incl. every `success` green,
saturated `info`/`primary` blues, coral `danger`); no `warning`, pale, or gray
changes. **Accessibility tradeoff:** vivid accents can ship white text at
~2.3–3.0:1 (below AA 4.5) — a deliberate appearance/perception choice; the
strict-AA fix is palette-level (darken those accents), deferred to Workstream
E. Earlier iterations (raw max-contrast, then plain white-preferred@3.0) are
superseded; so is the original bootstack hue rule that put white on light cyan
`info`. The `secondary` grays intentionally stay black (white on a light gray
is genuinely low-contrast).

This helper deliberately supersedes `Style.dynamic_foreground` inside private
ttk recipes: readable on-colors become deterministic instead of opt-in.
`Colors.get_foreground(label)` and the public toggle remain unchanged for
external compatibility and the datepicker path. Ttk recipes use
`on_color(resolved_hex)`, keeping builder policy out of `Colors`.

### `border(color)`

Port bootstack's border derivation: mix the surface toward `on_color(surface)`
while retaining 84% of the original surface (16% on-color). There is no public
strength parameter in this focused slice. Because `on_color` is mode-aware,
border derivation is mode-aware indirectly. Theme-authored structural borders
remain where they describe the theme surface; this helper only replaces a
border derived from a specific accent/control fill.

### `disabled(role='background', surface=None)`

Port bootstack's explicit mode-aware neutral blends against `surface` (default
`colors.bg`):

| Mode | Text | Background |
|---|---|---|
| light | 35% `#6c757d` | 15% `#dee2e6` |
| dark | 25% `#adb5bd` | 20% `#495057` |

The remaining fraction is the supplied surface. Any other role raises
`ValueError`. Existing 40% blends for unchecked controls are generic muting,
not disabled state, and remain local.

## Recipe migration boundary

Migrate only calculations directly matching a helper:

- solid/default button, date button, menubutton, and toolbutton fills;
- scale and scrollbar interaction assets;
- calendar and Treeview interaction states;
- disabled values in button, menubutton, toolbutton, checkbutton, radiobutton,
  toggle, entry, combobox, spinbox, calendar, and Treeview recipes;
- filled-surface foregrounds currently using `Colors.get_foreground`;
- genuinely distinct boundaries derived from a local control/accent fill.

Do not mechanically replace every `colors.border`/`selectbg` branch or force
progress/floodgauge troughs, stripes, and unchecked indicators through these
helpers. `StyleBuilderTK` remains unchanged; legacy-tk parity can follow only
if visual review exposes a meaningful mismatch.

In particular, ttk option names do not define semantic color roles. The clam
button, menubutton, toolbutton, and calendar recipes use `bordercolor`,
`darkcolor`, and `lightcolor` regions to paint the same flat face; those values
must continue to track the face state. Entry/combobox/spinbox borders and
readonly fills are theme-authored structural colors and also remain authored.
Use `border()` only when the rendered design has a distinct derived boundary.

Add an AST guard for ttk recipes: direct `Colors.update_hsv` or
`Colors.make_transparent` calls require an allowlisted special-effect site with
a reason. This stops state-color math from spreading while retaining the
public utilities.

## Rejected alternatives

- **Public ramps now:** `colors.primary[300]` needs a resolved color object,
  legacy normalization, typing, mutation semantics, and a compatibility story.
  That is the full Workstream E/F design.
- **Copy all of bootstack:** its token parser, surfaces, subtle/emphasis,
  focus/elevation, and muted-text model belong to its widget framework.
- **Preserve every current shade:** current recipes disagree and reverse
  direction based on surface. The 2.0 plan permits normalized palette drift.
- **Unbounded memoization:** custom styles may supply arbitrary colors during a
  long process; a 256-entry cache is sufficient and bounded.

## Automated verification

1. All 19 ramp stops for black, white, gray, and representative accents.
2. Bootstrap-compatible 100-step values and monotonic luminance.
3. Named/short/long hex normalization and invalid-color failure.
4. Cache bound after more than 256 unique anchors.
5. Active/pressed HLS direction, exact 8%/12% deltas, ordering, and distinctness.
6. On-color light/dark buckets, hue bias, 3:1 floor, and black/white fallback.
7. Exact 84% border mix; all four disabled mode/role blends plus custom surface
   and invalid-role behavior.
8. Representative button, date, scale, scrollbar, Treeview,
   check/radio/toggle, and menubutton maps/assets in light and dark themes.
9. Repeated light↔dark switching: no stale assets or cache growth.
10. Structural allowlist for remaining direct HSV/alpha calculations.
11. Full suite plus warning-free import, standalone imports, Python 3.10 parse,
    and forced annotation evaluation.

The current expected suite is 177 tests. This machine may retain the documented
Tcl `tk8.6/msgs/nl.msg` failure; excluding localization must otherwise be green.

## Human visual gate

Add `examples/color_states_preview.py` covering filled/outline/link buttons,
menubutton/toolbutton, disabled and readonly input controls, check/radio/toggle,
scale, scrollbars, Treeview, and normal/disabled date buttons. Review at 100%
in `flatly`, `minty`, `morph`, `darkly`, `solar`, and `vapor`, spot-checking
primary/warning/info/light/dark variants.

Accept only if active and pressed states are ordered and visible, disabled
controls recede without disappearing, derived borders do not look heavily
outlined, and filled text/icons remain legible. Finish with light↔dark switches
to catch stale raster assets.

## Implemented sequence

1. Add private color math and pure tests.
2. Add the five coordinator helpers and tests.
3. Migrate approved recipe sites and add the special-effect allowlist.
4. Run focused/full/structural gates.
5. Run the six-theme visual gate and record approved tuning here.
6. Update the handoff and open one PR against `2.0`.

## Implementation results

- Private 50–950 ramps use bootstack's Bootstrap-compatible RGB weights and a
  bounded 256-entry cache. The returned mapping is immutable.
- `StyleBuilderTTK` now owns the five approved helpers with bootstack parity:
  luminance-directed 8%/12% HLS interaction states, mode-aware on-colors,
  84%/16% borders, and explicit light/dark disabled blends.
- Solid buttons, date buttons, menubuttons, toolbuttons, input controls,
  scale/scrollbar assets, calendar, Treeview, labels, Notebook tabs, and
  indicator disabled assets use the helpers according to their rendered color
  role. Filled disabled foregrounds use the disabled face as their surface;
  input controls use `inputbg`; the date icon has a disabled asset.
- No current clam face region was converted to `border()`: face regions track
  face colors, while authored field borders/readonly fills remain authored.
  Ten remaining direct HSV/alpha sites are special effects guarded by an exact
  AST allowlist.
- Added 12 focused tests. Corrected-audit Python 3.12 result: **188 passed / 1
  known local Tcl `nl.msg` environment failure**; excluding localization:
  **183 passed**. Focused helper suite: **12 passed**.
- Warning-free import passes; Python 3.10 parsed 91 source/test files; 255
  annotation targets across 36 style modules force-evaluated cleanly.
- `examples/color_states_preview.py` constructs and switches through all six
  representative themes without error. Human inspection remains required.

## Approved decisions

Approved by the user on 2026-06-30:

1. Keep ramps private; expose no new palette or `Colors` API in this slice.
2. Port bootstack's luminance-directed 8%/12% HLS active/pressed derivation.
3. Port bootstack's mode-aware on-color policy and 3:1 safety floor; private ttk
   recipes no longer depend on the opt-in dynamic-foreground setting.
4. Port bootstack's 84% surface / 16% on-color border mix while retaining
   theme-authored structural borders.
5. Port bootstack's explicit light/dark disabled neutral blends, resolving the
   surface from the color actually behind the disabled foreground.
6. Migrate ttk recipes only; defer legacy-tk parity and the public semantic
   theme/ramp model.
7. Keep face-painting ttk border options equal to their face color and retain
   theme-authored structural borders; option names alone do not select the
   `border()` helper.
