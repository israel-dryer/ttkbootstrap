"""Take light and dark screenshots of docs scene files.

Each docs page's screenshots come from a scene file in docs/screenshots/<name>.py.
A scene file defines a SCENES dict of self-contained callables; each creates its
own ttk.App and calls app.mainloop(). A file without SCENES is run as a plain
script (its module level ends in mainloop()).

Output (no scenes):  docs/_static/examples/<name>-light.png
                                            <name>-dark.png
Output (scenes):     docs/_static/examples/<name>-<scene>-light.png
                                            <name>-<scene>-dark.png

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
    scale = img.width / bounds["Width"]
    if content_only:
        # Crop the content area (Tk root coords) out of the whole-window image.
        box = tuple(round(v * scale) for v in
                    (x - bounds["X"], y - bounds["Y"],
                     x - bounds["X"] + w, y - bounds["Y"] + h))
        img = img.crop(box)
    if scale != 1:
        # Normalize to logical size so the docs show the widget at its
        # on-screen size — the same density the Windows canon captures at.
        img = img.resize((max(1, round(img.width / scale)),
                          max(1, round(img.height / scale))),
                         Image.LANCZOS)
    return img


def _patch(cls):
    orig_init = cls.__init__
    orig_loop = cls.mainloop

    def _init(self, *args, **kwargs):
        for key in ("theme", "themename", "light_theme", "dark_theme"):
            kwargs.pop(key, None)
        orig_init(self, *args, theme=theme, **kwargs)

    def _mainloop(self, *args, **kwargs):
        def _grab():
            # Scenes can set app._capture_target (a Toplevel, e.g. a dialog) to
            # capture that window instead of the app, and/or
            # app._capture_full_window to grab the whole OS window (titlebar +
            # chrome) rather than just the content area.
            target = getattr(self, "_capture_target", None)
            full = getattr(self, "_capture_full_window", False)
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
            if sys.platform == "darwin":
                img = _mac_grab_window(win, not whole_window,
                                       x + inset, y + inset,
                                       w - 2 * inset, h - 2 * inset)
            elif whole_window and sys.platform == "win32":
                # inset=2 cuts just inside the native frame so the docs'
                # single CSS border replaces it (no native + CSS double border)
                fx, fy, fw, fh = _windows_frame_rect(win)
                img = _grab_region(win, fx + inset, fy + inset,
                                   fw - 2 * inset, fh - 2 * inset)
            else:
                img = _grab_region(win, x + inset, y + inset,
                                   w - 2 * inset, h - 2 * inset)
            # Default 720px keeps shots crisp inside a sidebar'd doc page; a
            # scene can opt into a wider capture via app._capture_max_width.
            max_w = getattr(self, "_capture_max_width", 720)
            if img.width > max_w:
                ratio = max_w / img.width
                img = img.resize((max_w, max(1, int(img.height * ratio))), Image.LANCZOS)
            img.save(output)
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

    cls.__init__ = _init
    cls.mainloop = _mainloop


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
              scene: str = "") -> bool:
    env = {
        **os.environ,
        "TTKB_THEME":      theme,
        "TTKB_OUTPUT":     str(output),
        "TTKB_SCENE_FILE": str(source),
        "TTKB_DELAY":      str(delay),
    }
    if scene:
        env["TTKB_SCENE"] = scene
    result = subprocess.run(
        [sys.executable, "-c", _RUNNER],
        env=env,
        timeout=20,
        cwd=str(REPO),
    )
    return result.returncode == 0


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
                        success = run_scene(source, theme, out, scene=scene)
                        print(f"OK  {out.relative_to(REPO)}" if success else "FAIL  non-zero exit")
                        ok += success; failed += not success
                    except subprocess.TimeoutExpired:
                        print("FAIL  timeout"); failed += 1
                    except Exception as exc:
                        print(f"FAIL  {exc}"); failed += 1
            else:
                out = OUTPUT / f"{name}-{suffix}.png"
                print(f"  {name:28s} [{suffix:5s}]  ", end="", flush=True)
                try:
                    success = run_scene(source, theme, out)
                    print(f"OK  {out.relative_to(REPO)}" if success else "FAIL  non-zero exit")
                    ok += success; failed += not success
                except subprocess.TimeoutExpired:
                    print("FAIL  timeout"); failed += 1
                except Exception as exc:
                    print(f"FAIL  {exc}"); failed += 1

    print(f"\n{ok} succeeded, {failed} failed.")


if __name__ == "__main__":
    main()
