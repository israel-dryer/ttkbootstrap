# 2.0 Docs — Widgets-catalog usage-guide enrichment (audit + plan)

Author steer (2026-07-13): the existing catalog usage pages were authored *before*
the "don't write lite pages — mine the Tcl/Tk manuals for concepts/caveats" rule
([[feedback_mine_tcltk_manuals_for_usage]]). This pass re-evaluates every existing
`docs/widgets/*.rst` page against its `ttk_*`/`tk` manual (shipped widgets against
their real source/API) and enriches the thin ones. Canvas (just authored) and Text
(already robust) are excluded.

**Method:** 6 parallel audit agents, one per family, each read the full page +
fetched the manual + verified names against the live API. Findings below are their
grounded output. **Execution:** one PR per family (same structure as the original
catalog PRs), every new snippet verified headlessly, build gate `sphinx -W -q -E`
exit 0. Depth stays *usage* depth — teach the real patterns/caveats, not an
exhaustive option dump (the API reference is the depth home).

**Five factual errors to fix (independent of enrichment):** radiobutton
"unrelated buttons" note (backwards — shared `::selectedButton`), button "no
default flag" (false — `default=` exists), labeledscale "shows whole numbers"
(`:g`), toast default-position + 4-anchor list (OS-specific; 8 anchors), tooltip
`delay` default (250 not 500).

---

## PR 1 — Containers (frame, labelframe, notebook, panedwindow)

- **frame** (OK→minor): geometry-propagation caveat (`width`/`height` ignored once
  children packed; `pack_propagate(False)`/`grid_propagate(False)` to force); note
  `relief` needs non-zero `borderwidth` + prefer `card`/`highlight` over raw relief;
  frames are non-interactive.
- **labelframe** (MODERATE): `labelanchor=` (12 forms, where the caption sits);
  `labelwidget=` (replace caption text with a widget, e.g. a checkbutton that
  enables the group — overrides `text=`, must be child/ancestor); `underline=`
  mnemonic.
- **notebook** (MODERATE): `enable_traversal()` (Ctrl-Tab / Alt-mnemonic; needs all
  pages as direct children) + tab `underline=`; tab display options on `add`/`tab`
  (`image`/`compound`/`underline`/`sticky`/`padding`); tab-id forms
  (index/widget/`@x,y`/`current`/`end`); `state="hidden"` third state; `tabs()` +
  `identify(x,y)`; `<<NotebookTabChanged>>` also fires on initial map (matters for
  lazy-load).
- **panedwindow** (MODERATE): `insert(pos,child,weight=)` / `forget(child)`;
  `panes()` + `pane(child, weight=)` to reconfigure; multi-sash monotonic clamp;
  `sashpos` only after mapped (`update_idletasks()`); `orient` is configurable
  (page implies construction-only); no per-pane `minsize` (unlike tk.PanedWindow).

## PR 2 — Range & misc (label, progressbar, scale, scrollbar, separator, sizegrip)

- **label** (MODERATE): `anchor=` vs `justify=` distinction (block position vs
  wrapped-line alignment); `width=` (char width, negative=min, for aligning form
  label columns); `relief=`+`padding=` (badge/chip look); `compound=` values;
  `disabled` greys text.
- **progressbar** (MODERATE-light): indeterminate `value` wraps modulo `maximum`
  (so maximum sets cycle length); `variable` overrides `value`; `step` default
  `1.0`; `start(interval)` default 50 ms; read-only `phase` drives stripes.
- **scale** (MODERATE): `.set()` clips to range but assigning the variable directly
  bypasses clipping (footgun); `command` receives the value as a **string**
  (explains the `float()` cast); `.coords(value)` + `.get(x,y)` (pixel↔value, how
  LabeledScale places its label); no `resolution`/`tickinterval`/`showvalue`/`label`
  vs tk.Scale (migrator note); `to<from_` inverts.
- **scrollbar** (MODERATE): auto-disable when whole range visible (set gets
  `0.0 1.0`) — "dead scrollbar" surprise; fraction model 0.0–1.0; `.get()` →
  `(first,last)`; `command` subcommands (`moveto`/`scroll n units|pages`) for
  custom/canvas wiring.
