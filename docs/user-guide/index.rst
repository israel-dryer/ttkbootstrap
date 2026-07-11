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

Each subsystem, end to end — the utilities that work on plain tkinter, not just
ttkbootstrap widgets.

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

   .. grid-item-card:: Windows, icons & high-DPI
      :link: feature-guides/windows
      :link-type: doc

      ``App``/``Toplevel``, positioning, application icons, and DPI scaling.

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
   feature-guides/windows

.. toctree::
   :hidden:
   :caption: How-To

   how-to/index
