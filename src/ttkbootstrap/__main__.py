"""Interactive demo showcasing ttkbootstrap widgets"""
import ttkbootstrap as ttk

def setup_demo(app: ttk.App, theme: str):

    # variables
    gc = []
    curr_theme = ttk.StringVar(value=theme)
    on_value = ttk.BooleanVar(value=True)
    off_value = ttk.BooleanVar(value=False)

    bag = ttk.Frame(app, padding=8)

    # configure grid layout
    for i in range(4):
        bag.columnconfigure(i, weight=1, minsize=200)

    def change_theme(*_):
        app.theme_use(curr_theme.get())

    # header
    ttk.Label(bag, textvariable=curr_theme, font='-size 20 -weight bold').grid(row=0, column=0, columnspan=2, sticky='w')
    cbo = ttk.Combobox(bag, values=app.theme_names(), textvariable=curr_theme, state='readonly').grid(row=0, column=3, sticky='e')
    cbo.bind('<<ComboboxSelected>>', change_theme)

    # semantic colors
    semantic_colors = ('neutral', 'primary', 'secondary', 'success', 'info', 'warning', 'danger')
    color_frm = ttk.Labelframe(bag, text='Semantic accents', padding=8).grid(row=1, column=0, columnspan=4, sticky='nsew', pady=4)
    for color in semantic_colors:
        ttk.Label(color_frm, text=color, anchor='center', bootstyle=f'@{color}', padding=8).pack(side='left', fill='x', expand=True, padx=2, pady=4)

    # Button
    button_frm = ttk.Labelframe(bag, text='Button', padding=8).grid(row=2, column=0, sticky='nsew', pady=4)
    ttk.Button(button_frm, text='Default').pack(pady=2, fill='x')
    ttk.Button(button_frm, text='Outline', bootstyle='outline').pack(pady=2, fill='x')
    ttk.Button(button_frm, text='Ghost', bootstyle='ghost').pack(pady=2, fill='x')

    # Menubutton
    mb_frm = ttk.Labelframe(bag, text='Menubutton', padding=8).grid(row=2, column=1, sticky='nsew', pady=4, padx=8)
    ttk.Menubutton(mb_frm, text='Default').pack(pady=2, fill='x')
    ttk.Menubutton(mb_frm, text='Outline', bootstyle='outline').pack(pady=2, fill='x')
    ttk.Menubutton(mb_frm, text='Ghost', bootstyle='ghost').pack(pady=2, fill='x')

    # Toolbutton
    tb_frm = ttk.Labelframe(bag, text='Toolbutton', padding=8).grid(row=2, column=2, sticky='nsew', pady=4, padx=(0, 8))
    ttk.Checkbutton(tb_frm, text='Default', bootstyle='toolbutton').pack(pady=2, fill='x').invoke()
    ttk.Checkbutton(tb_frm, text='Outline', bootstyle='outline toolbutton').pack(pady=2, fill='x').invoke()
    ttk.Checkbutton(tb_frm, text='Ghost', bootstyle='ghost toolbutton').pack(pady=2, fill='x').invoke()

    # Meter
    meter_frm = ttk.Labelframe(bag, text='Meter', padding=8).grid(row=2, column=3, sticky='nsew', pady=4)
    ttk.Meter(
        meter_frm,
        meter_size=100,
        padding=0,
        amount_used=65,
        meter_type="semi",
        interactive=True,
        stripe_thickness=25,
        amount_total=100
    ).pack(fill='both')

    nb = ttk.Notebook(bag, padding=8).grid(row=4, column=0, sticky='nsew', pady=4, columnspan=2)
    inner = ttk.Frame(nb, padding=8)
    nb.add(inner, text='Tab 1')
    nb.add(ttk.Frame(nb), text='Tab 2')
    nb.add(ttk.Frame(nb), text='Tab 3')

    # Checkbutton
    check_frm = ttk.Labelframe(inner, text='Checkbutton', padding=8).pack(side='left', fill='both', expand=True)
    ttk.Checkbutton(check_frm, text='Unselected', variable=off_value).pack(fill='x', pady=2)
    ttk.Checkbutton(check_frm, text='Selected', variable=on_value).pack(fill='x', pady=2)
    ttk.Checkbutton(check_frm, text='Indeterminate').pack(fill='x', pady=2)
    ttk.Checkbutton(check_frm, text='Disabled', state='disabled').pack(fill='x', pady=2)

    # Radiobutton
    radio_frm = ttk.Labelframe(inner, text='Radiobutton', padding=8).pack(side='left', fill='both', padx=8, expand=True)
    ttk.Radiobutton(radio_frm, text='Unselected', variable=off_value).pack(fill='x', pady=2)
    ttk.Radiobutton(radio_frm, text='Selected', value=1, variable=on_value).pack(fill='x', pady=2)
    ttk.Radiobutton(radio_frm, text='Disabled', value=1, variable=on_value, state='disabled').pack(fill='x', pady=2)

    # Toggle
    toggle_frm = ttk.Labelframe(inner, text='Toggle', padding=8).pack(side='left', fill='both', expand=True)
    ttk.Checkbutton(toggle_frm, text='Off', variable=off_value, bootstyle='toggle').pack(fill='x', pady=2)
    ttk.Checkbutton(toggle_frm, text='Round (on)', variable=on_value, bootstyle='toggle').pack(fill='x', pady=2)
    ttk.Checkbutton(toggle_frm, text='Square (on)', variable=on_value, bootstyle='square toggle').pack(fill='x', pady=2)
    ttk.Checkbutton(toggle_frm, text='Disabled', state='disabled', bootstyle='toggle').pack(fill='x', pady=2)

    # Inputs
    input_frm = ttk.Labelframe(bag, text='Inputs', padding=8).grid(row=3, column=2, rowspan=2, sticky='nsew', pady=4, padx=(0, 8))
    ttk.Entry(input_frm).pack(pady=2, fill='x').insert(0, 'Entry')
    ttk.Entry(input_frm, show='•').pack(pady=2, fill='x').insert(0, 'supertopsecret')
    ttk.Spinbox(input_frm, values=app.theme_names()).pack(pady=2, fill='x').insert(0, curr_theme.get())
    ttk.DateEntry(input_frm).pack(pady=2, fill='x')
    ttk.Combobox(input_frm, values=app.theme_names()).pack(pady=2, fill='x').current(0)
    ttk.Text(input_frm, width=20, height=5).pack(pady=2, fill='both', expand=True).insert('end', 'This is a multiline text entry')

    # Data table
    table_frm = ttk.Labelframe(bag, text='Tableview', padding=8).grid(row=3, column=0, columnspan=2, pady=4, padx=(0, 8))
    ttk.Tableview(
        table_frm,
        bootstyle='primary',
        coldata=['Name', 'Occupation'],
        rowdata=[
            ('Israel Dryer', 'Software Developer'),
            ('Alan Turing', 'AI Researcher'),
            ('Grace Hopper', 'Software Engineer'),
            ('Tim Berners-Lee', 'Web Architect'),
            ('Linus Torvalds', 'Open Source Project Lead'),
            ('Barbara Liskov', 'Software Architecture Researcher')
        ],
        paginated=True,
        height=5,
    ).pack().sort_column_data(None, 0, 1)

    # Other
    other_frm = ttk.Labelframe(bag, text='Other', padding=8).grid(row=3, column=3, rowspan=2, pady=4, sticky='nsew')

    ttk.Label(other_frm, text='Progress').pack(fill='x', pady=2)
    ttk.Progressbar(other_frm, value=25).pack(fill='x', pady=4)
    ttk.Progressbar(other_frm, value=50, bootstyle='thin').pack(fill='x', pady=4)
    ttk.Progressbar(other_frm, value=75, bootstyle='striped').pack(fill='x', pady=4)

    ttk.Label(other_frm, text='Scale').pack(fill='x', pady=(12, 2))
    ttk.Scale(other_frm, value=25, from_=0, to=100).pack(fill='x', pady=4)
    ttk.LabeledScale(other_frm, value=50, from_=0, to=100).pack(fill='x', pady=4)

    ttk.Label(other_frm, text='Separator').pack(fill='x', pady=(12, 2))
    ttk.Separator(other_frm).pack(fill='x', pady=4)
    ttk.Separator(other_frm, bootstyle='primary').pack(fill='x', pady=4)
    ttk.Separator(other_frm, bootstyle='success').pack(fill='x', pady=4)

    ttk.Label(other_frm, text='Scrollbar').pack(fill='x', pady=(12, 2))
    ttk.Scrollbar(other_frm, orient='horizontal', bootstyle='round').pack(fill='x', pady=4)
    ttk.Scrollbar(other_frm, orient='horizontal').pack(fill='x', pady=4)

    # return vars to avoid losing in garbage collection
    gc.extend([curr_theme, on_value, off_value])
    return bag, gc


if __name__ == "__main__":
    app = ttk.App("ttkbootstrap widget demo", minsize=(600, 0))

    bagel, _ = setup_demo(app, "bootstrap-light")
    bagel.pack(fill='both', expand=True)

    app.mainloop()
