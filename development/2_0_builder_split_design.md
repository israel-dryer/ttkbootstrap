# ttkbootstrap 2.0 — `StyleBuilderTTK` Module Split Design

> Approved and implemented locally (2026-06-28) on
> `refactor/2.0-builder-modules`. This document pairs with
> `development/2_0_plan.md` and the living
> `development/2_0_handoff.md`. The branch is based on `2.0` merge commit
> `080e3d19` after recolorable raster assets merged as #1081.

## Decision summary

Replace the 2,689-line `style/builders_ttk.py` recipe monolith with:

- a small `StyleBuilderTTK` per-theme context/coordinator;
- a private decorator registry keyed by `(variant, widget_family)`;
- an explicitly loaded `style/builders/` package with one module per widget
  family; and
- a deliberately small `builders/utils.py` for helpers used by multiple
  families.

This is a structural refactor. It does not change the bootstyle grammar, ttk
style names, recipe output, public style-construction toolkit, theme lifecycle,
lazy build behavior, or widget visuals.

## Scope and invariants

The following are hard acceptance criteria:

1. `Bootstyle.ttkstyle_name()` returns exactly the same names for every existing
   input, including tuple/list compatibility and the current regex matching
   behavior.
2. Every built-in bootstyle dispatches to the same recipe with the same
   `colorname` value as today.
3. Recipes create, configure, map, lay out, and register exactly the same ttk
   style names and image elements. Recipe bodies are moved, not redesigned.
4. A recipe may build more than the requested name. Horizontal/vertical pairs,
   Treeview body/heading pairs, Calendar chevrons, and other supporting styles
   remain one recipe transaction.
5. Theme creation still eagerly builds the root `.` settings, base `TButton`,
   Link button, base Label, and the existing tableview/tooltip support styles.
   All other styles remain lazy and per-theme.
6. Unknown/unregistered third-party styles still pass through unchanged.
   Exceptions raised *inside a registered recipe* remain visible; they must not
   be mistaken for a missing recipe.
7. `StyleBuilderTTK` remains importable from `ttkbootstrap.style` and continues
   to own the theme/style context, raw configure seam, assets facade, scaling,
   theme setup, dispatch, and combobox-popdown update seam.
8. No new public API is introduced. `style/builders/` and its registry are
   implementation details.
9. `import ttkbootstrap` remains warning-free, and all new modules pass the
   standalone-import and Python 3.14/PEP 649 annotation checks.
10. The visual result is unchanged on light and dark themes.

Out of scope:

- canonicalizing or validating bootstyle grammar (Workstream D);
- semantic theme anchors or state-color changes (Workstream E);
- changing asset templates, glyph choices, dimensions, padding, or colors;
- redesigning recipe signatures around bootstack's style/options model;
- public third-party recipe registration; and
- modularizing `StyleBuilderTK`.

## Current architecture and dispatch

`StyleBuilderTTK` currently contains 36 dispatchable `create_*_style` entry
points plus theme setup, shared helpers, family-local asset builders, and the
combobox popdown updater. Dispatch is convention-based:

1. `Bootstyle.ttkstyle_name(widget, style_string)` parses the existing regex
   grammar and generates the ttk style name.
2. If that name is absent from the active theme,
   `Bootstyle.ttkstyle_method_name(widget, ttkstyle)` converts the parsed type
   and class to a string such as `create_outline_button_style`.
3. `StyleBuilderTTK.name_to_method()` performs
   `getattr(StyleBuilderTTK, method_name)`.
4. `Bootstyle.update_ttk_widget_style()` invokes the unbound method as
   `recipe(builder, widget_color)`.
5. `AttributeError` from the lookup means “not a ttkbootstrap recipe,” so the
   original third-party style is returned unchanged. The recipe invocation is
   outside that `try`, so an `AttributeError` raised by recipe code propagates.

The generated method name is therefore both a routing protocol and an
implementation name. The split removes that coupling while preserving step 1,
step 2's compatibility helper, step 4's effective callable contract, and step
5's fallback semantics.

## Bootstack findings and deliberate differences

Bootstack's `style/builders/` demonstrates the useful mechanism:

- builder functions live in widget-family modules;
- decorators register a `(variant, widget class)` pair;
- the package imports each module to trigger registration; and
- a small builder context invokes the selected function.

The following bootstack behavior will **not** be copied:

