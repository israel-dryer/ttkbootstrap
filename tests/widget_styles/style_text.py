import ttkbootstrap as ttk


DARK = 'superhero'
LIGHT = 'flatly'




if __name__ == '__main__':
    # create visual widget style tests
    window = ttk.App(theme='darkly')

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)
    text = ttk.Text(window, font='helvetica 24 bold')
    text.pack(padx=10, pady=10)
    text.insert('end', 'Hello, this is my text.')
    window.mainloop()