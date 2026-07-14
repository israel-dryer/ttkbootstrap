Stacking order
==============

Where widgets overlap, **stacking order** decides which is drawn on top. Sibling
widgets stack in creation order by default; these methods change it.

The canonical upstream references are the Tk
`raise <https://www.tcl-lang.org/man/tcl8.6/TkCmd/raise.htm>`__ and
`lower <https://www.tcl-lang.org/man/tcl8.6/TkCmd/lower.htm>`__ manual pages
(Tcl 8.6).

.. py:method:: lift(aboveThis=None)
   :noindex:

   Raise the widget above its siblings, or above one specific sibling. Alias:
   ``tkraise`` (``lift`` avoids shadowing the Python builtin). Also raises a
   toplevel window to the front.

   :param aboveThis: the sibling to raise above; if omitted, raises to the top.
   :returns: ``None``.

.. py:method:: lower(belowThis=None)
   :noindex:

   Lower the widget below its siblings, or below one specific sibling.

   :param belowThis: the sibling to lower below; if omitted, lowers to the
      bottom.
   :returns: ``None``.
