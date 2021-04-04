Timer Widget
============
This simple data entry form accepts user input and then prints it to the screen when submitted.

All three buttons use different styles. The *Start/Pause* toggle button uses a different style depending on the state of
the timer state:

:Start: ``style="info.TButton"``
:Pause: ``style="info.Outline.TButton"``
:Reset: ``style="success.TButton"``
:Exit: ``style="danger.TButton"``


.. figure:: ../../src/ttkbootstrap/examples/images/timer_widget_started.png

    timer is running

.. figure:: ../../src/ttkbootstrap/examples/images/timer_widget_paused.png

    timer is paused

Run this code live on repl.it_

.. _repl.it: https://replit.com/@IsraelDryer/timer-widget

.. literalinclude:: ../../src/ttkbootstrap/examples/timer_widget.py
    :language: python
