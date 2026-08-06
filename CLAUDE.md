# CLAUDE.md

Guidance for working in the ttkbootstrap repository.

## What this is

ttkbootstrap is a theming extension for tkinter/ttk: it generates modern,
flat, Bootstrap-inspired themes on demand and adds a `bootstyle` keyword
API to ttk widgets. Pure Python; the only runtime dependency is Pillow
(used for image-based widget assets). Public API entry point is
`src/ttkbootstrap/__init__.py`, typically imported as `import ttkbootstrap as ttk`.

- Package version / metadata: `pyproject.toml` (src layout, `requires-python >=3.10`).
- Docs site: Sphinx + `pydata_sphinx_theme` (`docs/`, config in `docs/conf.py`),
  published to Read the Docs. (Was mkdocs pre-2.0; rebuilt onto Sphinx in Workstream H.)

## Direction: 2.0 cleanup (read before large changes)

> **STATUS (2026-07-19): ttkbootstrap 2.0.0 is RELEASED.** Tagged `v2.0.0`,
> published to PyPI (https://pypi.org/project/ttkbootstrap/2.0.0/), GitHub release
> live. **`master` has been promoted to 2.0** — the old 1.x `master` is preserved
> on the **`release/v1`** branch and as the **`version-1`** Read the Docs version
> (docs at `/en/version-1/`; `latest` now serves the 2.0 Sphinx docs). **New work
> targets `master`** (the 2.0 mainline); the `2.0` branch is retired (identical to
> `master`). 1.x maintenance, if any, targets `release/v1`. RTD redirect map for
> the old mkdocs URLs: `development/2_0_rtd_redirects.md`. Everything below is the
> record of how 2.0 was built — background, not an active worklist.

The initiative was a **2.0 cleanup/consolidation release — no new
features.** Goals: remove cruft, standardize/normalize the API (aggressive/
breaking is OK when meaningful, paired with a migration path), fix memory leaks
and theme-switch perf, make user-defined custom styles easy, and overhaul the
docs. ttkbootstrap stays a **styling extension for vanilla tkinter** — not a
widget library (the forward-looking framework is a separate project, bootstack).

The full worklist (locked decisions + workstreams) lives in
**`development/2_0_plan.md`**. (During development the integration branch was
**`2.0`**; it has since been promoted to `master` — see the status banner above,
so new work targets `master`.) Headlines: mixin-hybrid API (replace the import-time
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
sweep was applied to Quickstart + the landing hero. **#1173 (merge `4fe63b50`)**
folded **Custom themes** into the Theming & Colors guide (one theming home;
`custom-themes.rst` deleted). **#1174 (merge `fd9841d6`)** authored the last How-To
recipes (*Scroll long content*, *Run background work*), **promoted Menus to a
feature guide** (`feature-guides/menus.rst`), and **added a new public API — the
native macOS application menu** on `ttk.Menu` (moved into
`src/ttkbootstrap/menu.py`): `add_application_menu`/`add_window_menu`/
`add_help_menu` + `on_preferences`/`on_quit`, all no-op off macOS, closing the
Tcl-reach-in gap the guide exposed (design `2_0_menu_api_design.md`, Design 1;
`tests/test_menu_api.py`; suite `2.0` **648 passed**). Also made How-To titles
**task-shaped + short so they don't wrap**, dropped internal **"blessed"** jargon +
implementation call-outs from the docs, and used the existing public
`ttk.windowing_system` over raw `tk.call` — **two more standing docs rules
(memory-saved):** no jargon/impl-detail asides (incl. no "under the hood" notes
that re-expose what an API hides), and task-shaped short How-To titles. **#1175
(merge `2173f0f0`)** started the **Widgets catalog**: locked the authoring plan
(`2_0_docs_design.md §5a-plan` — ~27 pages, Text/Canvas robust & in, Scrolled
thin-stub, coverage sync-test no-gaps mechanism, one PR per family) and rewrote
`docs/widgets/button.rst` as the **usage-first gold-standard template** (one
concept per digestible section). **Phase 1 (one PR per family) is in progress** —
**Inputs #1176 / Choice #1177 / Command #1178 MERGED**. #1176 also carried a
**style fix**: colored Combobox/Spinbox forced their base border to the accent, so
all inputs now show the accent **on focus only** (1.x→2.0 visual change, in
`2_0_breaking_changes.md`). Remaining families: Containers · Range & misc ·
Shipped · **Text** · **Canvas**, then the coverage sync test. Governing
rule now:
[[feedback_docs_teach_tkinter_ttkbootstrap_dialect]] — **the docs teach tkinter
itself, in the ttkbootstrap dialect** (a self-sufficient learning source; teach,
don't defer). **Bands sort by DEPTH:** Getting Started · **Fundamentals** ·
Feature guides · How-To — **there is NO "Concepts" band** (dissolved: styling
essentials → Fundamentals; deep styling/theming → Feature guides). **Variables &
events are FEATURES** (Foundations gives the on-ramp; robust `Variables`/`Events`
feature guides own the depth). Author was firm: **teach layout/mechanics
BY BUILDING, never option-tours.** **More standing rules (2026-07-15 batch):**
**one job per How-To** (that split "Beep and show busy" in two); **no band index
pages** (only How-To had one — the sidebar + the user-guide cards already do it);
**don't `/`-join items in a table cell** — one per line via an rST line block
(prose slashes are fine: *"returns "OK" / "Cancel""* reads well in a sentence);
**state what a thing IS, not what it isn't** — don't write defensively at a bug you
just found (the macOS busy limit is "not supported on macOS", full stop; the
rationale for why it can't be emulated belongs in git, not the page — CLAUDE.md's
comment convention applies to docs too). The full IA (charters, §14 curriculum map,
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

**Widgets-catalog progress (since):** catalog pages **Treeview** (#1184, PR open),
**Text** (#1185, PR open), and the **Tableview** expansion (#1183, merged) landed;
`ttk.Listbox` was newly **blessed** (#1186, PR open) so it can be documented. **A
new, large sub-workstream then started: a self-authored WIDGET API REFERENCE** —
because python.org documents the classic tk widgets (Text/Canvas/Listbox/Menu) not
at all. Full handoff (goals, LOCKED scope, two-layer structure, format rules,
grounding discipline, build cmd, done/remaining, PR-stack state, deferred ideas) is
in **`development/2_0_docs_api_reference.md` — read it first to continue this
work.** Headlines: a **Capabilities** section (`docs/reference/capabilities/`, one
spec page per Tcl/Tk-manual area — configuration/pack/grid/place/stacking/focus/
grab/after/lifecycle/clipboard/selection, with events+winfo folded in; `busy` and
`interpreter` were added later by the #1232 audit, and pack/grid/place/stacking
have since moved to the top-level Geometry section) plus
**per-widget API pages** (`docs/reference/api/<w>.rst`, options tables +
`py:method` specs). **Done:** the Capabilities section + the tk pages
Text/Canvas/Listbox/Menu. **Remaining:** the trivial tk containers (Tk/TkFrame/
TkLabel/LabelFrame) and the ~19 native ttk pages. Work is on branch
`docs/2.0-api-reference-text-stacked`, **stacked on #1185** (retarget its PR to
`2.0` once #1185 merges). Build gate: `.venv-home/Scripts/python.exe -m sphinx -b
html -W -q docs <out>` must exit 0.

**Docs H — the widget API reference + whole Reference layer are COMPLETE and
merged** (#1184–#1187, #1189–#1192; catalog + capabilities + all autodoc sections;
full handoff in `development/2_0_docs_api_reference.md`). **Session through
2026-07-14 (all MERGED into `2.0`):** #1215 the **Migrating to 2.0** guide +
backfilled the early engine/delivery breaks into `2_0_breaking_changes.md` (the log
had started mid-initiative) + styled the screenshot placeholders; #1216 a
**cross-platform Installation** guide (per-OS tkinter/venv, `screeninfo` is a plain
`pip install`, not an extra); #1217 a **new public `App`/`Toplevel.on_close`
handler** (`_BaseWindow` method + `on_close=` kwarg; runs the zero-arg callback then
auto-destroys, `return False` to veto, `WM_DELETE_WINDOW`-only so macOS ⌘Q stays
with `Menu.on_quit`) + the getting-started finishes (**Structuring an app**
authored; Quickstart theme section moved onto the `App` theming delegates
`theme_use`/`theme_mode`/`toggle_theme`; build-first-app link/aside fixes); #1218
deepened **the widget model** (a **Lifecycle** section — create≠display, destroy
cascade, `<Destroy>` cleanup — + the `state=`-option-vs-flags / `cget("state")`
-not-authoritative clarification) and **refocused the variables pages on
reactivity** (retitled "State & variables"→**"Variables & reactivity"**; added a
**Named variables** section with the GC-lifetime + `getvar`/`setvar` type-bypass
footguns); #1219 **typography** — a "Setting a font on a widget" section teaching
every `font=` form (tuple, points-vs-pixels, `-option` string, named font, `Font`
object); #1220 **corrected the Text Appearance section** (colors/`padx`/`pady` are
theme-managed → `autostyle=False` to own them; the old example silently lost
`padx=8`) and **surfaced direct color-setting on Label** (promoted out of a buried
note; raw hex + `style.colors` palette/ramp + `contrast_color` helper; a direct
color is a fixed snapshot that survives but doesn't adapt). Standing color/appearance
fact (probed): on a themed **tk.Text** a direct color is overridden unless
`autostyle=False`; on a **ttk.Label** an instance `foreground`/`background`
overrides the style and survives theme switches (no `autostyle` — ttk widgets reject
it). **Session through 2026-07-15 — the HOW-TO BAND is COMPLETE (#1225) + a `busy()`
shim (#1226), both MERGED into `2.0`.** The band was audited with the #1222 grounded
method (one read-only agent per page; every claim probed and every snippet run
headlessly against the real library, cross-checked against the Tcl/Tk 8.6 manuals) —
**all 7 authored pages had a real defect**, several macOS-shaped: `tk busy` is a
**no-op on macOS/Aqua** *and* tkinter's busy methods are **3.13+** (the page had
claimed the opposite of both); `<Control-c>` isn't the macOS copy key (`<<Copy>>` →
`<Mod1-Key-c>`) and `bind_all` on it clobbers the user's selection; the `TclError`
example used a bad `bootstyle`, which warns-and-falls-back rather than raising;
`multiple-windows` taught raw `protocol("WM_DELETE_WINDOW")` over the public
`on_close` and its "reuse a window" broke after ✕; `ScrolledFrame` never sizes to
content and has no hbar; the threads "one rule" gave the wrong mechanism (tkinter
*marshals* cross-thread calls → clean `RuntimeError`); `compound="none"` was
backwards. Authored the 3 real recipes (**animate-gif**, **splash-screen**,
**application-icon**), converted the Foundations-overlapping index entries to
cross-references, and — on author review — **split "Beep and show busy" into two
how-tos** (`bell` + `busy`; one job per recipe). **#1226** adds
`internal/busy.py` `BusyMixin` (delegates to tkinter's methods where they exist,
issues the identical `tk.call` where they don't; all 16 aliases; mixed into
`BootMixin`/`AutoStyleMixin`/`_BaseWindow`), verified byte-identical on a real
3.10.11 interpreter vs 3.14; `tests/test_busy_api.py` (+25) forces the <3.13 branch
by deleting the methods off `tkinter.Misc`. **The macOS no-op is deliberately not
shimmed** (Tk's busy window is a *transparent* input shield; Tk has no transparent
color, so any emulation is opaque and hides the UI) — docs state it as a plain
platform fact plus the disable+cursor fallback. **Standing lesson (memory-saved):**
`event_generate` **bypasses pointer hit-testing** and can never prove input is
blocked — probe with `winfo_containing` + a positive control. **An author-review
batch then merged (#1227–#1233)**, all driven by the author reading the shipped
docs; in nearly every case the plausible answer was wrong and only a probe settled
it: #1227 **dropped `how-to/index`** (the only band index; it duplicated the sidebar
and invented 3 buckets) + **unslashed 32 list-table cells** onto rST line blocks;
#1228 **nested the variant Styling-options sections** on Button/Checkbutton (two
generated partials × the same 5 headings had rendered every heading twice at h3 —
structural, not duplicated content; nested partials now render at `^`, guarded by
two tests derived from the `.. include::` order); #1229 made the menu `*_off_mac`
tests **force the windowing-system probe** rather than trust the host (**suite is
now 689/0 on macOS** — forcing beats `skipif`, which would leave a Mac dev running
neither branch); #1230 fixed **`command` fires on invoke, not on selection change**
(probed: `var.set()` selects without firing; re-invoking the already-selected button
fires without a change — wrong in *both* directions; Space invokes too, so the docs
say "invoked"); #1231/#1232 reworked **the widget model** — explicit
configure/cget/`[]` patterns (a widget is NOT a dict; `config` is an older alias),
a new **What comes back** section (`cget("width")`→int even from `"8"`;
`command`/`textvariable` → **Tk's name, not your object**), and **Walking the tree**
(`master` is the object, `winfo_parent()` a *string*, `nametowidget()` converts,
`children` is a **dict attribute**, `winfo_children()` does **not** recurse);
#1232 also closed a **reference audit of `tkinter.Misc`: 41 → 8 undocumented** —
new `capabilities/busy.rst` (a hole we made in #1226: 16 aliases shipped, 3
documented, no reference page) and `capabilities/interpreter.rst` (the homeless
methods shared a theme — they all cross the Python↔Tcl boundary), plus `after_info`,
`unbind_all`/`unbind_class`, `selection_handle`, `quit`, `image_types`, and
`event_add`/`event_delete`/`event_info` (bind.rst had *promised* the Events
reference specced them; it didn't). The **option database** got a brief mention +
Tk-manual link (not ours to teach, but the tk widgets make it reachable) — probing
corrected the draft: it can't reach ttk widgets at all, and on tk widgets **our own
theming overrides it** (only `autostyle=False` lets it through). Remaining 8 are
deliberate (`getvar`/`setvar` → Variables guide; `propagate`/`slaves` aliases; 4
legacy). #1233 added the Foundations page **What tkinter wraps** — the docs leaned
on the Tcl seam everywhere (`TclError` across 8 pages, a dash the reader never
wrote, `bad window path name`, "named Tcl variable") and explained it nowhere; its
scope is the **seam, not Tcl**, spined on `app.tk.call(str(w), "cget", "-text")`
== `w.cget("text")`, placed **after** the-widget-model. **Two corrections to earlier
CLAUDE.md claims:** the menu `*_off_mac` failures are **fixed** (not "worth
gating"), and suite is **689**. **PROCESS NOTE:** a `checkout -b … || checkout …`
fallback once left commits on a second branch while `git push origin <name>` pushed
a different ref — #1231 merged without the work reported in it (recovered as
#1232). **Verify `git branch --show-current` before pushing.**
**Session 2026-07-16 (all MERGED into `2.0`) — an author-review + issue-sweep
batch.** **#1235** docs polish + three probe-driven style fixes: tutorial uses
top-level `ttk.Tableview`/`ttk.Validation`; widget-model Tk/Tcl glosses (+
*What tkinter wraps* pointers); arranging-widgets gains a **Spacing** section
(three layers: `padx`/`pady` vs `padding` vs `ipadx`/`ipady` + the
container-owns-margins idiom) and a **Geometry managers** section;
**`LabelFrame` is now the ttk alias for `Labelframe`** (matching tkinter.ttk —
the 1.x classic-tk export was never sanctioned; deliberately NOT in the
migration guide, author call, see the dev-log entry); **bare `outline` renders
neutral** across the button family (closing the last primary fallback from
#1098/#1099; toggles keep primary — the accent carries on-state); **`@surface`
fixed on Checkbutton/Radiobutton** (builders resolved the surface for text but
never set `background=`; tests now assert background — the `@surface` silent
drop on toolbutton/menubutton/entry is a KNOWN, logged gap). **#1237** the
**2.1 value-tokens design brief** (`development/
2_1_bootstyle_value_tokens_design.md`, PROPOSED, design-session-gated) + a
**Post-2.0 (2.1) backlog** section in `2_0_plan.md`; tracked as **issue #1236
on the new 2.1 milestone** (repo's first milestone). **Open-issue sweep** (all
8 verified by probe, not by reading): #1155 closed (Dialog.close() shipped +
documented); **#1239** merged — **eager native-dialog base styles**
(entry/combobox/menubutton/scrollbars join #1062's TButton in
`create_default_style`; fixes the dark-mode white-on-white file dialog, #1224
closed) + **DateEntry `start_date` docs per author ruling** ("a configuration
option, by its name — no configure-time display refresh"; it fills the field
at construction and is the `get_date()` empty-field fallback; live handle is
`value`/`set_date()`; #1151 closed); #1161/#1160/#1238 **paired on the 2.1
milestone** under one future design — a **durable style-options layer** the
builders read from (the author then closed #1160/#1161). **#1240** merged —
**ToolTip popup `topmost=True` by default** (native parity; `topmost=False`
opts out via the now-documented Toplevel-kwargs passthrough; probed: aqua's
`help` window class already floats, so the default lands on Windows/X11;
#1086 closed). Suite on `2.0` was **692** excl. the two known flakes; every
docs change verified headlessly + built green.
**Session 2026-07-16b (all MERGED into `2.0`) — the widget API-reference
introspection audit + an author-review batch.** **#1244** ran the #1232 Misc-audit
method over **every** reference page (31 widget pages + `tk.rst` +
`reference/windows/` + `reference/dialogs/`): enumerate each live class's public
surface minus the Capabilities-owned baseline, diff both directions against the
page's specs/prose/options tables, probe every flag before acting. Real gaps
closed (canvas `find_above`/`find_below` + text-item `select_*`; menu
`add`/`xposition`/`type`; entry-family `scan_*` + `cursor` rows; the
inconsistent `cursor`/`takefocus` cluster; DateEntry `state`; wm_-alias sentence
+ `configure(menu=)` note on windows pages; QueryDialog `validate`/`apply`;
toast documented only the deprecated `hide_toast` alias, not `hide()`; tooltip
`destroy()`; `report_callback_exception`). Verified-deliberate exclusions
(probed): classic-tk **trap methods inherited by ttk widgets** (Panedwindow
`sash*`/`proxy*`/`pane(config|cget)`, `Scrollbar.activate` — all TclError on the
ttk widget), deprecated Tableview aliases, Floodgauge's Canvas base (author:
impl detail), Text `debug`/`window_config`/`yview_pickplace`, entry-family
`background` compat option. **Author ruling (memory-saved): "works ≠ designed
surface"** — composite widgets' container-Frame option passthrough
(borderwidth/relief/padding on DateEntry/Meter/LabeledScale/Tableview) is NOT
API and must not be documented; designed delegates (DateEntry `state`/`width`)
are. The audit found two library bugs, fixed separately: **#1245**
`Tableview.configure` never returned query results (+ no `pagesize` cget
parity; `style`/`class` kept on the wrapper so the #1122 theme-walk read is
unchanged; explicit `__getitem__`/`__setitem__` because tkinter binds
`__getitem__ = cget` at *function* level, bypassing subclass overrides), and
**#1247** `bootify` **crashed** (`TclError: Layout not found`) for any widget
with its own ttk class — even bare construction — because the unknown-family
resolve returned the raw bootstyle fragment as a style name; now
warn-and-keep-current-style (silent for the implicit `default`), with the
effectiveness contract documented (full vocabulary for standard ttk classes;
explicit base type `"info-frame"` borrows a recipe; probed: composite internals
follow the theme on their own — only the accent isn't fanned out;
`apply_bootstyle` on the child is the designed path). **#1246** fixed the
author's nine docs-review findings: `create_alias("Caption")` shadowed
`TkCaptionFont` → `HeadingSm`; `grid_propagate` taught nowhere on the grid
foundations page (pack/frame/reference already covered it); pack/grid/place
got real Options list-tables; `El`/`StyleName`/`Theme` attributes documented
(napoleon Attributes + `#:` dataclass doc-comments; `__slots__` descriptors
excluded from `:members:` to avoid duplicate-object warnings); `icon_element`'s
grammar list de-blockquoted (nested inline markup is illegal in rST); and four
leftover **mkdocs `!!!` admonitions in docstrings** (scaling.py high-DPI,
colordropper, tableview ×2) that rendered as plain text → napoleon `Warning:`
sections. **#1248** unslashed the new geometry tables' paired option cells onto
rST line blocks (the #1227 convention applies at authoring time, not just in
sweeps; memory-saved). Suite on `2.0` is **701** excl. the two known flakes;
every claim probed live and every docs change built green.
**Session 2026-07-16c→17 — the SCREENSHOT SLICE started: harness + the full
widgets catalog (PRs #1251 + #1254, OPEN at handoff — merge #1251 first, then
retarget #1254 from the harness branch to `2.0`).** Also merged: **#1250**
deleted the stale pre-2.0 `docs_scripts/` + `cookbook/` trees (mkdocs-era,
unreferenced; `examples/` and `gallery/` stay), and 30 merged local branches
were pruned (`feat/2.0-pr6-toolkit-migration` left — unmerged/superseded, user
call pending). **#1251** ports bootstack's `docs/scripts/take_screenshots.py`:
scene files `docs/screenshots/<page>.py` (a `SCENES` dict of self-contained
callables that MIRROR the page's own code blocks), captured per theme into
`docs/_static/examples/<page>-<scene>-{light,dark}.png` via a patched `ttk.App`
(forced theme; position→focus→grab→destroy); proof = button.rst. **Sizing
contract:** PNGs keep the capture box's full pixel density (2× on Retina) and
every rST image directive pins `:width: <logical>px` (the harness prints the
value per shot) — never downscale (blurry on HiDPI) and never leave unpinned
(2× renders double-size). **macOS authoring path** (Windows stays the canonical
capture box): capture by CGWindowID (`screencapture -l`; needs
`pyobjc-framework-Quartz`, installed in `.venv`) — a plain region grab sees only
the active Space, so a full-screen IDE yields wallpaper/IDE shots. **#1254**
authors every remaining catalog scene — **`docs/widgets/` has ZERO placeholders**
(26 pages, 31 shots × light/dark, each eyeballed against its spec; one commit
per family). Harness capabilities grown along the way: **composite capture**
(`app._capture_extra` = popup widgets *or raw Tcl paths* — the combobox popdown
exists only Tcl-side; mac composites via `CGWindowListCreateImageFromArray`
over the union rect, popups ordered in front, theme-bg fill; win32 = union
region grab); **parent capture** for native aqua menus, which BLOCK the Tcl
loop while posted (`app.capture_via_parent()` announces the content rect, the
scene posts, the harness parent composites the child pid's windows — a posted
menu sits on window-server layer ≥ 100 — and kills the blocked child; the
in-child grab is suppressed in this mode because its timer CAN fire during
menu tracking and destroyed the app mid-shot); **NSAppearance pinned** to the
captured theme after Tk init (native titlebars/menus follow the SYSTEM
appearance — a dark-mode host tinted the light shots; pinning before Tk creates
its NSApplication crashes, and a MISMATCHED pin aborts menu tracking, so menu
scenes revert to the system appearance before posting — the two light menu-open
shots carry a system-dark menu, author-accepted as provisional). Scene/authoring
rules from author review: **size the window tall enough that a popup drops
within it**; closed+open pairs render **side by side** via the new
`tb-screenshot-row` flex container (stacked pairs don't align); dateentry shows
the **open** shot only; a text highlight tag needs **both** bg and fg —
`ttk.contrast_color(colors.warning, model="hex")`, NOT
`colors.get_foreground()` (theme-dependent; returned white-on-yellow in light).
All PNGs are provisional macOS renders; the Windows canonical run re-captures
byte-for-byte under the same names and the pinned `:width:` values stay valid.
**Both catalog PRs (#1251 harness + #1254 catalog) are now MERGED into `2.0`.**
**NEXT docs-H thread — TRANSFERRED TO THE WINDOWS BOX, tracked as issue #1255:**
the remaining **30 placeholders across 18 pages outside the catalog** (foundations
7 · getting-started 4 · feature guides 14 · how-tos 5 — full per-page inventory +
capture specs in #1255), then the **Windows canonical capture run** of the whole
catalog (re-capture byte-for-byte under the same names; also re-takes the two
menu-open light shots properly). Same pipeline as #1251/#1254 (scene file in
`docs/screenshots/<page>.py` → `python docs/scripts/take_screenshots.py <page>` →
replace the placeholder admonition with the light/dark `.. image::` pair, pinning
`:width:` to the harness-printed logical px). Suggested PR split: foundations +
getting-started · feature guides · how-tos. Find the placeholders with
`grep -rl screenshot-placeholder docs --include='*.rst'`; each admonition body IS
the capture spec. Then landing/hero shots per design §6–§7; plus optional Track B
odds/ends (Linux/x11, DPI matrix). Every docs change verified headlessly + built
green (`.venv/bin/python -m sphinx -b html -W -q -E docs <out>`, exit 0).

**Session 2026-07-17 — the placeholder slice + the Windows canonical recapture
are DONE and MERGED into `2.0`.** The remaining non-catalog placeholders landed as
**PR (a)** foundations + getting-started (**#1256**) and **PR (c)** how-tos
(**#1261**); **PR (b) #1262** carried the feature-guide shots + a new top-level
**Themes catalog** page (`docs/themes.rst` + `docs/scripts/theme_gallery.py`,
15 families as side-by-side light/dark cards, in the nav before Release Notes) +
the **Windows canonical recapture of the whole widget catalog**. The recapture
also: **regrouped the catalog by purpose** (bootstack pattern — seven octicon
cards + captioned toctrees, replacing the flat list); gave the container/popup
shots the **window treatment** (frame/labelframe/panedwindow/notebook/sizegrip as
full windows; dateentry/menubutton/optionmenu/tooltip/combobox as full windows
with a posted popup + `tb-window-screenshot`); fixed the tooltip + combobox popups
(weren't showing on Windows) via the win32 parent-capture; and **dropped the closed
dropdown shots** (combobox/menubutton/optionmenu now show only the open window,
like dateentry). Two **standing screenshot facts (memory-saved):** the Windows box
runs at **100% scaling = 1× density** (macOS Retina was 2×) — sharp on standard
displays, soft on HiDPI viewers, accepted; and bordered screenshots need
**`box-sizing: content-box`** (the theme's global border-box otherwise subtracts
the 1px border from the pinned `:width:` and distorts the aspect — the same bug
lies **dormant in bootstack**, tracked for a future issue). **PR #1262 also carried
three library regression fixes (with tests):** `fix(optionmenu)` — the dropdown was
a raw `tkinter.Menu` showing the native light menu in a dark theme (a PR-3
monkey-patch-removal regression), now themed at construction; `fix(text)` — a
standalone `Text` gets its flat themed 1px border back (2.0 left tk's sunken
relief), with `ScrolledText` marking its inner text `_tb_borderless` so the
container border isn't doubled; `fix(combobox)` — the border no longer paints the
focus-ring while pressed (accent on focus only). Suite **708 passed** excl. the
`nl.msg` env flake. **NEXT (optional):** the deferred **macOS application-menu
shot** (`menus.rst`, inherently a Mac capture), **landing/hero shots** for the docs
index (design §6–§7), and Track B odds/ends (Linux/x11, the DPI matrix).

**Session 2026-07-18 — landing-hero direction + two visual tweaks (UNCOMMITTED
in the working tree on `2.0`; nothing pushed).** Work paused mid-session for the
author to rework the demo. **(1) Landing hero — DECISION + DEFERRED to the
author.** The hero should be a **curated widget SAMPLER, not an example app**:
ttkbootstrap is a styling layer, so visitors scan for "what will my widgets look
like + what's the palette," not "what can I build" (that's bootstack's framing).
Density is fine; what to avoid is a *fake-app dashboard* aesthetic (bootstack's
KPI/chart/txn hero) that over-claims a framework. Plan: the **author is reworking
the `__main__` demo** into that sampler and will hand it off; then **copy it into a
self-contained scene** `docs/screenshots/home-hero.py` (own `ttk.App`, ends in
`mainloop()`, `app._capture_full_window = True`, `app._capture_max_width` ~940 —
adapt, don't import the demo), capture light/dark on THIS Windows box, and wire the
`.. image::` pair into `docs/index.rst` **right after the `.. container:: hero-ctas`
block** (CSS infra already present: `tb-screenshot-light/dark` + `tb-window-
screenshot`). Also add the **"glimpse" shot** after that section's code block (reuse
the `quickstart` `hello` scene) and **delete the stale "in development" `.. note::`**.
A throwaway sampler scene was built and discarded this session (the author preferred
tuning the proven demo). **(2) Bare solid `toolbutton` now renders NEUTRAL (was
primary)** — `style/builders/toolbutton.py`: the `DEFAULT`/`""` branch merged into
the `neutral` path (ON/selected = `neutral_fill(builder, 2)` `#e0e0e0`, was
`colors.primary`), so a bare `toolbutton` is now byte-identical to `neutral
toolbutton`; the last button-family bare default still latching to the accent.
Outline toolbutton (already neutral) and the round/square **toggle switch** (keeps
primary — its accent carries the on-state) are unchanged. Test
`test_bare_solid_toolbutton_is_neutral` in `tests/widget_styles/test_neutral.py`;
logged in `2_0_breaking_changes.md`. **(3) Tableview row height 27→21px** —
`style/builders/treeview.py` `Table.Treeview`: `row_height = linespace + ascent //
2` (was `linespace + ascent`, ~2× the text line and visibly bloated; original 1.x
was bare `linespace` = flush/cramped). The plain **`Treeview`** builder (`linespace`)
is UNCHANGED, so only Tableview shots move. The `// 2` literal tripped
`tests/test_scaling.py`'s geometry-scaling AST guard → added a narrow, documented
`_reads_font_metric` exemption (font metrics are already DPI-physical; a ratio of a
metric is not a logical pixel literal — same spirit as the existing
`_is_hairline_border` exception). **Re-captured the 4 Tableview screenshots at 21px**
(`tableview-hero-{light,dark}`, `build-your-first-app-hero-{light,dark}` — the only
two scenes rendering a Tableview; the `hero` scene only in build-your-first-app);
pinned `:width:` unchanged (620/558) so **no rST edits**. Suite **709 passed** (1
known `nl.msg` env flake); docs build clean under `-W`. **`src/ttkbootstrap/
__main__.py` is modified in the tree — that is the AUTHOR'S demo WIP, leave it
untouched** (as with the author's other live WIP: dialog-button styling in
`dialogs/colorchooser.py`, `dialogs/fontdialog.py`, `examples/widgets/dialogs.py`).

**Session 2026-07-18b→19 — ghost variant across the button family + LabeledScale
`value=` + demo rework + landing hero + Object lifetime docs (all MERGED into
`2.0`; supersedes the 2026-07-18 UNCOMMITTED state above — now shipped).**
**#1265 (`feat/2.0-ghost-and-widget-polish`, merge `c896b18d`)** completed the
**`ghost`** look across the button family (plain Button already had it): a new
**ghost toolbutton** (`style/builders/toolbutton.py`, `("ghost","toolbutton")`) —
transparent at rest, and when toggled **ON reuses the ghost *button's* hover
surface** (`neutral_fill(1)` neutral / a `0.16` accent tint colored), no
hover/press preview (a toolbutton is a toggle), quieter than `outline toolbutton`;
and a new **ghost menubutton** (`style/builders/menubutton.py`,
`("ghost","menubutton")`) — momentary like a button (wash on hover/press), caret
via `_build_menubutton_arrow`, **inherited free by `OptionMenu`** (winfo_class
`TMenubutton`). Because menubutton **infers** its base, ghost menubutton reuses the
existing `ghost`/`<color> ghost` strings (NO new `BootStyle` entries — only a
reference-table row); ghost *toolbutton* DID add 10 entries (`<color> ghost
toolbutton` + bare + `neutral ghost toolbutton`), regenerated via
`tools/generate_bootstyle_reference.py`. Registry keys added to
`test_builder_registry` EXPECTED_KEYS; catalog docs surface the three toolbutton
fills (checkbutton/radiobutton), the three menubutton variants, and outline+ghost
on optionmenu; logged in `2_0_breaking_changes.md`. The PR also folded in the held
**bare-solid-neutral toolbutton** + **Tableview row-height 27→21** + **demo
rework** (the 2026-07-18 WIP) and a **LabeledScale `value=`** fix
(`widgets/labeledscale.py`): the advertised param was ignored (ctor always set
`from_`); now forwarded, default `None`→`from_` (a **sentinel**, so a non-zero
`from_` and the passed-`variable` contract survive — `test_explicit_variable_
respected`), **clamped into `[from_,to]`** because LabeledScale's `_adjust` reverts
out-of-range values and `_last_valid` must stay in range (a bare `ttk.Scale` stores
raw). Suite **718 passed** excl. the `nl.msg` flake. **#1266 (`docs/2.0-landing-
hero`, merge `5d10c788`)** added the **landing hero**: `docs/screenshots/home-
hero.py` — a self-contained widget **sampler** (own `App`, **module-level so the
harness writes clean `home-hero-{light,dark}.png`** — a SCENES dict would name them
`<page>-<scene>-…`; reads the live theme name; `_capture_full_window`,
`_capture_max_width=960`), captured **874×529** light/dark on THIS Windows box;
wired into `docs/index.rst` after `.. container:: hero-ctas`, deleted the stale "in
development" `.. note::`, added the `quickstart hello` **glimpse** shot after the
code block. It shows the palette + the button family (default/primary/outline/
ghost) + inputs + toolbuttons (all ON) + meter/progress + a **Tableview** + a
**Notebook** — the choice controls (check/radio/toggle) live on the notebook's
**VISIBLE first tab** because **only the active tab renders in a static screenshot**
(anything on a hidden tab is invisible). The scene is **frozen/self-contained
(adapt the demo, don't import it)** so the demo evolves independently. **#1267
(`docs/2.0-object-lifetime`, merge `1624fafb`)** added a Foundations page
**`object-lifetime.rst`** consolidating tkinter's GC footguns (previously scattered
across ~9 files) onto the *Python owns / Tcl references by name* model from
`what-tkinter-wraps`: a collected `StringVar`/`PhotoImage`/named `Font` takes its
Tcl entity with it → the widget empties/blanks/reverts, while **widgets survive
because the tree owns them**; teach-by-example fixes (instance attr / return it /
`label.image=`) + the inverse (callbacks/`after` keeping objects alive; the
pending-`after`-into-a-destroyed-widget case → `after_cancel` in `destroy()`).
Wired into the foundations toctree + card after What-tkinter-wraps; repointed that
page's variable-footgun link + seealso at it. Every claim probed live (var→empty,
image→blank, `ttk.Font`→reverts, orphan widget survives) and every snippet verified
headlessly; docs build clean under `-W`. **A follow-on theme backwards-compat fix**
(`style/engine.py` `_resolve_theme_alias` + a guard in `theme_use`): an
unregistered theme name is routed through an alias resolver so the five pre-2.0
names that carried over as curated families (`minty`/`pulse`/`sandstone`/`united`/
`vapor`) resolve to their **curated** variant at the *legacy theme's own*
light/dark mode (`minty`→`minty-light`, `vapor`→`vapor-dark`) — no error, no
deprecation warning, and **never the app's current mode** (a 1.x caller sees the
light/dark they expect). An explicit `install_legacy_themes()` still wins (only
names not already registered are aliased). Legacy-only names (`darkly`/`flatly`/…)
keep the legacy-dict migration path + warning. Added `LEGACY_THEME_ALIASES` in
`themes/standard.py` so the historical `cerculean` typo (1.x shipped Bootswatch's
*cerulean* misspelled; the typo stays canonical for 1.x code) also accepts the
correct `cerulean` spelling. **Author ruling: bare curated-*only* family names
(`nord`/`bootstrap`/…) intentionally stay an error** — not a backwards-compat case.
Logged in `2_0_breaking_changes.md` (extended the Slice-1 legacy-names entry) + the
migrating/theming guides; `tests/widget_styles/test_theme_anchor.py` +2. Suite
**719 passed** excl. the `nl.msg` flake; docs build clean under `-W`. **NEXT
(optional, unchanged):** the deferred **macOS application-menu shot** (`menus.rst`),
landing/hero polish, Track B odds/ends (Linux/x11, DPI matrix).

**Session 2026-07-19 — RELEASE: ttkbootstrap 2.0.0 shipped.** The last mile, all
merged into `2.0` then promoted to `master`. **Docs/README/packaging prep**
(PRs #1265–#1274): completed the ghost variants + LabeledScale/theme fixes (above);
a **from-scratch README rewrite** for 2.0 (hero + `bootstyle`-first framing, icons
clarified — 2.0 ships Bootstrap Icons built-in, `ttkbootstrap-icons` is the
optional extension for *other* sets, verified still 2.0-compatible); removed stale
files (`README_ja/zh`, `ROADMAP.md`, `beginningresult.png`) + fixed `MANIFEST.in`;
a **Release-notes nav link** to GitHub Releases + JetBrains **Support** on the docs
About page; an **Object lifetime** Foundations page; and **RTD/packaging**:
`sphinx-notfound-page` + `docs/404.rst` (absolute body links), `.readthedocs.yaml`
`fail_on_warning: true` + `ubuntu-24.04`, and the copy-paste **redirect map**
`development/2_0_rtd_redirects.md` (mkdocs dir-URLs → Sphinx `.html`, `latest`
-scoped to protect the `version-1` build; includes the retired ja/zh trees).
**The release cutover:** snapshot 1.x to **`release/v1`** (the 65 master-only
commits were all JP/ZH translations of deleted mkdocs docs — nothing to
forward-port); **promote `2.0` → `master`** via reset + force-push (Option A);
RTD `latest` now serves the 2.0 Sphinx docs, `version-1` preserves 1.x at
`/en/version-1/`; **redirects added in the RTD dashboard** (user) + spot-checked.
**Publish:** git tag **`v2.0.0`** (annotated, on `a2920620`) + a **GitHub release**
(title `v2.0.0`, matching the `vX.Y.Z` convention); `python -m build` →
`twine check` PASSED → **uploaded to PyPI**
(https://pypi.org/project/ttkbootstrap/2.0.0/); verified by a clean-env
`pip install ttkbootstrap==2.0.0` (30 themes, icon engine, theme switch all work).
No CI publish workflow exists (at the time, `.github/workflows/` was empty; #1317
later added a test/docs workflow, still nothing that publishes) — PyPI upload is
manual, creds in a gitignored repo-root `.pypirc`. **Announcement** (r/tkinter —
python.org no longer allows announcements — + LinkedIn) drafted; advised to post a
**weekday** (Tue–Wed AM) not the release Sunday, after a short soft-bake. **2.0 is
DONE.** Optional post-release polish only from here.

## Direction: 2.1 milestone (post-release)

> **STATUS (2026-08-02): ttkbootstrap 2.1.1 is RELEASED** — a typing/docs-only
> patch, cut from `master` per the runbook. Tagged `v2.1.1` (annotated, on
> `4fb79e59`), [GitHub release](https://github.com/israel-dryer/ttkbootstrap/releases/tag/v2.1.1)
> live, on PyPI (https://pypi.org/project/ttkbootstrap/2.1.1/), verified by a
> clean-environment install. `master` reads **2.1.1** and, per the standing
> convention, **`master` is always the most recent release**. 2.1.0 shipped
> 2026-07-30 and its milestone closed with 48 items; everything below is the
> record of how 2.1 was built — background, not an active worklist.
>
> **Two open milestones, both with one issue.** **`2.1.x`** (the post-2.1
> maintenance bucket) still holds **#1322** — four asset-geometry tests fail on a
> non-baseline-density display, test-only, contributor-facing; it did **not** ship
> in 2.1.1, so the milestone is still open. **`3.0`** holds **#1276** (make
> `DateEntry` `value=None` the default). (The **`2.2` milestone (#4) has since
> been created** — see the 2.2 section below.)
>
> **`2.1.x` GOES UNREACHABLE THE MOMENT 2.2 SHIPS, so #1322 has to move.** It is
> a consequence of the release convention, not a bookkeeping preference: `master`
> is always the most recent release and a patch is cut *from* `master`, while
> `release/*` exists only for **superseded majors** — the 2.0.1 attempt at a
> `release/2.0` branch is recorded above as a mistake not to repeat. So once
> `master` reads 2.2.0 there is no branch a 2.1.2 could be cut from, and anything
> still sitting on `2.1.x` can never ship. Fix #1322 before the 2.2 release and it
> moves to **`2.2`**; otherwise move it to a **`2.2.x`** bucket and close out
> `2.1.x` as part of the release. Nothing about #1322 gates the release either
> way — it is test-only and contributor-facing.
>
> **CLOSED OUT:** discussion **#1326** (the 2.1.1 bug report) has been told the
> fix shipped — no longer an open follow-up (author, 2026-08-05).
>
> **The next user-visible change starts a new log.** `development/2_1_changes.md`
> and `development/2_1_1_changes.md` are both frozen history now. Create
> `development/2_2_changes.md` (or `2_1_2_` for another patch) when the first such
> change lands, with scope **relative to 2.1.1**, and log there as you land — not
> at release time. 2.1.1 was the first patch to get its own log; 2.0.1's two Tk 9
> fixes were recorded only in this file.
>
> New work targets `master`. **Labels carry no version** — the author dropped the
> `Version 1/2/3` labels because the milestone already conveys the target release;
> tag issues/PRs topically (`enhancement`/`bug`) and **set the milestone on every
> issue AND PR** (PRs were the gap: most 2.1 PRs went unmilestoned, so
> `gh pr list --search "milestone:2.1"` under-reported the release until it was
> backfilled).
>
> **2.0.1 SHIPPED (2026-07-23)** — a patch release carrying two Tcl/Tk 9 fixes and
> nothing else: the scroll-event contract (#1290, PR #1291 — trackpads fire
> `<TouchpadScroll>` and were completely dead; wheel deltas normalized to ±120 so
> one notch jumped to the end; X11 no longer delivers Button-4/5) and the aqua
> scaling baseline (PR #1292 — Tk 9 moved aqua from 72 to 96 dpi, so every asset
> and padding rendered 33% larger than designed while the text stayed put).
> It was cut from the `v2.0.0` tag on a `release/2.0` branch (deleted after
> publishing). **AUTHOR CORRECTION (2026-07-28): making that branch was a
> mistake — do not repeat it.** The convention is that **`master` is always the
> most recent release**; `release/*` is only for *superseded* majors
> (`release/v0.5`, `release/v1`). A patch release is cut from `master`, so the
> version bump lands there naturally. The consequence of getting it wrong is
> exactly what happened here: the bump commit (`8fbf3aa`) lived only on the
> deleted branch and its tag, so **`master` kept claiming 2.0.0 while 2.0.1 was
> the released version** — caught 2026-07-28 and corrected on
> `chore/2.1-version-catchup`. (Both *fixes* were on `master` already, via the
> original #1291/#1292 merges; only the bump was stranded.) Note the version
> literal in `pyproject.toml` is load-bearing beyond packaging: `docs/conf.py`
> reads it through `importlib.metadata`, so a stale value mislabels the docs too. Tag `v2.0.1` + GitHub
> release live; on PyPI at https://pypi.org/project/ttkbootstrap/2.0.1/.
> **Tk 9 is now testable on the Mac** — Homebrew `/opt/homebrew/bin/python3.14` is
> Tk 9.0.4 while the default `python`/`.venv` is 8.6.17; run the suite against it
> with a `--system-site-packages` venv + `PYTHONPATH=src`. **CI does not cover
> Tk 9** (`.github/workflows/ci.yml` runs Linux, Windows and macOS on the stock
> Tk 8.6 that ships with CPython — it reports the build per job, so this is
> stated by the run rather than assumed), so a Tk 9 run stays a manual step —
> worth doing for anything touching scaling, assets, geometry, or event bindings.
>
> **The durable style-options cluster is COMPLETE** — #1253, #1238, #1161, #1160
> all closed (PRs #1277–#1283). Suite **770 passed**. **Remaining 2.1 work (5
> open issues) and the LOCKED sequence (2026-07-24):**
>
> **Phase 1 — durable-options review cluster: COMPLETE (2026-07-24, all merged).**
> **#1284** register-before-configure invariant bug (PR #1294 — new
> `Style._derived_styles` excludes icon styles from the durable-options fan-out;
> `_build_icon_style` reorders to configure-first/register-last); **#1286** test
> backfill (PR #1295 — notebook per-state equivalence, color-reverts-on-theme-
> switch, `_effective_style_option` inherited values, icon reconfigures on theme
> switch); **#1285** inert-option warning — **DECISION: docs-only, no runtime
> warning** (PR #1296, design `2_1_durable_style_warn_design.md`). Key finding:
> empirical detection (`lookup != recorded`) catches ONLY the map-masking case
> (a library defect), NOT the font/sashthickness cases users hit — those succeed
> at the style level. Author rationale: we wrap ttk→Tk, so "will this option take
> effect" is lower-layer behavior we can't reliably track; a warning
> sometimes-wrong about it is worse than none (memory:
> feedback_wrap_a_wrapper_prefer_docs_over_runtime_detection). No API/docs change
> (the #1283 `custom-styles.rst` caveat already covers it); shipped one source-guard
> test (`test_no_recipe_masks_configured_padding_across_the_built_surface` — a
> runtime `lookup` guard, NOT an AST audit, since builder `map` values are
> variables). Each PR got a `/review` (all three caught a real self-defect: #1294 a
> redundant guard, #1296 a test-pollution bug). Suite ~793. **Housekeeping earlier
> this session:** closed #1224 (subsumed by #1242) and #1252 (superseded by #1253/
> #1276); #1285 milestoned onto 2.1.
> **Phase 2 — #1236 (bootstyle value tokens): COMPLETE (2026-07-24, all merged;
> issue closed).** Design session settled §10 of
> `development/2_1_bootstyle_value_tokens_design.md` (now CONFIRMED/shipped): extend
> `Colors.get`; **docs-only registry-growth mitigation, NO runtime warning** per the
> #1285 ruling; hex accents take the generic contrast path; accept 3-digit hex.
> Shipped in four PRs: **#1300** engine — raw hex `#rrggbb`/`#rgb` + ramp-addressed
> `role[stop]` in the color and `@surface` slots; loud-fail validation; ramp-reactive
> vs hex-frozen contract (a ramp re-resolves on theme switch, a hex is a frozen
> snapshot whose derived states still recompute); value-token vocab/validators in
> `constants.py`, tokenizer in `bootstyle.py` (both dialects), `Colors.get`
> resolution, `resolve_surface`/`on_surface_fg`; `examples/value_token_preview.py`.
> **#1301** docs — grammar-page "Value tokens" section + light/dark screenshot (new
> `value_tokens` scene) + generated-reference prose. **#1302** review follow-up —
> ramp-token canonicalization (`primary[050]`→`primary[50]`, was minting duplicate
> styles) + route the loud path through the exported `looks_like_value_token`. An
> independent adversarial `/review` of the merged engine found **no correctness
> bugs**; its two minor findings landed in #1302. Suite **837**, docs build clean.
> **Two spin-offs from this work:** **#1299** — a pytest `--capture=sys` fix in
> `pyproject.toml`; the long-standing flaky `nl.msg` Tcl file read was pytest's
> **fd-level capture** swapping OS fds 0/1/2 out from under the Tk interpreter on
> Windows (NOT an OS/AV transient, NOT a Style-singleton order flake) — **the
> `nl.msg` flake is now GONE** (see [[pre-existing-test-flakes]]). And **#1298
> filed** — a pre-existing durable-options gap found while testing: a durable
> `style.configure` override is not re-applied when `theme_use` switches to an
> **already-visited** theme (the theme walk only rebuilds *mounted* styles; the
> first visit's eager `create_default_style` masks it). Low severity, self-heals on
> first visit.
> **#1298 (durable theme-switch re-apply) is DONE (PR #1304, MERGED).**
> Root cause was exactly as filed: `theme_use`'s existing-theme branch
> (`super().theme_use` + walk) rebuilds only *mounted* styles, so a durable
> override on an unmounted style kept the recipe default in an already-built
> theme's style DB (the first-visit `create_default_style` masked it → order
> -dependent). Fix: new `_reapply_user_options_for_theme(themename)` in
> `style/engine.py`, called in the existing-theme branch right after
> `super().theme_use` — replays `_user_options` across the target theme's
> registered styles (ancestor merge most-specific-wins + un-namespaced globals
> like `"Sash"`; excludes derived icon styles; writes via `_build_configure` so
> replays aren't re-captured). Mirrors `_reapply_user_options` but theme-scoped.
> Regression test `test_override_reaches_previsited_theme` pre-visits the target
> theme before setting the override (reads 5 without the fix, 3 with). Suite
> **838 passed**; an adversarial `/review` of the diff found no defects (ordering
> vs. the later walk is idempotent; the loop is guarded + fires only on repeat
> visits). No `2_1_changes.md` entry — the durable "survives a theme switch"
> guarantee is a new-in-2.1 feature that never shipped, so this pre-release gap is
> a dev-log/PR item, not a user-facing changelog line.
>
> **Phase 3 — #1242** (in-house themed file dialog). Deliberately last: biggest
> single build, most standalone (doesn't touch the seam), lowest urgency (dialog
> works, just unthemed on X11), and the named DROP CANDIDATE if 2.1 must close
> sooner — parks cleanly to 2.2 without stranding seam work. **Design gate DONE**
> (2026-07-26, `development/2_1_file_dialog_design.md` CONFIRMED): reproduce
> `tkfbox.tcl`'s layout with themed widgets (`ttk.Treeview` details view swaps the
> unstyleable `IconList` Canvas); per-platform default + `native: bool|None`
> override (X11 → themed, Win/macOS → native, `native=False` forces themed);
> minimal chrome (no sidebar — that's 2.2+); overwrite-confirm via `Messagebox`.
> **PR 1 (dialog + backend + opt-in seam) MERGED (#1305):**
> `dialogs/filedialog.py` (themed `FileDialog`, all four modes, pure-Python
> listing/filter/nav backend) + `native=` selector on the four `Querybox.get_*`
> wrappers (native the default; themed only when `native=False` is forced).
> Findings baked in from a live demo (`examples/themed_file_dialog.py`): the
> selection background is a neutral **gray** and `secondary` *equals* that gray in
> a light theme (contrast 1.0), so a static icon color vanishes on select → **row
> icons swap color with selection state** (`selectfg` when selected)
> [[reference_selectbg_is_neutral_gray]]; default flush treeview rows are too short
> → a dialog-scoped `Filedialog.Treeview` bumps `rowheight`; and Tk's file dialogs
> return **forward-slash** paths on every platform → results go through
> `Path.as_posix()` for drop-in parity. `tests/test_filedialog_api.py` (+43).
> A post-hoc `/review` of the merged PR 1 + PR 2 found two real defects (both
> fixed): a macOS 3-tuple `filetypes` crash in `_normalize_filetypes` (index, not
> unpack), and the dialog setting `rowheight` via the *public* `Style.configure`,
> which the durable-options layer captured as a phantom user override (switched to
> `_build_configure`). **PR 2 (X11-default routing + review fixes) MERGED (#1306):**
> `_use_native_filedialog` makes `native=None` **platform-aware** — native OS
> chooser on Windows/macOS, themed dialog on X11 (via
> `windowing_system(parent-or-default-root)`; native fallback when no interpreter
> is reachable). Two **X11 defects** the author found running it on Linux were
> committed just *after* #1306 merged (they missed that merge), so they landed as
> a **separate fix PR (#1307)**: a hardcoded `640x480` clipped the bottom
> checkbutton where platform fonts run taller (now sizes from `winfo_reqheight`,
> `minsize`-pinned); and `_locate` computed centered coords but never *applied*
> them, so an X11 transient opened at the virtual-desktop origin (between
> monitors) — now applies them explicitly. `tests/test_filedialog_api.py` totals
> **51**. (Process note: a commit pushed to a PR branch *after* the PR is merged
> does not land — verify the merge SHA includes your latest push.) **PR 3 (docs)
> MERGED (#1308):** rewrote the Dialogs-guide *File dialogs* section (native-vs
> -themed + `native=`) + `Querybox` reference `native=` params + a themed
> `dialogs-file` screenshot scene (light/dark, Windows-canonical capture — the
> dialog body is platform-identical; a real-Linux recapture is an optional Track-B
> follow-up). An adversarial `/review` of the #1307 fix found one MEDIUM defect,
> fixed in **PR #1311 (OPEN at pause):** `_locate` clamped an explicit `position=`
> through `ensure_on_screen` but applied the *centered* coords raw, so a parent
> near a screen edge (or shorter than the ~480px dialog) could push the centered
> dialog partly off-screen — now both paths are clamped. The review confirmed the
> rest of #1307 sound and rated a ≤40px off-true-center (withdrawn-reqsize)
> item cosmetic/won't-fix. **#1242 is COMPLETE and in `master`** (the design's
> three PRs + two review-driven fixes); only #1311 awaits merge.
> **Two cross-platform items filed as SEPARATE 2.1 issues** (NOT part of #1242,
> found during this work): **#1309** — themed popup menu border missing on X11
> (a `StyleBuilderTK` menu styling gap); **#1310** — base `Dialog._locate`
> (`dialogs/base.py`) has the same *unapplied-`center_on_parent`-coords* bug the
> file dialog just fixed, so Messagebox/Querybox/pickers may open between monitors
s> on multi-head X11. #1311 has since **MERGED** (`c882c3db`).
> **Housekeeping (prior session):** closed **#1224** (filedialog
> white-on-white — subsumed by #1242; the dark-mode base-style half was already
> fixed in #1239) and **#1252** (v1 empty/clearable DateEntry — superseded by
> shipped #1253 + 3.0 #1276).
>
> **Session 2026-07-27 — pre-release cleanup audit + the two bug fixes it and
> #1310 called for. TWO PRs OPEN at pause: #1312 (dialog positioning) and #1313
> (`color_to_rgb`).** A "what's left before 2.1" sweep found the repo green
> (suite 890, docs clean) and produced the punch list below; the author then
> asked for the bugs fixed.
>
> **#1313 (`fix/2.1-color-to-rgb-raises`, OPEN)** — `color_to_rgb`, a public
> export, swallowed every parse error with a bare `except`, printed the debug
> string `this` to stdout, and returned `None`. All five callers unpack into
> `r, g, b`, so a bad color surfaced as *"cannot unpack non-iterable NoneType"*
> naming neither the color nor the model. Now raises `ValueError` naming the
> value, chaining the PIL error. Not a new crash path in the color chooser —
> `on_entry_value_change` calls `widget.validate()` first. +5 tests.
>
> **#1312 (`fix/2.1-dialog-centering-multihead`, OPEN)** — fixes **#1310**, but
> **the issue's filed premise was wrong**: base `Dialog._locate` *did* apply its
> coordinates. The actual cause is that there are **two same-named
> `center_on_parent` functions with opposite contracts** —
> `internal/positioning.py` (pure, *returns* coords; used by datepicker +
> filedialog) and `internal/utility.py` (*applies* geometry, no clamp) — and
> `dialogs/base.py` was the last caller of the legacy one. Three defects, only
> the first visible off X11: (a) it measured the dialog with
> `winfo_width() or winfo_reqwidth()`, but **a dialog is withdrawn when it is
> positioned and an unmapped window reports width 1 — which is truthy**, so the
> fallback never ran and it centered a **1×1 box** (proven: the legacy helper
> applies `1x1+393+416`); (b) it re-applied a `WxH` size along with the offset;
> (c) it never clamped onto a monitor. `_locate` now runs the same
> center → clamp → apply sequence as the file dialog. The legacy helper **stays**
> — still reachable through the deprecated `ttkbootstrap.utility` shim until 3.0
> — with a docstring saying which of the two first-party code uses.
>
> **Then a `/review` of the merged #1311 found a real MEDIUM defect that this
> branch's fix shared, so it was folded in.** Both dialogs position while
> withdrawn, so `_window_size` falls back to the **content request — not the size
> the window will have**: FileDialog clamped against 578×445 but maps at 640×480
> (the `_build` floor); MessageDialog clamped against 122×102 but maps at 250×102
> (the `minsize` floor). Under-clamping left the right-hand column — the OK/Cancel
> buttons — past the screen edge, on the `position=None` path every
> `Querybox.get_*` wrapper uses. Fix: an optional **`size=` override** on
> `center_on_screen`/`center_on_parent`/`ensure_on_screen`; base `Dialog` derives
> a `_footprint()` from the minsize floor, `FileDialog` records the geometry
> `_build` applies. The review's two LOW findings also landed: #1311 had moved the
> `position` unpack outside the `try`, so `show(position=(1,2,3))` raised instead
> of centering; and its off-screen test asserted only that the result *moved*.
>
> **Then the author pushed back on "we can't know the monitor layout without
> `screeninfo`" — correctly, and the claim was wrong twice.** First for Windows
> (Tk reports the primary screen and the virtual desktop as *different* numbers,
> and the difference derives the grid — verified: it reproduces `screeninfo`'s
> answer exactly). Then, more importantly, in general: **Tk exposes no monitor
> enumeration on ANY platform, but the X server does.** `XineramaQueryScreens`
> returns the count and every monitor's `x/y/w/h` in one call. So
> `internal/positioning.py` now resolves the layout **screeninfo → X11 Xinerama
> via ctypes → Tk vroot**, matching how the library already reaches Windows' DPI
> and shell APIs (**the library has never used `subprocess`** — ctypes is the
> house pattern; don't shell out to `xrandr`). The query is skipped off X11,
> caches its own unavailability, and cannot raise. **Windows/macOS unchanged**;
> macOS multi-monitor still needs `screeninfo` (`CGGetActiveDisplayList` is a
> separate, undecided call). Suite **904**, and re-run with `screeninfo` forced
> off (136) so the fallback path is exercised.
>
> **KEY FACT to keep (why any of this is needed):** on X11 `winfo screenwidth`
> reports the **union of every display**, and `winfo vrootwidth` falls back to
> that same value unless a virtual-root WM is running (nothing modern sets
> `__SWM_VROOT`). So Tk's own metrics can never locate a monitor seam on X11 —
> which is exactly why a clamp against them let a dialog straddle two screens.
> Windows differs: `winfo screenwidth` is the primary monitor, `winfo vrootwidth`
> the virtual desktop.
>
> **VERIFICATION — Windows, macOS and X11 are ALL DONE.** New
> **`tools/verify_positioning.py`** prints a PASS/FAIL line per check plus the raw
> metrics; **Windows 4/4 (Tk 8.6.15, dual 2560×1440)**. Full instructions are in a
> comment on **#1310**.
>
> **X11 verified 2026-07-28 — 5/5** (WSL2/WSLg XWayland, Tk 8.6.12, Python 3.10.12,
> dual 2560×1440). Run twice as the instructions require: **without `screeninfo`
> 4/4** — the only way to exercise the new Xinerama path, and it read both monitors
> `[(2560,0,2560,1440), (0,0,2560,1440)]` while Tk reports one 5120×1440 screen
> *and* the same for `vroot`, which is the blind spot the whole fix exists for;
> **with `screeninfo` 5/5**, check 2b confirming the two sources agree exactly.
> **Two traps worth knowing before re-running it on X11:** (a) the script's check 4
> passed **vacuously** — WSLg reports a `-32730` sentinel position until the
> compositor has mapped a window, so `app.geometry(...)` + `update()` then building
> the dialog immediately parks the parent nowhere near the seam. Re-run by hand with
> a settle-wait it is genuinely green: parent at 2356 would naively centre the dialog
> across 2441..2691 (seam at 2560) and the fix lands it 2290..2540, wholly on the
> left monitor; four parent positions all landed inside one monitor. (b) **a
> `geometry()` readback is not the position you applied on X11** — a withdrawn
> window reports the WM's own placement (a dialog asked for `+4460+20` reads back
> `+32+32`), which is why the three `_locate` tests were rewritten to record the
> call instead. **The Linux suite is now GREEN — 917 passed, 0 failed** (branch
> `fix/2.1-linux-suite-gaps`), stable across repeat runs and with every affected
> module run standalone. It had never been run on Linux and sat at 16 failures;
> probing each group first turned up **one real bug** — `below_widget` applied
> `ensure_on_screen`'s 20px free-window margin to a *widget-anchored* dropdown,
> so a DateEntry within 20px of a screen edge had its calendar pushed off the
> entry (9px out for a target at x=11); `padding` now defaults to 0, the same
> reasoning that already gave it `titlebar_height=0`. **The third known flake is
> gone and was misdiagnosed:** `test_below_widget_flips_above_when_no_room_below`
> was never order-dependent — a geometry request is not applied synchronously, and
> until the WM places the window `winfo_rootx()` returns a sentinel, so it
> measured nothing unless an earlier test happened to pump the loop; a
> `_settled()` helper waits properly. The rest were test assumptions, each
> recorded in the commit: **Tk length lookups** can return `_tkinter.Tcl_Obj`
> pixel objects once a style is *built* (`int()` rejects them, `str()` renders
> the number) — confined to test helpers, since `_effective_style_option` is the
> only library consumer of a lookup and reads a *font description*, never a
> number; **font families that are not installed do not round-trip** (Tk
> substitutes, so `== "Georgia"` asserted the host's font inventory); and two
> tests over-claimed — `icon_only` height is approximate *by design*
> (`_build_icon_style`: padding is "fixed, not derived"), and `-topmost` is a
> hint a window manager may decline, so it is asserted at the kwargs seam like
> the aqua case already was. The former list of failures, for the record: `_tkinter.Tcl_Obj` from style lookups fed to
> `int()` (6), hardcoded Windows font names Georgia/Courier New (5), an icon padding
> metric, and two X11 window-manager behaviours. `test_below_widget_flips_above_when_
> no_room_below` is **order-dependent** — it fails run alone, passes in the full
> suite, and does so at the branch base too (a third known flake alongside the two
> already logged).
>
> **The two rough edges the macOS run found in the tool are FIXED** (on
> `feat/2.1-center-before-first-map`): a `hold()` helper now pumps the event loop so
> the LOOK windows in checks 4 and 6 actually stay on screen — `after(...)` plus a
> bare `update()` never waits, so both windows were torn down before anyone could
> look (check 4 had the bug too, not just the new check 6) — and a missing `else` on
> `if monitors:` made check 4 vanish silently when no layout is available; it now
> prints `[SKIP]` and a summary line.
>
> **macOS verified 2026-07-28 — 5/5 on BOTH Tk lines** (aqua, single 1470×956,
> Tk 8.6.17 and Tk 9.0.4; the Mac has a venv per Tk line — bare `python` is
> `.venv34`/Tk 9, `.venv` is Tk 8.6). The three headless API suites
> (`test_window_api` + `test_dialogs_api` + `test_filedialog_api`, 140 tests) pass
> on both, and so does the **FULL suite — Tk 9: 911 passed; Tk 8.6: 908 passed +
> 3 skipped** (the 3 are `test_scroll_events`' own Tk-9-only skips: 8.6 aqua
> reports a notch as 1 and generates no `<TouchpadScroll>`), which closes the
> punch list's "Tk 9 run on the Mac" item. **Both aqua-specific risks are
> closed:** check 3 (mapped size vs. the
> footprint we clamp against) PASSES — `250x104` both ways, so aqua chrome does
> *not* differ the way #1147 might have suggested; and centering is byte-identical
> on Tk 9 (`applied=(435,278)` == `want`), so 9.0's moved aqua scaling baseline
> doesn't shift it. Manual checks confirmed by eye: the themed file dialog opens
> fully on-screen and returns a POSIX path, and a 600×400 window is centered
> *before* it is displayed (no flash, no jump). **One known gap stays:** without
> `screeninfo` there is no monitor enumeration on aqua (`_monitors()` → `None` →
> whole-screen fallback, correct on one display), so **multi-monitor macOS is
> still unverified** — that is the undecided `CGGetActiveDisplayList` call, not
> anything this branch regressed. Installing `screeninfo` turns checks 1 and 4
> green. **ACCEPTED ASSUMPTION (author, 2026-07-28): multi-monitor macOS is taken on
> trust — there is no second display to test with.** What that actually leaves
> unverified is narrow, because the path splits: **with `screeninfo` installed** the
> layout comes from that package and everything after it is platform-independent
> arithmetic, already covered live on dual-monitor Windows (4/4) and dual-monitor
> X11 (5/5) and synthetically by
> `test_clamp_uses_the_monitor_under_the_point_not_the_whole_desktop`, so the only
> untested link is screeninfo's own aqua backend — a third-party concern, and one
> the Mac confirmed works on a single display. **Without `screeninfo`** aqua has no
> enumeration at all (Xinerama is X11-only, pinned for `darwin` by
> `test_xinerama_query_is_skipped_off_x11`), so placement falls back to Tk's screen
> metrics; the genuinely unknown fact is what `winfo screenwidth`/`vrootwidth`
> report on a two-display Mac. That unknown is made *safe* rather than merely
> untested by `test_placement_stays_on_screen_when_no_layout_is_available`, which
> pins the property that matters: with no layout, a window still lands fully inside
> the screen Tk describes, so the worst case is landing on the wrong display —
> never straddling two or hanging off an edge. **The real closure is the deferred
> `CGGetActiveDisplayList` ctypes call** (the aqua sibling of the Xinerama work);
> note it would be *partly* verifiable on a single display, since a correct
> implementation must return one rect matching the main display.
>
> **Two rough edges in the verification tool itself** (found while running
> it; **both since FIXED** — see the X11 entry above): when `_monitors()` returns
> `None` the whole check-4 block was skipped *silently* — the run reported 4 checks
> instead of 5 with no "skipped" line; and check 6's window was destroyed at script
> exit, because `app.after(2000, probe.destroy)` is followed only by
> `app.update()`, which does not wait — so there was nothing on screen to eyeball.
> (Check 4 carried the same window-teardown bug, which this run did not reach.)
>
> **Session 2026-07-28 (WSL2/Linux box) — everything below is MERGED to `master`
> and pushed.** Seven branches: **#1312** dialog centering (X11 verified here,
> macOS verified on the Mac — gate closed); **`feat/2.1-center-before-first-map`**
> (`place_window_center` before the first map + `verify_positioning.py` check 6);
> **`fix/2.1-filedialog-no-parent`** (`Querybox.get_open_filename()` with no
> parent raised `AttributeError` on X11 — the one platform where the themed
> dialog is the default, which is why it shipped); **#1313** `color_to_rgb`;
> **`fix/2.1-linux-suite-gaps`** (the suite is GREEN on Linux — see above);
> **`chore/2.1-version-catchup`** (`master` was still 2.0.0 — see above); and
> **`fix/2.1-demo-window-placement`**. Suite **919**, docs clean under `-W`.
>
> **Three facts worth carrying forward.** (a) **`withdraw()` goes before you build
> a window's contents, not after.** Building widgets *shows* the window, and
> re-showing an already-shown window is a fresh placement the WM decides for
> itself — measured drifting hundreds of px, differently each run. Reproduced in
> **pure tkinter** (raw `tk.Tk()`, raw `geometry("+x+y")`), so it is the window
> manager, not us. This is why `python -m ttkbootstrap` opened off-screen: it
> never positioned itself at all. (b) **Two sources of truth need an ordering, not
> a preference.** `_unmapped_size` first preferred the recorded size (stale after a
> WM maximize), then the realized size (stale against a `geometry` call made while
> hidden) — both wrong. A record now survives only between the `geometry` call
> that set it and the next map, so the *newer* wins; all four orderings are
> tested, one test per failure direction. (c) **`git merge-tree | grep '^<<<<<<<'`
> is not a reliable conflict check** on modern git — it reported "0 conflicts" for
> two branches that then conflicted for real. **Do a throwaway trial merge**
> (`git checkout -b tmp/check master && git merge --no-commit …`) before claiming a
> branch is ready.
>
> **Environment on the WSL box** (fresh this session): `.venv` now has `pytest`,
> `screeninfo` and the docs requirements installed; `credential.helper` is set
> **repo-locally** to the Windows-side Git Credential Manager
> (`/mnt/c/Program Files/Git/mingw64/bin/git-credential-manager.exe`), which is how
> pushes authenticate — `git config --local --unset credential.helper` undoes it.
> `gh` is **not** installed, so PRs cannot be opened from here; this session's
> merges were done locally and pushed to `master`.
>
> **Session 2026-07-28b (Windows box) — the demo opened off-centre; fixed, and
> the verification gap that hid it closed. MERGED 2026-07-30b; **x11 VERIFIED
> 2026-07-30c and macOS 2026-07-30d, so the cross-platform gate on
> `verify_positioning.py` check 7 is now CLOSED on all three platforms.**
> The branch sat unmerged
> for two days because it was written on Windows *after* the Linux session closed
> out, so no later session knew it existed. In the meantime `master`'s suite was
> **red on Windows** — `test_unmapped_size_falls_back_to_content_raised_to_minsize`
> failed there, returning the content request `(14, 19)` instead of the
> `minsize` floor `(500, 300)`, because after `update_idletasks()` a withdrawn
> win32 **Toplevel** also reports a realized size, so the `winfo_width() > 1`
> inference fires and skips the floor. That widens the bug below: it is not
> root-only, and the platform gap made the Linux suite green while Windows was
> not.
> `_unmapped_size` decided "has this window ever been shown?" with
> `winfo_width() > 1`. That is x11 reasoning: there a never-mapped window really
> does report 1x1, but on **win32 the root reports the size Tk started it at**,
> so the demo centred a 600x200 box that maps at 846x696 — applied `+980+620`
> instead of `+857+372`, ~123px right and 248px down. **Only the root is
> affected** (a win32 Toplevel does report 1x1), which is why every existing
> Toplevel-based test passed. Being shown is now *tracked* (`_ever_shown`, set
> from the `<Map>`/`<Configure>` handler) rather than inferred, with the watch
> installed in both `App.__init__` and `Toplevel.__init__`. A `/code-review`
> then found three **pre-existing** defects in last session's size bookkeeping
> (each reproduces at the branch base); two cheap ones were folded in — the
> handler is gated on `winfo_ismapped()` so a **stale** map dispatched after a
> newer `geometry()` cannot discard it, and it also listens to `<Configure>`
> because a `geometry()` call on an already-shown window is realized at once and
> otherwise never retires. The third (a user's `bind("<Map>", ...)` without
> `add=True` clobbers the watch — LOW, pre-existing) was **deliberately left**;
> the fix wanted a private bindtag plus a `destroy` override on every window,
> which the author judged not worth the lifecycle surface. **File it if it ever
> bites.**
>
> **WHAT NEEDED RUNNING:** `tools/verify_positioning.py`, whose docstring
> explains why a green run on one box proves little — **done on all three**
> (Windows in this session, x11 2026-07-30c, macOS 2026-07-30d) — plus
> `python -m pytest -q` (**924 passed, 3 skipped** on Windows; green on x11 and
> both macOS Tk lines too) and an eyeball of `python -m ttkbootstrap`, **which
> has only ever been done on Windows**. **The risk being checked is narrow:** on x11 old and
> new code both fall through to the content-request path, so behaviour is
> identical there; what is new is that a *shown-then-withdrawn* window returns
> its realized size only if the flag got set, i.e. only if the event arrived.
> Measured on Windows, `winfo_ismapped()` is already 1 in **both** handlers, and
> the flag is still set with `<Map>` suppressed — so `<Configure>` backstops it
> and the mechanism does not hinge on map timing, the part most likely to differ
> under a window manager.
>
> **The verification gap is the more valuable lesson.** Check 6 (“centered
> before first map”) passed against this bug the whole time, because it uses
> `Toplevel(size=(600,400))` — the *explicitly sized* path, which this never
> touched. Closing it took three attempts, each failing for a different reason
> worth knowing: a `Toplevel` cannot reproduce it (win32 reports 1x1 there, so
> the check must spawn a **subprocess** with its own never-shown root); and
> content packed **straight into the root** lets Tk settle on the real size
> before anyone measures, so the check must build into a frame **packed
> afterwards**, as the demo does — variant A reads `winfo=(600,246)`==mapped,
> variant B reads `(600,200)` vs mapped `(600,246)`. New **check 7** now reads
> FAIL/5-of-7 at the branch base and PASS/7-of-7 with the fix. **Standing rule:
> prove a new check fails against the bug by reverting the fix, never by reading
> the code.**
>
> **Session 2026-07-30 (WSL2/Linux box) — #1309 (X11 menu border) is DONE.**
> PR **#1314**, squash-merged to `master` as **`07a37ae`**; suite **929**
> (919 + 10 new in `tests/test_menu_border.py`). **The next session is on the
> Windows box — see "Handoff to the Windows box" below.**
>
> **The fix.** A themed popup menu had no border on Linux (menubutton/`OptionMenu`
> dropdowns, right-click menus, menu-bar cascades). The recipe set
> `borderwidth=0, relief="flat"`; on Windows/macOS a popup is a **native OS menu**
> whose frame supplied the border, so only x11 — where Tk draws the whole menu
> itself — was left with none. Gated on `scaling.windowing_system`, so the native
> platforms keep byte-identical configuration.
>
> **Why it takes an indirect route (all three measured, not assumed).** Tk gives
> `tk.Menu` **no border color of its own**: it has no `highlightthickness`,
> `relief="solid"` is **hardcoded black** (`#000000`, unaffected by `-foreground`
> /`-background`), and the 3D reliefs derive *both* shades from `-background`
> (`#e6e6e6`/`#999999` on a white bg — a bevel, not a hairline). The only route to
> a flat `colors.border` hairline is to paint the **menu** in the border color and
> each **entry** in the surface color: entries tile a popup's whole interior, so
> only the 1px strip shows.
>
> **The trap, and why the paint waits for `<Map>`.** That holds for a popup and
> **not** a menu bar, whose entries cover only the left of the bar — painting one
> floods the rest (measured: an entire menubar filled `#d6d6d6`). Detecting
> menubars is unreliable, because `Menu(app)` → `configure(menu=…)` means a menu
> is *not yet* one when it is styled. But **Tk displays a menu bar through a
> clone** (`.!menu` original + `.#!menu` clone, `-type menubar`), so the widget we
> style never maps — waiting for `<Map>` makes the two cases separate themselves
> with nothing to detect. The same hook catches entries added *after* theming,
> which inherit the menu background and would otherwise come up border-colored.
> The repaint rides its own bind tag, so a caller's `bind("<Map>")` cannot
> displace it (verified: both fire).
>
> **Two consequences on Linux, logged in `2_1_changes.md`:** entry colors are
> **theme-managed** (an entry given its own `background` keeps it; the rest follow
> the theme), and **`menu.cget("background")` returns the *border* color** — read
> `style.colors.bg` for the surface.
>
> **REUSABLE — pixel verification on WSLg.** Claims about what Tk *draws* were
> settled by capturing real pixels. **Pillow's `ImageGrab.grab(xdisplay=…)` and
> `xwd -root` both fail under WSLg** (`BadMatch` on the XWayland root), but
> **`xwd -id <widget.winfo_id()>` works** once the window is actually mapped —
> and only then, since WSLg reports the `-32730` sentinel position until the
> compositor places it (the settle-loop trait already recorded for
> `verify_positioning.py`). No netpbm/ImageMagick is installed, so the XWD v7 dump
> is parsed directly (25-field header, endianness detected via `file_version == 7`,
> RGB via the visual's masks) — ~70 lines. **A posted menu is capturable this
> way**, which is how the border, the menubar flood, the hover highlight and the
> `tk_popup` path were all confirmed. **Sample away from separators** — a
> separator draws a 3D line spanning the full width and will masquerade as a
> border pixel (it confounded the first measurement run).
>
> **Process notes (three, all mine).** (a) **`git reset --hard` discards
> uncommitted WIP** — rewinding `master` this session destroyed the author's
> untracked-to-me working-tree edits (`.gitignore`,
> `examples/file_dialog_default_routing.py`; author confirmed they did not matter).
> Being careful not to *commit* someone's WIP is not the same as not *destroying*
> it: **stash first, or use a plain `git reset`**, when the tree is dirty.
> (b) **"push" is not "merge"** — merging straight to `master` foreclosed the PR
> the author then asked for, costing a force-push to undo. Push the **branch**
> first; merging is a separate decision. (c) **GitHub squash-merges PRs**, so the
> merge commit is a *new* SHA and `git branch -d` reports "not fully merged" —
> confirm the content landed, then `-D`.
>
> **Opening a PR without `gh`.** `gh` is still not installed on the WSL box, but a
> PR *can* be opened from here: read the token from the same credential helper the
> pushes use (`git credential fill` → the `password=` line, never printed) and
> `POST /repos/israel-dryer/ttkbootstrap/pulls`, then `PATCH /issues/<n>` to set
> the **milestone** and topical label per the repo convention. Installing `gh`
> would make this a one-liner and is worth doing.
>
> **NEXT — the rest of the pre-2.1 punch list. The 2.1 milestone now has ZERO
> open issues** (verified via the API this session: #1309 auto-closed on merge,
> #1242 was already closed). Everything below is housekeeping, not features:
> **bump `pyproject.toml` → 2.1.0** — **DONE**, and it is the *first* step of the
> release proper, so everything after it (build, `twine check`, upload, tag,
> GitHub release, clean-env verify) follows in one sitting per the "Releasing"
> runbook under *Dev environment & commands*. Until the upload lands, **2.0.1 is
> still the latest released version**, which is why the change log's scope line
> still names it.
> **DONE 2026-07-30b (Windows):** the prior-art trees are deleted, the branch
> prune is finished remotely, and the stale root scripts are gone — see that
> session's entry below. **CI now EXISTS** (`.github/workflows/ci.yml`, #1317,
> badge #1318, macOS added in #1319): the suite on **all three windowing systems**
> — Linux, Windows and macOS on py3.13, plus the py3.10 floor — and the docs under
> `-W`, on push to `master` and every PR. It closes the gap that let a
> Windows-only suite failure sit on `master` for two days (#1315).
> **`screeninfo` is deliberately left out** so the runners exercise the fallback
> layout path, and the Xvfb display is pinned to 96 dpi so it is a
> standard-density screen rather than an arbitrary one. **What CI does NOT
> cover:** Tk 9 (every runner is Tk 8.6) and anything visual — so the
> per-platform manual gates below are still manual.
>
> **HANDOFF TO THE WINDOWS BOX (next session, from 2026-07-30).** The last few
> sessions ran on WSL2/Linux; the next is on Windows, which is a **different
> working copy** — the WSL checkout is `/home/iddryer/ttkbootstrap` and its `.venv`
> is a *Linux* venv, so none of it carries over. Start with:
>
> 1. **`git pull`** — `master` is **`07a37ae`** (the #1314 squash merge). The
>    Windows copy is behind by at least that.
> 2. **Use the venv that matches the profile you are on.** Per "Dev environment"
>    above, `.venv-home` belongs to the *other* Windows profile (its base
>    interpreter is under `C:\Users\Israel Dryer\...`) and is unusable from the
>    `Logistiview` profile, which has the docs deps in `.venv`. Neither is stale.
> 3. **Expected gates:** suite **929** (`python -m pytest -q`), docs clean under
>    `-W`.
>
> **What the menu fix means for Windows — nothing should change, and that is the
> thing to confirm.** The border is gated to x11, so Windows keeps the native OS
> menu chrome it already had. Two specific implications:
>
> - **No screenshot recapture is needed.** Windows is the canonical capture box and
>   Windows rendering is unchanged, so every existing menu shot (`menus.rst`, the
>   dropdown/popup shots in the widgets catalog) stays valid. Do **not** re-run the
>   harness for #1309.
> - **The headless tests already cover the Windows branch** —
>   `tests/test_menu_border.py` *forces* the windowing-system probe both ways
>   (the #1229 convention), so `win32`/`aqua` are asserted on Linux and x11 is
>   asserted on Windows. A 60-second eyeball of a real menubutton dropdown is
>   still worth it, since "unchanged on Windows" is the claim the gate rests on
>   and it has only been verified by forcing the probe, never on the platform.
>
> **Verified on Linux, unverified elsewhere:** the border itself (all four edges
> `colors.border`, light and dark) was confirmed against real pixels on X11 only —
> which is the only platform it applies to, so nothing is outstanding.
>
> **Session 2026-07-30b (Windows box) — branch cleanup, and the stranded window
> fix it turned up. Two PRs.** Started as housekeeping — delete every merged
> branch, local and remote — and the audit that gate required found real work.
>
> **#1315 (MERGED) — the stranded fix.** Twelve local branches deleted and six
> remote; two of the twelve were not ancestors of `master` because GitHub
> squash-merges (verified patch-equivalent via `git cherry`, and `master` had
> since superseded both). One branch survived the sweep —
> `fix/2.1-center-content-sized-root`, three commits refining `_unmapped_size`,
> written on **this** box at 13:58 on 07-28, *after* the Linux session closed out
> at 08:47. Because its own `CLAUDE.md` entry never landed, no later session knew
> it existed. **`master`'s suite had been red on Windows for two days** as a
> result. The whole episode was the argument for CI — there was none at the time,
> and `pytest` + `sphinx -W` would have caught it the same day — which is why this
> session ended by adding it (#1317, then macOS in #1319).
>
> **How to check a squash-merged branch** (the reusable part): `git branch
> --merged` is necessary but not sufficient. `git cherry master <branch>` matches
> by **patch-id**, so it still reports 0 for a squash-merge whose content landed;
> a non-zero count means *look*, not *unmerged*. And read the diff direction —
> `git diff master..<branch>` showing thousands of deletions means the branch is
> **behind**, not that it carries removals.
>
> **#1316 — the cleanup.** `development/` now holds only design and handoff
> documents (`filedialogs/`, `scrolledframe/`, `validatedinput/` deleted — the
> #1250 precedent), and two stale root scripts are gone: `build_instructions.txt`
> said to bump the version in `setup.py` and run `python setup.py sdist`, and
> there is no `setup.py`; `setup_project.bat` built a `venv\` and installed
> `requirements.txt`, which resolved to documentation deps alone, so its
> environment had no pytest. `requirements.txt` now declares the real gate set
> (RTD is unaffected — `.readthedocs.yaml` reads `docs/requirements.txt`
> directly), and `tmp/` is ignored. `build_instructions.txt`'s steps did not just
> vanish: **this file now carries a "Releasing" runbook** under "Dev environment
> & commands," which is where the version-bump-on-`master` convention and the
> 2.0.1 stranded-bump warning now live.
>
> **`AGENTS.md` is DELETED, and the reasoning generalizes.** It was an
> orientation file for non-Claude agents, frozen since ~2026-07-01, and it did not
> merely lag — it instructed the *opposite* of current practice: cut every PR
> against the retired `2.0` branch, suite is 177, and the docs are "MkDocs, not
> Sphinx" with a directive to write docstrings in plain Markdown and avoid reST.
> Docs moved to Sphinx in #1148; #1246 then had to clean up four leftover mkdocs
> `!!!` admonitions in docstrings — exactly the drift that instruction causes.
> **Author ruling: don't keep a second hand-maintained instruction file.** This
> one can be regenerated at will, so a parallel copy buys nothing and guarantees
> staleness; the unique content (the release runbook) was ported here first.
> **A stale instruction file is worse than no file** — the same argument that
> keeps the 3.0 shim list grep-discoverable instead of hand-maintained.
>
> **Two environment facts.** `gh` **is** installed on this box (2.92.0), unlike
> the WSL box — so PRs are a one-liner here. And an **editable install wins over
> a worktree's own `src/`**: a branch suite run from a worktree silently tested
> `master`'s code and reported 5 failures; pin `PYTHONPATH` when testing a branch
> checked out elsewhere.
>
> **Session 2026-07-30c (WSL2/Linux box) — the x11 gate on check 7 is CLOSED.**
> `tools/verify_positioning.py` was run on WSLg XWayland, Tk 8.6.12, Python
> 3.10.12, dual 2560×1440, twice as the docstring requires: **with `screeninfo`
> 8/8**, and **without it 7/7** (forced off with an `ImportError` shim placed
> ahead of `src` on `PYTHONPATH`, so the check-7 subprocess inherits it too —
> that is the only way to exercise the Xinerama path). The new **check 7 is
> green on x11**: a content-sized root predicted 600×258 and mapped 600×258,
> centered at exactly the wanted coords. Nothing regressed: check 3's footprint
> matched the mapped size, and 2b confirmed Xinerama and `screeninfo` agree
> exactly. **The full suite is 933 passed, 4 skipped on Linux** (up from 929 at
> #1314). The demo eyeball is still unrun here.
>
> **Check 4 passed vacuously again, and the WSLg trap deserves restating.** In
> the no-`screeninfo` run the dialog landed at 171..421 — nowhere near the
> 2560 seam it is supposed to straddle — because WSLg reports a sentinel
> position until the compositor has mapped a window, so `app.geometry(...)` +
> `update()` parks the parent nowhere. Re-run by hand with a settle-wait it is
> genuinely green: with the parent really at x=2362, naive centering spans
> 2447..2697 across the seam while the clamp lands the dialog 2290..2540, wholly
> on the left monitor; four parent positions all landed inside one monitor.
> **Treat an in-script check-4 PASS on this box as unproven until the parent's
> `winfo_rootx()` is confirmed to be where it was asked to go.**
>
> **Session 2026-07-30d (macOS box) — the macOS gate on check 7 is CLOSED, so
> `verify_positioning.py` is now green on all three platforms.** Run on aqua,
> single 1470×956, against **both Tk lines** as the docstring requires —
> Tk 8.6.17 (`.venv`) and Tk 9.0.4 (`.venv34`, what bare `python` resolves to) —
> and, as on x11, twice: **with `screeninfo` 7/7 on both lines**, and without it
> **5/6 with 1 skip and 1 fail on both**. The count is 7 here rather than x11's 8
> because **check 2b (Xinerama and `screeninfo` agree) only runs on x11**; aqua
> runs check 2 instead, which asserts the Xinerama path is *skipped* off X11.
>
> **The no-`screeninfo` fail/skip is the known aqua gap, not a regression:**
> `_monitors()` returns `None` (Xinerama is X11-only, pinned for `darwin` by
> `test_xinerama_query_is_skipped_off_x11`), so **check 1 FAILS** and **check 4
> SKIPS** — correct on one display, and made *safe* rather than merely untested
> by `test_placement_stays_on_screen_when_no_layout_is_available`. Both go green
> the moment `screeninfo` is installed. **New check 7 is green on aqua:** a
> content-sized root predicted **600×252** and mapped **600×252**, and 7b
> centered it at exactly the wanted `(435,352)` — so the `_ever_shown`
> `<Map>`/`<Configure>` tracking works where map timing was most likely to
> differ. Nothing else moved: **check 3's footprint is `250x104` == mapped on
> both Tk lines** (aqua chrome does not differ, confirming 07-28), and check 6
> applied `(435,278)` == want with no flash or jump.
>
> **ENVIRONMENT CORRECTION: `screeninfo` was NOT installed in either macOS
> venv**, despite the 2026-07-28 entry above reading as though it had been left
> installed — so the first run of the session was the fallback path whether or
> not that was intended. It is in the root `requirements.txt` gate set and was
> `pip install`ed into **both** venvs this session. **Check which venv actually
> has it before reading a check-1 FAIL as a regression** (`p._HAS_SCREENINFO` is
> printed in the header).
>
> **STILL UNRUN on macOS:** check 5 is **manual and was not run** — it opens a
> blocking modal file dialog, which is exactly what
> [[feedback_dialog_testing]] says not to drive externally; run
> `Querybox.get_open_filename(native=False, parent=app)` by hand and confirm it
> opens fully on-screen with OK/Cancel visible and returns a forward-slash path.
> The `python -m ttkbootstrap` demo eyeball is also still unrun here. And
> **multi-monitor macOS remains taken on trust** (no second display) — the real
> closure is still the deferred `CGGetActiveDisplayList` ctypes call, the aqua
> sibling of the Xinerama work.
>
> **Session 2026-07-30e (Windows box) — 2.1.0 SHIPPED.** Version bumped to 2.1.0
> (#1323), release notes written from `development/2_1_changes.md`, gates re-run
> (**934 passed, 3 skipped**; docs `-W` exit 0; CI green on all three windowing
> systems), `python -m build` + `twine check` PASSED, **uploaded to PyPI by the
> author**, annotated tag `v2.1.0` + GitHub release published, and verified by a
> clean-environment install. The published artifacts are byte-identical in size to
> the locally built ones (535,901 / 576,678).
>
> **The smoke test went past "does it resolve."** On a fresh venv installing from
> PyPI: warning-free import, 30 themes, a live theme switch, the **vendored icon
> font present on disk** (package data, the classic wheel failure), and all three
> headline features — `Querybox.get_open_filename`, value tokens
> (`bootstyle="#2f4f4f"` and `"primary[300]"`), and a durable option surviving a
> variant build (`danger.TEntry` → `padding=(8,)`).
>
> **Three release-mechanics traps, all found by doing it rather than reading it.**
> (a) **`dist/` is gitignored, so it keeps the previous release's artifacts** — it
> still held the 2.0.0 wheel and sdist from July 19, and the runbook's
> `twine upload dist/*` would have tried to re-publish 2.0.0. Runbook fixed in
> #1324: empty `dist/` first, upload by explicit version glob, and check wheel
> *contents* because `twine check` validates metadata only. (b) **PyPI's JSON API
> and the simple index propagate separately** — the JSON API returned 2.1.0
> immediately while the index pip reads did not have it yet, so the first
> clean-env install failed on a release that was genuinely live. (c) **pip then
> cached that empty index page**, so it kept failing *after* propagation;
> `--no-cache-dir` is what fixes it. Verify a fresh release with that flag, or a
> cache will read as a broken release.
>
> **Noted, not fixed: `ttk.__version__` does not exist** (and did not in 2.0.x
> either). `import ttkbootstrap; ttkbootstrap.__version__` is a common reflex and
> currently raises `AttributeError`. Additive, `2.1.x`-shaped, unfiled.
>
> **Also this session:** the branch sweep that started it (12 local + 6 remote
> merged branches deleted), the stranded #1315 window fix it uncovered, the
> `AGENTS.md` deletion, CI (#1317/#1319), the badge and change-log review (#1318),
> the milestone backfill, and #1322 filed.
>
> **Session 2026-08-02 (Windows box) — 2.1.1 SHIPPED: the widget type stubs are
> back.** Started from discussion **#1326** — "updated to 2.1.0, hover
> documentation is gone" — filed as **#1327** and fixed in **#1328**, with the
> version bump as **#1329**. Suite **992 passed, 5 skipped**; CI green on all four
> jobs.
>
> **The bug, and why nobody had reported it.** 1.x shipped a hand-written
> `__init__.pyi` spelling out every widget's keywords. 2.0 PR 3 (`66dfa45a`)
> deleted it when the monkey-patch became real subclasses, expecting inheritance
> to carry the signatures. It doesn't: **`BootMixin` precedes the ttk class in the
> MRO and its constructor is `(*args, **kwargs)`**, so that is what an editor
> resolves, leaving the one-line class docstring as the whole tooltip. The quieter
> half is worse — `py.typed` kept shipping, so mypy and pyright read the same
> `**kwargs` and **stopped checking widget keywords entirely**. That failed *open*,
> which is why it sat unreported through 2.0 and 2.1.
>
> **The fix is generated, not hand-maintained** (`tools/generate_widget_stubs.py`,
> regen instructions under *Dev environment & commands*). Which classes need
> stubbing is **discovered** — an exported mixin subclass whose ctor is generic —
> and each one's options *and description* come from the authored reference pages
> under `docs/reference/api/`, so the tooltip and the documentation cannot drift.
> A measured fact made a strict stub possible: **the reference tables already cover
> the live Tk option set**, the only gaps being `bd`/`bg`/`fg` (documented inline
> as ``background`` (``bg``) — parse them, don't hardcode a list), the entry-family
> `background`, and Tcl's `from`. So the stub declares **no `**kwargs`** and a typo
> is an error again.
>
> **THE LESSON WORTH KEEPING: type-checking cannot see a bad tooltip.** The first
> version type-checked perfectly under both mypy and pyright and still showed the
> *wrong* hover — the `Args:` docstring sat on the **class**, so editors read
> `__init__`, found nothing, and fell back to `BootMixin.__init__`'s "*args /
> **kwargs" text, i.e. the original bug in disguise. Only an actual hover request
> caught it. Hence **`tools/verify_hover.py`**: drives **pyright over LSP**
> (`textDocument/hover` — what VS Code/Pylance renders) plus **jedi**, and was
> proven to fail against that defect by reverting the fix. **PyCharm cannot be
> scripted** — the author checked it by hand and confirmed it good.
>
> **A `/code-review` then found six real defects the self-review missed**, every
> one reproduced by probe before acting. Two were the stub being *wrong*, not
> merely narrow: **`Menu` was re-declared `(AutoStyleMixin, tkinter.Menu)`**, which
> discarded `ttkbootstrap.menu.Menu` and its five macOS application-menu methods
> (#1174) — a public API vanishing from editors, the very failure the PR existed to
> fix; and **`ttk.OptionMenu.__init__` pops only `style`/`direction`/`name`/
> `command` then raises `TclError: unknown option`**, so the menubutton options on
> its page type-checked and then crashed. The rest were false positives on working
> code — `font=("Helvetica", 12)`, tuple `values=`/`columns=`, Pillow's
> `ImageTk.PhotoImage`, a Tk image *name*, `takefocus=""`, and `class_` on classic
> tk widgets (only Frame/Toplevel extract it). **Standing rules from that:** a
> class defined outside `__init__.py` must subclass its **real implementation**, not
> be rebuilt from the mixin; and value annotations stay **wider than the docs'
> shorthand**, because rejecting working code is worse than missing a wrong value.
> My own sweep had missed the false positives because it counted only `call-arg`
> and never `arg-type`.
>
> **Three test-design facts.** The sync test **regenerates in a subprocess** —
> `enable_global_api()`, which another test enables, wraps `__init__` on the
> tkinter classes, so an in-process run reads the wrapper and the test passes alone
> but fails in the full suite. The completeness audit compares against
> `configure()` keys and therefore **structurally cannot see a filtering
> constructor**, which is how OptionMenu got through; a second test now builds each
> widget with every keyword the stub offers. And the Options regex needs `\Z`, or a
> page ending in its table parses as **zero options** and silently stubs that widget
> with no keywords — nothing would fail, since the sync test compares against the
> same empty output.
>
> **Release mechanics.** `dist/` again held the previous release's artifacts, as
> #1324 warns. The **PyPI JSON API had 2.1.1 immediately while the simple index pip
> reads had zero entries** — the 2.1.0 trap, so `--no-cache-dir` on the verify
> earned its place again. Published sizes were byte-identical to the local build.
> Author feedback on the notes, now in memory: **unwrapped is not unstructured** —
> the first draft was correctly unwrapped and rejected as a wall of prose; release
> notes need real section headings and bullet lists, and folding the *wrapped*
> `2_1_1_changes.md` into them means **rewriting each paragraph as one long line**,
> never pasting it through.

Order (dependency- and design-gate-driven), with status:

1. **#1253 — `DateEntry.value` nullable (additive slice). DONE (#1277).** The
   release turned two of the original acceptance criteria into breaking changes, so
   #1253 was split along the semver line (recorded in the issue comment): the
   **additive** slice shipped behind an internal `_UNSET` sentinel — omitted `value`
   still defaults to today (2.0.0 behavior preserved, no break); explicit
   `value=None` gives a genuinely empty, clearable field (`clear()`,
   `set_date(None)`, `value = None`), and `get_date()` returns `None` **only** for a
   widget that opted into the nullable model (entering it via ctor `value=` or a
   runtime `clear()`). The **breaking** finish — `value=None` as the default +
   dropping the `_startdate` empty-read fallback unconditionally — is deferred to
   **3.0**, tracked in **#1276**.
2. **#1238 + #1161 — durable style options. DONE (design #1278, impl #1279).**
   #1238/#1160/#1161 were ONE design problem: a *durable style-options layer* so a
   user's `style.configure("TEntry", padding=…)` survives a bootstyle-variant build
   or theme switch. Brief (decisions LOCKED):
   `development/2_1_durable_style_options_design.md`. **Mechanism:** capture the
   geometry subset of user overrides on the **public** `Style.configure` into a
   theme-independent `Style._user_options` registry, and re-apply it after every
   build (`_register_ttkstyle` tail) so user values are the last write and beat the
   recipe. The seam that makes it work: **builders write via the internal
   `_build_configure`, users via the public `configure`** — so recipe writes are
   never captured. Locked decisions: **geometry allowlist** (`DURABLE_STYLE_OPTIONS`
   in `style/engine.py`; colors stay theme-reactive), **base→variant fan-out**
   most-specific-wins, `reset_style_options()`, `map` overrides out of scope.
   Three implementation findings worth remembering:
   - **Fan-out had to become retroactive.** Build-time-only fan-out is
     order-dependent (a variant built *before* the override never got it), so
     recording also pushes onto already-built descendants.
   - **Two framework seam violations fixed** — `create_default_style`
     (`symbol.Link.TButton`/`tooltip.TLabel`) and `apply_icon`'s derived style were
     calling the *public* `Style.configure` internally, which would miscapture their
     `font`/`padding`/`relief` as fake user overrides. **Rule: framework code uses
     `_build_configure`, never the public `configure`.**
   - **Durability ≠ the widget honoring the option.** The layer faithfully
     persists any allowlisted option — including ones the widget never reads. Two
     probed cases the docs must name: (a) ttk `Entry`/`Combobox`/`Spinbox` read
     `font` from the widget/named font (`TkTextFont`), **not** the style, so
     `configure("TEntry", font=…)` persists but never renders (entry height
     unchanged at 29px, vs 50px when set on the widget); (b) `sashthickness` works
     **only** on the global pseudo-style `"Sash"` — `configure("TPanedwindow",
     sashthickness=20)` persists and does nothing (sash gap stays 2px vs 20px via
     `"Sash"`), because `ttk::panedwindow` is a C widget querying the literal name
     `"Sash"` and has no `Sash` element in its layout to namespace. `padding` —
     the actual #1238/discussion-#536 ask — is honored and renders (29→59px).
   Guarded by `tests/test_durable_style_options.py` (+16) incl. an **AST guard**
   asserting every non-color option any recipe writes is in the allowlist (it
   already caught `pbarrelief`).
3. **#1160 — Treeview/Tableview rowheight ignores the configured font. DONE
   (#1281).** The *companion* builder fix, not the durable layer: `treeview.py`
   computed `rowheight` from `TkDefaultFont` at build time, so a configured font
   clipped rows. Row height now derives from the style's effective font, resolved
   via a new **`Style._effective_style_option`** — which prefers a durable override
   over the live Tcl `lookup`, because **overrides are re-applied AFTER a recipe
   runs**, so a recipe deriving geometry from an option would otherwise compute
   from the pre-override value. (Before that: `configure(".", font=…)` worked but
   `configure("Treeview", font=…)` silently did not.) Metrics come from Tk's
   `font metrics`, which accepts any font *description* (named font, tuple, or
   `-size N` spec), so no `Font` object is allocated per build. The two row
   formulas live in `_grid_row_height`/`_tree_row_height` **so the geometry passed
   to `configure(rowheight=…)` carries no numeric literal** — that keeps
   `test_scaling`'s AST guard strict instead of widening its font-metric
   exemption. Locked scope was build-time only; live font-change recompute stays
   out (an existing style is not rebuilt).
4. **Docs slice. DONE (#1283).** *Change an option everywhere* (fan-out,
   specificity, retroactivity, the colors exception, `reset_style_options`) plus
   *Options a widget doesn't read*, in `feature-guides/custom-styles.rst`. #1161's
   "not discoverable" half resolved HERE, deliberately: a `bootstyle` keyword for
   sash thickness would be misleading, since `bootstyle` is per-widget but sash
   thickness is process-global. **rST trap learned:** a line block (`|`) inside a
   list-table cell needs a **blank line before it**, or the literal `|` leaks into
   the rendered text — and `-W` does NOT flag it (same class as the earlier
   double-backtick bug). Verify built HTML, don't trust a clean build.

**Review round (post-#1281).** A `/review` over the combined `#1279 + #1281` found
three real defects, all fixed in **#1282**: (a) a base-class override **stretched
`icon_only` buttons** (29×29 → 103×27) because #1279 wired the derived icon style
into fan-out — triggered by exactly the workflow #1238 enables; (b) **notebook tab
padding was silently un-overridable** — the recipe mapped `padding`/`bordercolor`
to the *same* value for both `selected` and `!selected`, and since those cover
every state, `lookup` always resolved through the map and masked any user
`configure` (vanilla ttk honors the same call, so this was ours, not Tk's; note
`bordercolor` had **no** `configure` value, only the map, so it had to move into
`configure` rather than just be deleted); (c) `_effective_style_option` **swallowed
falsy lookups** (`or None` turned a real `borderwidth=0` into the caller's
default). Perf was measured and dismissed (0.06 ms per `configure` with 44 built
styles). A second review of #1282/#1283 confirmed all three fixes correct
(notebook values identical across *every* state; the icon fix not over-broad — a
text+icon button still follows a global override) and found one latent issue,
now **#1284**.

**Open follow-ups from those reviews:** **#1284** (icon styles register *before*
they configure, so `registered ⇒ configured` is false — a failed configure leaves
a permanently blank icon the build gate never rebuilds; low severity, self-heals
on theme change), **#1286** (backfill tests for guarantees we rely on but don't
pin), and **#1285** (design question: should the layer *warn* when a durable
option can't take effect? Four distinct no-op cases surfaced — silently inert
overrides are the worst failure mode for a "set it once and it sticks" promise).

**Standing lesson from this cluster:** durability ≠ the widget honoring the
option. `style.configure` persistence cannot make a widget read an option it never
reads. Probed cases: `font` on `Entry`/`Combobox`/`Spinbox` (they use the widget /
named `TkTextFont`), and `sashthickness` (only the global `"Sash"` style works —
`ttk::panedwindow` is a C widget querying that literal name). A third class is
**self-inflicted**: a recipe that `map`s an option for *all* states masks
`configure` entirely — audit for that shape before adding a map.
5. **#1236 — bootstyle value tokens (hex + ramp accents/surfaces). DONE
   (2026-07-24; PRs #1300/#1301/#1302 + the #1299 test-infra spin-off).** Design
   session settled §10 of `development/2_1_bootstyle_value_tokens_design.md`
   (CONFIRMED); see the Phase-2 entry in the status banner above for the full record.
6. **#1242 — in-house themed file dialog (X11 default; opt-in elsewhere).** Biggest
   single build (draw our own dialog; the Tk X11 `tkfbox.tcl` canvas hardcodes a
   white panel no styling can reach). Most standalone, lowest urgency (dialog is
   already functional/readable). Prior art was in `development/filedialogs/`
   (deleted 2026-07-30b once the dialog shipped; recover from git if ever needed).
   Natural
   drop-candidate if 2.1 needs to close sooner.

NOTE (line numbers): #1160/#1161 reference `src/ttkbootstrap/style.py:NNNN` — filed
pre-2.0-split; those recipes now live in the `style/builders/` package (per-family
modules registered via `@register_builder`, e.g. `builders/treeview.py`), with
`builders_ttk.py` only the thin `StyleBuilderTTK` coordinator.

**3.0 (future major) — deferred breaking work.** GitHub **milestone #2 (`3.0`)** is
the home for cleanup deferred out of 2.x. Two kinds: (a) the **~30 code shims**
marked `removed in 3.0` across ~19 source files — grep-discoverable
(`grep -r "removed in 3.0" src`), so intentionally NOT enumerated in a meta-issue (a
hand-maintained list would just drift); (b) **design decisions** with no code shim
(e.g. a future default change), which ARE the fragile ones and get their own tracked
issues. First such issue: **#1276** — make `DateEntry` `value=None` the default +
drop the `start_date` empty-read fallback (the 3.0 half of #1253). Don't build a
full 3.0 removal checklist until 3.0 is actually scoped.

## Direction: 2.2 milestone (IN PROGRESS)

> **STATUS (2026-08-05): the 2.2 milestone's two PRs are both MERGED and the
> review gate is CLOSED — nothing released yet.** `master` reads **2.1.1**, which
> is still the latest released version, and the 2.2 milestone (#4, created this
> session per the standing rule) now has **no open issues or PRs**. The next step
> is the release proper whenever the author wants it: the "Releasing" runbook
> under *Dev environment & commands* (bump `pyproject.toml` on `master`, fold in
> `development/2_2_changes.md`, gates, build, upload, tag).
>
> **SUPERSEDED (2026-08-06b): the release is no longer the next thing.** An
> unmerged branch, `feat/2.2-version-and-cli`, now carries four more 2.2 items —
> `__version__`, the `ttkb` CLI, pre-root `Theme.register()`, and the #1322 fix —
> plus the review round that followed. **Land that branch first**; the release
> runbook below is still correct and still next after it. See the two 2026-08-06
> session entries at the end of this section for the branch's state and what the
> next session owes it.
>
> **HANDOFF — THE NEXT SESSION IS THE 2.2 RELEASE** (final checks, then ship).
> Set up 2026-08-05; everything below was verified on the Windows box at
> `e05a9deb`, so start by confirming nothing moved rather than re-deriving it.
>
> **State at handoff.** `master` = `e05a9deb`, tree clean, no open PRs, 2.2
> milestone at 0 open / 3 closed. Suite **1015 passed, 5 skipped**; docs clean
> under `-W`; CI green on all four jobs. The complete user-visible surface of
> 2.2 since `v2.1.1` is seven files — the new `convert_theme.py`, the
> `load_user_themes` docstring in `engine.py`, four docs pages, and the
> converter's tests. That is the whole release: **one feature plus its docs.**
>
> **`development/2_2_changes.md` is complete and is the release-notes source.**
> It was audited against `git diff v2.1.1..master` this session and the one gap
> found — #1333's scrollbar fix, missing entirely — was added. Do not assume it
> is still complete if anything lands before the release; re-run that diff.
>
> **Follow the "Releasing" runbook** under *Dev environment & commands*. Four
> traps it already documents that are **live right now**, so do not skip them:
>
> - **`dist/` still holds the 2.1.1 wheel and sdist** (it is gitignored, so it
>   keeps whatever the last release built). Empty it first and upload by
>   explicit version glob — a bare `dist/*` would try to re-publish 2.1.1.
> - **A local docs build cannot confirm the version bump.** This checkout's
>   editable install reports **`2.0.0a1`** through `importlib.metadata`, which is
>   what `docs/conf.py` reads. RTD installs fresh and is unaffected.
> - **`twine check` validates metadata, not contents** — confirm the wheel
>   carries `ttkbootstrap/assets/icons/` (the vendored font is package data; a
>   wheel missing it installs and then fails at first render) and that the sdist
>   has no `docs/` or `development/`.
> - **Verify the clean-env install with `--no-cache-dir`.** PyPI's JSON API and
>   the simple index propagate separately, and pip caches the empty index page —
>   this bit both 2.1.0 and 2.1.1, each time reading as a broken release.
>
> **Two decisions the release needed — both now made** (2026-08-06 session,
> below): **`ttk.__version__` is IN** (it never existed before), and **#1322 is
> FIXED**, so it moves to the `2.2` milestone rather than a `2.2.x` bucket.
> `.pypirc` is present at the repo root.
>
> **One milestone chore belongs to that release: #1322 must come off `2.1.x`.**
> A patch is cut from `master` and `release/*` is only for superseded majors, so
> the moment `master` reads 2.2.0 there is no branch a 2.1.2 could come from and
> `2.1.x` is unreachable. Move #1322 to **`2.2`** if it is fixed first, else to a
> new **`2.2.x`** bucket, and close `2.1.x`. It gates nothing — four
> asset-geometry tests that fail only on a non-baseline-density display,
> test-only and contributor-facing.
>
> **The two PRs, both milestoned `2.2` and squash-merged 2026-08-05:**
>
> - **#1332** (`6f01984b`) — the theme converter + the docs gap that prompted it,
>   plus the review round below.
> - **#1333** (`d40e6ef8`) — a one-line docs render fix, independent of #1332.
>
> **What #1332 shipped.** 2.0 removed the in-package user theme store
> (`themes/user.py` + `USER_THEMES`) and ttkcreator's Import/Export buttons, but
> **the migration guide never said so** and offered no path forward for an
> already-saved theme. New `python -m ttkbootstrap.convert_theme` reads **all
> three** artifacts 1.x could produce — a `user.py` holding `USER_THEMES`, a `.py`
> holding a `ThemeDefinition(...)` call, or a `load_user_themes` JSON — and emits
> the equivalent `Theme(...).register()` call. Pure text transformation, no Tk, no
> display. Accents + `secondary` + that mode's background/foreground carry over;
> the plumbing colors (`border`/`inputbg`/`inputfg`/`selectbg`/`selectfg`/
> `active`) and the `light`/`dark` accents are **dropped** because `Theme` derives
> them, and the opposite mode is left **commented out** rather than invented.
> Suite **1015 passed, 5 skipped**; docs clean under `-W`.
>
> **Three facts worth carrying forward.**
>
> (a) **The 1.x artifact is a `.py`, not a `.json`** — settled by reading
> `release/v1`, and it inverted the design. 1.x `save_theme` wrote
> `'USER_THEMES = ' + json.dumps(...)` **into the in-package `user.py`**, and
> Export was `shutil.copyfile` of that file. So the *contents* are JSON but the
> *file* is a `.py`, and that is the **only** `json.dump*` call in all of 1.x
> `src/` — no 1.x code ever wrote a `.json`. The `{"themes": [...]}` shape
> `load_user_themes` reads was hand-authored only. Hence `ast.literal_eval` of the
> `USER_THEMES` assignment is the primary input path.
>
> (b) **`load_user_themes` never went away and is the thinner path.** It works
> fully in 2.1 (ramps, `@surface`, value tokens all resolve against a JSON-loaded
> theme) but **bypasses the legacy adapter**: it takes all sixteen 1.x colors
> verbatim where `theme_from_legacy_dict` *regenerates* `border`/`inputbg`/
> `active` from `bg` (measured on identical input: border `#ced4da` verbatim vs
> `#d6d6d6` adapted). It also registers a **single mode**, so `toggle_theme()`
> has nothing to flip to. Its docstring was one line and never stated the file
> format; #1332 fixes that.
>
> (c) **A converted theme is close, not pixel-identical** — an accent is
> re-derived per mode for contrast, so a dark theme's authored `#6a5acd` resolves
> to `#887bd7`. Documented rather than hidden.
>
> **THE REVIEW ROUND (2026-08-05b) — six defects, and one of them was the
> review's own.** The `/code-review` gate found 4 MEDIUM + 2 LOW in #1332, all
> fixed in `a65d55e3` before merge. Precedent held for the third time running: a
> careful self-review had missed every one, and two were the artifact being
> *wrong* rather than merely narrow.
>
> - **Unescaped interpolation into generated source.** Every value went into the
>   emitted file raw. 1.x only did `name.lower().replace(" ", "")`, so a quote in
>   a theme name emitted a file that would not compile — and a crafted *color*
>   value could close the string and append its own keyword argument, which then
>   **executed on import** of a file we tell people to run. Fixed by routing every
>   value through `json.dumps`, whose string escapes are a subset of Python's, so
>   the double-quoted output style is unchanged.
> - **A whole 1.x export format rejected.** ttkcreator had **three** save paths,
>   not two (`release/v1:src/ttkcreator/__main__.py:34-38`): Save, Export all
>   themes, and **Export theme definition**, which writes a `.py` holding
>   `ThemeDefinition(name=..., themetype=..., colors={...})`. That is the one most
>   likely to be in a user's own project, since the other two live *inside* the
>   installed package. Now read, in both the keyword and the 1.x positional
>   `(name, colors, themetype)` spellings.
> - **A parity claim that was wrong for half its keys** — see (b): the docs said
>   the six dropped plumbing colors get "the same regeneration the built-in legacy
>   themes get," but `theme_from_legacy_dict` regenerates only **three** and
>   passes `inputfg`/`selectbg`/`selectfg` verbatim. Replaced, not narrowed.
> - **The `light`/`dark` accents dropped silently** and absent from the documented
>   drop list. Now stated in the generated header, the migration guide and the
>   change log, pointing at `Theme(neutral=...)`.
> - Two LOW: the `-o` write sat *outside* the `try` (bare `FileNotFoundError`
>   traceback), and shape errors in parseable input (`{"themes": null}`,
>   `USER_THEMES = [1, 2]`) reached `TypeError`. Input shape is now validated
>   where it is read, so the `except` tuple stays precise instead of widening to
>   swallow genuine bugs. And a **`:func:` role on a method** — the Python domain
>   maps `func` only to `objtype: function`, so `Style.toggle_theme` never
>   resolved and, with `nitpicky` off, rendered as unlinked text under a clean
>   `-W` build.
>
> **THE FINDING THAT WAS WRONG, and why it matters more than the five that were
> right.** The review proposed mapping 1.x `light` → 2.x `Theme(neutral=)`,
> reasoning that `_DEFAULT_NEUTRAL` is byte-identical to `#adb5bd` — "strong
> evidence" of the intended mapping. That value came from **the PR's own test
> fixture**, not from any 1.x theme. The shipped 1.x catalog's `light` is a
> near-white (`litera`, ttkcreator's default base, ships `#F8F9FA`), which
> corresponds to `Colors.light` = **ramp step [100]**, not the ramp *base*. Since
> `neutral` also drives `selectbg` and an uncolored `secondary`, passing a
> near-white through as `neutral` would have washed out selection backgrounds
> across the theme. **A review finding is a hypothesis with a reproduction
> attached, not a verdict** — the reproduction proves the *defect*, which does not
> make the proposed *fix* right. Probe the recommendation against real data
> (`STANDARD_THEMES`, `release/v1`) before implementing it.
>
> **Two process facts, both already in this file and both earned again.** (a) A
> branch showing large deletions in `git diff master..<branch>` is **behind**, not
> carrying removals — #1333 read as `CLAUDE.md | -75` purely because master had
> moved. (b) `merge-tree | grep` is not a conflict check: a **throwaway trial
> merge** is, and it is also the only way to gate the *combined* result, which
> neither PR's own CI covers (each runs in isolation). Both were trial-merged
> together and re-gated — 1015 passed, docs clean, stray-backtick scan clean —
> before either was merged.
>
> **A THIRD `-W`-invisible rST class**, alongside the two already recorded (nested
> inline markup inside `**bold**`; a line block inside a list-table cell needing a
> preceding blank line): **an inline-literal start-string not preceded by
> whitespace never parses.** ``` ``first``..``last`` ``` shipped raw double
> backticks to the rendered page, because rST only begins markup after whitespace
> or an opener (`(` `[` `<` `-` `:` …) and `.` is not one — while the *closing*
> backticks of `first` were fine, since an end-string may be followed by
> punctuation. That is why the line rendered half-correct. **The cheap catch-all:
> strip tags from every built page and search the body text for surviving
> ``` `` ```** — it catches all three classes at once. After #1332 + #1333 that
> scan is clean across the whole site. A clean `-W` build is still not evidence
> the markup parsed.
>
> **Session 2026-08-06 — four more things landed on 2.2 before the release, on
> the branch `feat/2.2-version-and-cli` (7 commits, not pushed, no PR yet).**
> Gates: suite **1031 passed, 5 skipped**; docs clean under `-W`; the strip-tags
> stray-backtick scan clean; **every commit independently green** (verified in a
> worktree with `PYTHONPATH` pinned — an editable install otherwise wins over a
> worktree's own `src/`). The author asked for `__version__`, #1322 if it was
> doable, and a live demonstration that the theme converter works; the CLI and its
> docs came out of that conversation.
>
> **THE `/code-review` OF THOSE 7 COMMITS IS DONE (2026-08-06b) — 4 findings, all
> real, all fixed in 3 follow-up commits. The branch now has 10 commits, still
> unpushed with no PR.** Gates after the fixes: suite **1033 passed, 5 skipped**;
> docs clean under `-W`. Precedent held for the fourth round running — a careful
> self-review had missed every one.
>
> | Fix commit | What the review found |
> |---|---|
> | `3530c673` `fix(themes): keep every pre-root theme registration` | **MEDIUM.** The deferral commit keyed the queue on the *family name*, and the seam keeps one applier per key — so two `register()` calls splitting a family across separate `Theme` objects collapsed to the last. Probed: pre-root `['acme-dark']` vs post-root `['beta-dark','beta-light']`, i.e. **the queue changed the answer**, silently, surfacing only as `theme_use` raising later. Now a key per call. |
> | `40642e23` `fix(cli): only claim ttkcreator is missing when it is` | **LOW.** The `try` wrapped an import that executes all of ttkcreator, so an `ImportError` from *inside* it reported "ttkcreator is not installed". Narrowed to `ModuleNotFoundError` naming ttkcreator itself; anything else re-raises. Trailing newline too. |
> | `e6e2b617` `test: rebuild the eager styles at the pinned density` | **LOW.** #1322 was only half fixed: the pin lands after `Window()`, so the styles `create_default_style` builds on the way up stayed sized to the host. Re-running it re-sizes them — the recipes are invoked unconditionally, the build-once check is at the call site (probed: stale `10 4` → `15 6` at `tk scaling 2.0`). |
>
> **A counter, not `id(self)`.** The review proposed keying on `id(self)`, as
> `on_theme_change` does for callbacks. **`Theme(...).register()` need not keep a
> reference**, so the object can be collected and its id reused by the next theme
> — reinstating the very collision. `itertools.count()` in `theme.py` instead.
> ([[the #1332 lesson]] again: the reproduction proves the *defect*, not the
> proposed *fix*.)
>
> **The #1322 guard is asserted on conftest's SOURCE, and that is a deliberate
> compromise worth re-examining.** The first version read the eight eager styles'
> geometry, re-ran `create_default_style`, and compared — it **passed alone and
> failed in the full suite**, because it mutates global style state mid-run and
> some earlier test leaks a `Link.TButton` padding of `40 2` that the rebuild
> reset. So `create_default_style` is idempotent at session start (nothing has
> been configured yet) but **NOT** once styles carry overrides. The replacement
> asserts the pin precedes the rebuild in conftest's text, proven to fail with the
> rebuild line removed. Testing it properly would mean driving a scaled root in a
> subprocess.
>
> **NEXT SESSION — `/code-review` the three fix commits (`d7561785..HEAD`), then
> ship the branch.** The first four commits are already-reviewed context, not the
> subject. It cannot be launched from inside a session (`disable-model-invocation`
> — reserved for explicit user invocation), so the author runs `/code-review`.
> Three questions worth putting in front of it, since the author of the fixes is
> not a neutral judge of them:
>
> 1. **`style/theme.py`** — module-level `itertools.count()` and a per-call defer
>    key. Anything the per-family key didn't have: unbounded queue growth, or
>    `register()` in a loop queueing duplicate work that all runs at flush?
> 2. **`tests/conftest.py`** — the second `create_default_style()` call is safe
>    *only* because nothing is configured at session-root creation. That is the
>    claim to check, given it is demonstrably not idempotent later.
> 3. **`tests/test_scaling.py`** — is a source-order guard reasonable here (the
>    repo has precedent), or papering over a claim that wants a real test?
>
> **Then:** fold in any fixes, open the PR against `master` with the **`2.2`
> milestone set** (on the PR, not just the issue), and move **#1322** off `2.1.x`
> onto `2.2` since it is fixed here — closing `2.1.x` out.
>
> **Unrelated, noticed in passing — a pre-existing test-isolation leak.** Something
> in the suite leaves `Link.TButton` padding at `40 2`. Invisible unless a test
> re-runs a builder mid-suite, which is how it surfaced. Not caused by this branch;
> worth a look sometime, not a release gate.
>
> **(1) `ttkbootstrap.__version__`** — read from the installed metadata
> (`importlib.metadata.version`), so `pyproject.toml` stays the one place the
> literal lives, matching what `docs/conf.py` already did. **It also has to be
> declared in `__init__.pyi`**: a `.pyi` replaces the module for type checkers,
> and the stub generator's `_reexports` pass sources every name from an *import
> statement* in `__init__.py`, so an assignment is invisible to it. Proven both
> ways with pyright — `reportAttributeAccessIssue` without the declaration, `str`
> with it. The line lives in `_HEADER` in `tools/generate_widget_stubs.py`. The
> flip side of reading metadata is that it reports what was **installed**, so an
> editable install lags a bump; that is why no test asserts it against
> `pyproject.toml`, and why **`ttkb version` cannot confirm the release bump
> without a reinstall** — the same trap the runbook already records for the docs
> build. (`.venv-home` on this box reports `2.0.0a1`; `.venv314`, which `python`
> resolves to, reports `2.1.1`.)
>
> **(2) The `ttkb` command line** (`src/ttkbootstrap/cli.py`, new
> `docs/reference/cli.rst`, `tests/test_cli_api.py` +12) — `version` · `demo` ·
> `convert-theme` · `creator`, installed under **two** `[project.scripts]` names
> (`ttkb` and `ttkbootstrap`) per the author's choice. Each subcommand already
> existed as its own `python -m` invocation that nothing surfaced; all of those
> still work. The converter's arguments moved into a shared
> `convert_theme.add_arguments`/`run` pair so the two spellings cannot drift, and
> `__main__.py` (demo) and `ttkcreator/__main__.py` grew a `main()` instead of
> bare `if __name__` blocks. **Standing docs rule, memory-saved:
> [[feedback_docs_use_ttkb_cli_spelling]] — the docs say `ttkb <command>`
> everywhere**, even where another spelling works; the alternatives are stated
> once, in a note on the CLI page. README updated to match, and its
> `ttkbootstrap-icons` link repointed at **`tkinter-icons`**, the extension's
> current name (verified live: repo + PyPI both exist).
>
> **(3) `Theme(...).register()` now works before the App exists** — found by
> actually running a converted theme rather than reading it. It raised
> `RuntimeError: No Style instance yet`, which made the natural top-of-file form
> impossible *and* made a custom theme unusable as an `App(theme=...)` argument:
> registration needed the app, and the app needed the name. It now queues on the
> **deferred-config seam that already existed for this exact shape**
> (`utils/config.defer`, the `set_default_button` tenant) — and because
> `flush_pending_config()` runs in `Style.__init__` *before* `theme_use(theme)`,
> `import brand; ttk.App(theme="acme-light")` just works. The theme is still
> **validated eagerly** at the `register()` call, so a missing anchor raises where
> it is written rather than out of a window constructor. `install_legacy_themes()`
> got the same treatment and still warns from the call site. Three tests in
> `test_theme_anchor.py`; the two docs pages that said "register after the App
> exists" were rewritten.
>
> **(4) #1322 is FIXED** — `tests/conftest.py` pins the shared root to
> `Scaling.baseline` (4/3, or 1.0 on aqua before Tk 9), which is the issue's own
> suggested fix. **Reproduced before fixing**: forcing `tk scaling 2.0` in the
> fixture produced exactly the four filed failures with the issue's 144-dpi
> numbers — `(23,23)`, `(60,8)`. With the pin the **whole suite passes at 1.0,
> 1.4, 1.6667 and 2.0**, so the fix is density-independent rather than
> Windows-shaped. Pinned *after* the root is built (`Window()` makes the root and
> the `Style` together); the handful of eagerly-built styles carry the host's
> density, and empirically nothing asserts their geometry. New
> `test_test_root_runs_at_baseline_density` guards the invariant. **The milestone
> chore still applies**: move #1322 off `2.1.x` (to `2.2`, since it is now fixed)
> and close that milestone out, or it becomes unreachable when `master` reads
> 2.2.0.
>
> **The converter demonstration** (the author's third ask) ran end-to-end on real
> 1.x artifacts reconstructed from `release/v1`'s own save code — a `USER_THEMES`
> `user.py`, a `ThemeDefinition(...)` export, and a `load_user_themes` JSON, built
> from two shipped 1.x specs. All three converted; the generated module was
> imported and rendered light and dark. Two findings came out of *running* it, not
> reading it: the registration bug in (3), and that the generated header stopped a
> step short — it now names the registered variant (`app = ttk.App(theme="acme
> -light")`), since the 2.x name is `<family>-<mode>`, not the 1.x name.
>
> **`development/2_2_changes.md` is updated for all four** (new *Testing*
> section). The release notes source is therefore current as of this work — but
> re-run `git diff v2.1.1..master` before the release, as the handoff says.
>
> **Two process notes from assembling the branch.** (a) **The Bash tool is not
> PowerShell** — `git commit -m @'…'@` there passes a literal `@` as the first
> line of the message, which is how the first commit got a stray `@` subject
> (fixed by `--amend -F`). Write the message to a file and use `-F`; it sidesteps
> every quoting difference between the two shells. (b) Splitting mixed files
> across single-purpose commits without interactive staging is done by
> *temporarily reverting* the other thread's hunk, committing, and re-applying it
> in the later commit — three files needed it here (`README.md`,
> `feature-guides/theming.rst`, `migrating.rst`) plus the converter's generated
> header, which could only claim `App(theme=…)` once the deferral commit made it
> true.

## Repository layout

```
src/ttkbootstrap/
  __init__.py        # public exports; defines the concrete BootMixin/AutoStyleMixin widget
                     #   subclasses (e.g. `class Button(BootMixin, ttk.Button)`) that carry the
                     #   `bootstyle`/`autostyle` api + fluent pack/grid/place (return self). No
                     #   import-time monkey-patch (2.0, PR 3) — opt into it via enable_global_api().
                     #   Blessed tk widgets: Tk/Menu/Text/Canvas/Listbox/TkFrame/TkLabel.
                     #   `LabelFrame` is the ttk alias for `Labelframe` (matching tkinter.ttk),
                     #   NOT the classic tk widget (that 1.x meaning was dropped — see
                     #   development/2_0_breaking_changes.md).
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
  internal/          # PRIVATE plumbing (no underscore in the name): publisher.py, utility.py,
                     #   positioning.py, configure_delegation.py, busy.py (tkinter busy shim).
                     #   No back-compat guarantee. See "internal/ vs public" below.
  utility.py         # PUBLIC utility funcs: enable_high_dpi_awareness, scale_size
  publisher.py       # deprecation shim -> internal/publisher.py (warns; removed in 3.0)
tests/               # HEADLESS pytest only (4 test_*.py + conftest.py). CI-runnable.
examples/            # interactive mainloop() demos (moved out of tests/ in #1068)
docs/, gallery/      # documentation and showcase apps
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
- Build docs: `python -m sphinx -b html -W -q -E docs <out>` (must exit 0 — the
  docs are kept warning-clean; RTD enforces `fail_on_warning`). Deps in
  `docs/requirements.txt`. **`.venv-home` belongs to the author's other Windows
  profile** (its base interpreter lives under `C:\Users\Israel Dryer\...`), so it
  is unusable from the `Logistiview` profile — the docs deps were installed into
  `.venv` there on 2026-07-27. Use whichever venv matches the profile you are on;
  neither is stale.
- `pip install -r requirements.txt` (root) installs the local gate set — pytest,
  `screeninfo`, and the docs deps. RTD reads `docs/requirements.txt` directly.
- **An editable install wins over a worktree's own `src/`.** A branch suite run
  from a `git worktree` silently tests the *main* checkout's code; pin
  `PYTHONPATH` to the worktree's `src` when testing a branch checked out
  elsewhere.
- **Regenerate the type stub** after adding a widget or editing an `Options`
  table on a `docs/reference/api/` page: `python tools/generate_widget_stubs.py`
  (writes `src/ttkbootstrap/__init__.pyi`; `--output` targets somewhere else).
  `tests/test_widget_stubs.py` fails until the committed stub matches, and it
  regenerates in a **subprocess** — an in-process run would read the `(*args,
  **kwargs)` wrappers `enable_global_api()` installs on the tkinter classes,
  since another test in the suite enables it. The same file also audits the
  reference tables against the live Tk option set, so an undocumented option
  fails there rather than becoming a false positive in a user's type checker.
- **The stub's *tooltip* is a separate, manual gate:**
  `python tools/verify_hover.py` (needs `pip install pyright jedi`). A stub can
  type-check perfectly and still show the wrong hover — the first working
  version put the `Args:` docstring on the class, so editors read `__init__`,
  found nothing, and fell back to `BootMixin.__init__`'s "*args, \*\*kwargs"
  text. The script drives **pyright over LSP** (`textDocument/hover`, i.e. what
  VS Code/Pylance renders) and **jedi** for signature + `bootstyle=`
  completion. **PyCharm is not covered and cannot be scripted** — check it by
  hand when a report names it, as #1327 did.
- **CI runs the two automatable gates** (`.github/workflows/ci.yml`, #1317) on
  push to `master` and every PR: the suite on **all three windowing systems** —
  Linux, Windows and macOS on py3.13, plus the py3.10 floor from
  `pyproject.toml` (macOS added in #1319) — and the docs under `-W`.
  `fail-fast` is off so one platform's failure cannot hide another's — the whole
  reason it exists, after a Windows-only failure sat on `master` for two days
  (#1315). All three report **identical counts**, which is the signal to watch:
  the suite's platform branches are forced probes (the #1229 convention), not
  `skipif`, so every box runs the whole matrix and the numbers should match.
  **`screeninfo` is left uninstalled on purpose** (it is optional at runtime, so
  omitting it exercises the more fragile fallback layout path), and the Xvfb
  display is pinned to 96 dpi to be a standard-density screen.
- **CI does not cover Tk 9 or anything visual.** Every runner is **Tk 8.6** — the
  workflow reports the Tcl/Tk build per job rather than leaving it inferred from
  the Python version, because 8.6-vs-9 is the split behind the aqua dpi baseline
  and the scroll-event contract. Adding a Tk 9 job is not free: `setup-python`
  ships no interpreter built against it. Visual gates stay manual and still need
  the right box — see `tools/verify_positioning.py` and the screenshot harness.

### Releasing

No CI publishes; the upload is manual, with credentials in a gitignored
repo-root `.pypirc`. **`master` is always the most recent release** — a patch
release is cut from `master`, so the version bump lands there naturally;
`release/*` exists only for *superseded* majors.

1. Bump `version` in `pyproject.toml`, **at release time, on `master`**. It is the
   only place the version is written — nothing under `src/`, `docs/` or `tools/`
   hardcodes it. 2.0.1 shipped its bump on a throwaway `release/2.0` branch and
   `master` kept claiming 2.0.0 for days — don't repeat that branch.
   `docs/conf.py` reads the *installed* distribution's version through
   `importlib.metadata` into `release`/`version`. Neither is rendered anywhere
   today (`html_title` is a fixed string and there is no version switcher), so a
   wrong value is latent rather than visible — but do not read a local docs build
   as confirmation of the bump: an editable install keeps whatever metadata it was
   built with, and this checkout's has read **2.0.0a1** for the whole 2.x cycle.
   RTD is unaffected; it installs fresh, so it reports the real version.
2. Fold `development/2_<x>_changes.md` into the release notes.
3. Run the gates: the full suite, and the docs build under `-W`.
4. **Empty `dist/` first**, then `python -m build`, then `twine check dist/*`, then
   upload **by explicit version glob** — `twine upload dist/ttkbootstrap-X.Y.Z*`.
   `dist/` is gitignored, so it keeps whatever the last release built: at 2.1.0 it
   still held the 2.0.0 wheel and sdist from July 19, and a bare `dist/*` upload
   would have tried to re-publish 2.0.0 alongside the new version. Worth spending
   a minute on the artifact while you are there — `twine check` validates metadata
   but not contents, so confirm the wheel carries `ttkbootstrap/assets/icons/`
   (the vendored Bootstrap Icons font is package data, and a wheel missing it
   installs and then fails at first render) and that the sdist has no `docs/` or
   `development/` in it.
5. Annotated tag `vX.Y.Z`, plus a GitHub release titled the same way.
6. Verify with a clean-environment `pip install ttkbootstrap==X.Y.Z`.

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
- Branch + PR per change. **Work targets `master`** (now the 2.0 mainline; the
  `2.0` branch is retired). 1.x maintenance, if any, targets **`release/v1`**.
- **Set a milestone on every issue AND every PR** — not just issues. The
  milestone is the single source of truth for "which release is this in"
  ([[feedback_no_version_labels]] is the other half: no `Version x` labels), and
  it is only as good as its coverage. Most 2.1 PRs went unmilestoned, so
  `gh pr list --search "milestone:2.1"` returned 17 when 19 code changes had
  shipped — the milestone stopped being usable for exactly the question it
  exists to answer, and reconstructing the release required diffing merged PR
  numbers against the change log by hand. Set it when you open the PR;
  `gh pr edit <n> --milestone "2.1"` after the fact works but is easy to forget.
