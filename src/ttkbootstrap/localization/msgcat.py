"""Message catalog wrapper for ttkbootstrap localization.

A Python interface to the Tcl/Tk msgcat system: translate UI text by the user's
locale, set locale preferences, register per-language translations, and format
translated messages. See https://www.tcl.tk/man/tcl/TclCmd/msgcat.html.

All commands go through ``tk.call`` (not ``tk.eval`` with hand-built command
strings): each argument is passed as a proper Tcl value, so source strings
containing ``{ } [ ] $`` or spaces are handled without quoting tricks or
injection risk.
"""
from os import PathLike
from typing import Any, Optional, Union

from ttkbootstrap.window import get_default_root

#: Virtual event fired on the default root when the locale changes, so live
#: widgets (e.g. ``LocaleVar``) can re-translate themselves.
LOCALE_CHANGED = "<<LocaleChanged>>"


def normalize_locale(code: str) -> str:
    """Canonicalize a locale code so it reliably matches msgcat's catalog.

    msgcat matches locales case-insensitively using ``_`` as the region
    separator; this maps the common ``de-DE`` / ``pt_BR`` variants onto that
    canonical form (``de_de`` / ``pt_br``).
    """
    return str(code).replace("-", "_").lower()


class MessageCatalog:
    """Static wrapper for the Tcl/Tk `::msgcat` message catalog commands."""

    @staticmethod
    def translate(src: str, *fmtargs: Any) -> str:
        """Returns a translation of src according to the user's current
        locale.

        This is the main function used to localize an application.
        Instead of using an English string directly, an applicaton can
        pass the English string through `translate` and use the result.
        If an application is written for a single language in this
        fashion, then it is easy to add support for additional languages
        later simply by defining new message catalog entries.

        Parameters:

            src (str):
                The string to be translated.

            *fmtargs (Any, optional):
                Extra arguments passed internally to the Tcl
                [format](https://www.tcl-lang.org/man/tcl/TclCmd/format.html)
                command (msgcat applies `%`-style specifiers). For the Python
                `str.format` idiom, use `L` instead.

        Returns:

            str:
                The translated string.
        """
        root = get_default_root()
        return root.tk.call("::msgcat::mc", src, *fmtargs)

    @staticmethod
    def locale(newlocale: Optional[str] = None) -> str:
        """Sets the locale to newlocale. If newlocale is
        omitted, the current locale is returned, otherwise the current
        locale is set to newlocale. The initial locale defaults to the
        locale specified in the user's environment.

        Setting a new locale emits a `<<LocaleChanged>>` virtual event on the
        default root so live widgets can re-translate.

        Parameters:

            newlocale (str, optional):
                The new locale code used to define the language for the
                application. Default is None.

        Returns:

            str:
                The current locale name if newlocale is None or an empty
                string.
        """
        root = get_default_root()
        if newlocale:
            result = root.tk.call("::msgcat::mclocale", normalize_locale(newlocale))
            root.event_generate(LOCALE_CHANGED, when="tail")
            return result
        return root.tk.call("::msgcat::mclocale")

    @staticmethod
    def preferences() -> list[str]:
        """Returns an ordered list of the locales preferred by the user,
        based on the user's language specification. The list is ordered
        from most specific to the least preference. If the user has specified
        LANG=en_US_funky, this method would return {en_US_funky en_US en}.

        Returns:

            list[str]:
                Locales preferred by the user.
        """
        root = get_default_root()
        items = root.tk.splitlist(root.tk.call("::msgcat::mcpreferences"))
        # Keep every non-empty preference. Older code dropped the last item to
        # skip a trailing empty root locale, but Tcl 8.7 no longer emits it, so
        # that slice silently discarded a real preference.
        return [p for p in items if p]

    @staticmethod
    def load(dirname: Union[str, PathLike[str]]) -> int:
        """Searches the specified directory for files that match the
        language specifications returned by `preferences`. Each file
        located is sourced.

        Parameters:

            dirname (str or Pathlike object):
                The directory path of the msg files.

        Returns:

            int:
                Then number of message files which matched the
                specification and were loaded.
        """
        from pathlib import Path
        msgs = Path(dirname).as_posix()  # format path for tcl/tk

        root = get_default_root()
        return int(root.tk.call("::msgcat::mcload", msgs))

    @staticmethod
    def set(locale: str, src: str, translated: Optional[str] = None) -> None:
        """Sets the translation for 'src' to 'translated' in the
        specified locale. If translated is not specified, src is used
        for both.

        Parameters:

            locale (str):
                The local code used when translating the src.

            src (str):
                The original language string.

            translated (str, optional):
                The translated string. Default is None, in which case
                src is used.
        """
        root = get_default_root()
        root.tk.call("::msgcat::mcset", normalize_locale(locale), src, translated or "")

    @staticmethod
    def set_many(locale: str, *args: str) -> int:
        """Sets the translation for multiple source strings in *args in
        the specified locale and the current namespace. Must be an even
        number of args.

        Parameters:

            locale (str):
                The local code used when translating the src.

            *args (str):
                A series of src, translated pairs.

        Returns:

            int:
                The number of translation sets.
        """
        root = get_default_root()
        # mcmset takes a single {src trans ...} list; passing the tuple lets
        # Tkinter build a proper Tcl list (no manual brace-wrapping).
        return int(root.tk.call("::msgcat::mcmset", normalize_locale(locale), args))

    @staticmethod
    def max(*src: str) -> int:
        """Given several source strings, max returns the length of the
        longest translated string. This is useful when designing localized
        GUIs, which may require that all buttons, for example, be a fixed
        width (which will be the width of the widest button).

        Parameters:

            *src (str):
                A series of strings to compare

        Returns:

            int:
                The length of the longest str.
        """
        root = get_default_root()
        return int(root.tk.call("::msgcat::mcmax", *src))


if __name__ == "__main__":
    # testing
    from ttkbootstrap import localization

    localization.initialize_localities()
    MessageCatalog.locale("zh_cn")
    result = MessageCatalog.translate("Skip Messages")
    print(result)
    result = MessageCatalog.translate("yes")
    print(result)
    from ttkbootstrap.dialogs import Messagebox

    Messagebox.okcancel("this is my message")
