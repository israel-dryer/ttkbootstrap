App
===

``App`` is the ttkbootstrap application **root window** (also exported as
``Window``). It wraps tkinter's ``tk.Tk`` — folding the theme, title, icon, size,
position, and window constraints into a single constructor — and starts the
Tcl/Tk interpreter.

Keep **one** ``App`` per process. The style engine is a process-wide singleton
bound to the first root, so a second root would silently stop theming. Every
other window is a
:doc:`Toplevel </reference/windows/toplevel>`.

Options
-------

Set these on the constructor — ``App(title="ttkbootstrap", theme=None,
**options)``, where ``title`` and ``theme`` may be passed positionally and every
other option is keyword-only.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``title``
     - ``str``
     - The text shown on the window's title bar. Default ``"ttkbootstrap"``.
   * - ``theme`` (``themename``)
     - ``str``
     - The ttkbootstrap theme to apply. Defaults to ``bootstrap-light``.
   * - ``light_theme``
     - ``str``
     - The light theme the :py:meth:`toggle_theme` / :py:attr:`theme_mode` pair
       switches to.
   * - ``dark_theme``
     - ``str``
     - The dark theme the light/dark toggle switches to.
   * - ``default_button``
     - ``str``
     - The color a bare ``Button``/``Menubutton`` (no ``bootstyle``) uses.
       Default ``"neutral"``; pass ``"primary"`` for the pre-2.0 accented default.
   * - ``iconphoto``
     - ``str``
     - Path to the title-bar / taskbar icon image, applied application-wide.
       ``""`` (default) uses the ttkbootstrap brand icon; ``None`` leaves the
       icon untouched so you can call ``iconphoto``/``iconbitmap`` yourself.
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
   * - ``high_dpi``
     - ``bool``
     - Enable high-DPI awareness (Windows). Default ``True``.
   * - ``scaling``
     - ``float``
     - The Tk scaling factor — pixels per point — for converting physical units
       to pixels.
   * - ``transient``
     - ``Widget``
     - Mark the window as transient with respect to another window.
   * - ``override_redirect``
     - ``bool``
     - Remove the border and title bar (a bare window). Ignored on macOS, where
       it destabilizes Tk. Default ``False``.
   * - ``alpha``
     - ``float``
     - The window's opacity, ``0.0``–``1.0``. Default ``1.0`` (opaque).

Theming
-------

``App`` adds application-wide theme control; drop to :py:attr:`style` for the
full engine.

.. include:: /reference/windows/_theme.rst

Lifecycle
---------

.. py:method:: destroy()
   :noindex:

   Destroy the window and all its children. As the application root, this also
   resets the ttkbootstrap style engine and named-font cache, so a later root
   rebinds them cleanly.

   :returns: ``None``.

.. include:: /reference/windows/_lifecycle.rst

Window management
-----------------

Every window carries the full window-manager (``wm``) protocol below — its title,
icon, size, position, state, and relationships. The common ones fold into the
constructor above; the :doc:`Windows guide </user-guide/feature-guides/windows>`
teaches them by building.

.. include:: /reference/windows/_wm-1.rst

.. include:: /reference/windows/_positioning.rst

.. include:: /reference/windows/_wm-2.rst

Shared capabilities
-------------------

``App`` also has the methods every widget inherits — configuration, event
binding, lifecycle, focus, and introspection. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Toplevel </reference/windows/toplevel>` — every window other than the root.
- :doc:`Windows </user-guide/feature-guides/windows>` — how to build and manage
  windows, step by step.
- :doc:`Tk </reference/api/tk>` — the classic ``tk.Tk`` root and its full
  window-manager surface.
