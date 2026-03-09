# CLI Review & Recommended Changes

## Current State

The `ttkb` CLI provides 6 commands: `start`, `run`, `add`, `promote`, `build`, and `demo`.
The config system (`ttkb.toml`), PyInstaller integration, and project scaffolding are well-structured.

### Files Involved

| File | Purpose |
|------|---------|
| `src/ttkbootstrap/cli/__init__.py` | Main dispatcher, argparse setup |
| `src/ttkbootstrap/cli/start.py` | `ttkb start` — project scaffolding |
| `src/ttkbootstrap/cli/run.py` | `ttkb run` — launch app |
| `src/ttkbootstrap/cli/add.py` | `ttkb add view/dialog/theme/i18n` |
| `src/ttkbootstrap/cli/promote.py` | `ttkb promote --pyinstaller` |
| `src/ttkbootstrap/cli/build.py` | `ttkb build` — PyInstaller build |
| `src/ttkbootstrap/cli/demo.py` | `ttkb demo` — widget showcase |
| `src/ttkbootstrap/cli/config.py` | `ttkb.toml` loader/writer |
| `src/ttkbootstrap/cli/templates/__init__.py` | All code-generation templates |

---

## Issues

### 1. No AppShell Template (Major Gap)

`ttkb start` only generates a basic `ttk.App` + single view. AppShell is the flagship composite widget (toolbar + sidenav + pages) and should be the most prominent template option.

**Current behavior:**
```
ttkb start MyApp                    # -> App + GridFrame view
ttkb start MyApp --container pack   # -> App + PackFrame view
ttkb start MyApp --simple           # -> Minimal, no assets
```

**Proposed behavior:**
```
ttkb start MyApp                        # -> AppShell (new default)
ttkb start MyApp --template appshell    # -> AppShell explicitly
ttkb start MyApp --template basic       # -> Current App + single view
ttkb start MyApp --simple               # -> Minimal, no assets (keep as-is)
```

The `appshell` template should generate:
- `main.py` using `ttk.AppShell` instead of `ttk.App`
- A `pages/` directory instead of `views/`
- 2-3 starter pages (Home, Settings)
- Wired-up navigation with `add_page`, `add_separator`, footer items

### 2. Templates Don't Match the 7 Paradigms

`templates/README.md` defines 7 app paradigms, but the CLI only knows about grid/pack container variations.

**Minimum viable template set:**
| Template | Paradigm | Description |
|----------|----------|-------------|
| `appshell` | Modern Navigation App | SideNav + pages (new default) |
| `basic` | Dialog-First Utility | Current single-view app |

**Future candidates:** `tabs`, `master-detail`, `wizard`

### 3. `ttkb add view` Doesn't Support AppShell Pages

For AppShell projects, users need to add *pages*, not GridFrame/PackFrame views. AppShell pages are frames added via `shell.add_page()`.

**Proposed:** Add `ttkb add page <PageName>` that generates a page module appropriate for AppShell projects. Detection via a new `template` field in `ttkb.toml`.

### 4. `--container` Flag Is Misleading for AppShell

The `grid`/`pack` choice only makes sense for `basic` template apps. AppShell pages don't require a specific container type. The `--container` flag should only apply when `--template basic` is used.

### 5. Demo Doesn't Showcase AppShell

`ttkb demo` only shows the widget showcase in a plain `ttk.App`. Consider:
- `ttkb demo --appshell` to launch the AppShell demo
- Or restructuring the demo itself as an AppShell (widget categories as pages)

### 6. Config Doesn't Track Template Type

`ttkb.toml` has no `template` field. This means `ttkb add` commands can't know whether the project is an AppShell or basic app, so they can't generate the right scaffolding.

**Proposed addition to `[app]`:**
```toml
[app]
name = "MyApp"
id = "com.example.myapp"
entry = "src/myapp/main.py"
template = "appshell"
```

### 7. Minor Issues

- **`ttkb run`** doesn't read `settings.theme` from `ttkb.toml` — the generated app hardcodes `theme="cosmo"`.
- **Theme JSON templates** in `add.py` use keys like `inputBackground`/`inputForeground` — verify these match the actual v2 theme schema.
- **PO file date** is hardcoded to `2024-01-01` in the i18n template.

---

## Recommended Additions (User Expectations)

### `ttkb list themes`
Users expect to discover available themes from the CLI. Add a `list` command with subcommands:
```
ttkb list themes       # Show available themes
ttkb list templates    # Show available project templates
```

### `ttkb doctor` / `ttkb check`
Validate the project structure:
- Check `ttkb.toml` exists and is valid
- Verify entry point file exists
- Check dependencies are installed
- Report missing directories (assets/, locales/, etc.)

### `--verbose` Flag
The top-level `ttkb` command should accept `--verbose` to show full tracebacks on error instead of just `Error: <msg>`.

### `--theme` Flag on `ttkb start`
Let users pick a starting theme:
```
ttkb start MyApp --theme superhero
```
Instead of always defaulting to `cosmo`.

---

## Implementation Priority

1. **Add `--template` flag with `appshell` template** — highest impact
2. **Add `template` field to `ttkb.toml`** — enables smart `add` commands
3. **Add `ttkb add page`** — complements AppShell workflow
4. **Add `--theme` flag to `ttkb start`** — quick win
5. **Add `ttkb list themes`** — quick win
6. **Update demo to showcase AppShell** — nice to have
7. **Add `ttkb doctor`** — nice to have
