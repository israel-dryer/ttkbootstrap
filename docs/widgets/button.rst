Button
######
A ``ttk.Button`` widget displays a textual string, bitmap or image. If text is displayed, it must all be in a single
font, but it can occupy multiple lines on the screen (if it contains newlines or if wrapping occurs because of the
``wraplength`` option) and one of the characters may optionally be underlined using the ``underline`` option. It can
display itself in either of three different ways, according to the ``state`` option; it can be made to appear raised,
sunken, or flat; and it can be made to flash. When a user invokes the button (by pressing mouse button 1 with the
cursor over the button), then the Tcl command specified in the ``command`` option is invoked.

Overview
========
The ``ttk.Button`` includes the **TButton** and **Outline.TButton** style classes. The **TButton** style is applied to
all buttons by default. Other styles must be specified with the ``style`` option. These two primary styles are
further subclassed by each of the theme colors to produce the following color and style combinations:

.. image:: images/buttons.png

How to use
==========

Create a default **solid button**

.. code-block:: python

    ttk.Button(parent, text='Submit')

Create a default **outline button**

.. code-block:: python

    ttk.Button(parent, text='Submit', style='Outline.TButton')

Create an **'info' solid button**

.. code-block:: python

    ttk.Button(parent, text='Submit', style='info.TButton')

Create a **'warning' outline button**

.. code-block:: python

    ttk.Button(parent, text="Submit", style='warning.Outline.TButton')

Style configuration
===================
Use the following classes, states, and options when configuring or modifying a new ttk button style.

Class names
-----------
- TButton
- Outline.TButton

Dynamic states
--------------
- active
- disabled
- pressed
- readonly

Style options
-------------
:anchor: `e, w, center`
:background: `color`
:bordercolor: `color`
:compound: `top, bottom, left, right`
:darkcolor: `color`
:embossed: `amount`
:focuscolor: `color`
:focusthickness: `amount`
:foreground: `color`
:font: `font`
:highlightcolor: `color`
:highlightthickness: `amount`
:justify: `left, right, center`
:lightcolor: `color`
:padding: `padding`
:relief: `flat, groove, raised, ridge, solid, sunken`
:shiftrelief: `amount`
:width: `amount`

Create a custom style
=====================

Change the **font** and **font-size** on all buttons

.. code-block:: python

    Style.configure('TButton', font=('Helvetica', 12))

Change the **foreground color** when the button is active

.. code-block:: python

    Style.map('TButton', foreground=[
        ('disabled', 'white'),
        ('active', 'yellow')])

Subclass an existing style to create a new one, using the pattern 'newstyle.OldStyle'

.. code-block:: python

    Style.configure('custom.TButton', background='red', foreground='white', font=('Helvetica', 24))

Use a custom style

.. code-block:: python

    ttk.Button(parent, text='Submit', style='custom.TButton')


Tips & tricks
=============
Apply the **TLabel** style to remove the button's hover effects and to invert the colors. The button will still
behave as a button, though it will look like a standard label.  Conversely, you can apply a **TButton** style to a label
to inherit the colors and hover effects of the button.

References
==========
- https://www.pythontutorial.net/tkinter/tkinter-button/
- https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Button.html
- https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_button.htm
- https://tkdocs.com/widgets/button.html
