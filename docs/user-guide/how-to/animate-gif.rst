Animate a GIF
=============

An animated GIF is a stack of still frames. Tk shows one image at a time, so
animating one means loading each frame, then swapping the ``Label`` image on a
timer. This recipe builds a spinner that starts and stops.

Load the frames
---------------

``PhotoImage`` reads a single GIF frame at a time. Ask for a frame by number
with the ``format`` option — ``"gif -index 0"`` is the first frame:

.. code-block:: python

   import tkinter
   import ttkbootstrap as ttk

   app = ttk.App(theme="bootstrap-light")

   first = tkinter.PhotoImage(file="spinner.gif", format="gif -index 0", master=app)

There is no "how many frames?" call. Tk raises ``TclError`` once you ask for an
index past the end, which is the loop's stopping condition:

.. code-block:: python

   def load_frames(path, master):
       frames = []
       while True:
           try:
               frames.append(tkinter.PhotoImage(
                   file=path, format=f"gif -index {len(frames)}", master=master))
           except tkinter.TclError:
               return frames

   frames = load_frames("spinner.gif", app)

The list doubles as the reference that keeps the images alive — an image with no
Python reference is garbage collected and the widget goes blank. See
:doc:`Show images and icons <working-with-images>` for that gotcha in full.

Cycle through them
------------------

``after`` schedules the next frame; each frame schedules the one after it. Keep
the job id ``after`` returns so the animation can be stopped:

.. code-block:: python

   label = ttk.Label(app, image=frames[0])
   label.pack(padx=20, pady=20)

   index = 0
   job = None

   def next_frame():
       global index, job
       index = (index + 1) % len(frames)
       label.configure(image=frames[index])
       job = app.after(80, next_frame)

The ``% len(frames)`` wraps back to frame 0, so the animation loops forever.
The ``80`` is the delay in milliseconds — roughly 12 frames per second.

Start and stop it
-----------------

Starting is one ``after`` call; stopping cancels the pending job so no new frame
is ever scheduled:

.. code-block:: python

   def start():
       global job
       if job is None:
           job = app.after(80, next_frame)

   def stop():
       global job
       if job is not None:
           app.after_cancel(job)
           job = None

   ttk.Button(app, text="Start", command=start, bootstyle="success").pack(side="left")
   ttk.Button(app, text="Stop", command=stop, bootstyle="secondary").pack(side="left")

   app.mainloop()

.. note::

   Cancel the job before the window closes. A pending ``after`` that fires
   against a destroyed widget raises ``TclError``. If the animation outlives its
   own widget, cancel it on ``<Destroy>``:

   .. code-block:: python

      label.bind("<Destroy>", lambda e: stop())

Use each frame's own delay
--------------------------

The single ``80`` above gives every frame the same delay. A GIF can specify a
different delay per frame, and Tk does not expose it — Pillow does. Read the
durations once, then use the current frame's:

.. code-block:: python

   from PIL import Image

   def load_delays(path):
       delays = []
       with Image.open(path) as im:
           for n in range(im.n_frames):
               im.seek(n)
               delays.append(im.info.get("duration", 80))
       return delays

   delays = load_delays("spinner.gif")

   def next_frame():
       global index, job
       index = (index + 1) % len(frames)
       label.configure(image=frames[index])
       job = app.after(delays[index], next_frame)

Pillow is already a ttkbootstrap dependency, so this costs no extra install. It
is also the way to animate formats Tk cannot read at all, such as animated WebP
or APNG — load the frames with ``ImageTk.PhotoImage`` instead and swap them on
the same timer.

.. seealso::

   - :doc:`Show images and icons <working-with-images>` — loading images, Pillow
     formats, and the keep-a-reference gotcha.
   - :doc:`Run background work <threads>` — ``after`` for scheduling, and why
     long work must leave the main loop free.
   - :doc:`Events guide </user-guide/feature-guides/events>` — ``<Destroy>`` and
     the rest of the binding model.

Reference
---------

- :doc:`Label </reference/api/label>` — the ``image`` option this recipe swaps.
- :doc:`after and the event loop </reference/capabilities/after>` — ``after``,
  ``after_cancel``, and job ids.