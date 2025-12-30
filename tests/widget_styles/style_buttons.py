import ttkbootstrap as ttk

DARK = 'dark'
LIGHT = 'light'


def button_style_frame(bootstyle, widget_name):
    frame = ttk.Frame(root, padding=5)

    title = ttk.Label(
        master=frame,
        text=widget_name,
        anchor='center'
    )
    title.pack(padx=5, pady=2, fill='both')

    ttk.Separator(frame).pack(padx=5, pady=5, fill='x')

    ttk.Button(
        master=frame,
        text='Default',
        variant=bootstyle,
        compound="left",
        icon="bootstrap",
    ).pack(padx=5, pady=5, fill='both')

    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'dark', 'light']:
        ttk.Button(
            master=frame,
            text=color.title(),
            color=color,
            variant=bootstyle,
            compound="left",
            cursor="hand2" if bootstyle == "link" else None,
            icon="bootstrap",
        ).pack(padx=5, pady=5, fill='both')

    ttk.Button(
        master=frame,
        text='disabled',
        state='disabled',
        cursor="hand2" if bootstyle == "link" else None,
        color=color,
        variant=bootstyle,
    ).pack(padx=5, pady=5, fill='both')

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.App(theme="dark")

    button_style_frame('default', 'Solid Button').pack(side='left')
    button_style_frame('outline', 'Outline Button').pack(side='left')
    button_style_frame('ghost', 'Ghost Button').pack(side='left')
    button_style_frame('text', 'Text Button').pack(side='left')
    button_style_frame('link', 'Link Button').pack(side='left')
    ttk.Button(
        root, cursor="hand2", icon="sun", command=lambda: ttk.set_theme('light'),
        style_options={"icon_only": True}).pack(padx=10, pady=10)
    ttk.Button(
        root, cursor="hand2", icon="moon", command=lambda: ttk.set_theme('dark'),
        style_options={"icon_only": True}).pack(padx=10, pady=10)
    root.mainloop()
