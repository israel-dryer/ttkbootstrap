.. _file-backup-utility:

File Backup Utility
===================
In this example, I demonstrate how to use various styles to build a UI for a File Backup UI. The reference material is
from an image you can find here_. The overall theme of this application is **flatly**. I use a ``CollapsingFrame``
class to contain the left-side info panels as well as the output on the bottom right. These contain indicator buttons
on the right-side of the header which collapse and expand the frame with a mouse-click action.

Some of the styles used in this application include:

.. _here: http://www.leo-backup.com/screenshots.shtml

    :top button bar: ``primary.TButton``
    :collapsible frames: ``secondary.TButton``
    :separators: ``secondary.Horizontal.TSeparator``
    :progress bar: ``success.Horizontal.TProgressbar``
    :properties, stop, add-to-backup buttons: ``Link.TButton``
    :file open button: ``secondary.Link.TButton``

There are two custom styles which are subclassed from ``TFrame`` and ``TLabel``. I used the **inputbg** color from the
``Style.colors`` property and applied this style to the left panel, and the logo image background.

.. figure:: ../../src/ttkbootstrap/gallery/images/back_me_up.png


.. literalinclude:: ../../src/ttkbootstrap/gallery/back_me_up.py
    :language: python
