import ttkbootstrap as ttk


root = ttk.Window()
root.geometry('200x400')
style = ttk.Style()

sb = ttk.Scrollbar(root, orient='vertical')
sb.pack(fill='y', expand=True, padx=20, pady=20, side='left')
sb.set(0, 1)

sb = ttk.Scrollbar(root, orient='vertical', bootstyle='danger-rounded')
sb.pack(fill='y', expand=True, padx=20, pady=20, side='left')
sb.set(0, 1)

sb = ttk.Scrollbar(root, orient='horizontal', style_options={"show_arrows": False})
sb.pack(fill='x', expand=True, padx=20, pady=20)
sb.set(0, 1)

sb = ttk.Scrollbar(root, orient='horizontal', bootstyle='danger-rounded')
sb.pack(fill='x', expand=True, padx=20, pady=20)
sb.set(0, 1)

sb = ttk.Scrollbar(root, orient='horizontal', bootstyle='danger-rounded', style_options={"show_arrows": False})
sb.pack(fill='x', expand=True, padx=20, pady=20)
sb.set(0, 1)

def change_theme():
    if style.theme_use() == 'dark':
        style.theme_use('light')
    else:
        style.theme_use('dark')

ttk.Button(root, text="Change Theme", command=change_theme).pack(padx=20, pady=20)

root.mainloop()


