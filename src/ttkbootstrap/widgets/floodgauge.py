import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from uuid import uuid4


class Floodgauge(ttk.Progressbar):

    def __init__(self, parent, **kw):
        """
            HACK - need to create a custom style to manipulate to text properties because I don't know how to add new
            options to the ttk widget constructor that tcl will accept Progressbar + Label options
        """
        _style = kw.get('style') or 'TFloodgauge'
        _id = uuid4()
        _orient = kw.get('orient').title() or 'Horizontal'
        self._widgetstyle = f'{_id}.{_orient}.{_style}'
        parent.tk.call("ttk::style", "configure", self._widgetstyle, '-%s' % None, None, None)

        kwargs = {k: v for k, v in kw.items() if k not in ['text']}

        self.textvariable = kw.get('textvariable') or tk.StringVar(value=kw.get('text'))
        self.textvariable.trace_add('write', self._textvariable_write)
        self.variable = kw.get('variable') or tk.IntVar(value=kw.get('value') or 0)

        super().__init__(parent, class_='Floodgauge', style=self._widgetstyle, variable=self.variable, **kwargs)

    @property
    def text(self):
        return self.textvariable.get()

    @text.setter
    def text(self, value):
        self.textvariable.set(value)

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, value):
        self.variable.set(value)

    def _textvariable_write(self, *args):
        """
        Update the label text when there is a `write` action on the textvariable
        """
        self.tk.call("ttk::style", "configure", self._widgetstyle, '-%s' % 'text', self.textvariable.get(), None)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x400')
    s = Style()
    p = Floodgauge(root, value=55, text='55', orient='vertical')


    def auto(progress):
        p.text = f'Memory Usage\n{p.value}%'
        p.step(1)
        p.after(50, auto, p)


    p.pack(fill='both', padx=20, pady=20, expand='yes')
    auto(p)
    root.mainloop()
