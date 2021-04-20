Frame
#####
A ``ttk.Frame`` widget is a container, used to group other widgets together.

Overview
========
The ``ttk.Frame`` includes the **TFrame** class. This class is further subclassed by each of the theme colors to
produce the following color and style combinations.

.. image:: images/frame.png

By default, the **TFrame** style is applied to all frame widgets with the theme background color. In this example, that
color is *white*. However, you can easily use a themed color for the background by using one of the `color.TFrame`
patterns above.

How to use
==========

Create a default **frame**

.. code-block:: python

    ttk.Frame(parent)

Create an **'info' frame**

.. code-block:: python

    ttk.Frame(parent, style='info.TFrame')

Style configuration
===================
Use the following classes, states, and options when configuring or modifying a new ttk button style.
:ref:`tutorial:create a new theme` using TTK Creator if you want to change the default color scheme.

Class names
-----------
- TFrame

Dynamic states
--------------
- disabled
- focus
- pressed
- readonly

Style options
-------------

:background: `color`
:relief: `flat, groove, raised, ridge, solid, sunken`

Create a custom style
=====================

Subclass an existing style to create a new one, using the pattern 'newstyle.OldStyle'

.. code-block:: python

    Style.configure('custom.TFrame', background='green', relief='sunken')

Use a custom style

.. code-block:: python

    ttk.Frame(parent, style='custom.TFrame')

Tips & tricks
=============
If you use a themed **Frame** widget, then you will likely want to use a **Label** widget with an *Inverse.TLabel*
style. This will create the effect that is presented in the Overview_, with the the label background matching the
background color of its parent.

.. code-block:: python

    frm = ttk.Frame(parent, style='danger.TFrame')
    lbl = ttk.Label(f, text='Hello world!', style='danger.Inverse.TLabel')

References
==========

- https://www.pythontutorial.net/tkinter/tkinter-frame/
- https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Frame.html
- https://tcl.tk/man/tcl8.6/TkCmd/ttk_frame.htm