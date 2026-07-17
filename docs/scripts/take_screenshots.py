"""Take light and dark screenshots of docs scene files.

Each docs page's screenshots come from a scene file in docs/screenshots/<name>.py.
A scene file defines a SCENES dict of self-contained callables; each creates its
own ttk.App and calls app.mainloop(). A file without SCENES is run as a plain
script (its module level ends in mainloop()).

Output (no scenes):  docs/_static/examples/<name>-light.png
                                            <name>-dark.png
Output (scenes):     docs/_static/examples/<name>-<scene>-light.png
                                            <name>-<scene>-dark.png

Images keep the capture box's full pixel density (2x on Retina); each rST
image directive pins the display size with ``:width: <W>px`` using the
logical size the harness prints per shot. That keeps HiDPI captures crisp
and makes the display size independent of which machine captured.

Canonical captures are taken on Windows (the docs' visual canon: Segoe UI,
native chrome for full-window shots). The harness also runs on macOS for
authoring/verification: it captures the Tk window by its CGWindowID
(`screencapture -l`), which works even when another app's full-screen Space
is active. That path needs `pip install pyobjc-framework-Quartz`; without it,
it falls back to a screen-region grab that requires the window's Space to be
the active one.

Usage:
    python docs/scripts/take_screenshots.py
    python docs/scripts/take_screenshots.py button            # single page
    python docs/scripts/take_screenshots.py button --light    # one theme only
    python docs/scripts/take_screenshots.py button --scene hero  # one scene only
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO        = Path(__file__).parent.parent.parent
SCREENSHOTS = REPO / "docs" / "screenshots"
OUTPUT      = REPO / "docs" / "_static" / "examples"

THEMES = [
    ("light", "bootstrap-light"),
    ("dark",  "bootstrap-dark"),
]

# Injected into each subprocess via python -c
_RUNNER = r"""
import os, importlib.util, sys
import ttkbootstrap as ttk
from ttkbootstrap.window import App

theme      = os.environ["TTKB_THEME"]
output     = os.environ["TTKB_OUTPUT"]
scene_file = os.environ["TTKB_SCENE_FILE"]
delay      = int(os.environ.get("TTKB_DELAY", "800"))
scene_name = os.environ.get("TTKB_SCENE", "")
probe_mode = os.environ.get("TTKB_PROBE", "")


def _windows_frame_rect(win):
    # Whole OS window (a dialog/Toplevel target, or the app itself) via DWM
    # extended frame bounds — the exact VISIBLE rect (no drop-shadow margin).
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    # Declare HWND-returning/taking signatures so 64-bit handles are not
    # silently truncated to a 32-bit c_int (the ctypes default).
    user32.GetParent.argtypes = [wintypes.HWND]
    user32.GetParent.restype = wintypes.HWND
    user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    user32.GetWindowRect.restype = wintypes.BOOL
    hwnd = user32.GetParent(win.winfo_id()) or win.winfo_id()
    rect = wintypes.RECT()
    ok = ctypes.windll.dwmapi.DwmGetWindowAttribute(
        wintypes.HWND(hwnd), ctypes.c_uint(9),  # DWMWA_EXTENDED_FRAME_BOUNDS
        ctypes.byref(rect), ctypes.sizeof(rect))
    if ok != 0:  # fall back to the full window rect (incl. shadow margin)
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top


def _grab_region(win, x, y, w, h):
    # Capture a screen region. On macOS ImageGrab returns physical (Retina)
    # pixels while Tk coordinates are logical points, so grab the full screen
    # and scale the crop box by the actual pixel ratio.
    from PIL import ImageGrab
    if sys.platform == "darwin":
        img = ImageGrab.grab()
        scale = img.width / win.winfo_screenwidth()
        box = tuple(round(v * scale) for v in (x, y, x + w, y + h))
        return img.crop(box)
    return ImageGrab.grab(bbox=(x, y, x + w, y + h))


