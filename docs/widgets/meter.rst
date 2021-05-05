Meter
#####
The ``Meter`` is a custom **ttkbootstrap** widget that can be used to show progress of long-running operations or the
amount of work completed. It can also be used as a `Dial` when `interactive` mode is set to True. See the
:ref:`documentation <reference:meter>` for a complete reference on widget options and settings.

Overview
========
This widget is very flexible and can be customized to show a wide variety of styles. The ``metertype`` parameter has
two stock settings: `full` and `semi`, which shows a full circle and a semi-circle respectively. You can also customize
the arc of the circle with the ``arcrange`` and ``arcoffset`` parameters in order to move the starting position of the
arc, or to shorten the arc altogether.

The color of the meter is set with the ``meterstyle`` parameter and uses any of the `TLabel` styles to color the meter
as well as the central text. There is also an option label below the central text as well as `append` and `prepend` text
that can be set with the ``labelstyle`` parameter using any of the `TLabel` styles.

.. image:: images/meter.png

By default, the widget color is set to the `primary` theme color, and the supplemental label is set to the `secondary`
theme color. Below is an example of the color options. The supplemental label contains the style name used in the
``meterstyle`` parameter.

Below is sample of configurations that demonstrate how versatile this widget can be. You can see the code for this
example in the :ref:`Cookbook <dials_and_meters>`.

.. image:: images/meter_variations.png





