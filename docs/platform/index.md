# Platform

The **Platform** section explains how ttkbootstrap builds on top of Tk and ttk to provide
a consistent, modern application foundation.

This section is not widget documentation.
Instead, it describes the **runtime model**, **event system**, **styling architecture**,
and **system-level behaviors** that apply across all widgets and applications built with
ttkbootstrap.

If you are new to Tk or ttk, these pages will help you understand the underlying concepts.
If you are experienced with Tk, this section explains what ttkbootstrap standardizes,
extends, or intentionally constrains.

---

## What ttkbootstrap is (and is not)

ttkbootstrap is **not** just a theme.

It is a framework that provides:

- a structured application runtime
- a unified styling and theming system
- consistent handling of images, fonts, and DPI
- built-in localization and formatting support
- predictable interaction and layout behavior

ttkbootstrap does **not** replace Tk or ttk.
It builds on them and embraces their strengths, while smoothing over their rough edges.

---

## How to use this section

Start here if you want to understand:

- how applications are created and managed
- how the event loop and event delivery work
- how widgets are created, updated, and destroyed
- how layout and geometry behave at runtime
- how styles, assets, and localization are applied

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

The Platform section covers:

- **Fundamentals**
    - Tk vs ttk
      - the event loop
      - event delivery and bindings
      - widget lifecycle
      - geometry and layout
- **Styling internals**
    - ttk styles and elements
- **Windows**
    - top-level windows and modality
- **Rendering**
    - images, DPI, and scaling
- **Operations**
    - performance considerations
      - debugging techniques

Together, these topics define the foundation on which all ttkbootstrap applications are built.
