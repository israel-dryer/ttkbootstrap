# ttkbootstrap 2.0 — Documentation overhaul (Workstream H) — design / scoping

> Design pass for the last 2.0 headliner, per the hard rule (run a design pass
> before a large slice). Pair with `development/2_0_plan.md` (§H), the two staged
> sources (`2_0_bootstyle_reference.md`, `2_0_theme_migration.md`), and the
> handoff. Vision locked with the author 2026-07-06; see memory
> `project-2-0-docs-vision`.

## 1. Context & goal

2.0 is code-complete; the docs have not caught up and are the one remaining
workstream. Goal: fill the gap of *modern tkinter documentation* — a docs site
that teaches semantic styling, custom styles/themes, and the shipped widgets —
modeled on **bootstack.org**'s IA (Diátaxis), but adapted to ttkbootstrap's
nature as a **styling extension for vanilla ttk** (not a widget framework).

### Toolchain decision — LOCKED 2026-07-10 (supersedes the mkdocs assumptions below)

The docs move **off mkdocs onto bootstack's stack**: **Sphinx +
`pydata_sphinx_theme` + `autodoc`/`napoleon` + `autosummary` + `sphinx_design` +
`myst_parser`**, authored in **reStructuredText** (bootstack is rST-primary — 319
rst / 19 md; MyST is enabled only to pull in `CHANGELOG.md`). Rationale: the PyData
theme is the numpy/pandas/scipy theme our scientific/utility audience already
reads; `autodoc` keeps docstring-driven API pages (ttkbootstrap's `Parameters:`/
`Examples:` docstrings parse under `napoleon_google_docstring=True` **as-is** — no
docstring rewrite); Sphinx stays readthedocs-native (no publishing change); and
authoring in rST lets us copy-adapt bootstack's mature page templates + reuse its
`conf.py`, `_static/` CSS, `_templates/`, and **`docs/screenshots/` + `docs/scripts/`
screenshot tooling** wholesale (only the palette + the images themselves change).
Borrow the **infrastructure and IA**, author ttkbootstrap-specific **content**, and
keep the **styling-extension positioning** (bootstack is a widget library; we are
not) — the code-side [[borrow-bootstack-mechanisms-not-api]] rule, applied to docs.

