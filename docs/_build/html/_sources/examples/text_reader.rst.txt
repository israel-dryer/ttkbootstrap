Text Reader
===========
This application opens a text file and puts the data into a scrolled text widget.

Notice that I've used the ``Style.colors`` property to adjust the colors on the ``ScrolledText`` widget?
widget. This is handy when you want to make some customizations, but want to stay consistent with the theme color
palette.

Need to see the hex codes? Just print the colors property:

.. code-block:: python

    style = Style(theme='sandstone')
    print(style.colors)


You'll see this output in your console:

.. code-block::

    (('primary', '#3e3f3a'), ('secondary', '#8e8c84'), ('success', '#93c54b'), ('info', '#29abe0'), ('warning', '#f47c3c'), ('danger', '#d9534f'), ('bg', '#ffffff'), ('fg', '#3e3f3a'), ('selectbg', '#8e8c84'), ('selectfg', '#ffffff'), ('light', '#fdfcfb'), ('border', '#ced4da'), ('inputfg', '#3e3f3a'))


.. figure:: ../../src/ttkbootstrap/examples/images/text_reader.png

    **flatly** theme

Run this code live on repl.it_

.. _repl.it: https://replit.com/@IsraelDryer/text-reader

.. literalinclude:: ../../src/ttkbootstrap/examples/text_reader.py
    :language: python

The poem used in this demonstration can be found here_.

.. _here: https://gist.githubusercontent.com/mrtnzlml/1e35b552b24e0637d2e3d1dcd9154de7/raw/95b055dd524a45df9a7d004a7bd310c031401d59/poem.txt
