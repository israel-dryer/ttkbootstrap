---
title: Threading & Async
---

# Threading & Async

Tk's event loop is single-threaded. Any long-running work — network requests, file I/O, heavy computation — blocks the event loop and freezes the UI until it finishes.

This page covers the patterns ttkbootstrap recommends for keeping the UI responsive while doing background work.

---

## The constraint

All widget operations must happen on the main thread. Calling any Tk method from a background thread is not safe and produces unpredictable behavior — crashes, corrupted state, or silent failures.

The correct pattern is:

1. Start background work on a separate thread.
2. When the work completes, **schedule a UI update back on the main thread** using `after` or `after_idle`.

---

## Worker thread + Queue

The standard pattern uses `threading.Thread` for the work and `queue.Queue` to transfer results back to the main thread without calling Tk directly from the background:

```python
import threading
import queue
import ttkbootstrap as ttk

app = ttk.App(title="Background Task")

result_queue = queue.Queue()

status = ttk.Label(app, text="Ready")
status.pack(padx=20, pady=10)

progress = ttk.Progressbar(app, mode="indeterminate")
progress.pack(fill="x", padx=20)


def do_work():
    # Runs on a background thread — no Tk calls here
    import time
    time.sleep(3)                      # simulate work
    result_queue.put("Done!")


def poll_queue():
    try:
        result = result_queue.get_nowait()
        progress.stop()
        status.configure(text=result)
    except queue.Empty:
        app.after(100, poll_queue)     # check again in 100 ms


def start():
    status.configure(text="Working…")
    progress.start()
    threading.Thread(target=do_work, daemon=True).start()
    app.after(100, poll_queue)


ttk.Button(app, text="Start", command=start).pack(pady=10)
app.mainloop()
```

Key points:

- `do_work` runs on a daemon thread. It never touches Tk.
- `poll_queue` runs on the main thread via `after`. It reads from the queue and updates the UI.
- `queue.Queue` is thread-safe; `result_queue.put()` from a background thread is safe.
- Use `daemon=True` so the thread doesn't prevent the process from exiting.

---

## Posting directly with `after_idle`

For a one-shot UI update (no polling loop), the background thread can schedule a callback via `app.after_idle`. `after_idle` is the one Tk call that **is safe to invoke from a background thread**, because it queues a callable into the event loop rather than executing Tk operations directly:

```python
import threading
import ttkbootstrap as ttk

app = ttk.App(title="after_idle example")

label = ttk.Label(app, text="Waiting…")
label.pack(padx=20, pady=20)


def do_work():
    import time
    time.sleep(2)
    # Schedule the UI update back on the main thread
    app.after_idle(lambda: label.configure(text="Done!"))


threading.Thread(target=do_work, daemon=True).start()
app.mainloop()
```

!!! note "after_idle thread safety"
    `after_idle` (and `after`) are safe to call from a background thread. All other Tk/ttk methods are not. When in doubt, use the Queue pattern above — it makes the threading boundary explicit.

---

## Periodic updates with `after_repeat`

For work that streams results (progress, live data), `after_repeat` is cleaner than a manual reschedule loop:

```python
import threading
import queue
import ttkbootstrap as ttk

app = ttk.App()
result_queue = queue.Queue()

progress_label = ttk.Label(app, text="0 records loaded")
progress_label.pack(padx=20, pady=20)


def load_data():
    for i in range(1, 101):
        import time; time.sleep(0.05)
        result_queue.put(i)


def update_ui():
    count = 0
    while not result_queue.empty():
        count = result_queue.get_nowait()
    if count:
        progress_label.configure(text=f"{count} records loaded")


threading.Thread(target=load_data, daemon=True).start()
cancel = app.after_repeat(100, update_ui)   # poll every 100 ms

app.mainloop()
```

Call the returned `cancel()` function to stop the repeating schedule when the work is done.

---

## asyncio integration

Tk and `asyncio` each want to own the event loop. They cannot share one directly. The practical options are:

### Option A: asyncio in a background thread (recommended)

Run an `asyncio` event loop in a dedicated thread. Use `asyncio.run_coroutine_threadsafe` to submit coroutines to it, and the Queue or `after_idle` pattern to send results back to the UI:

```python
import asyncio
import threading
import queue
import ttkbootstrap as ttk

app = ttk.App()
result_queue = queue.Queue()

# Start an asyncio event loop on a background thread
loop = asyncio.new_event_loop()
threading.Thread(target=loop.run_forever, daemon=True).start()


async def fetch_data():
    await asyncio.sleep(2)             # simulate async I/O
    return "Fetched!"


def on_result(future):
    # Called on the asyncio thread — put result in queue, don't touch Tk
    result_queue.put(future.result())


def start_fetch():
    future = asyncio.run_coroutine_threadsafe(fetch_data(), loop)
    future.add_done_callback(on_result)
    app.after(100, poll)


def poll():
    try:
        result = result_queue.get_nowait()
        ttk.Label(app, text=result).pack()
    except queue.Empty:
        app.after(100, poll)


ttk.Button(app, text="Fetch", command=start_fetch).pack(padx=20, pady=20)
app.mainloop()
```

### Option B: `asyncio.run` with Tk polling

For simpler cases, run a short asyncio operation to completion in a thread and report back via `after_idle`:

```python
import asyncio
import threading
import ttkbootstrap as ttk

app = ttk.App()
label = ttk.Label(app, text="Waiting…")
label.pack(padx=20, pady=20)


async def fetch():
    await asyncio.sleep(1)
    return "Result"


def run_async():
    result = asyncio.run(fetch())
    app.after_idle(lambda: label.configure(text=result))


threading.Thread(target=run_async, daemon=True).start()
app.mainloop()
```

### Trade-offs

| Approach | Best for | Trade-off |
|---|---|---|
| Queue + thread | CPU work, blocking I/O | Simple; polling adds small latency |
| `after_idle` from thread | One-shot result delivery | Slightly lower latency; less explicit |
| asyncio in background thread | Async I/O, network calls | More setup; clean async code |
| `asyncio.run` in thread | Simple one-off async ops | Each call starts a new event loop |

Avoid libraries that require `asyncio.run()` at the top level alongside a Tk `mainloop()` — they are not directly composable without the background-thread approach.

---

## What not to do

**Don't call Tk methods from background threads:**

```python
# Wrong — do_work is called from a background thread
def do_work():
    label.configure(text="Done!")     # NOT SAFE
```

**Don't block the main thread:**

```python
# Wrong — blocks the event loop; UI freezes
def on_click():
    result = requests.get("https://example.com")   # blocks until complete
    label.configure(text=result.text)
```

**Don't use `time.sleep` in event handlers:**

```python
# Wrong — freezes the UI for 5 seconds
def on_click():
    time.sleep(5)
    label.configure(text="Done")
```

Use `app.after(5000, callback)` instead.

---

## Summary

| Pattern | Use when |
|---|---|
| Worker thread + Queue | Most background work |
| `after_idle` from thread | One-shot result, no polling loop |
| `after_repeat` | Streaming progress, live data |
| asyncio in background thread | Async I/O-heavy code |

---

## Next steps

- [Event Loop](event-loop.md) — how the Tk event loop dispatches work
- [Performance](performance.md) — other sources of UI latency
- [Capabilities → After](../reference/capabilities/after.md) — `after`, `after_idle`, and `after_repeat` API reference
