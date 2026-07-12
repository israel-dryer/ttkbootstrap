LabeledScale
============

``LabeledScale`` is a composite widget that ttkbootstrap ships
(``ttk.LabeledScale``) — a ttk :doc:`Scale </widgets/scale>` paired with a
:doc:`Label </widgets/label>` that automatically shows the scale's current
value. The scale and label are reachable as the ``scale`` and ``label``
attributes. For screenshots and worked examples, see the
:doc:`LabeledScale catalog page </widgets/labeledscale>`; this page is the
complete lookup reference.

Options
-------

.. list-table::
   :header-rows: 1
   :widths: 20 18 62

   * - Option
     - Type
     - Description
   * - ``bootstyle``
     - ``str``
     - The color of the scale and label — one of ``primary``, ``secondary``,
       ``success``, ``info``, ``warning``, ``danger``, ``light``, ``dark``.
       Default ``"default"``.
   * - ``variable``
     - ``Variable``
     - The variable bound to the scale's value. If omitted, a ``DoubleVar`` is
       created automatically. Default ``None``.
   * - ``from_``
     - ``int | float``
     - The minimum value of the scale. Default ``0``.
   * - ``to``
     - ``int | float``
     - The maximum value of the scale. Default ``10``.
   * - ``compound``
     - ``str``
     - Where the label sits relative to the scale: ``"top"`` or ``"bottom"``.
       Default ``"top"``.

``LabeledScale`` is a ``Frame`` subclass and also accepts the frame's own
options (``padding``, ``cursor``, ``width``, ``height``, …), applied to the
container.

Methods
-------

.. py:attribute:: value
   :noindex:

   The current scale value (property). This mirrors the bound ``variable``, so
   you can also read or set it through that variable.

Shared capabilities
-------------------

``LabeledScale`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection. These are
documented under :doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`LabeledScale catalog page </widgets/labeledscale>` — usage, screenshots,
  and examples.
- :doc:`Scale </widgets/scale>` — the native ttk scale.