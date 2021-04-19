from ttkbootstrap import Style
import tkinter as tk
from pathlib import Path
from tkinter.scrolledtext import ScrolledText

class Demo(Style):
    """
    An application class for demonstrating styles
    """

    def __init__(self):
        super().__init__()
        self.theme_use('journal')
        self.root = self.master
        self.root.geometry('500x695')
        self.root.title('TTK Bootstrap')
        self.theme_name = tk.StringVar(name='themename', value=self.theme_use())
        self.setup()
        self.root.mainloop()

    def setup(self):

        # scrollbar
        tk.Scrollbar(self.root, orient='vertical').pack(side='right', fill='y')

        # header
        header = tk.Frame(self.root)
        header.pack(fill='x', padx=10, pady=(10, 0))

        ## title
        tk.Label(header, font='Helvetica 30', textvariable='themename').pack(side='left', fill='y')

        ## menubutton
        mb = tk.Menubutton(header, text='Select a theme to preview')
        mb.pack(side='right')
        mb.menu = tk.Menu(mb)
        mb['menu'] = mb.menu
        for t in self.theme_names():
            mb.menu.add_command(label=t, command=lambda t=t: print(t))

        # labelframe container
        lf = tk.LabelFrame(self.root, text='Styled widgets')
        lf.pack(fill='both', padx=10, pady=10, ipadx=5, ipady=5)


        ## label
        tk.Label(lf, text='This is a label', anchor='w').pack(fill='x', padx=5, pady=5)

        # entry - button - spinner frame
        frame1 = tk.Frame(lf)
        frame1.pack(fill='both')

        ## Entry
        ent = tk.Entry(frame1)
        ent.insert('end', 'An entry field')
        ent.pack(side='left', fill='both', expand='yes', padx=10, pady=10)

        ## Spinner
        spin = tk.Spinbox(frame1, values=['Spinner option 1', 'Spinner option 2'])
        spin.pack(side='left', fill='both', expand='yes', padx=10, pady=10)

        ## Button
        tk.Button(lf, text='Solid Button').pack(fill='both', padx=10, pady=10)

        # radio - checkbutton frame
        frame2 = tk.Frame(lf)
        frame2.pack(fill='both', padx=10, pady=10)

        ## Radio buttons
        tk.Radiobutton(frame2, text='Radio one', value=1).pack(side='left', fill='x', padx=5, pady=5, expand='yes')
        tk.Radiobutton(frame2, text='Radio two', value=2).pack(side='left', fill='x', padx=5, pady=5, expand='yes')

        ## Checkbuttons
        tk.Checkbutton(frame2, text='Option one').pack(side='left', fill='x', padx=5, pady=5, expand='yes')
        tk.Checkbutton(frame2, text='Option two').pack(side='left', fill='x', padx=5, pady=5, expand='yes')

        # Scale
        frame3 = tk.Frame(lf)
        frame3.pack(fill='both', padx=10, pady=10)
        scale = tk.Scale(frame3, from_=1, to=100, orient='horizontal', variable='scale')
        scale.pack(side='left', fill='x', expand='yes')
        scale.setvar('scale', 75)
        tk.Label(frame3, textvariable='scale', width=3).pack(side='left', fill='x')

        # # Canvas
        # tk.Canvas(lf, height=50).pack(fill='both', padx=10, pady=10)

        # text and listbox
        frame4 = tk.Frame(lf)
        frame4.pack(fill='both')

        # text
        text = tk.Text(frame4, height=5, width=30)
        text.pack(side='left', fill='both', padx=10, pady=10)
        text.insert('end', Path(__file__).read_text())

        # #Listbox
        lb = tk.Listbox(frame4, height=10)
        lb.pack(side='left', padx=10, pady=10, fill='both', expand='yes')
        for x in ['one', 'two', 'three', 'four']:
            lb.insert('end', x)

        st = ScrolledText()
        st.insert('end', Path(__file__).read_text())
        st.pack(padx=10, pady=10)





if __name__ == '__main__':
    Demo()
    #
    # slider = tk.Scale(from_=0, to=100, borderwidth=0, activebackground='red', sliderrelief='flat', orient='horizontal')
    # slider.pack(fill='x', padx=10, pady=10)
    # slider.mainloop()
