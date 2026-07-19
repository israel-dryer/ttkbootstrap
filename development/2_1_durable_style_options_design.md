# ttkbootstrap 2.1 — durable style options: user `configure()` that survives variants & theme switches (design brief)

> Design brief for a **durable style-options layer**: a mechanism that makes a
> user's `style.configure("TEntry", padding=3)` persist across bootstyle-variant
> builds and theme switches, instead of being silently clobbered by the recipe
> that rebuilds the style.
>
> **Status: DECISIONS LOCKED (design session 2026-07-19) — ready to implement per
> the §8 PR shape.** The umbrella design for the #1238 / #1161 / #1160 2.1 cluster
> (milestone 2.1). The three load-bearing forks were settled by the author (§10);
> the remaining items are implementation-detail leans, locked here. Pairs with
> `2_0_engine_design.md` (the version-stamped walk + lazy build) and
> `2_0_style_split_design.md` (the `style/` package this touches).
>
> Grounded against the 2.0 engine on 2026-07-19 by two code sweeps (engine
> lifecycle + the full hardcoded-write inventory); file:line refs throughout are
> from that ground truth, not memory.

## 1. Motivation & the three issues

Three open 2.1 issues are one problem wearing three hats: **builders write
hardcoded geometry values, run again per color-variant and on every theme
switch, and there is nowhere for a user's own value to survive that rebuild.**

