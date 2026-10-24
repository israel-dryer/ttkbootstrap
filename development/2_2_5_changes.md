# ttkbootstrap 2.2.5 — notable changes

Changes since **2.2.4**. Released 2026-10-24.

| Area                                  | Kind |
|---------------------------------------|------|
| **Scrollbars redraw quickly**         | Fix  |
| **ScrolledFrame content holds still** | Fix  |

No API breaks.

---

## Scrollbars redraw quickly *(Fix)*

Dragging or hovering a scrollbar redrew its thumb slowly, worst on a long thumb, and at some display scalings the
thumb drew only its end caps. The thumb now redraws as fast as a stock `ttk.Scrollbar`. Its minimum length is 16px
instead of 17.

**Affected**: default, round and thin scrollbars, every 2.x release. (#1348, contributed by @bszollosinagy)

## ScrolledFrame content holds still *(Fix)*

With `auto_hide=True`, showing and hiding the scrollbar on hover shifted and re-wrapped the content by the bar's
width. The bar's space is now kept reserved, as `ScrolledText` already did.

**Affected**: `ScrolledFrame(auto_hide=True)`, every 2.x release. (#1352, contributed by @Agent-0808)
