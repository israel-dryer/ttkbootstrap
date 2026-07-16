# ttkbootstrap 2.1 — bootstyle value tokens: hex + ramp accents & surfaces (design brief)

> Design brief for extending the `bootstyle` grammar with **value tokens** —
> raw hex colors and ramp-addressed roles — in the color and surface slots.
> Author-initiated (2026-07-16), assessed feasible against the 2.0 engine.
>
> **Status: PROPOSED — tracked 2.1 enhancement (issue #1236, milestone 2.1).** 2.0 is feature-frozen; this
> is additive and backward-compatible, so it loses nothing by waiting. Per the
> project hard rule, a design session confirming §10 precedes implementation.
> Pair with `2_0_bootstyle_grammar_design.md` (the tokenizer this extends),
> `2_0_surface_color_design.md` (the `@surface` mechanism), and
> `2_0_theme_anchor_design.md` (the ramp model these tokens address).

## 1. Motivation & author intent

The author's ask, verbatim forms:

```python
bootstyle="@light[200] #2f2f2f"      # ramp surface + hex accent
bootstyle="@background[200] danger"  # ramp surface + semantic accent
bootstyle="@#ff0000 #ffffff"         # hex surface + hex accent
```

The grammar today is a closed vocabulary: nine semantic colors, fixed variant
set. Anything else routes through the custom-style path (`register_style` /
`Style.configure` + `style=`), which is the right home for bespoke *looks* but
heavy ceremony for a one-off *color*. Value tokens give the one-line spelling.

Author's accepted cost (stated): **uglier style class names**
(`@background[200].danger.TButton`). These are mostly internal — visible in
`cget("style")` and debugging, not in user code.

Two pieces of prior art make this a natural extension rather than a swerve:

- `resolve_surface`'s docstring already says **"Raw-hex surfaces are not yet
  accepted (deferred)"** — half of this was anticipated at the surface-color
  design.
- Tailwind's arbitrary-value syntax (`bg-[#ff0000]`) is the same move on the
  same kind of closed utility vocabulary, and is heavily used in practice.

## 2. The three token forms

| Form | Slot(s) | Example | Resolves to | Theme-reactive? |
|---|---|---|---|---|
| **Ramp token** `role[stop]` | color, surface (`@role[stop]`) | `primary[300]`, `@background[200]` | the role's 50–950 ramp at `stop`, re-derived from the role's *current* anchor | **Yes** |
| **Hex accent** `#rrggbb` | color | `#2f2f2f` | that color, verbatim | No — frozen anchor; *derived* states (hover/pressed/disabled via `shade`/`tint`/`on_color`) recompute per theme |
| **Hex surface** `@#rrggbb` | surface | `@#ff0000` | that color as the blend surface | No (same contract) |

Rules:

- `stop` ∈ the existing `_RAMP_STOPS` (multiples of 50 in 50–950); `[500]` is
  the role's anchor, matching `colors.primary[300]` Python-side addressing.
- `role` = any label the `Colors` view resolves (the nine semantic colors plus
  the surface roles — exact set enumerated at implementation, §10).
- Value tokens are legal **only in the two color-bearing slots** (color,
  surface). Variants, base-types, and orients stay closed vocabulary.
- Everything existing is unchanged; this is purely additive grammar.

**Philosophy check.** The grammar's promise is "names intent; the theme renders
it in light and dark." Ramp tokens *keep* that promise — they are semantic and
re-resolve on theme switch (`@background[200]` is "a slightly darker panel" in
both modes). Raw hex deliberately trades it away for control, the same
documented trade as a direct color on a Label: a **frozen snapshot** that
survives theme switches without adapting; contrast is the caller's
responsibility. The docs teach it with exactly that existing vocabulary.

## 3. Tokenizer design

`_classify_tokens` (`style/bootstyle.py`) classifies over frozensets from
`constants.py`. Value tokens add **two anchored, eagerly-validated patterns**
alongside the sets — the model becomes *"closed vocabulary plus two validated
value patterns."* The loud-typo property is preserved because validation is
eager and total:

- `#ff00zz` → not hex digits → warn/raise (existing strictness gate:
  `set_bootstyle_strict` / `TTKBOOTSTRAP_STRICT`).
- `light[123]` → not a valid ramp stop → warn/raise.
- `light[200` / `[200]` → malformed → warn/raise.

Dialect notes:

- **Dash dialect**: no conflict — neither pattern can contain `-` — but docs
  teach the space dialect only (already the standing recommendation).
- **Dotted ttk-style-name dialect** (the lenient path fed by the theme walk /
  `Style.configure`): must pass value-token segments through unchanged; the
  classifier's segment logic gains the same two patterns.

## 4. Resolution & builder plumbing

Builders funnel color labels through `builder.colors.get(colorname)`, which
returns `None` for these tokens today. One central seam covers the bulk:

- **`resolve_color_token(colors, token) -> hex`** handling
  label | `label[stop]` | `#hex`. Decision point (§10): extend `Colors.get`
  itself vs a separate resolver; lean = extend `Colors.get`, since it is the
  single funnel and unknown labels already return `None` there.

The long tail is the **builder special-case audit**: identity checks that value
tokens will never satisfy — `colorname == LIGHT`/`DARK` (radiobutton's
contrast fix), `== NEUTRAL`, `in (DEFAULT, "")` routes. All degrade gracefully
(the token takes the generic accent path), but each must be *deliberately*
confirmed, not discovered.

Assets need nothing: the recolor pipeline and the image cache are
content-addressed by render inputs, so arbitrary hexes dedupe and rebuild
correctly per theme.

## 5. Style names & Tcl safety

Minted names look like `@background[200].danger.TButton`, `#2f2f2f.TButton`,
`@#ff0000.#ffffff.TButton`.

- Tokens can never contain `.` (guaranteed by pattern) — the only hard
  constraint of ttk's dotted namespace.
- `tk.call` passes arguments as Tcl objects, not script text, so `[`/`]` do
  **not** trigger command substitution and `#` does not start a comment on the
  paths the engine uses (configure/map/layout/element/lookup).
- **Required**: a one-time audit for any place a style name is interpolated
  into an *eval'd script string* (rather than passed as a `tk.call` argument),
  plus a regression test that builds, maps, lays out, looks up, and
  theme-switches a style named with brackets and hashes.

## 6. Theme-switch behavior

The version-stamped theme walk rebuilds registered styles on switch. Value-token
styles rebuild like any other:

- Ramp tokens re-resolve from the role's new anchor → fully adaptive.
- Hex tokens keep their anchor; the builder recomputes derived state colors
  against the new theme's surfaces, so a hex button remains *usable* (correct
  hover/pressed/disabled/on-color) even when the anchor itself doesn't adapt.

