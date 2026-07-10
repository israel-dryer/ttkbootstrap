Input validation
================

.. note::

   This guide is being written for 2.0.

ttkbootstrap ships a small validation framework for ``Entry``, ``Spinbox``, and
``Combobox``: attach a rule and a failing value paints the widget with a
``danger`` border until it is corrected.

This guide will cover:

- **Ready-made rules** — ``add_text_validation``, ``add_numeric_validation``,
  ``add_range_validation(start, end)``, ``add_regex_validation(pattern)``,
  ``add_option_validation(options)``, ``add_phonenumber_validation``.
- **When they fire** — the ``when=`` argument (``"focusout"``, ``"key"``, …).
- **Custom rules** — the ``@validator`` decorator over ``add_validation`` and the
  ``ValidationEvent`` passed to your function.