- **separator** (OK): optional — default `orient` horizontal; purely decorative.
- **sizegrip** (MODERATE): negative-geometry caveat (window positioned with
  `-x-y` won't resize — the marquee bug); SE-only (why bottom-right + `anchor=SE`);
  macOS draws a native grip already.

## PR 3 — Inputs (entry, combobox, spinbox)

- **entry** (MODERATE): index vocab (`insert`/`sel.first`/`sel.last`/`@x`;
  out-of-range rounds); `icursor()`; selection methods (`selection_range`/`_clear`/
  `_present`, `index()`); `show=` copies mask chars caveat; validatecommand `%`
  substitutions pointer (`%P`/`%s`/`%S`/`%d`/`%V`) + `invalidcommand`; ttk caveat:
  validation NOT re-triggered on programmatic `textvariable` change; `invalid`
  state auto-set.
- **combobox** (MODERATE): `current()` as getter (index or `-1` if typed value not
  in list) — detect pick-vs-typed; `postcommand=` (refresh `values` before
  dropdown); `height=`; `<<ComboboxSelected>>` fires only on pick, not typed edits
  (trace the var too); dropdown list is a classic `listbox`, NOT ttk-styled
  (option-database only) — the look-mismatch surprise; readonly still settable via
  dropdown/`.set()`.
- **spinbox** (MODERATE): `format="%.2f"` (kills float noise on fractional
  `increment`); `values=` overrides `from_`/`to`/`increment`; keyboard
  `<Up>`/`<Down>` + `<<Increment>>`/`<<Decrement>>` events; `command` on spin only
  (typed edits via var trace); `wrap` works for numeric ranges too; `.set()` exists
  but NO `current()` (unlike Combobox).

## PR 4 — Choice + Command (checkbutton, radiobutton, menubutton, optionmenu)

- **checkbutton** (OK): one line — `selected` state tracks the variable
  automatically.
- **radiobutton** (MODERATE, **correctness**): FIX the note — without `variable=`
  they share the default global `::selectedButton` (interfere), not independent;
  add `alternate`/tristate state (variable unset → mixed look); `selected` tracks
  variable.
- **menubutton** (OK): optional one line — build the menu as a child of the
  menubutton.
- **optionmenu** (MODERATE): `set_menu(default=None, *values)` to rebuild choices
  after construction (the "it builds its own menu" concept, made dynamic).

## PR 5 — Button + Treeview

- **button** (MODERATE, **correctness**): FIX "no default flag" — `default=`
  (`normal`/`active`/`disabled`) is real; teach `Button(default="active")` for the
  platform default-ring + still show the `<Return>` binding; add `invoke()`; name
  the `active` state.
- **treeview** (MODERATE, additive): `selectmode=` (extended/browse/none; code
  selection ignores browse); `selection_add`/`_remove`/`_toggle`;
  `<<TreeviewOpen>>`/`<<TreeviewClose>>` (lazy-load children); `detach`/`reattach`
  (hide/filter without delete); hit-testing `identify_region`/`_column`/`_row` +
  `bbox` (context menus); `see(item)`; focus vs selection distinction; hierarchy
  nav (`parent`/`children`/`index`/`next`/`prev`/`exists`); `displaycolumns=`;
  `column(stretch=False)` pin + tag priority = creation order + `foreground`/`font`
  tag options.

## PR 6 — Shipped (meter, floodgauge, labeledscale, dateentry, tableview, toast, tooltip)

- **meter** (MODERATE): `text_left`/`text_right` (`$`/`%` affixes); `amount_format`
  (`"{:.1f}"`); `amount_min` (negative/offset ranges); `value` property;
  `step()` bounces at min/max (reverses, not clamp); `wedge_size` look.
- **floodgauge** (OK-minor): `length`/`thickness` sizing; `mask` formats
  `int(value)` (fractional shows truncated); `font`.
- **labeledscale** (MODERATE, **correctness**): FIX "whole numbers" (`:g` →
  `3.7` shows `3.7`); `.scale`/`.label` sub-widget access; `value` read/write
  property (variable optional); horizontal-only (no `orient`).
- **dateentry** (MODERATE): `<<DateEntrySelected>>` event; typed-text + blur
  validation (`get_date()` parses live entry text; unparseable → `invalid` on
  focus-out); `get_date()` never returns None here (vs `Querybox.get_date` dialog
  which does); `value` property; `show_outside_days`.
- **tableview** (OK-minor): `iid_field` (natural-key iids, for stable
  `delete_row(iid=)`/`get_row(iid=)`); `insert_row(reload=True)` already redraws;
  `autofit`/`height` (viewport rows ≠ `pagesize`); column-scoped
  `search_table_data(criteria, *columns)`.
- **toast** (MODERATE, **correctness**): `show_toast()` returns the toast as a
  dismiss handle; FIX anchor list (8 compass points); FIX default position
  (SE win32/x11, NE aqua); auto-stacking of concurrent toasts; `hide()` canonical.
- **tooltip** (MODERATE, **correctness**): FIX `delay` default (250 not 500);
  `position=` ("top left"/…) anchors to widget vs following pointer;
  `configure()`/`cget()` live reconfig; `justify`/`image`/`padding`.

## PR 7 (optional, small) — Text

- One line: inline `image_create(index, image=)` / `window_create(index, window=)`
  to embed pictures/widgets between characters. Low priority; API ref is depth home.

---

**Status:** COMPLETE 2026-07-13 — all six family PRs authored, verified headlessly,
`-W` green, and **MERGED** into `2.0`: PR 1 Containers (#1196), PR 2 Range & misc
(#1197), PR 3 Inputs (#1198), PR 4 Choice + Command (#1199), PR 5 Button + Treeview
(#1200), PR 6 Shipped (#1201). The optional PR 7 (Text `image_create`/
`window_create`) was **dropped** — Text is already robust and the API reference is
its depth home. Five factual errors were fixed along the way (radiobutton
shared-global note, button `default=` claim, labeledscale `:g`, toast
anchors/default-position, tooltip `delay`). Merged `2.0` builds clean (`-W`, exit 0)
and the catalog coverage test stays green.
