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

- [ ] **Deterministically green suite.** Root-cause the two "flakes" rather than
      wave them through: the `test_color_helpers` *Duplicate element
      TSpinbox.uparrow* failure is a real order-dependent theme-rebuild bug, not
      noise; confirm `nl.msg`/`zh_cn.msg` is genuinely env-only (Tcl can't read
      the catalog) and not a real localization regression.
- [ ] **Clean-env install smoke.** Build the wheel, `pip install` into a fresh
      venv, import warning-free (`-W error::DeprecationWarning`), and construct
      one of every widget/dialog. Catches missing package-data / subpackages
      (assets globs don't recurse; the new `utils/` subpackage; icon font).
- [ ] **Min-Python parse.** 3.10 grammar parse of all `src/` + PEP 649
      annotation evaluation (the sweep the color PRs ran).
- [ ] **Warning-free import** of `ttkbootstrap` and every submodule; the
      deprecation shims warn *only* when the old path is actually used.
- [ ] **Docs stubs.** The broken API `:::` stubs that crash mkdocstrings are
      release-blocking (Workstream H §11).

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

- `test_color_helpers` order-dependent *Duplicate element TSpinbox.uparrow*
  (theme-rebuild path) — real bug, currently reads as a flake.
- `center_on_screen` negative-origin multi-monitor bug (parked from PR B).
- `colorutils`/`utils.color` `color_to_rgb` swallows errors with a bare
  `except: print('this')` — behavior-preserving-move wart, worth fixing pre-3.0.
- Cross-platform gates owed but never eyeballed: win32 AppUserModelID/taskbar
  icon, aqua `overrideredirect`/`MacWindowStyle` popups, multi-monitor centering.
- Docs Workstream H: nav/IA skeleton + un-break the API `:::` stubs.
