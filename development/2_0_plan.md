# ttkbootstrap 2.0 — Cleanup & Consolidation Plan

> Status: planning. This document is the durable worklist for the 2.0 effort.
> It captures decisions, rationale, and concrete starting points for PRs.
> File/line references are point-in-time (as of mid-2026) — verify against
> current code before relying on them.

## North star

**2.0 makes ttkbootstrap the clean, well-documented, leak-free way to style
vanilla tkinter — and to build your own styles.** Every item below serves that
sentence.

ttkbootstrap stays a **styling extension for tkinter/ttk**, not a widget
library. The existing custom widgets stay, but they are citizens of the styling
system, not the headline. The forward-looking, non-tkinter framework is a
separate project (**bootstack**); 2.0 is *consolidation*, not new features.

### Scope
- Remove cruft and dead code.
- Standardize and normalize the public API (aggressive/breaking is OK when it's
  a meaningful improvement; pair with a migration path).
- Shore up memory leaks and theme-switch performance.
- Make user-defined custom styles/themes easy.
- Dramatically improve the docs (fill the gap of modern tkinter documentation).

### Non-goals
- New widgets or new feature surface.
- Multi-root support (decide: document + enforce, or defer — see Workstream A).
- Porting bootstack's *API* (different paradigm). We borrow its **mechanisms**
  (memory maintenance, repaint) only.

---

## Locked decisions

1. **bootstyle API delivery = mixin hybrid.** One shared `BootMixin`; concrete
   built-in subclasses (`class Button(BootMixin, ttk.Button)`) for real
   signatures/docstrings/typing; a generic `bootify(cls)` factory to wrap any
   third-party class; `apply_bootstyle(widget, style)` for zero-mutation
   per-instance styling; `enable_global_api()` re-applies today's global
   monkey-patch for those who want it. Replaces the import-time monkey-patch as
   the default.
2. **bootstyle is a single canonical string — NOT polymorphic.** Only
   `bootstyle="round-toggle"`; no tuple/list forms, no alternate orderings.
   This makes the valid set enumerable → real `Literal` typing + generated
   reference.
3. **Theme model = semantic-anchor.** Declare ~5 accent anchors + neutral +
   light/dark `{background, foreground}` blocks; auto-generate the 50–950 ramp
   and per-mode step selection; one declaration produces both light+dark
   variants. Collapses the redundant flat per-theme dicts.
4. **Deprecation policy = tiered, via a centralized compat layer.** New 2.0
   standardizations get warn-and-normalize (removed in 3.0); things already
   deprecated for years are removed outright in 2.0.
5. **Structure cleanup is in scope.** Dead scaffolding already removed; the
   `style.py` split rides along with the engine rewrite.

---

## Workstreams

### A. Engine: memory & repaint (highest impact)

Borrow bootstack's **mechanisms** (not its API). The leaks the audit found and
bootstack's fixes line up one-to-one:

| Problem (ttkbootstrap) | Fix (from bootstack) |
|---|---|
| `_style_registry`/`_theme_styles` grow unbounded; theme switch rebuilds *all* styles, O(n) (`style.py` ~`599`, `889`, `893`) | **Version-stamped deterministic theme walk**: `winfo_children()` DFS, stamp `_theme_version` on each styled widget, repaint only stale; drop the `<Map>`-deferred + registry model |
| `theme_images` PhotoImage cache never evicts; old builders' images persist after switch (`style.py` ~`1281`) | **Unified image cache + `clear_cache()` + deferred render**, keyed by (color/size/state) so identical assets dedupe |
| Canvas-embedded widgets mis-repaint via `<Map>` | The walk is event-free → fixes this bug class |
| Frozen-hex colors don't follow theme | **Store style/surface *tokens* on widgets; re-resolve on walk** (never store resolved hex) |

Also decide the **singleton/multi-root** posture (`style.py` ~`578-607`): the
singleton silently returns the first root's instance with no error. Options:
(1) enforce single-root with a clear `RuntimeError`; (2) index state by root for
real multi-root; (3) document as a hard requirement. Recommended for 2.0:
enforce + clear error (full multi-root is out of scope).

Replace fragile `_PhotoImage__photo.name` access (`style.py` ~`1624`, `2212`)
and the bare `except:` blocks (`style.py` ~`2998, 3460, 4456, 5145, 5434, 5482,
5509`) with explicit handling.

