.. The ttkbootstrap positioning helper, included on the App and Toplevel pages
   right after the inherited Size and position methods (so it reads as part of
   that group). Not a standalone document.

.. py:method:: place_window_center()
   :noindex:

   Center the window on the screen — the monitor under the cursor when
   ``screeninfo`` is installed — clamped to stay fully visible. A ttkbootstrap
   convenience over :py:meth:`geometry`. Alias: ``position_center()``.

   May be called before the window has been shown, which is how a window is made
   to *appear* centered rather than appear and then jump: ``withdraw()``, center,
   then ``deiconify()``. Centering then uses the size the window will map at —
   the size applied through :py:meth:`geometry` (the ``size`` constructor
   argument routes through it), or the content's request raised to the
   ``minsize`` floor.

   :returns: ``None``.
