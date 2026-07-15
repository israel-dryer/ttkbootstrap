Toplevel
========

``Toplevel`` is a secondary window — every application window other than the
:doc:`App </reference/windows/app>` root. It wraps tkinter's ``tk.Toplevel``,
inherits the application theme and icon, and folds size, position, constraints,
and platform window hints into a single constructor.

Options
-------

Set these on the constructor — ``Toplevel(title="ttkbootstrap", **options)``,
where ``title`` may be passed positionally and every other option is keyword-only.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``title``
     - ``str``
     - The text shown on the window's title bar. Default ``"ttkbootstrap"``.
   * - ``iconphoto``
     - ``str``
     - Path to the title-bar icon image for this window. ``""`` (default)
       inherits the application icon; ``None`` leaves the icon untouched.
   * - ``size``
     - ``tuple``
     - The window's ``(width, height)`` in pixels.
   * - ``position``
     - ``tuple``
     - The window's ``(x, y)`` position relative to the top-left. Negative values
       are edge-relative — ``(-10, -10)`` sits near the bottom-right.
   * - ``minsize``
     - ``tuple``
     - The minimum ``(width, height)`` the user may resize the window to.
   * - ``maxsize``
     - ``tuple``
     - The maximum ``(width, height)`` the user may resize the window to.
   * - ``resizable``
     - ``tuple``
     - A ``(horizontal, vertical)`` pair of booleans controlling whether the user
       may resize each dimension.
   * - ``transient``
     - ``Widget``
     - Mark the window as transient with respect to another window (typical for a
       dialog owned by the main window).
   * - ``override_redirect``
     - ``bool``
     - Remove the border and title bar (a bare window). Ignored on macOS. Default
       ``False``.
   * - ``window_type``
     - ``str``
     - A window-type hint. On X11 it sets the ``-type`` attribute (``"dialog"``,
       ``"splash"``, ``"utility"``, …); on macOS the borderless types
       (``"tooltip"``, ``"splash"``, ``"utility"``, ``"dock"``) map to a native
       window class with a real shadow and no title bar.
   * - ``topmost``
     - ``bool``
     - Keep the window above all others. Default ``False``.
   * - ``tool_window``
     - ``bool``
     - On Windows, use the tool-window style (a thin title bar, no taskbar entry).
       Default ``False``.
   * - ``iconify``
     - ``bool``
     - Start the window minimized. Default ``False``.
   * - ``alpha``
     - ``float``
     - The window's opacity, ``0.0``–``1.0``. Default ``1.0`` (opaque).

Theming
-------

A ``Toplevel`` shares the application-wide theme control of
:doc:`App </reference/windows/app>` — switching the theme from any window
re-themes them all.

.. include:: /reference/windows/_theme.rst

Lifecycle
---------

.. include:: /reference/windows/_lifecycle.rst

Window management
-----------------

Every window carries the full window-manager (``wm``) protocol below. The common
ones fold into the constructor above; the :doc:`Windows guide
</user-guide/feature-guides/windows>` teaches them by building.

.. include:: /reference/windows/_wm-1.rst

.. include:: /reference/windows/_positioning.rst

.. include:: /reference/windows/_wm-2.rst

Shared capabilities
-------------------

``Toplevel`` also has the methods every widget inherits — configuration, event
binding, lifecycle, focus, and introspection. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`App </reference/windows/app>` — the application root window.
- :doc:`Windows </user-guide/feature-guides/windows>` — how to build and manage
  windows, step by step.
