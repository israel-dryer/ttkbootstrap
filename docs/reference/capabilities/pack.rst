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

.. py:method:: pack(**options)
   :noindex:

   Place the widget against a side of its parent. Alias: ``pack_configure``.

   :param options: ``side`` (``"top"``/``"bottom"``/``"left"``/``"right"``),
      ``fill`` (``"x"``/``"y"``/``"both"``), ``expand`` (bool), ``anchor``,
      ``padx``/``pady`` (external), ``ipadx``/``ipady`` (internal).
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
