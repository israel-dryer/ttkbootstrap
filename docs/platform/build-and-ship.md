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
ttkb start MyApp --simple
```

Or start with distribution-oriented defaults:

```bash
ttkb start MyApp --pyinstaller
```

(If your CLI separates these concerns, you can instead run `ttkb promote --pyinstaller` later.)

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
- **images** (PNG/SVG sources, runtime-generated caches if any)
- **localization** (message catalogs / language packs)

If you’re using ttkbootstrap’s built-in asset systems, the CLI/build integration should include the relevant folders.

!!! link "See [Capabilities → Icons & Imagery](../capabilities/icons-and-imagery.md) for how icons and images behave at runtime (DPI, caching, recoloring)."

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

Most apps should ship with:

- an **application icon** (window/taskbar)
- a **brand mark** (optional)
- optional installer metadata (publisher, description)

Your CLI can provide a default icon that users can replace.

If you support per-platform icons:

- Windows: `.ico`
- macOS: `.icns`
- Linux: `.png` (desktop file icon)

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

## Next steps

- Read [Platform → CLI](cli.md)
- Read [Guides → App Structure](../guides/app-structure.md)
- Read [Guides → Layout](../guides/layout.md)
- Read [Guides → Localization](../guides/localization.md)