- **#1238 (umbrella ask)** — "Set general style properties on the base style
  class." `style.configure("TEntry", padding=3)` works until you apply
  `bootstyle="danger"`, then the padding reverts.
  [discussion #536]
- **#1161** — `PanedWindow` sash thickness: `build_panedwindow_style` writes the
  **un-namespaced global `"Sash"` class** (`panedwindow.py:33-35`,
  `sashthickness=scale_size(2)`), so building *any* panedwindow variant clobbers
  a user's `configure("Sash", sashthickness=…)`, and a theme switch does too.
- **#1160** — Treeview/Tableview `rowheight` is computed from **`TkDefaultFont`**
  at build time (`treeview.py:82` and `:161`), so it ignores a font the user
  actually configured and clips tall rows. This is a *builder-reads-the-wrong-
  source* bug, only partly addressed by durable overrides (see §6).

### Why it happens (ground truth)

- Every `build_*_style` recipe runs **lazily, once per `(theme, variant, family,
  colorname)` tuple** via `StyleBuilderTTK.build_style` (`builders_ttk.py:231`).
  Each distinct variant re-runs the recipe body and re-writes every hardcoded
  value; a theme switch rebuilds under the new theme's Tcl DB, re-clobbering.
- Variants are **built from scratch by the same recipe** — `build_entry_style`
  handles both `TEntry` and `danger.TEntry`, explicitly setting
  `padding=scale_size(5)` on whichever name it's building (`entry.py:36-45`). It
  does **not** lean on ttk's dotted-name inheritance, so a user's `TEntry`
  padding never reaches `danger.TEntry`.
- **There is no existing storage** for a user's `configure()` call. `Style.configure`
  (`engine.py:147`) resolves the name and forwards to `super().configure` **once**,
  storing nothing for replay. The next `build_style` for that name overwrites it.

### The seam that makes this tractable

There is a **clean public/internal split**:

- **Users** write through the public `Style.configure(style, **opts)`
  (`engine.py:147`).
- **Builders** write through `builder.configure(...)` →
  `self.style._build_configure(...)` (`builders_ttk.py:87`) — a *different*
  method.

So the public `configure` is a user-only capture point: recording there does
**not** catch the ~200 builder writes inventoried in §9. This is the linchpin of
the whole design.

## 2. The mechanism (spine): capture + re-apply-last

Two small hooks, no new user API, `configure` just becomes durable.

**Capture.** In `Style.configure(style, **opts)`, after resolving the bootstyle
name to a ttk style name, record the options into a durable, **theme-independent**
registry before forwarding as today:

```
Style._user_options: dict[str_style_name, dict[option, value]]
```

Capture happens only on the public path, so builder writes (`_build_configure`)
are never recorded.

**Re-apply-last.** After any recipe (re)builds a style — i.e. at the tail of
`build_style` (`builders_ttk.py:231`) and after `create_default_style`
(`builders_ttk.py:306`) — re-apply the matching user overrides through the
**internal** `_build_configure` (so re-apply is not itself re-captured, and
merges on top of the freshly-built style rather than resetting it):

```
recipe writes danger.TEntry (padding=scale_size(5))   # builder
→ re-apply _user_options for danger.TEntry AND base TEntry   # user wins, last write
```

Because ttk `configure` **merges** (it does not reset unspecified options),
re-applying only the overridden keys on top of the recipe's output is correct:
the recipe's colors/other geometry stay, the user's keys win.

### Why "re-apply after every build" (not just after theme switch)

Builds are **lazy and per-variant**. A user sets `configure("Sash",
sashthickness=4)`; later a *new* `PanedWindow(bootstyle="info")` triggers
`build_panedwindow_style("info")`, which clobbers the global `Sash` again — long
after the theme switch. Only a hook at **build completion** catches this. The
registry is tiny (a handful of user overrides), so re-applying it after each
build is O(overrides) and negligible.

### Base-class → variant propagation (the "general property" in #1238)

A vanilla-ttk user expects `configure("TEntry", …)` to reach `danger.TEntry` by
dotted-name inheritance. Our recipes defeat that by setting the option explicitly
on the variant. To honor the mental model, re-apply resolves **base class then
exact name, most-specific-winning**: building `danger.TEntry` re-applies overrides
recorded for `TEntry` (the class) *and* for `danger.TEntry`. Setting the property
once on the base class fans out to every variant — exactly what "set general
properties on the base style class" asks for.

## 3. Capture immediacy & theme independence

- `configure` keeps its current behavior (apply now) **and** records — so an
  override set *after* a style is already built takes effect immediately (normal
  configure) and is remembered for future rebuilds.
- The registry stores **logical** `(style, option, value)`, theme-agnostic.
  Re-apply always writes into the *currently active* theme's Tcl DB via
  `_build_configure`, so on a theme switch the lazy rebuilds carry the overrides
  into the new theme automatically (plus a re-apply pass over the eager base
  styles from `create_default_style`).

## 4. What gets recorded — the reactivity question (KEY, §10.1)

Colors are theme-derived by design; recording a user's `configure("TButton",
background="red")` would **freeze** it across theme switches, silently defeating
adaptivity. Three postures:

- **(a) Record everything the user configures.** Simplest, most predictable
  ("what I set, stays"). A frozen color is the same documented trade as a direct
  color on a Label. Lowest maintenance.
- **(b) Geometry/layout allowlist.** Record only the override-worthy geometry
  options (§9's list: `padding`, `borderwidth`, `focusthickness`, `thickness`,
  `rowheight`, `sashthickness`, `gripcount`, `tabmargins`, `arrowsize`, `anchor`,
  `insertwidth`, …). Protects theme reactivity; a user setting an off-list option
  silently doesn't persist.
- **(c) Color denylist.** Record all except a fixed set of color options.

**LOCKED: (b) a geometry allowlist** (design session 2026-07-19). Colors stay
theme-reactive; only geometry/layout options persist. A user's `configure(...,
background=…)` applies immediately (unchanged) but is **not** recorded for replay,
so the theme's color reactivity is untouched.

**The allowlist** must cover — at minimum — every non-color option any recipe
writes, or that option stays clobbered. From the §9 sweep that is: `padding`,
`borderwidth`, `focusthickness`, `thickness`, `rowheight`, `sashthickness`,
`gripcount`, `tabmargins`, `arrowsize`, `anchor`, plus `font` (durable, not
theme-reactive; the documented `configure(".", font=…)` technique, #322) and the
common geometry a user might add (`relief`, `justify`, `insertwidth`,
`indicatormargin`, `indicatorsize`). Finalize the exact set at implementation and
**guard it with a sync test**: enumerate every non-color option written by any
recipe and assert each is in the allowlist (same spirit as the codebase's other
AST/sync guards), so a future recipe adding a geometry write can't silently escape
durability.

## 5. API surface

The spine needs **no new user API** — it makes the existing `style.configure()`
durable. That is the whole appeal. Two small optional additions (§10.3):

- `Style.reset_style_options(style=None)` — drop recorded overrides (all, or for
  one style) so the recipe default returns on the next rebuild. An escape hatch
  for "undo my override."
- Introspection (`Style.user_options` read-only view) for debugging.

Lean: ship the spine + one `reset_style_options`; defer introspection unless the
session wants it.

## 6. #1160 is a companion fix, not the same mechanism (§10.5)

The durable layer does **not** fix #1160's core. Even with overrides, a user's
`configure(".", font=big)` does not change `rowheight` — the treeview recipe
still computes it from `TkDefaultFont` at build time. The layer only helps if the
user sets `rowheight` *explicitly*.

So #1160 needs **mechanism B — builders derive font-based geometry from the
style's effective font**, mirroring the #1158 autofit fix:

```python
# treeview.py:82 / :161 — instead of font.nametofont("TkDefaultFont")
fname = builder.style.lookup(tb_ttk_style, "font") or "TkDefaultFont"
f = font.nametofont(fname)
row_height = f.metrics()["linespace"] + …
```

This handles the common case (a font set on `.`/the treeview style *before* the
widget builds). **Live** font-change → rowheight-recompute is genuinely separate
(no rebuild is triggered by a bare `configure(font=…)`); scoped out of v1 and
noted in §10.5. The general principle worth stating: *font-derived geometry reads
the effective font, never a hardcoded default.*

## 7. Interactions & correctness

- **`_build_configure` merge semantics** — ttk configure merges; re-applying only
  overridden keys is safe (§2).
- **`on_theme_change` custom-style callbacks** (`engine.py:315-321`) compose
  fine: the auto re-apply runs at build tail, independent of user callbacks.
- **`style.map(...)` overrides are out of scope for v1** (§10.4). Notebook tab
  padding is set via both `configure` and `map` (`notebook.py:53,69-72`); a user
  `configure` of tab padding persists, but the mapped-state padding is recipe-
  owned. Capturing `map` overrides is a larger, separate feature.
- **Global/un-namespaced writes** (`"Sash"`, `.` root `borderwidth`,
  `tooltip.TLabel`) are handled by the same registry — they are just style names
  with no color prefix; re-apply-all covers them without special-casing.

## 8. Suggested PR shape

- **PR 1 (the layer — #1238 + #1161):** `_user_options` registry; capture in
  `Style.configure`; re-apply-last in `build_style` + `create_default_style`;
  base→variant propagation; `reset_style_options`. Tests: entry `padding`
  survives a `danger` variant build **and** a theme switch; `Sash` `sashthickness`
  survives building another panedwindow variant and a switch; base→variant
  fan-out; reset restores the recipe default; a builder write is *not* captured
  as a user override.
- **PR 2 (font-geometry — #1160):** treeview/table-treeview `rowheight` from the
  style's effective font; tests with a tall configured font (rows not clipped),
  both `Treeview` and `Tableview`. Small, independent.
- **PR 3 (docs):** a "Persistent style options" section in the theming/custom-
  styles guide — the durability contract, base→variant fan-out, the
  color-reactivity caveat (per §10.1's outcome), and `reset_style_options`.

Moderate effort; the risk is all in §10.1 (what to record) and §10.2
(propagation semantics), not the plumbing.

## 9. Override-target inventory (from the code sweep)

Real geometry/layout override targets a user would want durable (excerpt; full
table in the sweep): `padding` (entry/combobox/spinbox/button family/notebook
tab/treeview heading/calendar), `borderwidth`, `focusthickness` (the single most-
repeated write — 18+ sites), `thickness` (progressbar/floodgauge), `rowheight`
(treeview ×2, computed), `sashthickness`+`gripcount` (global `Sash`), `tabmargins`
(notebook), `arrowsize` (scrollbar), `anchor`. **Excluded** (theme-derived, must
stay reactive): every `background`/`foreground`/`bordercolor`/`darkcolor`/
`lightcolor`/`troughcolor`/`focuscolor`/`insertcolor`/`fieldbackground` and all
`map(...)` color state lists.

Highest-risk clobbers (shared/global, one build wipes a user global): `"Sash"`
(#1161); notebook `TNotebook.Tab padding` (config + map); the `.` root
`borderwidth`. Silently-drifting *computed* geometry: both treeview `rowheight`
formulas (#1160), recolored-progressbar `thickness`, spinbox arrow-gap.

## 10. Resolved decisions (design session 2026-07-19)

**Author calls (the three load-bearing forks):**

1. **What to record → geometry allowlist.** Colors are not recorded; they stay
   theme-reactive. Allowlist spec + sync-test guard in §4.
2. **Base→variant propagation → yes, fan out.** Building a variant re-applies
   overrides recorded on its base class, most-specific-wins (exact name over base
   class). Setting a property once on the base class reaches every variant — the
   #1238 ask. §2.
3. **#1160 scope → build-time effective-font source only.** Treeview/Tableview
   `rowheight` derives from the style's effective font at build (fallback
   `TkDefaultFont`); no live font-change recompute (that tail is §11). §6.

**Implementation-detail leans (locked here; low-stakes, revisit only if
implementation surprises):**

4. **New API → spine + one `reset_style_options(style=None)`.** No introspection
   view in v1 (add later if debugging needs it). §5.
5. **`map` overrides → out of scope for v1** (configure-only). §7, §11.
6. **Re-apply granularity → re-apply the whole registry after each build.**
   Simple and cheap (the registry is a handful of entries); no per-name matching
   logic, and it covers global/un-namespaced names (`Sash`, `.`) for free. §2.
7. **Persistence scope → process-level, on the `Style` singleton.** Matches the
   current singleton model; no multi-root concern beyond the known singleton
   caveat.

## 11. Out of scope

- Capturing/replaying `style.map(...)` state overrides (v1 is `configure`-only).
- Live font-change → derived-geometry recompute (#1160 tail).
- Any new *bootstyle grammar* for geometry (that would be a value-token-style
  feature; this layer deliberately reuses vanilla `style.configure`).
- A per-widget-instance option store — this is style-level, matching ttk.
- Anything pre-2.1.
