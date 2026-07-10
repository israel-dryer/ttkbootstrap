# 2.0 compat & utilities — design / scoping note

The last substantive code work before release. Groups a set of **compatibility
fixes** (things 2.0 broke that shouldn't have) and **utility additions**
(long-standing usability gaps) that came out of a design conversation. Each is
small; together they close the "is 2.0 usable as-is / does it answer the FAQs"
gap.

## The boundary rule (applies to every item here)

> **Add utilities that work on vanilla tkinter widgets. Add nothing that
> requires ttkbootstrap to own a widget's behavior.**

This is the precise form of "styling extension, not a widget library." It is the
line that decided every scoping call below: a plain-string `L()` is in, an
`L()`-returns-a-spec (needs a widget mixin to re-resolve) is out; named Tk fonts
are in, a `font="body[bold]"` parser (needs to intercept `font=`) is out. When a
new idea comes up, ask: *does a stock `ttk.Label` benefit from this without
ttkbootstrap intercepting its methods?* If no, it belongs in bootstack, not here.

## Release gate

With these resolved, plus **widgets reviewed** (done), **utilities organized**
(this note), and **docs done** (Workstream H), 2.0 is release-ready. Nothing
below adds a widget; it's compat + utilities only.

## Slice 0 — Utility organization (module + docs)

Utilities are a **first-class** concern in ttkbootstrap in a way they aren't in
bootstack (where widgets are the product), so they get a deliberate home. Two
audiences drive both module layout and docs:

- **App developers** (common): color, fonts, localization, scaling/HiDPI,
  platform, config.
- **Custom-style authors** (advanced): the style-construction toolkit
  (`Assets`/`layout`/`El`/`Icon`/`statespec`/`StyleName`) — already in `style/`,
  stays there, documented separately.

**Module home** — a first-class `utils/` package instead of the current scatter
(`utility.py` grab-bag + `colorutils.py` + soon fonts/config):

```
ttkbootstrap/
  utils/
    __init__.py     # re-exports the public utility surface
    color.py        # <- colorutils.py
    fonts.py        # new (Slice 4)
    scaling.py      # enable_high_dpi_awareness, scale_size   (from utility.py)
    platform.py     # windowing_system                        (from utility.py)
    config.py       # deferred-config seam + setters          (Slice 5)
  localization/     # stays its own package (i18n engine); L/LocaleVar/set_locale
                    #   re-exported through utils + top level
  colorutils.py     # -> thin forwarding shim (warn, remove 3.0)
  utility.py        # -> thin forwarding shim (warn, remove 3.0)
```

- Old public paths (`colorutils`, `utility`) become **forwarding shims** (same
  warn-and-remove-3.0 pattern as `ttkbootstrap.publisher`); no hard break. The
  shims are **source-only back-compat — not documented**; docs present `utils/`
  as the canonical home.
- New utilities (fonts, config) are **born in `utils/`**.
- `localization/` stays put; its user-facing helpers surface through `utils` and
  top level so everything's discoverable in one place without moving the engine.
- Everything stays re-exported at **top level** (`ttk.contrast_color`, `ttk.L`,
  `ttk.set_global_family`) — the primary discovery path via `ttk.<tab>`.

**Docs** — a dedicated **Utilities** reference section mirroring the taxonomy
(one page per concern: Color · Fonts · Localization · Scaling & HiDPI · Platform
· Config), kept **separate** from a **Custom styles** area for the `style/`
toolkit. Same two-audience split as the modules.

This slice lands **first** — Slices 3/4/5 are built into `utils/`.

## Cross-cutting: the deferred-config seam (Slice 5 enables 3 & 4)

Several settings need a Tk root but users want to set them at the top of the file
before `App()` exists (locale, global font, default button). Rather than solve
each with its own chicken-and-egg, a small **pending-apply registry**:

- Pre-root setters (`ttk.set_locale(...)`, `ttk.set_global_family(...)`,
  `ttk.default_button(...)`) record intent into a module-level registry.
- `App.__init__` flushes the registry once the root exists (one ordered hook).
- If a root already exists, the setter applies live immediately.

Same lazy-until-root philosophy as the style builder. Keep it a ~small module,
**not** a config framework. (The theme case does **not** need this — Slice 1's
lazy auto-register already handles it.)

---

## Slice 1 — Theme compat: kill the `install_legacy_themes()` hard-stop

**Problem.** `ttk.Window(themename="darkly")` — the first line of ~every existing
app — raises `TclError`. Legacy names live in `STANDARD_THEMES` but are only
registered by the opt-in `install_legacy_themes()`, which needs a live `Style`,
which needs a root. There is no ordering that fixes this from user code
(`style/engine.py:233`, the `elif themename in STANDARD_THEMES: raise TclError`).

**Fix.** In `theme_use`, when a name is in `STANDARD_THEMES` but not yet
registered, **lazily adapt+register that one theme** (`theme_from_legacy_dict` →
`register_theme`), emit a **one-time `DeprecationWarning`**, and fall through to
the normal build path. Zero user migration; `themename="darkly"` works and still
looks like darkly (plumbing-cleaned).

- Keep `install_legacy_themes()` as the explicit **bulk** register (so
  `theme_names()` / ttkcreator can enumerate the full legacy set).
- Warn once per legacy name (Python's warning dedup handles repeats).

**Rationale.** Matches "prefer deprecation over hard breaks." No 1:1 legacy→2.0
theme mapping exists ("darkly" ≠ "bootstrap-dark", different palettes), so
forcing migration would change every app's colors *and* its code. This
intentionally reverses Workstream E's "opt-in only" decision — that decision is
what created the wall — while preserving its intent (the deprecation nudge).

**Out.** Not changing the default theme: `ttk.Window()` with no name still
renders `bootstrap-light` (a *visual* change, documented in the migration guide,
not a crash).

## Slice 2 — Naming: `App`/`Window` and `theme`/`themename`

Disambiguation, delivered as **additive permanent aliases** (no deprecation
warnings — these are the most-typed identifiers in every existing app).

**`App` canonical, `Window` permanent alias.** `Window` is ambiguous — a
`Toplevel` is also a window. `App` (the one root, paired with the singleton
`Style`) vs `Toplevel` (many) is the clearer split, and it mirrors tkinter's
`Tk`/`Toplevel`.

- Make `App` the real class (`class App(_BaseWindow, tkinter.Tk)`); `Window = App`
  a plain alias, so tracebacks/`type().__name__`/`repr` read `App` while every
  `ttk.Window(...)`, `isinstance(x, Window)`, and subclass keeps working.
- **Not** deprecated — a warning on `Window` would fire in ~100% of apps for a
  naming preference. Docs lead with `App`; `Window` documented as the alias.
- `Toplevel` unchanged (correct tkinter name, already unambiguous).

**`theme` canonical, `themename` permanent alias — on the authored
constructors.** `Style` already uses `theme`; only `Window`/`App` were out of
step. Accept both on `App`/`Window`/`Style` construction; `themename` stays a
permanent, non-deprecated alias.

- **`theme_use(themename)` / `theme_create(themename)` keep `themename`** — they
  override `ttk.Style` methods whose tkinter parameter is literally `themename`;
  keep the Tk spelling for drop-in compatibility. (They're almost always called
  positionally anyway.) This sharpens, not breaks, the naming convention:
  `theme` on authored constructors, Tk spelling on the ttk.Style method overrides.

## Slice 3 — Localization: bug fixes + ergonomic helpers

Bootstack's i18n is a gettext/Babel bridge (the dependency to avoid) and, under
that, makes the **same msgcat calls ttkbootstrap does** — so the value here is
fixing shared bugs and adding two ergonomic helpers, all dependency-free.

**Bug fixes (`localization/msgcat.py`):**
- **`tk.eval(f"...")` → `tk.call(...)`** across `translate`/`set`/`set_many`/
  `load`/`max`/`locale`. The manual `{%s}` brace-wrapping + `.strip('"')` breaks
  on any source string containing `{ } [ ] $` or spaces; `tk.call` passes each
  arg as a proper Tcl value (no quoting, no injection). Deletes `__join`.
- **`preferences()`**: replace `items[0:-1]` (assumes a trailing empty root
  locale that Tcl 8.7 no longer emits — silently drops a real preference) with
  `[p for p in items if p]`.
- **Locale-code normalization** utility (`de-DE`/`pt_br` → canonical) so
  `locale('de-DE')` reliably matches.

**New utility:**
- **`<<LocaleChanged>>` virtual event** emitted on `locale(new)`, so live widgets
  can re-translate. ttkbootstrap has no runtime-relocalize path today.

**Ergonomic helpers (the `L()` ask):**
- **`L(src, *args, **kwargs) -> str`** — short alias for
  `translate(src).format(*args, **kwargs)` (Python `str.format`, sidestepping the
  fragile Tcl `format` path). The universal i18n idiom (`_()`); resolved at call
  time (static — correct for the common "pick locale at startup" case).
- **`LocaleVar`** — a `StringVar` subclass that re-runs its translation on
  `<<LocaleChanged>>`; pass as `textvariable=` for live language switching on
  **vanilla** widgets (rides tkinter's own variable seam).

**Out.**
- Bootstack's **spec-object** model (`L()` returns `LocalizedTextSpec`): needs a
  widget mixin to re-resolve — framework territory.
- **`LV`** (bootstack's "localized *value*" — Babel number/currency/date
  formatting): the dependency being avoided, and a different feature. Do not
  reuse the name `LV` for a variable (collides with bootstack's meaning); the
  live handle is `LocaleVar`.

## Slice 4 — Typography: a tiny `Fonts` utility over the standard Tk named fonts

The FAQ ("how do I change the global font?") has no answer today — widgets read
`TkDefaultFont` / build ad-hoc `font.Font(...)` with no central control. Fix with
a small utility over the **standard Tk named fonts** (`TkDefaultFont`,
`TkTextFont`, `TkFixedFont`, `TkHeadingFont`, `TkCaptionFont`, `TkMenuFont`,
`TkTooltipFont`, …) — no ttkbootstrap font vocabulary, no bracket DSL.

- **`set_global_family(family, *, mono_family=None)`** — retint the proportional
  named fonts (and `TkFixedFont` from `mono_family`). The headline one-liner.
- **`configure(name, **opts)`** — tweak a single named font.
- **`describe()` / `names()`** — return/pretty-print each named font's resolved
  family/size/weight/slant (the "see them" ask).
- **`create_alias(name, **opts)`** — register a user named font (the "font
  aliases" ask), same seam.
- Optional: platform-aware defaults + the macOS pt→pixel size bump (~+2, parity
  with Win/Linux); **`reset()` on `App.destroy`** to clear named fonts bound to a
  dead root (same singleton/root-rebind hazard as `Style`).

**Why Tk named fonts, not a token vocabulary.** They already exist in every
interpreter, every widget reads them, and `font="TkHeadingFont"` works on stock
widgets with zero interception. A parallel `body`/`heading-lg` set would be
overhead to document and sync for no payoff.

**Out.** The token scale as a *new vocabulary*, and the `font="body[bold]"`
bracket DSL (needs to intercept `font=` — framework territory).

## Slice 5 — The deferred-config seam

(See "Cross-cutting" above.) The small pending-apply registry, wired to:
- `set_locale(...)` (Slice 3), `set_global_family(...)` (Slice 4),
  `default_button(...)`.
- Flushed in `App.__init__`; applied live if a root already exists.
- Re-exported as top-level `ttk.set_locale` / `ttk.set_global_family` / etc.

---

## Out of scope for this pass (explicit)

- **A broad `legacy_mode` / "1.x look" flag.** It could only revert the *visual
  defaults* (not the source-level API breaks), would ship two full style paths,
  and gives a false sense of compatibility. The one visual opt-out kept is the
  existing `default_button="primary"`.
- **Source-level breaks stay migration-guide items**, not flags: keyword-only
  constructors, `get_date`→`None`, `IntVar`→`DoubleVar` float returns,
  `Floodgauge.start()` positional meaning, `yview`/`state` return shapes. These
  are documented in `2_0_breaking_changes.md` / the *Migrating to 2.0* guide.
- Spec-object i18n, Babel `LV`, the font bracket DSL, any new font/token
  vocabulary — all fail the boundary rule.

## Suggested PR order

1. **Utility organization** (Slice 0) — `utils/` package + source-only shims; the
   home Slices 3/4/5 build into. **DONE — #1141.**
2. **Theme lazy-register** (Slice 1) — highest impact, unblocks every app; standalone.
   **DONE — #1139.**
3. **Naming aliases** (Slice 2) — `App`/`Window`, `theme`/`themename`; standalone.
   **DONE — #1140.**
4. **Deferred-config seam** (Slice 5 core) — small, enables localization & typography.
5. **Localization** (Slice 3) — msgcat fixes + `L()`/`LocaleVar` + event.
6. **Typography** (Slice 4) — `Fonts` utility, wired through the seam.

(Actual merge order was 1/2/0, all standalone; the remaining three are 5 → 3 → 4.)

Each is a small PR **branched from `2.0`** (not from a feature branch) with its
own tests; each lands an entry in `2_0_breaking_changes.md`. After Slice 4, the
cumulative capstone review runs per `2_0_prerelease_review_plan.md`.