| Bootstack behavior | ttkbootstrap design |
|---|---|
| Public/class-level registry API | Private leaf registry module; no re-export |
| Registry nested by ttk widget class | Flat tuple key `(variant, widget_family)` matching the existing parser vocabulary |
| Duplicate keys replace the existing callable | Duplicate keys raise immediately with both callable names |
| Loader catches `ImportError` and all other exceptions, then marks itself loaded | Import failures propagate; loaded state is set only after every explicit import succeeds |
| Recipe gets `(builder, ttk_style, accent, **options)` | Recipe gets `(builder, colorname)` to preserve existing behavior |
| Usually one invocation builds the supplied `ttk_style` | A recipe remains free to build the exact set of related names it builds today |
| Registry participates in bootstack's different style grammar and widget API | Existing ttkbootstrap `Keywords`/`Bootstyle` parsing stays untouched |

The callable difference is important. Passing a generated style name into the
recipes would force rewrites of oriented and compound builders and would risk
changing their registered names. Keeping the current effective contract makes
the move mechanical.

## Proposed package layout

```text
src/ttkbootstrap/style/
  builders_ttk.py          # small StyleBuilderTTK context/coordinator
  builders/
    __init__.py             # idempotent explicit loader only
    registry.py             # private registry/decorator/lookup errors
    utils.py                # only cross-family helpers
    button.py
    calendar.py
    checkbutton.py
    combobox.py
    entry.py
    floodgauge.py
    frame.py
    label.py
    labelframe.py
    menubutton.py
    notebook.py
    panedwindow.py
    progressbar.py
    radiobutton.py
    scale.py
    scrollbar.py
    separator.py
    sizegrip.py
    spinbox.py
    toggle.py
    toolbutton.py
    treeview.py
```

There is intentionally no `misc.py`. Even a small recipe belongs to the widget
family named by its registry key. This keeps lookup, ownership, and future
maintenance aligned.

### Module ownership and exact keys

`"default"` is the private sentinel for an absent bootstyle type. It is not a
new grammar token and never appears in generated ttk style names.

| Module | Registered `(variant, widget_family)` keys | Additional ownership |
|---|---|---|
| `button.py` | `("default", "button")`, `("outline", "button")`, `("link", "button")`, `("date", "button")` | Button layouts and date glyph setup |
| `calendar.py` | `("default", "calendar")` | Calendar body plus Chevron supporting styles |
| `checkbutton.py` | `("default", "checkbutton")` | Checkbox raster states |
| `combobox.py` | `("default", "combobox")` | Popdown updater; requests base Scrollbar recipe |
| `entry.py` | `("default", "entry")` | Entry field recipe |
| `floodgauge.py` | `("default", "floodgauge")` | Horizontal and vertical styles |
| `frame.py` | `("default", "frame")` | Frame recipe |
| `label.py` | `("default", "label")`, `("inverse", "label")`, `("meter", "label")`, `("metersubtxt", "label")` | Label-family variants |
| `labelframe.py` | `("default", "labelframe")` | Labelframe and label substyle |
| `menubutton.py` | `("default", "menubutton")`, `("outline", "menubutton")` | Menubutton caret helper |
| `notebook.py` | `("default", "notebook")` | Notebook and tab layout |
| `panedwindow.py` | `("default", "panedwindow")` | Horizontal/vertical sash styles |
| `progressbar.py` | `("default", "progressbar")`, `("thin", "progressbar")`, `("striped", "progressbar")` | Recolored and striped assets; horizontal/vertical styles |
| `radiobutton.py` | `("default", "radiobutton")` | Radio raster states |
| `scale.py` | `("default", "scale")` | Track/thumb assets; horizontal/vertical styles |
| `scrollbar.py` | `("default", "scrollbar")`, `("round", "scrollbar")` | Thumb assets; horizontal/vertical styles; legacy unused arrow helper stays local during the move |
| `separator.py` | `("default", "separator")` | Horizontal/vertical styles |
| `sizegrip.py` | `("default", "sizegrip")` | Sizegrip glyph/layout |
| `spinbox.py` | `("default", "spinbox")` | Spinbox field and arrows |
| `toggle.py` | `("default", "toggle")`, `("round", "toggle")`, `("square", "toggle")` | Switch raster states; default remains an alias of round |
| `toolbutton.py` | `("default", "toolbutton")`, `("outline", "toolbutton")` | Checkbutton/Radiobutton Toolbutton variants |
| `treeview.py` | `("default", "treeview")`, `("table", "treeview")` | Body and Heading styles |

This table contains all 36 current dispatchable recipe methods. A registry
completeness test will lock it exactly; adding or removing a key later requires
an intentional test and design update.

