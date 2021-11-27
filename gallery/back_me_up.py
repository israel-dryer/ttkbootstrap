"""
    Author: Israel Dryer
    Modified: 2021-11-10
    Adapted from: http://www.leo-backup.com/screenshots.shtml
"""
from datetime import datetime
from random import choices
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.style import utility
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
utility.enable_high_dpi_awareness()


class Application(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('Back Me Up')

        self.style = ttk.Style()

        self.bmu = BackMeUp(self, padding=2)
        self.bmu.pack(fill=tk.BOTH, expand=tk.YES)


class BackMeUp(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image_files = {
            'properties-dark': 'icons8_settings_24px.png',
            'properties-light': 'icons8_settings_24px_2.png',
            'add-to-backup-dark': 'icons8_add_folder_24px.png',
            'add-to-backup-light': 'icons8_add_book_24px.png',
            'stop-backup-dark': 'icons8_cancel_24px.png',
            'stop-backup-light': 'icons8_cancel_24px_1.png',
            'play': 'icons8_play_24px_1.png',
            'refresh': 'icons8_refresh_24px_1.png',
            'stop-dark': 'icons8_stop_24px.png',
            'stop-light': 'icons8_stop_24px_1.png',
            'opened-folder': 'icons8_opened_folder_24px.png',
            'logo': 'backup.png'
        }
        self.photoimages = []
        imgpath = Path(__file__).parent / 'assets'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(tk.PhotoImage(name=key, file=_path))

        # ----- buttonbar
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=tk.X, pady=1, side=tk.TOP)

        ## new backup
        _func = lambda: showinfo(message='Adding new backup')
        btn = ttk.Button(
            master=buttonbar, text='New backup set',
            image='add-to-backup-light', 
            compound=tk.LEFT, 
            command=_func
        )
        btn.pack(side=tk.LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        ## backup
        _func = lambda: showinfo(message='Backing up...')
        btn = ttk.Button(
            master=buttonbar, 
            text='Backup', 
            image='play', 
            compound=tk.LEFT, 
            command=_func
        )
        btn.pack(side=tk.LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## refresh
        _func = lambda: showinfo(message='Refreshing...')
        btn = ttk.Button(
            master=buttonbar, 
            text='Refresh', 
            image='refresh',
            compound=tk.LEFT, 
            command=_func
        )
        btn.pack(side=tk.LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## stop
        _func = lambda: showinfo(message='Stopping backup.')
        btn = ttk.Button(
            master=buttonbar, 
            text='Stop', 
            image='stop-light',
            compound=tk.LEFT, 
            command=_func
        )
        btn.pack(side=tk.LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## settings
        _func = command=lambda: showinfo(message='Changing settings')
        btn = ttk.Button(
            master=buttonbar, 
            text='Settings', 
            image='properties-light',
            compound=tk.LEFT, 
            command=_func
        )
        btn.pack(side=tk.LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        # ----- left panel
        left_panel = ttk.Frame(self, style='bg.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        ## ----- backup summary (collapsible)
        bus_cf = CollapsingFrame(left_panel)
        bus_cf.pack(fill=tk.X, pady=1)

        ## container
        bus_frm = ttk.Frame(bus_cf, padding=5)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(
            child=bus_frm, 
            title='Backup Summary', 
            bootstyle='secondary')

        ## destination
        lbl = ttk.Label(bus_frm, text='Destination:')
        lbl.grid(row=0, column=0, sticky=tk.W, pady=2)
        lbl = ttk.Label(bus_frm, textvariable='destination')
        lbl.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        self.setvar('destination', 'd:/test/')

        ## last run
        lbl = ttk.Label(bus_frm, text='Last Run:')
        lbl.grid(row=1, column=0, sticky=tk.W, pady=2)
        lbl = ttk.Label(bus_frm, textvariable='lastrun')
        lbl.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        self.setvar('lastrun', '14.06.2021 19:34:43')

        ## files Identical
        lbl = ttk.Label(bus_frm, text='Files Identical:')
        lbl.grid(row=2, column=0, sticky=tk.W, pady=2)
        lbl = ttk.Label(bus_frm, textvariable='filesidentical')
        lbl.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)
        self.setvar('filesidentical', '15%')

        ## section separator
        sep = ttk.Separator(bus_frm, bootstyle='secondary')
        sep.grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.EW)

        ## properties button
        _func = lambda: showinfo(message='Changing properties')
        bus_prop_btn = ttk.Button(
            master=bus_frm, 
            text='Properties', 
            image='properties-dark', 
            compound=tk.LEFT,
            command=_func, 
            bootstyle='link'
        )
        bus_prop_btn.grid(row=4, column=0, columnspan=2, sticky=tk.W)

        ## add to backup button
        _func = lambda: showinfo(message='Adding to backup')
        add_btn = ttk.Button(
            master=bus_frm, 
            text='Add to backup', 
            image='add-to-backup-dark', 
            compound=tk.LEFT,
            command=_func, 
            bootstyle='link'
        )
        add_btn.grid(row=5, column=0, columnspan=2, sticky=tk.W)

        # ----- backup status (collapsible)
        status_cf = CollapsingFrame(left_panel)
        status_cf.pack(fill=tk.BOTH, pady=1)

        ## container
        status_frm = ttk.Frame(status_cf, padding=10)
        status_frm.columnconfigure(1, weight=1)
        status_cf.add(
            child=status_frm, 
            title='Backup Status', 
            bootstyle='secondary'
        )
        ## progress message
        lbl = ttk.Label(
            master=status_frm, 
            textvariable='prog-message', 
            font='Helvetica 10 bold'
        )
        lbl.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.setvar('prog-message', 'Backing up...')

        ## progress bar
        pb = ttk.Progressbar(
            master=status_frm, 
            variable='prog-value', 
            bootstyle='success'
        )
        pb.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(10, 5))
        self.setvar('prog-value', 71)

        ## time started
        lbl = ttk.Label(status_frm, textvariable='prog-time-started')
        lbl.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=2)
        self.setvar('prog-time-started', 'Started at: 14.06.2021 19:34:56')

        ## time elapsed
        lbl = ttk.Label(status_frm, textvariable='prog-time-elapsed')
        lbl.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=2)
        self.setvar('prog-time-elapsed', 'Elapsed: 1 sec')

        ## time remaining
        lbl = ttk.Label(status_frm, textvariable='prog-time-left')
        lbl.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=2)
        self.setvar('prog-time-left', 'Left: 0 sec')

        ## section separator
        sep = ttk.Separator(status_frm, bootstyle='secondary')
        sep.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.EW)

        ## stop button
        _func = lambda: showinfo(message='Stopping backup')
        btn = ttk.Button(
            master=status_frm, 
            text='Stop', 
            image='stop-backup-dark', 
            compound=tk.LEFT, 
            command=_func, 
            bootstyle='link'
        )
        btn.grid(row=6, column=0, columnspan=2, sticky=tk.W)

        ## section separator
        sep = ttk.Separator(status_frm, bootstyle='secondary')
        sep.grid(row=7, column=0, columnspan=2, pady=10, sticky=tk.EW)

        # current file message
        lbl = ttk.Label(status_frm, textvariable='current-file-msg')
        lbl.grid(row=8, column=0, columnspan=2, pady=2, sticky=tk.EW)
        self.setvar('current-file-msg', 'Uploading: d:/test/settings.txt')

        # logo
        lbl = ttk.Label(left_panel, image='logo', style='bg.TLabel')
        lbl.pack(side='bottom')

        # ---- right panel
        right_panel = ttk.Frame(self, padding=(2, 1))
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

        ## file input
        browse_frm = ttk.Frame(right_panel)
        browse_frm.pack(side=tk.TOP, fill=tk.X, padx=2, pady=1)
        
        file_entry = ttk.Entry(browse_frm, textvariable='folder-path')
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        
        btn = ttk.Button(
            master=browse_frm, 
            image='opened-folder', 
            bootstyle=('link', 'secondary'),
            command=self.get_directory
        )
        btn.pack(side=tk.RIGHT)

        ## Treeview
        tv = ttk.Treeview(right_panel, show='headings')
        tv.configure(columns=(
            'name', 'state', 'last-modified', 
            'last-run-time', 'size'
        ))
        tv.column('name', width=150, stretch=True)
        
        # for col in ['last-modified', 'last-run-time', 'size']:
        #     tv.column(col, stretch=False)
        
        # for col in tv['columns']:
        #     tv.heading(col, text=col.title(), anchor=tk.W)
        
        tv.pack(fill=tk.X, pady=1)

        ## scrolling text output
        scroll_cf = CollapsingFrame(right_panel)
        scroll_cf.pack(fill=tk.BOTH, expand=tk.YES)
        
        output_container = ttk.Frame(scroll_cf, padding=1)
        _value = 'Log: Backing up... [Uploading file: D:/sample_file_35.txt]'
        self.setvar('scroll-message', _value)
        st = ScrolledText(output_container)
        st.pack(fill=tk.BOTH, expand=tk.YES)
        scroll_cf.add(output_container, textvariable='scroll-message')

        # ----- seed with some sample data ----------------------------

        ## starting sample directory
        file_entry.insert('end', 'D:/text/myfiles/top-secret/samples/')

        ## treeview and backup logs
        for x in range(20, 35):
            result = choices(['Backup Up', 'Missed in Destination'])[0]
            st.insert('end', f'19:34:{x}\t\t Uploading: D:/file_{x}.txt\n')
            st.insert('end', f'19:34:{x}\t\t Upload {result}.\n')
            timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            tv.insert('', 'end', x, 
                      values=(f'sample_file_{x}.txt', 
                              result, timestamp, timestamp, 
                              f'{int(x // 3)} MB')
            )
        tv.selection_set(20)

    def get_directory(self):
        """Open dialogue to get directory and update variable"""
        self.update_idletasks()
        d = askdirectory()
        if d:
            self.setvar('folder-path', d)


