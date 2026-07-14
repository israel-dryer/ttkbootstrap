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

.. py:method:: place(**options)
   :noindex:

   Position the widget by coordinates. Alias: ``place_configure``.

   :param options: ``x``/``y`` (absolute pixels) or ``relx``/``rely`` (0.0–1.0
      of the parent), ``width``/``height`` or ``relwidth``/``relheight``, and
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

.. py:method:: place_slaves()
   :noindex:

   Return the widgets this container manages with place. Call on the **parent**.

   :rtype: list
