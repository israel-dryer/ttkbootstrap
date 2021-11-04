from tkinter import ttk
from ttkbootstrap.constants import *
from ttkbootstrap.themes.standard import STANDARD_THEMES
from ttkbootstrap.themes.user import USER_THEMES
from ttkbootstrap.style.style_builder import StyleBuilderTTK, ThemeDefinition


class Style(ttk.Style):
    """A class for setting the application style.

    Sets the theme of the ``tkinter.Tk`` instance and supports all
    ttkbootstrap and ttk themes provided. This class is meant to be a
    drop-in replacement for ``ttk.Style`` and inherits all of it's
    methods and properties. Creating a ``Style`` object will
    instantiate the ``tkinter.Tk`` instance in the ``Style.master``
    property, and so it is not necessary to explicitly create an
    instance of ``tkinter.Tk``. For more details on the ``ttk.Style``
    class, see the python documentation_.

    .. code-block:: python

        # instantiate the style with default theme *flatly*
        style = Style()

        # instantiate the style with another theme
        style = Style(theme='superhero')

        # available themes
        for theme in style.theme_names():
            print(theme)

    .. _documentation: https://docs.python.org/3.9/library/tkinter.ttk.html#tkinter.ttk.Style
    """
    __instance = None

    def __init__(self, theme=DEFAULT_THEME, *args, **kwargs):
        """
        Parameters
        ----------
        theme : str
            the name of the theme to use at runtime; default='flatly'.

        *args : Any
            Other optional arguments

        **kwargs : Any
            Other optional keyword arguments
        """
        Style.__instance = self
        # this parameter has been replaced internally with py file
        if "themes_file" in kwargs:
            del kwargs["themes_file"]

        super().__init__(*args, **kwargs)
        self._styler = None
        self._theme_names = set(super().theme_names())
        self._theme_objects = {}  # prevents image garbage collection
        self._theme_definitions = {}
        self._load_themes()

        # load selected or default theme
        self.theme_use(themename=theme)

    @staticmethod
    def get_instance():
        return Style.__instance

    @staticmethod
    def get_builder():
        _style = Style.get_instance()
        _theme = _style.theme_use()
        return _style._theme_objects[_theme]

    @property
    def colors(self):
        """The theme colors"""
        theme = self.theme_use()
        if theme in list(self._theme_names):
            definition = self._theme_definitions.get(theme)
            if not definition:
                return [] #TODO refactor this
            else:
                return definition.colors
        else:
            return [] # TODO refactor this

    def _load_themes(self):
        """Load all ttkbootstrap defined themes"""
        # create a theme definition object for each theme, this will be
        # used to generate the theme in tkinter along with any assets
        # at run-time
        if USER_THEMES:
            STANDARD_THEMES.update(USER_THEMES)
        theme_settings = {"themes": STANDARD_THEMES}
        for name, definition in theme_settings["themes"].items():
            self.register_theme(
                ThemeDefinition(
                    name=name,
                    themetype=definition["type"],
                    font=definition.get("font") or DEFAULT_FONT,
                    colors=definition["colors"],
                )
            )

    def theme_names(self):
        """Return a list of all ttkbootstrap themes"""
        return list(self._theme_definitions.keys())

    def register_theme(self, definition):
        """Registers a theme definition for use by the ``Style`` class.

        This makes the definition and name available at run-time so
        that the assets and styles can be created.

        Parameters
        ----------
        definition : ThemeDefinition
            An instance of the ``ThemeDefinition`` class
        """
        self._theme_names.add(definition.name)
        self._theme_definitions[definition.name] = definition

    def theme_use(self, themename=None):
        """Changes the theme used in rendering the application widgets.

        If themename is None, returns the theme in use, otherwise, set
        the current theme to themename, refreshes all widgets and emits
        a ``<<ThemeChanged>>`` event.

        Only use this method if you are changing the theme *during*
        runtime. Otherwise, pass the theme name into the Style
        constructor to instantiate the style with a theme.

        Parameters
        ----------
        themename : str
            The name of the theme to apply when creating new widgets
        """
        self.theme = self._theme_definitions.get(themename)

        if not themename:
            return super().theme_use()

        if all([themename, themename not in self._theme_names]):
            print(f"{themename} is invalid.Try one of the following:")
            print(list(self._theme_names))
            return

        if themename in super().theme_names():
            # the theme has already been created in tkinter
            super().theme_use(themename)
            if not self.theme:
                return
            return

        # theme has not yet been created
        self._theme_objects[themename] = StyleBuilderTTK(self, self.theme)
        self._theme_objects[themename].styler_tk.style_tkinter_widgets()
        super().theme_use(themename)
        return

    def exists(self, style: str):
        """Return True if style exists else False"""
        return self.configure(style) is not None