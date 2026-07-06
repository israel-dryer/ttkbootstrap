# ttkbootstrap 2.0 — a `neutral` bootstyle color — design / scoping

> Design pass per the hard rule (this adds a token to the closed bootstyle
> vocabulary Workstream D locked, plus recipe + generator changes). Pairs with
> `development/2_0_bootstyle_grammar_design.md` (the closed-vocab grammar) and
> `development/2_0_color_helpers_design.md` / `2_0_color_math_followup_design.md`
> (the derived-color machinery this builds on).

## 1. Motivation

Today a bare `ttk.Button` renders **primary** (blue), and the only lower-emphasis
options are `secondary` (a medium-emphasis gray *fill*), `light` (a pale fill with
**no border**, so it vanishes on the `bg` surface), and `link` (hyperlink look).
There is no calm, low-emphasis "just a button" — *surface fill + a visible neutral
border + normal text* (the classic OS / Bootstrap-3 `btn-default`). Demos end up
accenting **every** control because the unaccented option doesn't read as a button.

Add an explicit, opt-in **`neutral`** color meaning *"no accent — render in the
theme's neutral surface tone."* The default stays primary; `neutral` is always
typed. (Author decision 2026-07-06: include in 2.0 — the demos benefit.)

## 2. It is a color, and it is *derived*

`neutral` occupies the **color slot** of the grammar (`[color-][modifier-]<base>`)
— it is an alternative to `primary`/`secondary`/…, mutually exclusive with them,
so it belongs in `BOOTSTYLE_COLORS`, not `BOOTSTYLE_MODIFIERS` (a modifier like
`outline` still takes a color; neutral replaces the color) and not a base type
(it is not widget-family-specific).

It is **derived** from the theme surface via the existing color-math helpers — no
per-theme authoring. Unlike the accent colors, though, neutral is not "one hex you
derive fill/text/hover from": its defining property is that **text stays `fg`**
(not the fill color) and it **carries a border**. A single resolved hex cannot
encode that policy — e.g. an outline recipe sets `foreground=<the color hex>`, and
a pale neutral hex would be invisible as text. So neutral is a *policy*, applied in
the recipe, not a value substituted into the generic derive-from-accent path.

**Neutral render policy — ported from bootstack** (`style/builders/button.py`,
`build_solid_button_style`, the `accent is None` branch). bootstack's neutral is
literally its *default* button: `bg = elevate(surface, 1)` (a mode-aware ~6% raise
of the surface — toward black in light, toward white in dark) with a **derived**
`border(bg)` (the fill blended ~16% toward its own text color) and `on_color(bg)`
text. That is more correct than a fixed `colors.light`, which is only right in
light themes. ttkbootstrap already has every equivalent helper (`shade`/`tint`,
`border`, `on_color`, `active`/`pressed`, `disabled`, `is_light_theme`), so this
ports 1:1 with no new helper.

| slot | solid `neutral` | `neutral-outline` |
|---|---|---|
| fill (`background`) | `shade(bg, 0.06)` (light) / `tint(bg, 0.06)` (dark) — the elevate | `colors.bg` |
| text (`foreground`) | `on_color(fill)` (= normal `fg`) | `colors.fg` |
| border (`bordercolor`) | `border(fill)` — derived from the fill | `border(colors.bg)` |
| hover / pressed | `active(fill)` / `pressed(fill)` | fill → `active(colors.bg)` |
| disabled | existing `disabled()` helpers | existing |

This closes the gap the author saw (`light` has no border and vanishes on the
surface) with a subtly raised, bordered fill that reads as a button in **both**
modes. The ~6% elevate weight and whether solid neutral shows a fill at all vs a
pure bordered/flat button are settle-on-the-light↔dark-visual-gate knobs.

> Provenance: mirrors bootstack's `StyleBuilderTtk.elevate`/`border` (memory
> `borrow-bootstack-mechanisms-not-api` — we take the derivation, not the API).

## 3. Scope — which families get `neutral` (the generator constraint)

`tools/generate_bootstyle_reference.py` crosses `BOOTSTYLE_COLORS` × **every**
registered `(variant, family)` key (`_strings_for_key`, line 76). So merely adding
`"neutral"` to `BOOTSTYLE_COLORS` would advertise `neutral-<anything>` for all ~22
families and let the resolver accept them — but only families with a neutral-aware
recipe would render correctly; the rest would feed a pale hex into their generic
accent path (invisible text/borders). We must not advertise combinations that look
broken.

**2.0 scope = the plain Button (solid + outline)** — the one place accent-vs-neutral
is unambiguous and exactly where demos over-accent.

Deliberately **out for 2.0**, with rationale (each is a poor or bespoke fit, not an
oversight):
- **Toolbutton** — stateful; a "neutral" toolbutton renders its *selected* state
  neutral too, destroying the selection affordance that is the whole point.
- **Menubutton** — the *outline* variant fills with the accent on hover; for neutral
  that would hover to near-`fg` (jarring), so it needs a bespoke neutral hover, not
  the shared branch. A clean fast-follow once Button lands, not part of the MVP.
- **entry/combobox/spinbox** — already neutral by default (a themed field border,
  no accent).
- **scale/progressbar/scrollbar** — geometry, not emphasis.
- **label/frame/labelframe** — their *default* already is the neutral surface.

**Generator gate:** add `NEUTRAL_FAMILIES = {"button"}` (next to the vocab tuples in
`constants.py`) and make `_strings_for_key` emit the `neutral` color only when
`family in NEUTRAL_FAMILIES`. This keeps neutral a real `BOOTSTYLE_COLORS` member
(so the tokenizer parses it) while the reference/`Literal` advertise it only where
it renders. Net new canonical strings: **2** (`neutral`, `neutral-outline`). Adding
a family later is a one-line change to the set plus that family's recipe branch.

