"""
    Script for generating Widget screenshots for documentation
"""
from multiprocessing.context import Process
from tkinter import ttk

from ttkbootstrap import Style
from ttkbootstrap.gallery.screenshot import Screenshot


# get_screensize = lambda: print((window.winfo_width(), window.winfo_height()))
# window.after(1000, get_screensize)

def screenshot_button(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for solid and outline pushbuttons
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    ss = Screenshot(window, '../images/buttons.png')

    # solid buttons
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='TButton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=5)
    ttk.Button(f1, text='TButton', style=f'TButton', width=20).pack(fill='x', padx=5, pady=10)
    for s in style.colors:
        ttk.Button(f1, text=f'{s}.TButton', style=f'{s}.TButton').pack(fill='x', padx=5, pady=10)

    # outline buttons
    f2 = ttk.Frame(window, padding=5)
    f2.pack(fill='both', side='left', expand='yes')
    ttk.Label(f2, text='Outline.TButton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f2).pack(fill='x', padx=5, pady=5)
    ttk.Button(f2, text='Outline.TButton', style='Outline.TButton').pack(fill='x', padx=5, pady=10)
    for s in style.colors:
        ttk.Button(f2, text=f'{s}.Outline.TButton', style=f'{s}.Outline.TButton').pack(fill='x', padx=5, pady=10)

    # link buttons
    f3 = ttk.Frame(window, padding=5)
    f3.pack(fill='both', side='left', expand='yes')
    ttk.Label(f3, text='Link.TButton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f3).pack(fill='x', padx=5, pady=5)
    ttk.Button(f3, text='Link.TButton', style='Link.TButton', width=20).pack(fill='x', padx=5, pady=10)
    for s in style.colors:
        ttk.Button(f3, text=f'{s}.Link.TButton', style=f'{s}.Link.TButton').pack(fill='x', padx=5, pady=10)

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_checkbutton(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for classic checkbutton style
    """
    style = Style(theme)
    window = style.master
    window.geometry('272x280')
    window.title('ttkbootstrap')
    ss = Screenshot(window, '../images/checkbutton.png')

    # classic checkbutton
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='TCheckbutton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=5)
    for s in style.colors:
        b = ttk.Checkbutton(f1, text=f'{s}.TCheckbutton', style=f'{s}.TCheckbutton')
        b.pack(fill='x', padx=5, pady=10)
        b.invoke()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_checkbutton_toolbutton(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for classic toolbutton
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    ss = Screenshot(window, '../images/checkbutton_toolbutton.png')
    f5 = ttk.Frame(window, padding=10)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text='Toolbutton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=(5, 10))

    def create_frame(parent, c):
        """Create frame for each item and insert widgets"""
        parent.setvar(f'{c}-a', True)
        parent.setvar(f'{c}-b', False)
        parent.setvar(f'{c}-c', False)
        ttk.Label(parent, text=f'{c}.Toolbutton').pack(padx=5, pady=(5, 0), fill='x')
        frame = ttk.Frame(parent)
        frame.pack()
        ttk.Checkbutton(frame, variable=f'{c}-a', text='Selected', style=f'{c}.Toolbutton', padding=5, width=10).pack(
            side='left', pady=(5, 10), fill='x')
        ttk.Checkbutton(frame, variable=f'{c}-b', text='Check', style=f'{c}.Toolbutton', padding=5, width=10).pack(
            side='left', pady=(5, 10), fill='x')
        ttk.Checkbutton(frame, variable=f'{c}-c', text='Check', style=f'{c}.Toolbutton', padding=5, width=10).pack(
            side='left', pady=(5, 10), fill='x')
        return frame

    for c in style.colors:
        create_frame(f5, c).pack()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_checkbutton_outline_toolbutton(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for classic outline toolbutton
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    ss = Screenshot(window, '../images/checkbutton_outline_toolbutton.png')
    f5 = ttk.Frame(window, padding=10)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text='Outline.Toolbutton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=(5, 10))

    def create_frame(parent, c):
        """Create frame for each item and insert widgets"""
        parent.setvar(f'{c}-a', True)
        parent.setvar(f'{c}-b', False)
        parent.setvar(f'{c}-c', False)
        ttk.Label(parent, text=f'{c}.Outline.Toolbutton').pack(padx=5, pady=(5, 0), fill='x')
        frame = ttk.Frame(parent)
        frame.pack()
        ttk.Checkbutton(frame, variable=f'{c}-a', text='Selected', style=f'{c}.Outline.Toolbutton', padding=5,
                        width=10).pack(
            side='left', padx=0, pady=(5, 10), fill='x')
        ttk.Checkbutton(frame, variable=f'{c}-b', text='Check', style=f'{c}.Outline.Toolbutton', padding=5,
                        width=10).pack(
            side='left', padx=0, pady=(5, 10), fill='x')
        ttk.Checkbutton(frame, variable=f'{c}-c', text='Check', style=f'{c}.Outline.Toolbutton', padding=5,
                        width=10).pack(
            side='left', padx=0, pady=(5, 10), fill='x')
        return frame

    for c in style.colors:
        create_frame(f5, c).pack()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_roundtoggle_toolbutton():
    """
    Get screenshot for a round toggle toolbutton
    """
    style = Style()
    window = style.master
    window.geometry('272x335')
    window.title('ttkbootstrap')
    ss = Screenshot(window, '../images/roundtoggle.png')

    # classic checkbutton
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f1, text='Roundtoggle.Toolbutton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=5)

    # buttons
    for s in style.colors:
        b = ttk.Checkbutton(f1, text=f'{s}.Roundtoggle.Toolbutton', style=f'{s}.Roundtoggle.Toolbutton')
        b.pack(fill='x', padx=5, pady=10)
        b.invoke()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_squaretoggle_toolbutton():
    """
    Get screenshot for a round toggle toolbutton
    """
    style = Style()
    window = style.master
    window.geometry('272x335')
    window.title('ttkbootstrap')
    ss = Screenshot(window, '../images/squaretoggle.png')

    # classic checkbutton
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f1, text='Squaretoggle.Toolbutton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=5)

    # buttons
    for s in style.colors:
        b = ttk.Checkbutton(f1, text=f'{s}.Squaretoggle.Toolbutton', style=f'{s}.Squaretoggle.Toolbutton')
        b.pack(fill='x', padx=5, pady=10)
        b.invoke()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_combobox_primary():
    """
    Get screenshot for a combobox
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'primary'
    ss = Screenshot(window, f'../images/combobox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TCombobox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Combobox(f5, style=f'{color}.TCombobox')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Combobox(f5, style=f'{color}.TCombobox')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Combobox(f5, style=f'{color}.TCombobox')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_combobox_secondary():
    """
    Get screenshot for a combobox
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'secondary'
    ss = Screenshot(window, f'../images/combobox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TCombobox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Combobox(f5, style=f'{color}.TCombobox')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Combobox(f5, style=f'{color}.TCombobox')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Combobox(f5, style=f'{color}.TCombobox')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_combobox_success():
    """
    Get screenshot for a combobox
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'success'
    ss = Screenshot(window, f'../images/combobox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TCombobox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Combobox(f5, style=f'{color}.TCombobox')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Combobox(f5, style=f'{color}.TCombobox')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Combobox(f5, style=f'{color}.TCombobox')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_combobox_info():
    """
    Get screenshot for a combobox
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'info'
    ss = Screenshot(window, f'../images/combobox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TCombobox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Combobox(f5, style=f'{color}.TCombobox')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Combobox(f5, style=f'{color}.TCombobox')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Combobox(f5, style=f'{color}.TCombobox')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_combobox_warning():
    """
    Get screenshot for a combobox
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'warning'
    ss = Screenshot(window, f'../images/combobox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TCombobox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Combobox(f5, style=f'{color}.TCombobox')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Combobox(f5, style=f'{color}.TCombobox')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Combobox(f5, style=f'{color}.TCombobox')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_combobox_danger():
    """
    Get screenshot for a combobox
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'danger'
    ss = Screenshot(window, f'../images/combobox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TCombobox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Combobox(f5, style=f'{color}.TCombobox')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Combobox(f5, style=f'{color}.TCombobox')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Combobox(f5, style=f'{color}.TCombobox')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_entry_primary():
    """
    Get screenshot for a entry
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'primary'
    ss = Screenshot(window, f'../images/entry_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TEntry', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Entry(f5, style=f'{color}.TEntry')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Entry(f5, style=f'{color}.TEntry')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Entry(f5, style=f'{color}.TEntry')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_entry_secondary():
    """
    Get screenshot for a entry
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'secondary'
    ss = Screenshot(window, f'../images/entry_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TEntry', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Entry(f5, style=f'{color}.TEntry')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Entry(f5, style=f'{color}.TEntry')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Entry(f5, style=f'{color}.TEntry')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_entry_success():
    """
    Get screenshot for a entry
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'success'
    ss = Screenshot(window, f'../images/entry_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TEntry', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Entry(f5, style=f'{color}.TEntry')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Entry(f5, style=f'{color}.TEntry')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Entry(f5, style=f'{color}.TEntry')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_entry_info():
    """
    Get screenshot for a entry
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'info'
    ss = Screenshot(window, f'../images/entry_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TEntry', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Entry(f5, style=f'{color}.TEntry')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Entry(f5, style=f'{color}.TEntry')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Entry(f5, style=f'{color}.TEntry')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_entry_warning():
    """
    Get screenshot for a entry
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'warning'
    ss = Screenshot(window, f'../images/entry_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TEntry', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Entry(f5, style=f'{color}.TEntry')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Entry(f5, style=f'{color}.TEntry')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Entry(f5, style=f'{color}.TEntry')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_entry_danger():
    """
    Get screenshot for a entry
    """
    style = Style()
    window = style.master
    window.title('ttkbootstrap')
    color = 'danger'
    ss = Screenshot(window, f'../images/entry_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TEntry', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Entry(f5, style=f'{color}.TEntry')
    a.insert('end', 'normal')
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Entry(f5, style=f'{color}.TEntry')
    b.insert('end', 'active')
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Entry(f5, style=f'{color}.TEntry')
    c.insert('end', 'focused')
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    window.after(1000, lambda: ss.get_bounding_box(None))
    window.after(1500, window.quit)
    window.mainloop()


def screenshot_frame(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for a entry
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('300x500')
    ss = Screenshot(window, f'../images/frame.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'TFrame', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    f = ttk.Frame(f5, padding=20, style='TFrame')
    f.pack(fill='both', expand='yes')
    ttk.Label(f, text=f'TFrame', anchor='center').pack(fill='both', expand='yes')

    for c in style.colors:
        f = ttk.Frame(f5, padding=20, style=f'{c}.TFrame')
        f.pack(fill='both', expand='yes')
        ttk.Label(f, text=f'{c}.TFrame', anchor='center', style=f'{c}.Inverse.TLabel').pack(fill='both', expand='yes')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_label(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for labels
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    ss = Screenshot(window, '../images/label.png')

    # regular labels
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='TLabel', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=5)
    ttk.Label(f1, text='TLabel', style=f'TLabel', width=20, padding=5).pack(fill='x', padx=5, pady=10)
    for s in style.colors:
        ttk.Label(f1, text=f'{s}.TLabel', style=f'{s}.TLabel', padding=5).pack(fill='x', padx=5, pady=10)

    # inverse labels
    f2 = ttk.Frame(window, padding=5)
    f2.pack(fill='both', side='left', expand='yes')
    ttk.Label(f2, text='Inverse.TLabel', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f2).pack(fill='x', padx=5, pady=5)
    ttk.Label(f2, text='Inverse.TLabel', style='Inverse.TLabel', padding=5).pack(fill='x', padx=5, pady=10)
    for s in style.colors:
        ttk.Label(f2, text=f'{s}.Inverse.TLabel', style=f'{s}.Inverse.TLabel', padding=5).pack(fill='x', padx=5,
                                                                                               pady=10)

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_labelframe(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for labelframes
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('400x600')
    ss = Screenshot(window, '../images/labelframe.png')

    # header
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='TLabelframe', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=5)

    ttk.Labelframe(f1, text='TLabelframe', style='TLabelframe', padding=10).pack(fill='both', expand='yes', padx=10,
                                                                                 pady=10)
    for c in style.colors:
        ttk.Labelframe(f1, text=f'{c}.TLabelframe', style=f'{c}.TLabelframe', padding=10).pack(fill='both',
                                                                                               expand='yes', padx=10,
                                                                                               pady=10)

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_menubutton(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for solid and outline menubuttons
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    ss = Screenshot(window, '../images/menubutton.png')

    # solid menubuttons
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='TMenubutton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=5)
    ttk.Menubutton(f1, text='TMenubutton', style=f'TMenubutton', width=25).pack(fill='x', padx=5, pady=10)
    for s in style.colors:
        ttk.Menubutton(f1, text=f'{s}.TMenubutton', style=f'{s}.TMenubutton').pack(fill='x', padx=5, pady=10)

    # outline menubuttons
    f2 = ttk.Frame(window, padding=5)
    f2.pack(fill='both', side='left', expand='yes')
    ttk.Label(f2, text='Outline.TMenubutton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f2).pack(fill='x', padx=5, pady=5)
    ttk.Menubutton(f2, text='Outline.TMenubutton', style='Outline.TMenubutton', width=25).pack(fill='x', padx=5,
                                                                                               pady=10)
    for s in style.colors:
        ttk.Menubutton(f2, text=f'{s}.Outline.TMenubutton', style=f'{s}.Outline.TMenubutton').pack(fill='x', padx=5,
                                                                                                   pady=10)

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_notebook(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for a notebook
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('400x300')
    ss = Screenshot(window, '../images/notebook.png')
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')

    # widget
    nb = ttk.Notebook(f1)
    f6 = ttk.Frame(nb)
    nb.add(f6, text='Tab 1')
    nb.add(ttk.Frame(nb), text='Tab 2')
    nb.add(ttk.Frame(nb), text='Tab 3')
    ttk.Label(f6, text='TNotebook', font='Helvetica 10 bold', anchor='center').pack(fill='both', expand='yes', pady=5)
    nb.pack(fill='both', expand='yes')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_progressbar_horizontal(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for horizontal progressbars
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('600x400')
    ss = Screenshot(window, '../images/progressbar_horizontal.png')

    # headers
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='Horizontal.TProgressbar', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=(5, 10))

    # widgets
    for c in style.colors:
        ttk.Label(f1, text=f'{c}.Horizontal.TProgressbar').pack(fill='x', padx=10)
        ttk.Progressbar(f1, value=75, style=f'{c}.Horizontal.TProgressbar').pack(fill='x', expand='yes', padx=10,
                                                                                 pady=(0, 10))

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_progressbar_horizontal_striped(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for horizontal striped progressbars
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('600x400')
    ss = Screenshot(window, '../images/progressbar_horizontal_striped.png')

    # headers
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='Striped.Horizontal.TProgressbar', font='Helvetica 10 bold', anchor='center').pack(fill='x',
                                                                                                          pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=(5, 10))

    # widgets
    for c in style.colors:
        ttk.Label(f1, text=f'{c}.Striped.Horizontal.TProgressbar').pack(fill='x', padx=10)
        ttk.Progressbar(f1, value=75, style=f'{c}.Striped.Horizontal.TProgressbar').pack(fill='x', expand='yes',
                                                                                         padx=10,
                                                                                         pady=(0, 10))

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_progressbar_vertical(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for horizontal progressbars
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('600x400')
    ss = Screenshot(window, '../images/progressbar_vertical.png')

    import tkinter as tk
    canvas = tk.Canvas(window, border=0, highlightthickness=0)
    canvas.pack(fill='both', side='left', expand='yes')
    ttk.Label(canvas, text='Vertical.TProgressbar', font='Helvetica 10 bold', anchor='center').pack(fill='x',
                                                                                                    pady=(10, 5))
    ttk.Separator(canvas).pack(fill='x', padx=5, pady=(5, 10))

    i = 50
    for c in style.colors:
        canvas.create_text((i, 200), text=f'{c}.Vertical.TProgressbar', angle=90, font='Helvetica 10')
        pb = ttk.Progressbar(canvas, value=75, style=f'{c}.Vertical.TProgressbar', orient='vertical', length=300)
        i += 25
        canvas.create_window((i, 225), window=pb)
        i += 70

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_radiobutton(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for a radiobutton
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('272x310')
    ss = Screenshot(window, '../images/radiobutton.png')
    f1 = ttk.Frame(window, padding=10)
    f1.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f1, text='TRadiobutton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=5)
    window.setvar('option', 1)

    # buttons
    for s in style.colors:
        b = ttk.Radiobutton(f1, text=f'{s}.TRadiobutton', variable='option', value=1, style=f'{s}.TRadiobutton')
        b.pack(fill='x', padx=5, pady=10)

    ttk.Radiobutton(f1, text='unselected').pack(fill='x', padx=5, pady=10)

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_radiobutton_toolbutton(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for radiobutton toolbutton
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    ss = Screenshot(window, '../images/radiobutton_toolbutton.png')
    f5 = ttk.Frame(window, padding=10)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text='Toolbutton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=(5, 10))

    def create_frame(parent, c):
        """Create frame for each item and insert widgets"""
        parent.setvar(f'{c}-a', True)
        parent.setvar(f'{c}-b', False)
        parent.setvar(f'{c}-c', False)
        ttk.Label(parent, text=f'{c}.Toolbutton').pack(padx=5, pady=(5, 0), fill='x')
        frame = ttk.Frame(parent)
        frame.pack()
        ttk.Radiobutton(frame, variable=f'{c}-a', text='Selected', style=f'{c}.Toolbutton', padding=5, width=10).pack(
            side='left', pady=(5, 10), fill='x')
        ttk.Radiobutton(frame, variable=f'{c}-b', text='Radio', style=f'{c}.Toolbutton', padding=5, width=10).pack(
            side='left', pady=(5, 10), fill='x')
        ttk.Radiobutton(frame, variable=f'{c}-c', text='Radio', style=f'{c}.Toolbutton', padding=5, width=10).pack(
            side='left', pady=(5, 10), fill='x')
        return frame

    for c in style.colors:
        create_frame(f5, c).pack()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_radiobutton_outline_toolbutton(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for radiobutton outlinetoolbutton
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    ss = Screenshot(window, '../images/radiobutton_outline_toolbutton.png')
    f5 = ttk.Frame(window, padding=10)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text='Outline.Toolbutton', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=(5, 10))

    def create_frame(parent, c):
        """Create frame for each item and insert widgets"""
        parent.setvar(f'{c}-a', True)
        parent.setvar(f'{c}-b', False)
        parent.setvar(f'{c}-c', False)
        ttk.Label(parent, text=f'{c}.Outline.Toolbutton').pack(padx=5, pady=(5, 0), fill='x')
        frame = ttk.Frame(parent)
        frame.pack()
        ttk.Radiobutton(frame, variable=f'{c}-a', text='Selected', style=f'{c}.Outline.Toolbutton', padding=5,
                        width=10).pack(
            side='left', pady=(5, 10), fill='x')
        ttk.Radiobutton(frame, variable=f'{c}-b', text='Radio', style=f'{c}.Outline.Toolbutton', padding=5,
                        width=10).pack(
            side='left', pady=(5, 10), fill='x')
        ttk.Radiobutton(frame, variable=f'{c}-c', text='Radio', style=f'{c}.Outline.Toolbutton', padding=5,
                        width=10).pack(
            side='left', pady=(5, 10), fill='x')
        return frame

    for c in style.colors:
        create_frame(f5, c).pack()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_scale_horizontal(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for horizontal scale
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('500x400')
    ss = Screenshot(window, '../images/scale_horizontal.png')

    # headers
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='Horizontal.TScale', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=(5, 10))

    # widgets
    for c in style.colors:
        ttk.Label(f1, text=f'{c}.Horizontal.TScale').pack(fill='x', padx=10)
        ttk.Scale(f1, value=75, from_=0, to=100, style=f'{c}.Horizontal.TScale', length=300).pack(fill='x',
                                                                                                  expand='yes', padx=10,
                                                                                                  pady=(0, 10))

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_scale_vertical(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for vertical
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('500x400')
    ss = Screenshot(window, '../images/scale_vertical.png')

    import tkinter as tk
    canvas = tk.Canvas(window, border=0, highlightthickness=0)
    canvas.pack(fill='both', side='left', expand='yes')
    ttk.Label(canvas, text='Vertical.TScale', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=(10, 5))

    ttk.Separator(canvas).pack(fill='x', padx=5, pady=(5, 10))

    i = 40
    for c in style.colors:
        canvas.create_text((i, 200), text=f'{c}.Vertical.TScale', angle=90, font='Helvetica 10')
        pb = ttk.Scale(canvas, from_=1, to=100, value=75, style=f'{c}.Vertical.TScale', orient='vertical', length=300)
        i += 25
        canvas.create_window((i, 225), window=pb)
        i += 50

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_scrollbar_horizontal(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for horizontal scrollbar
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('400x125')
    ss = Screenshot(window, '../images/scrollbar_horizontal.png')

    # headers
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='Horizontal.TScrollbar', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=(5, 10))

    # widgets
    hs = ttk.Scrollbar(f1, orient='horizontal')
    hs.pack(fill='x', padx=10, pady=10)
    hs.set(0.2, 0.3)

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_scrollbar_vertical(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for horizontal scrollbar
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('150x400')
    ss = Screenshot(window, '../images/scrollbar_vertical.png')

    # headers
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='Vertical.TScrollbar', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f1).pack(fill='x', padx=5, pady=(5, 10))

    # widgets
    hs = ttk.Scrollbar(f1, orient='vertical')
    hs.pack(fill='y', padx=10, pady=10, expand='yes')
    hs.set(0.2, 0.3)

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_separator_horizontal(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for horizontal separator
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('475x400')
    ss = Screenshot(window, '../images/separator_horizontal.png')

    # headers
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text='Horizontal.TSeparator', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=(5, 15))

    # widgets
    for c in style.colors:
        ttk.Label(f1, text=f'{c}.Horizontal.TSeparator').pack(fill='x', padx=10)
        ttk.Separator(f1, style=f'{c}.Horizontal.TSeparator').pack(fill='x', expand='yes', padx=10, pady=(0, 10))

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_separator_vertical(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for vertical separator
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('475x400')
    ss = Screenshot(window, '../images/separator_vertical.png')

    import tkinter as tk
    canvas = tk.Canvas(window, borderwidth=0, relief='flat', highlightthickness=0)
    canvas.pack(fill='both', side='left', expand='yes')
    ttk.Label(canvas, text='Vertical.TSeparator', font='Helvetica 10 bold', anchor='center').pack(fill='x',
                                                                                                  pady=(5, 20))

    i = 40
    for c in style.colors:
        canvas.create_text((i, 200), text=f'{c}.Vertical.TSeparator', angle=90, font='Helvetica 10')
        pb = ttk.Separator(canvas, style=f'{c}.Vertical.TSeparator', orient='vertical')
        i += 25
        canvas.create_window((i, 215), window=pb, height=300)
        i += 50

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_sizegrip(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for sizegrip
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('200x75')
    ss = Screenshot(window, f'../images/sizegrip.png')

    ttk.Label(text='TSizegrip', font='helvetica 10 bold').pack(expand='yes', pady=(10, 0))
    ttk.Sizegrip().pack(fill='both', expand='yes')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_sizegrip_primary(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for sizegrip
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('200x75')
    color = 'primary'
    ss = Screenshot(window, f'../images/sizegrip_{color}.png')

    ttk.Label(text=f'{color}.TSizegrip', font='helvetica 10 bold').pack(expand='yes', pady=(10, 0))
    ttk.Sizegrip(style=f'{color}.TSizegrip').pack(fill='both', expand='yes')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_sizegrip_secondary(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for sizegrip
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('200x75')
    color = 'secondary'
    ss = Screenshot(window, f'../images/sizegrip_{color}.png')

    ttk.Label(text=f'{color}.TSizegrip', font='helvetica 10 bold').pack(expand='yes', pady=(10, 0))
    ttk.Sizegrip(style=f'{color}.TSizegrip').pack(fill='both', expand='yes')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_sizegrip_success(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for sizegrip
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('200x75')
    color = 'success'
    ss = Screenshot(window, f'../images/sizegrip_{color}.png')

    ttk.Label(text=f'{color}.TSizegrip', font='helvetica 10 bold').pack(expand='yes', pady=(10, 0))
    ttk.Sizegrip(style=f'{color}.TSizegrip').pack(fill='both', expand='yes')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_sizegrip_info(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for sizegrip
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('200x75')
    color = 'info'
    ss = Screenshot(window, f'../images/sizegrip_{color}.png')

    ttk.Label(text=f'{color}.TSizegrip', font='helvetica 10 bold').pack(expand='yes', pady=(10, 0))
    ttk.Sizegrip(style=f'{color}.TSizegrip').pack(fill='both', expand='yes')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_sizegrip_warning(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for sizegrip
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('200x75')
    color = 'warning'
    ss = Screenshot(window, f'../images/sizegrip_{color}.png')

    ttk.Label(text=f'{color}.TSizegrip', font='helvetica 10 bold').pack(expand='yes', pady=(10, 0))
    ttk.Sizegrip(style=f'{color}.TSizegrip').pack(fill='both', expand='yes')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_sizegrip_danger(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for sizegrip
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('200x75')
    color = 'danger'
    ss = Screenshot(window, f'../images/sizegrip_{color}.png')

    ttk.Label(text=f'{color}.TSizegrip', font='helvetica 10 bold').pack(expand='yes', pady=(10, 0))
    ttk.Sizegrip(style=f'{color}.TSizegrip').pack(fill='both', expand='yes')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_spinbox_primary(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for a spinbox
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    color = 'primary'
    ss = Screenshot(window, f'../images/spinbox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TSpinbox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    a.set(1)
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    b.set(1)
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    c.set(1)
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_spinbox_secondary(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for a spinbox
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    color = 'secondary'
    ss = Screenshot(window, f'../images/spinbox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TSpinbox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    a.set(1)
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    b.set(1)
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    c.set(1)
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_spinbox_success(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for a spinbox
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    color = 'success'
    ss = Screenshot(window, f'../images/spinbox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TSpinbox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    a.set(1)
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    b.set(1)
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    c.set(1)
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_spinbox_info(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for a spinbox
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    color = 'info'
    ss = Screenshot(window, f'../images/spinbox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TSpinbox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    a.set(1)
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    b.set(1)
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    c.set(1)
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_spinbox_warning(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for a spinbox
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    color = 'warning'
    ss = Screenshot(window, f'../images/spinbox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TSpinbox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    a.set(1)
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    b.set(1)
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    c.set(1)
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_spinbox_danger(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for a spinbox
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    color = 'danger'
    ss = Screenshot(window, f'../images/spinbox_{color}.png')

    f5 = ttk.Frame(window, padding=5)
    f5.pack(fill='both', side='left', expand='yes')

    # header
    ttk.Label(f5, text=f'{color}.TSpinbox', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)
    ttk.Separator(f5).pack(fill='x', padx=5, pady=5)

    # widgets
    a = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    a.set(1)
    a.pack(side='left', fill='x', padx=5, pady=10)

    b = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    b.set(1)
    b.pack(side='left', fill='x', padx=5, pady=10)
    b.event_generate('<Enter>')

    c = ttk.Spinbox(f5, from_=101, to=100, style=f'{color}.TSpinbox')
    c.set(1)
    c.pack(side='left', fill='x', padx=5, pady=10)
    c.focus()

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_treeview_primary(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for treeview
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('300x125')
    color = 'primary'
    ss = Screenshot(window, f'../images/treeview_{color}.png')
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text=f'{color}.Treeview', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)

    # Treeview
    tv = ttk.Treeview(f1, height=3, style=f'{color}.Treeview')
    tv.pack(fill='x', pady=5)
    tv.heading('#0', text='Example heading')
    tv.insert('', 'end', 'example1', text='Example 1')
    tv.insert('', 'end', 'example2', text='Example 2')
    tv.insert('example2', 'end', text='Example 2 Child 1')
    tv.insert('example2', 'end', text='Example 2 Child 2')
    tv.selection_set('example1')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_treeview_secondary(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for treeview
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('300x125')
    color = 'secondary'
    ss = Screenshot(window, f'../images/treeview_{color}.png')
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text=f'{color}.Treeview', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)

    # Treeview
    tv = ttk.Treeview(f1, height=3, style=f'{color}.Treeview')
    tv.pack(fill='x', pady=5)
    tv.heading('#0', text='Example heading')
    tv.insert('', 'end', 'example1', text='Example 1')
    tv.insert('', 'end', 'example2', text='Example 2')
    tv.insert('example2', 'end', text='Example 2 Child 1')
    tv.insert('example2', 'end', text='Example 2 Child 2')
    tv.selection_set('example1')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_treeview_success(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for treeview
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('300x125')
    color = 'success'
    ss = Screenshot(window, f'../images/treeview_{color}.png')
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text=f'{color}.Treeview', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)

    # Treeview
    tv = ttk.Treeview(f1, height=3, style=f'{color}.Treeview')
    tv.pack(fill='x', pady=5)
    tv.heading('#0', text='Example heading')
    tv.insert('', 'end', 'example1', text='Example 1')
    tv.insert('', 'end', 'example2', text='Example 2')
    tv.insert('example2', 'end', text='Example 2 Child 1')
    tv.insert('example2', 'end', text='Example 2 Child 2')
    tv.selection_set('example1')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_treeview_info(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for treeview
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('300x125')
    color = 'info'
    ss = Screenshot(window, f'../images/treeview_{color}.png')
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text=f'{color}.Treeview', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)

    # Treeview
    tv = ttk.Treeview(f1, height=3, style=f'{color}.Treeview')
    tv.pack(fill='x', pady=5)
    tv.heading('#0', text='Example heading')
    tv.insert('', 'end', 'example1', text='Example 1')
    tv.insert('', 'end', 'example2', text='Example 2')
    tv.insert('example2', 'end', text='Example 2 Child 1')
    tv.insert('example2', 'end', text='Example 2 Child 2')
    tv.selection_set('example1')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_treeview_warning(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for treeview
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('300x125')
    color = 'warning'
    ss = Screenshot(window, f'../images/treeview_{color}.png')
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text=f'{color}.Treeview', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)

    # Treeview
    tv = ttk.Treeview(f1, height=3, style=f'{color}.Treeview')
    tv.pack(fill='x', pady=5)
    tv.heading('#0', text='Example heading')
    tv.insert('', 'end', 'example1', text='Example 1')
    tv.insert('', 'end', 'example2', text='Example 2')
    tv.insert('example2', 'end', text='Example 2 Child 1')
    tv.insert('example2', 'end', text='Example 2 Child 2')
    tv.selection_set('example1')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


def screenshot_treeview_danger(screenshot_on=True, theme='flatly'):
    """
    Get screenshot for treeview
    """
    style = Style(theme)
    window = style.master
    window.title('ttkbootstrap')
    window.geometry('300x125')
    color = 'danger'
    ss = Screenshot(window, f'../images/treeview_{color}.png')
    f1 = ttk.Frame(window, padding=5)
    f1.pack(fill='both', side='left', expand='yes')
    ttk.Label(f1, text=f'{color}.Treeview', font='Helvetica 10 bold', anchor='center').pack(fill='x', pady=5)

    # Treeview
    tv = ttk.Treeview(f1, height=3, style=f'{color}.Treeview')
    tv.pack(fill='x', pady=5)
    tv.heading('#0', text='Example heading')
    tv.insert('', 'end', 'example1', text='Example 1')
    tv.insert('', 'end', 'example2', text='Example 2')
    tv.insert('example2', 'end', text='Example 2 Child 1')
    tv.insert('example2', 'end', text='Example 2 Child 2')
    tv.selection_set('example1')

    if screenshot_on:
        window.after(1000, lambda: ss.get_bounding_box(None))
        window.after(1500, window.quit)
    window.mainloop()


if __name__ == '__main__':
    programs = [
        screenshot_button,
        screenshot_checkbutton,
        screenshot_checkbutton_toolbutton,
        screenshot_checkbutton_outline_toolbutton,
        screenshot_roundtoggle_toolbutton,
        screenshot_squaretoggle_toolbutton,
        screenshot_combobox_primary,
        screenshot_combobox_secondary,
        screenshot_combobox_success,
        screenshot_combobox_info,
        screenshot_combobox_warning,
        screenshot_combobox_danger,
        screenshot_entry_primary,
        screenshot_entry_secondary,
        screenshot_entry_success,
        screenshot_entry_info,
        screenshot_entry_warning,
        screenshot_entry_danger,
        screenshot_frame,
        screenshot_label,
        screenshot_labelframe,
        screenshot_menubutton,
        screenshot_notebook,
        screenshot_progressbar_horizontal,
        screenshot_progressbar_horizontal_striped,
        screenshot_progressbar_vertical,
        screenshot_radiobutton,
        screenshot_radiobutton_toolbutton,
        screenshot_radiobutton_outline_toolbutton,
        screenshot_scale_horizontal,
        screenshot_scale_vertical,
        screenshot_scrollbar_horizontal,
        screenshot_scrollbar_vertical,
        screenshot_separator_horizontal,
        screenshot_separator_vertical,
        screenshot_sizegrip,
        screenshot_sizegrip_primary,
        screenshot_sizegrip_secondary,
        screenshot_sizegrip_success,
        screenshot_sizegrip_info,
        screenshot_sizegrip_warning,
        screenshot_sizegrip_danger,
        screenshot_spinbox_primary,
        screenshot_spinbox_secondary,
        screenshot_spinbox_success,
        screenshot_spinbox_info,
        screenshot_spinbox_warning,
        screenshot_spinbox_danger,
        screenshot_treeview_primary,
        screenshot_treeview_secondary,
        screenshot_treeview_success,
        screenshot_treeview_info,
        screenshot_treeview_warning,
        screenshot_treeview_danger,
    ]

    p_list = []
    for p in programs:
        p_list.append(Process(target=p))

    for p in p_list:
        p.start()
        p.join()


    # TODO add an application window here to select the type of screenshots I want to do.

