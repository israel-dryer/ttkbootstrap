Tk
==

``Tk`` is tkinter's classic root window (``tk.Tk``), themed by ttkbootstrap and
re-exported as ``ttk.Tk``. It is the main window of an application and the top of
the widget tree; creating it also starts the Tcl/Tk interpreter.

.. admonition:: Prefer ``App``
   :class: tip

   For applications, use :doc:`App </reference/windows/app>` (also exported as
   ``Window``) instead of ``ttk.Tk``. ``App`` folds size, position, icon, and
   constraints into one constructor call and applies a theme for you, so you
   rarely call the raw window-manager methods below. Keep **one** root per program
   (the single-root rule); every other window is a
   :doc:`Toplevel </reference/windows/toplevel>`.

Options
-------

The root window takes the same surface options as a
:doc:`frame </reference/api/tkframe>`, plus a few of its own.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``autostyle``
     - ``bool``
     - **Constructor only.** ``True`` (default) applies the active theme;
       ``False`` opts out.
   * - ``menu``
     - ``Menu``
     - The ``Menu`` widget to use as the window's menu bar.
   * - ``screen``
     - ``str``
     - **Constructor only.** The X display to open the window on.
   * - ``use``
     - ``str``
     - **Constructor only.** The window id to embed this interpreter into.
   * - ``container``
     - ``bool``
     - **Constructor only.** Make the window a container that another
       application can be embedded into. Rarely needed.
   * - ``background`` (``bg``)
     - ``str``
     - The fill color of the window.
   * - ``borderwidth`` (``bd``)
     - ``int``
     - The 3-D border width in pixels.
   * - ``relief``
     - ``str``
     - The border style: ``"flat"``, ``"raised"``, ``"sunken"``, ``"groove"``,
       ``"ridge"``, or ``"solid"``.
   * - ``highlightthickness``
     - ``int``
     - The width of the focus highlight around the window.
   * - ``highlightcolor``
     - ``str``
     - The focus-highlight color when the window has focus.
   * - ``highlightbackground``
     - ``str``
     - The focus-highlight color when the window does not have focus.
   * - ``padx``
     - ``int``
     - Internal horizontal padding between the border and the content, in pixels.
   * - ``pady``
     - ``int``
     - Internal vertical padding between the border and the content, in pixels.
   * - ``width``
     - ``int``
     - The requested width in pixels. Usually set with ``geometry()`` instead.
   * - ``height``
     - ``int``
     - The requested height in pixels. Usually set with ``geometry()`` instead.
   * - ``cursor``
     - ``str``
     - The mouse cursor (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the window accepts keyboard focus during traversal.
   * - ``class``
     - ``str``
     - **Constructor only.** The widget class used for option-database lookups.
   * - ``visual``
     - ``str``
     - **Constructor only.** The X visual. Rarely needed.
   * - ``colormap``
     - ``str``
     - **Constructor only.** The X colormap. Rarely needed.

Window management
-----------------

As the application's root window, ``Tk`` carries the full window-manager
(``wm``) protocol below -- the same surface a :doc:`Toplevel
</reference/windows/toplevel>` has. The :doc:`Windows guide
</user-guide/feature-guides/windows>` teaches these by building.

.. include:: /reference/windows/_wm-1.rst

.. include:: /reference/windows/_wm-2.rst

Error handling
--------------

.. py:method:: report_callback_exception(exc, val, tb)
   :noindex:

   Called by tkinter whenever a callback raises an uncaught exception; the
   default prints the traceback to ``sys.stderr``. Assign your own function (or
   override in a subclass) to log or display callback errors — see
   :doc:`Handle errors gracefully </user-guide/how-to/error-handling>`.

   :param exc: the exception class.
   :param val: the exception instance.
   :param tb: the traceback object.

Shared capabilities
-------------------

``Tk`` also has the methods every widget inherits — configuration, event
binding, lifecycle, focus, and introspection. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`App </reference/windows/app>` / :doc:`Toplevel </reference/windows/toplevel>`
  — the ttkbootstrap window classes (the recommended API), and
  :doc:`Windows </user-guide/feature-guides/windows>` for how to use them.