### Shared utilities

Only two current helpers are demonstrably cross-family:

- `indicator_spacer(builder)` — used by Checkbutton, Radiobutton, and Toggle;
- `simple_arrow_assets(builder, normal, disabled, active, y_offset=0)` — used
  by Combobox, Spinbox, and Menubutton.

They move to `builders/utils.py`. `StyleBuilderTTK.configure()`, `scale_size()`,
and `assets` stay on the coordinator because they are context services used
throughout the package. Progressbar, scale, scrollbar, menubutton, and other
family-specific helpers remain private in their family modules. Visual
similarity alone is not grounds for a new abstraction in this PR.

The currently unused private `create_arrow_assets()` helper is not a shared
utility. It may be renamed module-private while moved, but its deletion is
deferred so this PR does not mix structural work with dead-code cleanup.

## Private registry design

`builders/registry.py` is a leaf: stdlib and typing only. It does not import
`Bootstyle`, `Style`, `StyleBuilderTTK`, tkinter, Pillow, or recipe modules.

Conceptual API (names may remain underscore-prefixed in implementation):

```python
BuilderKey = tuple[str, str]
BuilderRecipe = Callable[[object, str], None]
DEFAULT_VARIANT = "default"

@register_builder("outline", "button")
def build_outline_button(builder, colorname=""):
    ...
```

Registration rules:

- both key parts must be non-empty lowercase strings with no surrounding
  whitespace;
- registration stores the original callable and returns it unchanged;
- the same key may never be registered twice, even to the same callable;
- a duplicate raises a private `DuplicateBuilderError` naming the key, existing
  callable, and attempted callable; and
- the loader freezes the registry after all family imports succeed, so any
  attempted late registration also raises; and
- registry inspection helpers are private and exist only for dispatch/tests.

The registry does not import `Keywords` to validate vocabulary. Doing so would
create an upward dependency on `bootstyle.py`. The exact-key completeness test
is the guard against drift, while runtime keys continue to come from the
unchanged parser.

No custom lock is needed. Tk style construction is main-thread work, Python's
import lock serializes module execution, and the registry is immutable after
the explicit loader completes. Avoiding a lock also avoids bootstack's
load-while-registering deadlock concern.

## Explicit loading and import layering

`builders/__init__.py` exposes one private idempotent loader. The loader contains
an explicit import list for all 22 family modules; there is no `pkgutil`, glob,
filesystem scan, entry point, or implicit naming convention.

```python
def load_builders():
    global _loaded
    if _loaded:
        return
    from . import button, calendar, checkbutton, ...  # explicit, fixed order
    freeze_registry()
    _loaded = True
```

Required failure behavior:

- `_loaded` becomes true only after the complete import list succeeds;
- `ImportError`, duplicate registration, and any other import-time exception
  propagate to the caller;
- the registry freezes only after the complete import list succeeds;
- partial failure is fatal for that operation rather than silently producing a
  partially populated registry; and
- normal repeated calls are no-ops because modules and the loader are cached.

Import graph:

```text
style.__init__
  -> builders_ttk
       -> builders.__init__ (loader definition only)
       -> builders.registry (leaf)
  -> engine
  -> bootstyle

StyleBuilderTTK dispatch/default-theme setup (runtime)
  -> builders.load_builders()
       -> family modules
            -> registry + constants/theme/assets/layout/icons/elements
```

Family modules must not import `engine` or `bootstyle`. They operate through the
builder context passed at call time. They also do not need a runtime import of
`StyleBuilderTTK`; recipe parameters can remain unannotated, matching most
current methods and avoiding an annotation-only cycle. This keeps standalone
imports and the PEP 649 annotation sweep honest.

## Coordinator and callable contract

Final `StyleBuilderTTK` responsibilities:

- bind the process `Style` instance and `StyleBuilderTK`;
- expose `colors`, `theme`, `is_light_theme`, and cached `assets`;
- provide `configure()` and `scale_size()` context services;
- create/use a theme and establish root/default settings;
- translate a parsed key to a registered recipe and invoke it; and
- delegate the combobox popdown update to `builders/combobox.py`.

Every registered callable has the effective contract already used by the
monolith:

```python
def recipe(builder, colorname=DEFAULT) -> None:
    ...
```

`colorname` is passed exactly as returned by
`Bootstyle.ttkstyle_widget_color()`, including `""` when absent. The recipe is
responsible for the same default-to-primary handling it performs today.

