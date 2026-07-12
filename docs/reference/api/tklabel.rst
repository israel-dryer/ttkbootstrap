TkLabel
=======

``TkLabel`` is tkinter's classic ``tk.Label``, themed by ttkbootstrap and
re-exported as ``ttk.TkLabel``. It displays a line or block of read-only text,
an image, or both. Prefer the ttk :doc:`Label </widgets/label>` for themed text;
reach for ``TkLabel`` only when you need a classic-tk option the ttk label
doesn't expose (a per-widget ``background``/``foreground``, ``bitmap``,
``activeforeground``, ``disabledforeground``).

.. note::

   Python's standard library documents ``tk.Label`` only briefly. This
   reference is maintained by ttkbootstrap. The canonical upstream source is the
   `Tk label manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/label.htm>`__
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
     - **Constructor only.** ``True`` (default) paints the label with the active
       theme and repaints on a theme switch; ``False`` opts out.
   * - ``text``
     - ``str``
     - The string to display.
   * - ``textvariable``
     - ``Variable``
     - A ``StringVar`` whose value is shown and tracked live.
   * - ``image``
     - ``PhotoImage``
     - An image to display in place of, or beside, the text.
   * - ``bitmap``
     - ``str``
     - A built-in bitmap to display instead of an image.
   * - ``compound``
     - ``str``
     - How text and image are combined: ``"none"``, ``"left"``, ``"right"``,
       ``"top"``, ``"bottom"``, or ``"center"``.
   * - ``underline``
     - ``int``
     - The character index to underline (for a keyboard mnemonic), or ``-1``.
   * - ``font``
     - ``str | Font``
     - The font for the text.
   * - ``foreground`` (``fg``)
     - ``str``
     - The text color.
   * - ``background`` (``bg``)
     - ``str``
     - The surface color.
   * - ``activeforeground``
     - ``str``
     - The text color while the label is active (e.g. under the pointer in a
       menu).
   * - ``activebackground``
     - ``str``
     - The surface color while the label is active.
   * - ``disabledforeground``
     - ``str``
     - The text color when ``state`` is ``"disabled"``.
   * - ``justify``
     - ``str``
     - Alignment of multi-line text: ``"left"``, ``"center"``, or ``"right"``.
   * - ``anchor``
     - ``str``
     - Where the content sits within any extra space: ``"n"``, ``"ne"``,
       ``"center"``, and so on.
   * - ``wraplength``
     - ``int``
     - The width, in pixels, at which text wraps to a new line (``0`` disables
       wrapping).
   * - ``width``
     - ``int``
     - The requested width in characters (``0`` fits the content).
   * - ``height``
     - ``int``
     - The requested height in lines (``0`` fits the content).
   * - ``padx``
     - ``int``
     - Internal horizontal padding around the content, in pixels.
   * - ``pady``
     - ``int``
     - Internal vertical padding around the content, in pixels.
   * - ``borderwidth`` (``bd``)
     - ``int``
     - The 3-D border width in pixels.
   * - ``relief``
     - ``str``
     - The border style: ``"flat"``, ``"raised"``, ``"sunken"``, ``"groove"``,
       ``"ridge"``, or ``"solid"``.
   * - ``highlightthickness``
     - ``int``
     - The width of the focus highlight around the widget.
   * - ``highlightcolor``
     - ``str``
     - The focus-highlight color when the widget has focus.
   * - ``highlightbackground``
     - ``str``
     - The focus-highlight color when the widget does not have focus.
   * - ``state``
     - ``str``
     - ``"normal"``, ``"active"``, or ``"disabled"``.
   * - ``cursor``
     - ``str``
     - The mouse cursor (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the label accepts keyboard focus during traversal.

Shared capabilities
-------------------

``TkLabel`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection. These are
documented under :doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Label </widgets/label>` — the themed ttk label (preferred).
- `Tk label manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/label.htm>`__
  — the canonical upstream reference (Tcl 8.6).