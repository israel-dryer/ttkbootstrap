# ttkbootstrap 2.2.7 — notable changes

Changes since **2.2.6**. Unreleased.

| Area                                   | Kind |
|----------------------------------------|------|
| **Scrollbar thumbs draw on Tk 8.6.15+** | Fix  |

No API breaks.

---

## Scrollbar thumbs draw on Tk 8.6.15+ *(Fix)*

On Tk 8.6.15 and newer, scrollbar thumbs drew only their two end caps; the body between them was missing. The thumb now draws in full.

**Affected**: every scrollbar style in 2.2.5 and 2.2.6 on Tk 8.6.15+, which includes the python.org Windows installers. (#1355, reported by @gmm96)