def _mac_composite(app, rect_pts, fill):
    # Composite ALL of this process's on-screen windows (popups, popdowns,
    # dialogs) over a union rect, straight from the window server — works
    # regardless of the active Space. Returns a PIL image in physical pixels.
    import CoreFoundation
    import Quartz
    from PIL import Image
    infos = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    mine = [i for i in infos if i.get("kCGWindowOwnerPID") == os.getpid()]
    # The array is composited first-on-top; the app root sits on a raised
    # window level while the harness holds it topmost, so order by our own
    # rule — popups in front of the app window — rather than trusting the
    # server's current z-order.
    root_name = app.wm_title()
    mine.sort(key=lambda i: i.get("kCGWindowName") == root_name)
    ids = [i["kCGWindowNumber"] for i in mine]
    x, y, w, h = rect_pts
    rect = Quartz.CGRectMake(x, y, w, h)
    arr = CoreFoundation.CFArrayCreate(None, ids, len(ids), None)
    cgimg = Quartz.CGWindowListCreateImageFromArray(
        rect, arr, Quartz.kCGWindowImageBoundsIgnoreFraming)
    width = Quartz.CGImageGetWidth(cgimg)
    height = Quartz.CGImageGetHeight(cgimg)
    bpr = Quartz.CGImageGetBytesPerRow(cgimg)
    data = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(cgimg))
    img = Image.frombuffer("RGBA", (width, height), bytes(data),
                           "raw", "BGRA", bpr, 1)
    # Transparent gaps (outside window corners) take the theme background
    # instead of rendering black.
    canvas = Image.new("RGB", img.size, fill)
    canvas.paste(img, mask=img.getchannel("A"))
    return canvas


def _mac_grab_window(win, content_only, x, y, w, h):
    # Capture the Tk window by CGWindowID — the window server composites it
    # regardless of which Space is active or what overlaps it. Falls back to
    # a screen-region grab (active-Space only) if Quartz isn't installed.
    import subprocess, tempfile
    from PIL import Image
    try:
        import Quartz
    except ImportError:
        print("(pyobjc-framework-Quartz not installed; using region grab)",
              end=" ", flush=True)
        return _grab_region(win, x, y, w, h)
    infos = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID)
    mine = [i for i in infos if i.get("kCGWindowOwnerPID") == os.getpid()]
    match = [i for i in mine if i.get("kCGWindowName") == win.wm_title()] or mine
    info = match[0]
    bounds = info["kCGWindowBounds"]
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        path = f.name
    try:
        subprocess.run(
            ["screencapture", "-x", "-o", f"-l{info['kCGWindowNumber']}", path],
            check=True)
        with Image.open(path) as img:
            img.load()
    finally:
        os.unlink(path)
    # The image is in physical (Retina) pixels, bounds/Tk coords in points.
    # Keep the full pixel density — the rST pins the display size via
    # ``:width:`` (the logical size), so Retina captures stay crisp.
    scale = img.width / bounds["Width"]
    if content_only:
        # Crop the content area (Tk root coords) out of the whole-window image.
        box = tuple(round(v * scale) for v in
                    (x - bounds["X"], y - bounds["Y"],
                     x - bounds["X"] + w, y - bounds["Y"] + h))
        return img.crop(box), (w, h)
    return img, (round(bounds["Width"]), round(bounds["Height"]))


