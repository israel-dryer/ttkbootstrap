Geometry
========

A widget becomes visible only when a **geometry manager** places it in its
parent. There are three — ``pack``, ``grid``, and ``place`` — and a widget uses
one at a time. This page is the method spec; :doc:`Arranging widgets
</user-guide/foundations/arranging-widgets>` teaches when to reach for each.

In ttkbootstrap ``pack``/``grid``/``place`` (and their ``*_configure`` spellings)
return the widget, so construction and placement can be chained.

The canonical upstream references are the Tk
`pack <https://www.tcl-lang.org/man/tcl8.6/TkCmd/pack.htm>`__,
`grid <https://www.tcl-lang.org/man/tcl8.6/TkCmd/grid.htm>`__, and
`place <https://www.tcl-lang.org/man/tcl8.6/TkCmd/place.htm>`__ manual pages
(Tcl 8.6).

Pack
----

.. py:method:: pack(**options)
   :noindex:

   Place the widget by stacking it against a side of its parent. Alias:
   ``pack_configure``.

   :param options: ``side`` (``"top"``/``"bottom"``/``"left"``/``"right"``),
      ``fill`` (``"x"``/``"y"``/``"both"``), ``expand``, ``anchor``,
      ``padx``/``pady``, ``ipadx``/``ipady``.
   :returns: the widget (ttkbootstrap), for chaining.

.. py:method:: pack_forget()
   :noindex:

   Unmap the widget; it keeps existing and can be re-added later.

   :returns: ``None``.

.. py:method:: pack_info()
   :noindex:

   Return the widget's current pack options.

   :rtype: dict

Grid
----

.. py:method:: grid(**options)
   :noindex:

   Place the widget in a row/column grid in its parent. Alias:
   ``grid_configure``.

   :param options: ``row``, ``column``, ``rowspan``, ``columnspan``,
      ``sticky`` (any of ``"nsew"``), ``padx``/``pady``, ``ipadx``/``ipady``.
   :returns: the widget (ttkbootstrap), for chaining.

.. py:method:: grid_forget()
   :noindex:

   Unmap the widget and forget its grid options.

   :returns: ``None``.

.. py:method:: grid_remove()
   :noindex:

   Unmap the widget but **remember** its grid options, so a later ``grid()`` with
   no arguments restores it in place.

   :returns: ``None``.

.. py:method:: grid_info()
   :noindex:

   Return the widget's current grid options.

   :rtype: dict

Place
-----

.. py:method:: place(**options)
   :noindex:

   Position the widget by absolute or relative coordinates. Alias:
   ``place_configure``.

   :param options: ``x``/``y`` (absolute) or ``relx``/``rely`` (0.0–1.0 of the
      parent), ``width``/``height`` or ``relwidth``/``relheight``, and
      ``anchor``.
   :returns: the widget (ttkbootstrap), for chaining.

.. py:method:: place_forget()
   :noindex:

   Unmap the widget.

   :returns: ``None``.

.. py:method:: place_info()
   :noindex:

   Return the widget's current place options.

   :rtype: dict

Stacking order
--------------

.. py:method:: lift(aboveThis=None)
   :noindex:

   Raise the widget above its siblings, or above one specific sibling. Alias:
   ``tkraise``.

   :param aboveThis: the sibling to raise above; if omitted, raises to the top.
   :returns: ``None``.

.. py:method:: lower(belowThis=None)
   :noindex:

   Lower the widget below its siblings, or below one specific sibling.

   :param belowThis: the sibling to lower below; if omitted, lowers to the
      bottom.
   :returns: ``None``.
