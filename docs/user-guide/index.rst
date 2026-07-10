User Guide
==========

Learn ttkbootstrap by concept: how the ``bootstyle`` grammar works, how themes
are built from semantic colors, and how to make your own styles and themes.
Start with the :doc:`Quickstart <getting-started/quickstart>`, then read the
guides in any order.

Getting Started
---------------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Quickstart
      :link: getting-started/quickstart
      :link-type: doc

      Your first themed window; ``Window`` vs ``Tk``; choosing a theme.

   .. grid-item-card:: Migrating to 2.0
      :link: getting-started/migrating
      :link-type: doc

      bootstyle strings, theme names, removed shims, and icons.

Concepts
--------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: The bootstyle grammar
      :link: concepts/bootstyle-grammar
      :link-type: doc

      **Start here.** The canonical grammar for styling any widget, with the
      full reference table.

   .. grid-item-card:: Theming
      :link: concepts/theming
      :link-type: doc

      The semantic-anchor color model and the built-in light/dark themes.

   .. grid-item-card:: Make your own style
      :link: concepts/make-your-own-style
      :link-type: doc

      The custom style-construction toolkit — assets, layouts, and icons.

   .. grid-item-card:: Make your own theme
      :link: concepts/make-your-own-theme
      :link-type: doc

      The ``Theme`` API and the ttkcreator editor.

   .. grid-item-card:: Working with color
      :link: concepts/working-with-color
      :link-type: doc

      ``style.colors`` and ramp addressing (``c.primary[300]``).

How-To
------

Task-focused recipes — see the :doc:`How-To index <how-to/index>`.

.. toctree::
   :hidden:
   :caption: Getting Started

   getting-started/quickstart
   getting-started/migrating

.. toctree::
   :hidden:
   :caption: Concepts

   concepts/bootstyle-grammar
   concepts/theming
   concepts/make-your-own-style
   concepts/make-your-own-theme
   concepts/working-with-color

.. toctree::
   :hidden:
   :caption: How-To

   how-to/index
