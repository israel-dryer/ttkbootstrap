# 2.2 changes

Scope: changes relative to **2.1.1**. Log entries here as they land, not at
release time.

---

## Added

### `python -m ttkbootstrap.convert_theme` — carry a 1.x custom theme forward

A custom theme saved by ttkbootstrap 1.x now converts to the 2.x
`Theme(...).register()` form with one command:

```bash
python -m ttkbootstrap.convert_theme user.py -o brand.py
```

It reads either input a 1.x user could be holding:

- a **`user.py`** containing a `USER_THEMES` dict — what 1.x ttkcreator's
  **Export** button produced (it copied the in-package `themes/user.py`), and
  the file most people will actually have;
- a **JSON** file in the `Style.load_user_themes` format.

Every theme in the file converts, under a single `import`. Output goes to
standard output, or to `-o <file>`.

**What carries over:** the five accent anchors, the optional `secondary`, and
the theme's `background`/`foreground`.

**What does not, deliberately:**

- The plumbing colors — `border`, `inputbg`, `inputfg`, `selectbg`, `selectfg`,
  `active` — are dropped, because 2.x derives them from the anchors. This is the
  same regeneration `theme_from_legacy_dict` applies to the built-in legacy
  themes.
- The opposite mode. A 1.x theme declares one mode, so the generated family
  declares that one and leaves the other commented out rather than inventing
  colors for it.

Converted output is close but not pixel-identical: an accent is re-derived per
mode for contrast, so a dark theme's authored `#6a5acd` resolves to `#887bd7`.

The module is pure text transformation — no Tk, no display, importable and
runnable headlessly. `tests/test_convert_theme.py` (+13) covers both input
formats, the loud-failure paths, and an end-to-end check that the emitted
Python actually registers a theme and styles real widgets.

## Documentation

- **Migrating to 2.0** gained *Saved themes move into your code*: the
  `themes/user.py` store and ttkcreator's Import/Export buttons are gone, the
  converter command, what carries over vs. what 2.x regenerates, and a note
  that `Style.load_user_themes` still reads the 1.x JSON (thinner — verbatim
  plumbing, single mode, nothing for `toggle_theme()` to flip to).
  This removal shipped in 2.0 but was never written down; the gap is what
  prompted the converter.
- **Theming & Colors** gained a *Coming from 1.x* annotation under the visual
  editor pointing at the converter.
- **Reference › Theming** gained a *Converting a 1.x theme* section.
- `Style.load_user_themes` had a one-line docstring (`"Load user themes saved
  in json format"`) that never stated the file format; it now specifies the
  JSON shape, the verbatim-colors/single-mode behavior, and points at the
  converter.