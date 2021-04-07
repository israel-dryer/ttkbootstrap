Timer Widget
============
This simple data entry form accepts user input and then prints it to the screen when submitted. The overall theme is
**flatly** and various styles are applied to the buttons depending on state and function:

    :Start: ``style="info.TButton"``
    :Pause: ``style="info.Outline.TButton"``
    :Reset: ``style="success.TButton"``
    :Exit: ``style="danger.TButton"``


.. figure:: ../../src/ttkbootstrap/gallery/images/timer_widget_started.png

    timer is running

.. figure:: ../../src/ttkbootstrap/gallery/images/timer_widget_paused.png

    timer is paused

Run this code live on repl.it_

.. _repl.it: https://replit.com/@IsraelDryer/timer-widget

.. literalinclude:: ../../src/ttkbootstrap/gallery/timer_widget.py
    :language: python