The coordinator's private dispatcher returns whether a key exists, or uses a
private lookup exception caught only around lookup. In either implementation,
the critical boundary is:

1. missing key → resolver returns the original third-party style string;
2. found key → invoke the recipe; and
3. recipe exception → propagate unchanged.

Recipes that depend on another recipe use the coordinator dispatcher, not a
cross-family import. The current dependency graph remains:

- default theme setup → default Button, Link Button, default Label;
- default Toggle → Round Toggle; and
- Combobox → default Scrollbar.

Missing recipes on those internal required paths are programmer errors and must
raise, not degrade silently.

## Resolver changes and compatibility

`Bootstyle.ttkstyle_name()`, token lists, regexes, orientation resolution, color
resolution, and style-existence checks remain unchanged.

Only the internal selection step changes:

```text
before: parsed type/class -> method-name string -> getattr(class) -> call
after:  parsed type/class -> (variant-or-default, family) -> registry -> call
```

`Bootstyle.ttkstyle_method_name()` remains available and returns the same string
for compatibility, but production dispatch no longer calls it.
`StyleBuilderTTK.name_to_method()` is removed because its only purpose is the
reflection path.

The 36 `create_*_style` recipe methods become private module-level functions.
They are documented today as internal implementation and the `style.*`
submodules have no compatibility guarantee. The preserved surface is the
importable `StyleBuilderTTK` coordinator, not its recipe-method inventory.

This point should be explicit at sign-off: if “public API unchanged” is intended
to include direct external calls such as
`StyleBuilderTTK().create_outline_button_style()`, thin compatibility methods
would be required. The recommendation is **not** to add them: they would retain
the monolith's method surface and conflict with the agreed removal of
convention-based dispatch. There is no documented public use of these methods;
custom styles use the public `Assets`/`layout` toolkit.

## Preserving lazy theme behavior

Loading Python recipe modules is separate from building Tcl styles. The loader
may run on the first coordinator dispatch, but recipes execute only at the same
points as today:

- `create_default_style()` invokes the three required base recipes during theme
  creation;
- a widget requesting an absent style invokes one recipe on demand;
- `_register_ttkstyle()` records the same names in the global and per-theme
  registries; and
- after a theme switch, the version-stamped widget walk rebuilds only styles
  referenced by mounted widgets in the new theme.

The split must not pre-run every registered default recipe. In particular, it
must not copy bootstack's `initialize_all_default_styles()` behavior.

## Migration strategy

Use one branch and one PR, but keep intermediate commits reviewable and green:

1. Add the private registry/loader and registry tests. During migration only,
   unresolved built-in keys may fall back to the existing reflection path.
2. Move simple families: Frame, Label, Labelframe, Separator, Notebook,
   Panedwindow, and Sizegrip.
3. Move controls: Button, Toolbutton, Entry, Checkbutton, Radiobutton, Toggle,
   and Menubutton; introduce only the two approved shared utilities.
4. Move image-heavy/oriented families: Progressbar, Scale, Scrollbar,
   Floodgauge, Combobox, and Spinbox.
5. Move compound families: Treeview and Calendar; preserve all supporting style
   registrations.
6. Switch `Bootstyle` to registry-only dispatch, remove the temporary fallback,
   `name_to_method()`, and all recipe bodies from `builders_ttk.py`.
7. Run all structural, behavioral, annotation, headless, and visual gates; then
   update the handoff with implementation results.

The temporary reflection fallback is an implementation aid only. It must not be
present in the final PR diff.

## Verification plan

### Registry and dispatch

- Assert the loaded registry key set equals the 36-key table above.
- Assert every registered value is callable and every key is canonical
  lowercase.
- Unit-test empty/invalid keys and duplicate registration using an isolated
  registry instance so global state is not polluted.
- Assert a frozen registry rejects late registration.
- Assert the explicit loader is idempotent.
- Assert an import failure is visible and does not mark the loader complete.
- Parameterize representative grammar inputs to prove generated ttk style names
  and computed keys are unchanged, including default, colored, variant,
  oriented, Toggle, Toolbutton, and Treeview cases.
- Assert an unregistered third-party style returns unchanged.
- Assert an `AttributeError` raised inside a registered test recipe propagates.

### Recipe output and lazy behavior

- Add tests before moving bodies where practical, then run them unchanged after
  the split.
- Assert default theme setup still registers the base styles that must be eager,
  while an unused non-default style remains absent.
- Assert creating a widget lazily builds its style in the active theme.
- Assert switching light↔dark rebuilds mounted styles in the target theme and
  does not eagerly build unrelated registered recipes.
