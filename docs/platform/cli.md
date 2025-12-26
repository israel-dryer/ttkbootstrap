---
title: Command Line Interface
---

# Command Line Interface (CLI)

The `ttkb` command-line interface is an **optional productivity tool** that helps you scaffold, organize, and distribute
ttkbootstrap applications.

You can use ttkbootstrap **with or without** the CLI. The CLI exists to reduce boilerplate, encourage best practices,
and provide a smooth path from prototype to distributable application.

---

## What the CLI Is

The `ttkb` CLI is designed to:

- create consistent [project structures](project-structure.md)
- scaffold [views](../guides/layout.md), dialogs, and [assets](../guides/icons.md)
- manage [application configuration](../guides/app-settings.md)
- support [build and distribution](build-and-ship.md) workflows

It does **not** replace Python, Tkinter, or ttkbootstrap APIs. Everything the CLI generates can be modified or written
manually.

---

## What the CLI Is Not

The CLI is not:

- required to use ttkbootstrap
- a runtime dependency for your application
- a replacement for learning the framework

If you prefer a fully manual setup, you can ignore the CLI entirely.

---

## When to Use the CLI

The CLI is most helpful when:

- starting a new application
- maintaining a consistent project layout
- adding [views](../guides/layout.md) or dialogs incrementally
- preparing an app for [distribution](build-and-ship.md)
- working on larger or long-lived projects

For quick scripts or experiments, manual setup may be simpler.

---

## Core Commands

Common CLI commands include:

- `ttkb start` — create a new application
- `ttkb run` — run the current application
- `ttkb add view` — scaffold a new view
- `ttkb add dialog` — scaffold a dialog
- `ttkb add theme` — create a [theme](../guides/theming.md) skeleton
- `ttkb build` — prepare a [distributable build](build-and-ship.md)

Each command operates on the **current project** and respects project configuration.

---

## Configuration (`ttkb.toml`)

When present, the CLI reads configuration from a `ttkb.toml` file at the project root.

This file may define:

- application metadata
- default [layout](../guides/layout.md) preferences
- [localization](../guides/localization.md) settings
- [build and distribution](build-and-ship.md) options

If no `ttkb.toml` file exists, defaults are used and [application settings](../guides/app-settings.md) can be defined programmatically.

---

## CLI and Application Settings

The CLI integrates with the framework's [application configuration](../guides/app-settings.md) model:

- CLI settings populate or override defaults
- application code remains authoritative at runtime
- build-time and runtime concerns are kept separate

This allows CLI-generated projects to remain flexible and transparent.

---

## Next Steps

- See [Quick Start](../getting-started/quick-start.md) for creating new projects
- See [Project Structure](project-structure.md) to understand generated layouts
- See [App Settings](../guides/app-settings.md) for runtime configuration
- See [Build & Ship](build-and-ship.md) for packaging and distribution
