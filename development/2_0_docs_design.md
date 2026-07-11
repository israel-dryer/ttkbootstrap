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
| **User Guide** | tutorial + how-to + explanation | Getting Started · Concepts (styling core) · Feature guides (2.0 subsystems) · How-To |
| **Widgets** | (task/reference hybrid) | the visual catalog — grouped native vs. shipped |
| **Reference** | reference | **Style Reference** (generated) + **API Reference** (mkdocstrings) |
| *(supporting)* | — | Release Notes (link to GH releases), optional Roadmap |

### Governing principle + band charters (locked 2026-07-11)

**"We teach tkinter, in the ttkbootstrap dialect."** The User Guide is authored as
a place a reader can *learn tkinter*, start to finish, and may never consult
another source. The **software** stays a styling library (no scope change — a ttk
extension, no new widgets); the **docs** take on the second mission of being a
self-sufficient tkinter learning resource. The two don't conflict: teaching
tkinter well *is* teaching how to drive the thing ttkbootstrap styles, and every
example is `import ttkbootstrap as ttk`, so a reader learns both at once.

**This supersedes the earlier "welcoming on-ramp, NOT a tkinter tutorial, link
out for the real content" guardrail** (kept below for history). New posture:

- **Teach, don't defer.** The explanation lives *in* the docs. Link-outs
  (python.org, Tk man pages) are for exhaustive API enumeration and "further
  detail" — never the primary teacher.
- **Comprehensive ≠ exhaustive-on-every-page.** Teach the common 80% thoroughly;
  link the long tail. Depth where a beginner actually stumbles.
- **The dialect carries it** — `ttk.` widgets, fluent geometry, blessed tk
  widgets throughout.

**Band charters** — every page must pass its band's test (overlap between bands
is fine when it is *intentional*: a concept taught once, applied elsewhere):

The bands sort primarily by **altitude/depth**, not by topic — the same subject
can legitimately appear at more than one altitude:

| Band | Owns | Test |
|---|---|---|
| **Getting Started** | Onboarding: install → first window → app skeleton → migrate | "Is this first-hour setup?" |
| **Fundamentals** | The essential understanding needed to build a styled, themed app — tkinter mechanics *and* the ttkbootstrap styling/theming model, at a beginner altitude; each page hands off to a Feature guide / catalog / Reference for depth | "Is this the minimum a beginner needs to *understand* to build?" |
| **Feature guides** | The **in-depth** treatment of a subsystem — the full concepts + usage a Fundamentals intro only gestures at | "Is this the complete, deep version of a topic?" |
| **How-To** | A **specific task**, applied, minimal concept | "Does it answer 'how do I do X'?" |

**"Concepts" band dissolved (2026-07-11).** It mixed pure mental models
(bootstyle grammar, delivery), a subsystem (theming), and tasks/toolkits (make
your own style/theme) — three altitudes in one bucket. Resolution: the
*conceptual essentials* (bootstyle grammar, how styling is delivered, how theming
works) move to **Fundamentals**; the *deep usage/authoring* (theming, custom
styles, custom themes, color ramps) become **Feature guides**. Nothing is
homeless: the only cross-cutting idea (the bootstyle grammar) is foundational, so
it sits in Fundamentals.

**Fundamentals ⊂ Feature guides, by depth.** Fundamentals is deliberately a
*light, essential subset*: it teaches just enough of a topic to understand it and
start building, then links to the fuller treatment. A topic can have **both** — a
Fundamentals intro *and* an in-depth Feature guide — and that overlap is intended,
not redundant (e.g. Fundamentals *styling with bootstyle* → the *Custom styles*
guide; Fundamentals *how theming works* → the *Theming* guide; a Fundamentals
*events* intro → a *concurrency* guide). The Fundamentals page always points
onward to the depth.

**The guide↔how-to split (the repeatable pattern):** a feature guide teaches a
subsystem's concepts *and* usage in depth; the matching How-To applies them to one
concrete task. Feature-*scoped* concepts live in the feature guide (e.g. window
focus/modality/lifecycle → Windows guide). Precedent set 2026-07-11 by splitting
window focus/modality (Windows guide) from the *Multiple windows* recipe (How-To).

### User Guide internal structure — FOUR BANDS, Concepts dissolved (CURRENT, 2026-07-11)

**This is the live structure** (supersedes the FIVE/FOUR-band notes below, kept
for history). Bands sort by altitude: **Getting Started · Fundamentals *(flat)* ·
Feature guides · How-To.** Concepts is dissolved (see the charter note above).

