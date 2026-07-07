# ttkbootstrap 2.0 — neutral-by-default buttons — design / scoping

> Design pass per the hard rule (a breaking default change). Builds on
> `development/2_0_neutral_color_design.md` (the `neutral` color itself, merged in
> #1096). Decision locked with the author 2026-07-06: **neutral by default**,
> breaking, with a **construction-time opt-out** to restore the primary default.

## 1. Decision

A bare `ttk.Button()` (no `bootstyle`) currently renders **primary** (blue). Make
it render **neutral** — the quiet, theme-adaptive fill. You opt *into* an accent:
`ttk.Button(bootstyle="primary")`. This matches Bootstrap/bootstack semantics (a
plain button is not a call-to-action) and suits ttkbootstrap's utility/scientific
audience, who generally want a calm default rather than a blue CTA.

This is a **documented breaking change** (Visual): every existing app's bare
buttons change from blue to neutral gray. Justified for an aggressive 2.0, paired
with a one-line opt-out.

## 2. Scope — which widgets flip

Flip only the widgets where the default accent is *emphasis*, not *selection*:

- **`ttk.Button`** (base `TButton`) — flips to neutral. The core case.
- **`ttk.Menubutton`** (base `TMenubutton`) — flips too, for "default buttons are
  neutral" coherence (a dropdown trigger is a button). *(Open Q — see §6.)*

Explicitly **NOT** flipped (their default accent is the *selection indicator*, and
a neutral selection reads poorly):
- **Toolbutton**, **Toggle/switch**, **Checkbutton/Radiobutton** — the accent is
  the "on"/selected color; keep `primary`.
- **Date button** (DateEntry) — an internal affordance inside a compound widget,
  not a bare button the user creates; keep `primary`.
- **Link button** — already flat/text; unaffected.

## 3. Mechanism — construction-time, not a runtime toggle

The default is resolved when the base `TButton`/`TMenubutton` style is built (in
`StyleBuilderTTK.create_default_style` → `build_button_style(DEFAULT)`), which runs
once at theme load inside `Style.__init__`. So the setting must be known before
then and is read at build time — no mutable global that later changes what
`bootstyle=""` means (the hidden state 2.0 has been removing).

- **`Style` gains `default_button` (a color name, default `"neutral"`).** Set at
  the very top of `Style.__init__`, before `create_theme()`/`create_default_style()`
  run, so the base styles pick it up. Persists on the instance, so a later
  `theme_use()` (which rebuilds base styles) keeps the choice.
- **`Window(default_button="primary")`** threads the value into its `Style(...)`
  construction. `Style(themename, default_button="primary")` for `tk.Tk()` users.
- **`build_button_style` / `build_menubutton_style` DEFAULT branch** resolves the
  fill from `style.default_button` instead of hardcoding `colors.primary`:
  `neutral_fill(builder)` when it is `"neutral"`, else `colors.get(default_button)`.
  (Generalizes cleanly — `default_button` is just a color name; `"neutral"` is the
  new default value.)
- **Explicit styles are unaffected**: `primary.TButton`, `secondary.TButton`, etc.
  build exactly as today; only the *base* (no-color) style changes.

Opt-out to restore the 2.x look:
```python
app = ttk.Window(default_button="primary")   # bare buttons render primary again
```

## 4. Compatibility & migration

- **Dialogs are safe.** `MessageDialog.create_buttonbox` sets `bootstyle="primary"`
  on the default/CTA button and `"secondary"` on the rest — all explicit — so
  dialog emphasis is unchanged by the flip.
- **Native/third-party ttk buttons** (e.g. inside Tk's file dialog) fall back to
  the base `TButton`, so they become neutral too — consistent, not a regression.
- **Migration entry** (→ `2_0_breaking_changes.md` + Migrating-to-2.0): "Bare
  `ttk.Button()`/`ttk.Menubutton()` now render **neutral** instead of primary. Add
  `bootstyle="primary"` for a call-to-action, or pass
  `Window(default_button="primary")` to restore the old default globally."

## 5. Test impact

- `tests/widget_styles/test_default_button_style.py` (#1062) asserts the base
  `TButton` background `== colors.primary`; update it to assert the neutral fill by
  default, and add a case that `Style(default_button="primary")` restores primary.
- Add: bare button is neutral by default; `default_button="primary"` opt-out;
  explicit `primary.TButton` unchanged; the base style follows a theme switch.
- Sweep for internal bare-button assumptions (grep the suite for `TButton`
  background == primary).

## 6. Resolved (author, 2026-07-06)

- **Menubutton inclusion — YES.** Flip both `TButton` and `TMenubutton`.
- **Toolbutton — NO** (and Toggle/Checkbutton/Radiobutton). Their default accent
  is the *selection* signal, and they are **already neutral at rest** after the
  bootstack on/off work (OFF = `neutral_fill`, ON = accent). Flipping the ON state
  to neutral would only *remove* the selection color, not make them calmer. So
  they keep primary-on-select; the neutral toolbutton stays an explicit opt-in.
- **Param name — `default_button`** (a color name, default `"neutral"`; more
  flexible than a bool, reads as "the color a default button uses").
- **`Style` singleton timing** — if an app constructs `Style()` *after* `Window`
  already created the singleton, the later `default_button` is ignored (existing
  singleton behavior). Document: set it on the `Window`/first `Style`.

## 7. PR plan (one PR)

Single small PR: the `Style.default_button` plumbing + `Window` param + the two
DEFAULT-branch reads + tests + migration note. Gate on a light↔dark eyeball of a
few bare buttons and one `default_button="primary"` app.
