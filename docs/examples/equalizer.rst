Equalizer
=========
A simple equalizer interface using the ``ttk.Scale`` widget. Because I wanted the scale value to be reflected in a label
below the scale, this application is a lot more complicated than it really needs to be due to some oddities of the ttk
scale implementation. The ``ttk.Scale`` widget outputs a double type, which means that in order to display a nice
rounded integer, that number has to be converted when updated. Fortunately, the scale widget has a ``command`` parameter
for setting a callback. The callback will get the scale value, which can then be converted into a nice clean format.

In order to create some contrast, I've applied different styles to the "VOL" and "GAIN" sliders:
    - VOL & GAIN: ``success.Vertical.TScale``
    - OTHERS: ``info.Vertical.TScale``

.. note:: For a vertical orientation, the ``from_`` parameter corresponds to the top and ``to`` corresponds to the
    bottom of the widget, so you'll need to take this into account when you set the minimum and maximum numbers for your
    scale range.

.. figure:: ../../src/ttkbootstrap/examples/images/equalizer.png

    random scale values are generated at runtime for demonstration purposes

Run this code live on repl.it_

.. _repl.it: https://replit.com/@IsraelDryer/equalizer

.. literalinclude:: ../../src/ttkbootstrap/examples/equalizer.py
    :language: python
