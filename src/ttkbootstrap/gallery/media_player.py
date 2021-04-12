"""
    Author: Israel Dryer
    Modified: 2021-04-07
    Adapted for ttkbootstrap from: https://github.com/israel-dryer/Mini-VLC-Player
"""
import tkinter
from tkinter import ttk

from ttkbootstrap import Style


class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Media Player')
        self.style = Style()
        self.style.theme_use('minty')
        self.player = Player(self)
        self.player.pack(fill='both', expand='yes')
        self.style.configure('TButton', font='Helvetica 20')
        self.style.configure('header.TLabel', background=self.style.colors.border, padding=10)


class Player(ttk.Frame):
    """
    An interface for a media player
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=1)
        self.background = tkinter.PhotoImage(file='assets/mp_background.png')
        self.controls = {
            'skip-previous': '\u23EE',
            'play': '\u23F5',
            'pause': '\u23F8',
            'stop': '\u23F9',
            'skip-next': '\u23ED',
            'open-file': '\U0001f4c2'}

        # track information header
        self.track_info = tkinter.StringVar(value='Open a file to begin playback')
        header = ttk.Label(self, textvariable=self.track_info, font='Helvetica 12', style='header.TLabel')
        header.pack(fill='x', padx=2)

        # media container
        self.container = ttk.Label(self, image=self.background)
        self.container.pack(fill='both', expand='yes')

        # progress bar
        progress_frame = ttk.Frame(self, padding=10)
        progress_frame.pack(fill='x', expand='yes')
        self.time_elapsed = ttk.Label(progress_frame, text='00:00', font='Helvetica 12')
        self.time_elapsed.pack(side='left')
        self.time_scale = ttk.Scale(progress_frame, orient='horizontal', style='info.Horizontal.TScale')
        self.time_scale.pack(side='left', fill='x', expand='yes', padx=10)
        self.time_remaining = ttk.Label(progress_frame, text='00:00', font='Helvetica 12')
        self.time_remaining.pack(side='right')

        # button controls
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', expand='yes')
        self.buttons = {
            'play': ttk.Button(control_frame, text=self.controls['play']),
            'skip-previous': ttk.Button(control_frame, text=self.controls['skip-previous']),
            'skip-next': ttk.Button(control_frame, text=self.controls['skip-next']),
            'pause': ttk.Button(control_frame, text=self.controls['pause']),
            'stop': ttk.Button(control_frame, text=self.controls['stop']),
            'open-file': ttk.Button(control_frame, text=self.controls['open-file'], style='secondary.TButton')}
        for button in ['skip-previous', 'play', 'skip-next', 'pause', 'stop', 'open-file']:
            self.buttons[button].pack(side='left', fill='x', expand='yes', ipadx=5, ipady=5, padx=2, pady=2)


if __name__ == '__main__':
    Application().mainloop()
