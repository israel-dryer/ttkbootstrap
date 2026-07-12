Frame
=====

A **frame** is a rectangular container that groups and lays out other widgets.
``Frame`` is the native ``ttk.Frame``, styled with ``bootstyle=``. This page covers
using it to structure a layout, padding its contents, then the ``bootstyle`` color
and the bordered card variants.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A window split into frames — a colored header frame above a plain content
   frame — in light and dark themes.

Usage
-----

A frame holds other widgets: pass the frame as their ``master``, then place the
frame in its own parent. Frames are how you break a window into regions and nest
layouts — a header, a sidebar, a form — each managed independently:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *

   app = ttk.App()

   header = ttk.Frame(app, padding=10, bootstyle="primary")
   header.pack(fill=X)
   ttk.Label(header, text="Dashboard", bootstyle="inverse-primary").pack()

   content = ttk.Frame(app, padding=20)
   content.pack(fill=BOTH, expand=YES)
   ttk.Label(content, text="Body goes here").pack()

   app.mainloop()

``padding=`` insets the frame's contents so its children don't hug the edges
(one value for all sides, or ``(left, top, right, bottom)``). Which geometry
manager you use *inside* a frame is independent of the one used to place the frame
itself — see :doc:`Arranging widgets </user-guide/foundations/arranging-widgets>`.

Color
-----

By default a frame is invisible — it takes the window background. Give it a
``bootstyle`` color to make it a visible band (a header, a footer, a colored
section):

.. code-block:: python

   ttk.Frame(app, padding=10, bootstyle="secondary")

Put ``inverse-<color>`` labels inside a colored frame so their text reads against
the fill (as the header above does).

Card and highlight variants
---------------------------

Two variants give a frame a **hairline border** to set a region off from the
background — a ``card`` for grouped content, and ``highlight`` which turns its
border to the accent color when something inside has focus:

.. code-block:: python

   ttk.Frame(app, padding=16, bootstyle="card")
   ttk.Frame(app, padding=16, bootstyle="highlight")

API & reference
---------------

``Frame`` is the native ``ttk.Frame`` — ttkbootstrap adds ``bootstyle=`` but no
other Python API. For its constructor and options (``padding``, ``width``,
``height``, ``borderwidth``, ``relief``, …) see the
`tkinter.ttk.Frame <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Frame>`__
reference.

.. seealso::

   :doc:`Labelframe <labelframe>` for a frame with a titled border, and
   :doc:`Notebook <notebook>` / :doc:`Panedwindow <panedwindow>` for tabbed and
   split containers. For laying widgets out inside a frame, see
   :doc:`Arranging widgets </user-guide/foundations/arranging-widgets>`. Want to
   restyle the frame yourself? The
   :doc:`Style Reference › Frame </reference/style-reference/frame>` and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide
   document the hand-styling surface.
