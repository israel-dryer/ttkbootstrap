import tkinter
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap import Style


class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Text Reader')
        self.style = Style()
        self.reader = Reader(self)
        self.reader.pack(fill='both', expand='yes')


class Reader(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=10)
        self.filename = tkinter.StringVar()

        # scrolled text with custom highlight colors
        self.text_area = ScrolledText(self, highlightcolor=self.master.style.colors.primary,
                                      highlightbackground=self.master.style.colors.border, highlightthickness=1)
        self.text_area.pack(fill='both')

        # insert default text in text area
        self.text_area.insert('end', 'Click the browse button to open a new text file.')

        # filepath
        ttk.Entry(self, textvariable=self.filename).pack(side='left', fill='x', expand='yes', padx=(0, 5), pady=10)

        # browse button
        ttk.Button(self, text='Browse', command=self.open_file).pack(side='right', fill='x', padx=(5, 0), pady=10)

    def open_file(self):
        path = askopenfilename()
        if not path:
            return

        with open(path, encoding='utf-8') as f:
            self.text_area.delete('1.0', 'end')
            self.text_area.insert('end', f.read())
            self.filename.set(path)


if __name__ == '__main__':
    Application().mainloop()