> **Spike outcome (2026-07-10, PR #1148 — sub-PR 1).** The skeleton spike built
> clean (22 pages, zero warnings) and confirmed the toolchain. Three deltas from
> the assumptions above, now baked into `docs/conf.py`:
> 1. **`autoclass_content = "both"`** — ttkbootstrap documents constructor params in
>    each widget's `__init__` docstring (bootstack documents them on the class), so
>    autodoc must concatenate class + `__init__` to render the `Parameters:` tables.
> 2. **`inherited-members: False`** globally (as §5c specifies) — keeps tkinter's
>    ~200 inherited members off our pages.
> 3. **The "docstrings feed autodoc as-is — no docstring rewrite" claim is only
>    half true.** ttkbootstrap's `Examples:` blocks use **Markdown ```` ```python ````
>    code fences** (authored for mkdocstrings); napoleon/rST renders them as broken
>    inline literals. Resolved WITHOUT touching the source via a small
>    `autodoc-process-docstring` shim (`_convert_markdown_fences`) that rewrites
>    fences to `.. code-block::` at build time — so the "no rewrite" goal holds via
>    infrastructure. **Open decision for a later slice:** keep the build-time shim,
>    or sweep the docstrings to native rST (single-backtick inline code already
>    renders fine via `default_role = "code"`; only the triple-backtick fences break).

**Clean cut:** delete `docs/` (the mkdocs tree) — `docs/ja` + `docs/zh` go (English
only for 2.0; ~134 files + the `i18n` plugin), and the stale `docs/en` pages are
rebuilt, not repointed. So the "9 broken `:::` API stubs" resolve by *replacement*.

**Generators:** the introspection-based Style Reference and
`tools/generate_bootstyle_reference.py` stay **offline `tools/` steps that emit
committed rST** (the Style Reference needs a live Tk root — never a Sphinx
build-time extension, since readthedocs has no display). `autodoc` importing
ttkbootstrap at build is safe (Pillow-only, no Tk root created); keep
`autodoc_mock_imports` as a backstop.

**Mapping for the mkdocs-era references in the sections below:** mkdocstrings `:::`
→ `autodoc` (`automodule`/`autoclass` / `autosummary`); material → pydata; mkdocs
`nav:` → Sphinx `toctree`; `inherited_members: false` → autodoc's
`:no-inherited-members:` (or `autodoc_default_options`). The IA (§3), the native/
shipped dichotomy (§4), and the page templates (§5) are framework-agnostic and
stand.

## 2. Prerequisite (code, before docs): drop the character-based icons

Not part of H, but must land first because it changes widget/dialog appearance
(and therefore screenshots). Gets its own short design pass per the hard rule.

- **Remove** `src/ttkbootstrap/icons.py` — the `Emoji`/`EmojiItem` unicode-emoji
  catalog and the `Icon.info/.warning/.error/.question` constants. A "poor man's",
  OS-font-dependent, un-recolorable solution.
- **Keep** the Bootstrap-Icons **font-glyph** engine (`style/icons.py`,
  `IconRenderer`, `Assets.icon`, `Icon`/`icon_element`). Its only current
  consumers — DateEntry (`calendar3`), the caret arrows (`builders/utils.py`),
  and sizegrip (`grip-horizontal`) — are unchanged.
- **Rewire** the one real consumer of the removed module: Messagebox's four
  default icons (`dialogs/message.py:213/239/265/291`) → font glyphs
  (`info-circle-fill`, `exclamation-triangle-fill`, `x-circle-fill`,
  `question-circle-fill`). Strict upgrade (theme-matched, recolorable) that also
  dogfoods the glyph engine.
- **Side effect (good):** the `Icon` name collision disappears — there is no
  longer a character `ttkbootstrap.icons.Icon` shadowing the top-level
  `ttkbootstrap.Icon` (the glyph one). Delete `api/icons/emoji.md` +
  `api/icons/icon.md` and the "icons module" nav group.
- **Migration entry:** "`ttkbootstrap.icons` (`Emoji`, `Icon` constants) removed;
  dialog icons now render from the built-in icon font; paste a literal emoji
  character if you need one."

## 3. Target information architecture (4 destinations)

Down from today's 7 diffuse tabs (Home · Getting started · Style guide · API ·
Themes · Gallery · Cookbook).

| Destination | Diátaxis role | Contains |
|---|---|---|
| **Landing** | — | marketing hero (light+dark hero shot), "why" cards, a glimpse (minimal code + screenshot), install |
| **User Guide** | tutorial + how-to + explanation | Getting Started · Concepts (guides) · How-To |
| **Widgets** | (task/reference hybrid) | the visual catalog — grouped native vs. shipped |
| **Reference** | reference | **Style Reference** (generated) + **API Reference** (mkdocstrings) |
| *(supporting)* | — | Release Notes (link to GH releases), optional Roadmap |

### User Guide internal structure

```
User Guide
├─ Getting Started
│   ├─ Quickstart              first window; Window vs Tk; choosing a theme
│   └─ Migrating to 2.0        bootstyle strings, theme names, removed shims, icons
├─ Concepts (the guides)       ← the "modern tkinter docs" gap-fill
│   ├─ The bootstyle grammar   ★ FLAGSHIP — canonical grammar + reference table
│   ├─ Theming                 semantic-anchor model + 2-column light/dark gallery
│   ├─ Make your own style     ☆ second act — the custom-style toolkit
│   ├─ Make your own theme     Theme() API + ttkcreator
│   └─ Working with color      style.colors, ramp addressing (c.primary[300])
└─ How-To (tasks)              validate input, animate a gif, … (absorbs Cookbook)
```

