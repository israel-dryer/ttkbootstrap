from __future__ import annotations
from abc import ABC, abstractmethod
from tkinter.ttk import Style
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .theme import Theme


class StyleBuilderLegacy(ABC):

    def __init__(self, theme: "Theme"):
        self.theme = theme
        self.ttk = Style(theme.ttk.master)

    @abstractmethod
    def invoke(self, token: str, **extras):
        ...
