# Workstream D — Canonical bootstyle grammar: design

> Status: **DESIGN LOCKED** (2026-07-06). Supersedes the prep notes
> `development/2_0_bootstyle_grammar_notes.md` (ground truth + open forks). This
> doc records the locked decisions and the PR sequence. Implement **PR by PR**;
> do not exceed a PR's scope without revisiting this doc (the hard rule).

## 0. Goal (from `2_0_plan.md` §D)

Turn the incidental substring-regex resolver into a **closed, documented
vocabulary in fixed slot order** with **exactly one canonical spelling per
style**, that **fails loudly** on unknown tokens instead of silently falling
through to default. bootstyle stays **semantic** (role + variant); ramp
precision lives in the Theme/custom-style API (Workstream E, done). Retire the
component-tuple form.

## 1. The slot grammar (LOCKED)

Canonical bootstyle string:

```
[color-][modifier-]<base-type>[-orient]
```

- **Exactly one** of each slot. **Fork 4 resolved: single modifier**, not
  "modifier(s)". Ground truth: all 36 registry keys are `(single-variant,
  family)`; **no** builder takes two modifiers (`outline-striped` does not
  exist). The plan's `[modifier(s)]` plural was aspirational; the registry is
  the authority.
- Slots are **order-fixed** in the canonical form (color, then modifier, then
  base-type, then orient). The `_compat` normalizer (PR D2) accepts the legacy
  order-free / tuple input and rewrites it to canonical, warning as it does.
- `base-type` is usually **inferred from the widget** (`winfo_class`), so most
  users write just `[color-][modifier]` (e.g. `"success"`, `"primary-outline"`).
  It is only spelled explicitly for the family-selecting bootstyles the user
  applies to a host widget — `"toggle"`, `"round-toggle"`, `"toolbutton"`,
  `"striped"` (progressbar), `"thin"` (progressbar), `"inverse"` (label).

## 2. Single vocabulary source of truth (LOCKED — Fork 5)

The vocabulary is currently split across `Keywords` (bootstyle.py) and
`BootColor`/`BootType` (constants.py), out of sync. Consolidate to **one home:
`constants.py`** — it is the low layer (`style/` imports it, never the reverse),
already owns `BootColor`/`BootType`, and is public.

`constants.py` defines four runtime token tuples + the matching `Literal`s
adjacent to each (a test asserts tuple ≡ Literal membership, since static
`Literal[*tuple]` is not checker-visible). `Keywords` in `bootstyle.py`
**imports these tuples** and compiles its regexes from them — no second copy.

### 2.1 The token classification (the Fork-5 reclassification)

| Slot | Tokens | Literal |
|---|---|---|
| **color** (8) | primary secondary success info warning danger light dark | `BootColor` (unchanged) |
| **modifier** — public (7) | outline link inverse round square striped thin | `BootType` (**fixed**) |
| **modifier** — internal (4) | meter metersubtxt date table | not in a public Literal |
| **base-type / family** | button checkbutton radiobutton toggle toolbutton combobox entry spinbox scale progressbar floodgauge scrollbar separator sizegrip label labelframe frame notebook panedwindow treeview menubutton calendar optionmenu + tk: menu text canvas tk toplevel listbox | `BootBase` (**new**, the user-nameable subset: toggle toolbutton) |
| **orient** (2) | horizontal vertical | `Orient` (unchanged) |

Changes vs today:
- **`BootType` fixed**: was `["outline","link","toggle","inverse","striped",
  "thin","toolbutton","square"]`. New: `["outline","link","inverse","round",
  "square","striped","thin"]` — **adds `round`** (the plan's noted bug: buildable
  but missing), **removes `toggle`/`toolbutton`** (they are base-types/families,
  proven by registry keys `(default|round|square, toggle)` and
  `(default|outline, toolbutton)`).
- **`TOGGLE`/`TOOLBUTTON` constants stay** (still valid bootstyle values); their
  annotation moves from `Final[BootType]` to a new `Final[BootBase]`.
- **`focus`/`input` dropped** — dead keywords, no builder (grep-confirmed).
- **`meter`/`metersubtxt`/`date`/`table`** remain **valid internal** modifiers
  (registry variants of `label`/`button`/`treeview`) but are **undocumented** —
  not in any public Literal, not in the reference table. They exist only so
  Meter/DateEntry/Tableview can build their composite sub-styles.

### 2.2 Validity is the registry, not the cartesian product

A token being in-vocab is necessary but not sufficient: the `(modifier,
base-type)` pair must be a **registered builder key** (or `(default, family)`
for the bare-color forms). The validator's authority for "does this resolve to a
real style" is `builders.registry.builder_keys()` — the same 36 keys, already
frozen. `outline-scale` is well-formed tokens but not a real style; the resolver
already returns the base style for it, and the validator warns that the
`(outline, scale)` pair is unknown.

## 3. The tokenizer + validator (LOCKED)

Replace the four independent `re.search` substring probes with a **real
tokenizer**: split the input on `-`/whitespace (after `_compat` has normalized
tuples/lists to a string), then classify **each** token against the closed
vocab. This removes the substring hazards (`button` inside `toolbutton`,
`label` inside `labelframe`) that the hand-ordered alternations paper over.

