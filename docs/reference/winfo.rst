Widget & screen info
====================

Every widget carries a family of ``winfo_*`` methods that report information
about itself, its place in the widget tree, and the screen it lives on — its
class, size, position, geometry manager, the pointer location, screen
dimensions, and more. They are the read side of the widget: nothing here changes
state, so all of them are safe to call at any time.

.. note::

   This is standard tkinter. The methods come from Tk's ``winfo`` command, which
   Tk documents only in a C-oriented manual page; this reference restates the
   names and return types in Python terms. For the full list see the
   `tkinter module reference
   <https://docs.python.org/3/library/tkinter.html>`__ on python.org. For **how
   to use** these — centering a window, reacting to a resize — see
   :doc:`Windows </user-guide/feature-guides/windows>` in the User Guide.

Identity & hierarchy
--------------------

Where a widget sits in the tree, what it is, and whether it is still alive.

.. list-table::
   :header-rows: 1
   :widths: 26 14 60

   * - Method
     - Returns
     - Meaning
   * - ``winfo_class()``
     - str
     - The widget's Tk class name (``"TButton"``, ``"Frame"``). This is the
       class used for :doc:`class bindings
       </user-guide/foundations/events-and-callbacks>` and styling, not the
       Python type.
   * - ``winfo_name()``
     - str
     - The widget's own name within its parent (the last path component, e.g.
       ``"!button"``).
   * - ``winfo_parent()``
     - str
     - The **path name** of the parent widget (``".!frame"``), not the widget
       object.
   * - ``winfo_children()``
     - list
     - The child widget *objects*, in stacking order. One level only — it does
       not recurse.
   * - ``winfo_toplevel()``
     - widget
     - The ``Tk``/``Toplevel`` window that contains this widget.
   * - ``winfo_manager()``
     - str
     - The geometry manager currently managing the widget: ``"pack"``,
       ``"grid"``, ``"place"``, or ``""`` if it is not managed.
   * - ``winfo_id()``
     - int
     - The platform window identifier (an ``HWND`` on Windows, an X11 window id
       on Linux).
   * - ``winfo_pathname(id)``
     - str
     - The widget path for a numeric window ``id`` (the inverse of
       ``winfo_id``). Optional ``displayof`` keyword.
   * - ``winfo_exists()``
     - int
     - ``1`` while the widget exists, ``0`` after it is destroyed.
   * - ``winfo_ismapped()``
     - int
     - ``1`` if the widget has been placed by a geometry manager and its
       toplevel is shown.
   * - ``winfo_viewable()``
     - int
     - ``1`` only if the widget **and every ancestor** are mapped — i.e. it is
       actually on screen.

Two more tree accessors are not ``winfo_*`` methods, but belong beside them:

.. list-table::
   :header-rows: 1
   :widths: 26 14 60

   * - Name
     - Returns
     - Meaning
   * - ``master``
     - widget
     - The parent widget *object* — the counterpart to ``winfo_parent()``, which
       returns the parent's path name instead. An attribute, not a method.
   * - ``children``
     - dict
     - The child widget objects keyed by their own names
       (``{'!button': <Button ...>}``) — the same widgets ``winfo_children()``
       returns as a list. An attribute, not a method.
   * - ``nametowidget(path)``
     - widget
     - The widget object for a path name — turns ``winfo_parent()``'s string back
       into a usable widget.

Position & size
---------------

Coordinates are in pixels. Position methods come in two flavors: relative to the
parent (``x``/``y``) and relative to the whole screen (``rootx``/``rooty``).

.. list-table::
   :header-rows: 1
   :widths: 26 14 60

   * - Method
     - Returns
     - Meaning
   * - | ``winfo_x()``
       | ``winfo_y()``
     - int
     - Top-left position **relative to the parent**.
   * - | ``winfo_rootx()``
       | ``winfo_rooty()``
     - int
     - Top-left position **relative to the screen** — the value to use when
       placing another window next to this one.
   * - | ``winfo_width()``
       | ``winfo_height()``
     - int
     - The widget's *current* size. See the gotcha below.
   * - | ``winfo_reqwidth()``
       | ``winfo_reqheight()``
     - int
     - The size the widget *requests* from its geometry manager (its natural
       size before stretching). Valid immediately, without mapping.
   * - ``winfo_geometry()``
     - str
     - Size and position as one ``"WxH+X+Y"`` string, e.g. ``"300x200+100+80"``.

