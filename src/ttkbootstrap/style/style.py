from tkinter import ttk
from typing import Callable
from ttkbootstrap.constants import *
from ttkbootstrap.themes.standard import STANDARD_THEMES
from ttkbootstrap.themes.user import USER_THEMES
from ttkbootstrap.style.style_builder import StyleBuilderTTK, ThemeDefinition
from ttkbootstrap.style.publisher import Publisher, Channel
from ttkbootstrap.style import utility as util


class BootStyle(ttk.Style):
    """A class for setting the application style.

    Sets the theme of the `tkinter.Tk` instance and supports all
    ttkbootstrap and ttk themes provided. This class is meant to be a
    drop-in replacement for `ttk.Style` and inherits all of it's
    methods and properties.For more details on the `ttk.Style` class, 
    see the python documentation.
    """
    instance = None

    def __init__(self, theme=DEFAULT_THEME, **kwargs):
        """
        Parameters
        ----------
        theme : str
            The name of the theme to use at runtime; default="flatly".
        """
        print('creating a new instance')
        self._theme_objects = {}
        self._theme_definitions = {}
        self._style_registry = set() # all styles used
        self._theme_styles = {} # styles used in theme
        self._theme_names = set()
        self._load_themes()
        super().__init__(**kwargs)
        BootStyle.instance = self
        self.theme_use(theme)

    @staticmethod
    def get_builder():
        style: BootStyle = Style()
        theme_name = style.theme.name
        return style._theme_objects[theme_name]

    @staticmethod
    def get_builder_tk():
        builder = BootStyle.get_builder()
        return builder.builder_tk

    @property
    def colors(self):
        """The theme colors"""
        theme = self.theme.name
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

    def register_ttkstyle(self, ttkstyle):
        """Register that a style has been created"""
        self._style_registry.add(ttkstyle)
        theme = self.theme.name
        self._theme_styles[theme].add(ttkstyle)

    def register_theme(self, definition):
        """Registers a theme definition for use by the ``Style`` class.

        This makes the definition and name available at run-time so
        that the assets and styles can be created.

        Parameters
        ----------
        definition : ThemeDefinition
            An instance of the ``ThemeDefinition`` class
        """
        theme = definition.name
        self._theme_names.add(theme)
        self._theme_definitions[theme] = definition
        self._theme_styles[theme] = set()

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
        if not themename:
            return super().theme_use()

        if all([themename, themename not in self._theme_names]):
            print(f"{themename} is invalid.Try one of the following:")
            print(list(self._theme_names))
            return
        else:
            self.theme = self._theme_definitions.get(themename)

        existing_themes = super().theme_names()
        if themename in existing_themes:
            # the theme has already been created in tkinter
            super().theme_use(themename)
            # Publisher.publish_message(Channel.TTK)
            self.create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)
            if not self.theme:
                return
            return

        # theme has not yet been created
        self._theme_objects[themename] = StyleBuilderTTK(self, self.theme)
        self.create_ttk_styles_on_theme_change()
        #Publisher.publish_message(Channel.TTK)
        Publisher.publish_message(Channel.STD)        
        return

    def exists(self, ttkstyle: str):
        """Return True if style exists else False"""
        theme_styles = self._theme_styles.get(self.theme.name)
        exists_in_theme = ttkstyle in theme_styles
        exists_in_registry = ttkstyle in self._style_registry
        return exists_in_theme and exists_in_registry

    def create_ttk_styles_on_theme_change(self):
        """Create existing styles when the theme changes"""
        for ttkstyle in self._style_registry:
            if not self.exists(ttkstyle):
                color = util.ttkstyle_widget_color(ttkstyle)
                method_name = util.ttkstyle_method_name(string=ttkstyle)
                builder: StyleBuilderTTK = self.get_builder()
                method: Callable = builder.name_to_method(method_name)
                method(builder, color)

def Style(theme=DEFAULT_THEME, **kwargs):
    """Returns a singleton instance of the `BootStyle` class.

    Examples
    --------
    Return an instance of the BootStyle class
    >>> style = Style()

    Return instance with defined theme
    >>> style = Style(theme='superhero')
    """
    if BootStyle.instance is None:
        BootStyle(theme, **kwargs)
        return BootStyle.instance
    else:
        if theme == DEFAULT_THEME:
            return BootStyle.instance
        else:
            BootStyle.instance.theme_use(theme)
            return BootStyle.instance