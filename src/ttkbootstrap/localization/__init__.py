"""
    A partial wrapper on the tcl/tk msgcat (Tcl message catalog)

    The MessageCatalog provides a set of functions that can be used to 
    manage multi-lingual user interfaces. Text strings are defined in a 
    “message catalog” which is independent from the application, and 
    which can be edited or localized without modifying the application 
    source code. New languages or locales may be provided by adding a 
    new file to the message catalog.

    https://www.tcl.tk/man/tcl/TclCmd/msgcat.html    
"""
from pathlib import Path
from tkinter import _get_default_root as default_root

MSGS_PATH = (Path(__file__).parent / 'msgs').as_posix()


def initialize_localities():
    """Check if in a locality with custom messages. If so, load."""
    MessageCatalog.load(MSGS_PATH)

class MessageCatalog:

    @staticmethod
    def translate(src, *args):
        """Returns a translation of src according to the user's current 
        locale. If additional arguments past src are given, the format 
        command is used to substitute the additional arguments in the 
        translation of src. `msgcat_mc` will search the messages defined 
        in the current namespace for a translation of src; if none is 
        found, it will search in the parent of the current namespace, 
        and so on until it reaches the global namespace. If no translation 
        string exists, `msgcat_mcunknown` is called and the string 
        returned from `msgcat_mcunknown` is returned.

        The main function used to localize an application. Instead of 
        using an English string directly, an applicaton can pass the 
        English string through `msgcat_mc` and use the result. If an 
        application is written for a single language in this fashion, 
        then it is easy to add support for additional languages later 
        simply by defining new message catalog entries.

        Parameters:

            src (str):
                The string to be translated.

        Returns:

            str:
                The translated string.
        """
        root = default_root()
        command = '::msgcat::mc'
        return root.tk.eval(f'{command} "{src}"')

    @staticmethod
    def locale(newlocale=None):
        """"This function sets the locale to newlocale. If newlocale is 
        omitted, the current locale is returned, otherwise the current 
        locale is set to newlocale. The initial locale defaults to the 
        locale specified in the user's environment. See LOCALE AND 
        SUBLOCALE SPECIFICATION for a description of the locale string 
        format.

        Parameters:

            newlocale (str):
                The new locale code used to define the language for the 
                application.

        Returns:

            Union[str]:
                The current locale name if newlocale is None or an empty 
                string.
        """
        root = default_root()
        command = '::msgcat::mclocale'
        return root.tk.eval(f'{command} {newlocale or ""}')

    def preferences():
        """Returns an ordered list of the locales preferred by the user, 
        based on the user's language specification. The list is ordered 
        from most specific to least preference. If the user has specified 
        LANG=en_US_funky, this procedure would return 
        {en_US_funky en_US en}.

        Returns:

            List[str]:
                Locales preferred by the user.
        """
        root = default_root("preferences")
        command = '::msgcat::mcpreferences'
        items = root.tk.eval(command).split(' ')
        if len(items) > 0:
            return items[0:-1]
        else:
            return []

    def load(dirname):
        """Searches the specified directory for files that match the 
        language specifications returned by `msgcat_mcpreferences`. 
        Each file located is sourced. The file extension is .msg. The 
        number of message files which matched the specification and 
        were loaded is returned.

        Parameters:

            dirname (str):
                The directory path of the msg files.
        """
        root = default_root()
        command = '::msgcat::mcload'
        root.tk.eval(f'{command} {dirname}')

    def set(locale, src, translated=None):
        """Sets the translation for src to translated in the specified 
        locale. If translated is not specified, src is used for both. 
        The function returns translated.

        Parameters:

            local (str):
                The local code used when translating the src.

            src (str):
                The original language string.

            translated (str):
                The translated string.
        """
        root = default_root()
        command = '::msgcat::mcset'
        root.tk.eval(f'{command} {locale} {src} {translated or ""}')

    def set_many(locale, *args):
        """Sets the translation for multiple source strings in *args in 
        the specified locale and the current namespace. Must be an even
        number of args.

        Parameters:

            local (str):
                The local code used when translating the src.

            *args (str):
                A series of src, translated pairs.

        Returns:

            int:
                The number of translation sets.
        """
        root = default_root()
        command = '::msgcat::mcmset'
        return int(root.tk.eval(f'{command} {locale} {" ".join(args)}'))

    def max(*src):
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
        root = default_root()
        command = '::msgcat::mcmax'
        return int(root.tk.eval(f'{command} {" ".join(src)}'))


if __name__ == '__main__':

    initialize_localities()
    MessageCatalog.locale('zh_cn')
    result = MessageCatalog.translate('Skip Messages')
    print(result)