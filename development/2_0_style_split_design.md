# ttkbootstrap 2.0 — `style/` Package Split Design (Workstream G)

> Output of the Workstream G design pass (2026-06-25). Pairs with
> `development/2_0_plan.md` (durable worklist), `development/2_0_handoff.md`
> (session state), and `development/2_0_engine_design.md` (the engine keystone
> that PR 1/2 already landed). Line refs are point-in-time against `style.py` on
> the `2.0` branch — verify before relying.

## Scope

Workstream G's only remaining item is **splitting the ~5.9k-line `style.py`
into a real `style/` package** (the other G bullets — public/internal top-level
split #1069, dual-typing collapse PR 3, tests/examples split #1068 — are done).

This document does the **design pass on the package boundaries first**, per the
hard rule ("don't start the style.py refactor as ad-hoc coding"). No code moves
until the boundaries below are signed off.

## What's in `style.py` today

`wc -l` = 5870. Nine top-level definitions, in this order:

| Lines | Symbol | Role |
|---|---|---|
| 78–513 | `Colors` | color scheme + color math (HSV/contrast/ramp helpers) |
| 514–550 | `ThemeDefinition` | name + `Colors` + light/dark flag container |
| 551–1024 | `Style` | the engine: singleton, theme registry, `theme_use`, version-stamped walk, image cache, `_get_builder` |
| 1025–1371 | `StyleBuilderTK` | legacy `tk.*` widget styler (~350 lines) |
| 1372–5055 | `StyleBuilderTTK` | ttk widget styler — the bulk (~3700 lines, ~40 asset sites) |
| 5056–5132 | `Keywords` | bootstyle grammar data (regex patterns, keyword lists) |
| 5133–5693 | `Bootstyle` | the resolver: maps `bootstyle`/`style` → built ttk style |
| 5694–5784 | `BootMixin` | ttk `bootstyle` mixin (PR 3) |
| 5785–5809 | `AutoStyleMixin` | tk `autostyle` mixin (PR 3) |
| 5810–5870 | `bootify` / `apply_bootstyle` / `enable_global_api` (+ `_global_api_installed` flag) | delivery primitives (PR 3) |

## The central finding — why this split is safe

**Every cross-class reference inside `style.py` lives in a method body.** No
class uses another as a base class, default-argument value, decorator, or
class-body attribute; the only module-level executable statements are the nine
`class`/`def` definitions and one flag (`_global_api_installed = False`).

Consequence: splitting into submodules cannot create an *import-time* cycle as
long as each submodule's **top-level** `from … import …` statements only point
"downward" in the layering below. The remaining cross-module references (the
"back-edges") are all resolved at call time and become a small, enumerable set
of **function-local imports** — six sites total. Behavior is unchanged; this is
a pure structural move.

## Proposed package layout

```
src/ttkbootstrap/style/
  __init__.py        # public surface: re-exports everything below (keeps
                     #   `from ttkbootstrap.style import …` working unchanged)
  theme.py           # Colors, ThemeDefinition          (L1, lowest)
  builders_tk.py     # StyleBuilderTK                    (L2)
  builders_ttk.py    # StyleBuilderTTK                   (L3)
  engine.py          # Style                             (L4)
  bootstyle.py       # Keywords, Bootstyle, BootMixin, AutoStyleMixin,
                     #   bootify, apply_bootstyle, enable_global_api (L5, highest)
```

Naming follows the plan's target verbatim, except:
- **`theme.py` holds `Colors` + `ThemeDefinition`** now. The semantic-anchor
  `Theme` class + ramp generation (Workstream E) land here later — this is the
  module that grows, but for the move it's just the two existing classes.
- **`Keywords` folds into `bootstyle.py`** (it's the grammar data the resolver
  reads). When Workstream D builds the canonical grammar/parser it may earn its
  own `grammar.py`; not worth a separate module for the move.
- The public **style-construction toolkit** (Workstream I: `assets.py`,
  `layout.py`) is **not** part of this move — see "PR scope" below.

### Why this layer order

Layers are assigned so that the natural, heavy references go *downward* (cheap
top-level imports) and only a few go *upward* (deferred). The bulk of the file —
`StyleBuilderTTK`'s 3700 lines — references `Colors`/`ThemeDefinition`
constantly; putting `theme` at the bottom makes every one of those a plain
top-level import. The few references back *up* to `Style` from the builders and
`Colors`, and from `Style` up to `Bootstyle`, are the back-edges.

## Dependency graph (verified by grep, not assumed)

Top-level (`from . import`) edges — **downward only, import-safe**:

```
bootstyle  ──> engine, builders_ttk, builders_tk   (+ Keywords/mixins are local)
engine     ──> theme, builders_ttk
builders_ttk ──> theme, builders_tk
builders_tk  ──> theme
theme      ──> (colorutils, constants only — leaf)
```

Back-edges — **upward, resolved at call time → function-local import** (the
complete list, 6 sites):

| In module | Site | Needs | Note |
|---|---|---|---|
| `theme.py` | `Colors.get_foreground` (~`324`) | `Style().dynamic_foreground` | only place `Colors` touches the engine |
| `builders_tk.py` | `StyleBuilderTK.__init__` (~`1044`) | `Style.get_instance()` | sets `self.style`; methods use `self.style`/`self.colors` after |
| `builders_ttk.py` | `StyleBuilderTTK.__init__` (~`1382`) | `Style.get_instance()` | same pattern |
| `engine.py` | `Style.update_ttk/tk_widget_style` callers (~`649`, `955`, `957`) | `Bootstyle.*` | engine→bootstyle is the only engine back-edge |

Everything else resolves through instances already on hand: builder methods read
`self.style` / `self.colors` (set once in `__init__`); the resolver reaches the
builders via `Style._get_builder()` (returns the per-theme builder instance) and
`getattr(builder, method_name)`. None of those need a top-level import of the
upward module.

### Import order in `style/__init__.py`

Bottom-up, so each module is fully initialized before a higher one imports it:

```python
from .theme import Colors, ThemeDefinition
from .builders_tk import StyleBuilderTK
from .builders_ttk import StyleBuilderTTK
from .engine import Style
from .bootstyle import (
    Keywords, Bootstyle, BootMixin, AutoStyleMixin,
    bootify, apply_bootstyle, enable_global_api,
)
```

Importing `engine` alone pulls `engine → builders_ttk → builders_tk → theme`
with no cycle; `bootstyle` then sits on top. The function-local back-edges only
fire at runtime, by which point the whole package is imported.

## Per-module top-level imports (from the current header)

So the move reassigns, not rewrites, the imports:

- **`theme.py`**: `colorsys`; `from ttkbootstrap import colorutils`;
  `from ttkbootstrap.constants import *` (uses `LIGHT`/`DARK`). Back-edge: local
  `from ttkbootstrap.style.engine import Style` in `get_foreground`.
- **`builders_tk.py`**: `tkinter as tk`, `font`; PIL bits it uses; constants;
  `from .theme import Colors`. Back-edge: local `Style` import in `__init__`.
- **`builders_ttk.py`**: `tkinter`, `font`, `from math import ceil`, full PIL
  (`Image, ImageColor, ImageDraw, ImageFont, ImageTk, Resampling, Transpose`),
  constants, `from .theme import Colors, ThemeDefinition`,
  `from .builders_tk import StyleBuilderTK`. Back-edge: local `Style` in
  `__init__`. (PIL usage spans up to ~`4973` — all here.)
- **`engine.py`**: `json`, `tkinter/ttk`, `TclError`,
  `from ttkbootstrap.internal import utility as util` (`get_image_name`, ~`987`),
  `from ttkbootstrap.themes.standard import STANDARD_THEMES`, the `USER_THEMES`
  try/except, constants, `from .theme import Colors, ThemeDefinition`,
  `from .builders_ttk import StyleBuilderTTK`. Back-edge: local `Bootstyle`.
- **`bootstyle.py`**: `re`, `tkinter`, `TclError`, constants,
  `from .engine import Style`, `from .builders_ttk import StyleBuilderTTK`,
  `from .builders_tk import StyleBuilderTK`. No back-edges (top layer).

## Back-compat — no shim needed

`ttkbootstrap.style` is a **public import path** used internally by `window.py`
(`Style, Bootstyle`), `widgets/meter.py` (`Bootstyle, Colors`),
`widgets/floodgauge.py` (`Colors, Style`), and `__init__.py` (the eight
primitives) — plus external user code. Turning the module into a package keeps
the path `ttkbootstrap.style` valid; the `__init__.py` re-exports the same names,
so **every existing `from ttkbootstrap.style import X` keeps working** with no
deprecation shim. No `__init__.py`-level monkey business beyond the re-exports.

The new submodules (`style.engine`, `style.builders_ttk`, …) are **new** paths
that never existed publicly, so they carry no back-compat guarantee (treat like
`internal/`). Document that they're implementation detail; don't advertise them.

## Granularity decisions (recommended, not forced)

- **Keep `StyleBuilderTTK` whole** in `builders_ttk.py` for the move. It's one
  class (3700 lines); splitting a single class across files needs a mixin
  decomposition, which is real design churn that belongs to Workstreams I/E (they
  thin it via the asset/layout toolkit and the anchor model), not the move.
- **`engine.py`** (`Style`, ~470 lines) stays one module. The walk/registry and
  the image-cache helpers are all `Style` methods.
- **Don't pre-create** `assets.py`/`layout.py`/`_compat.py` empty. Add them with
  the workstream that fills them (I and D/E/F respectively).

## PR scope — the one open decision

The plan (lines 280–284) suggests landing Workstream I's **Tier-1 toolkit**
(`image_asset`, `layout()`, …) *together* with the split, arguing both touch the
same ~40 asset sites and splitting-then-rewriting is double-churn.

**Counter-point (recommend pure move first):** PR 2 already routed all ~40 sites
through the single `_get_or_create_image` chokepoint, so the sites are *already*
centralized — the double-churn the plan worried about is largely pre-paid. The
toolkit (`image_asset` + shape recipes + a `layout()` DSL) is a **new public API
surface** that deserves its own design pass (like the engine got), and bundling
a from-scratch DSL into a 5.9k-line file move produces a large, hard-to-review
PR that mixes "moved, prove-it-by-tests" with "rewritten, review-every-line."

Recommended sequencing:
1. **G (this PR): pure, behavior-preserving move.** Mechanical diff; the proof
   is "42 tests still pass + every `ttkbootstrap.style` import path unchanged."
   Verifiable by import-path stability and the existing suite.
2. **I (follow-on): the toolkit**, with its own short design pass, wrapping the
   `_get_or_create_image` chokepoint into the public `image_asset` and migrating
   the builders onto `layout()`. Lands in `style/assets.py` + `style/layout.py`.

→ **Decision needed from you** before code moves: pure-move-first (recommended)
vs bundle Tier-1 toolkit into the split.

## Verification plan (for the move PR)

- `python -m pytest -q` → still **42 passed** (the move changes no behavior).
- Assert every legacy import path resolves: `from ttkbootstrap.style import
  Style, Bootstyle, Colors, ThemeDefinition, BootMixin, AutoStyleMixin, bootify,
  apply_bootstyle, enable_global_api` and the internal consumers
  (`window`, `meter`, `floodgauge`) import clean.
- `import ttkbootstrap` stays **warning-free** (no shim added).
- Spot-check no import-time cycle: `python -c "import ttkbootstrap.style.engine"`
  and `… .bootstyle` both import standalone.

## Execution checklist (once scope is signed off)

1. Create `style/` package; move each class to its module per the table.
2. Reassign top-level imports per "Per-module top-level imports."
3. Convert the 6 back-edges to function-local imports.
4. Write `style/__init__.py` re-exports in the bottom-up order above.
5. Delete the old `style.py`.
6. Run the verification plan; update `2_0_handoff.md`.

## Implementation — DONE (2026-06-25)

Scope decision (asked + answered): **pure, behavior-preserving move**; the
Workstream I toolkit follows as its own PR. Implemented on
`feat/2.0-pr4-style-split` off `2.0`. Suite: **61 passed** (was 42; +19 from the
new structural-guard test).

What landed, exactly as designed:
- `style.py` → `style/` package: `theme.py` (Colors, ThemeDefinition, 489 L),
  `builders_tk.py` (StyleBuilderTK, 359 L), `builders_ttk.py` (StyleBuilderTTK,
  ~2.2k L — git tracks the move as a rename here), `engine.py` (Style, 502 L),
  `bootstyle.py` (Keywords, Bootstyle, BootMixin, AutoStyleMixin, bootify,
  apply_bootstyle, enable_global_api, 831 L), `__init__.py` (re-exports, 36 L).
- The 6 back-edges are function-local imports exactly as enumerated (Colors→Style;
  StyleBuilderTK.__init__→Style; StyleBuilderTTK.__init__→Style; engine.configure
  & engine._repaint_widget →Bootstyle ×2). No top-level cycle; each submodule
  imports standalone.
- Per-module imports reassigned; pruned the genuinely-unused (engine: `tk`,
  `ImageTk`, `Colors`; bootstyle: `tk`, `constants *`) verified via pyflakes.
- Public path unchanged: every `from ttkbootstrap.style import …` (window, meter,
  floodgauge, ttkcreator, conftest, __init__, test_mixin_api) resolves with **no
  shim**; `import ttkbootstrap` stays warning-free.
- New `tests/test_style_package.py`: public-surface completeness, legacy
  `from`-import per name, standalone submodule import (cycle guard), consumer
  imports via the public path.

### Notable finding — Python 3.14 / PEP 649 deferred annotations

The dev interpreter is **3.14**, where annotations are evaluated lazily. This
masked a real defect during the move: `builders_tk.py` references
`ThemeDefinition` only in a return annotation (`def theme(self) ->
ThemeDefinition`). The module **imported clean** despite the name being
unimported — the `NameError` only fires when `__annotations__` is accessed. So
the standard "does it import?" check is **insufficient** on 3.14 for catching
missing annotation-only imports. Added a verification step that force-evaluates
every function/method/property annotation across the package + consumers
(`dict(obj.__annotations__)`); it now resolves cleanly. **Carry this check into
future split/move PRs (E/D will move more code).**