class CollapsingFrame(ttk.Frame):
    """
    A collapsible frame widget that opens and closes with a click.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        _path = Path(__file__).parent / 'assets'
        self.images = [
            tk.PhotoImage(
                name='open', 
                file=_path / 'icons8_double_up_24px.png'
            ),
            tk.PhotoImage(
                name='closed', 
                file=_path / 'icons8_double_right_24px.png'
            )
        ]
    
    def add(self, child, title="", bootstyle='primary', **kwargs):
        """Add a child to the collapsible frame
        
        Parameters
        ----------
        child : Frame
            The child frame to add to the widget
        
        title : title
            The title appearing on the collapsible section header
        
        bootstyle : str
            The style to apply to the collapsible section header
        """
        if child.winfo_class() != 'TFrame':
            return
        style_color = utility.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=tk.EW)

        # header title
        lbl = ttk.Label(
            master=frm, 
            text=title, 
            bootstyle=(style_color, 'inverse')
        )
        
        if kwargs.get('textvariable'):
            lbl.configure(textvariable=kwargs.get('textvariable'))
        
        lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES, padx=(10, 0))

        # header toggle button
        _func = lambda c=child: self._toggle_open_close(child)
        btn = ttk.Button(
            master=frm, 
            image='open', 
            bootstyle=style_color, 
            command=_func
        )
        btn.pack(side=tk.RIGHT)

        # assign toggle button to child so that it's accesible when 
        # toggling (need to change image)
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky='news')

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button image 
        accordingly

        Parameters
        ----------
        child : Frame
            The child element to add or remove from grid manager
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image='closed')
        else:
            child.grid()
            child.btn.configure(image='open')


if __name__ == '__main__':
    Application().mainloop()
