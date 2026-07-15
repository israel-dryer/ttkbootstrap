.. Include-only: the on_close lifecycle handler shared by App and Toplevel.

.. py:method:: on_close(callback)
   :noindex:

   Run ``callback`` when the user closes the window — the title-bar close button
   on Windows, macOS, and Linux (and ``Alt+F4``) — then destroy the window
   automatically. You do not call :py:meth:`destroy` yourself. Registering a new
   handler replaces the previous one, and the callback is returned so ``on_close``
   also works as a decorator. Also available as the ``on_close=`` constructor
   argument.

   :param callback: a zero-argument callable. Return ``False`` from it to cancel
      the close and keep the window open (for example, after an unsaved-changes
      prompt); return ``None`` — or anything else — to let it close.
   :returns: ``callback``.

   .. note::

      On macOS the application-menu **Quit** (``⌘Q``), the Dock's Quit, and the
      app menu are a separate, app-wide gesture that does not trigger this
      per-window handler. Wire that with :py:meth:`ttkbootstrap.Menu.on_quit` on
      the native application menu.
