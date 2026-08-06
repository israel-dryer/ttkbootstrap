"""The `ttkb` command line.

One entry point for the things ttkbootstrap ships that are not library calls:
the version, the widget demo, the 1.x theme converter, and ttkcreator. Each was
reachable before only as its own `python -m ...` invocation, which nothing
surfaced.

The command installs under two names -- `ttkb` and `ttkbootstrap` -- that run
the same thing. Every `python -m` spelling still works, and is what to reach for
when the scripts directory is not on PATH::

    ttkb version
    ttkb demo
    ttkb convert-theme user.py -o brand.py
    ttkb creator
"""
import argparse
import sys

from ttkbootstrap import __version__


def _run_version(args, parser):
    """Print the installed version."""
    print(__version__)
    return 0


def _run_demo(args, parser):
    """Open the widget demo."""
    from ttkbootstrap.__main__ import main

    return main()


def _run_creator(args, parser):
    """Open ttkcreator."""
    try:
        from ttkcreator.__main__ import main
    except ImportError as error:
        # ttkcreator ships alongside ttkbootstrap but is a separate top-level
        # package, so it can be absent from a trimmed install.
        parser.exit(2, f"{parser.prog}: ttkcreator is not installed ({error}).\n")
    return main()


def _run_convert_theme(args, parser):
    """Convert a 1.x theme file."""
    from ttkbootstrap import convert_theme

    return convert_theme.run(args, parser)


def build_parser():
    """Return the `ttkb` argument parser."""
    parser = argparse.ArgumentParser(
        prog="ttkb",
        description="Command-line utilities for ttkbootstrap.",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=__version__
    )
    commands = parser.add_subparsers(dest="command", metavar="<command>")

    version = commands.add_parser(
        "version",
        help="print the installed ttkbootstrap version",
        description="Print the installed ttkbootstrap version.",
    )
    version.set_defaults(func=_run_version, parser=version)

    demo = commands.add_parser(
        "demo",
        help="open the widget demo",
        description="Open the widget demo -- every themed widget on one "
                    "window, with a theme picker.",
    )
    demo.set_defaults(func=_run_demo, parser=demo)

    # Imported lazily elsewhere, but the description and arguments are shared
    # here so the two spellings of the converter cannot drift apart.
    from ttkbootstrap import convert_theme

    convert = commands.add_parser(
        "convert-theme",
        help="convert a 1.x theme file to the 2.x Theme(...) form",
        description=convert_theme.DESCRIPTION,
    )
    convert_theme.add_arguments(convert)
    convert.set_defaults(func=_run_convert_theme, parser=convert)

    creator = commands.add_parser(
        "creator",
        help="open ttkcreator, the theme designer",
        description="Open ttkcreator: edit a theme's colors, preview the "
                    "result live, and export a Theme(...).register() snippet.",
    )
    creator.set_defaults(func=_run_creator, parser=creator)

    return parser


def main(argv=None):
    """Run the `ttkb` command line."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "func", None) is None:
        # No subcommand. argparse can require one, but the error it prints on
        # its own names the missing argument rather than showing what is
        # available -- and a bare `ttkb` is someone asking exactly that.
        parser.print_help()
        return 2
    # Each subparser records itself, so a failing command names itself in its
    # usage line rather than the bare `ttkb`.
    return args.func(args, args.parser)


if __name__ == "__main__":
    sys.exit(main())