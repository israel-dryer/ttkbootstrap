from tkinter.ttk import Style

from ttkbootstrap.exceptions import ThemeAlreadyExistsError, ThemeNotFoundError
from ttkbootstrap.style.theme import Theme, get_standard_themes
from ttkbootstrap.logger import logger


class ThemeManager:

    def __init__(self, theme=None, master=None):
        self.ttk = Style(master=master)
        self._themes = {}
        self._active_theme = None

        # initialize themes
        self.load_themes(get_standard_themes())
        self.use_theme(theme)

    @property
    def themes(self):
        return self._themes

    @property
    def active_theme(self):
        return self._active_theme

    @property
    def colors(self):
        return self.active_theme.colors

    def configure(self, style, query_opt=None, **kw):
        return self.ttk.configure(style, query_opt=query_opt, **kw)

    def theme_names(self):
        return self.themes.keys()

    def register_theme(self, theme: Theme):
        theme_name = theme.name
        if theme_name in self.ttk.theme_names():
            logger.warning('ThemeManager', f'Skipping theme registration: {theme_name} already exists')
            return
        self.themes[theme_name] = theme

    def use_theme(self, theme_name):
        if not theme_name:
            return self.ttk.theme_use()
        # check if theme_name is valid
        if theme_name not in self.themes.keys():
            raise ThemeNotFoundError(theme_name)

        theme = self.themes.get(theme_name)
        self._active_theme = theme

        # create a theme if not already existing
        existing = self.ttk.theme_names()
        logger.debug('ThemeManager', f'Existing themes: {existing}')
        if theme_name not in self.ttk.theme_names():
            logger.info('ThemeManager', f'Creating theme: {theme_name}')
            self.ttk.theme_create(theme_name, 'clam')

        # initialize the theme if not already activated
        if not theme.activated:
            theme.initialize()

        # apply the theme and generate <<ThemeChanged>>
        logger.info('ThemeManager', f'Applying theme: {theme_name}')
        self.ttk.theme_use(theme_name)

        return theme_name

    def create_theme(self, theme_name, parent, settings):
        if parent not in self.themes:
            raise ThemeNotFoundError(parent)
        if theme_name in self.themes:
            raise ThemeAlreadyExistsError(theme_name)

        logger.info('ThemeManager', f'Creating theme: {theme_name}')
        self.ttk.theme_create(theme_name, parent, settings)

        parent_theme = self.themes[parent]
        theme = Theme(name=theme_name, mode=parent_theme.mode, **parent_theme.colors())
        self.themes[theme_name] = theme

    def load_themes(self, themes):
        for theme in themes:
            self.register_theme(theme)


# --- Singleton accessor ---
_theme_manager_instance: ThemeManager | None = None


def get_theme_manager(theme="cosmo", master=None) -> ThemeManager:
    global _theme_manager_instance
    if _theme_manager_instance is None:
        _theme_manager_instance = ThemeManager(theme, master)
    return _theme_manager_instance
