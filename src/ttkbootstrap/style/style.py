from tkinter.ttk import Style as ttkStyle


class Style(ttkStyle):

    def __init__(self, master=None):
        super().__init__(master)

    def style_exists(self, style: str):
        return bool(self.configure(style))
