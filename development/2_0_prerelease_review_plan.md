# ttkbootstrap 2.0 — pre-release review plan

> The capstone review before tagging a 2.0 RC. Per-PR review (design pass →
> fork → diff review → suite) caught issues *inside* each slice; this plan
> covers what no single PR review ever saw: the **cumulative `2.0…master`
> delta as a whole**, the seams between PRs, and the things that predate the
> review discipline. Living checklist — tick items as they close.

## When this runs

**At the end of the compat & utilities initiative, not before.** Slices 5/3/4
are still to land (`2_0_compat_and_utilities_design.md`); running the cumulative
sweep now would only have to be redone against the final tree. The design doc
calls these slices "the last substantive code work before release," so this
review is the natural capstone once they're merged. (Individual items the author
flags in the meantime still get normal per-PR review.)

## Why a cumulative pass is needed

Two properties of 2.0 drive the whole strategy:

1. **A large share of the changes are structurally invisible to the headless
   suite** — window/positioning/aqua/win32 chrome, DPI scaling, and the visual
   restyles (buttons, scrollbars, inputs, icons, themes). Green CI says nothing
   about whether they *look* right or work off-Windows.
2. **It's a breaking release with a migration contract.** `2_0_breaking_changes.md`
   / the *Migrating to 2.0* guide must match the actual public-API delta in both
   directions, or users hit undocumented breaks (or chase documented ones that
   don't exist).

## The three tracks

### Track A — agentic correctness + API sweep (automatable)

Fan out over the cumulative `2.0…master` diff, **decomposed by subsystem** so
each agent holds one area in context. Adversarially verify every candidate;
triage into *release-blocker* vs *post-release*.

Subsystem partition (one finder cluster each):
- style engine / theme-walk / image cache / singleton lifecycle
- bootstyle grammar + `_compat` normalization/strictness
- widgets (`widgets/` — the ConfigureDelegationMixin family)
- dialogs (`dialogs/` — Messagebox/Querybox/pickers)
- window / Toplevel / `internal/positioning`
- themes / anchor model / legacy adapter / `utils/`
- the deprecation-shim surface (publisher, colorutils, utility, tableview et al.)

Tooling: `/code-review ultra <2.0 branch>` (multi-agent cloud review of the
branch) is purpose-built for this; a `Workflow` with the subsystem partition is
the alternative when finer control is wanted. **Dry-run first** on the current
branch to size the finding volume before the full pass.

### Track B — human-gated visual + cross-platform (cannot be automated)

The accumulated "owed visual gates" from the handoffs live here. No agent can
close this.

- **Platforms:** win32 (primary), plus macOS/aqua and Linux/x11 if reachable.
- **Matrix:** light + dark, at 100 / 125 / 150 / 200 % DPI.
- **Known-parked bug to close here:** `center_on_screen` negative-origin on a
  multi-monitor layout (memory `center-on-screen-negative-origin-bug`; the
  order-dependent `test_center_on_screen` failure is its headless shadow).
- **Harness:** a single "everything-bagel" script that constructs one of every
  widget + dialog so the eyeball pass is one window, not thirty. (`gallery/` and
  `examples/` already have most of the pieces.)

### Track C — migration-contract validation

Mechanically diff the **public API surface** (`master` vs `2.0`) — exported
names, class signatures, kwargs, return shapes — and reconcile against
`2_0_breaking_changes.md`:
- every real break is documented (no silent break), and
- every documented break is real (no phantom entry).

Gaps in either direction are findings. Doubles as QA for the Workstream-H docs
rewrite (the guide is the docs' migration page).

## Gates before tagging an RC

- [x] **Deterministically green suite.** Both "flakes" root-caused (2026-07-09):
      the `test_color_helpers` *Duplicate element TSpinbox.uparrow* was a **real**
      theme-rebuild bug — `element_create` was not idempotent, so any recipe re-run
      on an already-materialized ttk theme (a test force-build, or a production
      `_theme_styles`/Tcl desync) crashed. **Fixed** by an idempotent
      `Style.element_create` override (`style/engine.py`) that no-ops when the
      element already exists in the current theme; +14 regression tests. The
      `nl.msg` failure (`test_msgcat`/`test_set`) is **confirmed genuinely
      env-only**: the localization file flips pass/fail across identical runs
      (6/6 pass in some runs, one transient `couldn't read file nl.msg: No error`
      in others), the catalog is present and readable, and ttkbootstrap only calls
      the standard `::msgcat::mclocale`. Not a regression; a transient Tcl file-read
      hiccup. (Optional: de-flake by retrying the msgcat load in the test.)
- [x] **Clean-env install smoke** (2026-07-09). Built the wheel, `pip install`ed
      into a fresh venv, imported warning-free (`-W error::DeprecationWarning`), and
      constructed one of every widget + dialog. **Pass** — all subpackages ship
      (incl. `utils/`), the `assets/icons/bootstrap.ttf` font + `assets/elements`
      + `assets/app_icons` + json manifests are present; the non-recursive globs
      dropped nothing (asset dirs are one level deep and each is listed).
      **Finding: `pyproject.toml` version is still `1.20.4`** — bump before tagging.
- [x] **Min-Python parse** (2026-07-09). 3.10 (`py -V:3.10`) `py_compile` of all
      84 `src/` files: clean. PEP 649 annotation force-eval: 352 targets resolve;
      the single `get_type_hints`-on-`constants` `Final` complaint is a
      module-level-`Final` artifact, not an evaluation failure.
- [x] **Warning-free import** (2026-07-09) of `ttkbootstrap` and all 83 submodules;
      the only three that warn (`colorutils`/`utility`/`publisher`) do so **only**
      when the old path is imported directly — correct shim behavior.
- [ ] **Docs stubs.** 9 broken API `:::` stubs in `docs/en/api` point at removed
      paths — `ttkbootstrap.icons` (Emoji/Icon), `ttkbootstrap.scrolled`,
      `ttkbootstrap.tableview`, `ttkbootstrap.toast`, `ttkbootstrap.tooltip`.
      They crash mkdocstrings; repoint to `ttkbootstrap.widgets.*` / delete the
      icons stubs. Release-blocking; **belongs to Workstream H** (docs).

## Sequencing

```
finish Slices 5 → 3 → 4   (normal per-PR review)
      │
      ▼
freeze cleanup work
      │
      ▼
Track A agentic sweep  ──►  triage: release-blocker vs post-release
      │
      ▼
Track B human visual / cross-platform passes
      │
      ▼
fix release-blockers only  ──►  green suite + install smoke
      │
      ▼
tag RC  ──►  Workstream H docs  ──►  final release
```

## Known latent items already logged (feed the triage)

- ~~`test_color_helpers` order-dependent *Duplicate element TSpinbox.uparrow*~~ —
  **FIXED** 2026-07-09 (idempotent `Style.element_create`; see the green-suite gate).
- `center_on_screen` negative-origin multi-monitor bug (parked from PR B) — still
  open; a "Recenter window" button in the Track B harness exercises it.
- `colorutils`/`utils.color` `color_to_rgb` swallows errors with a bare
  `except: print('this')` — behavior-preserving-move wart, worth fixing pre-3.0.
- Cross-platform gates owed but never eyeballed: win32 AppUserModelID/taskbar
  icon, aqua `overrideredirect`/`MacWindowStyle` popups, multi-monitor centering.
- Docs Workstream H: nav/IA skeleton + un-break the API `:::` stubs (9 broken —
  see the docs-stubs gate).

## Pre-release review run — 2026-07-09 (results)

**Track A (agentic sweep)** — 8-subsystem Workflow + adversarial verify. 5
candidates, 2 confirmed:
- **RELEASE-BLOCKER (FIXED):** `bootstyle="neutral"` crashed construction on every
  non-button widget family (Label/Entry/Checkbutton/Progressbar/Scale/Scrollbar/
  Combobox). `neutral` is in the global color vocab + the canonical `BootStyle`
  Literal + exported `NEUTRAL`, but `NEUTRAL_FAMILIES` was consulted only by the
  reference generator, never enforced at runtime → `Colors.get("neutral")` → None →
  TclError/TypeError inside the recipe, before `build_style`'s graceful fallback.
  Fixed: the resolver now gates `neutral` on `NEUTRAL_FAMILIES`, dropping it to the
  family default with a loud warning (raise in strict mode). +14 regression tests.
- **POST-RELEASE (open, minor/cosmetic):** `DatePickerDialog` highlights the wrong
  day when browsing away from the selected month. 2.0 added `datevar.set(day)` for
  the toolbutton "on" look, but the shared `datevar` is only re-set in the branch
  that matches the selected month, so navigating to another month leaves it pinned
  and that month's same day-number renders falsely selected. `datepicker.py:360`.
  The returned selection is correct (grid-coord based); purely a cosmetic stray
  highlight while browsing. Fix = reset/track `datevar` per redraw. **Author's call
  whether to fix now or defer.**

**Track B (visual/cross-platform)** — human-gated, cannot be automated. Delivered
`examples/prerelease_visual_review.py`: a single warning-clean window with one of
every native + shipped widget in its states, a theme picker + light/dark toggle, a
dialogs launcher, a "Recenter window" button (for the parked multi-monitor bug),
and the run-matrix checklist in its docstring. **The eyeball pass itself is still
owed** (light/dark × 100/125/150/200% DPI × win32/aqua/x11).

**Track C (migration contract)** — mechanical `master→2.0` public-surface diff
(runtime `inspect.signature` + `dir()`), reconciled against
`2_0_breaking_changes.md`. **No silent breaks; no phantom entries.** 9 top-level
removals (1 real+documented `icons`, 3 shim-forwarded+documented, 5 incidental
typing-name leakage), 13 constructor signature changes all documented, no dropped
`__all__`/widget/dialog exports. Two doc nits fixed: the Toast `set_geometry` entry
referenced a non-existent `_set_geometry`; DateEntry's `""`→`"primary"` default was
unstated.
