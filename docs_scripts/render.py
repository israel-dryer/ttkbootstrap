"""Manifest-driven screenshot renderer for ttkbootstrap docs.

Reads `docs_scripts/screenshots.toml`, renders each shot once per requested
theme variant (default: light + dark, mapped to the `docs-light`/`docs-dark`
themes), and writes PNGs to `docs/assets/{light,dark}/<slug>.png`.

Each shot points at a factory `module:attr` callable. The factory receives a
`parent` Frame (the renderer's padded capture target) and builds widgets
inside it. It may optionally return a no-arg `finalize` callable; if
returned, the renderer invokes it just before screen grab so that visual
state flags like `state(["focus"])` and `state(["hover"])` survive any
focus-out events Tk fires while the window is becoming visible.

Multi-instance Tk lifecycle is brittle (named-font registration and other
process-global style state leaks across `App.destroy()`/recreate cycles),
so each shot is rendered in its own subprocess. The parent process drives
the manifest; each child process renders exactly one (shot, theme) pair.

Usage:
    python -m docs_scripts.render
    python -m docs_scripts.render --slug widgets-button-solid
    python -m docs_scripts.render --page widgets/actions/button.md
    python -m docs_scripts.render --theme light
"""

from __future__ import annotations

import argparse
import importlib
import subprocess
import sys
import tkinter
import tomllib
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

# Silence deprecation noise (e.g. `bootstyle=`) in factory code; the renderer
# is dev tooling and we don't want stderr clutter mid-batch.
warnings.simplefilter("ignore")

from PIL import Image, ImageGrab  # noqa: E402

import ttkbootstrap as ttk  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "docs_scripts" / "screenshots.toml"
ASSETS_DIR = REPO_ROOT / "docs" / "assets"

THEME_NAMES = {"light": "docs-light", "dark": "docs-dark"}


@dataclass
class Shot:
    slug: str
    page: str
    factory: str
    themes: list[str] = field(default_factory=lambda: ["light", "dark"])
    padding: int = 16

    def call_factory(self, parent: tkinter.Widget) -> Callable[[], None] | None:
        module_name, _, attr = self.factory.partition(":")
        if not module_name or not attr:
            raise ValueError(f"factory must be 'module:attr', got {self.factory!r}")
        module = importlib.import_module(module_name)
        fn: Callable[[tkinter.Widget], Callable[[], None] | None] = getattr(module, attr)
        return fn(parent)


def load_manifest(path: Path = MANIFEST_PATH) -> list[Shot]:
    data = tomllib.loads(path.read_text())
    shots = [Shot(**entry) for entry in data["shots"]]
    slugs = [s.slug for s in shots]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        raise ValueError(f"duplicate slug(s) in manifest: {sorted(dupes)}")
    return shots


def _normalize_to_logical(img: Image.Image, bbox: tuple[int, int, int, int]) -> Image.Image:
    """Downscale a Retina/HiDPI grab back to logical-pixel dimensions.

    `bbox` is in screen (logical) coordinates; the captured image may be 2x or
    3x that on HiDPI displays. Always resize to bbox dimensions for
    deterministic output across machines.
    """
    target_w = bbox[2] - bbox[0]
    target_h = bbox[3] - bbox[1]
    if img.size == (target_w, target_h):
        return img
    return img.resize((target_w, target_h), Image.LANCZOS)


