Long-Running (Indeterminate)
============================
This example demonstrates the use of a progress bar for long-running tasks where the number of steps or time required is
*unknown* ahead of time and cannot otherwise be calculated. Instead of filling from left to right as normal, this
*indeterminate* mode of progressbar will shift the indicator from left to right to indicate that they system is working.

IO task are thread-blocking in python, which means that if you create a gui with a button that downloads a file from
the internet, the gui will be unresponsive until that download task is completed. To prevent this kind of negative
user experience, you can use threading to handle IO tasks. This will ensure that your gui will remain responsive to the
end user while the task is being completed on another thread.

In this example, I'm using the python threading_ module to create a thread to run a simulated IO task using the
``sleep`` method. This sleep method is a proxy for any other thread-blocking operation you may perform.

When a task is finished, the gui needs to be notified in order to update the progress bar.  The vehicle for this
communication is a ``Queue``. When the long-running task is started, the application will add a thread to the Queue.
While the task is running, the application will poll the queue every 500ms to check that all tasks have been completed.
This is done by scheduling the ``listen_for_complete_task`` method to run in the main
event loop every 500ms using the ``after`` method in tkinter. When all tasks in the queue are completed, the task thread
will mark the task as compete in the queue and this will cause the gui to stop the progress bar and return a popup that
indicates success.

.. figure:: ../../src/ttkbootstrap/examples/images/long_running_indeterminate.png

.. note::
    You can change the speed of the progress indicator by passing a time in milliseconds to the ``start`` methods. This
    is 50ms by default.

.. _threading: https://realpython.com/intro-to-python-threading/


Run this code live on repl.it_

.. _repl.it: https://replit.com/@IsraelDryer/long-running-indeterminate

.. literalinclude:: ../../src/ttkbootstrap/examples/long_running_indeterminate.py
    :language: python