```
User Guide
├─ Getting Started            ← onboarding + the tutorial spine
│   ├─ Installation
│   ├─ Quickstart             first themed window; App vs Tk; pick a theme
│   ├─ Build your first app   ★ NEW — end-to-end guided tutorial
│   ├─ Structuring an app     App vs Tk, single-root rule, app skeleton
│   └─ Migrating to 2.0
├─ Fundamentals — the essentials to understand & build (FLAT; ~8 pages)
│   │   ‹tkinter mechanics›
│   ├─ How a tkinter app runs   ★ the run/event loop; after; update vs update_idletasks
│   ├─ The widget model         ★ the tree, options, configure/cget, ttk state()
│   ├─ Arranging widgets        pack/grid/place + fluent geometry (flesh out)
│   ├─ State & variables        Var classes, textvariable binding, traces
│   ├─ Events & callbacks       command=, bind, virtual events, after
│   │   ‹ttkbootstrap styling & theming essentials›
│   ├─ Styling with bootstyle   ★ FLAGSHIP model — the grammar + reference table
│   ├─ How styling is delivered  blessed subclasses, enable_global_api, bootify
│   └─ How theming works         the semantic-anchor conceptual framework
├─ Feature guides — use it, in depth (each = its concepts + usage; OPEN set)
│   ├─ Theming                 switch/theme_mode/catalog/custom themes/color ramps
│   ├─ Custom styles           the style-construction toolkit (née "make your own style")
│   ├─ Typography              Fonts, set_global_family
│   ├─ Localization            L(), LocaleVar, set_locale, <<LocaleChanged>>
│   ├─ Input validation        add_*_validation, @validator
│   ├─ Icons                   icon=, apply_icon, Icon, glyph discovery
│   ├─ Windows & high-DPI      App/Toplevel, focus/modality/lifecycle, DPI
│   └─ Dialogs                 ★ Messagebox/Querybox/date/font/color pickers
└─ How-To — specific-task recipes (see §14 for the list)
```

- **Flagship = the bootstyle grammar** ("Styling with bootstyle") — still leads
  the Landing hero + Quickstart; it now sits in Fundamentals rather than as page
  one of a Concepts band. A returning tkinter user reaches it via Landing/
  Quickstart; a newcomer reaches it via the "read in order" path.
- **Fundamentals is FLAT** (no sub-groups in the nav) for scannability; the two
  informal clusters above (tkinter mechanics / styling essentials) are authoring
  order, not nav structure.
- **Each Fundamentals styling/theming page hands off** to its deep Feature guide
  (bootstyle → Custom styles; theming concept → Theming).

### User Guide internal structure — FIVE BANDS (revised 2026-07-11) — HISTORICAL

**Revision 2026-07-11 — added a `Foundations` band (author call).** With the
Concepts styling band authored, review found newcomers arriving with no tkinter
experience have no *conceptual* on-ramp: they jump from Getting Started straight
into advanced styling with no grasp of how widgets are arranged, how UI binds to
data, or how it responds to input. Those are mental models (not tasks), so they
belong in the guide as concepts, not only as How-To recipes. Added a small
**Foundations** band between Getting Started and Concepts (3 pages: *Arranging
widgets*, *State & variables*, *Events & callbacks*). **Scope guardrail:** keep
them concept-level and ttkbootstrap-flavored, and link out to python.org's
`tkinter`/`tkinter.ttk` reference for exhaustive detail (the same see-also pattern
used for ttk styling internals) — a welcoming on-ramp, NOT a tkinter tutorial that
turns the library into a widget library. **bootstack's docs are a useful reference
for this band.** The four-band note below is kept for history.

### User Guide internal structure — FOUR BANDS (revised 2026-07-10)

Revised after the compat-and-utilities pass (Slices 0–5) and the other 2.0
non-widget additions landed — the original two-band plan (5 Concepts + a vague
How-To) had nowhere to teach the delivery model, fonts, localization,
validation, or windowing. Adopts bootstack's proven **four-band** shape (Getting
Started · Concepts · Feature guides · How-To), scoped down to a *styling
extension* (its framework-only bands — signals/store/streams/CLI/hot-reload —
are dropped). Two author decisions locked the shape (2026-07-10): **adopt the
four-band structure**, and **teach generic tkinter tasks "ttkbootstrap-flavored"**
in How-To (every example uses ttkbootstrap idioms and links out to python.org for
the raw tk API) — this is the concrete fill for the "modern tkinter docs" gap.

