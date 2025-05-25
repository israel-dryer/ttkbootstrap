from abc import ABC, abstractmethod
from tkinter.ttk import Style
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ttkbootstrap.style.theme import Theme


class StyleBuilder(ABC):

    def __init__(self, theme):
        self.theme: Theme = theme
        self.ttk = Style(theme.ttk.master)

    @abstractmethod
    def invoke(self, *args):
        pass