Note the asymmetry this introduces: neutral is the first color that is *not*
valid for every family. The resolver still tokenizes `neutral-<family>` for an
unsupported family (it's a real color token); it should then fall back to that
family's default like any unbuildable pair (the Workstream-D "invalid pairs fall
back to the family default" behavior already covers this). The gate is about what
we *document/advertise*, not a second parser rule.

## 3a. Follow-on decision — border *all* solid buttons (author, 2026-07-06)

Introducing a bordered neutral raised the question of whether the *accented* solid
buttons should stay flat/borderless (as they were) while neutral alone is bordered.
Decision: **border every solid button with the same `border(fill)` logic** — no
carve-out for neutral. This matches bootstack (its solid button always draws
`border(bg_normal)`), keeps the button family visually uniform, and lets neutral
fold into the single solid recipe as "just the no-accent fill" rather than a
separate code path.

Mechanics (in `build_button_style`): `relief=RAISED`, `bordercolor=border(fill)`,
`darkcolor=lightcolor=fill` (so only the border ring shows, no clam bevel), with
the border mapped across hover/pressed/disabled. The border is **fill-derived**
(the fill blended toward its own text color), so it is same-hue — a slightly
lighter edge on dark accents, a slightly darker edge on light accents — never a
gray outline. `neutral` is now `colorname == NEUTRAL -> fill = _neutral_fill(...)`
inside the same recipe; the standalone `_build_neutral_button_style` is gone.

Scope: the **solid `ttk.Button`** recipe only. Solid **toolbutton**, **menubutton**,
and **date** buttons remain flat for now — a consistency follow-up to weigh once
the bordered Button is eyeballed (they would look inconsistent beside bordered
plain buttons in a toolbar, so this likely wants to extend, but it is a separate,
gated visual change). This flips the earlier "solid button is a plain flat fill"
decision from the color-helper PR; `test_color_helpers.py`'s solid-button contract
is updated to assert the derived border instead of `relief=flat`/no-border.

**Human visual gate required** (light↔dark, all accents) — a same-hue border on a
solid fill can read as a bevel if too strong; `border()`'s strength is the knob.

## 4. Change list

- **`constants.py`**: add `"neutral"` to `BOOTSTYLE_COLORS`; add
  `NEUTRAL: Final[BootColor] = "neutral"`; add `"neutral"` to the `BootColor`
  `Literal`; add `NEUTRAL_FAMILIES`; export both. Regenerate the `BootStyle`
  `Literal` block.
- **`style/builders/button.py`**: `build_button_style` + `build_outline_button_style`
  branch on `colorname == NEUTRAL` to apply §2's policy (fill/text/border), reusing
  `active`/`pressed`/`disabled`. Register `neutral.TButton` / `neutral.Outline.TButton`.
- **`style/builders/toolbutton.py`, `menubutton.py`**: same neutral branch.
- **`tools/generate_bootstyle_reference.py`**: the `NEUTRAL_FAMILIES` gate in
  `_strings_for_key`; regenerate `development/2_0_bootstyle_reference.md`.
- **`test_bootstyle_grammar.py`**: `BootColor` ↔ `BOOTSTYLE_COLORS` sync now
  includes `neutral`; the reference/`Literal` sync test covers the ~6 new strings.
- **New built-style test**: a `neutral` button configures `background=colors.light`,
  `bordercolor=colors.border`, `foreground=colors.fg`; a `neutral-outline` button
  configures `background=colors.bg` + the neutral border/text.
- **Demos**: convert a few over-accented demos (e.g. the `python -m ttkbootstrap`
  showcase, dialog button rows, the calculator/media-player secondary actions) to
  `neutral` so the calmer default is visible — the payoff the author called out.
- **Docs (Workstream H)**: `neutral` lands in the *bootstyle grammar* Colors list
  and the Widgets/Button catalog as the low-emphasis option; no separate workstream.

## 5. Compatibility

Purely additive — a new valid token, no deprecation, no behavior change to existing
styles. Strict mode is unaffected (`neutral` is now a known token). The default
button is unchanged (still primary). `colors.get("neutral")` is **not** relied on
by the recipes (they branch on the name); we do **not** add a `neutral` entry to
the `Colors` resolved view, to avoid implying it is an authored/derivable single
hex when it is a render policy.

## 6. Open decisions

- **Name — needs confirmation.** `neutral` (recommended: design-system term of art
  — Spectrum/Radix; zero tk collisions; precisely "no accent"). Rejected: `normal`
  (collides with the exported `NORMAL = 'normal'` widget-state constant and the
  font weight), `default` (overloads ttk's dialog "default button" / `-default`,
  and implies a default-ness ttkbootstrap doesn't give it). Alternatives if
  `neutral` is unwanted: `subtle` (Bootstrap 5.3 lineage), `plain`, `quiet`.
- **Solid neutral fill = `colors.light` vs `colors.bg` + border only** (a truly
  flat, fill-less bordered button). Lean `colors.light` (reads as a button); settle
  on the light↔dark visual gate.
- **Menubutton inclusion** — include (consistent with buttons) vs defer (it's less
  commonly un-accented). Lean include; cheap once the button branch exists.
- **Later:** a universal neutral (all families) would want a recipe refactor onto a
  shared `resolve_accent(colorname) -> (fill, on, border, hover, pressed)` helper so
  the no-accent policy lives in one place. Out of scope for 2.0; noted as a possible
  follow-up.
