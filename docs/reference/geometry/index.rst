Geometry
========

The **geometry managers** — how a widget gets a size and position inside its
parent. Each page is a method spec (signatures, parameters, return types);
:doc:`Arranging widgets </user-guide/foundations/arranging-widgets>` teaches when
to reach for each.

A widget is only drawn once one of these places it, and a single container should
use **one** manager for its direct children (pack *or* grid, not both). Stacking
order then decides which widget wins where two overlap.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Pack
      :link: pack
      :link-type: doc

      Stack a widget against a side of its parent.

   .. grid-item-card:: Grid
      :link: grid
      :link-type: doc

      Place widgets in rows and columns, and shape the container.

   .. grid-item-card:: Place
      :link: place
      :link-type: doc

      Position a widget by absolute or relative coordinates.

   .. grid-item-card:: Stacking order
      :link: stacking
      :link-type: doc

      Raise and lower overlapping widgets — ``lift``, ``lower``.

.. toctree::
   :hidden:

   pack
   grid
   place
   stacking
