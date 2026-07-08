# ttkbootstrap 2.0 — Theme-aware icons (design pass)

> Design pass for closing the **inline-icon theme-awareness gap**: an icon placed
> on a widget instance today bakes its color once and goes stale on a theme
> switch. Follows the 2.0 hard rule (design before implementation). Pair with
> `2_0_icons_design.md` (the icon engine), `2_0_engine_design.md` (the no-`Publisher`
> theme walk), and `CLAUDE.md`.
>
> **Status: CONFIRMED (author sign-off 2026-07-07).** Worked out interactively;
> all three §7 forks resolved (states=: include; datepicker: migrate now;
> unsupported widgets: raise). Implementation proceeds per §5.

## 1. Why this, why now

The icon engine (`style/icons.py`, PR 6a/6b) delivers glyphs two ways:

- **Style-delivered** — `icon_element`/`assets.icon` called inside a
  `@register_builder` recipe (checkbox, radio, toggle, date button, carets,
  sizegrip). The 2.0 theme walk rebuilds each mounted widget's `(theme, style)`
  on `theme_use`, which re-runs the recipe and **re-renders the glyph in the new
  theme's colors**. These are theme-aware, automatically.
- **Inline** — `image=ttk.Icon(name, size, color)` set on a widget instance
  (what a user reaches for, and what `dialogs/datepicker.py` does for its header
  carets). `Icon` resolves the color **once** (its docstring says so) and returns
  a bare image name; the walk repaints the widget's *style* but never touches the
  widget-level `-image`. **These are not theme-aware.**

So a user writing `ttk.Button(image=ttk.Icon("gear", 16, "primary"))` sees the
glyph keep its old color after a theme switch. The image cache is content-addressed
and keyed on the resolved color (`engine.py`), and is **not** cleared on
`theme_use`, so nothing breaks — the widget just points at a stale-color image.
The only fix today is the user binding `<<ThemeChanged>>` themselves (the
`Meter`/`Floodgauge` pattern) — undiscoverable.

This is a **gap in an existing 2.0 feature**, not a net-new capability, so it fits
the "no new features" rule as *completing* the `Icon` theme story.

## 2. Ground truth (verified 2026-07-07)

