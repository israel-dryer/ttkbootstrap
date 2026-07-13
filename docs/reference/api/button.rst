Button
======

``Button`` is the native ttk push button (``ttk.Button``), themed by
ttkbootstrap — a clickable trigger that runs its ``command`` when pressed. This
page is the complete reference for its options, methods, and styling.

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
     - **Constructor keyword.** The style — an accent color (``primary``, …,
       ``dark``, ``neutral``) optionally with a variant (``outline``, ``link``,
       ``ghost``). See :ref:`Styling options <button-styling>`.
   * - ``icon``
     - ``str``
     - **Constructor keyword.** A Bootstrap Icons glyph name (e.g.
       ``"gear-fill"``) shown on the button; theme-aware — it follows the
       foreground color and states. See the
       :doc:`Icons guide </user-guide/feature-guides/icons>`.
   * - ``icon_size``
     - ``int``
     - **Constructor keyword.** The glyph size in pixels (scaled for high-DPI).
   * - ``icon_only``
     - ``bool``
     - **Constructor keyword.** Show only the glyph (hide the text) and pad the
       button into a square. Default ``False``.
   * - ``text``
     - ``str``
     - The label shown on the button.
   * - ``textvariable``
     - ``Variable``
     - A ``StringVar`` whose value is shown as the label and tracked live.
   * - ``command``
     - ``callable``
     - The function called when the button is pressed.
   * - ``image``
     - ``PhotoImage``
     - An image to display in place of, or beside, the text.
   * - ``compound``
     - ``str``
     - How text and image are combined: ``"none"``, ``"left"``, ``"right"``,
       ``"top"``, ``"bottom"``, or ``"center"``.
   * - ``underline``
     - ``int``
     - The character index to underline (for a keyboard mnemonic), or ``-1``.
   * - ``width``
     - ``int``
     - The requested width in characters (negative sets a minimum).
   * - ``padding``
     - ``int | tuple``
     - Extra space around the label, in pixels (a single value, or per-side).
   * - ``default``
     - ``str``
     - The default-button ring: ``"normal"``, ``"active"``, or ``"disabled"``.
   * - ``state``
     - ``str``
     - ``"normal"`` or ``"disabled"``. For finer control use the ``state`` method
       (see :doc:`Capabilities </reference/capabilities/index>`).
   * - ``cursor``
     - ``str``
     - The mouse cursor over the button (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the button accepts keyboard focus during traversal.

Methods
-------

.. py:method:: invoke()
   :noindex:

   Invoke the button — run its ``command`` and return whatever that returns.

   :returns: the command's return value.

.. _button-styling:

Styling options
---------------

This section is for changing how the button *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Button(style=...)``. The tables below list the style names you
can start from, the parts of the button you can target, the options each part
accepts, and the states they respond to.

.. include:: /reference/api/_style/button.rst

Shared capabilities
-------------------

``Button`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Button catalog page </widgets/button>` — usage, screenshots, and
  examples.
- `Tk ttk::button manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_button.htm>`__
  — the canonical upstream reference (Tcl 8.6).
