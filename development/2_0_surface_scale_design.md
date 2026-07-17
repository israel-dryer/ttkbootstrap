# 2.0 — Surface elevation scale + frames as surface consumers

Small follow-on to the 2.0 surface-color work (the `@surface` grammar). Two
changes, settled in a live design discussion:

## 1. A named elevation scale: `background` < `chrome` < `card`

The surface tokens now form a mode-aware elevation scale — each a step off the
window background (`shade` in a light theme, `tint` in a dark one), so a surface
reads as progressively more separated from the base content:

| token        | elevation | role                                             |
|--------------|-----------|--------------------------------------------------|
| `background` | 0         | the app canvas / main content (the default)      |
| `@chrome`    | 0.03      | recessive app framing: toolbars, status bars     |
| `@card`      | 0.06      | a distinct raised panel (the ceiling)            |

`card` stays the ceiling — past ~0.06 a flat theme reads muddy. `chrome` is
deliberately subtler than `card`: the deciding rule is **nesting** — a card can
sit *on* chrome (a panel inside a sidebar) and must still read as raised, while
chrome never sits on a card. So `card` out-contrasts `chrome`.

Concrete (light): `#ffffff → #f7f7f7 → #f0f0f0`; (dark): `#212529 → #282c2f →
#2e3236`. Implemented as `_CHROME_ELEVATION`/`_CARD_ELEVATION` +
`_elevated_surface(elevation)` in `style/builders_ttk.py`; `chrome_surface()`
joins `card_surface()`; `resolve_surface` handles `"chrome"`. Vocab: `chrome`
added to `BOOTSTYLE_SURFACES` in `constants.py`.

## 2. Frames consume a surface (a container that *is* a surface)

Previously frames were excluded from `_SURFACE_FAMILIES` — "surface producers,
not consumers." But there was then **no way to make a container render as a
given surface**: `bootstyle="card"` is the border-only `Card.TFrame` (background
= window bg), and `@card` was silently dropped on a frame. So a sidebar/panel
could not take the elevation surface, and the grammar docs' own example put a
`@card` button (blend `#f0f0f0`) on a `card`-variant frame (bg `#ffffff`) — a
mismatch.

`frame` is now in `_SURFACE_FAMILIES`, and the default frame recipe
(`style/builders/frame.py`) resolves `self._surface` for its background and
`surface_prefix`es its style name, mirroring the label recipe. So:

- `ttk.Frame(app, bootstyle="@card")` → `@card.TFrame`, filled with the card
  surface — a sidebar/panel on the scale.
- `ttk.Frame(app, bootstyle="@chrome")` → the recessive framing surface.
- `@surface` composes with a color (`@chrome primary` → `@chrome.primary.TFrame`).

Border and surface stay **orthogonal**: the `card`/`highlight` frame *variants*
(the hairline border, used internally by ScrolledText/datepicker) are untouched
and remain internal. A bordered card on a surface would be `card @card` once the
variant honors surface too — deferred; not needed here.

## Not done (deliberately)

- No rename of the internal `card`/`highlight` frame **variant**. The
  variant-vs-surface name clash only surfaced when the `card` variant was exposed
  in user docs; the docs now use the `@card` *surface* instead, so users never
  see the clash. Renaming the internal token is optional cleanup for later.
- `labelframe` not added as a surface consumer yet (no driver).

## Tests

`test_surface_color.py` (chrome rung), `test_surface_families.py` (frame in the
gate), `test_surface_grammar.py` (frame consumes surface + composes with color).
Reference regenerated via `tools/generate_bootstyle_reference.py`. Suite green.