### B. Lifecycle cleanup (the rest of the leaks)

Add `destroy()` overrides / unsubscribe paths:
- Floodgauge `after()` animation loop + variable traces that accumulate on every
  `configure` (`widgets/floodgauge.py` ~`127`, `253`, `360`).
- Meter binding IDs (`widgets/meter.py` ~`265`, `398`).
- Combobox `Publisher.subscribe` with no unsubscribe (`style.py` ~`5426`).

### C. API: the mixin hybrid

The resolver `update_ttk_widget_style` is already widget-agnostic (it introspects
`winfo_class()`), so the wrapping logic collapses into one primitive:

```python
class BootMixin:
    def __init__(self, *args, bootstyle="", **kw):
        super().__init__(*args, **kw)
        self.configure(bootstyle=bootstyle or "default")
    def configure(self, cnf=None, *, bootstyle=None, **kw):
        if bootstyle is not None:
            kw["style"] = update_ttk_widget_style(self, bootstyle, **kw)
        return super().configure(cnf, **kw)

class Button(BootMixin, ttk.Button): pass        # blessed built-ins (typed, documented)
ThemedCalendar = bootify(tkcalendar.Calendar)     # wrap anything
apply_bootstyle(widget, "success")                # per-instance, no class mutation
enable_global_api()                               # opt-in: re-apply old monkey-patch
```

Benefits: deletes the ~450-line inline `TYPE_CHECKING` stub block **and** the
55 KB `__init__.pyi` (real classes carry the types/docstrings); removes the
late-binding closure bug in `setup_ttkbootstrap_api` (`style.py` ~`5467-5475`,
where `__setitem__`/`__getitem__` capture loop vars by reference); honest
signatures feed autogenerated API docs.

Typing trade-off (accepted): concrete classes for the blessed set (statically
visible); `bootify()`/`apply_bootstyle()` for the dynamic long tail.

### D. bootstyle: canonical grammar

- Define a **closed, documented vocabulary** in fixed slot order:
  `[color]-[modifier(s)]-[base-type]-[orientation]`, e.g. `primary-outline-toolbutton`,
  `success-round-toggle`, `info-striped`, `secondary-link`. Exactly one spelling
  per style; publish the table; back it with a `Literal` type.
- **Fail loudly** on unknown tokens (warn by default; optional strict mode that
  raises) instead of silently falling through to default.
- Resolve specific inconsistencies the audit found: expose `round`/`square` as
  first-class (buildable but missing from `BootType` in `constants.py` ~`97`);
  document the `toggle` default; drop internal-only `focus`/`input` from the
  public vocabulary; document `striped`'s real scope (progressbar/floodgauge).
- bootstyle stays **semantic** (role + variant). Ramp-step precision
  (`primary[300]`) lives in the Theme/custom-style API, not in bootstyle.
- The component-tuple form (Meter's `("primary", "meter")`) is removed; those
  widgets get dedicated styling kwargs.

### E. Theme model: semantic anchors

Authoring (replaces the 16-key flat dict in `themes/standard.py`):

```python
Theme(
    name="cosmo",
    primary="#2780e3", success="#3fb618", info="#9954bb",
    warning="#ff7518", danger="#ff0039",
    neutral="#7e8081",                                   # has a default
    light=dict(background="#ffffff", foreground="#373a3c"),
    dark=dict(background="#222222",  foreground="#f8f9fa"),
).register()                                             # cosmo-light + cosmo-dark
```

Resolution — `Colors` becomes a resolved view that stays backward-compatible and
gains ramp addressing:

```python
c = style.colors
c.primary            # per-mode solid step (unchanged attr)
c.get("primary")     # unchanged
c.primary[300]       # NEW addressable ramp step
c.bg, c.fg, c.border, c.inputbg, c.selectbg   # derived plumbing, still attr-accessible
```

Notes / risk:
- Borrow bootstack's ramp weights + per-mode `_SOLID_STOP` logic directly (we are
  **not** required to reproduce the current active-state shades).
- All 8 bootstyle color keywords must still resolve — `light`/`dark`/`secondary`
  come from the neutral ramp now.
- Keep the surface layer minimal (ttk needs: window bg, input bg, select bg,
  border) — do **not** import bootstack's full `content/card/chrome/overlay`
  taxonomy.
- A legacy 16-key theme dict / old `Colors(...)` is accepted via an adapter (see
  Workstream F), not a second engine.

