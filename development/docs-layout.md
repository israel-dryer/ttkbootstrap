# ttkbootstrap 2 Docs - Final Navigation & Information Architecture

This document captures the finalized navigation design for the ttkbootstrap 2 documentation site, reflecting decisions aligned with discoverability while remaining Tk-native.

## Core principles

### Top navigation = primary modes
- Maximum 6 items.
- Optimized for repeat visits.
- Answers the question: What kind of thing am I looking for?

### Sidebar navigation = content depth
- Contextual to the selected top-level mode.
- Maximum three levels deep.
- Categories are index pages, not containers.

> Rule: Classification lives inside pages. Navigation stays shallow.

## Final top navigation (locked)
```
Getting Started | Widgets | Design | Guides | Reference | Showcase
```

## Getting Started (sidebar)
```
Getting Started
- What is ttkbootstrap 2?
- Why ttkbootstrap 2?
- Quickstart (5-Minute App)
- Installation
- First Application
- Project Templates
- Learning Resources
- Community & Support
```

## Widgets (sidebar - catalog-first)
All widgets are directly reachable. Categories serve as landing pages that link to widgets.

```
Widgets
- Overview
- Inputs
- Data Display
- Feedback
- Layout
- Navigation
- Dialogs
- Button
- Checkbutton
- Radiobutton
- Entry
- Combobox
- Spinbox
- Scale
- SelectBox
- PasswordEntry
- NumericEntry
- DateEntry
- TimeEntry
- PathEntry
- DropDownButton
- SpinnerEntry
- Label
- Meter
- FloodGauge
- Progressbar
- Treeview
- TableView
- Tooltip
- Toast
- Frame
- Labelframe
- Panedwindow
- ScrollView
- ScrolledText
- Scrollbar
- Separator
- Sizegrip
- LabeledScale
- Notebook
- PageStack
- ContextMenu
- MenuButton
- OptionMenu
```

## Dialogs (Widgets + Dialogs)

Single page with internal sections:

- **Base dialogs**: Dialog, MessageDialog, QueryDialog.
- **Helpers**: MessageBox, QueryBox.
- **Pickers**: ColorChooser, ColorDropper, DateDialog.
- **Advanced**: FormDialog, FilterDialog.

## Design (sidebar)
```
Design
- Design System Overview
- Variants & States
- Color System
- Typography
- Iconography
- Layout System
- Theming
- Localization
```

## Guides (sidebar)
```
Guides
- Application Runtime
- App Configuration
- Theming & Appearance
- State & Signals
- Events & Virtual Events
- Data & Validation
- Forms & Dialog Patterns
- Distribution & Packaging
- Testing & Architecture
```

## Reference (sidebar)
```
Reference
- API Reference
- Utilities
  - Application Utilities
  - Theme Utilities
  - Style Utilities
- CLI Tools
- Migration
  - Overview
  - v1 + v2 Guide
  - Breaking Changes
- FAQ & Troubleshooting
```

## Showcase (sidebar)
```
Showcase
- Gallery
- Templates in Action
- Community Projects
- Case Studies
```

## Footer (recommended)
- GitHub repository
- PyPI
- Discussions / Discord
- License
- Changelog
- Version selector (v1 / v2)

## Final constraints (do not break)
- Top navigation stays at 6 items.
- Sidebar depth stays at three levels.
- Widgets remain first-class citizens.
- Categories never nest widgets.
- Dialogs never create subtrees.

This structure is designed to scale with ttkbootstrap 2 while remaining approachable, discoverable, and professional.