```
User Guide
├─ Getting Started              ← the tutorial path
│   ├─ Installation            pip, requires-python >=3.10
│   ├─ Quickstart              first themed window; Window vs Tk; choosing a theme
│   ├─ Structuring an app      Window vs Tk, the single-root rule, an app skeleton
│   └─ Migrating to 2.0        bootstyle strings, theme names, removed shims, icons
├─ Foundations — tkinter mental models for newcomers (NEW 2026-07-11)
│   ├─ Arranging widgets        pack/grid/place — the model + when to use which;
│   │                             fluent geometry (.pack() returns the widget)
│   ├─ State & variables        StringVar/IntVar/BooleanVar + textvariable/variable
│   │                             binding (observer pattern); LocaleVar as example
│   └─ Events & callbacks        command=, bind + event objects, virtual events
│                                 (<<…>>, e.g. <<ThemeChanged>>), after()
├─ Concepts — the styling core (the FLAGSHIP band)
│   ├─ The bootstyle grammar   ★ FLAGSHIP — canonical grammar + reference table
│   ├─ How styling is delivered ★ NEW — no monkey-patch: blessed subclasses,
│   │                             BootMixin/AutoStyleMixin, enable_global_api,
│   │                             bootify, apply_bootstyle, fluent geometry
│   ├─ Theming                 semantic-anchor model + 2-column light/dark gallery
│   ├─ Working with color      style.colors, ramp addressing (c.primary[300])
│   ├─ Make your own style     ☆ the custom-style toolkit + icon engine
│   └─ Make your own theme     Theme() API + ttkcreator
├─ Feature guides — 2.0 subsystems (each a utility we shipped)
│   ├─ Typography              Fonts, set_global_family over the named fonts
│   ├─ Localization            L(), LocaleVar, set_locale, <<LocaleChanged>>
│   ├─ Input validation        add_*_validation, @validator
│   └─ Windows, icons & DPI    App/Toplevel, positioning, apply_icon,
│                                enable_high_dpi_awareness, window_type; the
│                                deferred-config seam as a sidebar
└─ How-To — short task recipes (absorbs Cookbook; ttkbootstrap-flavored tkinter)
    layout (pack/grid/place) · events & variables · menus & context menus ·
    images & PhotoImage · scrollable content · message boxes & dialogs ·
    multiple windows · background work without freezing the UI (after + threads) ·
    splash screen · app icon · validate a form · animate a GIF (salvaged)
```

- **Flagship = the bootstyle grammar** — leads the Landing hero and the User
  Guide (the universal "how do I style anything" front door). **How styling is
  delivered** sits second: it is the single biggest 2.0 conceptual shift
  (`import ttkbootstrap` no longer monkey-patches tkinter). *Make your own
  style/theme* remains a prominent act (the biggest *new* 2.0 capability).
- **Feature guides** is the NEW band that homes the shipped non-widget utilities
  end-to-end (typography, localization, validation, windowing); keeping them out
  of Concepts leaves the styling band uncluttered.
- **Themes** is folded here as the *Theming* guide; its gallery renders the 30
  themes as **light/dark pairs in a 2-column layout**.
- **Cookbook** is removed; its pages become **How-To** entries. The How-To band
  also gap-fills the common *generic-tkinter* tasks newcomers arrive needing
  (layout, events, threading, menus, images), each written ttkbootstrap-flavored.
- **Gallery** (real-app demos) is removed for 2.0; can return later.

**Authoring conventions (locked 2026-07-10, apply to every page):**
- **Lead with ``App``, not ``Window``.** ``App`` is the actual class; ``Window``
  is a permanent alias (``window.py`` `Window = App`). Prose and code examples
  teach ``ttk.App(...)`` as canonical and mention ``ttk.Window`` once as the
  alias. (Existing skeleton pages were swept to match.)
- **Use fluent geometry in examples where appropriate.** ``pack``/``grid``/
  ``place`` return the widget (2.0 `FluentGeometryMixin`), so construct-and-place
  in one expression — ``ttk.Button(app, text="Save").pack(...)`` — whenever the
  example does not need to keep a reference. Showcases a real 2.0 ergonomic.
- **Annotate cross-platform gotchas where relevant.** tkinter behaves
  differently across Windows/macOS/Linux, and a learner treating these docs as
  their only source must be warned. Call out platform differences inline (a
  `.. note::`/`.. warning::` admonition) *when they affect the reader* — e.g.
  macOS menu/aqua behavior and the app menu, `MouseWheel` `event.delta`
  direction/scale differing by platform, cursor names mapping to different
  glyphs (and Windows accepting any name silently), high-DPI/scaling, native
  file-dialog chrome, `bell` being the platform alert sound, `window_type`/
  `override_redirect` aqua no-ops. Ground-truth the claim (test where possible,
  or cite Tk docs); don't hand-wave "may vary." Precedent: the Cursors and
  Feedback pages already do this.

## 4. The native / shipped dichotomy — where it lives (revised 2026-07-10)

ttkbootstrap has a split bootstack doesn't: **native ttk widgets it *styles***
(Button, Entry, Combobox, Treeview…) vs. **widgets it *ships*** (Meter,
Floodgauge, DateEntry, Tableview, ScrolledFrame, tooltip, toast, dialogs).

Two orthogonal axes:
- **Axis A — widget kind:** native (no ttkbootstrap Python API) vs. shipped (real
  authored API).
- **Axis B — page purpose:** catalog/usage vs. manual-styling reference vs. API
  reference.