Per token, in slot-priority order: color? modifier (public or internal)?
base-type? orient? If a token matches **no** slot → it is **unknown**:

- **Default (warn)** — emit a `UserWarning` naming the offending token and, when
  cheap, the nearest valid token (`difflib.get_close_matches` against the flat
  vocab). Then resolve best-effort from the tokens that *did* classify (today's
  silent behavior, minus the silence). **Fork 1 resolved.**
- **Strict** — raise `ValueError` with the same message. Opt in process-wide via
  a flag (see §5).

Duplicate-slot input (two colors, two modifiers) is also a loud condition: warn
(or raise) "more than one <slot> token"; keep the first for best-effort.

### 3.1 Base-type is implied; validation splits into two phases

The base-type is **inferred from the widget** (`winfo_class`) and only taken from
the string when a base-type token is explicitly present (§1). The two families a
user ever spells out are the chameleons `toggle`/`toolbutton` (a Checkbutton
rendered as a switch / a Checkbutton|Radiobutton|Button rendered as a
toolbutton), where the desired family differs from the host widget's class.

Because the family is usually implied, loud-failure validation is **two phases**:
- **Unknown-*token*** (`"primaryy"`, `"focus"`) — a token matching no slot.
  Detectable at **parse time**, widget not required.
- **Invalid-*pair*** (`outline-scale`) — every token is in-vocab, but the
  `(modifier, resolved-family)` pair is not a registered builder key. Requires
  the **resolved family**, so it is checked at **resolve time** (widget class
  known). `bootstyle="outline"` is valid on a Button (`(outline, button)` ✓) and
  invalid on a Scale (`(outline, scale)` ✗).

Both phases route through the same warn/strict emitter.

Mirror the existing loud-failure seam: `style/layout.py`'s `statespec`/
`state_map` already validate the `!neg`/space-AND state grammar against
`TTK_STATES` and were built as "the Workstream D loud-failure seam." Same
shape — validate against a closed set, warn-or-raise.

## 4. The `_compat` quarantine (LOCKED — Fork 2)

New module **`src/ttkbootstrap/style/_compat.py`** (first tenant of the
Workstream-F compat quarantine). Public-ish to the package, not to end users.

```python
def normalize_bootstyle(value) -> str:
    """Accept a legacy bootstyle value (tuple/list, alt slot order, old
    token) and return the canonical dash-joined string. Emits a
    DeprecationWarning when the input used a retired form."""

def warn_deprecated(old, new, *, removed_in="3.0") -> None:
    """Standard deprecation-warning emitter for the quarantine."""
```

- **Tuple/list form** → dash-join then re-order to canonical, **with** a
  `DeprecationWarning` pointing at the canonical string. **Fork 2 resolved:
  warn-and-normalize through 2.x, removed in 3.0** — consistent with the tiered
  convention (new-2.0 standardizations warn through 2.x). The one exception:
  the resolver's *internal* call sites (after the D2 migration none remain) must
  not trip the warning; D2 migrates them off tuples first (§7).
- **Alt token order** (`outline-primary`) → normalized to canonical, no warning
  in 2.0 (order-freedom was never documented as deprecated; the canonical order
  is simply what the table publishes). *Optional:* a soft warning could be added
  later; not in 2.0 scope.
- `warn_deprecated` centralizes the message format so H docs can link one page.

## 5. Strictness opt-in mechanism (LOCKED)

Process-wide flag in `_compat` (the vocab/validator layer), with a public
setter re-exported from `ttkbootstrap`:

```python
ttkbootstrap.set_bootstyle_strict(True)   # raise on unknown/invalid tokens
ttkbootstrap.set_bootstyle_strict(False)  # default: warn
```

Also honor env var **`TTKBOOTSTRAP_STRICT=1`** at import (CI convenience, matches
how test suites want a hard gate without editing app code). Default = warn.
No per-widget granularity in 2.0 (keep it simple; revisit only on demand).

## 6. Meter / DateEntry / Tableview (LOCKED — Fork 3: no new public API)

Finding: these widgets **already expose clean public kwargs**
(`Meter(bootstyle=, subtextstyle=)`, `DateEntry(bootstyle=)`,
`Tableview(bootstyle=)`); the tuple/list form they use is **internal plumbing**
to build composite sub-styles. **No new public kwargs** — just internalize:

- `widgets/meter.py` — replace the six `bootstyle=(self._x, "meter"|"metersubtxt")`
  tuples with canonical strings `f"{color}-meter"` / `f"{color}-metersubtxt"`.
  (Line ~353 already builds the dash-joined string form.)
- `widgets/dateentry.py:180` — replace `[self._bootstyle, "date"]` with
  `f"{self._bootstyle}-date"` (line ~142 already does this).
- `widgets/tooltip.py:39` — `(DANGER, INVERSE)` → `"danger-inverse"`.
- `dialogs/datepicker.py:223` — `(SECONDARY, INVERSE)` → `"secondary-inverse"`.