- **Flagship = the bootstyle grammar** — leads the Landing hero and the User
  Guide (the universal "how do I style anything" front door). *Make your own
  style/theme* is the prominent second act (the biggest *new* 2.0 capability).
- **Themes** is folded here as the *Theming* guide; its gallery renders the 30
  themes as **light/dark pairs in a 2-column layout**.
- **Cookbook** is removed; its pages become **How-To** entries.
- **Gallery** (real-app demos) is removed for 2.0; can return later.

## 4. The native / shipped dichotomy (the core design idea)

ttkbootstrap has a split bootstack doesn't: **native ttk widgets it *styles***
(Button, Entry, Combobox, Treeview…) vs. **widgets it *ships*** (Meter,
Floodgauge, DateEntry, Tableview, ScrolledFrame, tooltip, toast, dialogs).

Two orthogonal axes:
- **Axis A — widget kind:** native (no ttkbootstrap Python API) vs. shipped (real
  authored API).
- **Axis B — page purpose:** catalog/usage vs. manual-styling reference vs. API
  reference.

**Resolution — 1 catalog + 2 references:**
- The **Widgets catalog** is *grouped* by Axis A ("Styling ttk widgets" /
  "ttkbootstrap widgets"). Membership carries the distinction — cheap, obvious,
  no duplicated machinery. It is the common front door for both kinds.
- A widget's *depth* lands on exactly one reference side: native → **Style
  Reference**; shipped → **API Reference**. The catalog cross-links to whichever
  is deep for that widget.
- The native/shipped split *already* half-falls-out of API docs (shipped widgets
  have API pages, native don't); the catalog-vs-manual-styling split is the part
  we design deliberately.

## 5. Page templates (with worked examples)

### 5a. Widgets catalog page — one shared skeleton (every widget)

```
<Widget>
  one-liner
  [ light screenshot ] [ dark screenshot ]        ← all color variants
  ## Semantic styling      → lead with bootstyle + copy-paste minimal example
  ## Variants | Common tasks   (screenshot + 2-line snippet each)
  ## Colors                (swatch strip, light+dark)
  ## States                (disabled/active/… where relevant)
  → cross-link to the deep reference (Style Reference OR API Reference)
```

Same skeleton regardless of widget kind — this is what makes 30+ pages read as
one system.

**Button** (native) — catalog page leads with `bootstyle`, shows Solid/Outline/
Link variants + 8 colors, cross-links to **Style Reference › Button**. No API
section (it's `ttk.Button`).

**Floodgauge** (shipped) — catalog page leads with `bootstyle`, then *Common
tasks* (determinate/indeterminate `mode`, `mask`/`text`, `.start()/.stop()/
.step()`, bind `variable`), cross-links to **API Reference › Floodgauge**. Style
Reference is N/A (Canvas).

### 5b. Style Reference (generated) — for native widgets & any widget with a ttk style surface

Reimagines today's thin "Style guide" into an *exhaustive, generated* reference
of the hand-styling surface. Generated from ttk introspection (same play as
`tools/generate_bootstyle_reference.py`): `style.element_options`, `style.layout`,
state specs.

```
<Widget> — style reference
  ## bootstyle → ttk style name     e.g. primary-outline → primary.Outline.TButton
  ## Layout (elements)              Button.border › Button.padding › Button.label
  ## Configurable options           background, foreground, bordercolor, relief, …
  ## Supported states               active, pressed, disabled, focus, !disabled
  ## Hand-styling example           style.configure("my.TButton", …) + Button(style=…)
```

Mostly populated for native ttk widgets; shipped widgets that expose a ttk style
surface get an entry too; pure-Canvas widgets (Floodgauge) get a one-line stub
pointing back to `bootstyle` + constructor.

**Action:** build `tools/generate_style_reference.py`. Decide per-widget vs. one
big table (lean: one page per widget family, browsable, matching the catalog).

### 5c. API Reference — only what ttkbootstrap authors

mkdocstrings over: shipped widgets, dialogs, engine/toolkit (`Style`, `Colors`,
`Theme`, `Window`/`Toplevel`, `Assets`/`layout`/`Icon`/`register_style`/…), the
delivery API (`BootMixin`/`AutoStyleMixin`/`bootify`/`apply_bootstyle`/
`enable_global_api` — documented once; this is where the `bootstyle` kwarg is
explained), and utilities (`colorutils`, `utility`, `validation`, `localization`,
`constants`).

- **`inherited_members: false`** globally — never leak tkinter/Canvas inherited
  members into our pages.
- **Native widgets get NO API page.** For their plain ttk constructor options:
  link out to python.org's `tkinter.ttk` reference + one shared "ttk widget
  options" page (curated: common options `state`/`textvariable`/`takefocus`/…
  plus a per-widget line for the few specific ones). Do **not** re-author the
  per-widget stubs PR 3 deliberately deleted.

## 6. Landing page

bootstack-style marketing landing (not a doc page): hero with light+dark window
screenshot, a "Why ttkbootstrap" card grid (semantic styling / batteries for
styling / looks right by default / pure-Python), a "glimpse" (minimal `Window` +
a few `bootstyle` widgets + its screenshot), "Start here" cards (Quickstart /
User Guide / Widgets / API Reference), install (note `requires-python >=3.10`).
Lead the "why" and glimpse with the **bootstyle grammar** flagship.

## 7. Screenshots

No capture tooling exists in-repo today. The author generates screenshots,
**borrowing bootstack's mechanism** (`bootstack/docs/screenshots/` + scripts —
light+dark pairs). Every catalog page and the theme gallery need light+dark. This
is gated on the icon-drop PR landing first (so arrows/date/dialog icons are final).

