Long-Running (Indeterminate)
============================
*When the number of tasks or time is unknown or variable*

You will often need to execute a task in tkinter that requires IO operations, or some other long-running task. For this
you will likely want to use a combination of threading, queues, and scheduling. In this example, I'm using the python
threading_ module to create a thread to run a simulated *blocking* task using the ``sleep`` function. This blocking
operation can't be run in the main thread with tkinter or the window will become unresponsive; so, a new thread is
created to handle this task.

While the thread is running, tkinter will start the progressbar in *indeterminate* mode, which means that the indicator
will shift from left to right in a cycle until it is commanded to stop. This mode is handy when you are running a task
or process, but you do not know how long it will take, and there is an *indeterminate* number of steps/time involved.

The thread needs to communicate to the application window when the process is finished. The vehicle for this is a
``queue.Queue``. When the process is started, the application will add the thread to the Queue. When the process
is complete, the task thread will mark this task as complete. While the thread is running, the application will poll the
queue every second to check if all tasks have been completed by scheduling the ``listen_for_complete_task`` method to
run in the main event loop every 1000ms (1 second) using the ``after`` method in tkinter. When all tasks in the queue
are completed, the progress bar will be stopped and a popup alert will display indicated success.

.. figure:: ../../src/ttkbootstrap/examples/images/long_running_indeterminate.png

.. note::
    You can change the speed of the progress indicator by passing a time in milliseconds to the ``start`` methods. This
    is 50ms by default.

.. _threading: https://realpython.com/intro-to-python-threading/


Run this code live on repl.it_

.. _repl.it: https://replit.com/@IsraelDryer/long-running-indeterminate

.. literalinclude:: ../../src/ttkbootstrap/examples/long_running_indeterminate.py
    :language: python
