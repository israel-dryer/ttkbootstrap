"""Cross-platform verification for window and dialog positioning.

Run from the repo root on each platform -- Windows, macOS (aqua) and Linux
(x11):

    PYTHONPATH=src python tools/verify_positioning.py

Prints a PASS/FAIL line per check. Checks 4, 5, 6 and 7 open real windows;
4, 5 and 6 want a human to look at them, the rest are automatic.

WHY THIS IS PER-PLATFORM, AND WHY A GREEN RUN ON ONE BOX PROVES LITTLE

Centering a window before it is shown means predicting the size it will map at,
and what a window reports about itself before its first map differs by platform:
x11 says 1x1, while win32 reports the size Tk started the window at -- a
plausible-looking number that is not the size the content will map at. Any
check that trusts what the window reports therefore passes on whichever
platform it happens to be right about. That is not hypothetical: it is how the
demo shipped opening off-centre on Windows while every test passed.

Two consequences for anyone adding a check here. It has to fail against the bug
it is meant to catch -- verify that by reverting the fix, not by reading the
code. And the *shape* of the window matters as much as the platform: a root and
a Toplevel report differently, and so do content packed straight into the root
versus content packed after the root has settled (see check 7).

There is no CI, so these runs are manual. On macOS run it against both Tk lines
(8.6 and 9.0 -- the aqua scaling baseline moved in 9). On x11 run it twice,
with and without `screeninfo` installed: that is the only way to exercise the
Xinerama fallback in check 2.
"""
import re
import subprocess
import sys
import textwrap
import time
import tkinter

import ttkbootstrap as ttk
from ttkbootstrap.dialogs.message import MessageDialog
from ttkbootstrap.internal import positioning as p

results = []
skipped = []


