import ttkbootstrap as ttk

if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.App()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)
    var = ttk.Variable()
    om = ttk.OptionMenu(root, var, ['dark', 'light'])
    om.pack(padx=10, pady=10, fill='x')

    for i, color in enumerate(['primary', 'secondary', 'success', 'info', 'warning', 'danger']):
        var = ttk.Variable()
        om = ttk.OptionMenu(root, var, ['primary', 'secondary', 'success', 'info', 'warning', 'danger'], accent=color)
        om.pack(padx=10, pady=10, fill='x')

    root.mainloop()


