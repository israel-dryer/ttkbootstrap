![](https://img.shields.io/github/release/israel-dryer/ttkbootstrap.svg)
[![Downloads](https://pepy.tech/badge/ttkbootstrap)](https://pepy.tech/project/ttkbootstrap)
[![Downloads](https://pepy.tech/badge/ttkbootstrap/month)](https://pepy.tech/project/ttkbootstrap)
![](https://img.shields.io/github/issues/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/license/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/stars/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/pypi/pyversions/ttkbootstrap.svg)

# ttkbootstrap

**Modern, themed tkinter — style any ttk widget with one keyword.**

ttkbootstrap is a theming extension for tkinter. It generates flat,
Bootstrap-inspired light and dark themes on demand and adds a single ``bootstyle``
keyword to every ttk widget, so you describe *intent* — ``"primary"``,
``"success"``, ``"outline"`` — instead of hand-tuning colors or long ttk style
names.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/_static/examples/home-hero-dark.png">
  <img alt="A ttkbootstrap window: color swatches above themed buttons, inputs, a meter, a table, and a notebook" src="https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/_static/examples/home-hero-light.png">
</picture>

## Why ttkbootstrap

- 🎨 **30 curated themes** — fifteen families, each in a coordinated light and dark variant, that switch at runtime.
- ⌨️ **One-keyword styling** — `bootstyle="success"`, `bootstyle="info outline"`, `bootstyle="round toggle"`. The same keyword means the same thing on every widget.
- 🧩 **Batteries-included** — styled ttk widgets plus a few extras (`Meter`, `DateEntry`, `Floodgauge`, `Tableview`) and fully themed dialogs.
- 🛠️ **Your own themes & styles** — a declarative `Theme(...)` API and a public toolkit for building custom widget styles.
- 🪶 **Pure Python** — one dependency (Pillow), Python 3.10+, no native extensions.

It's a **styling layer for vanilla tkinter**, not a new framework: the widgets stay
tkinter's, and everything you already know about tkinter still applies.

## Install

```bash
python -m pip install ttkbootstrap
```

## Quickstart

```python
import ttkbootstrap as ttk

app = ttk.App(title="Hello")

ttk.Label(app, text="Hello from ttkbootstrap!").pack(padx=16, pady=(16, 8))
ttk.Button(app, text="Primary", bootstyle="primary").pack(padx=16, pady=4)
ttk.Button(app, text="Success", bootstyle="success").pack(padx=16, pady=4)
ttk.Button(app, text="Danger Outline", bootstyle="danger outline").pack(padx=16, pady=(4, 16))

app.mainloop()
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/_static/examples/quickstart-hello-dark.png">
  <img alt="The Hello window: a greeting label above primary, success, and danger-outline buttons" src="https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/_static/examples/quickstart-hello-light.png">
</picture>

## The bootstyle keyword

A `bootstyle` value is a small grammar — a **color**, plus an optional **modifier**
and **widget type** — and the same keyword carries the same meaning across widgets:

```python
ttk.Button(app, bootstyle="success")
ttk.Progressbar(app, bootstyle="success")
ttk.Entry(app, bootstyle="success")
```

Add a modifier or a type for variants: `"info outline"`, `"success round toggle"`,
`"warning striped"`. The vocabulary is closed, so a typo fails loudly instead of
silently doing nothing. See the
[bootstyle grammar](https://ttkbootstrap.readthedocs.io/en/latest/user-guide/foundations/bootstyle-grammar.html)
for the full reference.

## Themes

Thirty curated light and dark themes, switchable at runtime:

```python
app.theme_use("bootstrap-dark")   # any theme by name
app.toggle_theme()                # flip light <-> dark
```

Browse them in the
[themes gallery](https://ttkbootstrap.readthedocs.io/en/latest/themes.html).

## Documentation

- **[Documentation](https://ttkbootstrap.readthedocs.io/en/latest/)** — guides, the widget catalog, and the API reference.
- **[Build your first app](https://ttkbootstrap.readthedocs.io/en/latest/user-guide/getting-started/build-your-first-app.html)** — a step-by-step walkthrough.
- **[Migrating to 2.0](https://ttkbootstrap.readthedocs.io/en/latest/user-guide/getting-started/migrating.html)** — upgrading from 1.x.
- **[Release notes](https://github.com/israel-dryer/ttkbootstrap/releases)** — what changed in each version.

## Upgrading from 1.x

2.0 is a cleanup-and-consolidation release with some breaking changes — a canonical
`bootstyle` grammar, a new theme catalog, and `App` alongside `Window`. Most code
keeps working: legacy theme names and older spellings are accepted with a
deprecation warning. The
[Migrating to 2.0](https://ttkbootstrap.readthedocs.io/en/latest/user-guide/getting-started/migrating.html)
guide sorts every change into breaking / deprecated / notable / new.

## Icons

Add icons to your app's buttons and labels with the
[ttkbootstrap-icons](https://github.com/israel-dryer/ttkbootstrap-icons) library.

## Contributing

Contributions are welcome — please check out our contributing guidelines.

## Support

This project is proudly developed with the support of the
<a href="https://www.jetbrains.com/pycharm/" target="_blank" rel="noopener">PyCharm IDE</a>, generously provided by JetBrains.

<a href="https://www.jetbrains.com/" target="_blank" rel="noopener"> <picture> <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/f6d4e79d-97f4-4368-a944-affd423aa922"> <img width="250" alt="JetBrains logo" src="https://github.com/user-attachments/assets/1e42e5db-ffb5-4c8d-b238-3f5633fb7e6d"> </picture> </a>

<sub> © 2025 JetBrains s.r.o. JetBrains and the JetBrains logo are registered trademarks of JetBrains s.r.o. </sub>
