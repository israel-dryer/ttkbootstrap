from tkinter import Canvas, Scrollbar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class ScrolledFrame(ttk.Canvas):

    def __init__(self, master):
        super().__init__(master)
        self.frame = ttk.Frame(self, bootstyle=SUCCESS)
        self.vbar = ttk.Scrollbar(self, orient=VERTICAL)
        self.create_window(0, 0, anchor=NW, window=self.frame)
        self.create_window(0, 0, anchor=NE, window=self.vbar)


if __name__ == '__main__':

    app = ttk.Window()

    sf = ScrolledFrame(app)
    sf.pack(fill=BOTH, expand=YES)

    for x in range(20):
        ttk.Button(sf.frame, text="Push").pack()

    app.mainloop()
