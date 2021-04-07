"""
    Author: Israel Dryer
    Modified: 2021-04-07
"""
import tkinter
from tkinter import ttk
from ttkbootstrap import Style


class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Accordian Widget')
        self.style = Style('flatly')

        # accordian widget 1
        accordian1 = AccordionWidget(self, header_text='Option Group 1', style='primary.TFrame')
        accordian1.pack(fill='x')
        contents1 = ttk.Frame(accordian1)
        for x in range(5):
            b = ttk.Checkbutton(contents1, text=f'Option {x + 1}')
            b.pack(side='top', fill='x')
            b.invoke()

        # accordian widget 2
        accordian2 = AccordionWidget(self, header_text='Option Group 2', style='danger.TFrame')
        accordian2.pack(fill='x')
        contents2 = ttk.Frame(accordian2)
        for x in range(5):
            b = ttk.Checkbutton(contents2, text=f'Option {x + 1}')
            b.pack(side='top', fill='x')
            b.invoke()
        entry = ttk.Entry(contents2, style='danger.TEntry')
        entry.pack(fill='x', pady=(10, 5))
        entry.insert('end', 'sample text')
        ttk.Button(contents2, text='Submit', style='danger.TButton').pack(fill='x', pady=5)

        # accordian widget 3
        accordian3 = AccordionWidget(self, header_text='Option Group 3', style='success.TFrame')
        accordian3.pack(fill='x')
        contents3 = ttk.Frame(accordian3)
        for x in range(5):
            b = ttk.Checkbutton(contents3, text=f'Option {x + 1}')
            b.pack(side='top', fill='x')
            b.invoke()

        accordian1.add(contents1)
        accordian1.header_btn.invoke()  # collapse accordian 1

        accordian2.add(contents2)
        accordian3.add(contents3)


class AccordionWidget(ttk.Frame):
    """
    An accordian widget that opens and closes with a button click. Only one content container will be visible at a time,
    so do not add more than one. The last will override any previous.
    """

    def __init__(self, *args, header_text='', contents_padding=(10, 10), style='primary.TFrame', **kwargs):
        super().__init__(style=style, *args, **kwargs)
        self.contents_padding = contents_padding
        color = self.cget('style').split('.')[0]

        self.images = [tkinter.PhotoImage(name='open', file='assets/icons8_double_up_24px.png'),
                       tkinter.PhotoImage(name='closed', file='assets/icons8_double_right_24px.png')]

        # header configuration
        self.container = ttk.Frame(self, style=f'{color}.TFrame')
        header_frm = ttk.Frame(self, style=f'{color}.TFrame')
        header_frm.pack(fill='x')
        header_txt = ttk.Label(header_frm, text=header_text, style=f'{color}.TButton', font=('Helvetica 11 bold'))
        header_txt.pack(side='left', fill='x', pady=10, padx=10)
        self.header_btn = ttk.Button(header_frm, image='open', command=self.toggle_accordion, style=f'{color}.TButton')
        self.header_btn.pack(side='right')

        # container setup
        self.contents = tkinter.Canvas(self, border=0, highlightthickness=0)
        self.contents.pack(fill='x')

    def add(self, contents):
        """Add contents to the canvas. Will overwrite existing contents"""
        self.contents.create_window(self.contents_padding, window=contents, anchor='nw')
        self.update()
        self.contents.configure(height=contents.winfo_height() + self.contents_padding[0] * 2)

    def toggle_accordion(self):
        """Collapse and expand accordian widget"""
        if self.contents.winfo_viewable():
            self._contents_info = self.contents.info()
            self.contents.pack_forget()
            self.header_btn.configure(image='closed')
        else:
            self.contents.pack(**self._contents_info)
            self.header_btn.configure(image='open')


if __name__ == '__main__':
    Application().mainloop()
