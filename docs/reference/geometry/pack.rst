Pack
====

The **pack** geometry manager places a widget by stacking it against one side of
its parent. This page is the method spec; :doc:`Arranging widgets
</user-guide/foundations/arranging-widgets>` teaches when to reach for pack.

In ttkbootstrap ``pack`` (and ``pack_configure``) return the widget, so
construction and placement can be chained.

The canonical upstream reference is the Tk
`pack <https://www.tcl-lang.org/man/tcl8.6/TkCmd/pack.htm>`__ manual page
(Tcl 8.6).

Options
-------

Every option below is a keyword argument to ``pack()``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``side``
     - ``str``
     - The side of the remaining space the widget stacks against: ``"top"``
       (default), ``"bottom"``, ``"left"``, or ``"right"``.
   * - ``fill``
     - ``str``
     - Stretch the widget to fill its slot: ``"x"``, ``"y"``, ``"both"``, or
       ``"none"`` (default).
   * - ``expand``
     - ``bool``
     - Claim a share of the parent's leftover space — the *slot* grows; pair
       with ``fill`` so the widget grows with it.
   * - ``anchor``
     - ``str``
     - Where the widget sits inside its slot when it does not fill it:
       ``"center"``, a side (``"n"``/``"s"``/``"e"``/``"w"``), or a corner
       (``"ne"``, ``"sw"``, …).
   * - ``padx`` / ``pady``
     - ``int | tuple``
     - External space around the widget, in pixels. A ``(left, right)`` /
       ``(top, bottom)`` tuple pads the two sides differently.
   * - ``ipadx`` / ``ipady``
     - ``int``
     - Internal padding added to the widget's own size, in pixels.
   * - ``before`` / ``after``
     - ``Widget``
     - Insert the widget into the packing order relative to a sibling that is
       already packed.
   * - ``in_``
     - ``Widget``
     - Pack inside a container other than the parent (the container must be
       the parent or one of its descendants). Rarely needed.

Methods
-------

.. py:method:: pack(**options)
   :noindex:

   Place the widget against a side of its parent, using the options above.
   Alias: ``pack_configure``.

   :returns: the widget (ttkbootstrap), for chaining.

.. py:method:: pack_forget()
   :noindex:

   Unmap the widget; it keeps existing and can be re-packed later.

   :returns: ``None``.

.. py:method:: pack_info()
   :noindex:

   Return the widget's current pack options.

   :rtype: dict

.. py:method:: pack_propagate(flag=None)
   :noindex:

   Get or set whether this container shrinks/grows to fit the widgets packed
   inside it. Call on the **parent**. Set ``False`` to keep a fixed size
   regardless of children.

   :param bool flag: the new setting; omit to query the current one.
   :returns: the current setting when queried, else ``None``.

.. py:method:: pack_slaves()
   :noindex:

   Return the widgets this container manages with pack, in packing order. Call on
   the **parent**.

   :rtype: list
