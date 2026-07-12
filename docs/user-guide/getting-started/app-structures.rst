Structuring an app
==================

.. note::

   This guide is being written for 2.0.

Where :doc:`Quickstart <quickstart>` shows the smallest possible window, this
guide covers how to structure a real application:

- **App vs Tk.** ``App`` (also exported as ``ttk.Window``) is the enhanced
  root — it owns the theme and sets title, geometry, icon, alpha, and DPI in one
  constructor. Use it for new code; a bare ``tk.Tk`` still works if you attach a
  :class:`~ttkbootstrap.style.Style` yourself.
- **The single-root rule.** ttkbootstrap enforces one application root per
  process (the ``Style`` engine is a singleton bound to it). Extra windows are
  ``ttk.Toplevel``, not a second ``App``.
- **An app skeleton.** Subclassing ``ttk.App`` (or a ``ttk.Frame``) into a
  class-based layout, wiring ``mainloop``, and cleaning up on ``destroy``.

.. seealso::

   :doc:`Windows </user-guide/feature-guides/windows>` for the
   full ``App``/``Toplevel`` surface (positioning, icons, ``window_type``,
   light/dark mode).
