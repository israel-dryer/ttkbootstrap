Windows, icons & high-DPI
=========================

.. note::

   This guide is being written for 2.0.

``App`` (also exported as ``ttk.Window``) and ``ttk.Toplevel`` are enhanced
replacements for ``tk.Tk``/``tk.Toplevel`` that fold window setup into the
constructor and add ttkbootstrap-specific conveniences.

This guide will cover:

- **The constructor surface** — ``title``, ``size``, ``position`` (signed and
  edge-relative), ``minsize``/``maxsize``, ``resizable``, ``alpha``,
  ``iconphoto``, plus the renamed ``high_dpi``/``override_redirect``.
- **Positioning** — ``place_window_center()`` (monitor-aware when ``screeninfo``
  is installed, clamped on-screen).
- **Light/dark mode** — the settable ``theme_mode`` property, ``toggle_theme()``,
  and ``set_theme_modes(light=, dark=)``.
- **Toplevels** — ``window_type``, ``topmost``, ``tool_window``, and inherited
  app icons.
- **High-DPI** — ``enable_high_dpi_awareness()`` and ``scale_size()``.
- **Sidebar: the deferred-config seam** — how ``set_locale``,
  ``set_global_family``, and ``set_default_button`` can be called before the root
  exists and flush when it comes up.
