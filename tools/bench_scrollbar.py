"""Time scrollbar redraws: ttkbootstrap's styles against stock tkinter/ttk.

Each run moves the thumb `--iters` times per thumb size (5% to 90% of the
trough) and times one redraw per move, including the X server finishing it,
then reports the median. Every variant runs in a fresh interpreter, because
importing ttkbootstrap restyles ttk process-wide.

A tall thumb is where an image-tiled thumb shows: ttk tiles the middle of an
image element, so its cost grows with thumb length, while a stock ttk thumb
costs the same at any length. Run at the standard 96 dpi to compare against CI
(Xvfb is pinned there):

    python tools/bench_scrollbar.py --scaling 1.3333

`--scaling` matters: the thumb's images are sized in logical units, so the
display density changes what gets drawn. Without it the display's own scaling
is used. Needs a display; run it under ``xvfb-run`` on a headless x11 box.
"""
import argparse
import json
import statistics
import subprocess
import sys
import time

VARIANTS = {
    "tk.Scrollbar (classic)": "tk_classic",
    "ttk.Scrollbar (clam)": "ttk_clam",
    "ttkbootstrap default": "default",
    "ttkbootstrap round": "round",
    "ttkbootstrap thin": "thin",
}
BASELINE = "ttk_clam"

THUMB_FRACTIONS = (0.05, 0.25, 0.5, 0.9)


def _dpi_aware():
    """What `Window(scaling=)` does on Windows before setting `tk scaling`, so
    the stock variants draw at the same density as ttkbootstrap's."""
    try:
        from ctypes import windll
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def _build(kind, scaling):
    import tkinter as tk
    from tkinter import ttk

    if kind in ("tk_classic", "ttk_clam"):
        if scaling is not None:
            _dpi_aware()
        root = tk.Tk()
        if scaling is not None:
            root.tk.call("tk", "scaling", scaling)
        if kind == "tk_classic":
            return root, tk.Scrollbar(root, orient="vertical")
        ttk.Style(root).theme_use("clam")
        return root, ttk.Scrollbar(root, orient="vertical")

    import ttkbootstrap as ttkb
    root = ttkb.Window(theme="bootstrap-light", scaling=scaling)
    return root, ttkb.Scrollbar(root, orient="vertical", bootstyle=kind)


def _sync(root):
    """Run Tk's pending redraws and wait for the X server to finish them:
    `winfo_pointerxy` is a server round trip, which returns only after every
    request queued before it."""
    root.update_idletasks()
    root.winfo_pointerxy()


def _median_us(root, step, iters):
    samples = []
    for i in range(iters):
        start = time.perf_counter()
        step(i)
        _sync(root)
        samples.append(time.perf_counter() - start)
    return statistics.median(samples) * 1e6


def _child(kind, iters, height, scaling):
    root, sb = _build(kind, scaling)
    root.geometry(f"60x{height}+50+50")
    sb.pack(fill="y", expand=True)
    root.update()
    time.sleep(0.3)  # let the window manager map the window
    root.update()

    results = {}
    for frac in THUMB_FRACTIONS:
        span = 1.0 - frac

        def move(i):
            first = span * i / (iters - 1)
            sb.set(first, first + frac)

        _median_us(root, move, 20)  # warm-up: image creation, caches
        results[str(frac)] = _median_us(root, move, iters)

    if kind != "tk_classic":
        # hover swaps the thumb's state colors / images
        sb.set(0.1, 0.6)
        results["hover"] = _median_us(
            root, lambda i: sb.state(["active" if i % 2 == 0 else "!active"]), iters)

    print(json.dumps({"tk_scaling": float(root.tk.call("tk", "scaling")),
                      "results": results}))
    root.destroy()


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--iters", type=int, default=300,
                        help="redraws timed per thumb size (default 300, min 2)")
    parser.add_argument("--height", type=int, default=800,
                        help="scrollbar height in px (default 800)")
    parser.add_argument("--scaling", type=float, default=None,
                        help="Tk scaling for every variant; 1.3333 is 96 dpi "
                             "(default: the display's own)")
    parser.add_argument("--child", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.iters < 2:
        parser.error("--iters must be at least 2")

    if args.child:
        _child(args.child, args.iters, args.height, args.scaling)
        return

    import tkinter
    from importlib.metadata import version
    import ttkbootstrap

    print(f"python {sys.version.split()[0]}, tk {tkinter.TkVersion}, "
          f"ttkbootstrap {version('ttkbootstrap')} ({ttkbootstrap.__file__})")

    runs = {}
    for label, kind in VARIANTS.items():
        cmd = [sys.executable, __file__, "--child", kind,
               "--iters", str(args.iters), "--height", str(args.height)]
        if args.scaling is not None:
            cmd += ["--scaling", str(args.scaling)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode:
            print(f"{label}: failed\n{proc.stderr}")
            continue
        runs[kind] = (label, json.loads(proc.stdout.strip().splitlines()[-1]))

    scaling = next(iter(runs.values()))[1]["tk_scaling"]
    print(f"tk scaling {scaling:.4f}, scrollbar {args.height}px, "
          f"{args.iters} redraws per column\n")
    columns = [str(f) for f in THUMB_FRACTIONS] + ["hover"]
    header = f"{'median us per redraw':26s}" + "".join(
        f"{'hover' if c == 'hover' else f'thumb {float(c):.0%}':>12s}" for c in columns)
    print(header)
    print("-" * len(header))
    base = runs.get(BASELINE, (None, {"results": {}}))[1]["results"]
    for label, info in runs.values():
        res = info["results"]
        cells = ""
        for c in columns:
            if c not in res:
                cells += f"{'-':>12s}"
            elif base.get(c):
                cells += f"{res[c]:6.0f} {res[c] / base[c]:4.1f}x"
            else:
                cells += f"{res[c]:12.0f}"
        print(f"{label:26s}{cells}")
    print(f"\n(Nx = times the {VARIANTS_LABEL[BASELINE]} median)")


VARIANTS_LABEL = {kind: label for label, kind in VARIANTS.items()}

if __name__ == "__main__":
    main()
