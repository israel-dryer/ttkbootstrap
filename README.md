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

**ttkbootstrap** is a modern, opinionated UI framework for building desktop applications with Python and Tkinter.

It's a **framework**, not just themed widgets. ttkbootstrap provides conventions for layout, styling, state, and reactivity that work together—so you can focus on building applications instead of wrestling with low-level UI mechanics.

> **v2 is under active development.**
> See the [documentation](https://ttkbootstrap.com) for guides, API reference, and migration info.

## Installation

```bash
pip install ttkbootstrap
```

## Quick Start

```python
import ttkbootstrap as ttk

app = ttk.App(theme="dark")

ttk.Label(app, text="Hello from ttkbootstrap!").pack(pady=10)
ttk.Button(app, text="Primary", bootstyle="primary").pack(pady=5)
ttk.Button(app, text="Success", bootstyle="success").pack(pady=5)
ttk.Button(app, text="Danger Outline", bootstyle="danger-outline").pack(pady=5)

app.mainloop()
```

## Core Ideas

### Containers express layout intent

Build layouts with purpose-built containers, not scattered geometry calls:

```python
form = ttk.GridFrame(app, columns=["auto", 1], gap=(12, 6), padding=12)
form.pack(fill="both", expand=True)

form.add(ttk.Label(form, text="Name"))
form.add(ttk.Entry(form))
form.add(ttk.Label(form, text="Email"))
form.add(ttk.Entry(form))
form.add(ttk.Button(form, text="Submit", bootstyle="primary"), columnspan=2)
```

### Styling is semantic

Widgets use semantic tokens—not hardcoded colors. Applications stay consistent across themes.

```python
ttk.Button(app, text="Primary", bootstyle="primary")
ttk.Button(app, text="Outline", bootstyle="success-outline")
ttk.Label(app, text="Heading", font="heading-lg")
```

### Reactivity is optional and explicit

Use simple callbacks when that's enough. Introduce signals when state needs to flow.

```python
counter = ttk.Signal(0)

def increment():
    counter.set(counter.get() + 1)

label = ttk.Label(app)
counter.subscribe(lambda v: label.configure(text=f"Count: {v}"))
```

## Features

- **Modern UI Defaults** — Consistent colors, typography, spacing, and Bootstrap-inspired variants
- **60+ Widgets** — Buttons, dialogs, forms, tables, navigation, and more
- **Layout Containers** — PackFrame and GridFrame for declarative, maintainable layouts
- **Reactive Signals** — Observable state management for declarative applications
- **Design Tokens** — Semantic colors and typography that adapt across themes
- **DataSource System** — Pagination, filtering, sorting, and CRUD for data-driven widgets
- **Built-in Validation** — Form validation without reinventing the wheel
- **Icons & Images** — First-class icon handling and image utilities
- **Localization** — i18n support for global applications
- **CLI Tools** — Project scaffolding, building, and packaging

## CLI

Scaffold new projects and add components quickly:

```bash
ttkb start MyApp          # Create new project
ttkb add view dashboard   # Add a view
ttkb add dialog settings  # Add a dialog
ttkb build                # Package for distribution
```

## Widget Categories

| Category | Widgets |
|----------|---------|
| **Actions** | Button, DropdownButton, MenuButton, ContextMenu, ButtonGroup |
| **Inputs** | TextEntry, PasswordEntry, PathEntry, NumericEntry, Scale, DateEntry, TimeEntry |
| **Selection** | CheckButton, RadioButton, ToggleGroup, OptionMenu, SelectBox, Calendar |
| **Data Display** | Label, ListView, TreeView, TableView, Badge, Progressbar, Meter, FloodGauge |
| **Layout** | Frame, PackFrame, GridFrame, LabelFrame, PanedWindow, ScrollView |
| **Navigation** | Notebook, PageStack |
| **Dialogs** | MessageDialog, ColorChooser, FontDialog, DateDialog, FormDialog, QueryDialog |
| **Overlays** | Toast, Tooltip |
| **Forms** | Form, Field with validation support |

## Why ttkbootstrap?

ttkbootstrap is for developers who want to:

- Build desktop apps that feel modern and intentional
- Move fast without reinventing UI patterns
- Maintain visual consistency across applications
- Apply reactive and declarative patterns in Tk
- Ship polished tools to end users

You don't need to deeply understand Tk or ttk internals to be productive with ttkbootstrap.

## Links

- **Documentation**: https://ttkbootstrap.com
- **GitHub**: https://github.com/israel-dryer/ttkbootstrap
- **Icons**: https://github.com/israel-dryer/ttkbootstrap-icons

## Support

This project is proudly developed with the support of the
<a href="https://www.jetbrains.com/pycharm/" target="_blank" rel="noopener">PyCharm IDE</a>, generously provided by JetBrains.

<a href="https://www.jetbrains.com/" target="_blank" rel="noopener"> <picture> <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/f6d4e79d-97f4-4368-a944-affd423aa922"> <img width="250" alt="JetBrains logo" src="https://github.com/user-attachments/assets/1e42e5db-ffb5-4c8d-b238-3f5633fb7e6d"> </picture> </a>

<sub> © 2025 JetBrains s.r.o. JetBrains and the JetBrains logo are registered trademarks of JetBrains s.r.o. </sub>