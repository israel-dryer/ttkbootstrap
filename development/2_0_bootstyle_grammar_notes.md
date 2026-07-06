# Workstream D — canonical bootstyle grammar: prep for the design pass

> **How to use this doc.** D is the next 2.0 headliner. Per the hard rule, it
> **starts with a design pass** (discussion → locked decisions → a design doc
> `development/2_0_bootstyle_grammar_design.md` → PR-by-PR), **not** ad-hoc
> coding. This file is the *ground truth + open forks* so that discussion is
> fast; it is **not** the design. Read it, then open the design discussion with
> the user on the forks in §4.

## 1. Scope (from `2_0_plan.md` §D)

- A **closed, documented vocabulary in fixed slot order**:
  `[color]-[modifier(s)]-[base-type]-[orientation]` (e.g. `primary-outline-toolbutton`,
  `success-round-toggle`, `info-striped`). **Exactly one spelling** per style;
  publish the table; back it with a `Literal`.
- **Fail loudly** on unknown tokens (warn by default; optional strict mode
  raises) instead of silently falling through to default.
- Resolve the audit's inconsistencies: make `round`/`square` first-class;
  document the `toggle` default; **drop internal-only `focus`/`input`**;
  document `striped`'s real scope (progressbar/floodgauge).
- bootstyle stays **semantic** (role + variant). Ramp precision lives in the
  Theme/custom-style API (Workstream E — **done**), not bootstyle.
