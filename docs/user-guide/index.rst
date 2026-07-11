User Guide
==========

Learn ttkbootstrap by working through it: set up and build your first window,
grasp the core styling concepts (the ``bootstyle`` grammar and how styling is
delivered), reach for a feature guide when you need a whole subsystem — fonts,
localization, validation, windowing — or grab a how-to when you have a specific
task in mind. For the complete lookup of every public name see the
:doc:`API Reference </reference/api/index>`; for the visual widget catalog see
:doc:`Widgets </widgets/index>`.

Getting Started
---------------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Installation
      :link: getting-started/installation
      :link-type: doc

      Install from PyPI; supported Python versions.

   .. grid-item-card:: Quickstart
      :link: getting-started/quickstart
      :link-type: doc

      Your first themed window; ``App`` vs ``Tk``; choosing a theme.

   .. grid-item-card:: Structuring an app
      :link: getting-started/app-structures
      :link-type: doc

      ``App`` vs ``Tk``, the single-root rule, and a real app skeleton.

   .. grid-item-card:: Migrating to 2.0
      :link: getting-started/migrating
      :link-type: doc

      bootstyle strings, theme names, removed shims, and icons.

Foundations
-----------

New to tkinter? These pages cover the mental models everything else builds on —
how an app runs, how widgets are arranged, how they bind to your data, and how
they respond to input.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: How a tkinter app runs
      :link: foundations/how-a-tkinter-app-runs
      :link-type: doc

      The event loop, ``mainloop``, callbacks, ``after``, and not freezing the UI.

   .. grid-item-card:: The widget model
      :link: foundations/the-widget-model
      :link-type: doc

      The widget tree, options (``configure``/``cget``), and ttk states.

   .. grid-item-card:: Arranging widgets
      :link: foundations/arranging-widgets
      :link-type: doc

      The three geometry managers and when to use each — start here, then the
      grid and pack tutorials.

   .. grid-item-card:: State & variables
      :link: foundations/state-and-variables
      :link-type: doc

      Binding widgets to ``StringVar``/``IntVar``/``BooleanVar`` and reacting to
      changes.

   .. grid-item-card:: Events & callbacks
      :link: foundations/events-and-callbacks
      :link-type: doc

      ``command``, ``bind`` and event objects, virtual events, and ``after``.

Concepts
--------

The styling core. **Start with the bootstyle grammar**, then read the rest in
any order.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: The bootstyle grammar
      :link: concepts/bootstyle-grammar
      :link-type: doc

      **Start here.** The canonical grammar for styling any widget, with the
      full reference table.

   .. grid-item-card:: How styling is delivered
      :link: concepts/delivery-model
      :link-type: doc

      How the ``bootstyle`` API reaches your widgets — the blessed subclasses,
      ``enable_global_api``, ``bootify``, and ``apply_bootstyle``.

   .. grid-item-card:: Theming
      :link: concepts/theming
      :link-type: doc

      The semantic-anchor color model and the built-in light/dark themes.

   .. grid-item-card:: Working with color
      :link: concepts/working-with-color
      :link-type: doc

      ``style.colors`` and ramp addressing (``c.primary[300]``).

   .. grid-item-card:: Make your own style
      :link: concepts/make-your-own-style
      :link-type: doc

      The custom style-construction toolkit — assets, layouts, and icons.

   .. grid-item-card:: Make your own theme
      :link: concepts/make-your-own-theme
      :link-type: doc

      The ``Theme`` API and the ttkcreator editor.

Feature guides
--------------

Each subsystem, end to end — its concepts and its usage in one place.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Typography
      :link: feature-guides/typography
      :link-type: doc

      ``Fonts`` and ``set_global_family`` over the standard named fonts.

   .. grid-item-card:: Localization
      :link: feature-guides/localization
      :link-type: doc

      ``L()``, ``LocaleVar``, ``set_locale``, and live language switching.

   .. grid-item-card:: Input validation
      :link: feature-guides/validation
      :link-type: doc

      ``add_*_validation`` helpers and the ``@validator`` decorator.

   .. grid-item-card:: Icons
      :link: feature-guides/icons
      :link-type: doc

      Theme-aware Bootstrap Icons glyphs — the ``icon=`` keyword, ``apply_icon``,
      and the standalone ``Icon`` image.

   .. grid-item-card:: Windows & high-DPI
      :link: feature-guides/windows
      :link-type: doc

      ``App``/``Toplevel``, focus & modality, positioning, application icons, and
      DPI scaling.

How-To
------

Task-focused recipes — common tkinter jobs done the ttkbootstrap way. See the
:doc:`How-To index <how-to/index>`.

.. toctree::
   :hidden:
   :caption: Getting Started

   getting-started/installation
   getting-started/quickstart
   getting-started/app-structures
   getting-started/migrating

.. toctree::
   :hidden:
   :caption: Foundations

   foundations/how-a-tkinter-app-runs
   foundations/the-widget-model
   foundations/arranging-widgets
   foundations/layout-with-grid
   foundations/layout-with-pack
   foundations/state-and-variables
   foundations/events-and-callbacks

.. toctree::
   :hidden:
   :caption: Concepts

   concepts/bootstyle-grammar
   concepts/delivery-model
   concepts/theming
   concepts/working-with-color
   concepts/make-your-own-style
   concepts/make-your-own-theme

.. toctree::
   :hidden:
   :caption: Feature guides

   feature-guides/typography
   feature-guides/localization
   feature-guides/validation
   feature-guides/icons
   feature-guides/windows

.. toctree::
   :hidden:
   :caption: How-To

   how-to/index
   how-to/working-with-images
   how-to/feedback
   how-to/multiple-windows
