import tkinter as tk
from tkinter import ttk

app = tk.Tk()
app.geometry('500x500')
style = ttk.Style()
#style.theme_use('clam')

class Scrolledframe(ttk.Frame):

    def __init__(self, master=None, **kwargs):
        container = ttk.Frame(master=master)
        super().__init__(master=container, **kwargs)
        self.place(rely=0.0, relwidth=1.0)
        self.container = container
        self.container.bind("<Configure>", lambda _: self.yview())
        self.vscroll = ttk.Scrollbar(self.container, command=self.yview)
        self.vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.winsys = self.tk.call('tk', 'windowingsystem')
        self.autohide_scrollbar()
        
    def yview(self, *args):
        if not args:
            first, _ = self.vscroll.get()
            self.yview_moveto(fraction=first)
        elif args[0] == 'moveto':
            self.yview_moveto(fraction=float(args[1]))
        elif args[0] == 'scroll':
            self.yview_scroll(number=int(args[1]), what=args[2])
        else:
            return

    def yview_moveto(self, fraction: float):
        base, thumb = self._position()
        if fraction < 0:
            first = 0.0
        elif (fraction + thumb) > 1:
            first = 1 - thumb
        else:
            first = fraction
        self.vscroll.set(first, first + thumb)
        self.place(rely=-first*base)

    def yview_scroll(self, number: int, what: str):
        first, _ = self.vscroll.get()
        fraction = (number/100) + first
        self.yview_moveto(fraction)

    def _position(self):
        outer = self.container.winfo_height()
        inner = max([self.winfo_height(), outer])
        base = inner / outer
        if inner == outer:
            thumb = 1.0
        else:
            thumb = outer / inner
        return base, thumb

    def hide_scrollbars(self, *_):
        """Hide the scrollbars."""
        try:
            self.vscroll.lower(self)
        except:
            pass

    def show_scrollbars(self, *_):
        """Show the scrollbars."""
        try:
            self.vscroll.lift(self)
            self._enable_scrolling()
        except:
            pass

    def autohide_scrollbar(self, *_):
        """Show the scrollbars when the mouse enters the widget frame,
        and hide when it leaves the frame."""
        self.container.bind("<Enter>", self.show_scrollbars)
        self.container.bind("<Leave>", self.hide_scrollbars)

    def _on_mousewheel(self, event):
        if self.winsys.lower() == 'win32':
            delta = -int(event.delta / 120)
        elif self.winsys.lower() == 'aqua':
            delta = -event.delta
        elif event.num == 4:
            delta = -4
        elif event.num == 5:
            delta = 4
        self.yview_scroll(delta, tk.UNITS)

    def _enable_scrolling(self, *_):
        """Enable mousewheel scrolling on the frame and all of its
        children."""
        children = self.winfo_children()
        for widget in [self, *children]:
            bindings = widget.bind()
            if self.winsys.lower() == 'x11':
                if '<Button-4>' in bindings or '<Button-5>' in bindings:
                    continue
                else:
                    widget.bind("<Button-4>", self._on_mousewheel, "+")
                    widget.bind("<Button-5>", self._on_mousewheel, "+")
            else:
                if '<MouseWheel>' not in bindings:
                    widget.bind("<MouseWheel>", self._on_mousewheel, "+")

    def _disable_scrolling(self, *_):
        """Disabled mousewheel scrolling on the frame and all of its
        children."""
        children = self.winfo_children()
        for widget in [self, *children]:
            if self.winsys.lower() == 'x11':
                widget.unbind("<Button-4>")
                widget.unbind("<Button-5>")
            else:
                widget.unbind("<MouseWheel>")


if __name__ == '__main__':

    sf = Scrolledframe()
    sf.container.pack(fill=tk.BOTH, expand=tk.YES)

    for x in range(25):
        btn = ttk.Button(sf, text=f'Button {x+1}')
        btn.pack(side=tk.BOTTOM, fill=tk.X)

    app.mainloop()