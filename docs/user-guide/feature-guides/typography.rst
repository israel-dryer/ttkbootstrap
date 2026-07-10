Typography
==========

.. note::

   This guide is being written for 2.0.

ttkbootstrap styles text through the **standard Tk named fonts**
(``TkDefaultFont``, ``TkTextFont``, ``TkFixedFont``, ``TkHeadingFont``, …) — there
is no separate font DSL. Retint a named font and every widget that uses it
updates at once.

This guide will cover:

- ``set_global_family(family, *, mono_family=None)`` — the one-liner: set the
  proportional (and optionally monospace) family for the whole app. It rides the
  deferred-config seam, so you can call it at the top of a file *before* the root
  exists, or live afterward.
- The ``Fonts`` namespace (call after the root exists): ``Fonts.configure``
  to tweak one named font, ``Fonts.create_alias`` to register your own
  (``font="Body"``), ``Fonts.names``/``Fonts.describe`` to introspect, and
  ``Fonts.reset``.
