File Search Engine
==================
This example demonstrates the use of several styles on the buttons, treeview, and progressbar. The overall theme is
**journal**. For individual widgets, the applied styles are:

    :Browse: ``primary.TButton``
    :Search: ``primary.Outline.TButton``
    :Treeview: ``info.Treeview``
    :Progressbar: ``success.Horizontal.TProgressbar``

Additionally, this application uses threading and a queue to manage IO tasks in order to keep the gui interactive. The
treeview updates the results in real-time and sets the focus and view on the most recently inserted result in the
results treeview.

.. figure:: ../../src/ttkbootstrap/gallery/images/file_search_engine.png


Run this code live on repl.it_

.. _repl.it: https://replit.com/@IsraelDryer/file-search-engine

.. literalinclude:: ../../src/ttkbootstrap/gallery/file_search_engine.py
    :language: python
