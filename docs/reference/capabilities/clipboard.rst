Clipboard
=========

Every widget can read and write the system **clipboard** — the buffer behind
copy and paste. For a worked copy/paste flow, see :doc:`Copy to the clipboard
</user-guide/how-to/clipboard>`.

The canonical upstream reference is the Tk
`clipboard <https://www.tcl-lang.org/man/tcl8.6/TkCmd/clipboard.htm>`__ manual
page (Tcl 8.6).

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