def _patch(cls):
    orig_init = cls.__init__
    orig_loop = cls.mainloop

    def _init(self, *args, **kwargs):
        for key in ("theme", "themename", "light_theme", "dark_theme"):
            kwargs.pop(key, None)
        orig_init(self, *args, theme=theme, **kwargs)
        if sys.platform == "darwin":
            # Native chrome (titlebars, menus) follows the SYSTEM appearance,
            # not the Tk theme — pin the app's appearance to the captured
            # theme so light shots get light chrome on a dark-mode host.
            # (After Tk exists: it owns the NSApplication instance.)
            try:
                from AppKit import NSApplication, NSAppearance
                name = ("NSAppearanceNameDarkAqua" if "dark" in theme
                        else "NSAppearanceNameAqua")
                NSApplication.sharedApplication().setAppearance_(
                    NSAppearance.appearanceNamed_(name))
            except ImportError:
                pass

    def _mainloop(self, *args, **kwargs):
        def _grab():
            # In parent-capture mode the harness parent takes the shot and
            # kills this process; the normal grab (whose timer can still fire
            # during native menu tracking) must not destroy the app under it.
            if getattr(self, "_ttkb_parent_mode", False):
                return
            # Scenes can set app._capture_target (a Toplevel, e.g. a dialog) to
            # capture that window instead of the app,
            # app._capture_full_window to grab the whole OS window (titlebar +
            # chrome) rather than just the content area, or
            # app._capture_extra (a list of popup Toplevels — popdowns,
            # calendars, tooltips) to composite them with the app content.
            target = getattr(self, "_capture_target", None)
            full = getattr(self, "_capture_full_window", False)
            extra = getattr(self, "_capture_extra", None)
            whole_window = full or target is not None
            win = target if target is not None else self
            win.update_idletasks()
            from pathlib import Path
            from PIL import Image
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            x = win.winfo_rootx()
            y = win.winfo_rooty()
            w = win.winfo_width()
            h = win.winfo_height()
            inset = 2  # trim window-border artifact from captured edges
            if extra:
                # Composite shot: the app content area plus popup windows
                # (popdowns, calendars, tooltips) — the union of their rects.
                pad = 4  # breathing room so popup edges aren't flush-cropped
                rects = [(x + inset, y + inset, w - 2 * inset, h - 2 * inset)]
                for item in extra:
                    # Accept a widget or a raw Tcl window path (some popups —
                    # e.g. the combobox popdown — exist only on the Tcl side).
                    if isinstance(item, str):
                        tkc = self.tk
                        tkc.call("update", "idletasks")
                        px, py, pw, ph = (
                            int(tkc.call("winfo", cmd, item))
                            for cmd in ("rootx", "rooty", "width", "height"))
                    else:
                        item.update_idletasks()
                        px, py, pw, ph = (item.winfo_rootx(), item.winfo_rooty(),
                                          item.winfo_width(), item.winfo_height())
                    # pad the popup only — padding the app content rect would
                    # bleed the capture into the window chrome
                    rects.append((px - pad, py - pad, pw + 2 * pad, ph + 2 * pad))
                ux = min(r[0] for r in rects)
                uy = min(r[1] for r in rects)
                ux2 = max(r[0] + r[2] for r in rects)
                uy2 = max(r[1] + r[3] for r in rects)
                logical = (ux2 - ux, uy2 - uy)
                if sys.platform == "darwin":
                    rgb = self.winfo_rgb(self.cget("background"))
                    fill = tuple(v // 256 for v in rgb)
                    img = _mac_composite(self, (ux, uy, *logical), fill)
                else:
                    img = _grab_region(win, ux, uy, *logical)
            elif sys.platform == "darwin":
                img, logical = _mac_grab_window(win, not whole_window,
                                                x + inset, y + inset,
                                                w - 2 * inset, h - 2 * inset)
            elif whole_window and sys.platform == "win32":
                # inset=2 cuts just inside the native frame so the docs'
                # single CSS border replaces it (no native + CSS double border)
                fx, fy, fw, fh = _windows_frame_rect(win)
                img = _grab_region(win, fx + inset, fy + inset,
                                   fw - 2 * inset, fh - 2 * inset)
                logical = (fw - 2 * inset, fh - 2 * inset)
            else:
                img = _grab_region(win, x + inset, y + inset,
                                   w - 2 * inset, h - 2 * inset)
                logical = (w - 2 * inset, h - 2 * inset)
            if sys.platform == "win32":
                # At >100% display scaling Tk coordinates are physical pixels;
                # report the CSS-pixel (logical) size for the rST ``:width:``.
                dpi_scale = win.winfo_fpixels("1i") / 96
                if dpi_scale > 1:
                    logical = (round(logical[0] / dpi_scale),
                               round(logical[1] / dpi_scale))
            # Default 720px logical keeps shots inside a sidebar'd doc page; a
            # scene can opt into a wider capture via app._capture_max_width.
            max_w = getattr(self, "_capture_max_width", 720)
            if logical[0] > max_w:
                ratio = max_w / logical[0]
                density = img.width / logical[0]
                logical = (max_w, max(1, round(logical[1] * ratio)))
                img = img.resize((round(logical[0] * density),
                                  max(1, round(logical[1] * density))),
                                 Image.LANCZOS)
            img.save(output)
            # The harness prints this as the ``:width:`` to pin in the rST.
            print(f"TTKB_LOGICAL {logical[0]}x{logical[1]}", flush=True)
            self.destroy()

        def _capture():
            self.attributes("-topmost", True)
            self.lift()
            self.update_idletasks()
            self.after(150, _grab)

        self.attributes("-topmost", True)
        self.after(0,  lambda: self.geometry("+200+100"))
        self.after(50, self.focus_force)
        self.after(delay, _capture)
        orig_loop(self, *args, **kwargs)

    def _capture_via_parent(self):
        # For popups that BLOCK the Tcl event loop while open (native aqua
        # menus): announce the content rect, then the scene posts the menu.
        # The harness parent process composites this process's windows —
        # including the native menu — and then kills the blocked child.
        import json
        self._ttkb_parent_mode = True
        if sys.platform == "darwin":
            # Menu tracking aborts under a pinned appearance that mismatches
            # the system — revert to the system appearance. The menu then
            # renders system-colored (a provisional mismatch on a dark-mode
            # host; the Windows canonical run replaces these shots).
            try:
                from AppKit import NSApplication
                NSApplication.sharedApplication().setAppearance_(None)
            except ImportError:
                pass
        self.update_idletasks()
        target = getattr(self, "_capture_target", None)
        win = target if target is not None else self
        rect = [win.winfo_rootx() + 2, win.winfo_rooty() + 2,
                win.winfo_width() - 4, win.winfo_height() - 4]
        rgb = self.winfo_rgb(self.cget("background"))
        fill = "#%02x%02x%02x" % tuple(v // 256 for v in rgb)
        print("TTKB_PARENT_GRAB " + json.dumps({"rect": rect, "fill": fill}),
              flush=True)

    cls.__init__ = _init
    cls.mainloop = _mainloop
    cls.capture_via_parent = _capture_via_parent


_patch(App)  # ttk.Window is the same class

spec = importlib.util.spec_from_file_location("_scene", scene_file)
mod  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

if probe_mode:
    import json
    print(json.dumps(list(getattr(mod, "SCENES", {}).keys())))
    sys.exit(0)

if scene_name and hasattr(mod, "SCENES") and scene_name in mod.SCENES:
    mod.SCENES[scene_name]()
# else: exec_module already ran the app (non-scene scripts)
"""


def _parent_composite_mac(pid: int, content_rect, fill_hex: str,
                          output: Path) -> tuple[int, int]:
    """Composite a child process's windows (incl. a posted native menu).

    Mirrors the in-process composite, but runs in the harness parent so it
    works while the child's event loop is blocked by native menu tracking.
    Menu windows sit on high window-server layers (>= 100); they define the
    union rect together with the announced content rect and draw on top.
    """
    import CoreFoundation
    import Quartz
    from PIL import Image
    import time
    mine = []
    deadline = time.time() + 4
    while time.time() < deadline:
        infos = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
        mine = [i for i in infos if i.get("kCGWindowOwnerPID") == pid]
        # wait until the posted menu (layer >= 100) is registered too
        if mine and any(i.get("kCGWindowLayer", 0) >= 100 for i in mine):
            break
        time.sleep(0.25)
    if not mine:
        # never composite an empty id list — Quartz falls back to the desktop
        raise RuntimeError(f"no on-screen windows for pid {pid}")
    if os.environ.get("TTKB_DEBUG"):
        for i in mine:
            print(f"  [debug] win {i['kCGWindowNumber']} "
                  f"name={i.get('kCGWindowName')!r} "
                  f"layer={i.get('kCGWindowLayer')}")
    pad = 4
    rects = [tuple(content_rect)]
    for info in mine:
        if info.get("kCGWindowLayer", 0) >= 100:  # pop-up menu windows
            b = info["kCGWindowBounds"]
            rects.append((b["X"] - pad, b["Y"] - pad,
                          b["Width"] + 2 * pad, b["Height"] + 2 * pad))
    ux = min(r[0] for r in rects)
    uy = min(r[1] for r in rects)
    ux2 = max(r[0] + r[2] for r in rects)
    uy2 = max(r[1] + r[3] for r in rects)
    mine.sort(key=lambda i: -i.get("kCGWindowLayer", 0))  # menus on top
    ids = [i["kCGWindowNumber"] for i in mine]
    rect = Quartz.CGRectMake(ux, uy, ux2 - ux, uy2 - uy)
    arr = CoreFoundation.CFArrayCreate(None, ids, len(ids), None)
    cgimg = Quartz.CGWindowListCreateImageFromArray(
        rect, arr, Quartz.kCGWindowImageBoundsIgnoreFraming)
    width = Quartz.CGImageGetWidth(cgimg)
    height = Quartz.CGImageGetHeight(cgimg)
    bpr = Quartz.CGImageGetBytesPerRow(cgimg)
    data = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(cgimg))
    img = Image.frombuffer("RGBA", (width, height), bytes(data),
                           "raw", "BGRA", bpr, 1)
    fill = tuple(int(fill_hex[i:i + 2], 16) for i in (1, 3, 5))
    canvas = Image.new("RGB", img.size, fill)
    canvas.paste(img, mask=img.getchannel("A"))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)
    return round(ux2 - ux), round(uy2 - uy)


def probe_scenes(source: Path) -> list[str]:
    """Return scene names from a screenshot script, or [] if none."""
    env = {
        **os.environ,
        "TTKB_THEME":      "bootstrap-light",
        "TTKB_OUTPUT":     "",
        "TTKB_SCENE_FILE": str(source),
        "TTKB_PROBE":      "1",
    }
    try:
        result = subprocess.run(
            [sys.executable, "-c", _RUNNER],
            env=env,
            timeout=10,
            cwd=str(REPO),
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout.strip()) if result.stdout.strip() else []
    except Exception:
        return []


def run_scene(source: Path, theme: str, output: Path, delay: int = 800,
              scene: str = "") -> tuple[bool, str]:
    """Run one capture; return (success, logical "WxH" for the rST :width:)."""
    env = {
        **os.environ,
        "TTKB_THEME":      theme,
        "TTKB_OUTPUT":     str(output),
        "TTKB_SCENE_FILE": str(source),
        "TTKB_DELAY":      str(delay),
    }
    if scene:
        env["TTKB_SCENE"] = scene
    import json
    import threading
    import time
    proc = subprocess.Popen(
        [sys.executable, "-c", _RUNNER],
        env=env,
        cwd=str(REPO),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    watchdog = threading.Timer(25, proc.kill)
    watchdog.start()
    logical = ""
    parent_grabbed = False
    try:
        for line in proc.stdout:
            line = line.strip()
            if line.startswith("TTKB_LOGICAL "):
                logical = line.split(" ", 1)[1].strip()
            elif line.startswith("TTKB_PARENT_GRAB ") and sys.platform == "darwin":
                # (On other platforms the marker is ignored; the watchdog
                # reaps the blocked child and the shot reports FAIL.)
                # The child is about to block in a native menu; give the menu
                # a beat to open, composite from here, then kill the child.
                time.sleep(0.5)
                info = json.loads(line.split(" ", 1)[1])
                size = _parent_composite_mac(proc.pid, info["rect"],
                                             info["fill"], output)
                logical = f"{size[0]}x{size[1]}"
                parent_grabbed = True
                proc.kill()
                break
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise
    finally:
        watchdog.cancel()
    if parent_grabbed:
        return True, logical
    if proc.returncode != 0:
        err = (proc.stderr.read() or "").strip()
        if err:
            print(err.splitlines()[-1], end="  ")
    return proc.returncode == 0, logical


def main():
    args = sys.argv[1:]

    filter_name  = None
    filter_scene = None
    themes       = THEMES

    for i, arg in enumerate(args):
        if arg == "--light":
            themes = [t for t in THEMES if t[0] == "light"]
        elif arg == "--dark":
            themes = [t for t in THEMES if t[0] == "dark"]
        elif arg == "--scene" and i + 1 < len(args):
            filter_scene = args[i + 1]
        elif not arg.startswith("--") and (i == 0 or args[i - 1] != "--scene"):
            filter_name = arg

    names = sorted(p.stem for p in SCREENSHOTS.glob("*.py"))
    if filter_name:
        names = [n for n in names if n == filter_name]

    if not names:
        print(f"No scene files found{f' matching {filter_name!r}' if filter_name else ''}.")
        sys.exit(1)

    OUTPUT.mkdir(parents=True, exist_ok=True)

    ok = failed = 0
    for name in names:
        source = SCREENSHOTS / f"{name}.py"
        scenes = probe_scenes(source)

        if filter_scene and scenes:
            scenes = [s for s in scenes if s == filter_scene]

        for suffix, theme in themes:
            if scenes:
                for scene in scenes:
                    out = OUTPUT / f"{name}-{scene}-{suffix}.png"
                    label = f"{name}:{scene}"
                    print(f"  {label:28s} [{suffix:5s}]  ", end="", flush=True)
                    try:
                        success, logical = run_scene(source, theme, out, scene=scene)
                        print(f"OK  {out.relative_to(REPO)}  ({logical})" if success
                              else "FAIL  non-zero exit")
                        ok += success; failed += not success
                    except subprocess.TimeoutExpired:
                        print("FAIL  timeout"); failed += 1
                    except Exception as exc:
                        print(f"FAIL  {exc}"); failed += 1
            else:
                out = OUTPUT / f"{name}-{suffix}.png"
                print(f"  {name:28s} [{suffix:5s}]  ", end="", flush=True)
                try:
                    success, logical = run_scene(source, theme, out)
                    print(f"OK  {out.relative_to(REPO)}  ({logical})" if success
                          else "FAIL  non-zero exit")
                    ok += success; failed += not success
                except subprocess.TimeoutExpired:
                    print("FAIL  timeout"); failed += 1
                except Exception as exc:
                    print(f"FAIL  {exc}"); failed += 1

    print(f"\n{ok} succeeded, {failed} failed.")


if __name__ == "__main__":
    main()