## 8. Staleness inventory (from the 2026-07-06 audit)

**HIGH — actively broken (fix or the build/examples break):**
- 7 API stub pages point `:::` at *removed* module paths → mkdocstrings fails:
  `api/toast.md`, `api/tooltip.md`, `api/scrolled/scrolledframe.md`,
  `api/scrolled/scrolledtext.md`, `api/tableview/tableview.md`,
  `api/tableview/tablecolumn.md`, `api/tableview/tablerow.md`
  → repoint to `ttkbootstrap.widgets.<name>`.
- `gettingstarted/tutorial.md` — teaches tuple bootstyle as *recommended*, "regex
  in the background", `litera` default, `themename="darkly"` (now throws). The
  canonical entry page → full rewrite into Quickstart.
- Runnable examples with legacy theme names that now crash:
  `gallery/stopwatch.md` (`cosmo`), `gallery/calculator.md` (`flatly`),
  `cookbook/gif-animation.md` (`superhero`). (Gallery is being removed; salvage
  gif-animation into How-To.)
- `themes/definitions.md`, `themes/themecreator.md` — document the retired 16-key
  `USER_THEMES` dict model → replace with the `Theme` model (fold in the
  migration guide).

**MED — outdated, not broken:** `api/index.md` (lists removed top-level modules);
`styleguide/index.md` (bootstyle "injected into the ttk constructor" — retired);
`themes/light.md`/`dark.md` (legacy Bootswatch names); tuple-bootstyle examples in
several gallery pages (moot once Gallery is dropped).

**LOW:** `index.md` (understates the 30-theme catalog); `styleguide/legacywidgets.md`
(Publisher moved to internal); `gettingstarted/installation.md` (add `>=3.10`).

**Reassuring:** most `styleguide/*` widget pages use plain string bootstyle and
are NOT stale — breakage is concentrated in the tutorial, galleries, theme pages,
and the 7 API stubs.

## 9. Undocumented 2.0 surface → new pages

- **Custom style-construction toolkit** — `Assets`, `El`, `layout`,
  `register_style`, `image_element`, `statespec`, `state_map`, `StyleName` →
  *Make your own style* + toolkit API pages.
- **Icon glyph engine** — `Icon`/`icon_element` (post-drop, the only `Icon`) →
  a section of *Make your own style* + API.
