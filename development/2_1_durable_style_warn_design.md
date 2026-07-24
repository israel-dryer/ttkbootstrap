# ttkbootstrap 2.1 — warn when a durable style option can't take effect (design brief)

> Design brief for **#1285**: whether (and how) the durable style-options layer
> should *tell the user* when a `style.configure(...)` override it faithfully
> records and replays will nonetheless have **no visible effect**.
>
> **Status: DECISION LOCKED (author, 2026-07-24) — Option A, docs-only. No
> runtime warning.** Follows the durable-options cluster (#1279 / #1281 / #1282 /
> #1283, all merged) and its umbrella brief `2_1_durable_style_options_design.md`.
> Last item of the Phase-1 review cluster (CLAUDE.md 2.1 sequence).
>
> Grounded on 2026-07-24 against merged 2.1 by live probes (recorded in §3); the
> detectability table is measured, not assumed.
>
> **DECISION (§5 fork resolved): Option A — docs-only.** Rationale: ttkbootstrap
> wraps ttk, which wraps Tk. Whether a `configure`d option is *honored* is decided
> one or two layers below us — behavior we don't control and that shifts across Tk
> versions. Runtime detection would have to reason about that lower-layer
> behavior; a warning that is sometimes wrong about it is worse than none. §3 also
> shows the only runtime-detectable case (map-masking) is a *library* defect, best
> caught by a test (§4a), not surfaced in the user's app. So: **state the caveat
> once in the docs, detect nothing at runtime.** The user-facing inert cases
> (font, sashthickness) are already documented in `custom-styles.rst` (#1283).
> Remaining work is docs-only + an optional regression test (§7); no library API.

## 1. The promise and the failure mode

The whole point of #1238 is **"set it once and it sticks."** A user writes
`style.configure("TEntry", padding=6)` and the layer makes that value survive
every bootstyle-variant build and theme switch.

The layer is honest about *persistence* — it always records and replays the
override. But **durability ≠ the widget honoring the option.** When the target
widget never reads the option, the override is stored, replayed forever, and does
nothing, **with no signal to the user.** That is the worst failure mode for a
"set it once" feature: it looks like it worked, persists silently, and cost real
debugging time during development (the `font` case first read as a bug in the
durable layer itself).

The two Tk-limitation cases are now **documented** (#1283, *Options a widget
doesn't read* in `custom-styles.rst`). This issue asks whether the **library
should say something at runtime**, not only the docs.

## 2. The four no-op cases

| # | setting | why it does nothing |
|---|---|---|
| 1 | `font` on `TEntry` / `TCombobox` / `TSpinbox` | the widget takes its font from the widget option / named `TkTextFont`, **not the style** |
| 2 | `sashthickness` on `TPanedwindow` | `ttk::panedwindow` is a C widget that queries the literal global name `"Sash"`; the panedwindow layout has no `Sash` element to scope |
| 3 | any option a recipe `map`s for **all** states | `lookup` always resolves through the map, masking the `configure` value (the #1282 notebook-tab bug — fixed, but the shape can recur) |
| 4 | an option the widget's layout has no element for | nothing consumes it |

## 3. Key finding — what is actually *detectable*

The issue leans **option 3 (empirical detection): after replay, compare
`lookup(style, option)` to the recorded value and warn on mismatch.** Probing
each case against merged 2.1 shows this catches **only case 3**:

```
case 1  configure("TEntry", font="-size 24")        lookup -> "-size 24"   (matches)
case 2  configure("TPanedwindow", sashthickness=20) lookup -> 20           (matches)
case 3  <option mapped for all states> + configure   lookup -> map value    (MISMATCH)
case 4  configure("TEntry", rowheight=40)            lookup -> 40           (matches)
```

**Why:** in cases 1, 2, and 4 the `configure` *succeeds at the style level* —
`lookup` returns exactly what the user set. The disconnect is downstream of the
style: between the style and the widget's *rendering* (font, sashthickness) or
between the style and *nothing consuming it* (no element). `lookup` cannot see
that; it reports the style's own state, which is correct. Only case 3 leaves a
`lookup`-visible trace, because the map genuinely overrides the configured value.

**Consequence that reshapes the issue:** empirical detection catches the wrong
subset. The genuinely user-facing surprises are **cases 1 and 2** (a real person
sets a font or a sash thickness and nothing happens) — and those are exactly the
cases `lookup` comparison **cannot** catch. Case 3 is the one it *can* catch, but
case 3 is **our-bug-shaped**: it is a ttkbootstrap recipe masking a user's
`configure`, not a Tk limitation. A runtime warning for case 3 would fire in the
*user's* app about a *library* defect — the wrong place to surface it.

### Detectability matrix

| mechanism | case 1 font | case 2 sash | case 3 map-mask | case 4 no-element |
|---|---|---|---|---|
| **1. docs only** (shipped #1283) | ✅ documented | ✅ documented | — | — |
| **2. curated table** `(class, option)` | ✅ warn | ✅ warn | (n/a — library) | ✅ if listed |
| **3. empirical** `lookup ≠ recorded` | ❌ undetectable | ❌ undetectable | ✅ warn | ❌ undetectable |
| **source guard** (AST/audit, dev-time) | — | — | ✅ *prevented* | — |

(Option **4 in the issue — "strict/debug mode only" — is not a mechanism** but a
*gate*: whichever mechanism is chosen fires only under `set_bootstyle_strict` /
`TTKBOOTSTRAP_STRICT`, so normal runs stay quiet. It composes with 2 or 3.)

## 4. The real cost of each mechanism

- **Curated table (2):** the only mechanism that reaches the user-facing cases
  (font, sash). Cost: a hand-maintained `{(style-pattern, option)}` set that
  **will drift** without a sync test (the same discipline `DURABLE_STYLE_OPTIONS`
  already gets). But the *known* inert set today is tiny and closed —
  effectively `font` on the three entry-family classes and `sashthickness` on
  `TPanedwindow`. Warned once per pair.
- **Empirical (3):** self-maintaining, catches any *future* map-masking without a
  table. But it only catches the class we can already prevent at source, and adds
  a `lookup` per replay plus ttk-normalization tolerance in the compare
  (`3` → `(3,)`, `"6 5"` vs `(6, 5)`).
- **Source guard (dev-time), §4a:** the map-masking shape (case 3) is best killed
  where it is born. An **AST audit is *not* the right tool** here (checked
  2026-07-24): builder `map` values are variables / `builder`-helpers /
  `state_map`, not literals, so AST can't see the state specs, and "covers all
  states" is flag-cover reasoning, not syntax. The reliable guard is a
  **generalized runtime-`lookup` test**: for every builder-produced style,
  `configure(name, <durable option>=SENTINEL)` and assert `lookup` returns the
  sentinel (a map that masks it fails). This is exactly
  `test_notebook_tab_padding_override_takes_effect` scaled to the whole built
  surface — dev-time intent, runtime-lookup reliability, no false positives.

## 5. THE FORK (author decision)

Given §3, the issue's leaned "option 3 gated behind option 4" catches only the
map-masking class — which is our-bug-shaped and better prevented at dev-time —
and does **not** help the font/sash cases users actually hit. So the real choice
is not "which detection mechanism" but **how much runtime machinery is worth it
for a set of inert cases that is small, mostly Tk-imposed, and already
documented:**

- **A — Docs-only (close with docs).** Accept that inertness is documented
  (#1283) and rare; the user-facing cases are undetectable at runtime anyway, and
  the map-masking case is prevented at source (add the AST audit as a separate
  small test). No runtime warning. *Cheapest; honest that the important cases
  can't be auto-detected.*
- **B — Curated table, strict-gated.** Add a tiny `KNOWN_INERT_OPTIONS` table
  (the 4 known pairs), warned once per pair when the override is recorded, only
  under strict mode, with a sync/drift test. *Reaches the font/sash cases; but a
  strict-mode-only warning largely restates what #1283 already documents.*
- **C — Empirical, strict-gated.** Implement `lookup ≠ recorded` after replay,
  strict-gated. *Self-maintaining net for map-masking only; lower value than the
  issue assumed; still want the source guard regardless.*
- **D — Source guard now; defer runtime warning.** Land the map-masking AST audit
  (prevent case 3 forever), keep #1283 docs for the rest, and **defer** any
  runtime warning until there is evidence users need more than the docs. *Splits
  the cheap, high-certainty win (the audit) from the uncertain one (a warning).*

**RESOLVED — Option A (docs-only).** The author's call (2026-07-24): because we
wrap ttk/Tk, "will this option take effect" is lower-layer behavior we can't
reliably track, so the library detects nothing at runtime and the caveat lives in
the docs. The only runtime-detectable case (map-masking) is a library defect,
kept out of the user's app and guarded by the §4a lookup test instead. (Superseded
lean was "D floor + B ceiling"; the layering argument moved it to A.)

## 6. Questions — resolved

1. **Is a runtime warning wanted at all?** → **No.** Docs (#1283) plus the §4a
   regression test. (The layering argument in the Status block.)
2. Strict-gated vs dev-default warning → **moot** (no warning).
3. Warn-on-record vs warn-on-replay → **moot** (no warning).
4. Land the map-masking guard as a test? → **yes, optional but recommended** — as
   the generalized `lookup` test of §4a, **not** an AST audit (see §4a for why AST
   can't do it). It guards *our own* recipes against re-introducing the #1282
   masking shape and is independent of the layering concern.

## 7. Work to do (docs-only)

The library gets **no new API**. Two items, the first required, the second
recommended insurance:

1. **Docs (required).** The user-facing inert cases — `font` on entry/combobox/
   spinbox, `sashthickness` on a panedwindow — are already in *Options a widget
   doesn't read* (`user-guide/feature-guides/custom-styles.rst`, from #1283).
   Confirm that section states the **general** caveat plainly — *a durable
   override persists but cannot make a widget read an option it doesn't read* —
   and add that one framing sentence if it is only implied by the two examples.
   No new examples needed beyond the existing two.
2. **Regression test (recommended — DONE, author took it).** The §4a generalized
   `lookup` test: for each builder-produced style, assert a sentinel `configure`
   on `padding` (the canonical durable option and the exact one #1282 masked)
   survives `lookup` (i.e. no recipe `map` masks it). Confined to the suite; not
   shipped into user apps. Landed as
   `test_no_recipe_masks_configured_padding_across_the_built_surface`; falsified
   against an injected all-states padding map (detector fires).

**Close #1285** once the docs caveat is confirmed present (and the test landed, if
taken). No `2_1_changes.md` entry — docs + test only, no user-visible library
change.
