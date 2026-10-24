# ttkbootstrap 2.2.4 — notable changes

Changes since **2.2.3**. Released 2026-10-23.

| Area                                 | Kind  |
|--------------------------------------|-------|
| **Pillow 13 allowed**                | Build |
| **Frozen apps report their version** | Fix   |

No API breaks.

---

## Pillow 13 allowed *(Build)*

The Pillow requirement is now `pillow>=10,<14`, so apps can install Pillow 13.0.0 and its security fixes. Python 3.10
still gets Pillow 12, since Pillow 13 drops 3.10.

**Affected**: every app pinned below Pillow 13 by ttkbootstrap's `<13` cap. (#1350, contributed by @dwf981)

## Frozen apps report their version *(Fix)*

In an app built with PyInstaller, `ttk.__version__` read `"unknown"`, because the hook bundled ttkbootstrap's assets
but not its package metadata. The hook now bundles both.

**Affected**: 2.2.3, the first release with the hook.