def render_shot(shot: Shot, theme: str, out_path: Path) -> None:
    """Render `shot` against `theme` and save to `out_path`.

    The window is briefly run on a real Tk mainloop so the OS actually
    composites and draws it; capture happens inside an `after` callback,
    after which the loop quits and the app is destroyed.
    """
    # We deliberately keep the window decorated (no override_redirect):
    # override_redirect interferes with WM focus event handling, which kills
    # `state(["focus"])` and `state(["hover"])` visuals on widgets we
    # manually flagged in factories. The capture target is the inner padded
    # Frame, not the window itself, so the titlebar is naturally excluded.
    app = ttk.App(theme=THEME_NAMES[theme], hdpi=False)
    error: list[BaseException] = []

    # The factory builds into this padded Frame; the Frame is what gets
    # captured. Padding lives on the Frame itself so the bbox can equal the
    # Frame's full screen rect with no inflation — meaning we never spill
    # outside the window into adjacent screen content.
    capture_frame = ttk.Frame(app, padding=shot.padding)
    capture_frame.pack()

    finalize_holder: list[Callable[[], None]] = []

    def _capture() -> None:
        try:
            # Re-apply any visual state flags the factory wants to be
            # in effect at capture time (focus rings, hover shading) —
            # Tk's WM may have cleared them between deiconify and now.
            for fn in finalize_holder:
                fn()
            # `update()` (not just update_idletasks) is needed so ttk
            # actually redraws after the state change before we grab.
            app.update()
            x = capture_frame.winfo_rootx()
            y = capture_frame.winfo_rooty()
            w = capture_frame.winfo_width()
            h = capture_frame.winfo_height()
            bbox = (x, y, x + w, y + h)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            img = ImageGrab.grab(bbox=bbox)
            img = _normalize_to_logical(img, bbox)
            img.save(out_path, "PNG")
        except BaseException as exc:  # noqa: BLE001
            error.append(exc)
        finally:
            app.quit()

    try:
        finalize = shot.call_factory(capture_frame)
        if finalize is not None:
            finalize_holder.append(finalize)
        # Position the window away from the screen edge so the bbox is
        # always within the visible display area.
        app.geometry("+200+200")
        app.deiconify()
        app.lift()
        app.attributes("-topmost", True)
        # NOTE: deliberately no `focus_force()`. Forcing focus to the app
        # clears any `state(["focus"])` we manually set on individual
        # widgets in the factory, which kills focus rings and hover shading
        # in the captured image. Topmost + lift is enough to bring the
        # borderless window to the front.
        # Give Cocoa enough runloop ticks to actually map, raise, and paint
        # the window before we capture.
        app.after(500, _capture)
        app.mainloop()
        if error:
            raise error[0]
    finally:
        app.destroy()


def _render_in_subprocess(slug: str, theme: str) -> int:
    """Spawn a child Python that renders exactly one (slug, theme) pair.

    Per-shot subprocess isolation is the simplest defense against Tk
    process-global state leaks (named fonts, style registrations, the
    `_default_root` ref) that surface when multiple `App` instances are
    created and destroyed in a single process.
    """
    return subprocess.call(
        [sys.executable, "-m", "docs_scripts.render", "--_render-one", slug, "--_theme", theme]
    )


def render_all(
    shots: list[Shot],
    *,
    filter_slug: str | None = None,
    filter_page: str | None = None,
    themes: list[str] | None = None,
) -> int:
    targets = shots
    if filter_slug:
        targets = [s for s in targets if s.slug == filter_slug]
    if filter_page:
        targets = [s for s in targets if s.page == filter_page]
    if not targets:
        print("no shots matched filter", file=sys.stderr)
        return 1
    requested = set(themes) if themes else None
    n = 0
    failed = 0
    for shot in targets:
        for theme in shot.themes:
            if requested and theme not in requested:
                continue
            out = ASSETS_DIR / theme / f"{shot.slug}.png"
            print(f"  → {out.relative_to(REPO_ROOT)}")
            rc = _render_in_subprocess(shot.slug, theme)
            if rc != 0:
                failed += 1
                print(f"    failed (exit {rc})", file=sys.stderr)
            n += 1
    print(f"rendered {n - failed}/{n} image(s)")
    return 0 if failed == 0 else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Render docs screenshots from the manifest.")
    p.add_argument("--slug", help="Render only the shot with this slug.")
    p.add_argument("--page", help="Render only shots for this docs page (e.g. widgets/actions/button.md).")
    p.add_argument(
        "--theme",
        action="append",
        choices=["light", "dark"],
        help="Render only this theme variant (may be repeated).",
    )
    # Internal flags used by the per-shot subprocess. Hidden from the user.
    p.add_argument("--_render-one", dest="render_one", help=argparse.SUPPRESS)
    p.add_argument("--_theme", dest="single_theme", help=argparse.SUPPRESS)
    args = p.parse_args(argv)
    shots = load_manifest()
    if args.render_one:
        # Child process: render exactly one (slug, theme).
        match = next((s for s in shots if s.slug == args.render_one), None)
        if match is None:
            print(f"unknown slug: {args.render_one}", file=sys.stderr)
            return 2
        out = ASSETS_DIR / args.single_theme / f"{match.slug}.png"
        render_shot(match, args.single_theme, out)
        return 0
    return render_all(shots, filter_slug=args.slug, filter_page=args.page, themes=args.theme)


if __name__ == "__main__":
    raise SystemExit(main())
