import ttkbootstrap as ttk
from ttkbootstrap.api.style import get_style

root = ttk.Window()


def show_toast(
        title=None, icon=None, message=None, memo=None, duration=None, buttons=None, show_close_button=True,
        bootstyle=None, position=None, alert=None):
    style = get_style()

    top = ttk.Toplevel()
    top.minsize(400, 30)

    # windows, mac "-25-75", linux "-25-25"
    geometry = "-25-75" if position is None else position
    top.geometry(geometry)
    top.attributes('-alpha', 0.97)
    top.overrideredirect(True)
    container = ttk.Frame(top, padding=4, bootstyle=bootstyle)
    container.pack(fill='both', expand=True)

    has_title = title is not None
    has_title_and_message = title is not None and message is not None
    resolved_message = message if has_title else message
    resolved_title_font = "label" if has_title else "body"

    header = ttk.Frame(container, padding=(8, 0, 0, 0))
    header.pack(side='top', fill='x')

    if icon:
        ttk.Label(header, icon=icon).pack(side='left', padx=(0, 8))

    ttk.Label(
        header, text=resolved_message if not has_title else title, font=resolved_title_font, wraplength=380,
        justify="left").pack(side='left', fill='x')

    muted_foreground = "background[muted]" if bootstyle is None else f"{bootstyle}[muted]"

    if show_close_button:
        ttk.Button(
            header, icon="x-lg", bootstyle=f"{muted_foreground}-text", style_options={"icon_only": True},
            command=top.destroy).pack(side='right')

    if memo:
        ttk.Label(header, text=memo, font="caption", bootstyle=muted_foreground).pack(
            side='right', pady=8, padx=(0, 0 if show_close_button else 12))

    if has_title_and_message:
        ttk.Separator(container).pack(side='top', fill='x')
        ttk.Label(container, text=message, wraplength=400, justify="left").pack(side='top', fill='x', pady=8, padx=8)

    if duration:
        top.after(duration, lambda _: top.destroy(), None)

    def execute_command(options, func=None):
        def inner():
            if func:
                func()
            top.destroy()
            print(options)
            return options

        return inner

    if buttons:
        ttk.Separator(container).pack(side='top', fill='x', pady=4)
        button_frame = ttk.Frame(container)
        button_frame.pack(side='top', fill='x')
        for i, button_options in enumerate(buttons):
            func = button_options.pop('command', None)
            cmd = execute_command(button_options, func)
            ttk.Button(button_frame, **button_options, command=cmd).grid(column=i, row=0, sticky='ew')

    if alert:
        top.bell()


title = "This is a really long title and probably it should not be a title if you are going to include this much text."
message = "This is a really long message and one that I think will cause the page to wrap hopefully if it gets too long."

ttk.Button(
    root, text="Normal Toast", command=lambda: show_toast(
        "ttkbootstrap",
        'bootstrap-fill',
        "Hello world! This is a toast message",
        'Just now')).pack(side='right', padx=20, pady=20)

ttk.Button(
    root, text="Long Title", command=lambda: show_toast(
        title,
        'bootstrap-fill',
        "Hello world! This is a toast message")).pack(side='right', padx=20, pady=20)

ttk.Button(
    root, text="Long Message", command=lambda: show_toast(
        "ttkbootstrap",
        'bootstrap-fill',
        message)).pack(side='right', padx=20, pady=20)

ttk.Button(
    root, text="Message with Icon", command=lambda: show_toast(
        icon='bootstrap-fill',
        message="You have new messages"
    )).pack(side='right', padx=20, pady=20)

ttk.Button(
    root, text="Message Only", command=lambda: show_toast(
        message="You have new messages",
        bootstyle="danger"
    )).pack(side='right', padx=20, pady=20)

ttk.Button(
    root, text="With Timeout", command=lambda: show_toast(
        message="This will only last for 2 seconds",
        duration=2000
    )).pack(side='right', padx=20, pady=20)

ttk.Button(
    root, text="Normal With Buttons", command=lambda: show_toast(
        "ttkbootstrap",
        'bootstrap-fill',
        "Hello world! This is a toast message",
        show_close_button=False,
        buttons=[{"text": "Submit", "command": lambda: print("Hello world")},
                 {"text": "Cancel", "bootstyle": "secondary"}],
        memo="Just Now")).pack(side='right', padx=20, pady=20)

ttk.Button(
    root, text="Primary Toast", command=lambda: show_toast(
        "ttkbootstrap",
        'bootstrap-fill',
        "Hello world! This is a toast message",
        bootstyle="primary",
        position="-100+100",
        memo='Just now')).pack(side='right', padx=20, pady=20)

root.mainloop()
