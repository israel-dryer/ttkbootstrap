---
title: Build & Ship
---

# Build & Ship

This guide shows how to **package and distribute** a ttkbootstrap application.

It is designed to work with the `ttkb` CLI workflow:

- `ttkb promote --pyinstaller` to enable packaging support
- `ttkb build` to produce a distributable bundle

!!! link "See [Platform → CLI](cli.md) for the full command reference."

---

## What “shipping” means

Shipping typically means producing **a single executable bundle** (or app folder) that:

- runs without requiring users to install Python
- includes your themes, icons, images, and localization resources
- behaves consistently across systems (fonts, DPI, scaling)

For most desktop apps, the most common approach is **PyInstaller**.

---

## Recommended workflow

### 1) Start a project

Create a project in the style you want:

```bash
# Default: a single-view App with assets/, README.md, and a starter view
ttkb start MyApp

# AppShell with sidebar navigation and starter pages
ttkb start MyApp --template appshell

# Pick the starting theme (any value from `ttkb list themes`)
ttkb start MyApp --theme superhero

# Minimal: skip assets/ and README.md
ttkb start MyApp --simple
```

Packaging support is opt-in — you'll add it via `ttkb promote --pyinstaller`
in step 3 once the app is working.

---

### 2) Run locally

Run the app in development mode:

```bash
ttkb run
```

You can also run directly with Python during early prototyping.

---

### 3) Promote the project for PyInstaller

Enable PyInstaller support (adds/updates the packaging assets):

```bash
ttkb promote --pyinstaller
```

This step is intentionally **opt-in**, so a simple local app stays simple.

What this typically does:

- writes or updates `ttkb.toml`
- creates or updates a PyInstaller spec file
- adds build-related defaults (icon, app name, entrypoint, data files)

---

### 4) Build for distribution

Build the distributable bundle:

```bash
ttkb build
```

For a clean rebuild:

```bash
ttkb build --clean
```

---

## Configuration via `ttkb.toml`

The CLI uses a single source of truth: `ttkb.toml`.

A typical configuration includes:

- app metadata (name, version, entrypoint)
- default container type (GridFrame / PackFrame)
- theme defaults
- localization settings
- build configuration (PyInstaller options, included files)

!!! link "If you’re using `ttkb` for project scaffolding, `ttkb.toml` becomes the central place to keep app and build defaults together."

---

## Including assets

Shipping a desktop app usually requires bundling:

- **icons** (app icon + in-app icon packs)
- **themes** (custom theme palettes, additional theme files)
- **images** (PNG/SVG sources)
- **localization** (compiled message catalogs)

The default `[build.datas].include` pattern in `ttkb.toml` covers
the standard locations:

```toml
[build.datas]
include = ["assets/**", "locales/**", "themes/**", "ttkb.toml"]
```

Add additional patterns if you keep assets elsewhere. Every path
in the source tree must also be reachable at runtime through a
helper like `resource_path` — see [Project Structure → Resolving
asset paths](project-structure.md#resolving-asset-paths) for the
canonical pattern. PyInstaller's onefile mode extracts assets to
a temp directory at launch; hardcoded paths break.

!!! link "See [Capabilities → Icons & Images](../capabilities/icons/index.md) for how icons and images behave at runtime (DPI, caching, recoloring)."

---

## Localization in shipped apps

If you enable i18n with the CLI:

```bash
ttkb add i18n
```

Make sure your build step includes the message catalog assets.

In your UI code, prefer **message tokens**:

```python
ttk.Button(app, text="button.save")
```

!!! link "See [Guides → Localization](../guides/localization.md) for the end-to-end localization workflow."
!!! link "See [Capabilities → Localization](../capabilities/localization.md) for how message tokens are resolved."

---

## App icon and branding

Set the app icon (visible in the taskbar / dock / Alt-Tab) by
pointing `[build.icon].path` at your file:

```toml
[build.icon]
path = "assets/icon.ico"     # Windows
# path = "assets/icon.icns"  # macOS
# path = "assets/icon.png"   # Linux desktop file
```

If `path` is unset, `ttkb build` uses the bundled ttkbootstrap
icon. Per-platform icon files require per-platform formats:

- **Windows** — `.ico` (multi-resolution recommended: 16, 32, 48,
  256 px)
- **macOS** — `.icns` (use `iconutil` from `.iconset/`)
- **Linux** — `.png` (referenced from the `.desktop` file when you
  package as `.deb` / Flatpak)

Branding metadata for installers (publisher, description) lives
under your installer-builder's config (Briefcase's `pyproject.toml`,
WiX, etc.), not in `ttkb.toml`.

---

## Common pitfalls

### Missing files at runtime

Symptoms:

- icons or images disappear
- theme assets aren’t found
- localization falls back to raw tokens

Fix:

- ensure those asset directories are included in the build (spec/data files)
- keep all runtime assets inside your project, not outside it

---

### DPI and scaling differences

In development, your environment may not match target systems.

- Test on multiple DPI settings when possible
- Avoid hardcoded pixel-perfect assumptions

!!! link "See [Platform → Images & DPI](images-and-dpi.md) for how Tk handles DPI and image scaling."

---

### Overriding build behavior

Advanced users may want to edit the spec file directly.

That’s fine — but the recommended path is:

- keep config in `ttkb.toml`
- let `ttkb build` generate/update the spec when possible

---

## Shipping to macOS

`ttkb build` produces a `.app` bundle on macOS via PyInstaller. That bundle
runs locally, but it is **not yet ready for distribution**: modern macOS
(10.15+) refuses to launch unsigned, unnotarized apps with the
"\"MyApp.app\" is damaged and can't be opened" Gatekeeper dialog.

To ship a `.app` to other users, you need four additional steps that
ttkbootstrap intentionally does **not** perform itself:

1. **Code-sign** the bundle with an Apple Developer ID certificate
   ($99/yr Apple Developer Program membership).
2. **Notarize** it via `xcrun notarytool submit` (Apple's automated
   malware scan).
3. **Staple** the notarization ticket to the bundle so it works offline
   (`xcrun stapler staple`).
4. **Package** the result into a DMG (or PKG) for distribution.

Apple's notarization toolchain changes often enough that wrapping it
into `ttkb build` would mean ongoing maintenance for a feature only a
fraction of users need. The recommended path instead is to hand off to
**[Briefcase](https://briefcase.readthedocs.io/)** (BeeWare), which
handles the full chain — signing, notarization, stapling, and DMG
creation — across macOS, Linux (`.deb`/AppImage), and Windows (MSI).

A typical workflow:

```bash
# Develop and iterate with ttkb
ttkb start MyApp
ttkb run

# When you're ready to ship to macOS:
pip install briefcase
briefcase create macOS
briefcase build macOS
briefcase package macOS --identity "Developer ID Application: Your Name (TEAMID)"
```

The Briefcase project layout is independent of the `ttkb start` layout,
so you'll typically point Briefcase at your existing `src/` package and
reuse your assets. See the
[Briefcase macOS docs](https://briefcase.readthedocs.io/en/stable/reference/platforms/macOS.html)
for the full setup.

---

## Shipping to Windows

`ttkb build` produces an unsigned `.exe` (and a folder of dependencies)
on Windows via PyInstaller. That bundle runs locally, but it is **not
ready for distribution**: when users download an unsigned executable,
Windows SmartScreen blocks it with a "Windows protected your PC" prompt
until the binary builds reputation, and most IT-managed environments
will refuse to run it at all.

To ship a Windows app to other users, you typically need:

1. **A code-signing certificate.** Standard Authenticode certificates
   (DigiCert, Sectigo, etc.) run roughly $200–500/year and require
   SmartScreen reputation to build over time. Extended Validation (EV)
   certificates cost more but skip the reputation phase and pass
   SmartScreen on first run.
2. **Sign the binary** with `signtool sign /fd SHA256 /tr <timestamp-url>`.
3. **Wrap it in an installer** — MSI (via WiX), MSIX, NSIS, or Inno
   Setup — so users get a familiar install/uninstall flow and Add/Remove
   Programs registration.
4. **Sign the installer** as well, with the same certificate.

Code-signing toolchains and certificate vendors change often enough
that ttkbootstrap intentionally does **not** wrap them into
`ttkb build`. The recommended path is again
**[Briefcase](https://briefcase.readthedocs.io/)**, which produces a
signed MSI via WiX:

```bash
pip install briefcase
briefcase create windows
briefcase build windows
briefcase package windows --identity <certificate-thumbprint>
```

See the
[Briefcase Windows docs](https://briefcase.readthedocs.io/en/stable/reference/platforms/windows.html)
for certificate setup and signing details.

---

## Shipping to Linux

`ttkb build` produces an executable and a folder of dependencies on
Linux via PyInstaller. That folder runs on the build machine, but
distributing it to other Linux systems is non-trivial: glibc versions
differ across distros, package managers expect distro-specific
metadata, and increasingly users expect sandboxed formats.

The four common distribution formats are:

- **AppImage** — single self-contained file, runs on most distros
  without installation. Best when you want one artifact for everyone.
- **`.deb`** — Debian/Ubuntu package, integrates with `apt` and the
  system menu.
- **`.rpm`** — Fedora/RHEL/openSUSE package.
- **Flatpak** — sandboxed, distro-agnostic, distributed via Flathub.
  Best for end-user GUI apps on modern desktops.

ttkbootstrap intentionally does **not** produce these formats from
`ttkb build` — each has its own metadata, dependencies, and review
process, and most projects only need one or two of them.

For AppImage and `.deb`,
**[Briefcase](https://briefcase.readthedocs.io/)** handles both:

```bash
pip install briefcase
briefcase create linux
briefcase build linux
briefcase package linux --target appimage   # or: --target deb
```

See the
[Briefcase Linux docs](https://briefcase.readthedocs.io/en/stable/reference/platforms/linux.html)
for the supported targets and per-distro requirements.

For Flatpak, the canonical path is `flatpak-builder` driven by a
manifest file, with publication through
[Flathub](https://flathub.org/). The
[Flatpak Python guide](https://docs.flatpak.org/en/latest/python.html)
covers the full setup; this is a separate toolchain from `ttkb build`.

---

## Next steps

- Read [Platform → CLI](cli.md)
- Read [Guides → App Structure](../guides/app-structure.md)
- Read [Guides → Layout](../guides/layout.md)
- Read [Guides → Localization](../guides/localization.md)
