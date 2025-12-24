# Platform

The **Platform** section explains how ttkbootstrap builds on top of Tk and ttk to provide
a consistent, modern application foundation.

This is not widget documentation.
Instead, these pages describe the **runtime model**, **styling model**, and **system-level
behaviors** that apply across all widgets and applications built with ttkbootstrap.

If you are new to Tk or ttk, this section will help you understand the underlying concepts.
If you are experienced with Tk, this section explains what ttkbootstrap standardizes,
extends, or intentionally constrains.

---

## What ttkbootstrap is (and is not)

ttkbootstrap is **not** just a theme.
It is a framework that provides:

- a structured application runtime (`App`)
- a unified styling and theming system
- consistent handling of assets, fonts, and DPI
- built-in localization and formatting support
- predictable interaction patterns across widgets

ttkbootstrap does **not** replace Tk or ttk.
It builds on them and embraces their strengths, while smoothing over their rough edges.

---

## How to use this section

Start here if you want to understand:

- how applications are created and managed
- how windows, menus, and dialogs fit together
- how themes and bootstyles are resolved
- how images and fonts behave at runtime
- how localization works at the platform level

For **how to use a specific widget**, see the Widgets section.
For **exact APIs and signatures**, see the API Reference.

---

## Relationship to Tk and ttk

Many concepts described here originate in Tk itself:
the event loop, geometry managers, widget lifecycles, and windowing behavior.

Where appropriate, these pages reference external resources such as:

- Python’s `tkinter` documentation
- the TkDocs tutorial

Those resources explain *how Tk works*.
The Platform section explains **how ttkbootstrap expects you to work with Tk**.

---

## Platform topics

- **Application**
    - the `App` object and runtime lifecycle
    - windows and menus
- **Styling**
    - themes, bootstyles, and assets
- **Localization**
    - message catalogs and formatting

Together, these topics define the foundation on which all ttkbootstrap applications are built.
