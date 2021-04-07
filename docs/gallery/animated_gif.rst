Animated Gif
============
This program demonstrates how to add animated GIFs to your application. These can be used for fancy splash screens or
loading screens for long-running tasks.

In this example, use the ``overrideredirect`` to prevent tkinter from decorating the window with a title bar and
border. However, this also removes the ability to close, minimize, or move the screen, so these need to be added back
as needed with key binding. Bind the *<Escape>* key to the ``quit`` method to give yourself the ability to close the
window. The window can be centered by directly calling a tcl command: ``self.eval('tk::PlaceWindow . center')``.

.. figure:: ../../src/ttkbootstrap/gallery/images/spinners.gif

Run this code live on repl.it_

.. _repl.it: https://replit.com/@IsraelDryer/animated-gif

.. literalinclude:: ../../src/ttkbootstrap/gallery/animated_gif.py
    :language: python
