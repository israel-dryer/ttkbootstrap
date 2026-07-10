Localization
============

.. note::

   This guide is being written for 2.0.

ttkbootstrap wraps Tcl/Tk's ``::msgcat`` so you can translate interface strings
and switch languages at runtime.

This guide will cover:

- ``L(src, *args, **kwargs)`` — the universal translate-and-format idiom:
  looks ``src`` up in the message catalog and applies ``str.format``.
- ``set_locale(locale)`` — set the active locale; queues before the root
  exists and applies live afterward, firing ``<<LocaleChanged>>``.
- ``LocaleVar`` — a ``StringVar`` that re-translates itself on
  ``<<LocaleChanged>>``, so a widget bound with ``textvariable=`` switches
  language without a restart.
- ``MessageCatalog`` — loading translation bundles, setting entries, and
  querying preferences.
