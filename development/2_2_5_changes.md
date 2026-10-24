# ttkbootstrap 2.2.5 — notable changes

Changes since **2.2.4**. Unreleased.

| Area                          | Kind |
|-------------------------------|------|
| **Scrollbars redraw quickly** | Fix  |

No API breaks.

---

## Scrollbars redraw quickly *(Fix)*

Dragging or hovering a scrollbar redrew its thumb slowly, worst on a long thumb, and at some display scalings the
thumb drew only its end caps. The thumb now redraws as fast as a stock `ttk.Scrollbar`. Its minimum length is 16px
instead of 17.

**Affected**: default, round and thin scrollbars, every 2.x release. (#1348, contributed by @bszollosinagy)