- **Remove the component-tuple form** (Meter's `("primary", "meter")`); those
  widgets get **dedicated styling kwargs**.

## 2. Current-state ground truth

### 2.1 The resolver — `style/bootstyle.py`

`Bootstyle.ttkstyle_name(widget, string, **kw)` builds a ttk style name by
`re.search`-ing the (lowercased, `"".join`-ed) string for a **color**, **type**,
**orient**, and **class** token via four `Keywords.*_PATTERN` alternations, then
title-cases and concatenates them into `"{Color}.{Type}.{Orient}.{Class}"`.

Consequences (the anti-patterns D replaces):
- **Order-free** — tokens are found anywhere, so `outline-primary` == `primary-outline`.
- **Unknown tokens are silently dropped** — a token that matches no pattern is
  just ignored; there is **no loud failure** and no closed vocabulary.
- **Tuple/list "support" is incidental** — `"".join(string)` concatenates tuple
  elements, then the same regex runs. There is **no explicit normalizer**.
- **Only one modifier is captured** — `ttkstyle_widget_type` returns the *first*
  TYPE match, so multi-modifier (`outline-striped`) isn't really supported today.
- **Latent substring hazards** — alternation is leftmost-match; `labelframe|label`
  is hand-ordered to work, but substring collisions (e.g. `button` inside
  `toolbutton`) are a lurking risk a real tokenizer removes.

### 2.2 The vocabulary is split across TWO out-of-sync sources

**`Keywords` (bootstyle.py):**
- `COLORS` (8): primary secondary success info warning danger light dark
- `ORIENTS` (2): horizontal vertical
- `TYPES` (13): outline link inverse round square striped thin **focus input date
  metersubtxt meter table**
- `CLASSES` (30): button progressbar … toolbutton toggle … (incl. `toggle`, `toolbutton`)

**`constants.py`:**
- `BootColor = Literal[8]` — matches COLORS.
- `BootType = Literal["outline","link","toggle","inverse","striped","thin","toolbutton","square"]`

**Mismatches to reconcile into ONE source of truth:**
- `round` is **buildable** (in `Keywords.TYPES`) but **missing from `BootType`** — the plan's noted bug.
- `toggle` and `toolbutton` are in `BootType` (typing) but are **CLASSES** in the
  resolver, not types. So the type/class boundary is muddled.
- `focus`/`input` — **dead keywords** (no builder; confirmed by grep). Drop.
- `date`/`meter`/`metersubtxt`/`table` — **internal composite-widget** keywords,
  used only via the tuple form (below). Not public.
- `inverse` — real, but only `inverse-label` exists (`builders/label.py`).

### 2.3 No compat quarantine yet

`_compat.py` (Workstream F) **does not exist**. Legacy normalization is currently
the implicit `"".join`+regex. D is the natural place to create it:
`normalize_bootstyle(value) -> str` (tuple/list/alt-order/old-name → canonical)
+ `warn_deprecated(old, new, removed_in="3.0")`.

### 2.4 Internal tuple/list callers (retiring the tuple form breaks these)

- `widgets/meter.py` ×6 — `(subtextstyle,"metersubtxt")`, `(bootstyle,"meter")`, `(subtextstyle,"meter")`.
- `widgets/dateentry.py:180` — `[self._bootstyle,"date"]` (list form + internal `date`).
- `widgets/tooltip.py:39` — `(DANGER, INVERSE)` (genuine color+modifier).
- `dialogs/datepicker.py:223` — `(SECONDARY, INVERSE)`.

→ Meter/DateEntry need **dedicated styling kwargs** to replace their internal
composite tuples; tooltip/datepicker just switch to the canonical string
(`"danger-inverse"`, `"secondary-inverse"`). Back-compat note: PR 3 kept the
tuple/list form resolving specifically for these callers — D is where it's retired.

### 2.5 The loud-failure seam already exists (PR 5)

`style/layout.py` `statespec`/`state_map` validate the `!neg`/space-AND state
grammar against `TTK_STATES` and were explicitly built as *"the Workstream D
loud-failure seam."* Bootstyle token validation should mirror that: validate
against the closed vocab; warn (default) or raise (strict).

The builder **registry** (`style/builders/registry.py`) holds the exact
`(variant, widget-family)` keys — that is the ground-truth set of valid
`(type, class)` combos to validate the grammar against and to generate the
reference table from.

## 3. Where the design doc should land decisions

Produce `development/2_0_bootstyle_grammar_design.md` with: the single vocab
source of truth, the slot grammar + tokenizer/validator, the strictness model,
the `_compat.normalize_bootstyle` contract, the Meter/DateEntry replacement
kwargs, the `Literal` + generated table plan, and the PR sequence.

## 4. Open forks for the design pass (decide WITH the user first)

1. **Strictness default** — warn-by-default + opt-in strict (plan lean) vs
   strict-by-default. (Plan open question.)
2. **Tuple-form retirement** — warn-and-normalize through 2.x (compat quarantine)
   vs hard-remove in 2.0. Internal callers migrate either way.
3. **Meter/DateEntry dedicated kwargs** — design the replacement API for the
   removed component tuples (e.g. `Meter(subtextstyle=…)`?). Biggest new surface.
4. **Multi-modifier** — does the grammar support >1 modifier (`outline-striped`)?
   Today it doesn't. Pin the slot model precisely.
5. **Reclassify `toggle`/`toolbutton`/`round`/`square`** — decide each token's
   canonical slot (base-type vs modifier) and collapse `BootColor`/`BootType` +
   the `Keywords` lists into ONE source.
6. **Generated reference table** — generate the canonical grammar table + `Literal`
   from the single vocab source; feeds Workstream H docs.

## 5. Suggested PR sequence (for the design doc to confirm)

- **D1** — single source of truth for the vocab + a real tokenizer/validator
  (closed vocab, fixed slot order, warn-on-unknown) behind the existing resolver;
  `normalize_bootstyle` in a new `_compat`. **No caller changes** (back-compat via
  normalize) → suite stays green.
- **D2** — migrate the internal tuple callers; add Meter/DateEntry dedicated
  kwargs; retire the tuple form to warn-and-normalize.
- **D3** — `Literal` typing + generated grammar table (feeds H docs).

## 6. Verification seams

- **No dedicated grammar test exists yet** — D adds one: token classification,
  slot order, unknown-token warn/raise, tuple normalization, and a round-trip
  that every built-in `(variant, family)` registry key produces the expected
  canonical string and resolves back to the same ttk style.
- Reuse the `statespec`/`state_map` validation pattern (`layout.py`).
- Gate `import ttkbootstrap` stays warning-free; the PEP 649 annotation sweep and
  standalone-submodule cycle guard carry over.
