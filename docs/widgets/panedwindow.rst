PanedWindow
###########
A ``ttk.PanedWindow`` widget displays a number of subwindows, stacked either vertically or horizontally. The user may
adjust the relative sizes of the subwindows by dragging the sash between panes.

Overview
========
The ``ttk.PanedWindow`` includes the **TPanedwindow** style class. Presently, this style contains default settings for
light and dark themes, but no other styles are included. This may change in the future. See the `Create a custom style`_
section to learn how to customize and create a paned window style.

How to use
==========
The examples below demonstrate how to *use a style* to create a widget. To learn more about how to *use the widget in
ttk*, check out the References_ section for links to documentation and tutorials on this widget.

Create and use a **Paned Window**

.. code-block:: python

    # create a new paned window
    pw = ttk.PanedWindow(parent, orient='horizontal')

    # add something on the left side
    left_frame = ttk.Frame(pw)
    left_frame.pack(side='left', fill='both')

    # add something on the right side
    right_frame = ttk.Frame(pw)
    right_frame.pack(side='left', fill='both')

    # add the frames to the paned window; a sash will appear between each frame (see image above)
    pw.add(left_frame)
    pw.add(right_frame)


Configuration
=============
Use the following classes, states, and options when configuring or modifying a new ttk paned window style.
See the `python style documentation`_ for more information on creating a style.

:ref:`tutorial:create a new theme` using TTK Creator if you want to change the default color scheme.


Class names
-----------
- TPanedwindow
- Sash

Style options
-------------
**TPanedwindow** styling options:

:background: `color`

**Sash** styling options:

:background: `color`
:bordercolor: `color`
:gripcount: `count`
:handlepad: `amount`
:handlesize: `amount`
:lightcolor: `color`
:sashpad: `amount`
:sashrelief: `flat, groove, raised, ridge, solid, sunken`
:sashthickness: `amount`

Create a custom style
=====================
Change the **relief** on all paned window sashes, and change the **gripcount**

.. code-block:: python

    Style.configure('Sash', relief='flat', gripcount=15)

Subclass an existing style to create a new one, using the pattern 'newstyle.OldStyle'

.. code-block:: python

    Style.configure('custom.TPanedwindow', background='red')

Use a custom style

.. code-block:: python

    ttk.PanedWindow(parent, style='custom.TPanedwindow')

.. _References:

References
==========
- https://www.pythontutorial.net/tkinter/tkinter-panedwindow/
- https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-PanedWindow.html
- https://tcl.tk/man/tcl8.6/TkCmd/ttk_panedwindow.htm

.. _`python style documentation`: https://docs.python.org/3/library/tkinter.ttk.html#ttk-styling