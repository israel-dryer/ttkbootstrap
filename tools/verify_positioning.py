"""Cross-platform verification for #1310 / PR #1312 (dialog positioning).

Run from the repo root on each platform:

    PYTHONPATH=src python tools/verify_positioning.py

Prints a PASS/FAIL line per check. Checks 4 and 5 open real windows and need a
human to look at them; everything else is automatic.
"""
import re
import sys

import ttkbootstrap as ttk
from ttkbootstrap.dialogs.message import MessageDialog
from ttkbootstrap.internal import positioning as p

results = []


def check(name, ok, detail="", always_show=False):
    results.append((name, ok))
    show = detail and (always_show or not ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{'  -- ' + detail if show else ''}")


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
        app.after(2500, d.close)
        app.update()
        try:
            d.close()
        except Exception:
            pass
    else:
        check("4. a dialog near a seam stays inside one monitor", True, "single monitor -- n/a")

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
app.after(2000, probe.destroy)
app.update()

failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} automatic checks passed")
if failed:
    print("failed: " + "; ".join(failed))
app.destroy()
