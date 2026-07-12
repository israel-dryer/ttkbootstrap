TkFrame
=======

``TkFrame`` is tkinter's classic ``tk.Frame`` container, themed by ttkbootstrap
and re-exported as ``ttk.TkFrame``. It is a plain rectangular surface used to
group and lay out other widgets. Prefer the ttk :doc:`Frame </widgets/frame>`
for themed layout; reach for ``TkFrame`` only when you need a classic-tk option
the ttk frame doesn't expose (``background``, ``highlightthickness``,
per-widget ``relief``/``borderwidth``, an off-screen ``container``).

.. note::

   Python's standard library documents ``tk.Frame`` only briefly. This
   reference is maintained by ttkbootstrap. The canonical upstream source is the
   `Tk frame manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/frame.htm>`__
   (Tcl 8.6).

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
   * - ``background`` (``bg``)
     - ``str``
     - The fill color of the frame.
   * - ``borderwidth`` (``bd``)
     - ``int``
     - The 3-D border width in pixels.
   * - ``relief``
     - ``str``
     - The border style: ``"flat"``, ``"raised"``, ``"sunken"``, ``"groove"``,
       ``"ridge"``, or ``"solid"``.
   * - ``highlightthickness``
     - ``int``
     - The width of the focus highlight drawn around the widget when it (or a
       child) has keyboard focus.
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

``TkFrame`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection. These are
documented under :doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Frame </widgets/frame>` — the themed ttk container (preferred).
- `Tk frame manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/frame.htm>`__
  — the canonical upstream reference (Tcl 8.6).