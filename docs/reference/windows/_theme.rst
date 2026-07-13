.. Shared ttkbootstrap theme methods, included by the App and Toplevel reference
   pages. Not a standalone document.

.. py:attribute:: style
   :noindex:

   The application's ``Style`` engine (a property) — drop to it for colors,
   ``configure``, registering themes, and the custom-style toolkit (see
   :doc:`Custom styles </user-guide/feature-guides/custom-styles>`).

.. py:method:: theme_use(themename=None)
   :noindex:

   Switch to ``themename``, or return the current theme name when called with no
   argument.

   :param themename: the theme to switch to.
   :returns: the current theme name.

.. py:method:: theme_names()
   :noindex:

   List every registered theme name.

   :returns: a list of theme names.

.. py:attribute:: theme_mode
   :noindex:

   The active theme mode (a property). Assign ``"light"`` or ``"dark"`` to switch
   to the corresponding theme of the configured pair.

.. py:method:: set_theme_modes(light=None, dark=None)
   :noindex:

   Designate the light/dark theme pair that :py:attr:`theme_mode` and
   :py:meth:`toggle_theme` switch between.

   :param light: the light theme name.
   :param dark: the dark theme name.
   :returns: ``None``.

.. py:method:: toggle_theme()
   :noindex:

   Toggle between the configured light and dark themes.

   :returns: the new mode (``"light"`` or ``"dark"``).
