![](https://img.shields.io/github/release/israel-dryer/ttkbootstrap.svg)
[![Downloads](https://pepy.tech/badge/ttkbootstrap)](https://pepy.tech/project/ttkbootstrap)
[![Downloads](https://pepy.tech/badge/ttkbootstrap/month)](https://pepy.tech/project/ttkbootstrap)
![](https://img.shields.io/github/issues/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/issues-closed/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/license/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/stars/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/forks/israel-dryer/ttkbootstrap.svg)

# ttkbootstrap

ttkbootstrap is a theming extension for tkinter. It generates modern, flat,
Bootstrap-inspired light and dark themes on demand and adds a single
`bootstyle` keyword to every ttk widget — so you describe *intent*
(`"primary"`, `"success"`, `"outline"`) instead of hand-picking colors or
wrangling long ttk style names.

## Documentation
👀 Read the [documentation](https://ttkbootstrap.readthedocs.io/en/latest/).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/_static/examples/home-hero-dark.png">
  <img alt="A ttkbootstrap window: color swatches above themed buttons, inputs, a meter, a table, and a notebook" src="https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/_static/examples/home-hero-light.png">
</picture>

## Features

✔️ [**30 curated themes**](https://ttkbootstrap.readthedocs.io/en/latest/themes.html)  
Fifteen families, each with a coordinated light and dark variant, that re-theme at runtime.

✔️ [**One-keyword styling**](https://ttkbootstrap.readthedocs.io/en/latest/user-guide/foundations/bootstyle-grammar.html)  
Style any ttk widget with the `bootstyle` keyword — `bootstyle="success"`, `bootstyle="info outline"`, `bootstyle="round toggle"` — instead of the legacy `primary.Striped.Horizontal.TProgressbar` style names. If you've used Bootstrap on the web, the idea will feel familiar.

✔️ [**Batteries-included widgets**](https://ttkbootstrap.readthedocs.io/en/latest/widgets/index.html)  
Beyond the styled ttk widgets, ttkbootstrap ships a few extras — **Meter**, **DateEntry**, **Floodgauge**, and **Tableview** — plus fully themed **dialogs**.

✔️ [**Custom themes & styles**](https://ttkbootstrap.readthedocs.io/en/latest/user-guide/feature-guides/theming.html)  
Define your own theme with the declarative `Theme(...)` API, or build reusable custom widget styles — the same machinery the built-in themes use.

## Installation

Requires Python 3.10+. Install with pip:

```bash
python -m pip install ttkbootstrap
```

## Simple usage

Instead of long ttk style names, style widgets with the `bootstyle` keyword:

```python
import ttkbootstrap as ttk

app = ttk.App(title="ttkbootstrap", theme="bootstrap-dark")

ttk.Button(app, text="Submit", bootstyle="success").pack(side="left", padx=5, pady=10)
ttk.Button(app, text="Submit", bootstyle="info outline").pack(side="left", padx=5, pady=10)

app.mainloop()
```

The `bootstyle` value is a small grammar — a color plus optional modifiers and a type:

- `bootstyle="info"` — a colored widget
- `bootstyle="info outline"` — color + variant
- `bootstyle="success round toggle"` — color + modifier + type

Dashes work too (`"info-outline"`). See the [bootstyle grammar](https://ttkbootstrap.readthedocs.io/en/latest/user-guide/foundations/bootstyle-grammar.html) for the full reference, and [Build your first app](https://ttkbootstrap.readthedocs.io/en/latest/user-guide/getting-started/build-your-first-app.html) for a step-by-step walkthrough.

## Upgrading from 1.x

2.0 is a cleanup-and-consolidation release with breaking changes (a canonical `bootstyle` grammar, a new theme catalog, `App` alongside `Window`, and more). Your existing code mostly keeps working — legacy theme names and older spellings are accepted with a deprecation warning. See the [Migrating to 2.0](https://ttkbootstrap.readthedocs.io/en/latest/user-guide/getting-started/migrating.html) guide.

## Icons

Add icons to your app's buttons and labels with the [ttkbootstrap-icons](https://github.com/israel-dryer/ttkbootstrap-icons) library.

## Contributing
We welcome contributions! If you'd like to contribute to ttkbootstrap, please check out our contributing guidelines.

## Links
- **Documentation:** https://ttkbootstrap.readthedocs.io/en/latest/
- **Release notes:** https://github.com/israel-dryer/ttkbootstrap/releases
- **GitHub:** https://github.com/israel-dryer/ttkbootstrap

## Support

This project is proudly developed with the support of the
<a href="https://www.jetbrains.com/pycharm/" target="_blank" rel="noopener">PyCharm IDE</a>, generously provided by JetBrains.

<a href="https://www.jetbrains.com/" target="_blank" rel="noopener"> <picture> <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/f6d4e79d-97f4-4368-a944-affd423aa922"> <img width="250" alt="JetBrains logo" src="https://github.com/user-attachments/assets/1e42e5db-ffb5-4c8d-b238-3f5633fb7e6d"> </picture> </a> 

<sub> © 2025 JetBrains s.r.o. JetBrains and the JetBrains logo are registered trademarks of JetBrains s.r.o. </sub>
