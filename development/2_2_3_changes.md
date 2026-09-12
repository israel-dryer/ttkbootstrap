# ttkbootstrap 2.2.3 — notable changes

Changes since **2.2.2**. Released 2026-09-12.

| Area                        | Kind |
|-----------------------------|------|
| **PyInstaller builds work** | Fix  |
| **Documentation**           | Docs |

No API breaks.

---

## PyInstaller builds work *(Fix)*

Apps frozen with PyInstaller crashed on startup with a `FileNotFoundError` for
`ttkbootstrap/assets/icons/bootstrap.ttf`, because PyInstaller doesn't bundle package data on its own. ttkbootstrap now
ships a hook that PyInstaller picks up automatically, so `pyinstaller your_app.py` works with no extra setup.

**Affected**: every 2.x release. (#1347, contributed by @NathanVaughn)

## Documentation *(Docs)*

New How-To, **Package your app**: building with PyInstaller, and pointing it at the hook by hand when it can't find it
on its own.
