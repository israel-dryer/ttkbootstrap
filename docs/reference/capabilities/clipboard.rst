Clipboard & selection
=====================

Every widget can read and write the system **clipboard** and the current
**selection** (the highlighted text handed between applications). For a worked
copy/paste flow, see :doc:`Copy to the clipboard
</user-guide/how-to/clipboard>`.

The canonical upstream references are the Tk
`clipboard <https://www.tcl-lang.org/man/tcl8.6/TkCmd/clipboard.htm>`__ and
`selection <https://www.tcl-lang.org/man/tcl8.6/TkCmd/selection.htm>`__ manual
pages (Tcl 8.6).

Clipboard
---------

.. py:method:: clipboard_clear()
   :noindex:

   Empty the clipboard. Call this before appending a fresh value.

   :returns: ``None``.

.. py:method:: clipboard_append(string)
   :noindex:

   Add text to the clipboard (after ``clipboard_clear`` for a clean replace).

   :param str string: the text to place on the clipboard.
   :returns: ``None``.

.. py:method:: clipboard_get()
   :noindex:

   Return the clipboard's current text.

   :returns: the clipboard contents.
   :rtype: str
   :raises tkinter.TclError: if the clipboard is empty.

Selection
---------

.. py:method:: selection_get(**kw)
   :noindex:

   Return the current selection (the highlighted text).

   :param kw: ``selection=`` names which selection (default ``"PRIMARY"``).
   :returns: the selected text.
   :rtype: str
   :raises tkinter.TclError: if there is no selection.

.. py:method:: selection_clear(**kw)
   :noindex:

   Clear the selection this widget owns.

   :param kw: ``selection=`` names which selection to clear.
   :returns: ``None``.
