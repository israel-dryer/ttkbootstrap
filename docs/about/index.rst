About
=====

.. note::

   **Draft.** This page carries over the "About this project" blurb from the 1.x
   site as a starting point — expand and sharpen it for 2.0.

ttkbootstrap is a theming extension for tkinter. It generates modern, flat,
Bootstrap-inspired themes on demand and adds a single ``bootstyle`` keyword to
the widgets you already use, so a standard tkinter app can look current without
a rewrite.

Why it exists
-------------

tkinter is everywhere — it ships with Python, it is stable, and it is the
fastest way to put a desktop window on screen. What it is *not* is modern-looking:
the default themes read as dated, and styling ttk by hand means wrestling with
element layouts, state maps, and image assets most people never want to touch.

ttkbootstrap closes that gap. It brings the look and vocabulary of Bootstrap —
semantic colors (``primary``, ``success``, ``danger`` …), light and dark themes,
flat surfaces — to the standard widget set, and it exposes them through an API
small enough to learn in a sitting:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Hello", theme="bootstrap-dark")
   ttk.Button(app, text="Save", bootstyle="success").pack(padx=16, pady=16)
   app.mainloop()

The goal is a modern desktop UI you can reach for without leaving the standard
library behind.

A styling extension, not a widget library
-----------------------------------------

ttkbootstrap is deliberately a **styling layer for vanilla tkinter**, not a new
UI framework. The widgets are tkinter's widgets; ttkbootstrap themes them and
adds a handful of conveniences. Everything you know about tkinter — geometry
managers, variables, events, the widget tree — still applies, and the
:doc:`documentation </user-guide/index>` teaches it in that dialect rather than
sending you elsewhere.

That focus is a design choice. A richer, component-oriented framework is a
separate project (bootstack); ttkbootstrap stays small, dependency-light (only
Pillow, for image-based assets), and true to the library it extends.

Where 2.0 is headed
-------------------

2.0 is a cleanup and consolidation release: a normalized API, a rebuilt theme
engine with faster theme switching and no widget leaks, a single canonical
``bootstyle`` grammar, an easier path to custom styles, and a documentation
overhaul. The through-line is the same as day one — make a standard tkinter app
look good with as little ceremony as possible.

----

ttkbootstrap is released under the :doc:`MIT License <license>`. Release notes
for every version are published on the
`GitHub releases page <https://github.com/israel-dryer/ttkbootstrap/releases>`_.

.. toctree::
   :hidden:

   Changelog <https://github.com/israel-dryer/ttkbootstrap/releases>
   license
