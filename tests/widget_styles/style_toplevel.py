import ttkbootstrap as ttk


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.App()

    ttk.Label(root, text="Root").pack(padx=10, pady=10)

    top = ttk.Toplevel(root)
    ttk.Label(top, text="Toplevel").pack(padx=10, pady=10)

    btn = ttk.Button(top, text="Change Theme", command=ttk.toggle_theme)
    btn.pack(padx=10, pady=10)

    root.after_idle(top.show)

    root.mainloop()