Below is a **design-first Markdown document** you can drop directly into a `templates/README.md`.
It explains the **app paradigms**, *when to use each*, and the **intended ttkbootstrap v2 building blocks**, without
prescribing implementation details yet.

You can treat this as the contract you’ll implement against.

---

# Application Templates

ttkbootstrap v2 supports multiple **application paradigms** rather than a single “one-true” layout.
Modern desktop applications no longer all center around a global menu bar; instead, navigation, commands,
and context are often scoped to views.

This module documents the **recommended application templates** and the design intent behind each.
These templates are not rigid frameworks — they are **starting points** that guide layout, navigation,
and command placement.

---

## 1. Classic Desktop Menu App

**Best for**

* IDEs
* Editors
* Admin / power-user tools
* Document-centric workflows

**Core idea**
A traditional desktop application with a persistent menu bar and global commands.

### Structure

* **MenuBar**

    * `before`: File / Edit / View / Tools
    * `center`: Application title or global search
    * `after`: Help, Account, About
* **Main content**

    * Single view or `PageStack`
* **Optional StatusBar**

    * Application state, selection info, messages

### Command strategy

* Global commands live in the MenuBar
* Contextual actions use ContextMenu
* Optional page-level CommandBars may exist but are secondary

### Notes

* MenuBar is chrome, not a toolbar
* Best for keyboard-heavy workflows
* Matches classic Windows, IDE, and legacy desktop expectations

---

## 2. Modern Navigation App (Side Navigation)

**Best for**

* Dashboards
* Settings applications
* View-based business apps
* Modern “WinUI-style” applications

**Core idea**
Navigation defines *where you are*; commands are scoped to the current page.

### Structure

* **NavigationView** (left rail)

    * Groups and items
    * Optional compact mode
* **PageStack**

    * One page visible at a time
* **Page header**

    * Page title
    * Page-scoped CommandBar

### Command strategy

* No global MenuBar by default
* Commands appear in page headers
* Secondary actions via ContextMenu or overflow menus

### Notes

* This is the dominant WinUI / modern desktop pattern
* Reduces global clutter
* Encourages contextual thinking

---

## 3. Top Tab Navigation App

**Best for**

* Apps with a small number of peer sections
* Monitoring dashboards
* Configuration panels

**Core idea**
Tabs act as the primary navigation mechanism.

### Structure

* **Optional header**

    * App title and utilities
* **TabView / Notebook**

    * Each tab hosts a page
* **Per-tab content**

    * Optional CommandBar inside each tab

### Command strategy

* Commands are scoped to the active tab
* Context menus for local actions
* MenuBar is optional and often unnecessary

### Notes

* Works best with 3–7 top-level sections
* Avoid nesting tabs inside tabs

---

## 4. Master–Detail App

**Best for**

* Email clients
* File browsers
* CRUD and data-management apps

**Core idea**
A persistent list on one side, details on the other.

### Structure

* **Header**

    * Optional search and filters
* **Splitter**

    * Left: list / tree / selectbox
    * Right: detail view (forms, previews, inspectors)

### Command strategy

* List actions via CommandBar above the list
* Item actions via ContextMenu
* Detail view actions scoped to the detail panel

### Notes

* One of the most common enterprise layouts
* Supports high-density data workflows

---

## 5. Document Workspace App

**Best for**

* Code editors
* Design tools
* Multi-document applications

**Core idea**
Multiple open documents with surrounding tools.

### Structure

* **MenuBar** (classic)
* **Optional toolbar / CommandBar**
* **TabView**

    * One tab per document
* **Optional side panels**

    * Toolboxes, inspectors, logs

### Command strategy

* Global commands in MenuBar
* Document-specific commands in toolbars
* Context menus inside editors

### Notes

* Heavy, flexible layout
* Requires careful state management

---

## 6. Wizard / Step-Based App

**Best for**

* Installers
* Setup workflows
* Guided multi-step tasks

**Core idea**
Linear progression through a fixed set of steps.

### Structure

* **Minimal header**

    * Title and close button
* **PageStack**

    * One step per page
* **Footer**

    * Back / Next / Finish actions

### Command strategy

* Commands are strictly scoped to the current step
* Validation gates progression

### Notes

* Avoid global navigation
* Strong focus on clarity and flow

---

## 7. Dialog-First Utility App

**Best for**

* Small utilities
* Single-purpose tools
* Modal or tool-like applications

**Core idea**
Minimal chrome, focused task.

### Structure

* **Simple header**

    * Title and close
* **Single composite panel**

    * Forms, previews, controls

### Command strategy

* Buttons and toggles inside the view
* Context menus for advanced options

### Notes

* Fast to build
* Ideal for standalone tools

---

## Choosing the Right Template

| If your app…                      | Use this template    |
|-----------------------------------|----------------------|
| Has global File/Edit workflows    | Classic Desktop Menu |
| Is view-driven with many sections | Navigation App       |
| Has few peer sections             | Top Tabs             |
| Works on lists and records        | Master–Detail        |
| Handles many open documents       | Document Workspace   |
| Is step-based                     | Wizard               |
| Does one thing well               | Dialog-First Utility |

---

## Design Philosophy

* **MenuBar is optional**, not mandatory
* **Commands should be scoped** whenever possible
* **Context menus are first-class**
* **Chrome should be quiet**
* Layout should serve *workflow*, not tradition

These templates are intentionally **composable** — real applications may blend patterns as needed.

---

If you want, next I can:

* Refine this into a MkDocs-ready page
* Add ASCII layout diagrams per template
* Generate a stub folder structure for each template
* Write “anti-patterns” (what *not* to do)

Just say the word.
