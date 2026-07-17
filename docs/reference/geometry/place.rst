Place
=====

The **place** geometry manager positions a widget by absolute or relative
coordinates. This page is the method spec; :doc:`Arranging widgets
</user-guide/foundations/arranging-widgets>` teaches when to reach for place.

In ttkbootstrap ``place`` (and ``place_configure``) return the widget, so
construction and placement can be chained.

The canonical upstream reference is the Tk
`place <https://www.tcl-lang.org/man/tcl8.6/TkCmd/place.htm>`__ manual page
(Tcl 8.6).

Options
-------

Every option below is a keyword argument to ``place()``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``x`` / ``y``
     - ``int``
     - The anchor point's position, in pixels from the parent's top-left
       corner.
   * - ``relx`` / ``rely``
     - ``float``
     - The anchor point's position as a fraction of the parent's size,
       ``0.0``–``1.0``. Combines with ``x`` / ``y``, which then act as a
       pixel offset.
   * - ``width`` / ``height``
     - ``int``
     - The widget's size, in pixels.
   * - ``relwidth`` / ``relheight``
     - ``float``
     - The widget's size as a fraction of the parent's size, ``0.0``–``1.0``.
       Combines with ``width`` / ``height`` as a pixel adjustment.
   * - ``anchor``
     - ``str``
     - Which point of the *widget* is placed at the given position:
       ``"nw"`` (default), ``"center"``, ``"se"``, ….
   * - ``bordermode``
     - ``str``
     - Whether coordinates are measured ``"inside"`` (default) or
       ``"outside"`` the parent's border.
   * - ``in_``
     - ``Widget``
     - Place relative to a container other than the parent. Rarely needed.

Methods
-------

.. py:method:: place(**options)
   :noindex:

   Position the widget by coordinates, using the options above. Alias:
   ``place_configure``.

   :returns: the widget (ttkbootstrap), for chaining.

.. py:method:: place_forget()
   :noindex:

   Unmap the widget.

   :returns: ``None``.

.. py:method:: place_info()
   :noindex:

   Return the widget's current place options.

   :rtype: dict

.. py:method:: place_slaves()
   :noindex:

   Return the widgets this container manages with place. Call on the **parent**.

   :rtype: list
