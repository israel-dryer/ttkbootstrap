"""Message catalog wrapper for ttkbootstrap localization.

This module provides a Python interface to the Tcl/Tk msgcat (message catalog)
system for managing multi-lingual user interfaces. It enables applications to
translate UI text based on the user's locale.

Classes:
    MessageCatalog: Static wrapper for Tcl/Tk msgcat commands

The MessageCatalog allows applications to:
    - Translate strings based on current locale
    - Set locale preferences
    - Define message translations for multiple languages
    - Format translated messages with arguments

See also:
    https://www.tcl.tk/man/tcl/TclCmd/msgcat.html

Example:
    ```python
    from ttkbootstrap.localization import MessageCatalog

    # Set locale
    MessageCatalog.locale('de')

    # Define German translations
    MessageCatalog.set('de', 'Hello', 'Hallo')
    MessageCatalog.set('de', 'Goodbye', 'Auf Wiedersehen')

    # Translate
    greeting = MessageCatalog.translate('Hello')  # Returns 'Hallo'
    farewell = MessageCatalog.translate('Goodbye')  # Returns 'Auf Wiedersehen'
    ```
"""
from os import PathLike
from typing import Any, Optional, Union

from ttkbootstrap.window import get_default_root


class MessageCatalog:
    @staticmethod
    def __join(*args: Any) -> str:
        """Join multiple format arguments into a joined argument string."""
        new_args = []
        for arg in args:
            if isinstance(arg, str):
                # remove surrounding quotes
                stripped = str(arg).strip('"')
                new_args.append("{%s}" % stripped)
            else:
                new_args.append(str(arg))
        return " ".join(new_args)

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

            *fmtargs (tuple, optional):
                Extra arguments passed internally to the
                [format](https://www.tcl-lang.org/man/tcl/TclCmd/format.html) package.

        Returns:

            str:
                The translated string.
        """
        root = get_default_root()

        command = '::msgcat::mc {%s}' % src
        if fmtargs:
            command = f"{command} {MessageCatalog.__join(*fmtargs)}"
        return root.tk.eval(command)

    @staticmethod
    def locale(newlocale: Optional[str] = None) -> str:
        """ "This function sets the locale to newlocale. If newlocale is
        omitted, the current locale is returned, otherwise the current
        locale is set to newlocale. The initial locale defaults to the
        locale specified in the user's environment.

        Parameters:

            newlocale (str):
                The new locale code used to define the language for the
                application.

        Returns:

            str:
                The current locale name if newlocale is None or an empty
                string.
        """
        root = get_default_root()
        command = "::msgcat::mclocale"
        return root.tk.eval(f'{command} {newlocale or ""}')

    @staticmethod
    def preferences() -> list[str]:
        """Returns an ordered list of the locales preferred by the user,
        based on the user's language specification. The list is ordered
        from most specific to the least preference. If the user has specified
        LANG=en_US_funky, this method would return {en_US_funky en_US en}.

        Returns:

            list[str, ...]:
                Locales preferred by the user.
        """
        root = get_default_root()
        command = "::msgcat::mcpreferences"
        items = root.tk.eval(command).split(" ")
        if len(items) > 0:
            return items[0:-1]
        else:
            return []

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
        command = "::msgcat::mcload"
        return int(root.tk.eval(f"{command} [list {msgs}]"))

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

            translated (str):
                The translated string.
        """
        root = get_default_root()
        command = "::msgcat::mcset"
        root.tk.eval('%s %s {%s} {%s}' % (command, locale, src, translated or ""))

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
        command = "::msgcat::mcmset"
        messages = " ".join(['{%s}' % x for x in args])
        out = f"{command} {locale} {{{messages}}}"
        return int(root.tk.eval(out))

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
        command = "::msgcat::mcmax"
        return int(root.tk.eval(f'{command} {" ".join(src)}'))


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
