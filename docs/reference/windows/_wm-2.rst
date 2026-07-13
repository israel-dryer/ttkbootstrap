.. Shared window-manager (wm) specs, part 2 (state/attributes/relationships/
   embedding), included after the size/position group. Not standalone.

.. rubric:: State and visibility

.. py:method:: deiconify()
   :noindex:

   Show the window, restoring it from a minimized or withdrawn state and raising
   it.

   :returns: ``None``.

.. py:method:: iconify()
   :noindex:

   Minimize the window to an icon.

   :returns: ``None``.

.. py:method:: withdraw()
   :noindex:

   Remove the window from the screen without destroying it (unmapped). Restore it
   with :py:meth:`deiconify`.

   :returns: ``None``.

.. py:method:: state(newstate=None)
   :noindex:

   Set the window state — ``"normal"``, ``"iconic"`` (minimized), ``"withdrawn"``,
   or ``"zoomed"`` (maximized, Windows/macOS) — or return the current state.

   :returns: the current state when queried, otherwise ``None``.

.. py:method:: overrideredirect(boolean=None)
   :noindex:

   Set whether the window manager ignores the window — a truthy value removes the
   border and title bar (a bare window, e.g. a splash) — or return the current
   flag. Ignored on macOS, where it destabilizes Tk.

   :param boolean: ``True`` for a borderless window.
   :returns: the current flag when queried, otherwise ``None``.

.. rubric:: Attributes

.. py:method:: attributes(*args)
   :noindex:

   Get or set platform window attributes. Call ``attributes("-alpha")`` to read
   one, or ``attributes("-alpha", 0.9)`` to set it. Common options:

   - ``-alpha`` — opacity, ``0.0``–``1.0``.
   - ``-topmost`` — keep above all other windows.
   - ``-fullscreen`` — fill the screen with no chrome.
   - ``-disabled`` — block input to the window.
   - ``-toolwindow`` — (Windows) a thin tool-window title bar, no taskbar entry.
   - ``-type`` — (X11) the window type, e.g. ``"dialog"`` or ``"splash"``.

   :returns: the requested attribute value when reading, otherwise ``None``.

.. rubric:: Relationships and protocols

.. py:method:: protocol(name=None, func=None)
   :noindex:

   Register ``func`` as the handler for a window-manager protocol — most often
   ``"WM_DELETE_WINDOW"`` (the close button), letting you confirm or veto a close.
   Call with only ``name`` to return the current handler.

   :param name: the protocol, e.g. ``"WM_DELETE_WINDOW"`` or ``"WM_TAKE_FOCUS"``.
   :param func: the callback to run when the protocol fires.
   :returns: the current handler name when queried, otherwise ``None``.

.. py:method:: transient(master=None)
   :noindex:

   Mark the window as a **transient** of ``master`` — a dependent window (a dialog
   or picker) that stays above its owner and minimizes with it — or return the
   current master.

   :param master: the owning window.
   :returns: the current master when queried, otherwise ``None``.

.. py:method:: group(pathName=None)
   :noindex:

   Add the window to the window group led by ``pathName`` so a window manager can
   treat the group as a unit, or return the current group leader.

   :returns: the current group leader when queried, otherwise ``None``.

.. py:method:: client(name=None)
   :noindex:

   Set the ``WM_CLIENT_MACHINE`` property (the host name the app runs on) for
   remote-display setups, or return it. X11 only.

   :returns: the current value when queried, otherwise ``None``.

.. py:method:: command(value=None)
   :noindex:

   Set the ``WM_COMMAND`` property — the command line that could restart the app,
   used by session managers — or return it. X11 only.

   :returns: the current value when queried, otherwise ``None``.

.. py:method:: colormapwindows(*wlist)
   :noindex:

   Set the ``WM_COLORMAP_WINDOWS`` list — the child windows whose colormaps the
   window manager should install — or return the current list. X11, rarely needed.

   :returns: the current list when queried, otherwise ``None``.

.. py:method:: focusmodel(model=None)
   :noindex:

   Set the window's focus model — ``"active"`` or ``"passive"`` — or return it.
   Governs how the window accepts keyboard focus from the window manager.

   :returns: the current model when queried, otherwise ``None``.

.. rubric:: Embedding (advanced)

.. py:method:: frame()
   :noindex:

   Return the platform window identifier of the outermost decorative frame the
   window manager drew around this window (or the window's own id if none).

   :returns: a platform window id (a string).

.. py:method:: manage(widget)
   :noindex:

   Turn a previously :py:meth:`forget`-ten or embedded ``widget`` into a managed
   toplevel window.

   :returns: ``None``.

.. py:method:: forget(window)
   :noindex:

   Unmap a managed toplevel and hand it back to its parent's geometry manager (the
   inverse of :py:meth:`manage`).

   :returns: ``None``.
