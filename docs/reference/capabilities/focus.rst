Focus
=====

Keyboard **focus** decides which widget receives key events. Every widget carries
these methods to query and move it. Setting focus is per–toplevel: a widget takes
focus within its window, and the window in turn has focus within the display.

The canonical upstream references are the Tk
`focus <https://www.tcl-lang.org/man/tcl8.6/TkCmd/focus.htm>`__ and
`tk_focusNext <https://www.tcl-lang.org/man/tcl8.6/TkCmd/focusNext.htm>`__ manual
pages (Tcl 8.6).

Setting focus
-------------

.. py:method:: focus_set()
   :noindex:

   Give this widget the keyboard focus the next time its toplevel window has
   focus. Alias: ``focus()``.

   :returns: ``None``.

.. py:method:: focus_force()
   :noindex:

   Take the focus immediately, even if the application's window does not have
   focus. Disruptive — prefer ``focus_set`` unless you specifically need to steal
   focus.

   :returns: ``None``.

Querying focus
--------------

.. py:method:: focus_get()
   :noindex:

   Return the widget that currently has focus in this application.

   :returns: the focused widget, or ``None`` if no widget in this application has
      focus.
   :rtype: Misc | None

.. py:method:: focus_displayof()
   :noindex:

   Like ``focus_get``, but resolves focus on the display this widget belongs to
   (relevant only with multiple displays).

   :returns: the focused widget on this display, or ``None``.
   :rtype: Misc | None

.. py:method:: focus_lastfor()
   :noindex:

   Return the widget that would receive the focus if this widget's toplevel
   regained it — the one that held focus there most recently.

   :returns: the widget that last had focus in this toplevel (the toplevel itself
      if none did).
   :rtype: Misc

Traversal order
---------------

.. py:method:: tk_focusNext()
   :noindex:

   Return the next widget after this one in keyboard-traversal (Tab) order,
   honoring each widget's ``takefocus`` setting.

   :returns: the next widget in traversal order.
   :rtype: Misc

.. py:method:: tk_focusPrev()
   :noindex:

   Return the previous widget before this one in traversal (Shift-Tab) order.

   :returns: the previous widget in traversal order.
   :rtype: Misc

.. py:method:: tk_focusFollowsMouse()
   :noindex:

   Switch this application to a focus-follows-mouse model, where focus tracks the
   pointer instead of requiring a click. There is no call to undo it.

   :returns: ``None``.