.. warning::

   Before a widget is drawn, ``winfo_width``/``winfo_height`` return ``1`` — the
   real size is not known until the geometry manager has laid the widget out. If
   you need the size *right after* creating a widget (for example to center a
   window), force a layout pass first with ``update_idletasks``:

   .. code-block:: python

      app.update_idletasks()
      w, h = app.winfo_width(), app.winfo_height()

   Or read ``winfo_reqwidth``/``winfo_reqheight``, which are valid immediately.

Pointer
-------

The mouse pointer position and what lies under it, independent of any event.

.. list-table::
   :header-rows: 1
   :widths: 30 14 56

   * - Method
     - Returns
     - Meaning
   * - | ``winfo_pointerx()``
       | ``winfo_pointery()``
     - int
     - Pointer position relative to the screen.
   * - ``winfo_pointerxy()``
     - tuple
     - Both as a ``(x, y)`` pair.
   * - ``winfo_containing(rootx, rooty)``
     - widget or None
     - The widget under a **screen** coordinate, or ``None`` if the point is
       outside every window of this application.

Screen & display
----------------

Facts about the display the widget is on — useful for sizing or centering a
window against the monitor.

.. list-table::
   :header-rows: 1
   :widths: 30 14 56

   * - Method
     - Returns
     - Meaning
   * - | ``winfo_screenwidth()``
       | ``winfo_screenheight()``
     - int
     - The screen size in pixels.
   * - | ``winfo_screenmmwidth()``
       | ``winfo_screenmmheight()``
     - int
     - The screen size in millimeters — divide against the pixel size for the
       physical DPI.
   * - ``winfo_screen()``
     - str
     - The screen name (``":0.0"`` on X11).
   * - ``winfo_server()``
     - str
     - A string describing the windowing server / OS
       (``"Windows 10.0 26200 Win64"``).
   * - | ``winfo_vrootwidth()``
       | ``winfo_vrootheight()``
     - int
     - The size of the **virtual root** — the bounding box of all monitors on a
       multi-monitor desktop.
   * - | ``winfo_vrootx()``
       | ``winfo_vrooty()``
     - int
     - The virtual root's offset from the screen origin.

Unit & color conversion
------------------------

Helpers that convert Tk's screen distances and color names using the widget's
own display, so results honor the actual DPI and colormap.

.. list-table::
   :header-rows: 1
   :widths: 26 14 60

   * - Method
     - Returns
     - Meaning
   * - ``winfo_pixels(distance)``
     - int
     - Convert a Tk distance — ``"2c"`` (cm), ``"10m"`` (mm), ``"1i"`` (inch),
       ``"12p"`` (points) — to whole pixels.
   * - ``winfo_fpixels(distance)``
     - float
     - The same conversion, unrounded.
   * - ``winfo_rgb(color)``
     - tuple
     - A color name or ``"#rrggbb"`` string as a ``(r, g, b)`` triple of
       **16-bit** values (0–65535).

Rarely needed
-------------

Low-level display and X-server introspection — colormap depth, visual class,
and X11 atoms. You will almost never call these from application code; they are
listed for completeness.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Method
     - Meaning
   * - | ``winfo_depth()``
       | ``winfo_screendepth()``
     - Bits per pixel of the widget's / screen's visual.
   * - | ``winfo_cells()``
       | ``winfo_screencells()``
     - Number of colormap cells.
   * - | ``winfo_visual()``
       | ``winfo_screenvisual()``
       | ``winfo_visualid()``
     - The X visual class (``"truecolor"``, …) and its id.
   * - ``winfo_visualsavailable()``
     - The list of visuals the screen supports.
   * - ``winfo_colormapfull()``
     - ``1`` if the widget's colormap is full.
   * - | ``winfo_atom(name)``
       | ``winfo_atomname(id)``
     - Intern an X11 atom name to its integer id and back.
   * - ``winfo_interps()``
     - The Tk interpreter names registered on the display.

Example
-------

Center a window on the screen using screen size and the window's requested size:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.Window()
   ttk.Label(app, text="Centered").pack(padx=40, pady=40)

   app.update_idletasks()                       # settle the layout
   w, h = app.winfo_width(), app.winfo_height()
   x = (app.winfo_screenwidth() - w) // 2
   y = (app.winfo_screenheight() - h) // 2
   app.geometry(f"{w}x{h}+{x}+{y}")

   app.mainloop()

.. tip::

   ttkbootstrap already ships this: ``Window.place_window_center()`` does the
   same thing (and stays correct across multiple monitors) — see
   :doc:`Windows </user-guide/feature-guides/windows>`. Reach for the raw
   ``winfo_*`` methods when you need custom placement.
