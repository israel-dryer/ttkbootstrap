"""
Demo: Meter dead-zone fix (issue #1047)

Drag the mouse around and below the zero position on each meter.
Before the fix, releasing in the gap snapped to MAX.
After the fix, the gap is split: upper half snaps to MIN, lower half to MAX.

Three meters cover the common arc configurations:
  - 270° arc  (default interactive meter)
  - 180° arc  (half-circle)
  - 360° arc  (full circle, no dead zone — should be unaffected)
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

app = ttk.Window(title="Meter Dead-Zone Fix — Issue #1047", size=(900, 420))

frame = ttk.Frame(app, padding=20)
frame.pack(fill=BOTH, expand=YES)

configs = [
    {"label": "270° arc (default)", "arcrange": 270, "arcoffset": 135},
    {"label": "180° arc", "arcrange": 180, "arcoffset": 180},
    {"label": "360° arc (no dead zone)", "arcrange": 360, "arcoffset": -90},
]

for cfg in configs:
    col = ttk.Frame(frame)
    col.pack(side=LEFT, expand=YES, fill=BOTH, padx=10)

    ttk.Label(col, text=cfg["label"], font="-size 11 -weight bold").pack(pady=(0, 6))

    meter = ttk.Meter(
        col,
        metersize=220,
        amountmin=0,
        amounttotal=100,
        amountused=0,
        interactive=True,
        arcrange=cfg["arcrange"],
        arcoffset=cfg["arcoffset"],
        subtext="drag me",
        bootstyle=INFO,
    )
    meter.pack()

    ttk.Label(
        col,
        text="Move mouse into the gap\nbelow zero — should snap\nto 0, not 100.",
        justify=CENTER,
        font="-size 9",
    ).pack(pady=(8, 0))

app.mainloop()