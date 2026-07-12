# CLAUDE.md

Guidance for working in the ttkbootstrap repository.

## What this is

ttkbootstrap is a theming extension for tkinter/ttk: it generates modern,
flat, Bootstrap-inspired themes on demand and adds a `bootstyle` keyword
API to ttk widgets. Pure Python; the only runtime dependency is Pillow
(used for image-based widget assets). Public API entry point is
`src/ttkbootstrap/__init__.py`, typically imported as `import ttkbootstrap as ttk`.

- Package version / metadata: `pyproject.toml` (src layout, `requires-python >=3.10`).
- Docs site: mkdocs (`mkdocs.yml`, `docs/`), published to readthedocs.

## Direction: 2.0 cleanup (read before large changes)

The active initiative is a **2.0 cleanup/consolidation release — no new
features.** Goals: remove cruft, standardize/normalize the API (aggressive/
breaking is OK when meaningful, paired with a migration path), fix memory leaks
and theme-switch perf, make user-defined custom styles easy, and overhaul the
docs. ttkbootstrap stays a **styling extension for vanilla tkinter** — not a
widget library (the forward-looking framework is a separate project, bootstack).

The full worklist (locked decisions + workstreams) lives in
**`development/2_0_plan.md`**, and the integration branch is **`2.0`** (cut PRs
against it, not `master`). Headlines: mixin-hybrid API (replace the import-time
monkey-patch), single canonical `bootstyle` string (no tuple/list/alt-order),
semantic-anchor theme model, deterministic version-stamped theme walk +
image-cache cleanup (mechanisms borrowed from bootstack, not its API), and a
centralized compat quarantine for all legacy normalization + deprecation
warnings. Consult that doc before starting 2.0 work.

