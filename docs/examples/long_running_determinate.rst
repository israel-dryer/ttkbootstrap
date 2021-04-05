Long-Running (Determinate)
==========================
*When the number of tasks or time is known*

You will often need to execute a task in tkinter that requires IO operations, or some other long-running task. For this
you will likely want to use a combination of threading, queues, and scheduling. In this example, I'm using the python
threading_ module to create a thread to run a simulated *blocking* task using the ``sleep`` function. This blocking
operation can't be run in the main thread with tkinter or the window will become unresponsive; so, a new thread is
created to handle this task.

Each thread needs to communicate to the application window when the process is finished. The vehicle for this is a
``queue.Queue``. When the process is started, the application will add the thread to the Queue. When the process
is complete, the task thread will mark this task as complete. While the thread is running, the application will poll the
queue every second to count how many tasks have been completed, and update the progressbar value. This is done by
scheduling the ``listen_for_complete_task`` method to run in the main event loop every 1000ms (1 second) using the
``after`` method in tkinter. When all tasks in the queue are completed, the progress bar will be updated to the maximum
value and a popup alert will display indicated success.

.. figure:: ../../src/ttkbootstrap/examples/images/long_running_determinate.png

.. note::
    If you set the parameter ``deaemon=True`` when creating the worker thread, it will close when your application
    window is closed, even if it has not yet finished. Most of the time this is the desired behavior. However, if you
    want the thread to continue to run until finished, even after the window has closed, you can ignore this parameter.

.. _threading: https://realpython.com/intro-to-python-threading/


Run this code live on repl.it_

.. _repl.it: https://replit.com/@IsraelDryer/long-running-determinate

.. literalinclude:: ../../src/ttkbootstrap/examples/long_running_determinate.py
    :language: python
