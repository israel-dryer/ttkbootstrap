![](https://img.shields.io/github/release/israel-dryer/ttkbootstrap.svg)
[![Downloads](https://pepy.tech/badge/ttkbootstrap)](https://pepy.tech/project/ttkbootstrap)
[![Downloads](https://pepy.tech/badge/ttkbootstrap/month)](https://pepy.tech/project/ttkbootstrap)
![](https://img.shields.io/github/issues/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/issues-closed/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/license/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/stars/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/forks/israel-dryer/ttkbootstrap.svg)


![](assets/ttkbootstrap-logo-horizontal-dark.png#only-dark)
![](assets/ttkbootstrap-logo-horizontal-light.png#only-light)

**ttkbootstrap** is an opinionated UI framework for building modern desktop applications with Python and Tkinter.

It goes beyond theming—providing a cohesive **design system**, a complete **widget ecosystem**, and **framework-level capabilities** so you can focus on building applications instead of wrestling with low-level UI mechanics.

> **v2 is under active development.**
> Documentation, examples, and migration guides are being added as the API stabilizes.

## Features

- **Modern UI Defaults** — Consistent colors, typography, spacing, and Bootstrap-inspired variants out of the box
- **Complete Widget Ecosystem** — 60+ widgets including buttons, dialogs, forms, tables, and navigation components
- **Reactive State with Signals** — Observable state management for declarative, composable applications
- **Design Token System** — Semantic colors and styles that adapt across themes
- **Built-in Validation** — Form validation without reinventing the wheel
- **Icon & Image Support** — First-class icon handling and image utilities
- **Localization Ready** — i18n support for global applications
- **CLI & Packaging Support** — Tools for building and distributing your apps

## Installation

```bash
pip install ttkbootstrap
```

## Quick Start

```python
import ttkbootstrap as ttk

app = ttk.App(theme="dark")

# Create styled widgets with bootstyle
ttk.Label(app, text="Hello from ttkbootstrap!").pack(pady=10)
ttk.Button(app, text="Primary", bootstyle="primary").pack(pady=5)
ttk.Button(app, text="Success", bootstyle="success").pack(pady=5)
ttk.Button(app, text="Danger Outline", bootstyle="danger-outline").pack(pady=5)

app.mainloop()
```

## Widget Categories

| Category | Widgets |
|----------|---------|
| **Actions** | Button, DropdownButton, MenuButton, ContextMenu, ButtonGroup |
| **Inputs** | TextEntry, PasswordEntry, PathEntry, NumericEntry, Scale, DateEntry, TimeEntry |
| **Selection** | CheckButton, RadioButton, ToggleGroup, OptionMenu, SelectBox, Calendar |
| **Data Display** | Label, ListView, TreeView, TableView, Badge, Progressbar, Meter, FloodGauge |
| **Layout** | Frame, LabelFrame, PanedWindow, ScrollView, Separator |
| **Views** | Notebook, PageStack |
| **Dialogs** | MessageDialog, ColorChooser, FontDialog, DateDialog, FormDialog, QueryDialog |
| **Overlays** | Toast, Tooltip |
| **Forms** | Form with validation support |

## Bootstyle System

All widgets support the `bootstyle` parameter for easy theming:

```python
# Color variants
ttk.Button(app, text="Primary", bootstyle="primary")
ttk.Button(app, text="Success", bootstyle="success")
ttk.Button(app, text="Warning", bootstyle="warning")
ttk.Button(app, text="Danger", bootstyle="danger")

# Style modifiers
ttk.Button(app, text="Outline", bootstyle="primary-outline")
ttk.Button(app, text="Link", bootstyle="info-link")
```

## Why ttkbootstrap?

ttkbootstrap is designed for developers who want to:

- Build desktop apps that feel modern and intentional
- Move fast without reinventing UI patterns
- Maintain visual consistency across applications
- Apply reactive and declarative patterns in Tk
- Ship polished tools to end users

You don't need to deeply understand Tk or ttk internals to be productive with ttkbootstrap.

## Links

- **GitHub**: https://github.com/israel-dryer/ttkbootstrap
- **Icons**: https://github.com/israel-dryer/ttkbootstrap-icons

## Support

This project is proudly developed with the support of the
<a href="https://www.jetbrains.com/pycharm/" target="_blank" rel="noopener">PyCharm IDE</a>, generously provided by JetBrains.

<a href="https://www.jetbrains.com/" target="_blank" rel="noopener"> <picture> <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/f6d4e79d-97f4-4368-a944-affd423aa922"> <img width="250" alt="JetBrains logo" src="https://github.com/user-attachments/assets/1e42e5db-ffb5-4c8d-b238-3f5633fb7e6d"> </picture> </a>

<sub> © 2025 JetBrains s.r.o. JetBrains and the JetBrains logo are registered trademarks of JetBrains s.r.o. </sub>