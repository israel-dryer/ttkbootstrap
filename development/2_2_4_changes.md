# ttkbootstrap 2.2.4 — notable changes

Changes since **2.2.3**. Unreleased.

| Area                          | Kind |
|-------------------------------|------|
| **Scrollbars redraw quickly** | Fix  |

No API breaks.

---

## Scrollbars redraw quickly *(Fix)*

The scrollbar thumb was an image whose 1px middle ttk tiles, so every redraw painted the thumb one pixel-row at a time:
about 8.7 ms for a tall thumb at 96 dpi, ~350x a stock `ttk.Scrollbar`. At some display scalings (e.g. Tk scaling 1.6)
the rounding left no middle at all, and the default and round thumbs drew only their end caps. The thumb is now two
small cap images around a solid fill, which redraws as fast as stock ttk at any length; the minimum thumb length is
16px instead of 17. `tools/bench_scrollbar.py` measures it.

**Affected**: default, round and thin scrollbars, every 2.x release. (#1348)