### F. Migration & deprecation (the compat quarantine)

**Rule: legacy is a thin adapter to the new canonical path, never a parallel
implementation.** All legacy handling lives in one module at the edges; the core
only ever sees normalized input.

```python
# _compat.py  — the ONLY place legacy shapes are understood
def normalize_bootstyle(value) -> str:      # tuple/list/alt-order/old names -> canonical str
def normalize_theme_input(spec) -> Theme:   # 16-key dict / old Colors -> Theme
def install_global_api(): ...               # the old monkey-patch, opt-in
def warn_deprecated(old, new, *, removed_in="3.0"): ...
```

Discipline:
- Each concern has **exactly one** choke point; legacy shapes must not leak past
  it. Canonical functions are typed to accept canonical input only (a leaked
  legacy shape is a type error, not a silent branch).
- Removal later = delete `_compat.py`; the import errors become the removal
  checklist.
- Tests assert each warning fires (`pytest.warns`); optional strict mode turns
  warnings into errors for users who want to be clean now.
- Publish a deprecation policy ("deprecated in 2.x, removed in 3.0") so soft
  deprecations have a stated end.

Tiering:
- **Remove outright in 2.0** (already warned for years): the 4 top-level shim
  modules (`scrolled.py`, `tableview.py`, `toast.py`, `tooltip.py`),
  `FloodgaugeLegacy`, the `dialogs/dialogs.py` path shim.
- **Warn-and-normalize through 2.x** (new in 2.0): bootstyle polymorphism, the
  16-key theme dict, the global monkey-patch (via `enable_global_api`).

### G. Repo structure

Already done: deleted dead empty/untracked scaffolding (`api/`, `core/`,
`runtime/`, `datasource/`, `cli/`, the empty `style/` package, and
`widgets/{composites,internal,mixins,parts,primitives}/`) + stray `nul`.

Remaining:
- **Split `style.py`** (~5.5k lines) into a real `style/` package — but do it
  **as part of** the engine/API/theme rewrites (Workstreams A/C/E rewrite large
  chunks anyway; splitting first then rewriting = double churn):
  ```
  style/
    engine.py        # Style singleton, theme walk, registry
    builders_ttk.py  # StyleBuilderTTK
    builders_tk.py   # StyleBuilderTK
    bootstyle.py     # BootMixin + grammar/parser
    theme.py         # Theme, Colors, ramp generation
  _compat.py         # normalization/deprecation quarantine
  ```
- **Public vs internal** at top level: move plumbing (`publisher.py`,
  `utility.py`) under a private `_internal/` or `_`-prefix; keep `colorutils`,
  `constants`, `validation`, `icons`, `window` public.
- **Collapse the dual typing surface** (`__init__.pyi` + inline `TYPE_CHECKING`)
  — the mixin move deletes most of it.
- **Tests**: split headless pytest (`tests/`) from interactive `mainloop()`
  demos (move to `examples/`), so the suite is CI-runnable cleanly.

### H. Documentation (Diátaxis, modeled on bootstack.org)

Restructure (keep mkdocs + mkdocstrings; adopt the *IA*, not Sphinx):
- **Getting Started** (tutorial) → **How-To** (tasks) → **Guides** (concepts:
  the bootstyle grammar, theming, building your own style/theme, typography,
  images) → **API Reference** (autogenerated from the new real docstrings).
- Flagship artifacts: the **authoritative bootstyle reference** (the canonical
  grammar table) and a **"create your own theme/style" guide** built on the
  declarative `Theme` API and addressable ramp tokens.
- Widget pages: visual-first, light+dark screenshots, lead with semantic styling.

### I. Style-construction toolkit (public + dogfooded internally)

Public helpers that make building image/state-based ttk styles tractable — the
delivery vehicle for "make custom styles easy," and the same code that
de-duplicates the ~40 hand-written asset/layout sites in `style.py`. Modeled on
bootstack's layout + image-layout builders. **Acceptance test:** rewriting
`create_scale_assets`/`create_radiobutton_style` on the toolkit must come out
shorter and clearer, or the abstraction is wrong.

