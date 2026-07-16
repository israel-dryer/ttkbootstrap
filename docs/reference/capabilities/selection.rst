Selection
=========

The **selection** is the highlighted text shared between applications (the
``PRIMARY`` selection on X11; also used for a widget's own highlighted range).
These methods read it, clear it, and claim ownership of it.

The canonical upstream reference is the Tk
`selection <https://www.tcl-lang.org/man/tcl8.6/TkCmd/selection.htm>`__ manual
page (Tcl 8.6).

.. py:method:: selection_get(**kw)
   :noindex:

   Return the current selection.

   :param kw: ``selection=`` names which selection (default ``"PRIMARY"``);
      ``type=`` the requested data form.
   :returns: the selected text.
   :rtype: str
   :raises tkinter.TclError: if there is no selection.

.. py:method:: selection_clear(**kw)
   :noindex:

   Clear the selection this widget owns.

   :param kw: ``selection=`` names which selection to clear.
   :returns: ``None``.

.. py:method:: selection_own(**kw)
   :noindex:

   Make this widget the owner of the selection.

   :param kw: ``selection=`` names which selection to claim; ``command=`` a
      callback invoked if ownership is later lost.
   :returns: ``None``.

.. py:method:: selection_own_get(**kw)
   :noindex:

   Return the widget that currently owns the selection.

   :param kw: ``selection=`` names which selection to query.
   :returns: the owning widget.
   :rtype: Misc
   :raises tkinter.TclError: if no widget in this application owns it.

.. py:method:: selection_handle(command, **kw)
   :noindex:

   Supply the selection's contents on demand: register ``command`` to be called
   when another application asks this widget for the selection it owns. Tk calls
   it with an offset and a maximum byte count, and it returns that slice of the
   value. Use it when the selection is large or generated — for a plain string,
   owning the selection is enough.

   :param command: called as ``command(offset, length)``; returns the requested
      slice as a string.
   :param kw: ``selection=`` names which selection, ``type=`` the target form.
   :returns: ``None``.
