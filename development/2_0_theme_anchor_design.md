# ttkbootstrap 2.0 — Workstream E: semantic-anchor theme model

**Status:** design pass approved; **PR E1 merged**; **PR E2 implemented + green,
awaiting the human visual gate** (§8). E3 not started.
**Branch:** E2 on `refactor/2.0-pr-e2-theme-model` (from `2.0`).
**Date:** 2026-07-06.

> **PR E2 — IMPLEMENTED, GATE PENDING.** `Theme` semantic-anchor model +
> schema→16-key derivation in `style/theme.py`; curated 15-family catalog
> (`themes/builtin.py`, 30 light/dark themes); legacy 16-key adapter + opt-in
> `install_legacy_themes()` (`themes/legacy.py`); `_load_themes` registers the
> curated catalog; default theme `bootstrap-light`; helpful `TclError` for
> legacy names pre-opt-in; `Theme`/`install_legacy_themes` re-exported. The
> deferred hue-correct `inputbg` fix is in and regression-tested. **`selectbg`
> correction** (§2 #9): reverted from `primary` to neutral after a visual check
> found the accent bleeding into dark troughs/borders (builders reuse `selectbg`
> as a neutral surface). Non-localization suite **210 passed** (+25 over E1's
> 201: 15 in `test_theme_anchor.py` + the E1 10; localization passes in
> isolation, order-dependent `nl.msg` env failure otherwise); warning-free
> import; standalone module imports; PEP 649 sweep (6 modules) clean;
> `examples/color_states_preview.py` sweeps all 30 curated themes. **Merge is
> gated on the six-theme (now full-catalog) human visual review.**

> **PR E1 — DONE** (branch `refactor/2.0-pr-e1-colors-ramp`, PR open against
> `2.0`). `Colors` is now a resolved view:
> each field is a `RampColor` (a `str` subclass, drop-in everywhere, additionally
> `c.primary[300]`-addressable) and `Colors.ramp(label)` returns the full 50-950
> mapping. `RampColor` re-exported from `ttkbootstrap.style`. No catalog/visual
> change. New `tests/widget_styles/test_theme_ramp.py` (10 tests). Suite **201
> passed** (191 + 10); warning-free import + standalone `style.theme` import
> clean. Only int keys that are ramp stops (50-950 step 50) are intercepted;
> ordinary str indexing/slicing falls through untouched.

Pairs with `development/2_0_plan.md` (§E, §F) and `development/2_0_handoff.md`.
This is the design pass required by the hard rule before any Workstream-E coding.

---

## 1. Goal

Replace the flat 16-key per-theme dict with a **semantic-anchor `Theme`
family**: declare the accent colors once (as `[500]` ramp anchors) plus a
`light`/`dark` background block, and generate a well-contrasted light **and**
dark variant from one declaration. The generator fixes today's hand-authored
contrast/consistency bugs (inconsistent `border`/`inputbg`/`selectbg`, sub-AA
on-colors) by *deriving* the plumbing instead of authoring it per theme.

The **mechanism is ported from bootstack** (`bootstack/src/bootstack/style/
theme.py`, `theme_provider.py`) — the same author, and ttkbootstrap already
carries the matching ramp math from the color-helper PR (`style/theme.py`
`_color_ramp`, `_mix_colors`, `_tint`/`_shade`, `_darken_color`/`_lighten_color`,
`_state_color`, `_accent_on_color`, luminance/contrast). We borrow the model, not
bootstack's public API or its full surface taxonomy.

---

## 2. Approved decisions (locked with user, 2026-07-06)

1. **Adopt bootstack's `Theme` family model.** One anchor set + `light=`/`dark=`
   blocks → `<name>-light` + `<name>-dark`. Per-mode ramp-step selection gives
   contrast in both modes with no per-mode shade authoring.
2. **`Colors` becomes a resolved view** keeping all 16 current attrs
   (`c.primary`, `c.bg`, `c.get(...)`, …) **and** gaining ramp addressing
   (`c.primary[300]`). Backward-compatible.
3. **Curated default catalog** (~15 families → ~30 light/dark themes), not a
   mechanical port of all ~18 built-ins. Membership in §5.
4. **`install_legacy_themes()`** — opt-in call that registers the old theme
   names, each re-expressed through the new generator. **Fidelity: keep each old
   theme's authored accents + bg/fg exact; regenerate only the plumbing**
   (`border`/`inputbg`/`selectbg`/`active`/on-colors). Preserves recognizability,
   fixes the contrast bugs, and stays a thin adapter (Workstream-F discipline).
5. **Raw 16-key dict stays an accepted input** (`ttkcreator`, `USER_THEMES`,
   `load_user_themes(json)`) via the same adapter — never a parallel engine.
6. **Minimal surface layer.** Derive only `bg/inputbg/selectbg/border/active`
   (+ their on-colors). Do **not** import bootstack's chrome/content/card/
   overlay/raised taxonomy — ttk does not need it.
7. **Plumbing is derived, not authored, for the curated set** (this is where the
   deferred `inputbg` fix lands).

### E2-kickoff forks (locked 2026-07-06)

8. **Default theme = `bootstrap-light`** (was `litera`, which folds into the
   bootstrap family; `litera` reachable via `install_legacy_themes()`).
9. **`selectbg = neutral`** for the curated set (from the neutral ramp,
   `_SECONDARY_STOP` step); `selectfg = _accent_on_color(selectbg)`. Legacy
   themes keep their authored `selectbg`.
   **Correction (2026-07-06):** the kickoff pick of `selectbg = primary` was
   reverted after a visual check — the builders **reuse `selectbg` as a neutral
   surface** for dark-mode borders (`entry`/`combobox`/`notebook`/`scrollbar`/
   `labelframe`/`panedwindow`) and for scale/progress/label troughs
   (`shade(selectbg)`). An accent `selectbg` therefore bled the primary color
   into every dark trough and border. Keeping `selectbg` neutral honors E2's
   "builders untouched" rule. Accent-colored *selection* (Treeview/Entry) would
   require decoupling the true selection sites from the trough/border sites in
   the builders — a separate change, not E2.
10. **Legacy names = helpful error, no aliases.** `themename="darkly"` without
    `install_legacy_themes()` raises a `TclError` naming the fix (call
    `install_legacy_themes()` or use a 2.0 theme). No silent aliases.

---

## 3. The `Theme` model (ttkbootstrap port)

A `Theme` is a *family* declared in code. Ported from bootstack's dataclass,
trimmed to ttkbootstrap's needs (no `surfaces` taxonomy, no `display_name`
machinery beyond a label).

