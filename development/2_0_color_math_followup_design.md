# 2.0 — Fast-follow color-math PR (`elevate` + `input_bg`)

> **STATUS: DESIGN STUB — NOT YET APPROVED.** Per the hard rule (see
> `CLAUDE.md` / handoff), this PR does **not** start as ad-hoc coding. Hold the
> design discussion, settle the open decision below, get user sign-off, then
> implement. This file captures the scope carried over from the color-helper
> design's fast-follow section so the next session starts from the right place.

## Context

The color-helper PR (#1085, merged into `2.0`) added the private 50–950 ramps
and the five `StyleBuilderTTK` helpers (`active`, `pressed`, `border`,
`disabled`, `on_color`). It deliberately **left 10 ad-hoc HSV/alpha color-math
sites in place**, guarded by an exact AST allowlist, because they are
specialized surface/mute effects rather than state-color derivation. This
fast-follow retires those sites onto two mode-aware utilities built on the
private `_mix` / `_relative_luminance` primitives.

Prereq reading: `development/2_0_color_helpers_design.md` (esp. its fast-follow
section) and the handoff's "Fast-follow scoped" block.

## Proposed surface

### `elevate(surface, level)` — mode-aware surface raise
Built on `_mix` / `_relative_luminance`. Replaces the 5 inconsistent
trough/track `update_hsv` sites and folds the 4 `make_transparent(0.4, …)`
unchecked-indicator muting sites onto `_mix` (must stay visually identical):

- `label.py` — trough darken 20%
- `progressbar.py` (×2) — trough darken 20%
- `scale.py` — track darken 20%
- `floodgauge.py` — lightens 80% (the odd one out — confirm direction under
  `elevate`'s mode-aware model)
- 4× `make_transparent(0.4, …)` unchecked-indicator mute sites → `_mix`
- One stripe site (`progressbar.py:40`) may want a `tint` rather than `elevate`
  — decide during the design pass.

### `input_bg(surface=None)` — mode-aware field background policy
Built on `elevate`. Encodes "fill vs outline are substitutes, use one per mode":

- **light:** `= bg` (border carries the affordance)
- **dark:** `= elevate(bg)` (fill carries it; border ≈ bg)

## OPEN DECISION (settle first)

Does `input_bg` **derive** `inputbg` (dropping the hand-authored, inconsistent
per-theme dark deltas), or **coexist** with them?

- The **derive** path needs the deferred built-in theme-dict conversion
  (Workstream E) — so deriving here may pull E's scope forward or block on it.
- The **coexist** path keeps the authored deltas and only routes *new* uses
  through `input_bg`.

Recommendation to bring to the design discussion: **coexist** for this PR (keep
it self-contained, no E dependency), and fold the derive path into E when the
theme-dict conversion lands. Confirm with user.

## Constraints / guardrails (carry from color-helper PR)

- `StyleBuilderTK` (legacy tk) stays out of scope.
- Keep the AST allowlist mechanism; shrink it as sites migrate. New direct
  `Colors.update_hsv` / `Colors.make_transparent` in ttk recipes must still fail
  the guard unless allowlisted with a reason.
- Behavior-preserving: the mute sites must be **visually identical**; the
  trough/track sites are allowed normalized drift (2.0 plan permits it) but
  should be reviewed light↔dark.
- Carry the **PEP 649 annotation force-evaluation sweep** (3.14 gotcha) over any
  new/moved module.

## Gates

- Focused unit tests for `elevate` / `input_bg` (mode-aware direction, exact
  deltas, mute-equivalence to the old `make_transparent(0.4)` output).
- Full headless suite green (expected baseline on `2.0`: **189 passed** / 1 known
  Tcl `nl.msg` env failure).
- **Human visual gate** light↔dark across the affected widgets
  (troughs/tracks/stripes, unchecked indicators, input fields) — the headless
  suite asserts color-at-pixel, not appearance. Extend or reuse
  `examples/color_states_preview.py`.

## Next steps for the implementing session

1. Hold the design discussion; settle the open decision; get sign-off.
2. Flesh this doc into the full design (signatures, mix ratios, mode detection).
3. Cut a branch from `2.0`; implement PR-by-PR per the doc.
4. Run automated + human gates; open the PR against `2.0`; update the handoff.