.. The ttkbootstrap positioning helper, included on the App and Toplevel pages
   right after the inherited Size and position methods (so it reads as part of
   that group). Not a standalone document.

.. py:method:: place_window_center()
   :noindex:

   Center the window on the screen — the monitor under the cursor when
   ``screeninfo`` is installed — clamped to stay fully visible. A ttkbootstrap
   convenience over :py:meth:`geometry`. Alias: ``position_center()``.

   :returns: ``None``.
