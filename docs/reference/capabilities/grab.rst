Grab
====

A **grab** routes all input events to one widget (and its descendants), which is
how a modal dialog blocks the rest of the application until it is dismissed.

The canonical upstream reference is the Tk
`grab <https://www.tcl-lang.org/man/tcl8.6/TkCmd/grab.htm>`__ manual page
(Tcl 8.6).

.. py:method:: grab_set()
   :noindex:

   Make this widget the **local** grab holder: events for this application are
   directed to it and its descendants until the grab is released.

   :returns: ``None``.

.. py:method:: grab_set_global()
   :noindex:

   Make this widget the **global** grab holder: events for the whole screen —
   every application — are directed to it. Use rarely; it locks out the user's
   other windows.

   :returns: ``None``.

.. py:method:: grab_release()
   :noindex:

   Release this widget's grab.

   :returns: ``None``.

.. py:method:: grab_current()
   :noindex:

   Return the widget in this application that currently holds a grab.

   :returns: the grab holder, or ``None`` if there is none.
   :rtype: Misc | None

.. py:method:: grab_status()
   :noindex:

   Report this widget's grab state.

   :returns: ``"local"``, ``"global"``, or ``None`` if this widget has no grab.
   :rtype: str | None