- Assert multi-output recipes produce their complete current sets, preserving
  registration exactly where the current recipe registers it:
  horizontal/vertical Separator, Progressbar, Scale, Floodgauge, Scrollbar, and
  Panedwindow; Treeview body/Heading; Calendar body/Chevron.
- Keep the current recolor/cache/layout tests unchanged. They are the strongest
  headless guard for the six raster-backed families.

### Structural gates

- `import ttkbootstrap` emits no warnings.
- Every new `ttkbootstrap.style.builders.*` module imports standalone.
- The existing style-package cycle guard includes `builders`, `registry`, and
  `utils`, plus every family module.
- Force evaluation of every module/function annotation under Python 3.14 to
  catch PEP 649 annotation-only missing imports.
- Parse all moved modules with Python 3.10 grammar.
- Confirm no production `getattr(..., method_name)`, `name_to_method`, or
  recipe-method reflection remains.

### Runtime gates

- Full headless suite: expected **104 passed** in a complete Tcl environment.
- On the current machine, retain the documented Tcl localization caveat rather
  than weakening tests.
- Human light↔dark smoke check covering: buttons/fields, check/radio/toggles,
  scale/progressbar/scrollbar, Treeview headings, Notebook, Calendar/date button,
  and combobox/spinbox/menubutton carets.

## Risks and controls

| Risk | Control |
|---|---|
| A family module is never imported, so its recipe silently disappears | Explicit import list plus exact 36-key completeness test |
| Two decorators claim the same key | Immediate duplicate error; no replacement |
| Loader failure leaves a partial registry that appears valid | Propagate failure and set `_loaded` only after complete success |
| Missing recipe and broken recipe are conflated | Lookup boundary is separate from invocation; only missing lookup triggers passthrough |
| Default styles become fully eager like bootstack | Keep current `create_default_style()` calls only; test an unused variant remains absent |
| Cross-family helper extraction changes pixels/layout | Extract only arrow/spacer helpers verbatim; all other helpers stay family-local |
| Multi-output recipes are reduced to the requested name | Callable receives `colorname`, not a prescribed single name; assert supporting registrations |
| New import cycle through `engine`/`bootstyle` | Leaf registry, runtime explicit loader, family modules never import upper layers |
| Annotation-only imports fail on Python 3.14 | Force-evaluation sweep across every new module |
| Large mechanical move hides visual drift | Stage family moves, keep recipe bodies unchanged, run headless and human light↔dark gates |

## Sign-off resolution

Approved by the user on 2026-06-28:

1. Treat direct calls to `StyleBuilderTTK.create_*_style()` and
   `name_to_method()` as internal and remove them, while preserving the exported
   `StyleBuilderTTK` coordinator itself. This matches the existing class
   docstring, the prior `style/` split's “submodules are implementation detail”
   decision, and the requested removal of convention-based reflection. No
   compatibility wrappers are retained.

## Implementation — DONE (all gates pass)

- Added private `style/builders/registry.py`: canonical lowercase tuple keys,
  callable validation, duplicate rejection, and a frozen-after-load registry.
- Added an explicit, fail-visible loader plus 22 widget-family modules and
  `builders/utils.py`. Only the shared indicator spacer and caret renderer live
  in `utils`; other helpers remain family-local.
- Moved all 36 recipes mechanically. `StyleBuilderTTK` is now a 161-line
  context/coordinator (down from 2,689 lines) and no longer exposes
  `name_to_method()` or family `create_*_style()` methods.
- `Bootstyle` now dispatches the unchanged parsed type/family through the
  registry. Missing lookup still returns a third-party style unchanged; recipe
  exceptions propagate.
- Added 18 registry/dispatch/lazy/multi-output tests and 25 standalone family
  module cases to the package import guard. Expected suite is now **147 tests**
  (104 + 43).
- Verification: targeted registry/package tests **66 passed**; Python 3.10
  grammar parsed all 35 style modules; warning-free import; 25 fresh-process
  standalone builder imports; forced annotation evaluation covered 222 targets.
- Full local suite: **146 passed / 1 environment failure** because this Python
  3.12 Tcl install cannot read `tk8.6/msgs/nl.msg`. Excluding the six-test
  localization module gives **141 passed**. This is the existing machine caveat,
  not a builder failure.
- Human light↔dark smoke check passed (user, 2026-06-29) across the checklist in
  “Runtime gates.” No source behavior change was observed from the mechanical
  move.
