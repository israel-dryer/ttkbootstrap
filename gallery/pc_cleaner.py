"""
    Author: Israel Dryer
    Modified: 2021-10-24
    Adapted from: https://images.idgesg.net/images/article/2018/08/cw_win10_utilities_ss_02-100769136-orig.jpg
"""
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

PATH = Path(__file__)


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('PC Cleaner')
        self.style = Style('pulse')
        self.cleaner = Cleaner(self)
        self.cleaner.pack(fill=tk.BOTH, expand=tk.YES)

        # custom styles
        self.style.configure(
            style='header.TLabel',
            background=self.style.colors.secondary,
            foreground=self.style.colors.info
        )
        # do not allow window resizing
        self.resizable(False, False)


class Cleaner(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # application images
        self.logo_img = tk.PhotoImage(
            name='logo',
            file=PATH.parent / 'assets/icons8_broom_64px_1.png'
        )
        self.brush_img = tk.PhotoImage(
            name='cleaner',
            file=PATH.parent / 'assets/icons8_broom_64px.png'
        )
        self.registry_img = tk.PhotoImage(
            name='registry',
            file=PATH.parent / 'assets/icons8_registry_editor_64px.png'
        )
        self.tools_img = tk.PhotoImage(
            name='tools',
            file=PATH.parent / 'assets/icons8_wrench_64px.png'
        )
        self.options_img = tk.PhotoImage(
            name='options',
            file=PATH.parent / 'assets/icons8_settings_64px.png'
        )
        self.privacy_img = tk.PhotoImage(
            name='privacy',
            file=PATH.parent / 'assets/icons8_spy_80px.png'
        )
        self.junk_img = tk.PhotoImage(
            name='junk',
            file=PATH.parent / 'assets/icons8_trash_can_80px.png'
        )
        self.protect_img = tk.PhotoImage(
            name='protect',
            file=PATH.parent / 'assets/icons8_protect_40px.png'
        )

        # header
        header_frame = ttk.Frame(self, padding=20, bootstyle='secondary')
        header_frame.grid(row=0, column=0, columnspan=3, sticky=tk.EW)

        ttk.Label(
            master=header_frame,
            image='logo',
            style='header.TLabel'
        ).pack(side=tk.LEFT)

        logo_text = ttk.Label(
            master=header_frame,
            text='pc cleaner',
            font=('TkDefaultFixed', 30),
            style='header.TLabel'
        )
        logo_text.pack(side=tk.LEFT, padx=10)

        # action buttons
        action_frame = ttk.Frame(self)
        action_frame.grid(row=1, column=0, sticky=tk.NSEW)

        cleaner_btn = ttk.Button(
            master=action_frame,
            image='cleaner',
            text='cleaner',
            compound=tk.TOP,
            bootstyle='info'
        )
        cleaner_btn.pack(side=tk.TOP, fill=tk.BOTH, ipadx=10, ipady=10)

        registry_btn = ttk.Button(
            master=action_frame,
            image='registry',
            text='registry',
            compound=tk.TOP,
            bootstyle='info'
        )
        registry_btn.pack(side=tk.TOP, fill=tk.BOTH, ipadx=10, ipady=10)

        tools_btn = ttk.Button(
            master=action_frame,
            image='tools',
            text='tools',
            compound=tk.TOP,
            bootstyle='info'
        )
        tools_btn.pack(side=tk.TOP, fill=tk.BOTH, ipadx=10, ipady=10)

        options_btn = ttk.Button(
            master=action_frame,
            image='options',
            text='options',
            compound=tk.TOP,
            bootstyle='info'
        )
        options_btn.pack(side=tk.TOP, fill=tk.BOTH, ipadx=10, ipady=10)

        # option notebook
        notebook = ttk.Notebook(self)
        notebook.grid(row=1, column=1, sticky=tk.NSEW, pady=(25, 0))

        # windows tab
        windows_tab = ttk.Frame(notebook, padding=10)
        wt_scrollbar = tk.Scrollbar(windows_tab)
        wt_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        wt_canvas = tk.Canvas(
            master=windows_tab,
            border=0,
            highlightthickness=0,
            yscrollcommand=wt_scrollbar.set
        )
        wt_canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        # adjust the scrollregion when the size of the canvas changes
        wt_canvas.bind(
            sequence='<Configure>',
            func=lambda e: wt_canvas.configure(
                scrollregion=wt_canvas.bbox(tk.ALL))
        )
        wt_scrollbar.configure(command=wt_canvas.yview)
        scroll_frame = ttk.Frame(wt_canvas)
        wt_canvas.create_window((0, 0), window=scroll_frame, anchor=tk.NW)

        radio_options = [
            'Internet Cache', 'Internet History', 'Cookies',
            'Download History', 'Last Download Location',
            'Session', 'Set Aside Tabs', 'Recently Typed URLs',
            'Saved Form Information', 'Saved Password'
        ]

        edge = ttk.Labelframe(
            master=scroll_frame,
            text='Microsoft Edge',
            padding=(20, 5)
        )
        edge.pack(fill=tk.BOTH)

        explorer = ttk.Labelframe(
            master=scroll_frame,
            text='Internet Explorer',
            padding=(20, 5)
        )
        explorer.pack(fill=tk.BOTH, pady=10)

        # add radio buttons to each label frame section
        for section in [edge, explorer]:
            for opt in radio_options:
                cb = ttk.Checkbutton(section, text=opt, state=tk.NORMAL)
                cb.invoke()
                cb.pack(side=tk.TOP, pady=2, fill=tk.X)
        notebook.add(windows_tab, text='windows')

        # empty tab for looks
        notebook.add(ttk.Frame(notebook), text='applications')

        # results frame
        results_frame = ttk.Frame(self)
        results_frame.grid(row=1, column=2, sticky=tk.NSEW)

        # progressbar with text indicator
        pb_frame = ttk.Frame(results_frame, padding=(0, 10, 10, 10))
        pb_frame.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)

        pb = ttk.Progressbar(
            master=pb_frame,
            bootstyle=('success', 'striped'),
            variable='progress'
        )
        pb.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=(15, 10))

        ttk.Label(pb_frame, text='%').pack(side=tk.RIGHT)
        ttk.Label(pb_frame, textvariable='progress').pack(side=tk.RIGHT)
        self.setvar('progress', 78)

        # result cards
        cards_frame = ttk.Frame(
            master=results_frame,
            name='cards-frame',
            bootstyle='secondary button'
        )
        cards_frame.pack(fill=tk.BOTH, expand=tk.YES)

        # privacy card
        priv_card = ttk.Frame(
            master=cards_frame, 
            padding=1, 
        )
        priv_card.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 5), pady=10)

        priv_container = ttk.Frame(
            master=priv_card, 
            padding=40,
        )
        priv_container.pack(fill=tk.BOTH, expand=tk.YES)

        priv_lbl = ttk.Label(
            master=priv_container,
            image='privacy',
            text='PRIVACY',
            compound=tk.TOP,
            anchor=tk.CENTER
        )
        priv_lbl.pack(fill=tk.BOTH, padx=20, pady=(40, 0))

        ttk.Label(
            master=priv_container,
            textvariable='priv_lbl',
            bootstyle='primary'
        ).pack(pady=(0, 20))
        self.setvar('priv_lbl', '6025 tracking file(s) removed')

        # junk card
        junk_card = ttk.Frame(
            master=cards_frame,
            padding=1,
        )
        junk_card.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 10), pady=10)
        
        junk_container = ttk.Frame(junk_card, padding=40)
        junk_container.pack(fill=tk.BOTH, expand=tk.YES)
        
        junk_lbl = ttk.Label(
            master=junk_container, 
            image='junk',
            text='PRIVACY', 
            compound=tk.TOP, 
            anchor=tk.CENTER,
        )
        junk_lbl.pack(fill=tk.BOTH, padx=20, pady=(40, 0))
        
        ttk.Label(
            master=junk_container, 
            textvariable='junk_lbl',
            bootstyle='primary', 
            justify=tk.CENTER
        ).pack(pady=(0, 20))
        self.setvar('junk_lbl', '1,150 MB of unneccesary file(s)\nremoved')

        # user notification
        note_frame = ttk.Frame(
            master=results_frame, 
            bootstyle='secondary', 
            padding=40
        )
        note_frame.pack(fill=tk.BOTH)
        
        note_msg = ttk.Label(
            master=note_frame, 
            text='We recommend that you better protect your data', 
            anchor=tk.CENTER,
            style='header.TLabel', 
            font=('Helvetica', 12, 'italic')
        )
        note_msg.pack(fill=tk.BOTH)


if __name__ == '__main__':

    Application().mainloop()
