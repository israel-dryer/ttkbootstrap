"""Screenshot scenes for docs/user-guide/how-to/threads.rst."""

import ttkbootstrap as ttk


def clock():
    app = ttk.App(title="Clock")
    ttk.Label(app, text="14:32:07", font="-size 24").pack(padx=40, pady=40)
    app._capture_full_window = True
    app.mainloop()


def worker():
    # The worker window mid-run: Working… status, the progressbar partway, and
    # the (disabled, for the duration) Start button.
    app = ttk.App(title="Worker")
    frm = ttk.Frame(app, padding=20)
    frm.pack()
    ttk.Label(frm, text="Working…", bootstyle="warning").pack()
    ttk.Progressbar(frm, value=60, length=220, bootstyle="success").pack(pady=12)
    ttk.Button(frm, text="Start", bootstyle="primary", state="disabled").pack()
    app._capture_full_window = True
    app.mainloop()


SCENES = {
    "clock": clock,
    "worker": worker,
}
