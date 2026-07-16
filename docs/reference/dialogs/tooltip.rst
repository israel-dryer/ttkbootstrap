ToolTip
=======

``ToolTip`` is a helper that ttkbootstrap ships (``ttk.ToolTip``) — a
semi-transparent popup that shows text while the pointer hovers over a target
widget, and hides on leave or click. It is **not a widget**: you attach one to a
target by passing that widget to the constructor, and it manages its own hover
events thereafter.

Options
-------

Options are passed to the constructor and can be changed later with
``configure()`` (read back with ``cget()``).

.. list-table::
   :header-rows: 1
   :widths: 20 18 62

   * - Option
     - Type
     - Description
   * - ``widget``
     - ``Widget``
     - The target widget the tooltip is attached to and positioned over.
   * - ``text``
     - ``str``
     - The text shown in the tooltip. Default ``"widget info"``.
   * - ``bootstyle``
     - ``str``
     - The style applied to the tooltip label — any standard label style.
       Default ``None``.
   * - ``padding``
     - ``int``
     - Padding between the text and the tooltip border. Default ``10``.
   * - ``justify``
     - ``str``
     - Alignment of multi-line text: ``"left"``, ``"center"``, or ``"right"``.
       Default ``"left"``.
   * - ``wraplength``
     - ``int``
     - Width in screen units before the text wraps. Default ``None`` (a scaled
       factor of 300).
   * - ``delay``
     - ``int``
     - Milliseconds to hover before the tooltip appears. Default ``250``.
   * - ``image``
     - ``PhotoImage``
     - An optional image shown below the text. Default ``None``.
   * - ``position``
     - ``str``
     - Placement relative to the widget — a space-separated combination of
       ``"left"``, ``"right"``, ``"top"``, ``"bottom"``, ``"center"`` (e.g.
       ``"top left"``). Default ``None`` (offset from the pointer).
   * - ``**kwargs``
     - ``any``
     - Passed to the popup :class:`~ttkbootstrap.Toplevel` — e.g. ``alpha``
       (default ``0.95``) and ``topmost``. ``topmost`` defaults to ``True`` so
       the tip draws above every window, matching native tooltips; pass
       ``topmost=False`` to keep it above its own application only.

Methods
-------

.. py:method:: show_tip()
   :noindex:

   Create and show the tooltip window. Called automatically on hover; call it
   directly to show the tooltip programmatically.

   :returns: ``None``.

.. py:method:: hide_tip()
   :noindex:

   Hide the tooltip window.

   :returns: ``None``.

.. py:method:: move_tip()
   :noindex:

   Reposition the tooltip to track the pointer or the configured anchor.

   :returns: ``None``.

See also
--------

- :doc:`ToolTip catalog page </widgets/tooltip>` — usage, screenshots, and
  examples.