Utilities
=========

A small set of standalone helpers that don't belong to any one widget: color
conversion and contrast, high-DPI awareness and size scaling, and hooks that run
your code when the theme changes. They live in ``ttkbootstrap.utils`` and are
re-exported at the top level (``ttkbootstrap.contrast_color``, …).

Color
-----

Convert a color between models and derive readable pairings. A *model* is one of
the strings ``"hex"``, ``"rgb"``, ``"hsl"``, or ``"name"`` (exposed as the
constants ``HEX``/``RGB``/``HSL``/``NAME``); ``RGB`` is ``(r, g, b)`` with each
channel ``0–255`` and ``HSL`` is ``(hue, saturation, luminance)``.

.. autofunction:: ttkbootstrap.utils.color_to_hex

.. autofunction:: ttkbootstrap.utils.color_to_rgb

.. autofunction:: ttkbootstrap.utils.color_to_hsl

.. autofunction:: ttkbootstrap.utils.conform_color_model

.. autofunction:: ttkbootstrap.utils.update_hsl_value

.. autofunction:: ttkbootstrap.utils.contrast_color

High-DPI and scaling
--------------------

.. autofunction:: ttkbootstrap.utils.enable_high_dpi_awareness

.. autofunction:: ttkbootstrap.utils.scale_size

.. autofunction:: ttkbootstrap.utils.windowing_system

Reacting to theme changes
-------------------------

A custom style built by hand is not rebuilt when the theme switches. Register a
callback to re-run your build after every switch — or mark the builder with the
``theme_aware`` decorator, which registers it and runs it once.

.. autofunction:: ttkbootstrap.utils.on_theme_change

.. autofunction:: ttkbootstrap.utils.remove_theme_change_callback

.. autofunction:: ttkbootstrap.utils.theme_aware

Defaults
--------

.. autofunction:: ttkbootstrap.utils.set_default_button

See also
--------

- :doc:`Fonts <fonts>` and :doc:`Localization <localization>` — the font and
  message-catalog helpers are also re-exported from ``ttkbootstrap.utils`` but
  are documented on their own pages.
- :doc:`Custom styles </user-guide/feature-guides/custom-styles>` — where the
  theme-change hooks are put to use.
