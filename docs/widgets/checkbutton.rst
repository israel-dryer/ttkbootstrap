Checkbutton
###########
A ``ttk.Checkbutton`` an on/off widget.

Styles
======
The ``ttk.Checkbutton`` includes the **TCheckbutton**, **Toolbutton**, **Outline.Toolbutton**,
**Roundtoggle.Toolbutton**, and **Squaretoggle.Toolbutton** style classes. The **TCheckbutton** class is applied to all
checkbuttons by default. Other styles must be specified in the checkbutton's ``style`` option. These primary classes are
further subclassed by each of the theme colors to produce the following color and style combinations:

Classic checkbutton
-------------------
.. image:: images/checkbutton.png

Classic toolbutton
------------------

.. image:: images/toolbutton.png

Round toggle button
-------------------

.. image:: images/roundtoggle.png

Square toggle button
--------------------

.. image:: images/squaretoggle.png

How to use
==========

.. code-block:: python

    # default checkbutton
    ttk.Checkbutton(parent, text='include', value=1)

    # default toolbutton
    ttk.Checkbutton(parent, text='include', style='Toolbutton')

    # default outline toolbutton
    ttk.Checkbutton(parent, text='include', style='Outline.Toolbutton')

    # default round toggle toolbutton
    ttk.Checkbutton(parent, text='include', style='Roundtoggle.Toolbutton')

    # default square toggle toolbutton
    ttk.Checkbutton(parent, text='include', style='Squaretoggle.Toolbutton')

    # "info" checkbutton
    ttk.Checkbutton(parent, text='include', style='info.TCheckbutton')

    # "warning" outline toolbutton
    ttk.Checkbutton(parent, text="include", style='warning.Outline.Toolbutton')


Configuration
=============
Use the following classes, states, and options when configuring or modifying a new ttk checkbutton style. TTK Bootstrap
uses an image layout for this widget, so not all of these options will be available... for example: ``indicatormargin``.
However, if you decide to create a new widget, these should be available, depending on the style you are using as a
base. Some options are only available in certain styles.

Class names
-----------
- TCheckbutton
- Toolbutton
- Outline.Toolbutton
- Roundtoggle.Toolbutton
- Squaretoggle.Toolbutton

Dynamic states
--------------
- active
- alternate
- disabled
- pressed
- selected
- readonly

Style options
-------------
:background: `color`
:compound: `compound`
:foreground: `foreground`
:focuscolor: `color`
:focusthickness: `amount`
:font: `font`
:padding: `padding`

.. code-block:: python

    # change the font and font-size on all buttons
    Style.configure('TCheckbutton', font=('Helvetica', 12))

    # change the foreground color when the checkbutton is selected
    Style.map('TCheckbutton', foreground=[
        ('disabled', 'white'),
        ('selected', 'yellow'),
        ('!selected', 'gray')])

    # subclass an existing style to create a new one, using the pattern 'newstyle.OldStyle'
    Style.configure('custom.TCheckbutton', foreground='white', font=('Helvetica', 24))

    # use a custom style
    ttk.Checkbutton(parent, text='include', style='custom.TCheckbutton')



References
==========
- https://www.pythontutorial.net/tkinter/tkinter-checkbox/
- https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Checkbutton.html
- https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_checkbutton.htm
