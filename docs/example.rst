Example
=======
``ttkbootstrap`` works by creating pre-defined and user-defined themes at runtime which you can then apply and use as
you would any built-in ``ttk`` theme such as *clam*, *alt*, *classic*, etc...

.. code-block:: python

    from ttkbootstrap import Style
    from tkinter import ttk

    style = Style()
    style.theme_use('superhero')

    window = style.master
    ttk.Button(window, text="quit", style='warning.TButton').pack(side='left', padx=5, pady=10)
    ttk.Button(window, text="quit", style='warning.Outline.TButton').pack(side='left', padx=5, pady=10)
    window.mainloop()

The ``style`` object automatically creates the master widget that we assigned to ``window``. This is
standard ``ttk`` behavior, so you do not need to manually create a master widget by using ``tkinter.Tk()``.