def check(name, ok, detail="", always_show=False):
    results.append((name, ok))
    show = detail and (always_show or not ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{'  -- ' + detail if show else ''}")


def skip(name, why):
    """Record a check that could not run here, so it is never silently absent."""
    skipped.append(name)
    print(f"[SKIP] {name}  -- {why}")


def hold(window, seconds=2.5):
    """Keep a window on screen long enough to be looked at.

    `after(...)` followed by a single `update()` does not wait -- the callback
    has not fired yet, so the script races on and tears the window down. A LOOK
    line then points at something that was never really there.
    """
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            window.update()
        except tkinter.TclError:
            return  # closed by hand; nothing left to show
        time.sleep(0.05)


app = ttk.App(title="positioning verification")
app.geometry("420x220+80+80")
app.update()
winsys = ttk.windowing_system(app)
print(f"\nplatform={sys.platform}  windowingsystem={winsys}  tk={app.tk.call('info', 'patchlevel')}")
print(f"screeninfo installed: {p._HAS_SCREENINFO}")
print(f"Tk screen : {app.winfo_screenwidth()}x{app.winfo_screenheight()}")
print(f"Tk vroot  : {app.winfo_vrootwidth()}x{app.winfo_vrootheight()} "
      f"at ({app.winfo_vrootx()},{app.winfo_vrooty()})\n")

# --- 1. monitor discovery --------------------------------------------------
monitors = p._monitors()
print(f"monitors seen: {monitors}")
check("1. a monitor layout is discoverable", bool(monitors),
      "none found -- everything below falls back to the combined desktop")

# --- 2. the new Xinerama path specifically (X11 only) ----------------------
if winsys == "x11":
    p._XINERAMA_UNAVAILABLE = False
    xin = p._xinerama_monitors()
    print(f"xinerama says: {xin}")
    check("2. Xinerama answers directly (the no-screeninfo path)", bool(xin))
    if xin and monitors and p._HAS_SCREENINFO:
        check("2b. Xinerama agrees with screeninfo", sorted(xin) == sorted(monitors),
              f"xinerama={sorted(xin)} screeninfo={sorted(monitors)}", always_show=True)
else:
    check("2. Xinerama path is skipped off X11", p._xinerama_monitors() is None)

# --- 3. footprint == the size the dialog actually maps at ------------------
dlg = MessageDialog("ok", parent=app)
dlg.build()
footprint = dlg._footprint()
dlg._toplevel.deiconify()
dlg._toplevel.wait_visibility()
dlg._toplevel.update()
mapped = (dlg._toplevel.winfo_width(), dlg._toplevel.winfo_height())
check("3. footprint matches the mapped size", footprint == mapped,
      f"footprint={footprint} mapped={mapped}", always_show=True)
dlg.close()

# --- 4. a dialog lands fully inside one monitor ----------------------------
if monitors:
    # park the app so a centered dialog would cross the join between two screens
    seams = sorted({m[0] for m in monitors if m[0] != min(x for x, _, _, _ in monitors)})
    if seams:
        seam = seams[0]
        app.geometry(f"420x220+{seam - 210}+200")
        app.update()
        d = MessageDialog("Am I fully on one screen?", parent=app)
        d.build()
        d._locate()
        m = re.search(r"\+(-?\d+)\+(-?\d+)$", d._toplevel.geometry())
        x = int(m.group(1))
        w = d._footprint()[0]
        inside = any(mx <= x and x + w <= mx + mw for mx, _, mw, _ in monitors)
        check("4. a dialog near a seam stays inside one monitor", inside,
              f"dialog spans {x}..{x + w}, seam at {seam}", always_show=True)
        d._toplevel.deiconify()
        d._toplevel.update()
        print("    -> LOOK: the dialog above should sit wholly on one screen.")
        hold(d._toplevel)
        try:
            d.close()
        except Exception:
            pass
    else:
        check("4. a dialog near a seam stays inside one monitor", True, "single monitor -- n/a")
else:
    skip("4. a dialog near a seam stays inside one monitor",
         "no monitor layout on this platform (install screeninfo to exercise it)")

# --- 5. the themed file dialog (X11 default) -------------------------------
print("\n[MANUAL] 5. themed file dialog -- run this and confirm it opens fully")
print("            on-screen with the OK/Cancel buttons visible:\n")
print("    python -c \"import ttkbootstrap as ttk; app=ttk.App(); "
      "print(ttk.Querybox.get_open_filename(native=False, parent=app))\"\n")

# --- 6. a window centered before it has ever been shown --------------------
# The withdraw -> center -> deiconify recipe, which makes a window *appear*
# centered instead of appearing where the window manager put it and then
# jumping. Centering has to measure the size the window will map at: measuring
# its content request instead put the window's top-left at the screen center,
# out by half the window (298x216 for a 600x400 window on a 2560x1440 display).
probe = ttk.Toplevel(master=app, title="centered before shown", size=(600, 400))
probe.withdraw()

# Record the coordinates rather than reading geometry() back: a reparenting
# window manager reports the frame's position, so the readback is not what was
# applied. The frame offset moves where the window lands, not what we asked for.
applied = []
_real_geometry = probe.geometry
probe.geometry = lambda spec=None: (
    applied.append(spec) if spec is not None else None) or _real_geometry(spec)
probe.place_window_center()
del probe.geometry

probe.deiconify()
probe.update_idletasks()
probe.update()

mapped = (probe.winfo_width(), probe.winfo_height())
coords = re.search(r"\+(-?\d+)\+(-?\d+)$", applied[-1]) if applied else None
if coords is None:
    check("6. a window is centered before it is first shown", False,
          f"no +x+y was applied ({applied})", always_show=True)
else:
    ax, ay = int(coords.group(1)), int(coords.group(2))
    monitor = p._monitor_at_point(ax, ay)
    if monitor:
        mx, my, mw, mh = monitor
    else:
        mx, my = 0, 0
        mw, mh = probe.winfo_screenwidth(), probe.winfo_screenheight()
    # Centered for the size it actually maps at -- computed here rather than
    # borrowed from the positioning helpers, so this checks the answer instead
    # of restating how it was reached.
    want = (mx + (mw - mapped[0]) // 2, my + (mh - mapped[1]) // 2)
    check("6. a window is centered before it is first shown", (ax, ay) == want,
          f"applied=({ax},{ay}) want={want} mapped={mapped[0]}x{mapped[1]}",
          always_show=True)
print("    -> LOOK: that window should already be centered when it appears, and")
print("             should not flash or jump on the way in.")
hold(probe)
probe.destroy()

# --- 7. a content-sized ROOT, centered before its first map ----------------
# This is the demo's case (`python -m ttkbootstrap`) and the one check 6 misses:
# check 6 passes a size, which is remembered and used directly, while a window
# sized only by its content has to be measured. What a window reports before
# its first map is platform-specific -- x11 says 1x1, but win32 reports the
# size Tk started it at, a plausible number unrelated to the size the content
# will map at -- so a check that trusts it silently passes on the platform it
# is right on. It must be a *root*: on win32 a Toplevel does report 1x1, so a
# Toplevel version of this check passes even against the bug. Hence a separate
# process -- this one's root has long since been shown.
#
# The structure matters as much as the sizing: the content goes into a frame
# that is packed *afterwards*, exactly as the demo builds itself. Packing
# straight into the root instead lets Tk settle the root on the real size
# before anyone measures it, and the check then passes even against the bug.
_child = textwrap.dedent("""
    import ttkbootstrap as ttk
    app = ttk.App(title="content-sized root", minsize=(600, 0))
    app.withdraw()
    bag = ttk.Frame(app)
    for i in range(6):
        ttk.Button(bag, text=f"a reasonably wide button {i}").pack(padx=30, pady=6)
    app.update_idletasks()      # the root settles at its default size here
    bag.pack(fill="both", expand=True)
    predicted = app._unmapped_size()
    applied = []
    _g = app.geometry
    app.geometry = lambda spec=None: (
        applied.append(spec) if spec is not None else None) or _g(spec)
    app.place_window_center()
    del app.geometry
    app.deiconify()
    app.update_idletasks()
    app.update()
    print("RESULT", predicted[0], predicted[1],
          app.winfo_width(), app.winfo_height(), applied[-1])
""")
_proc = subprocess.run([sys.executable, "-c", _child], capture_output=True, text=True)
_line = next((ln for ln in _proc.stdout.splitlines() if ln.startswith("RESULT")), None)
if _line is None:
    check("7. a content-sized root is measured, not guessed", False,
          f"the child process reported nothing ({_proc.stderr.strip()[:200]})",
          always_show=True)
else:
    _, pw, ph, mw_, mh_, spec = _line.split(maxsplit=5)
    predicted, mapped = (int(pw), int(ph)), (int(mw_), int(mh_))
    check("7. a content-sized root is measured, not guessed", predicted == mapped,
          f"predicted={predicted[0]}x{predicted[1]} "
          f"mapped={mapped[0]}x{mapped[1]}", always_show=True)

    coords = re.search(r"\+(-?\d+)\+(-?\d+)$", spec)
    if coords is None:
        check("7b. a content-sized root is centered", False,
              f"no +x+y was applied ({spec})", always_show=True)
    else:
        ax, ay = int(coords.group(1)), int(coords.group(2))
        monitor = p._monitor_at_point(ax, ay)
        if monitor:
            mx, my, mw, mh = monitor
        else:
            mx, my = 0, 0
            mw, mh = app.winfo_screenwidth(), app.winfo_screenheight()
        want = (mx + (mw - mapped[0]) // 2, my + (mh - mapped[1]) // 2)
        check("7b. a content-sized root is centered", (ax, ay) == want,
              f"applied=({ax},{ay}) want={want} "
              f"mapped={mapped[0]}x{mapped[1]}", always_show=True)

failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} automatic checks passed")
if skipped:
    print(f"{len(skipped)} skipped: " + "; ".join(skipped))
if failed:
    print("failed: " + "; ".join(failed))
app.destroy()
