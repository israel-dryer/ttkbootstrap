"""
    Author: Israel Dryer
    Modified: 2021-10-24
"""
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap import Style


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Text Reader')
        self.style = Style()
        self.reader = Reader(self)
        self.reader.pack(fill=tk.BOTH, expand=tk.YES)


class Reader(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=10)
        self.filename = tk.StringVar()

        # scrolled text with custom highlight colors
        self.text_area = ScrolledText(
            master=self,
            highlightcolor=self.master.style.colors.primary,
            highlightbackground=self.master.style.colors.border,
            highlightthickness=1
        )
        self.text_area.pack(fill=tk.BOTH)

        # insert default text in text area
        self.text_area.insert(
            tk.END, 'Click the browse button to open a new text file.')

        # filepath
        ttk.Entry(
            master=self,
            textvariable=self.filename
        ).pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=tk.YES,
            padx=(0, 5),
            pady=10
        )

        # browse button
        ttk.Button(
            master=self,
            text='Browse',
            command=self.open_file
        ).pack(
            side=tk.RIGHT,
            fill=tk.X,
            padx=(5, 0),
            pady=10
        )

    def open_file(self):
        path = askopenfilename()
        if not path:
            return

        with open(path, encoding='utf-8') as f:
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, f.read())
            self.filename.set(path)


if __name__ == '__main__':
    Application().mainloop()
