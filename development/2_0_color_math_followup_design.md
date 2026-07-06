# 2.0 — Fast-follow color-math PR (`shade` / `tint` / `mute`)

**Status:** IMPLEMENTED on `refactor/2.0-color-math` (from `2.0`); automated
gates pass; human visual gate pending.
**Prereq reading:** `development/2_0_color_helpers_design.md` and the handoff's
"Fast-follow scoped" block.

## Decision summary

Retire the **10 ad-hoc HSV/alpha color-math sites** the color-helper PR (#1085)
deliberately left allowlisted in the ttk recipes, moving them onto three thin
mix-based `StyleBuilderTTK` helpers built on the private `_mix_colors`
primitive. Second and final focused color-math slice before the semantic-anchor
`Theme` API (Workstream E). No public palette surface; theme dictionaries
untouched.

Two forks were opened with the user and both were re-decided against the stub
after reading ground truth (2026-07-05 → 07-06):

1. **Trough/track/stripe sites (6):** the stub proposed a mode-aware `elevate`.
   Ground truth killed that framing — the trough sites are **already
   mode-branched** and the HSV call only runs in the **dark** `else` branch
   (light themes use `colors.light`/`bg`, which are not HSV and out of scope).
   A mode-aware `elevate` would *lighten* dark-theme troughs, which is visually
   wrong (an empty track should recede darker in a dark theme). So we **retire
   the HSV onto plain mix-based `shade`/`tint`, preserving each site's current
   appearance** — still well inside the drift envelope the user approved, but
   *less* drift, no direction flip. (For gray `selectbg` — the common dark case
   — `shade` is byte-identical to the old value.)
2. **`input_bg`: DEFERRED to Workstream E** (user, 2026-07-06). In light themes
   `bg == inputbg` already, so `input_bg()=bg` is a no-op; the field affordance
   is `bordercolor=colors.border`, not the fill. In dark themes the authored
   `inputbg` deltas *carry theme hue* (vapor `#190831`→`#30115e` toward purple),
   which a uniform tint-toward-white would desaturate — a regression. A
   hue-preserving derivation needs the semantic model, so it belongs in E.

This is visual normalization, not a behavior-exact refactor. The 2.0 plan
permits trough/track drift; the muting fold is visually identical (≤1/255).

## Ground truth — the 10 sites (all in `style/builders/`)

`builders_tk.py` (legacy tk) is out of scope and outside the AST guard.

| # | Site | Old math (dark branch / effect) | Migration |
|---|---|---|---|
| 1 | `label.py` `build_meter_label_style` | `update_hsv(selectbg, vd=-0.2)` | `builder.shade(selectbg)` |
| 2 | `progressbar.py` `build_striped_progressbar_style` | `update_hsv(selectbg, vd=-0.2)` | `builder.shade(selectbg)` |
| 3 | `progressbar.py` `_create_recolored_progressbar_style` | `update_hsv(selectbg, vd=-0.2)` | `builder.shade(selectbg)` |
| 4 | `scale.py` `_create_scale_assets` | `update_hsv(selectbg, vd=-0.2)` | `builder.shade(selectbg)` |
| 5 | `floodgauge.py` `build_floodgauge_style` | `update_hsv(background, sd=-0.3, vd=0.8)` | `builder.tint(background, 0.7)` |
| 6 | `progressbar.py` `_create_striped_progressbar_assets` | `update_hsv(bar_color, sd=-0.2, vd=value_delta)` | `builder.tint(bar_color)` |
| 7 | `checkbutton.py` `build_checkbutton_style` | `make_transparent(0.4, fg, bg)` | `builder.mute(fg)` |
| 8 | `radiobutton.py` `build_radiobutton_style` | `make_transparent(0.40, fg, bg)` | `builder.mute(fg)` |
| 9 | `toggle.py` `build_round_toggle_style` | `make_transparent(0.40, fg, bg)` | `builder.mute(colors.fg)` |
| 10 | `toggle.py` `build_square_toggle_style` | `make_transparent(0.40, fg, bg)` | `builder.mute(colors.fg)` |

Sites 1–4 are byte-identical copy-paste; only the dark branch is HSV. Site 5 is
a pale wash (kept via a strong `tint`). Site 6 is a lighter highlight over the
bar; its brightness-adaptive `value_delta` block is **deleted** — mixing toward
white is self-limiting (a near-white bar barely shifts; a dark bar lifts
clearly), which is what the adaptive delta hand-rolled. Sites 7–10 are alpha
blends → `_mix_colors` (visually identical: `make_transparent` truncated,
`_mix_colors` rounds).

## New primitives (`style/theme.py`)

```python
def _tint(color, weight):   return _mix_colors('#ffffff', color, weight)  # toward white
def _shade(color, weight):  return _mix_colors('#000000', color, weight)  # toward black
```

`_mix_colors(a, b, w) = round(w·a + (1-w)·b)` per channel; `weight` is the
fraction of `a`. So `_tint`/`_shade` mix `weight` of white/black into `color`.

## New builder helpers (`StyleBuilderTTK`, `builders_ttk.py`)

Three methods, mirroring the existing five (`active`/`pressed`/`border`/
`disabled`/`on_color`). Keeping all color policy on the coordinator lets the AST
guard enforce **zero** raw `Colors.update_hsv`/`make_transparent` in recipes.

```python
_TROUGH_SHADE = 0.2   # recessed dark-theme track/trough
_STRIPE_TINT  = 0.2   # progress-stripe highlight
_MUTE_AMOUNT  = 0.4   # unchecked-indicator muting

def shade(self, color, weight=_TROUGH_SHADE):  # darken toward black
    return _shade(color, weight)

def tint(self, color, weight=_STRIPE_TINT):    # lighten toward white
    return _tint(color, weight)

def mute(self, color, surface=None, amount=_MUTE_AMOUNT):
    return _mix_colors(color, surface or self.colors.bg, amount)
```

No `elevate` and no `input_bg` in this PR (see Decision summary). The floodgauge
wash passes an explicit `0.7` weight at its single site (gate-tunable).

## AST guard

`test_direct_color_math_is_limited_to_special_effects`: `expected = Counter()`
(empty). The guard now enforces **zero** direct `Colors.update_hsv` /
`Colors.make_transparent` in every `style/builders/*.py` recipe — strictly
stronger than the old 10-entry allowlist. A future genuine special effect must
be re-added to `expected` with a reason.

## Tests (all passing)

Added to `tests/widget_styles/test_color_helpers.py`:

- `test_tint_and_shade_move_toward_white_and_black` — `_tint`/`_shade` equal the
  matching `_mix_colors` call; tint lightens / shade darkens; 0-weight no-op,
  full-weight reaches target.
- `test_shade_tint_mute_builder_helpers` (darkly) — `shade`/`tint` delegate to
  the primitives and move luminance the right way; `mute` equals
  `_mix_colors(fg, bg, 0.4)` and is within 1/255 per channel of the old
  `Colors.make_transparent(0.4, fg, bg)`.
- AST guard `expected` emptied.

Gates run: focused **14 passed**; full headless **191 passed** (189 baseline + 2
new; this Windows box has the `nl.msg` locale file, so no env failure);
warning-free `import ttkbootstrap`; PEP 649 annotation sweep over 26 changed/
dependent modules (152 targets) clean; standalone `style.theme` import; all
edited modules compile; the seven migrated recipe files shed their now-unused
`from ...theme import Colors` import.

End-to-end smoke: scale, standard/striped progressbar, floodgauge, check/radio/
round-toggle all build in darkly and flatly; `shade(#555)→#444444` (identical to
the old HSV for gray selectbg).

## Human visual gate (blocks merge)

Extend `examples/color_states_preview.py` to include: scale, standard/striped/
thin/recolored progressbars, and the ttk floodgauge. Review at 100% in
`flatly`, `minty`, `morph`, `darkly`, `solar`, `vapor`, then switch light↔dark.

Accept only if: dark-theme tracks/troughs read as recessed and distinct from
their fill; the floodgauge pale-wash trough still reads correctly; the striped
highlight is visible on light and dark bars; muted unchecked indicators are
unchanged. Tune `_TROUGH_SHADE`, `_STRIPE_TINT`, and the floodgauge `0.7` here
and record settled values in this doc + the handoff.

## Out of scope (carry to Workstream E)

- `input_bg` / field-background policy and the authored-vs-derived `inputbg`
  reconciliation; the theme-dict conversion.
- A mode-aware `elevate` / surface-elevation model (the sites that would use it
  are already mode-branched; the general model belongs to the semantic theme).
- Legacy `builders_tk.py` (tk) color math.
- Any public palette / semantic-anchor `Theme` surface.