**Resolution — the split lives in the *references*, NOT the catalog (revised).**
The original design grouped the Widgets catalog itself by Axis A ("Styling ttk
widgets" / "ttkbootstrap widgets"). That was reversed 2026-07-10 (author call):
the catalog is *usage guides* — set ``bootstyle``, pick a variant/color, handle
states — and that recipe is identical for native and shipped widgets, so the
split adds friction without meaning there. Where the distinction *does* pay off,
it already has its own section:
- The **Widgets catalog** is **one unified list** of usage guides, uniform shape,
  no native/shipped grouping. Each page ends with an **API link that points where
  the API actually lives** — python.org's ``tkinter.ttk`` for a native widget,
  the **API Reference** for a shipped one — plus a link to the deep **Style
  Reference**.
- A widget's *depth* still lands on exactly one reference side: native → **Style
  Reference** (the ttk styling surface); shipped → **API Reference** (the authored
  API). Those two references *are* where Axis A is expressed.
- "Make your own style" (Concepts) is a third, separate section; unifying the
  catalog does not touch it.

## 5. Page templates (with worked examples)

### 5a. Widgets catalog page — one shared skeleton (every widget)

```
<Widget>
  one-liner
  [ light screenshot ] [ dark screenshot ]        ← all color variants
  ## Usage             → lead: what the widget is FOR + the common pattern that
                          drives it (e.g. Button → wire an action with command=),
                          as a real runnable example — NOT styling
  ## Semantic styling  → bootstyle + copy-paste minimal example
  ## <pattern sections>   one section PER common pattern/option, each a runnable
                          snippet + light/dark screenshot (see below)
  ## Colors                (swatch strip, light+dark)
  ## States                (disabled/active/… where relevant)
  → PRIMARY link: the usage/API reference — tkinter.ttk options (native) or
    API Reference (shipped)
  → SECONDARY link: Style Reference, framed as "want to restyle it yourself?"
    (customization/advanced — see §5b), not the default "learn more"
```

Same skeleton regardless of widget kind — this is what makes 30+ pages read as
one system.

**Widget pages are USAGE pages, not styling catalogs (author note 2026-07-11).**
The current `docs/widgets/button.rst` prototype is **sorely lacking** — it shows
`bootstyle` values but never shows *using* a Button (no `command=`, no real
patterns). Model the depth on **bootstack's** widget pages
(`D:/Development/bootstack/docs/widgets/button.rst`): open with a **Usage**
section ("a button runs an action — wire it with `command=`"), then a **section
per common pattern**, each a runnable example + a light/dark screenshot pair.
bootstack's Button, for reference, covers: Usage · Accent colors · Style variants
· Icons · Icon position · Icon-only · Uniform width · Compact density · Disabled.
The ttkbootstrap equivalent should cover the analogous real patterns — `command=`
wiring, `icon=`/icon-only (2.0), a uniform-width button row, a toolbar, default
button (`Return`), enable/disable — *then* the bootstyle/colors surface. Applies
to **every** widget page: teach how to *use* the widget first, style it second.
(Not part of Fundamentals; slots into the Widgets-catalog authoring phase.)

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

**Framing — this is the CUSTOMIZATION surface, not a normal-usage reference
(author note 2026-07-11).** The Style Reference answers *"I want to hand-customize
the style myself"* — element layouts, configurable options, state maps. It is
**not** what a typical user reaches for to *use* a widget; that path is the
widget's **Usage page** (§5a) plus its `tkinter.ttk` constructor options. So:
frame it as **advanced/customization**, and pair it with the **Custom styles**
feature guide (its natural companion). The generator's index intro should say so
(it's generated — update the generator, not the committed rST). On a widget
catalog page, the Style-Reference cross-link is the *"want to restyle it
yourself?"* link — deliberately secondary to the usage/API link, not the default
"learn more."

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
3. **User Guide** — the four-band IA (revised §3): Getting Started (Installation,
   Quickstart rewrite, Structuring an app, Migrating), Concepts (6 styling guides,
   flagship + delivery-model first), Feature guides (typography, localization,
   validation, windowing), How-To (salvage cookbook + ttkbootstrap-flavored
   generic-tkinter recipes). The IA skeleton (index + honest stubs) lands as a
   fast-follow to sub-PR 1; prose fills in per band.
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

## 12. "tkinter essentials" reference/guide strand (added 2026-07-11)

Filling the *modern-tkinter-docs* gap (§1) is a first-class goal, and much of Tk's
own material lives only in C-oriented man pages. This strand restates that material
in Python terms — **ttkbootstrap-flavored, always linking out** to python.org /
Tk for exhaustive detail (a welcoming reference, NOT a tkinter fork). The split,
locked with the author, mirrors Diátaxis:

- **Reference = the names / catalog** (tables of tokens, attributes, options).
- **Guide = the usage** (how to bind, generate, keep a reference, etc.).

**Landed (uncommitted):** the **Event reference** (`reference/events/`: index +
event-types, modifiers-and-keys, event-object, event-generate-options,
virtual-events) + the expanded **Events & callbacks** guide
(`foundations/events-and-callbacks.rst`) + the **Working with images** How-To.

**Roadmap (author-requested; recommended order winfo → cursors → usage guides):**

| Topic | Home | Notes |
|---|---|---|
| `winfo_*` widget & screen info | **Reference** (new table page) | Highest-value next; undocumented-in-friendly-form |
| Cursors + `bell`/`busy` | cursor-names **Reference** table; feedback **guide** | Cursor list is another "exists nowhere" table |
| Focus, modality & lifecycle (`focus`/`grab`/`lift`/`lower`/`destroy`/`WM_DELETE_WINDOW`) | **Guide** — extend *Windows, icons & DPI* | Mostly usage |
| Clipboard & selection (`clipboard_*`/`selection_*`) | **How-To** | Small recipe |
| Error handling (`report_callback_exception`, `TclError`) | **How-To** | Pairs with the threading recipe; documents the swallowed-exception gotcha |
| `bindtags` | **Done** (events guide) | Ref stub optional |

### 12a. Image handling decision (2026-07-11)

- **`ttk.PhotoImage` stays `tkinter.PhotoImage`.** Re-pointing it to
  `ImageTk.PhotoImage` was considered and **rejected**: empirically not a drop-in
  — base64 `data=` raises `UnidentifiedImageError`, it is not a subclass (breaks
  `isinstance`), it drops ~18 methods (`put`/`get`/`zoom`/`subsample`/`copy`/
  `configure`/`cget`/…), and it does **not** fix GC anyway (it wraps a
  `tk.PhotoImage` whose `__del__` frees it; the Python wrapper must still be held).
- **Docs approach (now):** the *Working with images* How-To documents the GC
  keep-a-reference gotcha (applies to both classes) and **recommends Pillow**
  (`ImageTk.PhotoImage`) for real image work — the "use the PIL version" guidance
  delivered as a recommendation, not a class swap.
- **2.1 candidate (design pass required):** a bootstack-style **`Image` handle**
  (`D:/Development/bootstack/src/bootstack/images.py`) — a PIL-based handle that
  owns its `PhotoImage`; the blessed widgets keep the handle, so GC-safety is
  structural (widget → handle → photo). A NEW, distinctly named export (not a
  reused `PhotoImage`); must NOT duplicate the font-glyph `Icon`/`icon_element`/
  `apply_icon` engine. Auto-ref-keeping needs our widget classes to own `image=`,
  so it brushes the utilities-not-widgets boundary — a conscious call, deferred.

## 14. The complete User Guide curriculum — the "learn tkinter" plan (2026-07-11)

Planned end-to-end against the governing principle (§3): the User Guide is *the*
place to learn tkinter, in the ttkbootstrap dialect. This section is the working
map — the pages a complete curriculum needs, their band, and their status. It
supersedes the older per-band sketches for the User Guide's *completeness*
(individual page templates in §5 still apply).

**This map is a living target, not a closed checklist.** No band is "done" until
a reader can actually learn the framework from it; re-audit every band for gaps as
the rest fills in. Statuses below are a snapshot, and the page *set* — especially
Feature guides — is expected to grow.

**Audience & promise.** The reader is a Python developer — often a
scientific/utility/tools author ([[project_user_base]]) — who wants to *build a
desktop UI and understand the framework for doing so*, possibly with no other
tkinter source. By the end they can: lay out a window, choose and drive the right
widgets, manage state, wire behavior, use the common widgets (including the hard
ones — Text, Canvas, Treeview/Tableview), open windows and dialogs, style it all,
and grasp *why* it works (the event loop, the widget tree).

**Status key:** ✓ authored · ~ partial · ⊘ stub · + planned (in current IA) ·
★ NEW-proposed here.

### Coverage audit — against the tkinter surface + desktop-UI expectations (2026-07-11)

Because the docs teach tkinter itself, completeness is judged against **what
tkinter actually ships** and **what any desktop UI needs**, not just the 2.0
additions. Grounded in the stdlib surface: tkinter's dialog submodules
(`filedialog`, `colorchooser`, `messagebox`, `simpledialog`, `font`,
`scrolledtext`, `dnd`) and the **tk-only widgets with no ttk version**
(*Canvas, Listbox, Menu, Text, Message*). The canonical categories a desktop-UI /
tkinter learner expects, and where each is homed:

| # | Category | Home | Status / gap |
|---|---|---|---|
| 1 | Widgets — inputs & choices (Label/Button/Entry/Check/Radio/Combobox/Spinbox/Scale/OptionMenu) | Widgets catalog | structure ✓, pages pending |
| 2 | Widgets — containers & layout (Frame/LabelFrame/Panedwindow/Notebook) | Widgets catalog | pending |
| 3 | Widgets — collections & data (Treeview, **Listbox**, Tableview) | Widgets catalog (deep) | **Listbox easily missed — no ttk version** |
| 4 | Widgets — text & drawing (**Text, Canvas**) | Widgets catalog (deep) | big tkinter topics; tk-only, hand-authored. (`Message` is legacy — superseded by `Label(wraplength=…)`; omit.) |
| 5 | Widgets — indicators & feedback (Progressbar/Meter/Floodgauge/Toast/ToolTip/Separator/Sizegrip/Scrollbar) | Widgets catalog + *Feedback* | Progressbar/Meter etc. pending |
| 6 | **Menus & menubars** (Menu, Menubutton) | How-To + catalog | + planned; a fundamental category |
| 7 | Layout & geometry (pack/grid/place) | Fundamentals | ~ (flesh out) |
| 8 | Events, bindings & protocols | Fundamentals + Reference | ✓ |
| 9 | State, variables & data binding | Fundamentals | ✓ |
| 10 | Input validation | Feature: Validation | ⊘ |
| 11 | Windows: focus/modality/lifecycle/DPI | Feature: Windows | ~ |
| 12 | **Standard dialogs** (file/color/message/font/simple + Querybox/Messagebox) | Feature: Dialogs | ★ — **`filedialog` is a real gap** (see below) |
| 13 | Fonts & typography | Feature: Typography | ⊘ |
| 14 | Images | How-To | ✓ |
| 15 | Icons (glyphs) | Feature: Icons | ✓ |
| 16 | Styling & theming | Fundamentals + Theming | mixed |
| 17 | App lifecycle & the run loop | Fundamentals | ★ |
| 18 | Concurrency (threads + `after`) | How-To (feature candidate) | + |
| 19 | Clipboard & selection | How-To | ★ |
| 20 | Scrolling (Scrollbar wiring, ScrolledText/Frame) | How-To (feature candidate) | + |
| 21 | Keyboard nav, focus traversal, accelerators, mnemonics | **unhomed** | **gap — decide a home** |
| 22 | Cursors & pointer feedback | Reference + *Feedback* | ✓ |
| 23 | Introspection (`winfo_*`) | Reference | ✓ |
| 24 | Error handling (`report_callback_exception`, `TclError`) | How-To | ★ |
| 25 | Localization / i18n | Feature: Localization | ⊘ |
| 26 | Drag & drop (`tkinter.dnd`; external `tkdnd`) | **scope call** | teach-lite + link out (weak in core) |
| 27 | Persistence/settings · packaging/distribution | **scope call** | app-level; brief How-To or link out |
| 28 | Accessibility | **scope note** | tkinter is limited; document honestly, don't overpromise |

**Supersession — teach the ttkbootstrap version, not the tkinter original.**
"Teach tkinter in the dialect" means: where ttkbootstrap ships a *superseding*
version, that version **is** the dialect — teach it as primary, and mention the
stdlib original only as "what it replaces (don't reach for it)." Confirmed map:

| tkinter original | ttkbootstrap supersedes with | teach |
|---|---|---|
| `messagebox` | `Messagebox` (show_info/error/…, ok/okcancel/yesno) | ttkbootstrap |
| `simpledialog` (askstring/askinteger/askfloat) | `Querybox` (get_string/get_integer/get_float/get_item) | ttkbootstrap |
| `colorchooser` (askcolor) | `ColorChooserDialog` / `Querybox.get_color` (+ `ColorDropperDialog`) | ttkbootstrap |
| font dialog | `FontDialog` / `Querybox.get_font` | ttkbootstrap |
| `scrolledtext` | `ScrolledText` (+ `ScrolledFrame`) | ttkbootstrap |
| *(no stdlib equiv)* | `DatePickerDialog` / `Querybox.get_date` | ttkbootstrap |
| **`filedialog`** | **not superseded** (native OS dialogs; only used internally by Tableview) | **stdlib `filedialog`** |

Not superseded — **teach the tkinter widget, styled** (ttkbootstrap has no
replacement, only styling): **Text, Canvas, Menu, Listbox**, Progressbar
(Meter/Floodgauge are *additions*, not replacements). (`Message` is legacy —
`Label(wraplength=…)` replaced it; omit from the catalog.)

**Concrete gaps this surfaced (act on these):**
- **`filedialog`** (open/save/choose-directory) — the **one** standard dialog
  ttkbootstrap does *not* supersede, essential for desktop apps, and currently
  unaccounted-for. The **Dialogs** guide teaches the ttkbootstrap dialogs as
  primary (per the map above) **and `filedialog` as the stdlib you still reach
  for**. Everything else stdlib is "replaced — don't use."
- **Listbox** — a native tk widget with **no ttk equivalent**; easy to omit from a
  ttk-centric catalog. Explicitly include it.
- **Text / Canvas / Menu / Listbox** — tk-only, so they won't fall out of ttk
  introspection; they need deliberately hand-authored catalog pages. (`Message` is
  omitted as legacy — `Label(wraplength=…)` replaced it.)
- **Keyboard navigation & focus traversal** (tab order, `takefocus`, accelerators,
  mnemonics, `Return`-to-default) — a baseline desktop-UI expectation with no home.
  Decide: a Fundamentals subsection (basics) + a feature/how-to for depth.

**Scope boundaries (intentional gaps, decide once):** drag-and-drop
(core is weak — teach the basics, link `tkdnd`), packaging/distribution and
settings-persistence (app-level, not tkinter — a short How-To or link out), and
accessibility (document tkinter's real limits honestly). Marking these keeps a
gap from reading as an oversight.

### Getting Started — onboarding + the tutorial spine

| Page | Status | Scope |
|---|---|---|
| Installation | ✓ | pip, Python 3.10+ |
| Quickstart | ✓ | first themed window; `App` vs `Tk`; pick a theme |
| **Build your first app** | ★ | A guided **end-to-end tutorial** (Diátaxis's weak leg today): a small but complete app — a form + a data table, say — touching layout, widgets, events, state, and styling. The learning-by-doing spine newcomers need. |
| Structuring an app | ✓ | `App` vs `Tk`, single-root rule, app skeleton |
| Migrating to 2.0 | ✓ | bootstyle strings, theme names, removed shims, icons |

### Fundamentals — the essentials to understand & build (FLAT, the CORE expansion)

The *essential* understanding needed to build a styled, themed app — a light
subset at a beginner altitude, each page handing off to its deeper home (a Feature
guide, the Widgets catalog, or Reference) rather than exhausting the topic. This
band carries the "understand the framework" half of the promise and is the biggest
gap. **Flat** (no nav sub-groups); the two clusters below are authoring order.
Pages, in learning order (each links onward to depth):

*tkinter mechanics:*

| Page | Status | Scope |
|---|---|---|
| **How a tkinter app runs** | ✓ | The run model: the root, `mainloop`, the **event loop**, callbacks-run-your-code, `after`/idle tasks, `update` vs `update_idletasks`, when the UI actually draws. The single most important mental model. → depth: *Concurrency* guide. |
| **The widget model** | ✓ | What a widget *is*: the master/child tree, widget paths, common options (`text`/`width`/`state`/`cursor`/`takefocus`…), `configure`/`cget`/`widget["opt"]`, ttk `state()`/`instate()`, enable/disable. → depth: the Widgets catalog. |
| Arranging widgets | ~ | pack/grid/place + fluent geometry — **flesh out** (bootstack-modeled): nesting frames, `sticky`/`weight`/resize behavior, when to use which. [[project_arranging_widgets_docs_flesh_out]] — the #1 beginner wall. |
| State & variables | ✓ | Var classes, `textvariable`/`variable` binding, `trace_add`/`remove`; `LocaleVar` as an example (defers to Localization). |
| Events & callbacks | ✓ | `command`, `bind`, event objects, bindtags, virtual events, `after`. |

*ttkbootstrap styling & theming essentials* (relocated from the dissolved
Concepts band; content largely reused, reframed as essentials that hand off):

| Page | Status | Scope |
|---|---|---|
| **Styling with bootstyle** | ✓ (relocate) | ★ FLAGSHIP model — the canonical grammar + reference table. → depth: *Custom styles* guide. |
| How styling is delivered | ✓ (relocate) | blessed subclasses, `enable_global_api`, `bootify`, `apply_bootstyle`. |
| **How theming works** | ~ (split) | The **semantic-anchor conceptual framework** — the concept half of today's *Theming* page. → depth: *Theming* guide (usage). |

### Feature guides — subsystems, in depth (concepts + usage; OPEN set)

**The set below is open, not closed** — don't assume this is the full list. A
"subsystem" earns a guide when it's a nameable, reusable capability with its own
concepts. Beyond the table, candidates to evaluate (promote from How-To to guide,
or add fresh, when they warrant concept-level treatment): **Scrolling**
(ScrolledFrame/Text + native scrollbar wiring), **Menus & menubars**,
**Concurrency** (threads + `after`, keeping the UI responsive), **Keyboard &
focus traversal** (tab order, accelerators, mnemonics), **Feedback/notifications**
(ToolTip/Toast as a family), **Clipboard & drag-and-drop**. Revisit this list
every few slices rather than treating it as fixed.

| Page | Status | Scope |
|---|---|---|
| **Theming** | ✓→~ (recompose) | The theming subsystem *usage*: switch themes, `theme_mode`/light-dark, the 30-theme catalog, **color ramps** (`style.colors`, `c.primary[300]`), and **custom themes** (`Theme()` + ttkcreator). Absorbs today's *Theming* usage + *Working with color* + *Make your own theme*. Concept half → Fundamentals *How theming works*. |
| **Custom styles** | ✓ (relocate) | The style-construction toolkit (Assets, layouts, elements, `icon_element`) — née *Make your own style*. |
| Typography | ⊘ | `Fonts`, `set_global_family` over the named fonts — **author** |
| Localization | ⊘ | `L()`, `LocaleVar`, `set_locale`, `<<LocaleChanged>>` — **author** |
| Input validation | ⊘ | `add_*_validation`, `@validator` — **author** (pairs with a "validate a form" How-To) |
| Icons | ✓ | `icon=`, `apply_icon`, `Icon`, glyph discovery |
| Windows & high-DPI | ~ | focus/modality/lifecycle ✓; **finish**: constructor surface, positioning, light/dark `theme_mode`, Toplevel options, high-DPI, deferred-config seam |
| **Dialogs** | ★ | The shipped-dialog subsystem — `Messagebox`, `Querybox`, date/font/color pickers: how to call them, what they return, modality. Currently homeless (scattered across How-Tos + API ref). |

### How-To — specific tasks (recipes, not re-teaching)

Generic "lay out widgets" / "wire events" are **dropped** — Foundations owns
those; a How-To is a *specific* task. Keep and add:

| Page | Status |
|---|---|
| Working with images | ✓ |
| Feedback: bell & busy | ✓ |
| Multiple windows & modal dialogs | ✓ |
| Menus & context menus | + |
| Make content scrollable | + |
| Validate a form | + (pairs with Validation guide) |
| Background work without freezing the UI (`after` + threads) | + |
| Animate a GIF | + (salvaged from cookbook) |
| Splash screen | + |
| Set the application icon | + |
| Clipboard & selection | ★ (essentials strand) |
| Handle callback errors (`report_callback_exception`, `TclError`) | ★ (essentials strand) |

### The complex widgets — where "learn tkinter" gets deep

Text, Canvas, and Treeview are large, essential tkinter topics; the shipped
Tableview/Meter/DateEntry/etc. are their ttkbootstrap counterparts. **Their
teaching home is the Widgets catalog** (§4), where each widget's page goes as
deep as the widget warrants — a `Button` page is short; a `Text` page teaches
tags/marks/indices, a `Canvas` page teaches items/coords/tags, a `Treeview` page
teaches columns/selection/sorting. Fundamentals' *widget model* + a short **widget
toolbox** orientation (what each widget is for) link into the catalog. This keeps
one home per widget and avoids a second widget-docs axis in the User Guide.

### Suggested authoring order (highest learner-value first)

1. **Fundamentals core** — *How a tkinter app runs*, *The widget model*, and the
   *Arranging widgets* flesh-out. (Unblocks everything; biggest gap.)
2. **Recompose the styling/theming pages** into the new shape — relocate
   *bootstyle grammar* + *delivery* to Fundamentals; split the *How theming works*
   concept out; fold today's *Theming*/*Working with color*/*Make your own theme*
   into the **Theming** feature guide; *Make your own style* → **Custom styles**
   guide. (Mostly moves of authored content; low risk, high IA payoff.)
3. **Finish the essentials strand** — winfo ✓ / cursors ✓ done; add clipboard and
   error-handling How-Tos.
4. **Author the feature-guide stubs** — Typography, Localization, Validation;
   finish Windows.
5. **Dialogs guide** + the *Validate a form* / *Menus* / *Scrollable* / *Threads*
   How-Tos.
6. **Getting Started tutorial** — *Build your first app* (ties the above
   together; best written once the pieces it references exist).
7. **Widgets catalog depth** — the Text/Canvas/Treeview/Tableview pages (separate
   destination; large, ongoing). **Usage-first** per §5a: every page opens with
   real usage (`command=` wiring, common patterns) before styling; rework the
   `button.rst` prototype to bootstack's depth. Include the tk-only widgets
   (Text/Canvas/Menu/Listbox) and don't drop `Listbox`.

### A visible learning path

Surface a linear "**New to tkinter? Read in this order**" path on the User Guide
landing: Getting Started → Fundamentals → *Build your first app* → the feature
guides/how-tos as needed. A newcomer should never have to guess the sequence.

## 13. Open / deferred

- Style Reference: one page per widget family vs. one big generated table (lean:
  per-family, browsable).
- "Working with color" as its own guide vs. a section of *Make your own style*
  (lean: keep small standalone; the ramp API is a clean new feature).
- Roadmap page: include or omit (bootstack has one; optional for a mature lib).
- ja/zh: untouched for 2.0; revisit post-release.