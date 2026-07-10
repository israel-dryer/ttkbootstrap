The bootstyle grammar
=====================

.. note::

   This is the flagship guide of the 2.0 documentation and is being written. It
   will fold in the generated reference table from
   ``development/2_0_bootstyle_reference.md``.

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

The parser is a tokenizer over a closed vocabulary: unknown tokens fail loudly.
The full reference table of every valid string will appear here.
