Input validation
================

ttkbootstrap ships a small validation framework for the text-entry widgets —
``Entry``, ``Spinbox``, and ``Combobox``. Attach a rule to a widget and a value
that fails it flags the widget with a ``danger``-colored border until the
contents become valid again. This guide covers the ready-made rules, when they
fire, and writing your own.

The rules live on the :class:`~ttkbootstrap.Validation` namespace, re-exported
at the top level — import it directly, or reach it as ``ttk.Validation``:

.. code-block:: python

   from ttkbootstrap import Validation

The ready-made rules
--------------------

Each method takes the widget as its first argument and wires up a rule in one
call:

.. list-table::
   :header-rows: 1
   :widths: 46 54

   * - Rule
     - Passes when the contents are…
   * - ``Validation.text(widget)``
     - alphabetic (or empty).
   * - ``Validation.numeric(widget)``
     - numeric (or empty).
   * - ``Validation.range(widget, start, end)``
     - a number within ``start``–``end`` inclusive (or empty).
   * - ``Validation.regex(widget, pattern)``
     - a match for the regular expression ``pattern``.
   * - ``Validation.options(widget, options)``
     - one of the values in ``options``.
   * - ``Validation.phonenumber(widget)``
     - a match for a common phone-number pattern.

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap import Validation

   app = ttk.App()

   age = ttk.Entry(app)
   age.pack(padx=20, pady=20)
   Validation.range(age, 0, 120)      # 0–120 accepted; anything else flags danger

   app.mainloop()

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   An entry with a valid value (normal border) beside the same entry holding an
   out-of-range value (``danger``-red border).

.. note::

   The text, numeric, and range rules treat an **empty** field as valid, so an
   untouched entry is not flagged before the user types anything. Combine a rule
   with a "required field" check of your own if empty should fail.

When validation fires
---------------------

Every helper takes a ``when=`` argument that controls *when* the rule runs.
The default is ``"focusout"`` — validate when the widget loses focus, the least
intrusive choice:

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - ``when``
     - Validates…
   * - ``"focusout"``
     - when the widget loses focus (the default).
   * - ``"focusin"``
     - when the widget gains focus.
   * - ``"focus"``
     - on both focus in and focus out.
   * - ``"key"``
     - on every keystroke — live, as the user types.
   * - ``"all"``
     - in all of the above situations.

.. code-block:: python

   Validation.numeric(entry, when="key")     # reject non-digits as they are typed

With ``when="key"`` the rule runs on each edit, so a rejected change keeps a bad
character from ever landing in the field; with ``"focusout"`` the value is
accepted into the widget but the widget is flagged until corrected.

.. note::

   The ``danger`` border is the ttk ``invalid`` widget state, toggled
   automatically from the rule's result — so a validated widget reports
   ``"invalid"`` in ``widget.state()`` while it holds a bad value. You can force
   a check at any time (for example, before submitting a form) by calling
   ``widget.validate()``, which returns ``True`` or ``False``.

Custom rules
------------

When no ready-made rule fits, write your own. A **rule** is a function that
receives a :class:`~ttkbootstrap.validation.ValidationEvent` and returns
``True`` (valid) or ``False`` (invalid). Decorate it with ``@validator`` so it
receives the event object, then attach it with ``Validation.add``:

.. code-block:: python

   from ttkbootstrap import Validation, validator

   @validator
   def is_even(event):
       text = event.postchangetext
       return text.isdigit() and int(text) % 2 == 0

   Validation.add(entry, is_even, when="focusout")

The event's most useful attribute is ``postchangetext`` — the value the widget
*will* hold if the change is allowed — along with ``widget`` (the widget being
validated). The full set (``actioncode``, ``insertdeletetext``,
``validationreason``, …) is documented on
:class:`~ttkbootstrap.validation.ValidationEvent`.

Pass extra keyword arguments through ``Validation.add`` and they arrive at your
rule — the same mechanism the built-in ``Validation.range`` uses:

.. code-block:: python

   @validator
   def max_length(event, limit):
       return len(event.postchangetext) <= limit

   Validation.add(entry, max_length, when="key", limit=10)

.. seealso::

   :doc:`Variables </user-guide/feature-guides/variables>` for reacting to input
   changes generally with traces, and
   :doc:`Events </user-guide/feature-guides/events>` for the binding system these
   validation callbacks are built on.
