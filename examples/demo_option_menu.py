if __name__ == '__main__':
    import ttkbootstrap as ttk

    root = ttk.Window(theme="dark", size=(200, 200))

    om = ttk.OptionMenu(
        root, value="Python", dropdown_button_icon="chevron-down",
        options=["Python", "Javascript", "Swift", "C#", "Go", "PHP", "Java"])
    om.pack(pady=20, padx=20, fill='x')

    om.on_changed(print)

    om = ttk.OptionMenu(
        root, value="Python",
        state="disabled",
        options=["Python", "Javascript", "Swift", "C#", "Go", "PHP", "Java"])
    om.pack(pady=20, padx=20, fill='x')

    om['show_dropdown_button'] = False



    root.mainloop()