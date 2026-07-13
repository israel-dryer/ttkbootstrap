.. Shared window-manager (wm) specs, part 1 (title/icon + size/position),
   included by the App, Toplevel, and Tk pages. The window pages slot
   place_window_center in after this, under Size and position. Not standalone.

.. rubric:: Title, icon, and taskbar

.. py:method:: title(string=None)
   :noindex:

   Set the window's title-bar text, or return the current title when called with
   no argument.

   :param string: the new title.
   :returns: the current title when queried, otherwise ``None``.

.. py:method:: iconphoto(default=False, *images)
   :noindex:

   Set the title-bar / taskbar icon from one or more ``PhotoImage`` objects (Tk
   picks the best size). Pass ``default=True`` to make it the default icon for
   this window and every toplevel created afterward.

   :param default: make this the application-wide default icon.
   :param images: one or more ``PhotoImage`` objects.
   :returns: ``None``.

.. py:method:: iconbitmap(bitmap=None, default=None)
   :noindex:

   Set the window icon from a bitmap. On Windows, ``default`` accepts a ``.ico``
   path and applies it to this window and its future toplevels. Called with no
   argument, returns the current icon bitmap.

   :param bitmap: the bitmap for this window.
   :param default: (Windows) a ``.ico`` path applied as the default icon.
   :returns: the current bitmap when queried, otherwise ``None``.

.. py:method:: iconname(newName=None)
   :noindex:

   Set the name shown with the window's icon (when minimized), or return it.

   :returns: the current icon name when queried, otherwise ``None``.

.. py:method:: iconmask(bitmap=None)
   :noindex:

   Set the mask bitmap that controls which pixels of the icon are drawn, or
   return the current mask.

   :returns: the current mask when queried, otherwise ``None``.

.. py:method:: iconposition(x=None, y=None)
   :noindex:

   Hint to the window manager where to place the window's icon. Advisory — many
   window managers ignore it.

   :returns: ``None``.

.. py:method:: iconwindow(pathName=None)
   :noindex:

   Use another window as the icon for this one, or return the current icon
   window. Rarely supported on modern desktops.

   :returns: the current icon window when queried, otherwise ``None``.

.. rubric:: Size and position

.. py:method:: geometry(newGeometry=None)
   :noindex:

   Set the window's size and position as a ``"WxH+X+Y"`` string (any part may be
   omitted, e.g. ``"400x300"`` or ``"+100+100"``), or return the current geometry.

   :param newGeometry: a geometry string such as ``"640x480+200+120"``.
   :returns: the current geometry string when queried, otherwise ``None``.

.. py:method:: minsize(width=None, height=None)
   :noindex:

   Set the smallest size the user may resize the window to, or return the current
   minimum as ``(width, height)``.

   :returns: the current minimum when queried, otherwise ``None``.

.. py:method:: maxsize(width=None, height=None)
   :noindex:

   Set the largest size the user may resize the window to, or return the current
   maximum as ``(width, height)``.

   :returns: the current maximum when queried, otherwise ``None``.

.. py:method:: resizable(width=None, height=None)
   :noindex:

   Set whether the user may resize the window horizontally and vertically (two
   booleans), or return the current pair.

   :param width: allow horizontal resizing.
   :param height: allow vertical resizing.
   :returns: the current ``(width, height)`` flags when queried, otherwise ``None``.

.. py:method:: aspect(minNumer=None, minDenom=None, maxNumer=None, maxDenom=None)
   :noindex:

   Constrain the window's width-to-height ratio between ``minNumer/minDenom`` and
   ``maxNumer/maxDenom``, or return the current constraint. Call with no arguments
   to clear it.

   :returns: the current aspect constraint when queried, otherwise ``None``.

.. py:method:: grid(baseWidth=None, baseHeight=None, widthInc=None, heightInc=None)
   :noindex:

   Ask the window manager to report and constrain the window's size in **grid
   units** of ``widthInc`` × ``heightInc`` pixels (used by text-grid apps like a
   terminal), or return the current setting.

   :returns: the current grid setting when queried, otherwise ``None``.

.. py:method:: sizefrom(who=None)
   :noindex:

   Set who is considered to have specified the window's size — ``"program"`` or
   ``"user"`` — or return the current value. Affects how the window manager treats
   the size.

   :returns: the current value when queried, otherwise ``None``.

.. py:method:: positionfrom(who=None)
   :noindex:

   Set who is considered to have specified the window's position — ``"program"``
   or ``"user"`` — or return the current value.

   :returns: the current value when queried, otherwise ``None``.