Warts it targets (observed in `style.py`): per-state asset boilerplate
(`Image.new`→draw→`PhotoImage(resize)`→`get_image_name`→`theme_images[]`, 4× per
family, e.g. ~`1883–1934`, ~`3837–3880`); hand-coded supersample/downscale with
inconsistent oversample canvases + magic coords; positional image-element state
tuples with bare statespecs (~`3911`); hand-nested layout tuple/dict pyramids
(~`1976`, ~`3920`); bare-string `map` statespecs (~`3793`); name/orientation
surgery + the `DEFAULT/""` dance; ad-hoc `update_hsv(±0.1)` state colors.

- **Tier 1 (mechanical, low-risk):**
  - `image_asset(key, render_fn, *, size, oversample)` — supersample-draw +
    LANCZOS downscale + cache + return name. **This is the same chokepoint as the
    content-addressed image cache (Workstream A / PR 2)** — `render_fn` is pure,
    `key` is the memo key. Shape recipes on top: `circle/rounded_rect/rect_asset`.
  - `image_element(name, default=, states={spec: img}, **opts)` — named, validated
    state→image map over `element_create(..., "image", ...)`.
  - `layout()` builder — nested `El(name, side=, sticky=, children=[...])` →
    ttk's tuple/dict tree (bootstack layout analog; biggest readability win).
  - `statespec`/`when` + `state_map()` — validate the `!`/AND grammar vs bare
    strings; the natural home for loud-failure validation (cf. Workstream D).
  - `StyleName(base, color, orient)` → `.ttkstyle`/`.element`; absorbs the
    `DEFAULT/""` + `.TS→.S` rules.
- **Tier 2 (opinionated, after E):** `state_colors(base)` from ramp steps
  (depends on the semantic-anchor model) replacing scattered `update_hsv`;
  composite recipes (indicator, thumb+track) built on Tier 1.

Sequencing: **land Tier 1 with the `style/` split (Workstream G)** — both touch
the same 40 sites; building helpers + migrating builders in one pass avoids
double-churn, and the helpers get a stable home (`style/assets.py`,
`style/layout.py`). Keep it thin (helpers, not a DSL); it is a new *public*
compat surface, so small + orthogonal. Tier 2 follows E.

1. **(this) Plan documented** on `docs/2.0-plan`.
2. **Maintenance release from `master`** for the recently merged fixes
   (#1062–#1067, etc.). Independent of 2.0.
3. **2.0 work begins** — suggested order:
   - Tier-0/1 structure cleanup that's independent (shims removal, public/internal
     split, demos→examples). Low risk, immediate clarity.
   - **C (mixin) + the `style.py` split** together — keystone; unlocks typing/docs
     and removes the stub surface.
   - **A (engine walk + image cache) + B (lifecycle)** behind a destroy/recreate +
     theme-switch **stress harness** so every fix has a before/after number.
   - **E (Theme/anchor) + D (bootstyle canonical)** — the user-facing
     standardizations; carry the `_compat` adapters.
   - **H (docs)** — continuous; the reference pages fall out once C lands.

---

## Post-2.0 (2.1) backlog

Tracked enhancements deliberately held out of the feature-frozen 2.0:

- **bootstyle value tokens** — hex + ramp-addressed accents and surfaces
  (`bootstyle="@background[200] danger"`, `"#2f2f2f"`, `"@#ff0000"`). Design
  brief: `development/2_1_bootstyle_value_tokens_design.md` (PROPOSED,
  2026-07-16; design session before implementation). Tracked as **#1236**
  on the **2.1 milestone**.
- **`@surface` participation for toolbutton/menubutton/entry** — those recipes
  silently drop the surface token today (known gap, logged in
  `2_0_breaking_changes.md` under the check/radio surface fix). Extend per
  demand.

---

## Open questions

- **bootstyle strictness default**: warn-by-default with opt-in strict mode
  (lean), vs strict-by-default.
- **Multi-root**: enforce single-root with a clear error (lean) vs defer.
- **Built-in theme drift**: accept that auto-ramps refresh the shipped palette
  (lean, since matching old active-state shades is not required) vs pin specific
  themes that regress.

---

## Appendix: supporting investigations

Three audits informed this plan (mid-2026):
- ttkbootstrap debt audit (bootstyle grammar, deprecation shims, custom-style
  friction, leak/perf suspects, singleton) — file/line refs throughout.
- bootstack mechanism mining (version-stamped theme walk, token-not-hex,
  unified image cache, semantic-anchor theme model) — borrow mechanisms only.
- bootstack docs IA + custom-style UX (Diátaxis, declarative `Theme`).
