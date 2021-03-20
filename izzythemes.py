from tkinter import ttk
from themes import superflat


class Style(ttk.Style):
    def __init__(self):
        super().__init__()
        superflat.create_theme(self)