- **Canonical bootstyle grammar** — closed-vocab tokenizer, slot order, strict
  mode → the *bootstyle grammar* flagship; **fold in
  `development/2_0_bootstyle_reference.md`** (generated table).
- **Delivery model** — `enable_global_api`/`bootify`/`apply_bootstyle`/
  `BootMixin`/`AutoStyleMixin`, "no more import-time monkey-patch".
- **Theme model + migration** — semantic-anchor `Theme`, `install_legacy_themes()`,
  `bootstrap-light` default, ramp addressing → *Theming* / *Make your own theme* /
  *Migrating*; **fold in `development/2_0_theme_migration.md`**.

## 10. Folding in the staged sources

- `2_0_bootstyle_reference.md` → the *bootstyle grammar* guide's reference table
  (keep it generated; wire `tools/generate_bootstyle_reference.py` output into the
  docs, sync-tested).
- `2_0_theme_migration.md` → split across *Theming*, *Make your own theme*, and
  *Migrating to 2.0*. Keep the source in `development/` until the docs land.

## 11. Suggested sub-PR sequence

Docs work is continuous but breaks into reviewable slices:

0. **(prereq, code)** ~~Drop character-based icons~~ — DONE (#1094). *(kept for
   history.)*
1. **Sphinx skeleton (clean cut)** — delete the mkdocs `docs/` tree (incl.
   `ja`/`zh`); lift bootstack's `conf.py` + `_static/` CSS + `_templates/` +
   `screenshots/`/`scripts/` tooling; stand up the pydata theme + `toctree` IA
   skeleton; `autodoc`/`napoleon`/`sphinx_design` wired; a **spike** first — one
   widget page + the api-reference pattern lifted from bootstack — to prove the
   structure. Site builds clean (no dead autodoc targets). *(First task next
   session.)*
2. **Reference generators** — `tools/generate_style_reference.py` (offline, emits
   committed rST); retarget `tools/generate_bootstyle_reference.py` md→rST and wire
   it in; sync tests.
3. **User Guide** — Quickstart (rewrite the tutorial), the 5 Concept guides
   (flagship first), How-To (salvage cookbook), Migrating to 2.0 (fold theme +
   icon migration).
4. **Widgets catalog** — the shared template across all widgets, grouped native/
   shipped, cross-linked to the deep reference.
5. **Landing + screenshots** — marketing hero; light+dark screenshots (author,
   bootstack mechanism) across catalog + theme gallery.

## 11a. ~~Caveat: shipped-widget APIs are still pre-normalization~~ — RESOLVED

**Update 2026-07-10: this caveat is obsolete.** The shipped-widget API
normalization is **DONE** — `Window`/`Toplevel` (#1103), dialogs (#1102),
`Tableview` (#1104), and the full widget-review series (Meter/DateEntry/Floodgauge/
Scrolled/LabeledScale/ToolTip/Toast, #1110–#1115) all landed, plus the
property/accessor pass. Docs are now written against **final** signatures — the
churn risk below no longer applies. (Original text kept for history.)

Churn is asymmetric, so mitigate by page type:
- **API Reference (autogen, mkdocstrings)** — cheap. Regenerates from the new
  docstrings when an API changes; effectively zero manual rework. No special care.
- **Catalog "Common tasks" prose + How-To examples** — fragile (hand-written code
  that *calls* these APIs). For the un-passed widgets, keep examples
  **conservative** — use the stable/core parameters and methods, avoid leaning on
  surfaces likely to be renamed/reshaped — so a later API pass edits few pages.

Track the pending API-normalization pass as its own future workstream (not H);
when it lands, re-sweep the catalog/How-To examples for those widgets.

## 12. Open / deferred

- Style Reference: one page per widget family vs. one big generated table (lean:
  per-family, browsable).
- "Working with color" as its own guide vs. a section of *Make your own style*
  (lean: keep small standalone; the ramp API is a clean new feature).
- Roadmap page: include or omit (bootstack has one; optional for a mature lib).
- ja/zh: untouched for 2.0; revisit post-release.