```python
Theme(
    name="pulse",
    primary="#593196", success="#13b955", info="#009cdc",
    warning="#efa31d", danger="#fc3939",
    secondary=None,              # optional colored secondary; else from neutral ramp
    neutral="#adb5bd",           # gray base for secondary/light/dark/border/muted
    light=dict(background="#ffffff", foreground="#17141f"),
    dark=dict(background="#17141f",  foreground="#e9ecef"),
).register()                     # registers pulse-light + pulse-dark
```

- **Accent roles** (`primary success info warning danger`) + optional
  `secondary` take a `[500]` anchor and generate a private 50–950 ramp
  (`_color_ramp`, already cached/bounded).
- `neutral` generates the gray ramp used for `secondary` (when uncolored),
  the `light`/`dark` accent keys, `border`, and muted text.
- `light`/`dark` each carry only `{background, foreground}`. A family may define
  one or both; `register()` produces a variant per defined block.
- `.register()` = ttkbootstrap's analog of bootstack's `.install()`. It builds a
  per-mode **schema** and registers it with `Style` (see §7 back-compat for how
  this coexists with `Style.register_theme(ThemeDefinition)`).
- **`Theme.from_existing(base, name=..., **overrides)`** ported for
  brand-a-builtin ergonomics (change just `primary`, inherit the rest).

`Theme` lives in `style/theme.py` alongside `Colors`/`ThemeDefinition`.

### Per-mode step tables (ported, tunable in the visual gate)

```python
_SOLID_STOP = {  # which ramp step a solid fill uses per mode
    "light": {"primary":600,"success":600,"danger":600,"info":500,"warning":500},
    "dark":  {"primary":400,"success":400,"danger":400,"info":400,"warning":400},
}
_SECONDARY_STOP = {"light": 700, "dark": 400}   # neutral step for uncolored secondary
```