**Current handoff state** (read `development/2_0_handoff.md` first): all the
independent cleanup slices are **merged** into `2.0` — deprecated top-level shims
removed + headless/demo test split (#1068), public/internal split (#1069),
widget lifecycle-leak fixes (Workstream B, #1070), `FloodgaugeLegacy` runtime
`DeprecationWarning` (#1071), and the `examples/` `test_`-prefix rename (#1072).
The engine keystone (Workstream A) is now in progress: the design is locked in
`development/2_0_engine_design.md`, and **PR 1 — the repaint engine** (version
-stamped theme walk replacing `Publisher`, lazy per-theme style rebuild,
single-root `RuntimeError`) is **merged** into `2.0` (#1073). **PR 2** — the
content-addressed image cache (`Style._image_cache` + `_get_or_create_image` +
`clear_image_cache`; per-builder `theme_images` leak removed) — is **merged**
into `2.0` (#1074). That **completes the engine (Workstream A) keystone**.
**PR 3** — the mixin API (Workstream C) — is **merged** into `2.0` (#1075): the
import-time monkey-patch is retired in favor of concrete
`BootMixin`/`AutoStyleMixin` subclasses re-exported from `__init__.py`, plus
`bootify`/`apply_bootstyle`/opt-in `enable_global_api`; the ~450-line
`TYPE_CHECKING` stub block + `__init__.pyi` are deleted. **PR 4** — the `style/`
package split (Workstream G) — is **merged** into `2.0` (#1076): `style.py`
became a `style/` package (`theme`/`builders_tk`/`builders_ttk`/`engine`/
`bootstyle`) via a pure, behavior-preserving move; `ttkbootstrap.style` stays a
valid public path (no shim). Design pass: `development/2_0_style_split_design.md`.
**PR 5** — the public style-construction toolkit (Workstream I, Tier 1) — is
**merged** into `2.0` (#1077): new `style/assets.py` (`Assets` facade —
`circle`/`rect`/`rounded_rect` recipes + an `image()` escape hatch wrapping PR
2's image cache, with keys *derived* from the render inputs and bootstack's
snapped/oversampled render pipeline) + `style/layout.py` (`El`/`layout`,
`image_element`, `statespec`/`state_map`, `StyleName`), re-exported from
`ttkbootstrap.style` and top-level `ttkbootstrap`. The scale + radiobutton
builders are migrated onto it as the acceptance proof. Design pass:
`development/2_0_toolkit_design.md`. The held **PR 6** (asset/layout fast-follow on
`feat/2.0-pr6-toolkit-migration`) was **superseded**: its hand-drawn glyphs
looked poor, so 2.0 instead **renders glyph-shaped assets from a vendored
Bootstrap Icons font** (metrics-based fit ported from bootstack; reuses the PR-5
pipeline + PR-2 cache; no new pip dep), per the API-locked design in
`development/2_0_icons_design.md`. **PR 6a** — the icon engine — is **merged** into
`2.0` (#1079): vendored `assets/icons/` font + `style/icons.py` (`IconRenderer`) +
`Assets.icon` + public `Icon` atom / `icon_element` state→icon sugar, re-exported
from `ttkbootstrap.style` and top-level `ttkbootstrap`; no builder changes, suite
89 passed. Render tuning (icon-specific 6×/3×/1× supersample + gentle 0.5/50
sharpen) and `record-circle-fill` for radio-on were settled via a live visual
spot-check; `examples/icon_preview.py` is the tool. **PR 6b** — the glyph-builder
migration — is **merged** into `2.0` (#1080): check/radio/toggle×2/date/arrows/
sizegrip wired onto `a.icon`/`icon_element` (six `create_*_assets` glyph methods
deleted), the held branch's geometric/`layout` cleanup landed, and the public
style-registration path added (`register_style` + `layout()` auto-registers — the
PR-6a finding). Two light↔dark spot-check rounds settled the arrows on solid
`caret-*-fill` (incl. menubutton + datepicker header), toggle sizing, and
`calendar3`; suite 92. That completes the Workstream I icon work. **Historical next:** an
optional small visual-polish PR (value/asset tweaks — see
`development/2_0_handoff.md` "FOLLOW-UP"), then theme/anchor (E) + bootstyle
canonical (D), each with a design pass first. Proceed PR by PR per the design doc;
don't exceed a PR's scope without revisiting it.

Recolorable raster widget assets (#1081), the modular `StyleBuilderTTK`
registry (#1082), and scaling/asset-geometry normalization (#1083) are now also
merged into `2.0`; the expected suite is 177 tests. The focused private color
ramps and `StyleBuilderTTK` helpers (#1085, merge commit `b7872a98`, per
`development/2_0_color_helpers_design.md`) are now also **merged** into `2.0`;
the expected suite is 189 tests. The fast-follow color-math PR (#1087, merge
commit `0218aba3`, per `development/2_0_color_math_followup_design.md`) is now
also **merged** — it retired the last 10 ad-hoc HSV/alpha sites onto mix-based
`shade`/`tint`/`mute` helpers (the AST guard now enforces zero raw color math in
ttk recipes); `elevate` and `input_bg` from the original stub were **dropped/
deferred to Workstream E** after ground truth invalidated them. Expected suite is
191 tests. **Workstream E (theme/anchor) is now COMPLETE** — the semantic-anchor
`Theme` model, curated 15-family/30-theme catalog, `install_legacy_themes()` +
16-key adapter, `Colors` resolved view + ramp addressing, the hue-correct
`inputbg` fix, and the ttkcreator `Theme` rework all merged (PRs #1088/#1089/
#1090; default theme is now `bootstrap-light`; expected suite 211). Design in
`development/2_0_theme_anchor_design.md`; migration guide (for the Workstream-H
docs rewrite) in `development/2_0_theme_migration.md`. **Workstream D (canonical
bootstyle grammar) is now COMPLETE** — three PRs merged into `2.0` (design in
`development/2_0_bootstyle_grammar_design.md`): D1 #1091 (closed-vocab tokenizer
replacing the substring regex + loud failure on unknown tokens; single vocab
source of truth in `constants.py`; new `style/_compat.py` quarantine with
`set_bootstyle_strict`/`TTKBOOTSTRAP_STRICT`), D2 #1092 (migrated every
first-party tuple caller — meter/dateentry/tooltip/datepicker + the two demos —
to canonical strings, then turned the tuple `DeprecationWarning` on), D3 #1093
(generated `BootStyle` `Literal` (107 strings) + reference table
`development/2_0_bootstyle_reference.md` from vocab × registry, via
`tools/generate_bootstyle_reference.py`, with sync tests). `BootType` fixed
(`round` added; `toggle`/`toolbutton` moved to the new `BootBase`); dead
`focus`/`input` dropped. Expected suite ~263 (excl. the known `nl.msg`
localization env flake). **Workstream H (docs) DESIGN PASS is now COMPLETE** — the
hard-rule design/scoping gate is done; full design in
`development/2_0_docs_design.md` (bootstack-modeled 4-destination Diátaxis IA;
native-vs-shipped widget dichotomy carried by catalog grouping; generated Style
Reference; both staged sources fold in; flagship = the bootstyle grammar). The
design pass surfaced two follow-on **code** items (not docs): a **PREREQ** to drop
the character-based icons (now **merged**, #1094 — `ttkbootstrap.icons`
`Emoji`/`Icon` constants removed, brand logo preserved as `window.py`
`_DEFAULT_ICON_DATA`, Messagebox's 4 icons rendered from the font-glyph engine),
and a **deferred** shipped-widget API-normalization pass (`Window`/dialogs/
`Tableview`; docs-first is accepted). **A batch of visual-polish PRs then merged
into `2.0`** (design/rationale in `development/2_0_breaking_changes.md`): the
`neutral` color + flat hairline-border button-family restyle (#1096), button-family
follow-ups (#1097), `neutral` as the bare-button default with `default_button=`
opt-out (#1098), a `ghost` button variant + `thin` scrollbar + full scrollbar
restyle + datepicker/font-dialog fixes (#1099), and the input-indicator refinements
(#1100 — menubutton/combobox/spinbox arrow glyphs, padding, constant-color arrows,
striped-progressbar flat trough). Expected suite on `2.0` ~283 (excl. the known
`nl.msg` localization env flake). **The deferred shipped-widget API-normalization
pass (`Window`/dialogs/`Tableview`) was then STARTED ahead of the docs** (the
author reversed docs-first so the docs get written against normalized signatures):
design pass done + confirmed in `development/2_0_shipped_widget_api_design.md`
(Hybrid posture · port bootstack window mechanisms · unify dialog returns +
`get_date`→None-on-cancel · Tableview fix+re-export now, defer the verb rename).
**PR A (dialogs) is MERGED (#1102):**
Messagebox uniform keyword-only signatures, Querybox `get_*` return via `.result`,
`get_date`→None-on-cancel + `position=`, `DatePickerDialog` `autoshow`/`show()`/
`result`, `MessageDialog.command` plain-callable (tuple deprecated via `_compat`),
`ColorChoice` deduped, dialogs re-exported at top level; `tests/test_dialogs_api.py`
(+19); expected suite on `2.0` ~302 (297 excl. localization). **PR B (Window/
Toplevel) is MERGED into `2.0` (#1103)** (design §5a; a cross-platform visual gate
is still worth an eyeball but did not block merge): private `_BaseWindow` mixin
shared by `Window`/`Toplevel`, unified `_setup_icon` (fixes the
`Toplevel(iconphoto=None)` crash), new private `internal/positioning.py` (subset of
bootstack's `WindowPositioning`; optional `screeninfo`, graceful single-screen
fallback) re-pointing `place_window_center`, snake_case kwarg aliases via
`_compat.normalize_window_kwargs` (`hdpi`/`overrideredirect`/`windowtype`/
`toolwindow`, warn-and-normalize), keyword-only constructors, `iconify` promoted,
edge-relative/combined geometry, aqua `overrideredirect` no-op guard, win32
AppUserModelID; `tests/test_window_api.py` (+15), suite 317 excl. the `nl.msg`
flake. **PR C (Tableview fixes + re-export, §5c) — the pass's last PR — is
**MERGED (#1104)**:** re-export `Tableview`/`TableColumn`/`TableRow` at top level
(`ttk.Tableview`) + from `ttkbootstrap.widgets`, fix two dead-on-call bugs
(`delete_column(cid=...)` called the `cidmap` dict — `cidmap` is int-keyed, not
`str`; header right-click menu `self.master` self-assignment), `insert_row([])`
raises `ValueError` instead of `print()`ing to stdout, delete dead code
(`reset_row_sort` stub / unused `_build_table_*` / commented `_select_pagesize` /
`maxwidth` docstring); `tests/test_tableview_api.py` (+6), suite 323 excl. the
`nl.msg` flake. **With A/B/C the shipped-widget API pass is COMPLETE.** **A large
batch has since merged into `2.0`:** icon-delivery fixes (#1105 theme-aware
`apply_icon`, #1106 pagination glyph buttons, #1107 widget self-deprecation
hotfix) + top-level widget re-exports (#1108); the **widget-review normalization
pass** on a shared `ConfigureDelegationMixin` (`internal/configure_delegation.py`,
#1109) — Meter (#1110), DateEntry (#1111), Floodgauge (#1112), Scrolled (#1113),
LabeledScale+ToolTip (#1114), Toast (#1115) — each keyword-only, cget/configure
parity, `_compat` warn-and-normalize renames, lifecycle/leak fixes; a
**property/accessor consistency pass** (#1116 — options live on configure/cget
only, deprecated bare-attr `__getattr__`/`__setattr__` shims); a **Tableview polish
run** — verb rename (#1117), sizegrip recolor asset (#1118), header restyle
(#1119), themed right-click menus (#1120) with plain-text labels (#1121), a
theme-walk `cget('style')` fix (#1122), `builders_tk` string-literal cleanup
(#1123), a locale-robust test fix (#1124); **macOS native popup chrome** for
borderless `window_type` popups via `MacWindowStyle` (#1125); and the
**ScrolledText container-owned card border + scrollbar polish** (#1126 — new
`card`/`highlight` frame style variants, `Text` border left to the container
[`update_text_style` no longer imposes it], auto-hide flicker/window-growth fixes,
trough removed + darker light-mode thumb, dead `scrollbar_thumb` asset deleted);
and an **input focus-ring + card/highlight border cleanup** (#1127 — the
`Entry`/`Combobox`/`Spinbox` focus color now shows on `focus` only, not `hover`;
the `card`/`highlight` frames draw a single `bordercolor` hairline via
`relief=RAISED` with the bevel neutralized [`lightcolor`/`darkcolor` = background],
matching the inputs' 1px border weight, `highlight` state-maps light/dark to the
accent on focus). The
deferred **Tableview method-verb rename** is now also done (#1117). **A fluent-
geometry batch then merged:** #1130 added `FluentGeometryMixin` (a shared mixin so
`pack`/`grid`/`place` — and the `*_configure` spellings — return the widget for
one-expression construct-and-place; mixed into both `BootMixin`/`AutoStyleMixin`,
re-exported; `enable_global_api()` also patches tkinter's `Pack`/`Grid`/`Place`
mixins so stock/native/third-party widgets get it on opt-in), plus a 39-site
sweep collapsing first-party construct-then-place pairs. #1131 fixed a **2.0
regression** where `ColorChooser` crashed in the default config — its swatch/
preview widgets were native `tk.Frame`/`tk.Label` passed `autostyle=False`, which
stock tkinter rejects now that the import-time monkey-patch is gone (PR 3); they
now use the blessed `ttk.TkFrame` and a **new blessed `ttk.TkLabel`**
(`AutoStyleMixin` subclass, re-exported), and a keyword-only `ToolTip(...)` caller
was fixed. A follow-on audit for the same two latent-regression classes — native
tk/ttk widgets taking `bootstyle=`/`autostyle=`, and positional args to now-
keyword-only APIs — found **no other crash-class bugs** in `src/`; the only extra
finding was the `__main__` demo tripping its own deprecation warnings, fixed in
#1132 (`meter_size`/`amount_used`/`auto_hide`). Expected suite on `2.0` ~492
(excl. the known `nl.msg` localization flake). **The compat & utilities initiative
(the last substantive code work before release,
`development/2_0_compat_and_utilities_design.md`) is now COMPLETE: Slice 1 (legacy
theme-name auto-register, #1139), Slice 2 (`App`/`Window` + `theme`/`themename`
aliases, #1140), Slice 0 (`ttkbootstrap.utils` package + `utility`/`colorutils`
shims, #1141), Slice 5 (deferred-config pending-apply seam + `set_default_button`,
#1143), Slice 3 (localization: msgcat `tk.call` fixes + `L()`/`LocaleVar`/
`set_locale` + `<<LocaleChanged>>`, #1144), and Slice 4 (typography: `ttk.Fonts` +
`ttk.set_global_family` over the standard Tk named fonts, #1145) are all MERGED into
`2.0` (born into `utils/`); suite ~552 excl. the two known flakes. **With all
slices in, the last substantive code work before release was done.**

**The cumulative pre-release review is now COMPLETE** (per
`development/2_0_prerelease_review_plan.md`; results appended there). **#1146**
(`53f5b72b`) landed **Track A** (8-subsystem agentic `2.0…master` sweep — found +
fixed the `bootstyle="neutral"` crash on non-button families), **Track C**
(migration-contract diff — no silent breaks), and the **RC gates** (green suite —
root-caused the `TSpinbox.uparrow` bug via an idempotent `Style.element_create`;
`nl.msg` confirmed an env-only transient; clean-env install smoke; 3.10 parse;
warning-free import), plus visual-pass fixes (datepicker stale-highlight, dialog
icon scoping, Querybox/Messagebox) and **two author-sanctioned utilities**
(utilities, not widgets): **`theme_mode`** light/dark toggle and **`icon_only=True`**.
The **pyproject version is bumped to 2.0.0.** **Track B** (human visual/
cross-platform) was then largely run **on macOS**; its aqua fixes merged as
**#1147** (`745fb997`): toast off-screen/stack/icon, `get_date` centering,
DatePicker no-flash + aqua-gated tooltip popover, `place_window_center` using the
real mapped size. A high-effort `/code-review` gated both PRs. Suite ~567 excl. the
two known flakes (`nl.msg` env + the order-dependent `test_color_helpers`).

**NEXT — docs Workstream H, a from-scratch rebuild on a new toolchain**
(`development/2_0_docs_design.md`; toolchain LOCKED at the top of §1, 2026-07-10).
The docs move **off mkdocs onto bootstack's stack** (sibling repo at
`D:/Development/bootstack`): **Sphinx + `pydata_sphinx_theme` + `autodoc`/`napoleon`
+ `sphinx_design`**, authored in **rST**. Lift bootstack's `conf.py` + `_static/`
CSS + `screenshots/`/`scripts/` tooling + page templates wholesale; borrow the
*infra & IA*, author ttkbootstrap content, keep the styling-extension positioning.
ttkbootstrap's `Parameters:`/`Examples:` docstrings feed `autodoc` as-is (napoleon
Google) — no docstring rewrite. **Clean cut:** delete the whole mkdocs `docs/` tree
(incl. `ja`/`zh`); the 9 broken `:::` API stubs resolve by *replacement*. Keep the
introspection Style-Reference + BootStyle generators as **offline `tools/` steps
emitting committed rST** (RTD has no display). **First task next session: a Sphinx
skeleton spike** — lift bootstack's `conf.py` + one widget page, prove the
structure. Remaining Track B odds/ends (Linux/x11, the DPI matrix) are optional.
The user keeps live WIP in the working tree (`dialogs/colorchooser.py`,
`dialogs/fontdialog.py`, `examples/widgets/dialogs.py` — dialog-button styling) —
**leave it untouched.**

**Docs H sub-PR 1 — the Sphinx skeleton spike — is MERGED into `2.0` (#1148, merge
`e88bd525`).** Clean cut done (mkdocs `docs/`
tree + `mkdocs.yml` deleted, `.readthedocs.yaml`→sphinx); bootstack `conf.py` +
`_static/custom.css` + autosummary template lifted/adapted; the 4-destination IA
toctree stands up with browsable stubs; **spike proof pages** = `widgets/button.rst`
(native) + `widgets/meter.rst` (shipped) + `reference/api/widgets.rst` (autodoc
`Meter`). Builds clean (**22 pages, zero warnings**). **Three findings baked in:**
`autoclass_content = "both"` (ttkbootstrap docs ctor params in `__init__`, not the
class); `inherited-members: False`; and — correcting the design's "docstrings feed
autodoc as-is" claim — ttkbootstrap docstrings use **Markdown ```` ```python ````
fences** that rST can't parse, resolved via a build-time `autodoc-process-docstring`
shim in `conf.py` (no docstring rewrite; keep-shim-vs-sweep is a later-slice
decision). Sphinx deps live in `.venv-home` (`pip install`ed this session). **NEXT:**
iterate skeleton content/IA (author has changes in mind), then §11 sub-PR 2 =
reference generators. See `development/2_0_handoff.md` top entry for the full spike
detail.

**Docs H — progress since the spike (through 2026-07-11, all MERGED into `2.0`).**
#1159 reference generators (per-family Style Reference + rST BootStyle table via
`tools/`) + unified Widgets catalog + the `bootstyle` spaces/`@surface` grammar
sweep; #1162 theme-API consolidation (`theme_mode`/`toggle_theme`); #1163
theme-aware custom styles (`on_theme_change`/`@theme_aware`); #1164 Concepts band;
#1165 removed the in-library user-theme store (ttkcreator now exports a
`Theme(...).register()` snippet); #1166 Foundations band + tkinter **event
reference** + images how-to; **#1167 (merge `4f73aaa4`) the FUNDAMENTALS band +
the Concepts-band DISSOLUTION**; **#1168 (merge `c3daa3f2`) the three
feature-guide stubs authored (Typography/Localization/Validation) + a
`Validation` namespace API rename** (flat `add_*_validation` →
`Validation.text`/`numeric`/`range`/… + `Validation.add`, re-exported
`ttk.Validation`; old `add_*` kept as warn-and-forward deprecated aliases removed
in 3.0; `ColorChooser` migrated; logged in `2_0_breaking_changes.md`). With that,
the three natural utility families are all namespaced (`Fonts`/`MessageCatalog`/
`Validation`) — the surface survey found no further namespacing worth doing. **#1169 (merge
`624272d8`) the Dialogs feature guide + two essentials How-Tos (clipboard,
error-handling) + file dialogs surfaced through `Querybox`** (new
`Querybox.get_open_filename`/`get_open_filenames`/`get_save_filename`/
`get_directory` wrappers over `tkinter.filedialog`, cancel normalized to `None`;
`ttk.filedialog` re-exported; additive) **+ a teach-by-building robustness pass**
over the feature guides authored this cycle (Typography/Localization/Validation/
Dialogs reworked from option-tours into build-a-real-flow guides). **#1170 (merge
`294ef12f`) feature-guide retitles into the noun-phrase register** ("Make your own
style/theme" → **Custom styles**/**Custom themes**; **"Working with color" folded
into the Theming guide → "Theming & Colors"**; "Windows & high-DPI" left as a stub
to reframe when finished). **#1171 (merge `45730422`) the Windows guide finished,
deepened, and retitled → "Windows"** (teach-the-geometry/state-model not an
option-tour; a consolidated cross-platform behavior table + inline notes; a bonus
fix for nested-inline-markup leaking literal double backticks, caught by a
state-machine scanner over `docs/` since `-W` doesn't flag it). **#1172 (merge
`1c2b5a4e`) the flagship Build-your-first-app tutorial**
(`getting-started/build-your-first-app.rst`, wired after Quickstart): a complete
contact-book app built step by step (shell → `grid` form → `StringVar` binding →
`Validation.regex` → searchable `Tableview` → button `command=` callback), each
step handing off to its Foundations/feature-guide home; every code block verified
headlessly. Established three **standing docs-code rules** (memory-saved): **no
`\` backslash line-continuations** (assign to a variable and reuse), **use
`theme=` not `themename=`** on the `App` constructor, and **use curated 2.0 theme
names** (`bootstrap-dark`, not legacy `darkly`); the same `theme=`/curated-name
sweep was applied to Quickstart + the landing hero. Governing rule
now:
[[feedback_docs_teach_tkinter_ttkbootstrap_dialect]] — **the docs teach tkinter
itself, in the ttkbootstrap dialect** (a self-sufficient learning source; teach,
don't defer). **Bands sort by DEPTH:** Getting Started · **Fundamentals** ·
Feature guides · How-To — **there is NO "Concepts" band** (dissolved: styling
essentials → Fundamentals; deep styling/theming → Feature guides). **Variables &
events are FEATURES** (Foundations gives the on-ramp; robust `Variables`/`Events`
feature guides own the depth). Author was firm: **teach layout/mechanics
BY BUILDING, never option-tours.** The full IA (charters, §14 curriculum map,
tkinter-surface coverage audit + supersession map, screenshot-placeholder
convention) lives in `development/2_0_docs_design.md`. **NEXT (content authoring,
fresh branch off `2.0`):** the **Build-your-first-app** tutorial
(Getting Started; the flagship teach-by-building on-ramp); **Widgets-catalog**
depth (usage-first per design §5a; the button prototype is thin); remaining How-Tos
(*Menus*, *Scrollable*, *Threads*; *Validate a form* is now partly covered by the
Validation guide). (DONE this cycle: the Typography/Localization/Validation stubs authored
[#1168], the Dialogs guide + clipboard/error-handling How-Tos + the feature-guide
robustness pass [#1169].) Screenshots are a later slice (placeholders are in
place). See
`development/2_0_handoff.md` top entry for the full current state.

## Repository layout

```
src/ttkbootstrap/
  __init__.py        # public exports; defines the concrete BootMixin/AutoStyleMixin widget
                     #   subclasses (e.g. `class Button(BootMixin, ttk.Button)`) that carry the
                     #   `bootstyle`/`autostyle` api + fluent pack/grid/place (return self). No
                     #   import-time monkey-patch (2.0, PR 3) — opt into it via enable_global_api().
                     #   Blessed tk widgets: Tk/Menu/Text/Canvas/TkFrame/TkLabel/LabelFrame.
  style/             # THE CORE — theme/style engine package (see below). Split from the old
                     #   style.py in 2.0 (PR 4); public import path `ttkbootstrap.style` unchanged.
                     #   theme.py (Colors, ThemeDefinition), builders_tk.py (StyleBuilderTK),
                     #   builders_ttk.py (StyleBuilderTTK — the bulk), engine.py (Style),
                     #   bootstyle.py (Keywords, Bootstyle, tokenizer, FluentGeometryMixin +
                     #     BootMixin/AutoStyleMixin, delivery),
                     #   _compat.py (2.0 Workstream D/F quarantine: normalize_bootstyle, strictness).
  window.py          # Window / Toplevel classes
  constants.py       # constants (PRIMARY, SUCCESS, ...) + the single bootstyle vocab source of
                     #   truth: BOOTSTYLE_* tuples, BootColor/BootType/BootBase, generated BootStyle
  colorutils.py      # color math (Colors helpers, make_transparent, contrast)
  themes/standard.py # STANDARD_THEMES dict: pre-2.0 (Bootswatch) color defs, kept only for
                     #   the legacy theme-name migration path (removed in 3.0)
  themes/builtin.py  # CURATED_THEMES: the curated 2.0 semantic-anchor Theme families
                     #   (custom themes live in user code via Theme(...).register(), not here)
  widgets/           # CANONICAL custom widgets: dateentry, meter, floodgauge, tableview,
                     #   scrolled, tooltip, toast, labeledscale
  dialogs/           # Messagebox, Querybox, colorchooser, datepicker, fontdialog, etc.
  localization/      # msgcat-based i18n (msgs.py holds translations)
  internal/          # PRIVATE plumbing (no underscore in the name): publisher.py, utility.py.
                     #   No back-compat guarantee. See "internal/ vs public" below.
  utility.py         # PUBLIC utility funcs: enable_high_dpi_awareness, scale_size
  publisher.py       # deprecation shim -> internal/publisher.py (warns; removed in 3.0)
tests/               # HEADLESS pytest only (4 test_*.py + conftest.py). CI-runnable.
examples/            # interactive mainloop() demos (moved out of tests/ in #1068)
docs/, gallery/, cookbook/   # documentation and examples
```

### internal/ vs public (important — new in 2.0)

Implementation-detail modules live in **`src/ttkbootstrap/internal/`** (the
name is `internal`, *not* `_internal`). Anything under it has no
back-compat guarantee.

When moving something public→internal, leave a thin shim at the old public path
that re-exports from `internal/` and emits a `DeprecationWarning` ("…moved to
ttkbootstrap.internal.X; removed in 3.0") — e.g. `ttkbootstrap.publisher`. For a
module that stays public but sheds internal helpers (e.g. `utility.py`), forward
the moved names via module-level `__getattr__` with the same warning instead of
a whole shim module. **Importing `ttkbootstrap` itself must stay warning-free**
— shims warn only when an old path is actually used.

The older top-level shims (`ttkbootstrap.scrolled/tableview/toast/tooltip`,
`dialogs/dialogs.py`) were **removed** in #1068 — import from
`ttkbootstrap.widgets.<name>` / `ttkbootstrap.dialogs`. Edit real
implementations in `src/ttkbootstrap/widgets/`, never a shim.

## The style engine (`style/` package)

Everything visual flows through here. Split from the old monolithic `style.py`
in 2.0 (PR 4) into a `style/` package; `ttkbootstrap.style` re-exports the full
surface, so the import path is unchanged. The submodules layer downward
(`theme` → `builders_tk` → `builders_ttk` → `engine` → `bootstyle`), with a few
function-local back-edge imports. Key classes (by module):

- **`Style`** (`engine.py`) — singleton (`Style.get_instance()`), subclasses
  `ttk.Style`. Owns theme definitions and the active theme. `theme_use()`
  switches themes and runs the version-stamped theme walk (PR 1) that repaints
  only stale mounted widgets — styles rebuild lazily/O(mounted), not all up front.
- **`StyleBuilderTTK`** (`builders_ttk.py`) — holds `create_*_style(colorname)`
  methods (e.g. `create_button_style`, `create_outline_toolbutton_style`). These
  build a ttk style and call `_register_ttkstyle()`.
- **`StyleBuilderTK`** (`builders_tk.py`) — styles legacy `tk.*` widgets (Menu,
  Text, Canvas, …).
- **`Colors` / `ThemeDefinition`** (`theme.py`) — the color model + theme
  container.
- **`Bootstyle`** (`bootstyle.py`) — the resolver: `update_ttk_widget_style()` maps a
  `bootstyle=`/`style=` string to a built ttk style. Two delivery paths feed it
  (2.0, PR 3): the default `BootMixin`/`AutoStyleMixin` concrete subclasses
  (in `__init__.py`), and the opt-in global monkey-patch
  (`enable_global_api()` → `setup_ttkbootstrap_api()`). As of Workstream D the
  parser is a real **tokenizer over a closed vocabulary** (fixed slot order
  `[color-][modifier-]<base-type>[-orient]`), not a substring regex: unknown
  tokens fail loudly (warn by default; `set_bootstyle_strict(True)` /
  `TTKBOOTSTRAP_STRICT=1` raises). It handles **two input dialects** —
  dash/space bootstyle strings (loud) vs already-built dotted ttk style names
  from the theme walk / `Style.configure` / custom styles (lenient). The vocab
  lives once in `constants.py`; the reference (`BootStyle` `Literal` + docs
  table) is generated by `tools/generate_bootstyle_reference.py`, sync-tested.
  Legacy forms (tuple/list bootstyle) are quarantined in `style/_compat.py`
  (warn-and-normalize through 2.x, removed in 3.0).

### Lazy style building — the model to keep in mind

Styles are built **on demand**, not up front. The base `TButton`, `TEntry`,
etc. are only configured the first time a widget that needs them is created
(or via `_create_ttk_styles_on_theme_change` for already-registered styles).
At theme load, `create_default_style()` configures the root `.` style plus a
small set of always-needed styles.

Consequence (and a real past bug, #1062): native/third-party ttk widgets the
app never instantiates directly — e.g. the `ttk::button` widgets inside Tk's
file dialog on Linux — fall back to the bare clam look if no corresponding
ttkbootstrap widget has been created. The fix pattern is to build the needed
base style eagerly in `create_default_style()`.

## Gotchas

- **`Style` is a process-wide singleton (`Style.instance`) tied to the first Tk
  root.** Creating and destroying separate roots in one process leaves the
  singleton mis-bound, so later theming silently no-ops. Tests share ONE root
  via the `root` fixture in `tests/conftest.py` — see "Writing tests" below.
  (Properly fixing the singleton is part of the deferred `style.py` engine
  rewrite.)
- **Themes are clam-derived** (`theme_create(name, TTK_CLAM)`). An unstyled
  base ttk style shows clam's default appearance until ttkbootstrap configures it.

## Dev environment & commands

A virtualenv with an editable install lives at `.venv/` (Python 3.x on macOS;
`python` on PATH resolves to it). The package is also importable with
`PYTHONPATH=src`.

- Run the headless suite: `python -m pytest -q` (config in `pyproject.toml`
  under `[tool.pytest.ini_options]`; `testpaths = ["tests"]`).
- pytest is installed in `.venv`. If a fresh env lacks it: `pip install pytest`.
- The interactive demos in `examples/` call `mainloop()` and need a display —
  they are NOT collected by pytest.
- Build docs: `mkdocs serve` (deps in `requirements.txt`).

### Writing tests

`tests/` is headless-only. New GUI tests should **take the `root` fixture** from
`tests/conftest.py` (one shared session root; widgets and theme are reset per
test) instead of creating their own `ttk.Window` — creating your own root
re-triggers the singleton mis-binding above. Query a built style's value with
`app.tk.call("ttk::style", "lookup", "<Style>", "-<option>")`. Put any
interactive/visual demo in `examples/`, not `tests/`.

## Conventions

- Match the style of the file you're editing (comment density, naming).
- **Public-name casing (2.0 standardization):** ttkbootstrap-authored identifiers
  (functions, methods, new kwargs) use `snake_case` (`apply_icon`, `icon_size`,
  `high_dpi`, `window_type`); names that pass through to a real Tk/ttk option or
  method keep Tk's spelling verbatim (`iconphoto`, `minsize`/`maxsize`, `compound`,
  `themename`); `bootstyle`/`autostyle` are grandfathered brand tokens, not a
  template for new names. Test: "am I forwarding a real Tk name?" — yes → Tk
  spelling; no → snake_case.
- Custom widgets that need image assets generate them through the style
  builder / Pillow pipeline; favor native ttk/clam mechanisms over images
  where both are viable (perf and cross-platform consistency).
- Commit messages: imperative subject; reference the issue (`fixes #NNNN`)
  where applicable.
- Branch + PR per change. **2.0 cleanup work targets the `2.0` branch**;
  maintenance/bugfixes target `master`.
