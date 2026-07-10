# ttkbootstrap 2.0 — Session Handoff

> Living handoff for the 2.0 cleanup. Update at the end of each working session.
> Pair with `development/2_0_plan.md` (the durable worklist) and `CLAUDE.md`.

_Last updated: 2026-07-10 (**Surface-color workstream COMPLETE — ALL PRs MERGED into
`2.0`: PR 1 #1149 / PR 2 #1150 / PR 3 #1152 / PR 4 (bar families) #1154 (merge
`7953d2de`, branch deleted). PR 4 COMPLETES the family rollout, so the whole
surface-color workstream is DONE. >>> NEXT = RESUME docs Workstream H (next entry
below): iterate the Sphinx skeleton, then sub-PR 2 = reference generators.**
A mid-stream initiative that interrupted the docs work (next entry). Fixes a real
theming gap: every built style assumed widget bg == app bg (`colors.bg`), so a
ghost/link/outline control on a non-default surface (a card, an accent toolbar)
could not blend — surfaced running old examples (`gallery/collapsing_frame.py`).
Full design + per-PR log: `development/2_0_surface_color_design.md`.
**THE API (locked — learn this first):** a widget's surface is a `@<surface>` TOKEN
INSIDE the bootstyle string, NOT a separate param (because `bootstyle` is the compact
spelling of the ttk style name, and the style name already carries the `@surface`
segment). **Spaces are the recommended separator:**
`ttk.Button(bootstyle="@primary success ghost")` → style name
`@primary.success.Ghost.TButton`. A surface is a named neutral (`card`) OR an accent
color (`@primary`, so a control ghosts against an accent container). **Additive:** no
`@token` ⇒ byte-for-byte the pre-surface names/appearance. Memories:
`bootstyle-spaces-and-surface-token`, `styling-permissive-not-paternalistic`,
`project-surface-color-pass`.
**MECHANISM (`style/`):** `constants.surface_segment()` = the single `@<surface>.`
formatter shared by resolver + builder (so names can't drift) + `BOOTSTYLE_SURFACE_TOKENS`.
`bootstyle._classify_tokens` reads the `@token`; `_build_ttkstyle_name` /
`_classify_style_name` emit/round-trip the segment (theme walk stays lenient — a
custom `@brand` style name never warns); `_normalize_surface` case-normalizes +
validates through the `_compat` strict gate; a **family gate** `_SURFACE_FAMILIES`
(now {button, checkbutton, radiobutton, toggle, label}) makes not-yet-migrated
families ignore surface. `builders_ttk`: `build_style` exposes the surface to the
recipe as transient `self._surface`; `surface_prefix` (f-string recipes) /
`StyleName(surface=)` (check/radio/scale) prefix the name; `resolve_surface(_surface)`
gives the color; `on_surface_fg()` flips fg for **accent** surfaces (near-bg
card/neutral keep the soft theme fg); `neutral_fill`/`mute`/`disabled` take a
`base=`/`surface` arg. A **graceful-degrade net** in `update_ttk_widget_style`: if a
gated family's recipe forgot `surface_prefix`, fall back to the plain style (not bare
clam). Frames are surface **PRODUCERS** — never gated (out of scope). Phase-2
parent-inheritance + raw-hex surfaces are DEFERRED (design §7 / §9). **Accepted
by-design (permissive, not paternalistic):** a control on its own matching accent
surface renders low-contrast (fg≈bg) — the user's color choice; the example uses
contrasting `light` accents.
**MERGED:** PR 1 #1149 (resolver + `card` token + strict-gate follow-up), PR 2 #1150
(grammar + engine + button family — squashed after a `surface=`-param → `@token`
reversal that review drove out), PR 3 #1152 (checkbutton/radiobutton/toggle/label +
degrade net + `examples/surface_preview.py` visual proof + a gate↔recipe
correspondence test). Each PR had 1–2 high-effort `/code-review` passes.
**PR 4 = the bar families (scale / progressbar / scrollbar) — DONE (committed on
`feat/2.0-surface-color-pr4`, not yet pushed/PR'd).** The last rollout piece,
following the same template. Added all three to `_SURFACE_FAMILIES` (now 8); swapped
the `border(colors.bg)` trough sites → `border(resolve_surface(_surface))`, the
`white=colors.bg` slider-handle glyph bake → `white=surface`, and the widget
`background`/scrollbar trough → the resolved surface; prefixed names via
`StyleName(surface=)` (scale) and inline `builder.surface_prefix(...)`
(progressbar/scrollbar — incl. striped/thin/round). Extended
`test_every_gated_family_honors_surface` with the three cases + added
`test_scale_tracks_surface` / `test_progressbar_trough_tracks_surface` /
`test_scrollbar_trough_tracks_surface`; `examples/surface_preview.py` now shows a
scale/progressbar/scrollbar per surface. Additive — surfaceless names/appearance are
byte-for-byte unchanged (no `2_0_breaking_changes.md` entry needed, design §8). Suite
618 (+3). **This COMPLETES the surface-color family rollout** (frames stay out —
producers). **MERGED as #1154** (merge `7953d2de`, branch deleted) — high-effort
`/code-review` came back clean (surfaceless path proven byte-for-byte unchanged; no
hardcoded consumers break). **>>> NEXT: RESUME docs Workstream H.**
**Still pending before the docs finalize:** the **deferred "spaces sweep"** —
regenerate the dash-joined `BootStyle` Literal + reference to the space form and touch
up docstrings so autocomplete/docs match the recommended spelling
(`tools/generate_bootstyle_reference.py`, sync-tested).
**Env/tests:** repo `.venv` exits 127 — run the headless suite with
`PYTHONPATH=src python -m pytest -q`; baseline ~609 passed EXCL two known order/env
flakes (`test_msgcat` nl.msg, one order-dependent `test_color_helpers`). Import must
stay warning-free. **User WIP: `gallery/collapsing_frame.py`** is modified in the
working tree — LEFT UNTOUCHED all session; keep leaving it alone. Prior entry
(docs Workstream H) follows._

_Last updated: 2026-07-10 (**Docs Workstream H — Sphinx skeleton spike MERGED into
`2.0` (#1148, merge `e88bd525`, branch deleted); NEXT = iterate the skeleton, then
sub-PR 2 (generators)**).
Sub-PR 1 of the docs rebuild (`development/2_0_docs_design.md` §11) is merged. It moves
the docs off mkdocs onto bootstack's stack and **proves the structure end to end**;
content is deliberately skeletal (stubs) and will be iterated. **What landed:**
**Clean cut** — deleted the whole mkdocs `docs/` tree (incl. `ja`/`zh`, ~134 files)
+ `mkdocs.yml`; repointed `.readthedocs.yaml` `mkdocs:`→`sphinx:` (py3.12); root
`requirements.txt` now `-r docs/requirements.txt`. **Lifted+adapted from bootstack:**
`docs/conf.py` (pydata theme + autodoc/napoleon/autosummary/intersphinx),
`_static/custom.css` (bootstack palette is already Bootstrap blue; screenshot/hero
classes reprefixed `bs-`→`tb-`), `_templates/autosummary/class.rst`, `Makefile` +
`make.bat`. **IA (4 destinations):** Landing (`index.rst`) → User Guide
(getting-started · concepts · how-to) → Widgets (grouped *Styling ttk widgets* /
*ttkbootstrap widgets*) → Reference (Style Reference + API Reference); every
`toctree` entry resolves, guide bodies are honest "being written for 2.0" stubs.
**Spike proof pages:** `widgets/button.rst` (native — leads with `bootstyle`,
cross-links Style Reference) + `widgets/meter.rst` (shipped catalog) +
`reference/api/widgets.rst` (autodoc `Meter` via `autosummary :toctree: generated`).
**Three spike findings baked in (IMPORTANT for the design doc):** (1) ttkbootstrap
documents ctor params in `__init__`, so `autoclass_content = "both"` (bootstack docs
params on the class — the one conf divergence); (2) `inherited-members: False` keeps
tkinter's ~200 members off the pages; (3) **the design's "docstrings feed autodoc
as-is / no rewrite" assumption is only half true** — ttkbootstrap docstrings use
**Markdown ```` ```python ```` code fences** (authored for mkdocstrings) that
napoleon/rST renders as broken inline literals. Resolved WITHOUT a docstring rewrite
via a small `autodoc-process-docstring` shim in `conf.py` (`_convert_markdown_fences`)
that converts fences to `.. code-block::` at build time. **Open decision for a later
slice:** keep the build-time shim vs. sweep the docstrings to rST. **Build gate:**
`.venv-home/Scripts/python.exe -m sphinx -b html -q docs docs/_build/html` → **22
pages, ZERO warnings**; Meter API page renders the `__init__` Parameters table +
converted example code block, no leaked inherited members. Sphinx 9.1.0 + deps were
`pip install`ed into `.venv-home`. Live demo: `.venv-home/Scripts/python.exe -m
sphinx_autobuild docs docs/_build/html --open-browser`. **gitignore:** added
`docs/_build/` + `docs/reference/api/generated/` (autosummary output) and a
`!docs/_static/` re-include (the pre-existing broad `*_static` rule would ignore the
committed CSS). **>>> NEXT SESSION:** author will note skeleton changes to make
(iterate content/IA on the same branch or a fast-follow), then proceed down §11:
**sub-PR 2 = reference generators** (`tools/generate_style_reference.py` offline→rST;
retarget `tools/generate_bootstyle_reference.py` md→rST + wire in; sync tests) →
sub-PR 3 User Guide → sub-PR 4 Widgets catalog → sub-PR 5 Landing + screenshots.
Screenshots need bootstack's `docs/screenshots/`+`scripts/` tooling ported (not yet
done). **Env unchanged:** `.venv-home/Scripts/python.exe` launches (repo `.venv`
exits 127). **User WIP still in the working tree — dialog-button styling in
`dialogs/colorchooser.py`, `dialogs/fontdialog.py`, `examples/widgets/dialogs.py` —
LEFT UNTOUCHED (verified unstaged); keep leaving it alone.** Prior entry follows._

_Last updated: 2026-07-10 (**Pre-release review COMPLETE (#1146) + macOS Track B
visual pass (#1147); NEXT = docs Workstream H**). The cumulative pre-release review
(`development/2_0_prerelease_review_plan.md`) ran end-to-end. **#1146** (`53f5b72b`,
branch deleted) bundled: **Track A** (8-subsystem agentic `2.0…master` Workflow +
adversarial verify) — the one release-blocker was **`bootstyle="neutral"` crashing
construction on every non-button family** (`NEUTRAL_FAMILIES` was never enforced at
runtime); fixed with a resolver gate (drop to family default + loud warning).
**Green-suite gate:** the `test_color_helpers` *Duplicate element TSpinbox.uparrow*
"flake" was a **real** bug — `element_create` wasn't idempotent, so a recipe re-run
on an already-materialized ttk theme crashed; fixed with an idempotent
`Style.element_create` override. The `nl.msg`/`test_msgcat` failure is **confirmed
env-only** (transient Tcl file read; flips run-to-run). Other gates pass (clean-env
wheel install smoke, 3.10 parse, warning-free import). **Track C** (public-API diff
`master`→`2.0` vs `2_0_breaking_changes.md`): **no silent breaks, no phantom
entries.** Also in #1146: visual-pass bug fixes (datepicker stale-highlight, toast
overlap, dialog app-icon win32 scoping + Toplevel per-window, Querybox/Messagebox
spacing + icon warn/centering); **two author-sanctioned utilities** (utilities, NOT
widgets — the "no new features" rule is widgets-only): **`ttk`/`Style`/`App` light-
dark `theme_mode` / `toggle_theme_mode` / `use_theme_mode` / `set_theme_modes`** (+
`App(light_theme=, dark_theme=)`), and **`icon_only=True`** on icon widgets (fixed
`size=17`/`padding=3` pair -> square ~normal-button height; explicit overrides win;
dogfooded onto datepicker chevrons / Tableview pagination / DateEntry button);
**version bumped to 2.0.0.** New `examples/prerelease_visual_review.py` (Track B
"everything-bagel" harness). Then **Track B was largely run on macOS**, fixes merged
as **#1147** (`745fb997`, branch deleted): toast off-screen (absolute-positive
geometry) + minsize-floored stack height + `e`/`w` offset + icon centering; `get_date`
centers on its window; DatePicker built-hidden-then-shown (kills the flash) +
aqua-gated `window_type="tooltip"` native popover; `place_window_center` uses the real
mapped size (`_window_size` now keys on `winfo_ismapped()`, reused for parent/target).
Both PRs were gated by a high-effort `/code-review` (caught the `neutral` blocker's
sibling issues, the Toplevel-icon leak, the toast e/w-overlap regression, and the
x11 focus break from the tooltip window type — all fixed pre-merge). **Known-accepted:**
the DateEntry calendar clamps at the app bar instead of flipping on a short screen
(author OK). Suite **567 passed** excl. the two known flakes. **>>> NEXT: docs
Workstream H — a from-scratch rebuild on a NEW toolchain** (design LOCKED at the top
of `development/2_0_docs_design.md` §1, 2026-07-10). Move **off mkdocs onto
bootstack's stack** (sibling repo `D:/Development/bootstack`): **Sphinx +
`pydata_sphinx_theme` + `autodoc`/`napoleon` + `sphinx_design`**, authored in
**rST** (bootstack is 319 rst / 19 md). Lift bootstack's `conf.py` + `_static/` CSS
+ `_templates/` + `docs/screenshots/` + `docs/scripts/` tooling + page templates
wholesale; borrow the *infra & IA*, author ttkbootstrap content, keep the
styling-extension positioning (not a widget library). ttkbootstrap's `Parameters:`/
`Examples:` docstrings feed `autodoc` as-is (napoleon Google) — **no docstring
rewrite**. **Clean cut:** delete the whole mkdocs `docs/` tree (incl. `ja`/`zh`,
~134 files + the `i18n` plugin) — the 9 broken `:::` API stubs resolve by
*replacement*, not repointing. Style-Reference + BootStyle generators stay
**offline `tools/` steps emitting committed rST** (RTD build has no display; the
Style Reference needs a live Tk root). **First task: a Sphinx-skeleton spike** —
lift bootstack's `conf.py` + one widget page to prove the structure — then the §11
sub-PR sequence (skeleton → generators → user guide → catalog → landing/screenshots).
Optional remaining Track B: Linux/x11 + the DPI matrix.
**Env:** `.venv-home/Scripts/python.exe` launches (repo `.venv` exits 127); run
pytest `-p no:cacheprovider`. **User keeps live WIP in the working tree — dialog-
button styling in `dialogs/colorchooser.py`, `dialogs/fontdialog.py`,
`examples/widgets/dialogs.py` — LEAVE IT UNTOUCHED (do not stage/commit it).** Prior
entry follows._

_Last updated: 2026-07-09 (**Compat & utilities — Slice 4 (typography) MERGED into
`2.0` (#1145); the initiative's code work is now COMPLETE**). **Slice 4**
adds `ttkbootstrap/utils/fonts.py` — a tiny surface over the standard Tk named
fonts: module-level **`ttk.set_global_family(family, *, mono_family=None)`** (rides
the Slice 5 deferred-config seam — queued before `App()`, live if a root exists),
plus a **`ttk.Fonts`** namespace of live-root classmethods (`set_global_family` /
`configure` / `describe` / `names` / `create_alias` / `reset`); `Fonts.reset()` is
wired into `App.destroy` (root-rebind hazard). No new font vocabulary / no bracket
DSL (boundary rule); the optional macOS size-bump + platform default families were
dropped as scope creep. Re-exported top level + through `utils`. Mirrors the Slice
3/5 shape. `tests/test_fonts_api.py` (+10); suite **539 passed** excl. the two known
flakes (`nl.msg` env + order-dependent `test_color_helpers` *Duplicate element*);
warning-free import. **MERGED as #1145.** With 5→3→4
done, **all compat & utilities slices are complete.** A high-effort `/code-review`
of the diff caught + fixed one footgun before merge: the live `Fonts.*` classmethods
went through `get_default_root()` with no `what`, so a pre-root call would silently
spawn a phantom `tkinter.Tk()` (misbinding the real `App()`'s interpreter); now they
pass `what=` to raise a clear "too early" error, and the module-level
`set_global_family` remains the pre-root path. **>>> NEXT (author decision):
the cumulative pre-release review** per `development/2_0_prerelease_review_plan.md`
(Track A agentic `2.0…master` sweep · Track B human visual/cross-platform · Track C
migration-contract validation), then docs Workstream H. Env: `.venv-home/Scripts/
python.exe` launches on this box (repo `.venv` exits 127); run pytest with
`-p no:cacheprovider`. Leave the user's `gallery/text_reader.py` WIP untouched (not
staged). Prior entry follows._

_Last updated: 2026-07-09 (**Compat & utilities — Slices 0/1/2 MERGED into `2.0`;
pre-release review plan written**). Working through the compat & utilities
initiative (`development/2_0_compat_and_utilities_design.md`, the last substantive
code work before release). **Merged this session:** **#1139** Slice 1 (theme compat
— `theme_use` on a legacy (pre-2.0) name no longer hard-stops; it lazily
adapts+registers that one theme via `theme_from_legacy_dict`→`register_theme`,
warns once per name, and builds it — so `Window(themename="darkly")` works again;
`install_legacy_themes()` stays the bulk register); **#1140** Slice 2 (naming —
`App` is now the canonical root class, `Window = App` a permanent non-deprecated
alias; `theme` canonical on `App`/`Window`/`Style` ctors with `themename` a
permanent alias; `theme_use`/`theme_create` keep Tk's `themename`; full source
docstring/example/error-message sweep to the canonical names per author request);
**#1141** Slice 0 (utilities — new first-class `ttkbootstrap.utils` package:
`color.py`←colorutils, `scaling.py`+`platform.py`←utility; old `utility`/`colorutils`
modules become warn-and-forward shims like `publisher.py`; all first-party callers
migrated so import stays warning-free; a high-effort `/code-review` caught one
low-sev gap — `utils` didn't re-export the color-model constants — fixed in the
same PR). Expected suite on `2.0` ~**505 passed** excl. the two known flakes
(`nl.msg` localization env flake + the order-dependent `test_color_helpers`
*Duplicate element TSpinbox.uparrow*, which is a real theme-rebuild bug, not
noise). Every slice: branch from `2.0` → PR → author merge (one in flight), entry
in `2_0_breaking_changes.md`, migration-guide touch-ups.

**>>> NEXT-SESSION PICKUP:** finish the remaining compat & utilities slices in the
design's order — **Slice 5** (deferred-config pending-apply seam; enables 3 & 4) →
**Slice 3** (localization: msgcat `tk.call` fixes + `L()`/`LocaleVar` +
`<<LocaleChanged>>`) → **Slice 4** (typography: a `Fonts` utility over the standard
Tk named fonts). Slices 3/4/5 are **born into `utils/`**. **THEN**, as the capstone
before an RC, run the cumulative pre-release review per the new
**`development/2_0_prerelease_review_plan.md`** (Track A agentic `2.0…master` sweep
· Track B human visual/cross-platform · Track C migration-contract validation +
green-suite / install-smoke gates). Decision (author, 2026-07-09): **continue the
initiative, run the full review at the end**, not now.

**Env note (unchanged):** repo `.venv` fails to launch on this box (exit 127); use
`.venv-home/Scripts/python.exe` for python/pytest (run with `-p no:cacheprovider`).
Leave the user's `gallery/` WIP untouched.

Prior entry (2026-07-08) follows._

_Last updated: 2026-07-08 (**Remaining shipped-widget API review — COMPLETE; the
whole widget-review series (PRs 0–7) is MERGED into `2.0`**). The all-widgets API
review (design + all forks in `development/2_0_widget_api_review_design.md`) is
DONE. **Merged this session:** **#1111** PR 3 (DateEntry — live-text `get_date()`/
`value` via a tolerant `_coerce_date`, cross-layer `date_format`/`first_weekday`/
`start_date` rename incl. `Querybox.get_date`/`DatePickerDialog`, mixin +
single-string `state`, `<FocusOut>` blur→invalid, `width` double-apply fix,
keyword-only ctor, picker re-entrancy guard, `position=`), **#1112** PR 4
(Floodgauge — mixin 5-tuples + `cget` parity, `IntVar`→`DoubleVar`, live `mode`/
`orient`, `maximum=0` guard, value-vs-display split fixing `cget("text")`,
`start()`→`start(interval)` w/ `_compat` shim, `value` property; FloodgaugeLegacy
trace-leak `destroy()`), **#1113** PR 5 (Scrolled — ScrolledFrame **deep
Canvas-viewport rewrite** fixing the container leak via a re-entrancy-safe
`_ScrollContainer` + class-tag mousewheel seam + tuple `yview`; ScrolledText onto the
mixin w/ inner-`Text` target; `auto_hide`/`scroll_height` renames), **#1114** PR 6
(LabeledScale — `compound`/double-init crash fix, `IntVar`→`DoubleVar` w/ `:g`
label, `after_idle` use-after-destroy fix; ToolTip — `add="+"` binds + funcids,
idempotent `destroy()`, `<Destroy>` self-release, `ensure_on_screen` placement,
`configure`/`cget`), **#1115** PR 7 (ToastNotification — self-deprecation fix,
font-glyph icon via `apply_icon` (PUA/`iconfont` gone), timer+fade leak fix,
off-screen mismeasure fix, dismiss handle + idempotent `hide()`, **`_ToastStack`
concurrent-toast stack manager** w/ reflow-on-dismiss). **Expected suite on `2.0`
now 460 passed** excl. the known `nl.msg`/`zh_cn.msg` localization flake (and a
pre-existing order-dependent multi-monitor `test_center_on_screen` — see below).
Every widget now: `ConfigureDelegationMixin` (where applicable), keyword-only ctor,
`_compat` warn-and-normalize renames, lifecycle/leak fixes, and a per-widget entry
in `development/2_0_breaking_changes.md` (split breaking vs deprecated vs fixed).

**>>> NEXT-SESSION PICKUP → pick a thread (author's call):**
1. **Docs Workstream H sub-PR #1** — nav/IA skeleton + un-break the 7 broken API
   `:::` stubs, per `development/2_0_docs_design.md` §11. The stated primary next
   initiative in CLAUDE.md.
2. **Cross-widget property/accessor consistency pass** (memory
   `property-accessor-consistency-pass`) — now unblocked (series done): confirm every
   normalized widget follows the one rule (options via `configure`/`cget` only; only
   `value` + genuinely-computed-state as properties; no bare option attributes).
3. **Pre-release breaking-vs-deprecated audit** (memory
   `prerelease-breaking-deprecation-audit`) — the log started late, so sweep the whole
   2.0 diff vs `master` → the Migrating-to-2.0 guide (folds into docs H).
4. **Deferred Tableview method-verb rename** — the one remaining widget slice (own mini
   design pass).

**Working method that's been effective (KEEP):** cut the branch, dispatch a **fork**
(inherits full context) to implement per the design §8x spec, then **review the diff
+ independently spot-check + run the suite yourself** before committing. Commit →
push → `gh pr create --base 2.0` → **hold for the author to merge (one PR in
flight)** before the next. Require the fork to (a) update `2_0_breaking_changes.md`
and (b) leave user WIP untouched, as explicit deliverables.

**ENV CORRECTION (important):** on this box (Logistiview login), the repo **`.venv`
WORKS** (`.venv/Scripts/python.exe`, run pytest with `-p no:cacheprovider` — the
`.pytest_cache` dir throws Access-denied harmlessly). **`.venv-home` is NOW
access-denied** (it belongs to the `Israel Dryer` account) — the opposite of the
earlier handoff note. **Uncommitted WIP in the working tree (leave untouched, do NOT
commit):** the user's builder edits `src/ttkbootstrap/style/builders_tk.py`,
`style/builders/treeview.py`, `examples/widgets/tableview_yscrollbar.py`, plus the
long-standing `examples/widgets/tableview.py`. **Known non-blocking test failures:**
`nl.msg`/`zh_cn.msg` localization flake; and `test_window_api.py::
test_center_on_screen_is_within_bounds` — a real latent `center_on_screen`
negative-origin multi-monitor bug (memory `center-on-screen-negative-origin-bug`),
order-dependent, fix parked for the deferred PR B positioning fast-follow. Prior
entry (PRs 0/1/1.5/2) follows._

_Prior 2026-07-07 (**Remaining shipped-widget API review — DESIGN PASS**). After the pagination merge (#1106) the author
directed that **all remaining shipped widgets get a 2.0 API review** (the first
shipped-widget pass covered only Window/dialogs/Tableview). Verified first via three
audit agents that PRs A/B/C are genuinely complete in code (all §5a/5b/5c items
DONE; 19+15+tests pass) — the audit surfaced a live regression: **ToolTip fires 2
`DeprecationWarning`s/hover and Toast 1/show** because they still inject legacy
`overrideredirect`/`windowtype` into `Toplevel` (PR B migrated `dialogs/base.py`
but missed these callers), plus a pre-existing `Tableview.delete_column` `int(None)`
branch bug. Then ran **seven ground-truth surveys** (one per widget) + **six
bootstack mechanism-mining comparisons**; full design in
**`development/2_0_widget_api_review_design.md`**. Scope = Meter, Floodgauge
(+Legacy), DateEntry, LabeledScale, ScrolledText/Frame, ToolTip, Toast.
**Flagship borrow:** bootstack's `ConfigureDelegationMixin`/`@configure_delegate`
(the #1 pick for Meter+Floodgauge+Scrolled) → adopt as a shared private
`internal/` mixin that gives `cget` + get/set symmetry + reconfigurable options +
proper 5-tuples and deletes the buggy hand-maintained configure ladders (caveat:
inner-widget pass-through is ours to add). **ALL forks now locked (author):** value backing → `DoubleVar`; constructors →
keyword-only; adopt bootstack's `ConfigureDelegationMixin` as a shared `internal/`
backbone; **ScrolledFrame → deep outer-frame + Canvas-`create_window` rewrite**;
**include the toast STACK manager** (cancellable fade kept); **Floodgauge `start()`
→ realign to ttk `start(interval)`** + `_compat` shim; **unify `position`/value-access
where feasible** (§9: a `value` property everywhere + a shared popup anchor grammar;
`Window` stays absolute `(x,y)`). These deliberately go beyond "consolidation only"
for 2.0 quality. **8-PR plan** (design §5): **PR 0 self-deprecation hotfix — MERGED
#1107** (ToolTip/Toast internal `override_redirect`/`window_type`; +2 tests; suite
341) → PR 1 re-exports (`ttk.ToolTip`/`ToastNotification`/`ScrolledText`/
`ScrolledFrame` don't exist today; Scrolled isn't even in `widgets/__all__`) → **PR
1.5 the shared `internal/configure_delegation.py` mixin** (backbone; add the
inner-widget-fallthrough bootstack lacks) → PR 2 Meter → PR 3 DateEntry (coordinated
with the dialog layer's `start_date`/`first_weekday`) → PR 4 Floodgauge → PR 5
Scrolled (deep Canvas rewrite) → PR 6 LabeledScale + ToolTip lifecycle → PR 7 Toast +
stack. Borrowed-mechanism details per widget in design §8. **NEXT → merge #1107,
then PR 1 (re-exports).** (Author cadence: one PR in flight; wait for merge before the
next.) Prior entry (pagination #1106) follows._

_Prior 2026-07-07 (**Tableview pagination buttons on the icon path — MERGED
into `2.0` (#1106)**). Swaps the five character-symbol pagination controls
(`⎌ » › ‹ «`, all `symbol.Link.TButton`) for Bootstrap Icons glyphs on a **ghost**
base via the `icon=` sugar (first→`chevron-bar-left`, prev→`chevron-left`,
next→`chevron-right`, last→`chevron-bar-right`, reset→`arrow-counterclockwise`; the
searchable-frame reset button too). Scope **(b)** (author pick): the four nav
buttons now **disable at the page boundaries** (first/prev on page one, next/last on
the last page), driven from a new `_update_pagination_state` called by
`load_table_data` (the single page index/limit funnel) — the ghost disabled
-foreground mutes the glyph, so the boundary reads (previously a boundary click was a
silent no-op with no affordance). **Bar layout fixes (surfaced live):** the bar was
pinned ~40px because a bare vertical `ttk.Separator` requests the style's baked ~40px
length (the old 16pt-font symbol buttons matched it) — each divider is now bounded in
a fixed, DPI-scaled height frame (`_add_page_separator`) so the shorter controls
(buttons 30px, entry 29px) set the height; reset gains `fill=Y` for uniform buttons;
`padding=5` on the page frame (matching the search frame) keeps controls off the
edges. No public method signature changed (`goto_*_page` unchanged, still safe at a
boundary). `tests/test_tableview_api.py` (+4: ghost base, both boundaries, middle);
suite **340 passed** (the `nl.msg`/`zh_cn.msg` localization flake did not surface
this run); warning-free import. Breaking/behavior log updated. **A light↔dark visual
eyeball of the bar (glyphs + disabled muting) is still worth it before docs
screenshots.** Still-open icon follow-ups (both before docs screenshots): Sizegrip →
recolor raster asset; theme-wide **control-height parity** (buttons == inputs, memory
`control-height-parity`). **NEXT → docs Workstream H sub-PR #1** (nav/IA skeleton +
un-break the 7 broken API `:::` stubs, `development/2_0_docs_design.md` §11). Prior
entry (#1105) follows._

_Prior 2026-07-07 (**Theme-aware widget icons — MERGED into `2.0`
(#1105)**). Closes the inline-icon theme-awareness gap (a bare `Icon(...)` `image=`
baked its color once and went stale on a theme switch). New `ttk.apply_icon` +
`icon=`/`icon_size=` mixin sugar: renders a glyph following the widget's style
`foreground` (inverts on outline/toggle, mutes disabled), re-renders on
`<<ThemeChanged>>` (per-widget bind, no engine change), by augmenting the widget
with a derived content-hashed `Icon<hash>.<base>` style that inherits its
`bootstyle`/`style` (config/map/layout via ttk fallback). Supported on label-image
widgets (Button/Label/Menubutton/Check/Radio); others raise. Datepicker carets
migrated as dogfood. **Render tuning from the live gate:** glyph pad 10%→4% + snap
draw origin (sharpens all font-glyph icons — the 10% pad was rendering glyphs at
~80% of frame), default `icon_size`→14, `calendar3` trimmed 21→18/19 + date-button
+1px vertical pad. Raster indicators (check/radio/toggle/scale/scrollbar) unaffected.
`tests/test_icon_theme.py` (+12); suite **330 passed** excl. the `nl.msg` flake;
warning-free import. Design `development/2_0_icon_theme_awareness_design.md`.
**Follow-ups logged (not blockers):** move the Sizegrip onto a **recolor raster
asset** (retires its `grip-horizontal` font glyph — the conversion is the fix, no
glyph-size trim needed); theme-wide **control-height parity** (buttons == inputs,
memory `control-height-parity`) before docs screenshots. Also recorded the 2.0 naming
convention (snake_case authored / Tk-spelling pass-throughs; `CLAUDE.md` +
memory). **NEXT → Tableview pagination buttons on the icon path** (ghost base +
glyph; disabled first/prev arrows get muting for free), then docs Workstream H.

**The pagination pickup was COMPLETED as #1106 (scope (b) — see the top entry).**
Prior entry (PR C) follows._

_Prior 2026-07-07 (**shipped-widget API pass — PR C (Tableview)
OPENED as #1104 against `2.0`; the pass's LAST PR**). Fixes only per design §5c
(the method-verb rename stays a deferred later slice). Re-export
`Tableview`/`TableColumn`/`TableRow` at top level (`ttk.Tableview`) + from
`ttkbootstrap.widgets` (was the only widget not reachable as `ttk.<Name>`); fix
two dead-on-call bugs — `delete_column(cid=...)` called the `cidmap` dict
(`self.cidmap(int(cid))`→`self.cidmap.get(int(cid))`; ground truth: `cidmap` is
keyed by **int**, not the `str` the design sketch assumed) and the header
right-click menu's `self.master = self.master` now sets `master` from the arg;
`insert_row(values=[])` raises `ValueError` instead of `print()`ing to stdout +
returning `None` (surfaces in the `insert_rows`/`rowdata` batch paths too); delete
dead code (`reset_row_sort` stub, unused `_build_table_rows`/`_build_table_columns`,
commented `_select_pagesize`, never-implemented `maxwidth` docstring). New
`tests/test_tableview_api.py` (+6); suite **323 passed** excl. the known `nl.msg`
flake; warning-free import. No visual/cross-platform gate (bugs + dead-code +
re-exports only). Breaking/behavior log updated. **With A/B/C done the
shipped-widget API pass is COMPLETE**; the only remaining Tableview item is the
deferred method-verb rename slice (own mini design pass, after the H docs). **NEXT →
docs Workstream H sub-PR #1** (nav/IA skeleton + un-break the 7 broken API `:::`
stubs, `development/2_0_docs_design.md` §11). Prior entry (PR B) follows._

_Prior 2026-07-07 (**shipped-widget API pass — PR B (Window/Toplevel)
MERGED into `2.0` (#1103)**; expected suite **317 passed** excl. the `nl.msg`
flake. A cross-platform visual gate (win32 AppUserModelID / aqua guard /
multi-monitor centering) is still worth an eyeball but did not block merge. Per design §5a: new private `_BaseWindow` mixin
(`Window(_BaseWindow, tk.Tk)` / `Toplevel(_BaseWindow, tk.Toplevel)`) owning the
shared icon/geometry/alpha/positioning/`style` logic both classes were
duplicating and drifting on; `_setup_icon` unifies `iconphoto` (`None`=skip,
`''`=default/inherit, path=load-with-fallback — fixes the `Toplevel(iconphoto=None)`
crash, bad path now `UserWarning` not `print`, `.ico`→`wm_iconbitmap` on win32);
new private `internal/positioning.py` (subset of bootstack's `WindowPositioning`:
`center_on_screen`/`center_on_parent`/`ensure_on_screen`, optional `screeninfo`
with graceful single-screen fallback — no new hard dep) re-points
`place_window_center`; snake_case kwarg aliases via
`_compat.normalize_window_kwargs` (`hdpi`→`high_dpi`,
`overrideredirect`→`override_redirect`, `windowtype`→`window_type`,
`toolwindow`→`tool_window`, warn-and-normalize, removed 3.0); **keyword-only**
constructors after the leading positional(s) (`Window(title, themename, *, …)`,
`Toplevel(title, *, …)` — documented breaking, unshimmable); `iconify` promoted to
a real `Toplevel` kwarg; edge-relative + combined geometry (`f"{x:+d}{y:+d}"`);
aqua `overrideredirect` no-op guard; win32 AppUserModelID. First-party
`dialogs/base.py` migrated `windowtype`→`window_type`. New
`tests/test_window_api.py` (+15); suite **317 passed** excl. the known `nl.msg`
flake; warning-free import + end-to-end smoke verified. Breaking-change log +
design §8 updated. **Residual risk = cross-platform** (a manual win32 + if-available
x11/aqua check is still owed before merge). **Deferred fast-follow (NOT in PR B):**
the richer bootstack positioning surface (`place_center_on`/`place_at`/
`place_anchor`/`place_dropdown`/`place_cursor`), the `windowtype` unified switch
(§5a.9), and routing the dialogs' `internal/utility.center_on_parent` through the
new `positioning` module. **NEXT → PR C (Tableview fixes + re-export, §5c)** once PR
B lands. Prior entry (PR A) follows._

_Prior 2026-07-07 (**shipped-widget API pass: design done + PR A
(dialogs) MERGED into `2.0` (#1102)**). The deferred shipped-widget API
normalization (`Window`/dialogs/`Tableview`) was picked up ahead of the docs
(author reversed the docs-first call so docs get written against normalized
signatures). Design pass **confirmed**:
`development/2_0_shipped_widget_api_design.md` (Hybrid posture · port bootstack
window mechanisms · unify dialog returns + `get_date`→None-on-cancel · Tableview
fix+re-export now, defer verb rename). **PR A (dialogs) MERGED (#1102):** Messagebox
uniform keyword-only signatures; Querybox `get_*` return via `.result`;
`get_date` returns None on cancel + gained `position=`; DatePickerDialog
`autoshow=False`/`show()`/`result`; `MessageDialog.command` plain-callable (tuple
deprecated via `_compat`); `ColorChoice` deduped; dialogs re-exported at top
level. `tests/test_dialogs_api.py` (+19); suite on `2.0` **297 passed** excl. the
known `nl.msg` flake; modal cancel + happy paths were verified end-to-end. A human
visual spot-check of `examples/widgets/dialogs.py` (light↔dark) is still worth an
eyeball before docs screenshots. **NEXT → PR B (Window/Toplevel — the
cross-platform bootstack `_BaseWindow`/`WindowPositioning` port, design §5a), then
PR C (Tableview, §5c), per §8.** (Docs sub-PR #1 still trails the API pass.)_

_Prior 2026-07-07 (**icon-drop PREREQ + a visual-polish batch are all
MERGED into `2.0`; NEXT → docs sub-PR #1**). Merged since the prior entry:
**#1094** (icon-drop prereq — `ttkbootstrap.icons` removed, brand logo preserved
as `window.py` `_DEFAULT_ICON_DATA`, the 4 Messagebox icons render from the
font-glyph engine, `media_player` emoji inlined; `tests/test_icon_drop.py`), then
an unplanned **visual-polish batch** driven by live light↔dark review — all with
what/why entries in **`development/2_0_breaking_changes.md`**:
- **#1096** — new `neutral` bootstyle color (theme-adaptive, no-accent, derived
  from the surface via `neutral_fill`/bootstack's `elevate`) + flat **1px hairline
  border** restyle across the button family (clam "border ⟺ bevel" worked around by
  tracking `darkcolor`/`lightcolor` to the fill; `borderwidth=1` unscaled). New
  `NEUTRAL` const + `NEUTRAL_FAMILIES` gate in `constants.py`;
  `development/2_0_neutral_color_design.md`.
- **#1097** — button-family follow-ups: date-button hairline border; fixed the bare
  `bootstyle="toggle"` crash; toolbutton on/off + switch-off recolored to
  bootstack's model; toolbuttons made pure on/off toggles.
- **#1098** — **bare buttons/menubuttons now default to `neutral`** (breaking;
  opt out with `Style(default_button="primary")` / `Window(default_button=…)`, read
  at base-style build via `default_button_fill`). Demos adopt it.
  `development/2_0_neutral_default_design.md`.
- **#1099** — `ghost` button variant (transparent at rest, subtle hover wash) + new
  `GHOST` const/modifier; a `thin` scrollbar variant (used in the combobox popdown +
  font-dialog lists); a full **scrollbar restyle** (visible trough, ~1px inset thumb,
  minimum thumb length, square `default` vs `round` pill, arrowless); datepicker
  fixes (selected-day look, dark-mode chevron arrow color via `on_color(accent)`,
  smaller title, tighter cells); font-dialog scrollbar layout (bordered box +
  borderless `Flat.Treeview`).
- **#1100** — input-indicator refinements: menubutton caret moved inside
  `Menubutton.padding` with asymmetric `(10,5,6,5)` padding (clam ignores outer
  image-element `-padding`); combobox uses a `chevron-down` glyph laid out like the
  menubutton indicator; spinbox/combobox arrows render **one fixed color in every
  state** (no focus/hover/press/disabled recolor); spinbox right-edge gap is a real
  transparent spacer element; **striped progressbar gets its own flat clam trough**
  (it was falling back to the solid bar's rounded image trough via ttk dotted-name
  resolution).

Expected suite on `2.0`: **~283 passed** + the known `nl.msg` env flake. The two
merged local branches (`feat/2.0-followups`, `feat/2.0-input-indicators`) are
deleted. **NEXT → docs sub-PR #1** (nav/IA skeleton + un-break the 7 broken API
`:::` stubs + `inherited_members: false`); sub-PR sequence in
`development/2_0_docs_design.md` §11. The deferred **shipped-widget API
normalization** (`Window`/dialogs/`Tableview`) still trails the docs.)_

_Prior 2026-07-06 (**icon-drop PREREQ IMPLEMENTED** — the character-based
icons are removed on branch `feat/2.0-drop-char-icons` (cut from `2.0`), per the
mini design pass `development/2_0_icon_drop_design.md`. `src/ttkbootstrap/icons.py`
deleted (the `Emoji`/`EmojiItem` catalog + base64 `Icon` constants). **Design-pass
finding the docs-design §2 enumeration missed:** `Icon` carried a **fifth**
attribute — `Icon.icon`, the ttkbootstrap **brand logo** used as the default
`Window(iconphoto='')` icon in `window.py` — which is not an alert glyph and can't
become a Bootstrap glyph; deleting the whole module blind would regress every
Window to the bare Tk feather. Preserved as a private `_DEFAULT_ICON_DATA`
constant in `window.py`. The four `Messagebox.show_*` alert icons now render from
the font glyph engine (`info-circle-fill`/`info`, `exclamation-triangle-fill`/
`warning`, `x-circle-fill`/`danger`, `question-circle-fill`/`info`; size 30 —
`question` color=`info` is a settle-on-spot-check pick). `MessageDialog.create_body`
gained a third icon input form (a pre-rendered Tk image name, tried before the
existing base64-data → file-path cascade) so user-supplied base64/file icons still
work. `gallery/media_player.py` inlines the 6 literal emoji chars it used to look
up via `Emoji`. New `tests/test_icon_drop.py` (7 tests). Suite **269 passed** + the
known `nl.msg` env flake; warning-free import; media_player compiles. **PR #1094
open against `2.0`** (branch `feat/2.0-drop-char-icons`; commits: H-design docs +
icon-drop + a stray `gallery/calculator.py` `flatly`→`bootstrap-dark` theme fix).
Still needs the **live visual spot-check** of the four dialog glyphs + the
media-player transport controls (light↔dark) before merge/docs screenshots — the headless suite asserts the
image is wired, not that it looks right. The frozen `docs/zh/gallery/mediaplayer.md`
still shows the old `Emoji` import (zh untouched for 2.0; Gallery being dropped) —
noted for the docs sweep. **NEXT after this merges → docs sub-PR #1.**)_

_Prior 2026-07-06 (**Workstream H (docs) DESIGN PASS COMPLETE** — the
hard-rule design/scoping gate is done; full design in
`development/2_0_docs_design.md`; vision captured in memory
`project-2-0-docs-vision`). Locked with the author over a live vision session.
Headlines: bootstack-modeled Diátaxis IA collapsed to **4 destinations** (Landing
marketing hero → User Guide → Widgets catalog → Reference); the **native-vs-shipped
widget dichotomy** carried by *grouping* in the catalog (catalog = common front
door; a widget's depth lands in **Style Reference** (native, e.g. Button) or **API
Reference** (shipped, e.g. Floodgauge) — they're mirror-images); **Style Reference
is generated** from ttk introspection (like the `BootStyle` generator — biggest new
value-add); API Reference covers only authored surfaces with `inherited_members:
false`, native widgets link out to python.org's `tkinter.ttk`; Themes folded into
User Guide as a Theming guide with a **2-column light/dark gallery**; Cookbook →
How-To; Gallery removed for now; English only; **flagship = the bootstyle grammar**
(make-your-own-style/theme = second act). Both staged sources
(`2_0_bootstyle_reference.md`, `2_0_theme_migration.md`) fold in. Full staleness
inventory (from the 2026-07-06 audit) is in the design doc §8: 7 API `:::` stubs
point at removed module paths (mkdocstrings breaks), the tutorial + several gallery
pages have crashing legacy-theme/tuple examples, theme pages document the retired
16-key dict model.

**Two follow-on code items surfaced by the design pass (NOT part of H):**
- **PREREQ (next session) — drop the character-based icons.** Remove
  `ttkbootstrap.icons` (the `Emoji`/`EmojiItem` catalog + `Icon.info/.warning/
  .error/.question` constants — a poor-man's, OS-font-dependent solution). **Keep**
  the Bootstrap-Icons font-glyph engine (`style/icons.py`; date/caret/sizegrip are
  unchanged). Rewire Messagebox's 4 default icons (`dialogs/message.py:213/239/265/
  291`) onto font glyphs (`info-circle-fill`/`exclamation-triangle-fill`/
  `x-circle-fill`/`question-circle-fill`) — strict upgrade + dogfoods the engine +
  kills the `Icon` name collision. Documented breaking change (→ Migrating-to-2.0).
  Must land **before** docs screenshots (changes dialog-icon appearance). Own mini
  design pass per the hard rule. Design-doc §2.
- **DEFERRED — shipped-widget API normalization pass.** `Window`, dialogs,
  `Tableview`/datagrid, etc. have NOT had a 2.0 API cleanup. Docs-first is
  accepted (author, 2026-07-06); autogen API Reference regenerates for free, so
  keep the *hand-written* catalog/How-To examples for those widgets conservative to
  limit churn. Its own future workstream, after docs. Design-doc §11a.

**NEXT → the icon-drop PREREQ PR** (mini design pass → implement), then docs
sub-PR #1 (nav/IA skeleton + un-break the 7 API stubs + `inherited_members:
false`); sub-PR sequence in design-doc §11. Env note: the repo `.venv/` is broken
on this Windows box (launcher fails); use `.venv-home/` (pytest is installed
there). One known non-blocking test flake: `nl.msg` localization (Tcl can't read
the Dutch catalog; passes in isolation). _

_Prior 2026-07-06 (**Workstream D (canonical bootstyle grammar)
COMPLETE** — all three PRs merged into `2.0`; design in
`development/2_0_bootstyle_grammar_design.md`). **D1 #1091**: closed-vocab
tokenizer replacing the substring regex, loud failure on unknown tokens (warn by
default; `set_bootstyle_strict(True)` / `TTKBOOTSTRAP_STRICT=1` raises); single
vocab source of truth in `constants.py`; new `style/_compat.py` quarantine
(Workstream F's first tenant). **D2 #1092**: migrated every first-party tuple
caller (meter/dateentry/tooltip/datepicker + the `python -m ttkbootstrap` and
ttkcreator demos) to canonical strings, then turned the tuple `DeprecationWarning`
on (warn-and-normalize through 2.x, removed 3.0). **D3 #1093**:
`tools/generate_bootstyle_reference.py` derives the 107 canonical strings from
vocab × registry → generated `BootStyle` `Literal` in `constants.py`
(`apply_bootstyle` types `BootStyle | str`) + `development/2_0_bootstyle_reference.md`;
sync tests fail if a builder is added without regenerating. `BootType` fixed
(`round` added; `toggle`/`toolbutton` → new `BootBase`); dead `focus`/`input`
dropped. Merged-`2.0` suite ~263 (excl. the known `nl.msg` localization env
flake). Two design-pass gaps found during D1 and documented in the design doc's
"D1 — IMPLEMENTED" note: the resolver handles **two input dialects** (bootstyle
strings — loud — vs already-built dotted ttk style names from the theme walk /
`Style.configure` / custom styles — lenient), and invalid pairs now fall back to
the family default instead of returning an unusable fragment. _

_Prior 2026-07-06 (**Workstream E (theme/anchor) COMPLETE** — all three
PRs merged: E1 #1088 (`Colors`→`RampColor` resolved view + `c.primary[300]`),
E2 #1089 (semantic-anchor `Theme` model + curated 15-family/30-theme catalog +
`install_legacy_themes()` + 16-key adapter + hue-correct `inputbg`; default
`bootstrap-light`; visual gate passed with 7 fixes), E3 #1090 (ttkcreator
`Theme` editor + `USER_THEME_SPECS` + migration guide). Non-localization suite
**211 passed**. Design: `development/2_0_theme_anchor_design.md`. Locked forks:
default `bootstrap-light`, legacy-names helpful-error, `selectbg`=neutral,
readonly fields=`inputbg`. **Migration guide `development/2_0_theme_migration.md`
— FOLD INTO the Workstream-H docs rewrite** (kept in `development/` so it
survives the docs transition). **NEXT SESSION → Workstream D (canonical
bootstyle grammar): start from the prep doc `development/2_0_bootstyle_grammar_notes.md`
(ground truth + the 6 open forks), run the DESIGN PASS FIRST (hard rule) → write
`development/2_0_bootstyle_grammar_design.md` → PR-by-PR.** Headlines from the
prep: the resolver is a regex substring-search that silently drops unknown
tokens (no closed vocab); the vocab is split across two out-of-sync sources
(`Keywords` in bootstyle.py vs `BootColor`/`BootType` in constants.py — `round`
missing from BootType, `toggle`/`toolbutton` mis-typed, `focus`/`input` dead);
no `_compat.py` yet; internal tuple callers to migrate = meter/dateentry/tooltip/
datepicker; the loud-fail seam is `statespec`/`state_map` in layout.py. Also
ongoing: Workstream H (docs). Prior: color-math #1087 (`0218aba3`),
color-helper #1085 (`b7872a98`).)_

_Prior (2026-07-01): focused Workstream E private ramps and builder color
helpers implemented on `refactor/2.0-color-helpers`; `on_color` retuned to a
white-preferred, saturation-aware policy after visual feedback. pytest installed
and the suite ACTUALLY RUN — 188 passed / 1 known Tcl `nl.msg` env failure; two
stale `test_color_helpers` assertions corrected. Six-theme human visual gate
PASSED._

## Where we are

Integration branch: **`2.0`** (cut all 2.0 PRs against it, not `master`).
Expected suite on `2.0`: **191 passed** (the color-math PR #1087 is now merged;
merge commit `0218aba3`; +2 tests over the 189 at #1085), headless,
order-independent. A Tcl install that cannot read `tk8.6/msgs/nl.msg` shows one
localization env failure; excluding localization otherwise stays green.

The engine keystone (Workstream A) is **complete and merged**: PR 1 (repaint,
#1073) + PR 2 (content-addressed image cache, #1074). **PR 3 — the mixin API
(Workstream C)** is **merged** (#1075). **PR 4 — the `style/` package split
(Workstream G)** is **merged** (#1076; pure move, see "PR 4" below). **PR 5 —
the style-construction toolkit (Workstream I, Tier 1)** is **merged** (#1077; see
"PR 5" below). **PR 6a — the icon engine (Workstream I, Tier 1.5)** is **merged**
(#1079; see "PR 6a — MERGED" below).

**PR 6b is MERGED (#1080)** — the icon engine is wired into every glyph builder,
the geometric/layout cleanup landed, and the public registration path is in. That
completes the Workstream I icon work for 2.0.

**The recolorable raster-assets PR is MERGED (#1081).** At that merge the
expected suite was 104 tests, and the light↔dark manual gate passed. See the
implementation summary immediately below.

**PR #1082 is MERGED.** `2.0` now includes the 161-line coordinator, frozen
registry, and 22 widget-family modules. Merge commit: `fa1cede8`.

**PR #1083 is MERGED.** Scaling and asset-geometry normalization landed on
`2.0` as merge commit `c1f9ed73`; its automated and four-scale human gates pass.

**The color-helper PR is MERGED (#1085 → `2.0`, merge commit `b7872a98`,
2026-07-01).** Branch was `refactor/2.0-color-helpers` (cut from `2.0` at
`c1f9ed73`); approved design `development/2_0_color_helpers_design.md`; six-theme
human visual gate (`python examples/color_states_preview.py`) PASSED (user,
2026-07-01); automated gates passed (188/1). The local branch is fully contained
in `2.0` and safe to delete.

**Current actionable → pick the next workstream: canonical bootstyle grammar
(D) or theme/anchor (E).** Each needs its own design pass FIRST (per the hard
rule). E is where the deferred `input_bg` / authored-vs-derived `inputbg`
reconciliation lands, alongside the built-in theme-dict conversion.

## Fast-follow color-math — MERGED (#1087, 2026-07-06)

Merged into `2.0` (merge commit `0218aba3`; was `refactor/2.0-color-math` from
`2.0` at `26dd182f`). Expected suite: **191 passed**. Approved+as-built
design: `development/2_0_color_math_followup_design.md`. Retires the **10 ad-hoc
HSV/alpha sites** the color-helper PR left allowlisted, onto three thin mix-based
`StyleBuilderTTK` helpers: `shade`/`tint` (build on new `_shade`/`_tint` in
`theme.py`) and `mute`. The AST guard now enforces **zero** direct
`Colors.update_hsv`/`make_transparent` in `style/builders/*.py`.

**Two forks were opened with the user and BOTH re-decided against the original
stub after reading ground truth:**
- **No `elevate`.** The stub assumed troughs "always darken regardless of mode";
  ground truth showed they are **already mode-branched** and the HSV runs only in
  the dark `else` branch (light uses `colors.light`/`bg`). A mode-aware `elevate`
  would *lighten* dark troughs — wrong. So troughs migrate to plain `shade`
  (preserve appearance; for gray `selectbg`, `shade` is byte-identical to the old
  HSV). Floodgauge wash + progress stripe → `tint`.
- **`input_bg` DEFERRED to Workstream E** (user, 2026-07-06). Light: `bg ==
  inputbg` already, so it's a no-op there (the field affordance is
  `bordercolor=colors.border`). Dark: authored `inputbg` deltas carry theme hue
  (vapor `#190831`→`#30115e`) that a uniform tint-toward-white would desaturate —
  a regression. A hue-correct derivation needs the semantic model → E.

**Automated gates PASS:** focused **14 passed**; full headless **191 passed**
(189 baseline + 2 new; this Windows box has `nl.msg`, no env failure);
warning-free import; PEP 649 sweep (26 modules / 152 targets) clean; standalone
`style.theme` import; seven migrated recipes shed their unused `Colors` import.
End-to-end smoke: all affected widgets build in darkly + flatly.

**Human visual gate PASSED** (user, 2026-07-06): the six-theme
`examples/color_states_preview.py` sweep (new "Progress, stripe, and floodgauge"
section) was approved with no tuning changes — `_TROUGH_SHADE=0.2`,
`_STRIPE_TINT=0.2`, and the floodgauge `0.7` are settled. **PR #1087 MERGED
into `2.0`** (merge commit `0218aba3`).

**pytest gap closed + two stale tests fixed (2026-07-01).** The prior session's
env had no pytest, so `test_color_helpers` was written but never run. Installing
it surfaced two assertions written against the OLD clam-face pattern
(`bordercolor`/`darkcolor`/`lightcolor` = face, faking flatness under
`relief=RAISED`) that no longer hold: the branch's solid **button** and
**toolbutton** recipes are now genuine flat fills (`relief=FLAT`, no clam border
regions), so `config['bordercolor']` `KeyError`'d. Fix was test-only — the flat
recipes are correct and intended; the assertions now verify `relief=='flat'` +
`'bordercolor' not in config` (button) and no-`bordercolor` + `selected` fills
with the accent (toolbutton). `menubutton`/`calendar` still use the clam-face
pattern and their assertions were left intact. No production recipe changed.

## Private color ramps and builder helpers — IMPLEMENTED, VISUAL GATE PASSED

- Private immutable 50–950 ramps use bootstack's Bootstrap-compatible weights
  and a bounded 256-entry cache; no public palette API was added.
- `StyleBuilderTTK` owns `active`, `pressed`, `border`, `disabled`, and
  `on_color`, porting bootstack's luminance/mode-aware derivation policy.
- Approved ttk recipes now use those helpers according to the color actually
  rendered. Clam `bordercolor`/`darkcolor`/`lightcolor` regions that paint the
  control face continue to track the face color; theme-authored structural
  field borders and readonly fills remain authored. `border()` is available
  for a genuinely distinct derived boundary, not selected by option name.
- Input controls derive disabled foregrounds against `inputbg`; filled controls
  derive them against their disabled face; the date button has a separately
  colored disabled icon. Ten remaining direct HSV/alpha sites are specialized
  trough/stripe/unchecked-indicator effects guarded by an exact AST allowlist.
  Legacy `StyleBuilderTK` remains out of scope.
- Verification after the corrected audit: focused **12 passed**; full Python
  3.12 suite **188 passed / 1 known Tcl `nl.msg` environment failure**;
  excluding localization **183 passed**; warning-free import; Python 3.10
  parsed 91 files; annotation evaluation clean.
- `examples/color_states_preview.py` includes disabled/readonly input controls
  and a disabled date icon, and constructs/switches all six themes
  successfully.

### `on_color` retuned — white-preferred, saturation-aware (2026-07-01)

The design's original bootstack mode-aware `on_color` was replaced (after live
visual feedback that black-on-saturated-accent — e.g. sandstone `info`
#29abe0 — reads poorly) with `_accent_on_color(surface)` in `style/theme.py`:

- White wins whenever it clears the bold-text floor
  (`_ON_COLOR_MIN_CONTRAST = 3.0`); else, for a **vivid non-warm** accent
  (saturation `>= 45`, hue outside the warm 20–100° band, white
  `>= _ON_COLOR_WHITE_FLOOR = 2.3`) white is still chosen, because WCAG
  contrast understates white on saturated colors; else black. Mode-independent.
- Rationale: WCAG relative luminance is not perceptual (under-weights red/blue),
  so raw max-contrast picks black on vivid accents. Saturation separates a vivid
  accent (white) from a light gray (black); the warm band keeps yellow/orange/
  lime (`warning`) on black. Validated across the built-ins: exactly 14 vivid
  cool/red roles flip to white (every `success`, saturated `info`/`primary`,
  coral `danger`); no `warning`, pale, or gray changes. `secondary` grays stay
  black by design.
- Accessibility tradeoff: vivid accents can ship white at ~2.3–3.0:1 (below AA
  4.5). Deliberate appearance choice; strict-AA fix is palette-level (darken the
  accents), deferred to Workstream E. Three constants are the tuning knobs.
- Interim `on_color` iterations (raw max-contrast, plain white-preferred@3.0)
  were superseded; the design doc's `on_color` section is current. Test
  `test_on_color_is_safe_and_independent_of_legacy_toggle` now asserts the 2.3
  white floor, not 3.0. Now verified by an actual `python -m pytest -q` run
  (2026-07-01): 188 passed / 1 known Tcl `nl.msg` env failure.

### Fast-follow scoped (next PR, after this branch merges)

A separate PR (its own design pass, per the hard rule) to retire the remaining
ad-hoc HSV/alpha color math onto bootstack-style utilities:

- **`elevate(surface, level)`** — mode-aware surface raise (built on the private
  `_mix`/`_relative_luminance` primitives), replacing the 5 inconsistent
  trough/track `update_hsv` sites (`label.py`, `progressbar.py` ×2, `scale.py`,
  `floodgauge.py` — four darken 20%, floodgauge lightens 80%) and folding the 4
  `make_transparent(0.4, …)` unchecked-indicator muting sites onto `_mix`
  (visually identical). One stripe site (`progressbar.py:40`) may want a `tint`.
- **`input_bg(surface=None)`** — mode-aware field background policy built on
  `elevate`: `= bg` in light (border carries the affordance), `= elevate(bg)` in
  dark (fill carries it; border ≈ bg). Encodes "fill vs outline are substitutes,
  use one per mode." Open decision for that PR's design pass: derive `inputbg`
  (drop the hand-authored, inconsistent per-theme dark deltas) vs coexist — the
  derive path needs the deferred built-in theme-dict conversion (Workstream E).

## Scaling and asset geometry — MERGED #1083, VISUALLY APPROVED

Approved decisions: public size-bearing `Assets`/Icon APIs take logical UI
units; `IconRenderer.render()` remains a physical-pixel leaf; final
layout-facing images keep exact dimensions with no even snap; #1081 geometry is
locked at checkbox/radio 18×18, switches 38×18, scale thumb 22×22 and track
12×6, progressbar thickness 8/4/12, and scrollbar thumb 18×8 at 100%.

- New private `style/scaling.py`: one service attached to the Tk root; 96-DPI
  Windows/X11 and 72-DPI Aqua baselines; nominal quarter-step normalization;
  round-half-away conversion; direct source-pixel conversion; no global state.
- `Style`, both builders, public `utility.scale_size`, `Assets`, icons, and
  recolored rasters share that service. `Window(scaling=...)` remains applied
  before `Style` and the first lazy build. Windows stays system-DPI-aware;
  per-monitor-v2/live rebuilds remain out of scope.
- Size-bearing toolkit inputs are logical. Builders no longer pre-scale asset
  inputs. `icon_element` also scales numeric border/padding/width/height once.
  Exact odd image frames are preserved; the icon renderer owns its physical
  frame normalization.
- Element manifest v2 records `source_size` separately from approved logical
  `size`, `border`, and `padding`. Rotations transform logical metadata with the
  pixels. Cache keys remain based on final physical dimensions and colors.
- Tk-facing builder padding, borders, focus/insert widths, sash and arrow
  geometry, progress/floodgauge thickness, Treeview geometry, and legacy-tk
  widths now scale once. AST guards reject new unscaled numeric builder geometry
  and pre-scaled logical toolkit inputs.
- Verification: focused scaling/toolkit/icon/recolor suite **68 passed**;
  expected full suite **177 tests**; local full result **176 passed / 1 known Tcl
  `nl.msg` environment failure**; excluding localization **171 passed**.
  Warning-free import; 36 fresh-process style imports; Python 3.10 parsed 88
  source/test files; 226 annotation targets force-evaluated. Preview constructs
  successfully in separate processes at all four factors.
- Human gate passed (user, 2026-06-29): both preview tabs and flatly↔darkly
  switching approved at 100%, 125%, 150%, and 200%.

**Recolorable raster widget assets — MERGED #1081, VISUALLY APPROVED.** Source
branch: `feat/2.0-recolor-elements`. Locked design:
**`development/2_0_recolor_assets_design.md`**. Radio/checkbox/switch/scale/
scrollbar/progressbar now use bootstack-derived templates from
`assets/elements/`; icons remain for date/carets/sizegrip.

- New leaf `style/elements.py`: lazy JSON manifest/source cache; black/white
  structural channels + optional magenta fill; source alpha preserved; no
  cyan/teal or surface preblend. Horizontal flip handles switch-off; quarter
  turns generate vertical slider/scrollbar/progressbar assets and rotate their
  border/padding metadata. `Assets.recolor` is the only new public surface.
- `StyleBuilderTTK.configure()` now owns the builder-to-engine raw configure
  seam; all 44 raw configuration sites call the local alias, and only that
  alias reaches `Style._build_configure` to bypass public bootstyle resolution.
- Cache key covers asset, final scaled size, every resolved target color, and
  transform. Manifest sources are authored at 2x and resized once.
- Standard + round scrollbars are arrowless raster-thumb layouts; their native
  troughs blend into `colors.bg` and require no trough image asset.
  Selected radio is an accent annulus. Existing striped progressbars remain on
  the stripe renderer. New `bootstyle="thin"` progressbar + public `THIN`
  constant use `progressbar-thin.png`. Checkbutton, radiobutton, and both switch
  layouts use a cached transparent spacer between the indicator and label.
  Progressbar images and layout children stretch only along their orientation
  (`EW` horizontal, `NS` vertical), preventing cross-axis image repetition;
  their style background is the theme surface (`colors.bg`), not the bar color.
  Standard and round scrollbar thumbs now follow the same contract: no
  element-level sticky, axis-only layout sticky, and a surface background.
- Verification: recolor/channel/alpha/transform/metadata/cache/layout/package
  tests added; targeted **38 passed**; remaining headless suite excluding the
  broken local Tcl localization file **98 passed**; warning-free import,
  standalone module guard, Python 3.10 grammar parse, and 684-namespace
  annotation evaluation clean.
- Manual gate passed (user, 2026-06-28): `examples/recolor_assets_preview.py`
  approved after indicator spacing, progressbar stretch/surface, and scrollbar
  thumb-only/native-trough corrections.

## Builder modularization — MERGED #1082, VISUALLY APPROVED

Goal: replace the 2,600+ line `style/builders_ttk.py` recipe monolith with a
private, decorator-backed registry and one module per widget family, following
bootstack's organization without adopting its style grammar or widget API.

Locked scope from the 2026-06-28 discussion:

- Keep the existing bootstyle grammar, generated ttk style names, lazy build
  behavior, theme lifecycle, visuals, and public APIs unchanged.
- Keep `StyleBuilderTTK` as the small per-theme context/coordinator: style,
  colors/theme/assets, scaling/configuration helpers, theme setup, and registry
  dispatch.
- Add a private `style/builders/` package with explicit module imports,
  deterministic `(variant, widget-family)` registration, and family-local asset
  helpers. Put only genuinely shared helpers (such as arrow/spacer assets) in
  `builders/utils.py`.
- Preserve recipes that build/register multiple ttk styles (horizontal +
  vertical pairs, headers, chevrons, and related styles). Do not assume one
  registry call produces only the requested style name.
- Do not copy bootstack's swallowed loader exceptions or silent duplicate
  replacement: imports should fail visibly and duplicate registry keys should
  fail tests.

Implementation summary:

- Merged PR: **#1082**, targeting `2.0`; merge commit `fa1cede8`
  (implementation commit `96bcab40`, handoff commit `f8c20dd8`).
- Approved design: `development/2_0_builder_split_design.md`.
- `StyleBuilderTTK`: 2,689-line monolith → 161-line per-theme coordinator.
- Private frozen registry: 36 exact `(variant, widget-family)` keys; explicit
  loader; duplicate, late, invalid, and non-callable registration fail visibly.
- Recipes: 22 family modules plus `builders/utils.py`; only caret and indicator
  spacer helpers are shared. Multi-output recipes and the three existing recipe
  dependencies are preserved.
- Dispatch: `Bootstyle` uses registry lookup; `name_to_method()` and all ttk
  recipe reflection are removed. Third-party passthrough remains lookup-only,
  while exceptions inside registered recipes propagate.
- Tests: +18 registry/dispatch/lazy/multi-output tests and +25 standalone module
  cases. Targeted registry/package suite **66 passed**.
- Structural gates: warning-free import; Python 3.10 parsed 35 style modules;
  25 fresh-process builder imports; 222 annotation targets force-evaluated.
- Full local suite: **146 passed / 1 environment failure** at missing
  `tk8.6/msgs/nl.msg`; excluding the six-test localization module gives
  **141 passed**. Expected on a complete Tcl install: **147 passed**.
- Manual gate passed (user, 2026-06-29): the current light↔dark set runs well.

Use one implementation branch/PR. Splitting this into parallel branches would
create avoidable conflicts in `builders_ttk.py`, `bootstyle.py`, and package
imports; the coherent unit is the complete behavior-preserving modularization.

## PR 6b — MERGED (2026-06-28, #1080, Workstream I — glyph builders on icons)

Built hybrid: Opus settled the public API + the held-branch keep/drop split and
implemented the registration path; a Sonnet agent did the mechanical glyph/layout
migration against the locked `development/2_0_icons_design.md`; Opus reviewed the
diff. Three commits; suite **92 passed**, warning-free import, font not loaded at
import, standalone cycle guard + PEP 649 sweep clean.

- **`f282262` — public style-registration path** (the PR-6a finding). New
  `register_style(style, ttkstyle)` in `style/layout.py`; **`layout()` now
  auto-registers** the style it applies (defining a layout is what gives a style
  its identity — mirrors ttk's own `style.layout`), so a toolkit-built style
  whose terminal step is `layout()` resolves via `style="..."` with no extra
  step. Re-exported from `ttkbootstrap.style` + top-level. +3 tests.
- **`435ec23` — Part A: glyph builders → icons** (−715/+155). check/radio/
  round-toggle/square-toggle/date/arrows/sizegrip migrated onto `icon_element`/
  `a.icon` per the design's glyph+color tables; the six `create_*_assets` glyph
  methods deleted; `ImageFont`/`Transpose` imports removed. Toggles are **one
  look** (`toggle-on`/`toggle-off`; square is a visual alias). Radio on =
  `record-circle-fill`. Existing state-color math + scaled sizes preserved.
  **Deviation (correct):** element names use the full `{ttkstyle}.indicator`
  prefix (not `sn.element`) so `icon_element`'s foreground lookup targets the
  configured style — matches PR 5's radiobutton convention.
- **`b63db19` — Part B: geometric/layout cleanup** (−353/+150). Separator,
  progressbar (+stripes), scrollbars (round/square), combobox, floodgauge,
  spinbox, treeview, calendar layouts re-applied onto `rect`/`rounded_rect`/
  `image`/`image_element`/`layout`/`El`/`state_map` (re-applied fresh from the
  held branch as reference — not cherry-picked; the file had drifted).

- **Open glyph picks — settle on the spot-check:** `calendar-event` (date) vs
  `calendar`; `grip-horizontal` (sizegrip) vs a corner-grip glyph; LIGHT-on-light
  knockout readability (existing contrast logic preserved as a safety net);
  toggle aspect ratio (rendered at `[24,15]`). Change a pick by editing the one
  glyph name in the builder.
- **Spot-check checklist:** check/radio/toggle indicators across all states
  (esp. disabled = muted) on a light theme and a dark theme; combobox/spinbox/
  scrollbar chevrons (normal/active/disabled); date button calendar; sizegrip;
  separator + striped-progressbar tile alignment; round vs square scrollbar
  thumb shape.

### Spot-check round 2 — DONE (2026-06-28, commits `a8a5f5d`, `9590798`)
From the user's first visual pass: toggle sized up to the glyph's true ~1.6:1
aspect (`[24,15]→[32,20]`, element width 28→36); date button → `calendar3`;
combobox/spinbox arrows switched from outline `chevron-*` to solid `caret-*-fill`
+ right `-padding(6)`; **menubutton** (solid + outline) native clam triangle →
`caret-down-fill` image indicator (new `_build_menubutton_arrow` helper; outline
recolors on hover, solid doesn't); **datepicker header** `◀/▶` text →
`caret-left/right-fill` images in the bar's contrasting fg. Suite 92, warning-free.

### FOLLOW-UP (deferred to a separate PR) — visual polish
**Decision (user, 2026-06-28): PR 6b's job was the *bones* — the icon engine
wired into every glyph builder + the geometric/layout cleanup + the public
registration path. That is done, so PR 6b is merge-ready and a PR is open against
`2.0`. The remaining work is value/asset tweaking, deferred to a follow-up PR.**
Polish candidates (eyeball a fresh `python -m ttkbootstrap` + a date picker):
menubutton caret **size/right-padding** (currently `[13,11]` caret + 10px pad, up
from the tiny native `arrowsize=4` — may read large); datepicker arrow size (14px)
next to the bold title; toggle final sizing; remaining glyph picks
(`grip-horizontal` sizegrip, LIGHT-on-light readability).

## PR 6a — MERGED (2026-06-27, #1079, Workstream I Tier 1.5 — icon engine)

Merged into `2.0` (was `feat/2.0-pr6a-icon-engine`). Engine only — touches **no**
builders, so nothing visual changed yet; suite **89 passed** (was 75; +14 in
`tests/widget_styles/test_icons.py`). Independently diff-reviewed (no leaks;
cache/leaf-layering invariants hold). Per `development/2_0_icons_design.md` (see
its "PR 6a — IMPLEMENTED" section).

- **Vendored** `src/ttkbootstrap/assets/icons/` (`bootstrap.ttf` + `glyphmap.json`
  + `icon_metrics.json`, MIT, LICENSE+README) + regen tool
  `tools/generate_icon_metrics.py`; `assets/icons/*` added to pyproject
  package-data (the `assets/*` glob does not recurse). No new pip dep.
- **`style/icons.py`** (leaf: PIL+stdlib + the two leaf toolkit modules; `Style`
  reached only function-locally): `IconRenderer` lazy-loads font/glyphmap/metrics
  once (persists for process lifetime), renders one glyph via bootstack's
  metrics fit-and-center; **unknown glyph raises**. Public `Icon(name,size,color)`
  atom (keyword-or-hex, resolved once) + `icon_element(...)` state→icon sugar.
- **`Assets.icon`** routes through `Style._get_or_create_image`, key
  `("icon", name, even-snapped size, resolved color)`; takes an already-resolved
  color (like `circle`/`rect`), keyword resolution lives in `Icon`.
- **Render tuning** (settled via a live light↔dark spot-check on Retina):
  icon-specific **6×/3×/1× supersample** (vs bootstack's 3/2/1) + gentle
  **`UnsharpMask(0.5/50)`** — curve smoothness comes from supersampling, not the
  sharpen. **Radio "on" → `record-circle-fill`** (solid knockout), not the thin
  `record-circle`. `examples/icon_preview.py` is the spot-check tool.
- **Gates:** `icons` added to the standalone-import cycle guard; PEP 649
  annotation sweep clean; import warning-free + font not loaded at import.
- **Finding carried to PR 6b (IMPORTANT):** a hand-built custom style applied via
  `style="X.TWidget"` is **silently re-resolved to base `TWidget`** unless the
  name was registered with the private `Style._register_ttkstyle(...)` —
  `BootMixin` only honors `style=` for `style_exists_in_theme()` styles. The real
  builders register; the design's public mock #2 + the demo did not. **PR 6b /
  Tier-2 must give the public toolkit a non-private registration path** (e.g.
  `layout()` registers the style name, or a public `register_style`). Details in
  the design doc's "Finding for PR 6b" section.
- **Open minor glyph picks (defer to 6b spot-check):** `calendar` vs
  `calendar-event`; sizegrip glyph.

## PR 6 — HELD + icon pivot (2026-06-27)

The fast-follow toolkit migration was implemented on
`feat/2.0-pr6-toolkit-migration` (9 commits, suite 75 passed): geometric recipes
(`circle`/`rect`/`rounded_rect`), all 21 `layout()` pyramids, `image_element`/
`state_map` conversions, and `image()`-escape-hatch glyph draws for check/radio/
date/arrows/sizegrip/stripes. **It is NOT merged and is HELD** — the hand-drawn
*glyph* draws looked poor, prompting the icon-font pivot.

**Decision (LOCKED with user):** render glyph-shaped widget assets from a
**vendored Bootstrap Icons font** (`bootstrap.ttf` + `glyphmap.json` +
`icon_metrics.json` from `bootstack/src/bootstack/assets/icons/`, ~610 KB, MIT,
no new pip dep), porting bootstack's metrics-based fit-and-center renderer (the
alignment fix = precomputed em-fraction ink bbox, kills the `getbbox` skew /
`font_offset` fudge) and reusing the PR-5 `style/assets.py` snap/oversample/
UnsharpMask pipeline + the PR-2 `_get_or_create_image` cache. Full design +
locked API + acceptance proof: **`development/2_0_icons_design.md`**. Memory:
`project_2_0_icon_assets`.

Locked headlines: flat single-glyph indicator aesthetic; public surface =
`Icon(name,size,color)` atom + style-level `icon_element(...)` state→icon sugar
(spec grammar adopted from ttkbootstrap-icons' `StatefulIconMixin`, but **not**
its per-widget theme-follow delivery — that fights the no-`Publisher` engine);
switch = one look; arrows = chevron. Geometric assets (tracks/troughs, stripes,
plain scale thumb) stay on the recipes.

**PR plan (replaces the held PR 6):**
- **PR 6a — icon engine (no behavior change):** vendor the 3 assets + regen tool
  + license; `style/icons.py` (`IconRenderer`); `Assets.icon`; public `Icon` +
  `icon_element`; re-exports; tests. Touches **no** builders → suite stays green.
  **✅ MERGED (#1079) — see "PR 6a — MERGED" above.**
- **PR 6b — migrate glyph builders + land the kept geometric/layout cleanup**
  (cherry-pick the geometric/`layout`/`image_element` commits from the held
  branch; drop the hand-drawn glyph commits). Gate the merge on a **human visual
  spot-check** (light↔dark) — the headless suite asserts color-at-pixel, not
  appearance. **Also add the public style-registration path** (PR-6a finding).
  **← next actionable.**

### Merged into `2.0`
- **#1068** — Tier-0 cleanup:
  - Removed long-deprecated top-level shims (`scrolled.py`, `tableview.py`,
    `toast.py`, `tooltip.py`, `dialogs/dialogs.py`). Import from
    `ttkbootstrap.widgets.<name>` / `ttkbootstrap.dialogs` now.
  - Split headless tests from interactive demos: `tests/` is pytest-only (4
    `test_*.py` + new `tests/conftest.py`); ~54 demos moved to `examples/`.
  - `conftest.py` adds a session-scoped shared root + per-test `root` fixture
    (scene + theme reset) — fixes the `Style` singleton bleeding between tests.
  - `pyproject.toml` gained `[tool.pytest.ini_options]` (`testpaths=["tests"]`,
    `gui` marker).
- **#1069** — Public/internal split:
  - New `src/ttkbootstrap/internal/` package (name is `internal`, no underscore).
  - `publisher` → `internal/publisher.py`; top-level `ttkbootstrap.publisher`
    is now a warn-and-reexport shim (removed in 3.0).
  - `utility` stays public (`enable_high_dpi_awareness`, `scale_size`); its two
    internal helpers (`get_image_name`, `center_on_parent`) moved to
    `internal/utility.py`, forwarded from `utility.py` via `__getattr__` + warning.
- **Workstream B (widget-level lifecycle leaks)** — `destroy()`/unsubscribe paths:
  - Canvas `Floodgauge`: trace ids tracked; removed on `destroy()` and when a
    `variable`/`textvariable` is swapped via `configure` (was unbounded trace
    accumulation + external vars pinning a dead widget). `destroy()` also cancels
    the running `after()` animation loop.
  - `Meter`: `_set_interactive_bind()` unbinds before rebinding (no orphaned
    indicator binds when toggling `interactive`); `destroy()` detaches the
    `amountusedvar` write trace.
  - `Combobox` popdown: self-unsubscribes from `Publisher` via a once-bound
    `<Destroy>` handler (`style.py` ~`5434`), so cleanup no longer depends solely
    on the `Window` global `<Destroy>` binding (absent under a vanilla `tk.Tk()`).
  - New `tests/widgets/test_lifecycle.py` (6 headless regression tests).
  - **Not done (left for the engine session):** the `Publisher` mechanism itself
    (keystone, below).
- **`FloodgaugeLegacy` deprecation** — instantiating it now emits a runtime
  `DeprecationWarning` (3.0 removal); was docstring-only. Canvas `Floodgauge`
  stays warning-free, and so does `import ttkbootstrap` (warning fires on init,
  not import). New `tests/widgets/test_deprecations.py` (2 tests). Its lifecycle
  trace leaks were left as-is — the widget is on the way out.
- **Example demo rename** — dropped the misleading `test_` prefix from the ~31
  interactive demos under `examples/` (moved out of `tests/` in #1068 but kept
  their prefixes). Pure renames; `examples/widgets/test_tableview.py` →
  `tableview_yscrollbar.py` to avoid colliding with the existing `tableview.py`.

## The hard rule

**Do not start the `style.py` engine rewrite as ad-hoc coding.** The design
discussion has now been held (see below) — the agreed design lives in
`development/2_0_engine_design.md`. Implementation proceeds **PR by PR per that
doc**, starting with PR 1; do not exceed PR 1's scope without revisiting the doc.

## Engine design session — DONE (2026-06-25)

The dedicated design discussion is complete. Full design:
**`development/2_0_engine_design.md`**. Decisions locked this session:

1. **Style rebuild = lazy, version-stamped** — rebuild a `(theme, style)` only
   when a stale *mounted* widget references it; O(mounted), not O(all-styles).
2. **Multi-root = enforce single-root with a clear `RuntimeError`** — close the
   silent-no-op trap; full multi-root out of 2.0 scope.
3. **Packaging = engine PR in-place, split later** — rewrite repaint/image paths
   inside `style.py` first; `style/` package split is a follow-on PR.
4. **Image cache = content-addressed memoization** — key the asset builders on
   their pixel-determining inputs (resolved hex, scaled size, state, geometry),
   NOT the theme name, so cross-theme-identical assets dedupe and never
   re-render. This also moots theme-return rebuild cost and decouples eviction
   from theme-switch timing.

Resolved repaint model: monotonic `Style._theme_version`; DFS over
`winfo_children()` repaints+restamps only stale widgets (ttk → ensure its
`(theme,style)` fresh; tk-legacy → re-run `update_tk_widget_style` inline);
the `__init__wrapper` keeps its initial paint but **drops `Publisher.subscribe`**.
This deletes `Publisher` wholesale (the leak class disappears — no registry, no
strong refs).

### Agreed PR sequence
- **PR 1 — repaint engine (in-place):** version stamp + theme walk; delete
  `Publisher` (subscribe sites `style.py` ~`5427`/`5552`, publish ~`710`/`716`,
  unsubscribe `window.py` ~`106`); lazy per-theme style rebuild; single-root
  `RuntimeError`. **← next actionable slice.**
- **PR 2 — image cache:** route ~40 `theme_images[...]=` sites through
  `_get_or_create_image`; single content-addressed cache + `clear_image_cache()`;
  builder-purity audit.
- **PR 3+ —** mixin API (C), then `style/` split (G), then theme/anchor (E) +
  bootstyle canonical (D).

### Two pre-flight checks for implementation (not yet settled)
- (a) Is the **combobox popdown** toplevel reached by the root `winfo_children()`
  DFS, or does it need an explicit per-Combobox repaint in the walk?
- (b) **Builder-purity audit**: any asset builder reading color/size from
  `self.colors`/`self.theme` internally (not via args) must lift that input into
  the cache key, else stale images survive a theme change.

Verification to lean on: `tests/widgets/test_lifecycle.py` (destroy/recreate
harness) + `tests/widget_styles/` (built-style values).

## PR 1 — MERGED (2026-06-25, #1073)

Merged into `2.0` (was `feat/2.0-pr1-repaint-engine`); suite **24 passed**.
Full write-up + the pre-flight (a) resolution in
`development/2_0_engine_design.md`. Headlines:
- Monotonic `Style._theme_version`; `theme_use` bumps it then runs `_theme_walk`
  (DFS from the root, repaint+restamp only stale widgets). Deleted
  `_create_ttk_styles_on_theme_change`; rebuild is now lazy/O(mounted).
- `Publisher` removed from the engine (no subscribe/publish/unsubscribe). Module
  + the `ttkbootstrap.publisher` shim kept unused until the 3.0 removal date.
- Combobox popdown repainted inline in `update_ttk_widget_style` (pre-flight (a):
  the popdown is **not** reachable by the Python `winfo_children()` DFS).
- `autostyle=False` tk widgets set `_tb_no_autostyle`; the walk skips them.
- Single-root enforced: `Window.__init__` → `_require_single_root` raises a clear
  `RuntimeError`; `Window.destroy` now clears the class-level `Style.instance`.
- New tests in `tests/widgets/test_lifecycle.py`: no-Publisher-subscriptions,
  walk stamps/repaints mounted widgets, theme-switch-cycle leak check,
  autostyle-skip, single-root raise.

## PR 2 — MERGED (2026-06-25, #1074)

Merged into `2.0` (was `feat/2.0-pr2-image-cache`); suite **28 passed**.
Full write-up + pre-flight (b) resolution in `development/2_0_engine_design.md`.
Headlines:
- Single content-addressed cache `Style._image_cache` + private
  `Style._get_or_create_image(key, factory)` + `Style.clear_image_cache()`.
- All ~40 `theme_images[...] =` sites routed through the helper; per-builder
  `theme_images` dict removed (the image leak) and the fragile
  `_PhotoImage__photo.name` accesses gone.
- Keys are the resolved local colors + scaled size + variant/geometry tag
  (never `colorname`), so theme differences are captured by construction.
- `_get_or_create_image` kept **private**; public toolkit (`image_asset`) is
  Workstream I.
- Verified pixel-level (no stale image after switch) and bounded (20 theme
  round-trips hold the cache flat). New `tests/widget_styles/test_image_cache.py`.

## PR 3 — MERGED (2026-06-25, #1075)

Merged into `2.0` (was `feat/2.0-pr3-mixin-api`). Replaces the import-time
monkey-patch with the mixin-hybrid API (Workstream C). Suite: **42 passed**.
Design pass + the one open fork (tk-side scope) were resolved up front: **full
retirement of the import-time patch** — the blessed tk widgets get a mixin too,
not just ttk.

Headlines:
- **Two mixins in `style.py`** (after `Bootstyle`): `BootMixin` (ttk — intercepts
  `bootstyle`/`style` on `__init__`/`configure`/`config`/`__setitem__`/
  `__getitem__` via `super()`, reusing the unchanged `update_ttk_widget_style` +
  `stamp_theme_version`) and `AutoStyleMixin` (tk — autostyle at construction,
  honoring `autostyle=False` → `_tb_no_autostyle` opt-out, same flag the PR 1
  theme walk skips). Real `super()` methods, so the old late-binding closure bug
  is gone. (Side finding: the legacy `__setitem__`/`__getitem__` overrides never
  actually installed — `widget.__getitem` raised `AttributeError` swallowed by a
  bare `except: continue` — so the mixin's correct accessors are a net gain.)
- **Concrete subclasses re-exported from `__init__.py`**: 19 ttk (`class
  Button(BootMixin, ttk.Button)` …; `OptionMenu` restores tkinter's
  `__getitem__`/`__setitem__` for menu-item access) + 6 tk (`Tk`, `Menu`, `Text`,
  `Canvas`, `TkFrame`, `LabelFrame` with `AutoStyleMixin`). Defined **before** the
  widgets/dialogs/window imports, since those import widget names from
  `ttkbootstrap` — so the whole internal tree flows through the mixins with **no
  global patch**.
- **Import-time `setup_ttkbootstrap_api()` call removed**; it is now the body of
  the opt-in `enable_global_api()` (idempotent; its wrappers defer to
  `BootMixin`/`AutoStyleMixin` instances via an `isinstance` guard, so the global
  path never double-resolves a blessed widget). `import ttkbootstrap` stays
  warning-free.
- **New delivery primitives** (all re-exported): `bootify(cls)` →
  `type(cls.__name__, (BootMixin, cls), {})`; `apply_bootstyle(widget, bootstyle)`
  for per-instance styling with no class mutation; `enable_global_api()`.
- **Typing**: deleted the ~450-line inline `TYPE_CHECKING` block **and** the
  54 KB `__init__.pyi`. Concrete classes carry a one-line docstring each;
  `bootstyle` is now statically visible. Accepted trade-off (per the locked
  decision): native per-widget kwargs degrade from the hand-maintained stubs to
  typeshed-inherited + `**kwargs`.
- **Two regressions found + fixed during the sweep:** `Toplevel` (subclasses
  `tkinter.Toplevel` directly, so it missed the retired tk patch) now paints
  itself via `Bootstyle.update_tk_widget_style`/`stamp_theme_version` in
  `window.py`; `tableview.py`'s 8 context menus switched from raw `tk.Menu` to the
  blessed `ttk.Menu`. `Window` was already fine (its `Style(themename)` themes the
  root).
- **Back-compat preserved:** the legacy tuple/list `bootstyle` form still resolves
  (used internally by `Meter`/`DateEntry`/tooltip/datepicker) — canonical-string
  enforcement is Workstream D, untouched here.
- **Tests:** new `tests/test_mixin_api.py` (14 tests: subclass shape, stock
  tkinter stays unpatched, bootstyle/configure/item-access resolution, tuple
  back-compat, OptionMenu item access, autostyle opt-out, `bootify`,
  `apply_bootstyle`, `enable_global_api` idempotency). `test_lifecycle.py`'s
  autostyle-opt-out test updated to use the blessed `ttk.Canvas`.

## PR 4 — MERGED (2026-06-25, #1076, Workstream G — `style/` split)

Design pass first (per the hard rule): `development/2_0_style_split_design.md`.
Scope decision (asked + answered): **pure, behavior-preserving move**; the
Workstream I toolkit is a separate follow-on PR. Merged into `2.0` (was
`feat/2.0-pr4-style-split`). Suite: **61 passed**.

- `style.py` → `style/` package: `theme.py` (Colors, ThemeDefinition),
  `builders_tk.py` (StyleBuilderTK), `builders_ttk.py` (StyleBuilderTTK — the
  bulk), `engine.py` (Style), `bootstyle.py` (Keywords, Bootstyle,
  BootMixin/AutoStyleMixin, bootify/apply_bootstyle/enable_global_api),
  `__init__.py` (re-exports the full public surface).
- Strict downward import layering (theme→builders_tk→builders_ttk→engine→
  bootstyle); the only cycles are **6 function-local back-edges** (Colors→Style,
  the two builders' `__init__`→Style, engine→Bootstyle ×2). No import-time cycle;
  each submodule imports standalone.
- **No shim needed** — `ttkbootstrap.style` stays a valid public path; every
  existing `from ttkbootstrap.style import …` resolves unchanged;
  `import ttkbootstrap` stays warning-free. Submodule paths (`style.engine`, …)
  are implementation detail (treat like `internal/`).
- New `tests/test_style_package.py` (structural guards: public surface, legacy
  imports, standalone-submodule cycle guard, consumer imports).
- **Python 3.14 / PEP 649 gotcha** found + handled: lazy annotations masked a
  missing annotation-only import (`ThemeDefinition` in `builders_tk`). A
  "does it import?" check is insufficient on 3.14 — added an annotation
  force-evaluation sweep. **Reuse it for E/D code moves.** Details in the design
  doc's "Implementation — DONE" section.

## PR 5 — MERGED (2026-06-25, #1077, Workstream I Tier-1 toolkit)

Merged into `2.0` (was `feat/2.0-pr5-toolkit`), per
`development/2_0_toolkit_design.md`. Suite: **75 passed** (was 61; +14 in
`tests/test_toolkit.py`). Headlines:

- **New `style/assets.py`** — `Assets(style)` facade over PR 2's
  `Style._get_or_create_image`. Recipes `circle`/`rect`/`rounded_rect` + the
  `image(size, draw_fn, *key_parts)` escape hatch. The cache key is *derived
  from the render inputs* (resolved hex + snapped size + geometry), so it cannot
  drift from the pixels — the hazard PR 2's purity audit managed by hand. Ports
  bootstack's snap-at-the-source pipeline: even-pixel-snap the size, adaptive
  oversample (3×/2×/1× by size), LANCZOS + `UnsharpMask`. No public
  `oversample`/`inset` knobs. `rect` is solid-fill (no AA, no snap → keeps exact
  size, e.g. the 40×5 scale track).
- **New `style/layout.py`** — `El`/`layout` (lowers an `El` tree to ttk's nested
  `(name, opts)` form; children via constructor kwarg, not bootstack's fluent
  positional parenting), `image_element` (named, validated state→image map),
  `statespec`/`state_map` (validate the `!neg`/space-AND grammar against
  `TTK_STATES` — the Workstream D loud-failure seam; keep the token set here),
  `StyleName` (absorbs the `DEFAULT/""`→PRIMARY, `f"{color}.{STYLE}"`, and
  `.TS→.S` element-name dance).
- **Acceptance test met**: `create_scale_assets`/`create_scale_style` and
  `create_radiobutton_assets`/`create_radiobutton_style` migrated onto the
  toolkit — shorter and clearer (radio style 69→29 lines incl. docstring; the
  30-line layout pyramid → 5 readable lines). Behavior-preserved: layouts query
  identical to the originals (`expand`=`'1'`, `sticky`=`'nswe'`, same element
  names + radio pyramid, same `foreground`/disabled map). The migrated radio
  keeps the original `sticky=""` on indicator/focus (the design's example
  omitted it; kept for behavior-exactness).
- **Public surface** re-exported from `style/__init__.py` *and* top-level
  `ttkbootstrap` (`Assets`, `El`, `layout`, `image_element`, `statespec`,
  `state_map`, `StyleName`); `import ttkbootstrap` stays warning-free.
- **`test_image_cache.py` helper** updated: the scale thumb's key tag moved from
  `"scale.thumb"` to the recipe's `("circle", fill, size, None, 0)`; assertions
  unchanged (still color-at-pixel, robust to the snapped-pipeline AA change).
- **Gates re-run**: standalone-import cycle guard (assets/layout import alone;
  they're leaves — assets→PIL, layout→constants, no engine edge) and the PEP 649
  annotation force-evaluation sweep (3.14) over the two new modules + migrated
  builders — both clean.
- **Open follow-up (merged without it)**: a spot visual diff on scale/radio/check
  to confirm the snapped pipeline reads equal-or-better (sharper/DPI-stable, not
  color drift) — couldn't run a GUI in the headless dev env. Worth an eyeball
  before the next release.
- **Deferred (out of PR 5 scope)**: migrating the *remaining* ~25 asset / ~25
  layout sites onto the toolkit (mechanical, same shapes repeated) — design doc
  step 4, a fast-follow. Tier 2 (`state_colors` from ramp steps; composite
  recipes) waits on Workstream E.

## Workstream I — DESIGN PASS DONE (2026-06-25), implementation done (see "PR 5")

Design pass held (per the hard rule — new public surface, like the engine/split
got one). Full design: **`development/2_0_toolkit_design.md`**. The next session
**implements PR 5 from that doc**; do not exceed its scope without revisiting it.

Tier-1 toolkit lands in **`style/assets.py`** (`Assets` facade: `circle`/`rect`/
`rounded_rect` shape recipes + an `image(size, draw_fn, *key_parts)` escape hatch,
all wrapping PR 2's `_get_or_create_image`) + **`style/layout.py`** (`layout()`/
`El`, `image_element`, `statespec`/`state_map`, `StyleName`). Re-exported from
`style/__init__.py` and top-level `ttkbootstrap` (public custom-style API).

Decisions locked this session:
- **PR scope = one PR** (assets + layout together; the acceptance test spans both).
- **The key is derived from the recipe, never hand-written** — kills the
  hand-built-key purity hazard that PR 2's whole audit existed to manage.
- **Fidelity = adopt bootstack's snap-at-the-source pipeline** (not the earlier
  (A)/(B) drift tradeoff). Per user steer, mined `bootstack/src` and ported four
  mechanisms into `Assets`: round the DPI factor; **even-pixel-snap** the final
  size before keying/rendering (kills fractional-DPI LANCZOS blur); **adaptive
  oversample** (3×/2×/1× by size) + snap draw origin to oversample multiples;
  LANCZOS + `UnsharpMask`. Result is *crisper, DPI-stable* assets, not color drift
  → PR 2's color-at-pixel purity tests still pass. No public `oversample`/`inset`
  knobs. (bootstack refs in the design doc's fidelity section.)
- **`El`/`image_element` mirror bootstack's `Element.spec()`/`ElementImage.build()`**
  (same author, keep models in sync), with two deliberate divergences: constructor
  `children=[...]` (not fluent positional parenting) and validating `statespec`
  (the Workstream D loud-failure seam).

Acceptance test pre-validated in the doc: `create_scale_assets` ~64→~22 lines,
`create_radiobutton_style` ~67→~18, both clearer. Carry the **PEP 649 annotation
force-evaluation sweep** into the new modules + migrated builders (3.14 gotcha).

Then E (theme/anchor model) + D (bootstyle canonical grammar), carrying the
`_compat` adapters. Tier-2 toolkit (`state_colors` from ramp steps) follows E.

## Open decisions (from the plan)
- ~~Multi-root~~ — **LOCKED**: enforce single-root with a clear `RuntimeError`.
- bootstyle strictness default: warn-by-default + opt-in strict (lean) vs strict.
  (Deferred to Workstream D — does not gate the engine PRs.)
- Built-in theme drift from auto-ramps (lean: accept) vs pin specific themes.
  (Deferred to Workstream E — does not gate the engine PRs.)

## Conventions established this effort
- `internal/` (no underscore) for private plumbing; warn-shim old public paths,
  remove in 3.0; `import ttkbootstrap` stays warning-free.
- Tiered deprecation: things deprecated for years → removed in 2.0; new 2.0
  standardizations → warn-and-normalize through 2.x, removed in 3.0.
- 2.0 PRs target `2.0`; maintenance/bugfixes target `master`.
