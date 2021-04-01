Getting started
===============
ttkbootstrap works by generating pre-defined and user-defined themes at runtime which you can then apply and use as
you would any built-in ``ttk`` theme such as *clam*, *alt*, *classic*, etc... Check out :ref:`TTK Creator <ttkcreator>`
if you want to learn more about how this works and how you can create your own custom themes.

Simple example
--------------

.. code-block:: python

    from ttkbootstrap import Style
    from tkinter import ttk

    style = Style()
    style.theme_use('lumen')

    window = style.master
    ttk.Button(window, text="Submit", style='success.TButton').pack(side='left', padx=5, pady=10)
    ttk.Button(window, text="Submit", style='success.Outline.TButton').pack(side='left', padx=5, pady=10)
    window.mainloop()


This results in the window below:

.. image:: images/submit.png

The ``Style`` object automatically creates the master widget that we assigned to ``window``. This is
standard ttk behavior, so you do not need to manually create a master widget by using ``tkinter.Tk()``.

Check out the :ref:`Styling widgets <stylingwidgets>` section to learn more about how theming works and how you can
apply different colors and styles to the widgets.
