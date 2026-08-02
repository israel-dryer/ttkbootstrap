OptionMenu
==========

``OptionMenu`` is the native ttk menubutton preconfigured with a menu of
options that tracks the chosen one in a variable (``ttk.OptionMenu``), themed
by ttkbootstrap. This page is the
complete reference for its options, methods, and styling. It is a
convenience subclass of :doc:`Menubutton </reference/api/menubutton>` built
for you from a variable and a list of values; construct it as
``ttk.OptionMenu(master, variable, default, *values, command=None)``.

Options
-------

Most options are set with ``configure()`` after construction. ``OptionMenu`` is
the exception to the usual "either place works" rule: its constructor accepts
only ``command``, ``direction``, ``style`` and ``name`` alongside the variable
and values, and rejects the rest with ``TclError: unknown option``. Options
marked **Constructor only** below work the other way — set them when you build
the widget, not afterwards.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``bootstyle``
     - ``str``
     - **Constructor keyword.** An accent color, optionally with a variant. See
       :ref:`Styling options <optionmenu-styling>` for the available styles.
   * - ``command``
     - ``callable``
     - **Constructor only.** A callback invoked with the chosen value after an
       item is selected.
   * - ``icon``
     - ``str``
     - **Constructor keyword.** A Bootstrap Icons glyph name (e.g.
       ``"gear-fill"``) shown on the widget; theme-aware — it follows the
       foreground color and states. See the
       :doc:`Icons guide </user-guide/feature-guides/icons>`.
   * - ``icon_size``
     - ``int``
     - **Constructor keyword.** The glyph size in pixels (scaled for high-DPI).
   * - ``icon_only``
     - ``bool``
     - **Constructor keyword.** Show only the glyph (hide the text) and pad the
       widget into a square. Default ``False``.
   * - ``text``
     - ``str``
     - The label shown on the button.
   * - ``textvariable``
     - ``Variable``
     - A ``StringVar`` whose value is shown as the label and tracked live.
   * - ``menu``
     - ``Menu``
     - The ``Menu`` widget shown when the button is pressed.
   * - ``direction``
     - ``str``
     - Where the menu pops up relative to the button: ``"above"``,
       ``"below"``, ``"left"``, ``"right"``, or ``"flush"``.
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
   * - ``state``
     - ``str``
     - ``"normal"`` or ``"disabled"``. For finer control use the ``state`` method
       (see :doc:`Capabilities </reference/capabilities/index>`).
   * - ``cursor``
     - ``str``
     - The mouse cursor over the menubutton (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the menubutton accepts keyboard focus during traversal.

Methods
-------

.. py:method:: set_menu(default=None, *values)
   :noindex:

   Rebuild the menu from a new default and value list.

   :returns: ``None``.

.. _optionmenu-styling:

Styling options
---------------

This section is for changing how the option menu *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``OptionMenu(style=...)``. ``OptionMenu`` uses the Menubutton
style.

.. include:: /reference/api/_style/menubutton.rst

Shared capabilities
-------------------

``OptionMenu`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`OptionMenu catalog page </widgets/optionmenu>` — usage, screenshots,
  and examples.
- :doc:`Menubutton </reference/api/menubutton>` — the widget it builds on.
- `Tk ttk::menubutton manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_menubutton.htm>`__
  — the canonical upstream reference (Tcl 8.6).
