Fonts
=====

Working with fonts spans two surfaces: the ``Fonts`` manager for the
application's **named fonts** (the shared ``TkDefaultFont``/``TkTextFont``/… that
widgets use, and the global family), and the font tools — ``Font``,
``font_families``, ``nametofont`` — for **listing families, measuring text, and
building individual font objects**. The :doc:`Typography guide
</user-guide/feature-guides/typography>` shows them in use.

The Fonts manager
-----------------

.. autoclass:: ttkbootstrap.Fonts
   :members:

Font families and named fonts
-----------------------------

.. py:function:: font_families(root=None, displayof=None)
   :noindex:

   List the font families installed on the system — the values usable as a
   font's ``family``.

   :returns: a tuple of family names.

.. py:function:: nametofont(name, root=None)
   :noindex:

   Return the :py:class:`Font` object for a named font, so you can query or
   reconfigure it.

   :param name: the named font, e.g. ``"TkDefaultFont"``.
   :returns: a ``Font`` bound to that named font.

The Font object
---------------

.. py:class:: Font(font=None, name=None, exists=False, **options)
   :noindex:

   A font you can measure with and pass to a widget's ``font`` option. Build one
   from ``options`` — ``family``, ``size`` (points; negative is pixels),
   ``weight`` (``"normal"``/``"bold"``), ``slant`` (``"roman"``/``"italic"``),
   ``underline``, ``overstrike`` — or from an existing spec via ``font``. Pass
   ``name`` (with ``exists=True``) to bind to a named font.

.. py:method:: measure(text, displayof=None)
   :noindex:

   Measure how wide ``text`` is in this font.

   :param text: the string to measure.
   :returns: the width in pixels (``int``).

.. py:method:: metrics(*options, displayof=None)
   :noindex:

   Report the font's vertical metrics — ``ascent``, ``descent``, ``linespace``,
   and ``fixed``. Pass one option name to get that value alone.

   :returns: a dict of all metrics, or a single value when one option is named.

.. py:method:: actual(option=None, displayof=None)
   :noindex:

   Report the concrete attributes this font resolves to (useful for aliases like
   ``"TkDefaultFont"``). Pass one option name to get that value alone.

   :returns: a dict of the actual attributes, or a single value.

.. py:method:: configure(**options)
   :noindex:

   Get or set the font's attributes (``family``, ``size``, ``weight``, …). A
   named font reconfigured this way updates every widget using it. Alias:
   ``config``.

   :returns: the current options when called with no arguments, otherwise ``None``.

.. py:method:: cget(option)
   :noindex:

   Return the value of one font attribute.

   :param option: the attribute name, e.g. ``"size"``.
   :returns: the attribute's value.

.. py:method:: copy()
   :noindex:

   Make a new ``Font`` with the same attributes.

   :returns: a new ``Font``.

See also
--------

- :doc:`Typography </user-guide/feature-guides/typography>` — how to use fonts,
  with examples.
