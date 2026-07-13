LabelFrame
==========

``LabelFrame`` is tkinter's classic ``tk.LabelFrame`` — a :doc:`frame </reference/api/tkframe>`
with a caption drawn into its border — themed by ttkbootstrap and re-exported as
``ttk.LabelFrame``. Prefer the ttk :doc:`Labelframe </widgets/labelframe>` for
themed layout; reach for ``LabelFrame`` only when you need a classic-tk option
the ttk version doesn't expose (a per-widget ``background``/``foreground``, a
custom label ``font``). Mind the capitalization: ``ttk.LabelFrame`` (capital
**F**) is this classic tk widget, while ``ttk.Labelframe`` (lowercase **f**) is
the :doc:`themed ttk widget </reference/api/labelframe>`.

Options
-------

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``autostyle``
     - ``bool``
     - **Constructor only.** ``True`` (default) paints the frame with the active
       theme and repaints on a theme switch; ``False`` opts out.
   * - ``text``
     - ``str``
     - The caption drawn into the border.
   * - ``labelwidget``
     - ``Widget``
     - A widget to use as the label in place of ``text`` (it must be a child of
       the labelframe or a sibling).
   * - ``labelanchor``
     - ``str``
     - Where the label sits on the border: ``"nw"``, ``"n"``, ``"ne"``,
       ``"en"``, ``"e"``, and so on. Default ``"nw"``.
   * - ``font``
     - ``str | Font``
     - The font of the ``text`` label.
   * - ``foreground`` (``fg``)
     - ``str``
     - The color of the ``text`` label.
   * - ``background`` (``bg``)
     - ``str``
     - The fill color of the frame.
   * - ``borderwidth`` (``bd``)
     - ``int``
     - The 3-D border width in pixels.
   * - ``relief``
     - ``str``
     - The border style. Default ``"groove"``.
   * - ``highlightthickness``
     - ``int``
     - The width of the focus highlight drawn around the widget.
   * - ``highlightcolor``
     - ``str``
     - The focus-highlight color when the widget has focus.
   * - ``highlightbackground``
     - ``str``
     - The focus-highlight color when the widget does not have focus.
   * - ``width``
     - ``int``
     - The requested width in pixels. Ignored unless geometry propagation is
       turned off (``pack_propagate(False)`` / ``grid_propagate(False)``).
   * - ``height``
     - ``int``
     - The requested height in pixels. Ignored unless geometry propagation is
       turned off.
   * - ``padx``
     - ``int``
     - Internal horizontal padding between the border and the content, in pixels.
   * - ``pady``
     - ``int``
     - Internal vertical padding between the border and the content, in pixels.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the frame (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the frame accepts keyboard focus during traversal.
   * - ``class``
     - ``str``
     - **Constructor only.** The widget class used for option-database lookups
       and bindtags.
   * - ``container``
     - ``bool``
     - **Constructor only.** ``True`` makes the frame an embed target for a
       foreign application window.
   * - ``visual``
     - ``str``
     - **Constructor only.** The X visual. Rarely needed.
   * - ``colormap``
     - ``str``
     - **Constructor only.** The X colormap. Rarely needed.

Shared capabilities
-------------------

``LabelFrame`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection. These are
documented under :doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Labelframe </widgets/labelframe>` — the themed ttk version (preferred).
- :doc:`TkFrame </reference/api/tkframe>` — the classic frame without a caption.
- `Tk labelframe manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/labelframe.htm>`__
  — the canonical upstream reference (Tcl 8.6).