- `Icon(name, size, color)` (`style/icons.py`): resolves color once; "no auto-follow
  on a later theme switch (a re-render is the engine's job, or a fresh call)."
- The image cache (`Style._image_cache`, `_get_or_create_image`) is keyed on the
  resolved color + scaled size + geometry; **never cleared on `theme_use`**. So
  identical-color glyphs dedupe across styles *and* themes and render exactly once.
- `theme_use` calls `super().theme_use()`, so Tk fires `<<ThemeChanged>>` to **every**
  widget natively. Exactly three first-party widgets rely on it today:
  `meter.py:336`, `floodgauge.py:149,607` — the blessed pattern for widgets that
  own visuals outside the ttk style system.
- The theme walk (`engine.py:_theme_walk`) DFSes `winfo_children()`; it has known
  reachability holes (the combobox popdown is repainted out-of-band because the
  DFS can't reach it).
- `icon_element(style, name, ...)` (`style/icons.py`) already **augments an existing
  style**: a bare-string per-state spec renders the glyph in the color the style's
  `foreground` map defines for that state (`_state_foreground`). This is the
  mechanism we build on — not a new approach.

## 3. Decisions

### 3.1 Mechanism = per-widget `<<ThemeChanged>>` bind (not the engine walk)

The re-render is triggered by binding `<<ThemeChanged>>` **on the widget**, in the
apply helper; the handler rebuilds the icon in the new theme. Chosen over threading
icon logic through the engine's theme walk because:

- **Zero engine change** — the theme walk is delicate, carefully-tuned code.
- **No reachability caveat** — Tk broadcasts `<<ThemeChanged>>` to every widget;
  the walk's DFS does not reach everything (see the popdown).
- **Leak-free** — a widget-scoped binding is auto-removed by Tk on destroy; no
  registry, so it does not reintroduce the `Publisher` leak class 2.0 deleted.
- It's the **already-blessed pattern** (`Meter`/`Floodgauge`).
- Redundant rebuilds across many identical icons are **cheap**: the content-addressed
  image cache renders each unique glyph once; extra rebuilds just re-reference the
  cached bitmap.

The bind is added **only** on the themed path (`apply_icon`/`icon=`), never for a
static `Icon(...)`.

### 3.2 Layering = three tiers, split by intent

| Tier | Surface | Behavior |
|---|---|---|
| 1 | `Icon(name, size, color)` | Static image, explicit color, **no style, not themed**. The escape hatch for "a raw glyph, my color, don't manage it." |
| 2 | `apply_icon(widget, name, ...)` + mixin `icon=`/`icon_size=` | **Themed + stateful.** Follows the foreground; **always** generates/reuses a derived style; binds `<<ThemeChanged>>`. No color param. |
| 3 | `icon_element(style, name, ...)` | Full per-state control incl. explicit `{name, color}` specs. For authoring custom styles. |

### 3.3 The sugar follows the foreground — no `icon_color`

Tier-2 has **no color parameter**. The glyph color is always derived from the
style's per-state `foreground` map, which is what makes every case correct by
construction:

- **Invert** (outline/toggle: accent text on surface at rest → on-accent text on
  accent fill when active) — the glyph flips to the contrast color exactly when the
  fill appears, because it follows the same `foreground` map.
- **Disabled** — glyph goes muted (the disabled foreground).
- **Hover/pressed** — follows whatever the foreground map does.
- **Theme change** — re-derived from the new theme's foreground.

A pinned color would re-break the inverting case (accent-on-accent → invisible), so
it is deliberately excluded from the sugar. Needs:

- *A fixed/odd color, unmanaged* → tier 1 (`Icon(...)` as `image=`).
- *Explicit per-state colors* (e.g. accent-when-selected, as the built-in radio-on
  does) → tier 3 (`icon_element`, which keeps `{name, color}`).

### 3.4 `icon=` always generates a style (consistency over minimizing)

Tier 2 **always** ensures a derived style exists — it never falls back to a bare
`-image` "shortcut" for the simple case. Rationale: a sometimes-`-image`,
sometimes-style split is confusing and makes behavior depend on invisible
conditions. One consistent rule ("`icon=` → a themed style") is clearer, and it is
essentially free (§3.1: the image cache means "a new style" rarely means "a new
render", and identical images serve multiple themes when the resolved color
matches). The `-image`-only path remains available, but only via the **explicit**
tier-1 `Icon(...)` — so the two are separated by user intent, not by a hidden
heuristic.

### 3.5 Naming = snake_case (project convention, recorded separately)

Authored identifiers are snake_case (`apply_icon`, `icon_size`); Tk pass-through
option names stay verbatim (`compound`, `size`); `bootstyle`/`autostyle` are
grandfathered brand tokens and are **not** a template for new names. (The general
rule is recorded in `CLAUDE.md` Conventions + memory `naming-convention`.)

## 4. API spec

```python
def apply_icon(widget, name, *, size=16, states=None, compound=None) -> str | None:
    """Put a theme-aware Bootstrap Icons glyph on `widget`.

    Unlike a bare `Icon(...)` used as `image=`, this tracks the active theme and
    the widget's states: the glyph color follows the widget's style `foreground`
    (so it inverts on outline/toggle, mutes when disabled, and re-colors on a
    theme switch). It does so by ensuring a derived style exists on the widget
    (see "What this does to your widget's style"). `name=None`/"" removes it.

    Parameters:
        widget:    any ttk widget with an image-bearing layout (Button, Label,
                   Menubutton, Checkbutton, Radiobutton, ...).
        name:      a Bootstrap Icons glyph name; None/"" clears the icon.
        size:      logical UI size (converted by the root-bound scaling service).
        states:    optional {state_string: glyph_name} to show a *different glyph*
                   per state (color still follows the foreground). Advanced.
        compound:  the ttk `-compound` option (icon/text arrangement) if the
                   widget also has text.

    Returns the resolved (derived) ttk style name, or None if the icon was cleared.
    """
```

Mixin sugar on the blessed widgets (`BootMixin`):

```python
ttk.Button(master, text="Settings", icon="gear", icon_size=18, bootstyle="primary")
```

- `icon=` / `icon_size=` are intercepted by the mixin and routed to `apply_icon`
  **after** `bootstyle`/`style` resolve, so the derived style inherits the right base.
- Re-exported top level: `ttk.apply_icon`.

### 4.0 Supported widgets

`icon=`/`apply_icon` works on ttk widgets whose layout has a **label element that
honors the style `image` option + `compound`** — verified empirically (a derived
dotted style inherits the base layout/config/map via ttk fallback, and a style
`image` + per-state `image` map render through the existing `*.label` element,
exactly like the built-in date button):

- **In scope:** `Button` (incl. Outline/Toolbutton/link/ghost variants), `Label`,
  `Menubutton`, `Checkbutton`, `Radiobutton` (icon on the *label*, alongside the
  indicator — it does not replace the check/radio box).
- **Out — no label image:** `Entry`, `Combobox`, `Spinbox`, `Progressbar`, `Scale`,
  `Scrollbar`, `Separator`, `Sizegrip`, `Panedwindow`, `Frame`, `Labelframe`.
- **Out — per-item image API instead:** `Treeview` (`item(image=)`/`heading(image=)`)
  and `Notebook` (`add(image=)`) support images only per row/tab, a granularity
  `icon=` cannot address; they keep their own image parameter.

Setting a style `image` on an unsupported widget **silently no-ops** at the Tcl
level (its layout has no consuming element — no error is raised). So `apply_icon`
cannot rely on a Tcl failure: it checks the widget class against a **supported
allowlist and raises a clear `TypeError`/`ValueError`** otherwise (resolves §7.3).

### 4.1 What this does to your widget's style (the explicit contract)

`icon=`/`apply_icon` is *implicitly* a style operation — this section is the loud
documentation §1's gap analysis called for.

- **It augments your current style, never replaces it with a from-scratch one.**
  The generated style is `Icon<hash>.<your current style>` (e.g.
  `Icon<hash>.primary.Outline.TButton`, or `Icon<hash>.MyCustom.TButton` for an
  explicit `style=`). Config, state map, **and layout** all **inherit** via ttk's
  dotted-name fallback (verified: a derived name resolves the base's full layout,
  incl. its `*.label` element). We add only the `image` config + per-state `image`
  map on the derived style — the inherited label element renders it. So even a
  custom-layout `style=` is preserved; the icon'd widget matches its non-icon'd
  siblings exactly.
- **`widget.cget("style")` changes** to the derived name. Code that introspects or
  scripts the style will see the hash.
- **Content-hashed, so widgets dedupe.** The hash is over
  `(base style, glyph name, size, states)` — N identical `icon="gear"` primary
  buttons share **one** derived style; the count is bounded by config variety, not
  widget count.
- **`bootstyle`/`style` and `icon` compose and re-derive together.** Changing the
  base (`bootstyle=`/`style=`) regenerates the derived style on the new base; the
  mixin does this automatically. A user who manually `configure(style=...)`s *after*
  `icon=` replaces the derived style and **drops the icon** — documented.
- **Removal restores the base.** `apply_icon(widget, None)` / `icon=None` drops the
  derived style and returns the widget to its plain base style.
- **Customize the base, not the hash.** `Style.configure("primary.Outline.TButton",
  ...)` flows through by inheritance. The generated hashed style has an unstable name
  and is rebuilt on theme change — don't hand-edit it.

### 4.2 Mechanism detail

- On apply: read the base style's `foreground` state map (`style.map(base,
  "foreground")`) to enumerate the distinct states; render one glyph per state in
  that state's foreground color; set them on the derived style via
  `style.configure(derived, image=<rest>)` + `style.map(derived, image=[(state,
  img), ...])` (the inherited `*.label` element renders them — the date-button
  pattern, no custom element/layout needed); set `compound`;
  `widget.configure(style=derived)`.
- Bind `<<ThemeChanged>>` on the widget → rebuild the derived style for the new
  theme (idempotent: guard with `style_exists_in_theme` before `element_create`,
  exactly as the built-in recipes do; A→B→A cycles must not double-create). Store a
  single funcid so repeated `apply_icon` calls **replace**, never stack, the bind.
- Track the icon spec + base on the widget (e.g. `widget._tb_icon`) so the mixin's
  `bootstyle`/`style` setter can re-derive.

## 5. Scope & PR sequence

- **PR — theme-aware icon primitive + sugar.** `apply_icon`, the `icon=`/`icon_size=`
  mixin kwargs, top-level re-export, the derived-style + `<<ThemeChanged>>`
  machinery. Migrate the **datepicker** header carets onto it as first-party
  dogfooding (they have the same latent staleness if the theme changes while the
  modal is open). Headless tests: apply an icon, switch theme, assert the widget's
  `-image`/derived style re-renders to the new-theme color; assert `bootstyle`+`icon`
  compose; assert removal restores the base; assert the inverting (outline/toggle)
  case renders on-accent when active. Human spot-check: an icon button through a
  light↔dark switch, plus an outline/toggle icon button.
- **PR (follow-on) — Tableview pagination buttons on icons.** Ghost base + glyph via
  the same path (their disabled first/prev arrows get muting for free). Own small PR.
- **Docs (Workstream H).** §4.1 becomes a "Theme-aware icons" How-To/Guide section;
  the `Icon` vs `icon=` vs `icon_element` three-tier split is the teaching frame.

## 6. Compat

- Purely additive public surface (`apply_icon`, `icon=`/`icon_size=`); no existing
  signature changes. `Icon(...)` is unchanged (still the static escape hatch).
- `import ttkbootstrap` stays warning-free.
- Datepicker migration is internal (no API change).

## 7. Open questions — all RESOLVED (author, 2026-07-07)

1. **`states=` in v1 → INCLUDE.** The per-state *glyph* override ships in v1 (a thin
   pass-through to `icon_element`'s `states`; color still follows the foreground).
2. **Datepicker in this PR → YES.** Migrate its header carets onto `apply_icon` as
   first-party dogfooding.
3. **Non-image-bearing widgets → RAISE.** An unsupported widget silently no-ops at
   the Tcl level, so `apply_icon` class-checks against the §4.0 allowlist and raises.