`meter`/`metersubtxt`/`date`/`table` stay valid internal modifiers (§2.1). After
this migration, **zero internal callers use the tuple form**, so the D2
deprecation warning only fires for genuine external tuple use.

## 7. PR sequence (LOCKED)

> **D1 — IMPLEMENTED (2026-07-06, branch `feat/2.0-pr-d1-bootstyle-grammar`).**
> Suite **258 passed**, warning-free import, standalone `_compat` import,
> annotation force-eval clean, theme-switch smoke OK. Two things the design pass
> under-specified surfaced during implementation and are now handled:
> - **The resolver has two input dialects, not one.** Besides user bootstyle
>   strings, `update_ttk_widget_style` also receives *already-built ttk style
>   names* — from the theme-walk repaint (a widget's dotted `cget("style")`,
>   including a bare base like `"TFrame"`), from `Style.configure` subclassing a
>   base (`"symbol.Link.TButton"`), and from user custom style names. These are
>   parsed leniently (`_classify_style_name`, no unknown-token warnings — custom
>   prefixes are legal); only a genuine bootstyle string gets the closed-vocab
>   tokenizer + loud failure. `_looks_like_style_name` discriminates: a built
>   name has a Title-cased class (contains uppercase, no dash/space) or a dot.
> - **Invalid-pair best-effort improved.** Previously an unbuildable pair like
>   `outline`-on-Scale returned the raw fragment `"outline"` as the style name,
>   which then crashed in `configure`. Now it warns (bootstyle input only) and
>   falls back to the family's **default** style; genuine third-party widgets
>   (family not one of ours) still pass through untouched.

### D1 — vocab source + tokenizer/validator + `_compat` + strict flag (no caller changes)
- Consolidate the token tuples + reconciled Literals into `constants.py`
  (fix `BootType`, add `BootBase`, drop `focus`/`input`); `Keywords` imports
  them. Add the tuple≡Literal sync test.
- Replace the substring probes in `bootstyle.py` with the real tokenizer +
  closed-vocab validator (warn-on-unknown, warn-on-duplicate-slot).
- New `style/_compat.py`: `normalize_bootstyle` (tuples/lists/alt-order →
  canonical) + `warn_deprecated`. **In D1 the tuple form normalizes WITHOUT a
  deprecation warning** (internal callers still use tuples until D2) — this keeps
  the suite green and defers the user-facing warning to after the internal
  migration.
- `set_bootstyle_strict` + `TTKBOOTSTRAP_STRICT` env var; re-export from
  `ttkbootstrap`.
- Route the resolver's string handling through `normalize_bootstyle`.
- **No behavior change for valid input; suite stays green.** New
  `tests/test_bootstyle_grammar.py`: token classification, slot order, unknown
  → warn/raise, duplicate-slot, registry-pair validation, and a **round-trip**:
  every built-in `(variant, family)` registry key → expected canonical string →
  resolves back to the same ttk style.

### D2 — migrate internal callers + turn on the tuple deprecation
- Migrate meter/dateentry/tooltip/datepicker off the tuple form (§6).
- Flip `normalize_bootstyle` to **emit the `DeprecationWarning`** on tuple/list
  input now that no internal caller trips it.
- Verify `import ttkbootstrap` + constructing every widget stays warning-free;
  add a test that a tuple bootstyle warns and still resolves.

### D3 — generated reference table + combined-string Literal (feeds H docs)
- A small generator (a `tools/` script or a tested function) enumerates the
  vocab × registry into: (a) a **canonical grammar table** (markdown, for the
  Workstream-H docs), and (b) a generated **`BootStyle` Literal** union of the
  canonical strings that resolve to a real builder, for editor autocomplete.
  `bootstyle` params type as `BootStyle | str` (Literal aids completion; the
  runtime validator is the real gate).
- Test: the generated table/Literal matches the live vocab + registry (fails if
  a builder is added without updating the vocab).

## 8. Verification seams (carry forward)
- `import ttkbootstrap` stays **warning-free**; the PEP 649 annotation
  force-evaluation sweep and the standalone-submodule cycle guard carry over
  (any new module — `_compat` — joins the cycle guard).
- Reuse the `statespec`/`state_map` validation pattern as the model.
- The registry (`builder_keys()`) is the round-trip oracle for D1's test.

## 9. Decisions ledger (forks)
1. **Strictness** → warn-by-default + opt-in strict (`set_bootstyle_strict` /
   `TTKBOOTSTRAP_STRICT`). *(user, 2026-07-06)*
2. **Tuple form** → warn-and-normalize through 2.x, removed 3.0. *(user)*
3. **Meter/DateEntry** → no new public API; internalize the composite tuples.
   *(user)*
4. **Multi-modifier** → single modifier slot (registry proves it). *(design,
   ground-truth-forced)*
5. **Reclassify** → toggle/toolbutton = base-types; add `round` to `BootType`;
   new `BootBase`; drop focus/input; meter/metersubtxt/date/table = internal.
   *(design, registry-forced)*
6. **Generated table + Literal** → yes, from vocab × registry (D3). *(design)*
