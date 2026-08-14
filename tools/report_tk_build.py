"""Print the Tcl/Tk build a box actually carries.

Which Tk line a runner has is not something to assume: aqua's dpi baseline and
the scroll-event contract both differ between 8.6 and 9. The *patchlevel*
matters too -- a CPython patch release can change the Tk it links, and that is a
real behavior change, not a version-string detail. 3.13.14 -> 3.13.15 started
mapping menubars, which painted every X11 menubar in the border color; CI
reported only ``tk=8.6`` for both, so the drift was invisible for 8 days.

Needs a display, because the patchlevel comes from a real Tk interpreter --
``tkinter.Tcl()`` would load Tcl without Tk and report the wrong thing. Run it
under ``xvfb-run`` on x11.
"""
import sys
import tkinter


def main() -> None:
    root = tkinter.Tk()
    try:
        patchlevel = root.tk.call("info", "patchlevel")
    finally:
        root.destroy()

    print(
        f"{sys.platform} "
        f"python={sys.version.split()[0]} "
        f"tcl={tkinter.TclVersion} "
        f"tk={tkinter.TkVersion} "
        f"patchlevel={patchlevel}"
    )


if __name__ == "__main__":
    main()
