Separator
#########
A ``ttk.Separator`` widget displays a horizontal or vertical separator bar.

Overview
========
The ``ttk.Separator`` includes the **Horizontal.TSeparator** and **Vertical.TSeparator** style classes. These styles
are applied by default to *horizontal* and *vertical* orientations. These styles are further subclassed by each of the
theme colors to produce the following color and style combinations:

.. figure:: images/separator_horizontal.png

.. figure:: images/separator_vertical.png


How to use
==========
Create a default **horizontal separator**

.. code-block:: python

    ttk.Separator(parent, orient='horizontal')

Create a default **vertical separator**

.. code-block:: python

    ttk.Separator(parent, orient='vertical')

Create an **info vertical separator**

.. code-block:: python

    ttk.Separator(parent, orient='vertical', style='info.Vertical.TSeparator')

Configuration
=============
Use the following classes, states, and options when configuring or modifying a new ttk separator style. TTK Bootstrap
uses an image layout for this widget, so it is not possible to create a custom style without building a new layout.
However, if you decide to build your own layout, you are free to use the styling options below.
:ref:`tutorial:create a new theme` using TTK Creator if you want to change the default color scheme.

Class names
-----------
- Horizontal.TSeparator
- Vertical.TSeparator


Style options
-------------
:background: `color`


References
==========
- https://www.pythontutorial.net/tkinter/tkinter-separator/
- https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Separator.html
- https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_separator.htm