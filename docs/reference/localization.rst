Localization
============

ttkbootstrap translates its built-in strings — dialog buttons, date names, and
the like — through Tk's message catalog. ``L`` looks up a translation,
``set_locale`` switches the active locale, ``LocaleVar`` is a variable that
re-translates itself when the locale changes, and ``MessageCatalog`` is the
lower-level catalog API. The :doc:`Localization guide
</user-guide/feature-guides/localization>` shows them in use.

.. autofunction:: ttkbootstrap.L

.. autofunction:: ttkbootstrap.set_locale

.. autoclass:: ttkbootstrap.LocaleVar
   :members:

.. autoclass:: ttkbootstrap.localization.MessageCatalog
   :members:

See also
--------

- :doc:`Localization </user-guide/feature-guides/localization>` — how to use it,
  with examples.
