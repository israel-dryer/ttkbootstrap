from tkinter import Canvas, Pack, Grid, Place
from tkinter.ttk import Frame, Scrollbar


class ScrolledFrame(Frame):
    def __init__(self, master=None, **kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
        self.vbar.pack(side='right', fill='y')
        self.canvas = Canvas(self.frame, yscrollcommand=self.vbar.set, borderwidth=0, relief='flat',
                             highlightthickness=0, height=400, width=300)
        super().__init__(self.canvas, **kw)
        self.canvas.pack(side='left', fill='both')
        self.vbar.configure(command=self.canvas.yview)
        self.canvas.create_window((4, 4), window=self, anchor='nw')

        self.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

        frame_meths = vars(Frame).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(frame_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
