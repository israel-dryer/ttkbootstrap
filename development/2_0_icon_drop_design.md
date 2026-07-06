# ttkbootstrap 2.0 — Drop the character-based icons (PREREQ) — mini design pass

> Short design pass per the hard rule (a code change that alters widget/dialog
> appearance gets a design gate before implementation). Prerequisite to the
> Workstream-H docs rewrite: it changes dialog-icon appearance, so it must land
> **before** docs screenshots. Pairs with `development/2_0_docs_design.md` §2 and
> the handoff's "PREREQ" note.

## 1. Goal

Remove the legacy `ttkbootstrap.icons` module — a "poor man's", OS-font-dependent,
un-recolorable icon solution — now that 2.0 ships a real Bootstrap-Icons
**font-glyph** engine (`style/icons.py`). Rewire its one real first-party
consumer (Messagebox's default dialog icons) onto theme-matched font glyphs.

This is a **documented breaking change** (removes a public module), tiered as a
2.0 removal (long-obsolete surface, superseded by the glyph engine).

## 2. What `ttkbootstrap.icons` actually contains (ground truth)

The module has **two** distinct payloads, only one of which the docs-design §2
enumeration named:

1. **`Emoji` / `EmojiItem`** — a ~1500-entry unicode-emoji catalog with
   `Emoji.get(name)` lookup. Consumers: `gallery/media_player.py` (6 calls) and
   the frozen `docs/zh/gallery/mediaplayer.md` translation. **No first-party
   runtime consumer.**
2. **`Icon`** — a container of base64-PNG strings. It carries **five** attributes,
   not four:
   - `Icon.info` / `.warning` / `.error` / `.question` — the four dialog alert
     icons. Consumer: `dialogs/message.py` (the four `Messagebox.show_*` defaults).
   - **`Icon.icon`** — the **ttkbootstrap brand logo** (32×32 PNG). Consumer:
     `window.py:318/328` — the default window title-bar/taskbar icon when
     `Window(iconphoto='')`.

**Gap the docs-design missed:** `Icon.icon` (the logo) is *not* an alert icon and
*cannot* become a Bootstrap glyph (it's a brand mark, not a semantic symbol).
Deleting the whole module without preserving it would regress **every**
ttkbootstrap `Window` to the bare Tk feather icon. It must be preserved.

## 3. Decisions

### 3a. The four dialog alert icons → font glyphs (semantic-colored)

Rewire `Messagebox.show_info/_warning/_error/_question` defaults from base64 PNGs
to rendered glyphs via the public `Icon(name, size, color)` atom. Glyph + color:

| method       | glyph                        | color     |
|--------------|------------------------------|-----------|
| show_info    | `info-circle-fill`           | `info`    |
| show_warning | `exclamation-triangle-fill`  | `warning` |
| show_error   | `x-circle-fill`              | `danger`  |
| show_question| `question-circle-fill`       | `info`    |

Strict upgrade: theme-matched, recolorable, DPI-crisp, and it dogfoods the glyph
engine. **Size 30** (matches the old PNGs' 30×30). `question` color = `info`
(a neutral informational query; distinct from a `primary` CTA) — a
**settle-on-the-spot-check** pick like the project's other glyph picks; change by
editing the one call.

### 3b. `create_body` learns a third icon input form (pre-rendered image name)

`MessageDialog.__init__(icon=...)` stays public and keeps accepting **base64 data**
and a **file path** (back-compat for user-supplied icons). The four defaults now
pass a **Tk image name** (what `Icon()` returns). `create_body` gains a leading
branch that uses an existing image name directly, falling through to the existing
data → file cascade:

```python
# try, in order: an already-rendered Tk image name → base64 data → file path
for build in (
    lambda: ttk.Label(container, image=self._icon),
    lambda: ttk.Label(container, image=ttk.PhotoImage(data=self._icon)),
    lambda: ttk.Label(container, image=ttk.PhotoImage(file=self._icon)),
):
    try:
        icon_lbl = build()
        break
    except Exception:
        icon_lbl = None
```

`ttk.Label(image=<not-an-image-name>)` raises `TclError` immediately, so a base64
string cleanly falls through to the data branch — the three forms stay
unambiguous with no string sniffing. The engine's content-addressed cache holds a
strong ref to the glyph image, so no GC pin is needed on `self`. (The old code
kept `self._img`; the data/file branches still bind it so user PhotoImages stay
referenced.)

### 3c. The brand logo → a private constant in `window.py`

Move the `Icon.icon` base64 blob to a module-private `_DEFAULT_ICON_DATA` string
in `window.py` (its only consumer). No new module: the `internal/` convention is
for *shared* plumbing; a single-consumer literal belongs next to its use. The two
`Icon.icon` sites become `_DEFAULT_ICON_DATA`. Appearance unchanged.

### 3d. `Emoji` — deleted, no replacement

No first-party runtime use. `gallery/media_player.py` is updated to inline the
literal unicode characters `Emoji.get(...)` returned (6 media-control glyphs), so
the example stays runnable. The frozen `docs/zh/gallery/mediaplayer.md` is left
as-is (zh is untouched for 2.0 per docs-design; Gallery is being removed anyway) —
recorded as a known-stale zh page for the docs sweep.

## 4. Change list

- **Delete** `src/ttkbootstrap/icons.py`.
- **`window.py`**: drop `from ttkbootstrap.icons import Icon`; add private
  `_DEFAULT_ICON_DATA` (the logo base64); repoint the two `Icon.icon` sites.
- **`dialogs/message.py`**: drop `from ttkbootstrap.icons import Icon`; the four
  `show_*` defaults render a glyph via `ttk.Icon(<glyph>, 30, <color>)`; extend
  `create_body` per 3b; fix the `icon` docstring (drop the "Icon constant"
  mention).
- **`gallery/media_player.py`**: inline the 6 literal emoji chars; drop the import.
- **Tests** (`tests/`): (a) `import ttkbootstrap.icons` raises `ImportError` and
  neither `Emoji` nor a character `Icon` is importable from it; (b) `ttk.Icon` is
  the glyph atom and the four dialog glyph names render to valid Tk images;
  (c) a `MessageDialog` given a pre-rendered glyph image name builds an icon
  `Label` via `create_body` (3b's new branch); (d) `_DEFAULT_ICON_DATA` yields a
  valid `PhotoImage` under the shared root. `import ttkbootstrap` stays
  warning-free.

## 5. Migration entry (for Workstream-H "Migrating to 2.0")

> **`ttkbootstrap.icons` removed.** The `Emoji`/`EmojiItem` catalog and the
> `Icon` base64 constants (`Icon.info/.warning/.error/.question`) are gone. Dialog
> icons now render from the built-in Bootstrap-Icons font (theme-matched and
> recolorable) — no code change needed for the standard `Messagebox` dialogs. If
> you referenced an emoji via `Emoji.get(...)`, paste the literal emoji character
> instead. For a themed glyph in your own widgets, use `ttk.Icon(name, size,
> color)`.

Record this in the handoff so the docs PR folds it in (no standalone migration
doc exists yet beyond theme).

## 6. Out of scope

- Re-theming the media-player example's controls onto Bootstrap glyphs (it keeps
  literal emoji — a runnable example, not a showcase).
- Any change to the glyph engine (`style/icons.py`), the caret/date/sizegrip
  glyphs, or the `Icon`/`icon_element` public surface — all unchanged.
