import json
from tkinter import ttk
from .theme_engine import StylerTTK
from .theme_engine import ThemeSettings
from pathlib import Path


class BootStyle(ttk.Style):
    def __init__(self):
        super().__init__()
        self.themes = {}
        self.load_izzy_themes()
        self.settings = None

    def load_izzy_themes(self):
        """Load all izzy defined themes"""
        with open(Path('src/ttkbootstrap/themes.json'), encoding='utf-8') as f:
            settings = json.load(f)
        for theme in settings['themes']:
            settings = ThemeSettings(theme['name'], theme['type'], theme['font'], **theme['colors'])
            self.themes[settings.name] = StylerTTK(self, settings)
        self.apply_theme('darkly')

    def apply_theme(self, theme_name=None):
        """Apply a new theme"""
        if theme_name is None:
            return
        current_theme = self.themes.get(theme_name)
        current_theme.styler_tk.apply_style()
        self.theme_use(theme_name)
        self.settings = current_theme.settings

    def theme_names(self):
        """Return a sorted list of available themes"""
        return sorted(super().theme_names())
