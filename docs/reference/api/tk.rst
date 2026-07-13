Tk
==

``Tk`` is tkinter's classic root window (``tk.Tk``), themed by ttkbootstrap and
re-exported as ``ttk.Tk``. It is the main window of an application and the top of
the widget tree; creating it also starts the Tcl/Tk interpreter.

.. admonition:: Prefer ``ttk.Window``
   :class: tip

   For applications, use :doc:`ttk.Window </user-guide/feature-guides/windows>`
   (also exported as ``App``) instead of ``ttk.Tk``. ``Window`` folds size,
   position, icon, and constraints into one constructor call and applies a theme
   for you, so you rarely call the raw window-manager methods below. Keep **one**
   root per program (the single-root rule); every other window is a
   :doc:`Toplevel </user-guide/feature-guides/windows>`.

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

The root window carries the full window-manager (``wm``) protocol — the same
methods a :doc:`Toplevel </user-guide/feature-guides/windows>` has. The
:doc:`Windows guide </user-guide/feature-guides/windows>` teaches these by
building; the table below is the index.

.. rubric:: Title, icon, and menu

.. list-table::
   :widths: 30 70

   * - ``title(string=None)``
     - Get or set the window title.
   * - ``iconphoto(default, *images)``
     - Set the window/taskbar icon from one or more ``PhotoImage`` objects.
   * - ``iconbitmap(bitmap=None, default=None)``
     - Set the window icon from a bitmap file.
   * - ``iconname(newName=None)``
     - Get or set the icon-window name.

.. rubric:: Size and position

.. list-table::
   :widths: 30 70

   * - ``geometry(newGeometry=None)``
     - Get or set the window geometry as ``"WxH+X+Y"``.
   * - ``minsize(width=None, height=None)``
     - Get or set the minimum size.
   * - ``maxsize(width=None, height=None)``
     - Get or set the maximum size.
   * - ``resizable(width=None, height=None)``
     - Whether the user can resize the window horizontally / vertically.
   * - ``aspect(...)``
     - Constrain the window's width-to-height ratio.
   * - ``grid(...)``
     - Constrain the window to size in grid units.

.. rubric:: State

.. list-table::
   :widths: 30 70

   * - ``deiconify()``
     - Show the window (restore from minimized/withdrawn).
   * - ``iconify()``
     - Minimize the window to an icon.
   * - ``withdraw()``
     - Remove the window from the screen without destroying it.
   * - ``state(newstate=None)``
     - Get or set the window state (``"normal"``, ``"iconic"``, ``"withdrawn"``,
       ``"zoomed"``).
   * - ``attributes(*args)``
     - Get or set platform window attributes (``-alpha``, ``-topmost``,
       ``-fullscreen``, …).
   * - ``overrideredirect(boolean=None)``
     - Remove the window's border and title bar (a bare window).

.. rubric:: Relationships and protocols

.. list-table::
   :widths: 30 70

   * - ``protocol(name=None, func=None)``
     - Register a handler for a window-manager protocol, most often
       ``"WM_DELETE_WINDOW"`` (the close button).
   * - ``transient(master=None)``
     - Mark the window as a transient (a dialog) of another.
   * - ``group(pathName=None)``
     - Assign the window to a window group.

Shared capabilities
-------------------

``Tk`` also has the methods every widget inherits — configuration, event
binding, lifecycle, focus, and introspection. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Windows </user-guide/feature-guides/windows>` — how to build and manage
  windows with ``ttk.Window`` / ``ttk.Toplevel`` (the recommended API).
- `Tk toplevel <https://www.tcl-lang.org/man/tcl8.6/TkCmd/toplevel.htm>`__ and
  `wm <https://www.tcl-lang.org/man/tcl8.6/TkCmd/wm.htm>`__ manual pages — the
  canonical upstream reference (Tcl 8.6).