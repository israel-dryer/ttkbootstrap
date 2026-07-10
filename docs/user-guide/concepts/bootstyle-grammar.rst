The bootstyle grammar
=====================

Every ttkbootstrap widget is styled through one keyword: ``bootstyle``. This
guide is the canonical reference for its grammar.

A ``bootstyle`` value is a single string built from a fixed slot order::

   [color-][modifier-]<base-type>[-orient]

- **color** — the semantic intent: ``primary``, ``secondary``, ``success``,
  ``info``, ``warning``, ``danger``, ``light``, ``dark``, ``neutral``.
- **modifier** — a variant such as ``outline``, ``link``, ``ghost``, ``round``,
  ``toggle``.
- **base-type** — the widget family (usually inferred from the widget).
- **orient** — ``horizontal`` / ``vertical`` where applicable.

The parser is a tokenizer over a closed vocabulary: unknown tokens fail loudly
(a warning by default; ``set_bootstyle_strict(True)`` or
``TTKBOOTSTRAP_STRICT=1`` raises).

The full vocabulary and every registered widget family follow, generated from
the closed vocabulary and the builder registry.

.. include:: /_generated/bootstyle_reference.rst
