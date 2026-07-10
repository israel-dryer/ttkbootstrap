# ttkbootstrap 2.0 — Surface Color (design pass)

> Design pass for a **surface-color** capability: let any widget be told the
> background surface it sits on, so widgets placed on a non-application-background
> surface (a card, a chrome bar, an accent-colored toolbar) style and render
> correctly. Follows the 2.0 hard rule (design pass before implementation). Pair
> with `2_0_theme_anchor_design.md` (Workstream E), `2_0_bootstyle_grammar_design.md`
> (Workstream D), and `2_0_engine_design.md` (Workstream A).
>
> **Status: CONFIRMED (author sign-off 2026-07-10).** Motivating case + the accept-
> regular-color-tokens requirement raised while running
> `gallery/collapsing_frame.py`. All gating forks resolved: surface = separate
> kwarg (§5.1); minimal named set `background`+`card` (§5.2); auto on-surface
> foreground (§5.3); sigil `@<surface>` — verified safe (§5.4); manual-only /
> auto-inheritance deferred to Phase 2 (§5.5); raw-hex hatch deferred (§9.3).
> Implementation proceeds PR-by-PR per §6. **PR 1 (resolver + `card` token +
> vocab; additive/no-behavior-change) is MERGED into `2.0` (#1149).** Next: PR 2.

## 1. Why this, why now

Every built style today implicitly assumes **widget background == theme
background** (`colors.bg`). The moment a widget sits on a different surface, the
assumption leaks and the widget no longer matches its container. It surfaced
running old `examples/`/`gallery/` demos — most sharply in
`gallery/collapsing_frame.py`:

- The section header `frm` is an **accent frame** (`bootstyle=style_color`, e.g.
  `primary`/`danger`/`success`).
- The toggle button is `f'{style_color}-link'`. The link builder hardcodes
  `background=builder.colors.bg` (`style/builders/button.py:250`, and every state
  map entry `:270-272`), so the button paints the **application** background, not
  the accent frame it lives on. It cannot "ghost" against the toolbar.

The author also added a hairline **border** to the button family (#1096/#1127).
That border is drawn from a bg-derived `bordercolor`; on a non-default surface the
hairline shows against the wrong color, so even the "fake it with a matching bg"
trick no longer works. A true `ghost`/`link`/`outline` button is the right tool —
but today it only ever resolves against the one background, so it can't blend into
anything else.

This is a **correctness gap** in the theming model (visibly wrong rendering on
non-default surfaces), not a new feature — which keeps it inside the 2.0
"no new features" fence. It is cross-cutting (style-name scheme + every affected
builder), so it gets its own design pass like the other workstreams.

**Reference project:** bootstack (`D:/Development/bootstack`) has a mature,
first-class surface/elevation system; we borrow **mechanisms**, not its API
(memory `prefer-bootstack-reference`). Key files cited inline.

## 2. Scope & non-goals

**In scope:**
- A `surface=` keyword on ttkb widgets (via `BootMixin`/`AutoStyleMixin`),
  resolved through a single surface resolver.
- A small set of theme-derived **named surface tokens** (§5.2).
- Surface participating in the **style name** (one namespaced segment, emitted
  only when non-default) and, for free, in the **asset cache key**.
- Builder refactor: the affected `colors.bg` sites (§3) resolve against `surface`.
- Auto **on-surface foreground** so text/glyphs stay legible on the new surface.

**Non-goals (this pass):**
- **Auto/parent-inherited surface.** Bootstack auto-inherits a cached `_surface`
  from the parent, but relies on its constructor monkey-patch — which ttkb 2.0
  retired (PR 3). Explicit `surface=` only for 2.0; parent/container-derived
  surface is a clean **Phase 2 fast-follow** through `BootMixin.__init__` (§7).
- No continuous `[+N]` elevation mini-language (bootstack's `elevate()`); named
  tokens + accent tokens + hex cover the need.
- No new widgets. No bootstyle-grammar vocabulary changes (surface stays orthogonal
  to the closed D vocab).

## 3. Ground-truth: the surface-dependent sites

Confirmed by survey + direct read. Every flat/trough/outline/off-indicator region
pulls the app background from one anchor, `builder.colors.bg`. Representative,
`src/ttkbootstrap/style/`:

**Style options (ttk):**
- **button (solid)** `builders/button.py:66,68,69` — `bordercolor=border(fill)`,
  `dark/lightcolor=fill`. Fill is the *accent*, so surface-independent — **except**
  `neutral`/`default`, whose `neutral_fill` raises from bg.
- **button (outline)** `:175-178` — `background`/`darkcolor`/`lightcolor` = `colors.bg`.
- **button (neutral outline)** `:96-137` — `surface = colors.bg` throughout.
- **button (link)** `:250,270-272` — `background=colors.bg` in configure + all states.
- **button (ghost)** `:298,310-311` — `surface=colors.bg` **and** hover/pressed
  washes are `mute(fg, surface, …)`; surface enters the fill *and* the blend math.
- **checkbutton/radiobutton** — label bg inherited from `.`; off-state indicator
  glyphs recolored `white=colors.bg` (radiobutton.py:51,53).
- **toggle** — `off_track=border(colors.bg)`, style `background=colors.bg`, selected
  map `background=colors.bg`, switch assets `black=colors.bg`.
- **frame** `frame.py:23,28` — `background=colors.bg`.
- **label** `label.py:32,35,…` — `background=colors.bg` (+ inverse variants).
- **scale / progressbar / scrollbar** — trough/surface = `border(colors.bg)` /
  `colors.bg`; slider/handle glyphs recolored `white=colors.bg`.

**Assets (already keyed correctly — no pipeline work):** the recolor glyphs
(`style/assets.py:140` key `("recolor", name, size, white, black, magenta, transform)`)
pass the surface color *as a color channel*, so a different surface yields a
distinct cached PNG with correctly-matched anti-aliased edges automatically. Icon
glyphs render on a transparent canvas (`style/icons.py`) → surface-agnostic. **The
asset half is free**; the work is style-name + builder plumbing only.

## 4. Design

### 4a. The surface resolver (accept named tokens AND regular color tokens)

One entry point on the builder, mirroring bootstack's `color(token)`
(`bootstack/style/style_builder_base.py:117-192`), resolving three input dialects
to a concrete color:

1. **Named surface token** → theme lookup (`background` default, plus the §5.2 set).
   Theme-reactive: re-resolves on theme walk, so it follows light↔dark.
2. **Accent color token** (`primary`/`success`/`light`/`dark`/… — the full
   `BOOTSTYLE_COLORS` vocab) → `colors.get(token)`. **This is the author's
   load-bearing requirement:** a ghost/link/outline button must be able to ghost
   against an accent toolbar (`surface="primary"`), which today is impossible.
3. **Raw hex** (`"#1b1e21"`) → passthrough. A **static** escape hatch — does *not*
   follow theme switches (frozen), unlike named/accent tokens. Documented as such.

### 4b. On-surface foreground (auto)

Changing the surface can strand the foreground (dark text on a dark card, or a
default ghost's `colors.fg` on a `primary` toolbar). The resolver also yields an
**on-surface fg** via the existing contrast helper (`on_color(surface)` /
`colorutils`), used wherever a builder currently reads `colors.fg` for a
surface-relative element. The bootstyle *color* still independently sets the
accent parts — so `bootstyle="light-ghost", surface="primary"` gives light text
on a primary wash, while a bare `surface="primary"` ghost auto-flips its default
`colors.fg` to `on_color(primary)`.

### 4c. Style-name segment (namespaced, readable, non-default only)

Emit **one extra segment**, only when `surface != <default>`, prepended to the
existing `{color}.{Modifier}.{Orient}.{TFamily}` scheme
(`bootstyle.py:_build_ttkstyle_name`):

```
@<surface>.{color}.{Modifier}.{Orient}.{TFamily}
```

e.g. `@primary.info.Ghost.TButton`, `@card.success.TButton`. Raw-hex surfaces
get a short deterministic hash segment (`@a1b2c3.…`), confining opacity to that
one case.

Diverging from bootstack (which hashes the whole options dict → opaque
`bs[a1b2c3d4].success.TButton`): ttkb keeps **readable** names because Workstream
D's whole point is a legible closed vocabulary with a *generated reference table*.

**The segment MUST be namespaced with a sigil.** Surface values overlap the
*entire* color vocabulary (`primary`, `light`, `dark`, …) and even the internal
`card` frame modifier, so a bare segment is ambiguous (`primary.Ghost.TButton` —
is `primary` the bootstyle color or the surface?). The `@` sigil disambiguates and
lets the segment round-trip through the theme-walk's dotted-name parser
(`_classify_style_name` — which we teach to recognize a leading-`@` component as a
surface token). See §5.4 (LOCKED).

### 4d. Live theme switching

Because the surface is encoded as a **token** in the (readable) style name — not a
resolved hex — the version-stamped theme walk (Workstream A) rebuilds the right
style for the new theme automatically: the segment re-resolves to the new theme's
surface/accent color. This is the reason named/accent tokens are the blessed path
and raw hex is only an escape hatch (§4a.3).

### 4e. Frames are surface producers, not consumers

A `ttk.Frame` fills its whole area with its `bootstyle` color, so a `primary`
frame **is** a `primary` surface — for a frame the accent and the surface it
presents to children are the same color. A frame has no transparent halo / flat-
vs-fill tension (it just paints a rectangle), so:

- **`surface=` on a plain frame is redundant** with its bootstyle color — the frame
  *defines* the surface; it does not consume one.
- **Consumers are the non-frame widgets on top of it** (ghost/link/outline button,
  check/radio/toggle, scale) — the ones with edges that must blend. That's where
  `surface=` earns its keep.
- **The one frame that *does* consume a surface is the bordered `card` variant**:
  its hairline border is bg-derived, so a card on a `primary` bar needs
  `surface="primary"` for the border to match. Plain frames don't have this.

This is why bootstack treats frames specially (`CONTAINER_CLASSES = {'TFrame'}`): a
frame *sources* its children's surface from its own accent. That is the **Phase 2**
auto-inheritance hook (§7) — in `collapsing_frame.py` the accent `frm` would hand
`surface=<its accent>` to the ghost button automatically, no `surface=` written.
Phase 1 keeps it explicit; the model is the same: **the frame produces the surface,
the widgets on it consume it.**

## 5. Decisions / gating forks

### 5.1 Surface = separate kwarg, not a bootstyle token — **AGREED**
Folding surface into the bootstyle string would blow open the closed D vocabulary.
Orthogonal kwarg: `bootstyle="success-toggle", surface="card"`.

### 5.2 How large a named surface family? — **LOCKED: minimal (`background` + `card`)**
`background` (default) + `card` (one elevate), derived by lightening/darkening bg
per mode (bootstack `theme_provider.py:305-410`), aligned with the existing `card`
frame variant and `inputbg`. Expandable later; *not* porting bootstack's full 7.
Accent tokens work as surfaces regardless of this set — this fork was only about
the named *neutral* surfaces.

### 5.3 Auto on-surface foreground — **AGREED (auto-derive)**
Derive fg from surface via the contrast helper; otherwise text is unreadable on a
dark card / accent toolbar.

### 5.4 Style-name sigil — **LOCKED: `@<surface>`**
`@primary.info.Ghost.TButton`, `@card.success.TButton`; raw hex → `@<hash>.…`.
Chosen for the small footprint (one char, no extra token). **Verified safe**
(headless, 2026-07-10): `@` is not special in Tcl strings, and a ttk style name
carrying an `@` segment round-trips through `configure`/`lookup`/`map`, the
`-style` widget option, **and** ttk's left-strip dotted-parent inheritance
(`@primary.info.Ghost.TButton` correctly inherits from `TButton`). Tk's `@`
special-casing is confined to font / bitmap-cursor / canvas-index parsers, none of
which style-name resolution invokes → platform-independent (worth an aqua/x11
eyeball in the visual pass, but the resolution path is shared C code). Remaining
work is ttkb-side only: `_classify_style_name` learns a leading-`@` component ==
surface token.

### 5.5 Manual only for 2.0; defer auto-inheritance — **AGREED**
Explicit `surface=` this pass; parent/container-derived surface = Phase 2 (§7).

## 6. Implementation sketch (PR breakdown)

Proposed, PR-by-PR per the 2.0 hard rule:

- **PR 1 — resolver + theme tokens. [MERGED #1149]** Added `resolve_surface`
  (§4a) + `card_surface` (§5.2) on the builder + `BOOTSTYLE_SURFACES`/
  `DEFAULT_SURFACE` vocab. On-surface fg (§4b) reuses the existing `on_color`
  helper — no new API needed, so it lands where builders consume it (PR 3).
  Named-neutral surfaces derive from `colors.bg` in the resolver rather than
  expanding the 16-field `Colors` (avoids rippling every constructor). Unknown
  surface routes through the shared `_compat` strictness gate. No behavior change
  (default surface == `colors.bg`; nothing consumes it yet). Suite 581.
- **PR 2 — style-name segment + kwarg plumbing.** `surface=` on the mixins →
  resolver; namespaced segment (§4c) emitted only when non-default; round-trip
  through `_classify_style_name`; theme-walk rebuild (§4d). Tests: name assembly,
  parse round-trip, default-surface produces today's exact names (no regression).
- **PR 3 — builder migration.** Point the §3 `colors.bg` sites at the resolved
  surface, starting with the button family (the motivating case), then
  check/radio/toggle/frame/label/scale/progressbar/scrollbar. Asset recolor falls
  out for free. Update `gallery/collapsing_frame.py` as the acceptance proof
  (ghost/link button on the accent toolbar). Visual spot-check light↔dark.

## 7. Phase 2 (deferred, not this pass)

Parent/container-inherited surface: `BootMixin.__init__` reads the master's cached
resolved surface (bootstack's `_surface` pattern, `style_resolver.py:271-289`);
container frames (accent or card) source their children's surface from their own
fill. Big ergonomics win, but "spooky action" and a larger mechanism — designed
separately once the manual path is proven.

## 8. Compat / breaking

Additive: `surface=` defaults to the app background, so **every existing style
name and appearance is byte-for-byte unchanged** when `surface` is unset. No
deprecation needed; log a `2_0_breaking_changes.md` entry only if any default
rendering shifts (it should not). New public surface: the `surface=` kwarg + the
named-surface tokens (feed the Workstream-H docs / BootStyle reference).

## 9. Open questions for the author

1. ~~§5.2 named surface set~~ — **LOCKED: minimal `background` + `card`.**
2. ~~§5.4 sigil~~ — **LOCKED: `@<surface>`** (verified safe).
3. ~~Raw-hex surfaces in PR 1?~~ — **LOCKED: deferred.** PR 1/2/3 ship the theme-
   reactive path only (named `card` + accent tokens); the static hex hatch is a
   later PR.