Rationale (bootstack's, verified): on light a darker step reads against white; on
dark a brighter step reads against the dark bg. `warning`/`info` stay at `[500]`
on light — they carry dark on-color at any shade, so darkening only mutes them.

---

## 4. Schema → 16-key `Colors` mapping (the core of E)

`register()` generates a per-mode schema; an adapter resolves it into the 16
`Colors` fields the builders already consume. This is the whole compatibility
trick: **builders are untouched; only how `Colors` is populated changes.**

Let `mode ∈ {light, dark}`, `bg`/`fg` = the authored block, `R(role)` = the
role's 50–950 ramp, `N` = the neutral ramp. Surface derivations use the existing
hue-preserving `_darken_color`/`_lighten_color`.

| `Colors` key | Curated derivation | Notes |
|---|---|---|
| `primary` | `R(primary)[_SOLID_STOP[mode].primary]` | per-mode solid |
| `success` | `R(success)[…]` | ″ |
| `info` | `R(info)[…]` | ″ |
| `warning` | `R(warning)[…]` | ″ |
| `danger` | `R(danger)[…]` | ″ |
| `secondary` | authored `R(secondary)[…]` if given, else `N[_SECONDARY_STOP[mode]]` | |
| `light` | `N[100]` | fixed gray accent (both modes) |
| `dark` | `N[800]` | fixed gray accent (both modes) |
| `bg` | `bg` (authored) | |
| `fg` | `fg` (authored) | |
| `inputfg` | `fg` | |
| `inputbg` | light: `bg`; dark: `_lighten_color(bg, _INPUT_LIFT)` | **hue-correct — the deferred fix** |
| `border` | `_border_color(bg)` = `mix(bg, on_color(bg), 0.84)` | the **dedicated** border derivation, shared with `builder.border()`; desaturates toward the on-color (a lightness move kept saturated surfaces saturated — wrong) |
| `active` | light: `_darken_color(bg, _ACTIVE_MIX)`; dark: `_lighten_color(bg, _ACTIVE_MIX_D)` | subtle hover fill |
| `selectbg` | `N[_SECONDARY_STOP[mode]]` — **neutral**, see §4.2 | doubles as the trough/dark-border base |
| `selectfg` | `_accent_on_color(selectbg)` | reuses on-color policy |

### 4.1 Tunable constants (initial values; settle in the human visual gate)

```python
_INPUT_LIFT    = 0.03   # dark inputbg lift off bg
_BORDER_MIX    = 0.14   # light border darken
_BORDER_MIX_D  = 0.22   # dark border lighten
_ACTIVE_MIX    = 0.06   # light active/hover darken
_ACTIVE_MIX_D  = 0.09   # dark active/hover lighten
```

These are the E analog of the color-helper PR's `_ON_COLOR_*` knobs — named,
documented, and confirmed by the six-theme sweep, not guessed-and-shipped.

### 4.2 Open decision — `selectbg`

Today `selectbg` is usually the **secondary gray** (cosmo `#7e8081`). Modern
Bootstrap selection uses **primary**. Options for the doc to lock before coding:
- **(a) `selectbg = primary`** — modern, visible change to selection color
  everywhere (Treeview/listbox/text selection). Lean.
- **(b) `selectbg = secondary`** — preserves current behavior.

Recommend (a) for the curated set; **`install_legacy_themes()` keeps whatever the
legacy theme authored** (it only regenerates border/inputbg/active, per
decision 4), so legacy selection color is preserved regardless.

---

## 5. Curated default catalog (approved)

~15 families → ~30 `-light`/`-dark` themes.

| Source | Families |
|---|---|
| **From bootstack (10)** | bootstrap, pydata, nord, solarized, catppuccin, gruvbox, dracula, tokyo-night, one, everforest |
| **Migrated from ttkbootstrap (5)** | vapor, minty, pulse, united, sandstone |

The migrated five are expressed as `Theme` families: their existing accents +
bg become the light (or dark) anchors, and the **opposite** mode is generated
new (e.g. `vapor` is dark today → `vapor-light` is generated; author a light bg
block for it). Where a migrated theme has no natural opposite-mode background,
pick a neutral bg/fg pair in the family's spirit (settle in the visual gate).

Everything else (cosmo/flatly/litera/lumen/yeti/journal/simplex/cerulean/morph/
superhero/solar/cyborg) is covered by a near-equivalent (solar≈solarized,
cosmo≈bootstrap) or reachable via `install_legacy_themes()`.

---

## 6. `install_legacy_themes()` and the raw-dict adapter

```python
# style/_compat.py (or themes/legacy.py) — the ONLY place the 16-key shape is understood
def theme_from_legacy_dict(name, spec) -> ThemeDefinition:
    """Adapt a legacy {'type','colors':{16 keys}} into a resolved ThemeDefinition,
    keeping authored accents + bg/fg, regenerating border/inputbg/active/on-colors."""

def install_legacy_themes() -> None:
    """Register every legacy STANDARD_THEMES name via the adapter (opt-in)."""
```

- **Fidelity (decision 4):** accents, `bg`, `fg`, `selectbg`, `selectfg`,
  `light`, `dark` taken from the authored dict verbatim; `border`, `inputbg`,
  `active` **regenerated** by the §4 surface derivation (this is the "optimized
  as possible" part — the buggy plumbing is what we throw away). Legacy accents
  are **not** re-stepped through `_SOLID_STOP` (that would change identity).
- `USER_THEMES` and `load_user_themes(json)` route through the same adapter, so
  custom 16-key themes keep working and get the same plumbing cleanup.
- `install_legacy_themes()` is **not** called at import — opt-in, warns once that
  these names are legacy (removed/renamed guidance in the migration doc).

---

## 7. Back-compat & integration

- **`Style.register_theme(ThemeDefinition)`** stays the low-level registration
  primitive. `Theme.register()` builds per-mode `ThemeDefinition`s (whose
  `Colors` is the resolved view) and calls it — no second registry.
- **`Style._load_themes`** switches from iterating `STANDARD_THEMES` dicts to
  registering the curated `Theme` families. `STANDARD_THEMES` is retained (moved
  behind the legacy adapter) for `install_legacy_themes()`.
- **`themename="darkly"`** and friends: resolve only after
  `install_legacy_themes()`. Ship a migration note + a small alias map for the
  highest-traffic old names → nearest curated variant (e.g. `darkly` →
  `bootstrap-dark`?) — **alias list is an open item for the visual gate.**
- **`ttkcreator`** authors 16-key dicts → still valid via the adapter; a
  follow-up (Workstream H/docs) can teach it the `Theme` form.
- **Ramp addressing** (`c.primary[300]`): `Colors` gains `__getitem__`-on-attr
  or a small resolved-ramp holder. `c.primary` stays a `str` (the solid) but
  also indexable — implement as a `str` subclass carrying its ramp, or resolve
  `c.primary[300]` via a `Colors.ramp(role)` lookup. **Decision for PR E1:**
  prefer a `str` subclass (`RampColor(str)`) so `c.primary` is still a plain
  string everywhere it's used today and `c.primary[300]` works additively.

---

## 8. PR sequencing (proposed; confirm)

- **PR E1 — resolved `Colors` + ramp addressing, no catalog change.** `Colors`
  becomes a resolved view; add `RampColor`/`c.primary[300]`; keep the existing
  16-key dicts feeding it. No visual change → suite stays green, low risk.
- **PR E2 — `Theme` model + curated catalog + adapter.** Port `Theme`/schema/
  step tables; add the §4 derivation; replace `_load_themes` built-ins with the
  curated families; add `install_legacy_themes()` + raw-dict adapter. **Human
  visual gate here** (every theme shifts). Settle §4.1 knobs, §4.2 `selectbg`,
  §7 alias map, and the migrated-five opposite-mode backgrounds.
- **PR E3 — cleanup/migration doc + `ttkcreator`/`USER_THEMES` polish** as
  needed; retire any now-dead code paths.

---

## 9. Risks / open items

- **Every curated theme shifts visually** (intended; approved drift). Gate on the
  six-theme human sweep like the color PRs. Extend
  `examples/color_states_preview.py` (or a theme-gallery example) to cycle the
  full catalog light↔dark.
- **`selectbg = primary`** (§4.2) — lock before E2 coding.
- **Legacy alias map** (§7) — which old names get a courtesy alias vs a clean
  break. Lock in E2.
- **Migrated-five opposite-mode backgrounds** (§5) — need authored bg/fg for the
  mode each lacks today.
- **PEP 649 annotation sweep** — carry the 3.14 force-evaluation gate into the
  new/edited modules (per PR 4's finding).
- **`Colors.get_foreground` / `dynamic_foreground`** stay for external compat;
  the resolved view must keep them working.

---

## 10. Verification plan

- Ramp-addressing unit tests (`c.primary[300]` equals `_color_ramp` stop;
  `c.primary` still `== str`).
- Schema→Colors derivation tests: each of the 16 keys for a light and a dark
  family; `inputbg` hue-preservation (dark `inputbg` shares bg hue, is not
  desaturated toward white) — the explicit regression check for the deferred
  fix.
- `install_legacy_themes()` fidelity tests: authored accents/bg/fg preserved
  byte-for-byte; `border`/`inputbg`/`active` differ from the legacy dict.
- All 8 bootstyle color keywords resolve in every curated theme.
- Structural: warning-free import; standalone-submodule cycle guard; Python 3.10
  parse; PEP 649 force-evaluation sweep.
- Full headless suite green (record the new expected count).
- **Human visual gate** across the full curated catalog, light↔dark, before E2
  merge.
