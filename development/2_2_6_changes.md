# ttkbootstrap 2.2.6 — notable changes

Changes since **2.2.5**. Unreleased.

| Area                              | Kind |
|-----------------------------------|------|
| **Scrollbar thumbs drag again**    | Fix  |

No API breaks.

---

## Scrollbar thumbs drag again *(Fix)*

Scrollbar thumbs could no longer be dragged with the mouse after the redraw optimization in 2.2.5, although clicking the empty track still scrolled. Dragging now works from the middle and both ends of the thumb.

**Affected**: default, round and thin scrollbars in both orientations, in 2.2.5. (#1354, contributed by @Agent-0808)
