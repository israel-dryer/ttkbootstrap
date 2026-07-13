Panedwindow
===========

``Panedwindow`` is the native ttk container that divides its space between
children with draggable sashes (``ttk.Panedwindow``), themed by ttkbootstrap.
For usage and examples, see the
:doc:`Panedwindow catalog page </widgets/panedwindow>`; this page is the
complete reference for its options, methods, and styling.

.. note::

   Python's standard library documents ``ttk.Panedwindow`` only briefly. The
   canonical upstream source is the
   `Tk ttk::panedwindow manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_panedwindow.htm>`__
   (Tcl 8.6).

Options
-------

Each option can be set in the constructor and changed later with ``configure()``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``bootstyle``
     - ``str``
     - **Constructor keyword.** An accent color, optionally with a variant. See
       :ref:`Styling options <panedwindow-styling>` for the available styles.
   * - ``orient``
     - ``str``
     - The layout direction of the panes: ``"horizontal"`` or ``"vertical"``.
   * - ``width``
     - ``int``
     - The requested width, in pixels.
   * - ``height``
     - ``int``
     - The requested height, in pixels.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the panedwindow (see
       :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the panedwindow accepts keyboard focus during traversal.

Methods
-------

.. py:method:: add(child, **kw)
   :noindex:

   Add ``child`` as a new pane. ``kw`` include ``weight``.

   :returns: ``None``.

.. py:method:: insert(pos, child, **kw)
   :noindex:

   Insert a pane at ``pos``.

   :returns: ``None``.

.. py:method:: remove(child)
   :noindex:

   Remove a pane. Aliased as ``forget``.

   :returns: ``None``.

.. py:method:: pane(pane, option=None, **kw)
   :noindex:

   Query or set a pane's options (e.g. ``weight``).

.. py:method:: panes()
   :noindex:

   Return the child widgets, in order.

   :rtype: tuple

.. py:method:: sashpos(index, newpos=None)
   :noindex:

   Get, or set, the pixel position of sash ``index``.

   :rtype: int

   Lower-level ``sash_*`` and ``proxy_*`` methods also exist, for finer
   control over sash dragging.

.. _panedwindow-styling:

Styling options
---------------

This section is for changing how the panedwindow *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Panedwindow(style=...)``.

.. include:: /reference/api/_style/panedwindow.rst

Shared capabilities
-------------------

``Panedwindow`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Panedwindow catalog page </widgets/panedwindow>` — usage, screenshots,
  and examples.
- `Tk ttk::panedwindow manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_panedwindow.htm>`__
  — the canonical upstream reference (Tcl 8.6).