## 7. Typing, reference, tooling

- `bootstyle:` annotation becomes `BootStyle | str` — the generated `Literal`
  keeps autocomplete for the closed forms; value tokens type as plain strings
  (Python typing cannot express the patterns).
- `tools/generate_bootstyle_reference.py`: add a prose **Value tokens** section
  (patterns, validation rules, reactivity contract) — patterns cannot be
  enumerated as table rows. Sync tests updated accordingly.
- Grammar docs (`foundations/bootstyle-grammar.rst`): a "Value tokens" section
  after "Building up a style", teaching the ramp-vs-hex reactivity contract in
  the same words as the direct-color-on-Label contract.

## 8. Risks & mitigations

1. **Unbounded style registry.** Styles are never unregistered; every distinct
   hex mints a style (plus theme-walk state) for the life of the process. A
   user lerping a hex in an animation loop leaks styles without bound.
   Mitigation: document prominently; lean = also a one-time warning past a
   threshold of distinct value-token styles (threshold in §10).
2. **Surface-family gap inherited.** `@`-token surfaces (value or not) are
   silently dropped on families whose recipes don't participate
   (toolbutton/menubutton/entry — the known, logged gap). Value tokens change
   nothing here; extending participation is a separate work item.
3. **Contrast footguns.** A hex chosen for light mode may be illegible in dark.
   Docs contract (§2); a debug-mode contrast warning is possible but out of
   scope (§11).
4. **Grammar creep.** Hold the line at these two patterns in these two slots.
   No expressions, no `rgb()`/`hsl()`, no alpha, no named CSS colors, no
   per-state maps (§11).

## 9. Suggested PR shape

- **PR 1 (engine):** tokenizer patterns + validation; central resolution;
  `resolve_surface` hex/ramp acceptance; style-name plumbing; the Tcl-safety
  audit + regression test; grammar unit tests (valid/invalid hex and stops,
  combined forms, strict mode, dark-switch lookups); builder special-case
  audit notes in the PR body.
- **PR 2 (docs/tooling):** grammar-page Value tokens section; reference
  generator + sync tests; `BootStyle | str` typing; dev-log entry (*New*).

Moderate total effort; the builder audit is the long tail.

## 10. Open questions (settle in the design session)

1. Extend `Colors.get` to accept value tokens vs a separate resolver
   (lean: extend `Colors.get`).
2. Accept 3-digit hex `#rgb` and normalize to 6 (lean: yes)?
3. The exact rampable-role label set (lean: anything `colors.get` resolves,
   enumerated in the docs table).
4. Registry-growth mitigation: docs-only vs docs + one-time warning at N
   distinct value-token styles (lean: warn at 256).
5. Naming: keep `[stop]` brackets (matches Python-side `colors.primary[300]`)
   vs an alternative spelling — brackets are the lean unless the Tcl audit
   surfaces a problem.
6. Should hex accents participate in `light`/`dark`-style contrast special
   cases at all, or always take the generic path (lean: generic path)?

## 11. Out of scope

- `rgb()`/`hsl()`/alpha, color expressions (`mix`, `lighten 20%`), named CSS
  colors, per-state color maps, arbitrary-value versions of non-color slots.
- Extending `@surface` participation to toolbutton/menubutton/entry (existing
  gap, tracked separately in the 2.0 dev log).
- Anything in 2.0: this lands no earlier than 2.1.