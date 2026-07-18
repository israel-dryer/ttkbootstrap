:html_theme.sidebar_secondary.remove: true

ttkbootstrap
============

.. rst-class:: tb-lead

Modern, themed tkinter — style any ttk widget with one keyword.

ttkbootstrap is a theming extension for tkinter. It generates flat,
Bootstrap-inspired light and dark themes on demand and adds a single
``bootstyle`` keyword to every ttk widget, so you describe *intent*
("primary", "success", "outline") instead of hand-picking colors.

.. container:: hero-ctas

   .. button-ref:: user-guide/getting-started/quickstart
      :ref-type: doc
      :color: primary
      :class: sd-px-4 sd-fs-5

      Get started

   .. button-ref:: widgets/index
      :ref-type: doc
      :color: secondary
      :outline:
      :class: sd-px-4 sd-fs-5

      Browse widgets

.. note::

   **ttkbootstrap 2.0 is in development.** These docs are being rebuilt to
   match. Screenshots and the full catalog land in later documentation slices;
   the structure you see here is the new information architecture.

Why ttkbootstrap
----------------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: :octicon:`paintbrush;1.5em;sd-mr-1` Semantic styling

      One keyword does it: ``bootstyle="primary"``, ``bootstyle="success outline"``.
      Describe intent, not hex codes — the same code looks right across 30 light
      and dark themes and re-themes at runtime.

   .. grid-item-card:: :octicon:`stack;1.5em;sd-mr-1` Styles vanilla tkinter

      ttkbootstrap is an *extension*, not a new toolkit. It styles the ttk
      widgets you already know — ``Button``, ``Entry``, ``Treeview`` — plus a
      few batteries-included extras like ``Meter`` and ``DateEntry``.

   .. grid-item-card:: :octicon:`check-circle;1.5em;sd-mr-1` Looks right by default

      Flat, modern themes with sensible spacing and a coherent color system, so
      an app looks polished before you touch a single style option.

   .. grid-item-card:: :octicon:`package;1.5em;sd-mr-1` Pure Python

      One runtime dependency (Pillow). Requires Python 3.10+. No native
      extensions, no heavy runtime.

A glimpse
---------

A themed window is a handful of lines — every widget takes ``bootstyle``:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Hello", theme="bootstrap-light")

   ttk.Label(app, text="Hello from ttkbootstrap!").pack(padx=16, pady=(16, 8))
   ttk.Button(app, text="Primary", bootstyle="primary").pack(padx=16, pady=4)
   ttk.Button(app, text="Success", bootstyle="success").pack(padx=16, pady=4)
   ttk.Button(app, text="Danger Outline", bootstyle="danger outline").pack(padx=16, pady=(4, 16))

   app.mainloop()

Start here
----------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: :octicon:`rocket;1.5em;sd-mr-1` Quick Start
      :link: user-guide/getting-started/quickstart
      :link-type: doc

      Your first themed window in a few lines.

   .. grid-item-card:: :octicon:`book;1.5em;sd-mr-1` User Guide
      :link: user-guide/index
      :link-type: doc

      The bootstyle grammar, theming, and making your own styles and themes.

   .. grid-item-card:: :octicon:`apps;1.5em;sd-mr-1` Widgets
      :link: widgets/index
      :link-type: doc

      The visual catalog — every widget ttkbootstrap styles or ships.

   .. grid-item-card:: :octicon:`code;1.5em;sd-mr-1` Reference
      :link: reference/index
      :link-type: doc

      The per-widget API and styling reference, capabilities, and cursors.

Install
-------

ttkbootstrap requires Python 3.10 or newer. Install it with pip:

.. code-block:: bash

   pip install ttkbootstrap

.. toctree::
   :hidden:
   :maxdepth: 2

   user-guide/index
   widgets/index
   reference/index
   themes
   release-notes
