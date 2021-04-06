File Search Engine
==================
This example demonstrates the use of several styles on the buttons, treeview, and progressbar.

    - browse button: ``primary.TButton``
    - search button: ``primary.Outline.TButton``
    - treeview: ``info.Treeview``
    - progress bar: ``success.Horizontal.TProgressbar``

Additionally, this application uses threading and a queue to manage IO tasks in order to keep the gui interactive. The
treeview updates the results in real-time and sets the focus and view on the most recently inserted result in the
results treeview. For more details on *indeterminate* patterns, see the example titled *long running indeterminate*.

.. figure:: ../../src/ttkbootstrap/examples/images/file_search_engine.png


Run this code live on repl.it_

.. _repl.it: https://replit.com/@IsraelDryer/file-search-engine

.. literalinclude:: ../../src/ttkbootstrap/examples/file_search_engine.py
    :language: python
