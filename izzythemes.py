from theme import Theme, Colors, ttk


class Style(ttk.Style):
    def __init__(self):
        super().__init__()
        self.flatly = Theme(self, *FLATLY)
        self.minty = Theme(self, *MINTY)
        self.litera = Theme(self, *LITERA)
        self.cosmo = Theme(self, *COSMO)
        self.lumen = Theme(self, *LUMEN)
        self.simplex = Theme(self, *SIMPLEX)
        self.sandstone = Theme(self, *SANDSTONE)
        self.yeti = Theme(self, *YETI)
        self.pulse = Theme(self, *PULSE)
        self.united = Theme(self, *UNITED)
        self.journal = Theme(self, *JOURNAL)

        self.darkly = Theme(self, *DARKLY)
        self.superhero = Theme(self, *SUPERHERO)
        self.solar = Theme(self, *SOLAR)
        self.cyborg = Theme(self, *CYBORG)


    def theme_use(self, themename=None):
        """If themename is None, returns the theme in use, otherwise, set
        the current theme to themename, refreshes all widgets and emits
        a <<ThemeChanged>> event."""
        if themename is None:
            # Starting on Tk 8.6, checking this global is no longer needed
            # since it allows doing self.tk.call(self._name, "theme", "use")
            return self.tk.eval("return $ttk::currentTheme")

        # Set the global style settings for non-tk widgets
        theme_obj = self.__dict__.get(themename)
        if theme_obj:
            theme_obj.apply_global_tk_styles()

        # using "ttk::setTheme" instead of "ttk::style theme use" causes
        # the variable currentTheme to be updated, also, ttk::setTheme calls
        # "ttk::style theme use" in order to change theme.
        self.tk.call("ttk::setTheme", themename)


FLATLY = ('flatly',
          Colors(
              primary='#2c3e50',
              secondary='#95a5a6',
              success='#18bc9c',
              info='#3498db',
              warning='#f39c12',
              danger='#e74c3c',
              bg='#ffffff',
              fg='#212529',
              selectbg='#3498db',
              selectfg='#ffffff',
              light='#ecf0f1',
              dark='#212529',
              active='#dadada',
              border='#ced4da',
              inputfg='#7b8a8b'
          ), 'Helvetica')

MINTY = ('minty',
         Colors(
             primary='#78c2ad',
             secondary='#f3969a',
             success='#56cc9d',
             info='#6cc3d5',
             warning='#ffce67',
             danger='#ff7851',
             bg='#ffffff',
             fg='#5a5a5a',
             selectbg='#6cc3d5',
             selectfg='#ffffff',
             light='#f8f9fa',
             dark='#5a5a5a',
             active='#dadada',
             border='#ced4da',
             inputfg='#5a5a5a'
         ), 'Helvetica')

LITERA = ('litera',
          Colors(
              primary='#4582ec',
              secondary='#adb5bd',
              success='#02b875',
              info='#17a2b8',
              warning='#f0ad4e',
              danger='#d9534f',
              bg='#ffffff',
              fg='#343a40',
              selectbg='#17a2b8',
              selectfg='#ffffff',
              light='#f8f9fa',
              dark='#343a40',
              active='#dadada',
              border='#e5e5e5',
              inputfg='#343a40'
          ), 'Helvetica')

COSMO = ('cosmo',
         Colors(
             primary='#2780e3',
             secondary='#373a3c',
             success='#3fb618',
             info='#9954bb',
             warning='#ff7518',
             danger='#ff0039',
             bg='#ffffff',
             fg='#373a3c',
             selectbg='#3fb618',
             selectfg='#ffffff',
             light='#fdfdfe',
             dark='#373a3c',
             active='#dadada',
             border='#ced4da',
             inputfg='#49506a'
         ), 'Helvetica')

LUMEN = ('lumen',
         Colors(
             primary='#158cba',
             secondary='#555555',
             success='#28b62c',
             info='#75caeb',
             warning='#ff851b',
             danger='#ff4136',
             bg='#ffffff',
             fg='#555555',
             selectbg='#75caeb',
             selectfg='#ffffff',
             light='#f6f6f6',
             dark='#555555',
             active='#dadada',
             border='#ced4da',
             inputfg='#555555'
         ), 'Helvetica')

SIMPLEX = ('simplex',
           Colors(
               primary='#d7220e',
               secondary='#373a3c',
               success='#459307',
               info='#0282ae',
               warning='#cd7c1d',
               danger='#9a469e',
               bg='#fcfcfc',
               fg='#212529',
               selectbg='#0282ae',
               selectfg='#ffffff',
               light='#ffffff',
               dark='#212529',
               active='#d8d8d8',
               border='#bbbbbb',
               inputfg='#212529'
           ), 'Helvetica')

SANDSTONE = ('sandstone',
             Colors(
                 primary='#3e3f3a',
                 secondary='#8e8c84',
                 success='#93c54b',
                 info='#29abe0',
                 warning='#f47c3c',
                 danger='#d9534f',
                 bg='#ffffff',
                 fg='#3e3f3a',
                 selectbg='#29abe0',
                 selectfg='#ffffff',
                 light='#fdfcfb',
                 dark='#3e3f3a',
                 active='#d8d8d8',
                 border='#ced4da',
                 inputfg='#3e3f3a'
             ), 'Helvetica')

YETI = ('yeti',
        Colors(
            primary='#008cba',
            secondary='#333333',
            success='#43ac6a',
            info='#5bc0de',
            warning='#e99002',
            danger='#f04124',
            bg='#ffffff',
            fg='#222222',
            selectbg='#5bc0de',
            selectfg='#ffffff',
            light='#eeeeee',
            dark='#222222',
            active='#dadada',
            border='#cccccc',
            inputfg='#222222'
        ), 'Helvetica')

PULSE = ('pulse',
         Colors(
             primary='#593196',
             secondary='#17141f',
             success='#13b955',
             info='#009cdc',
             warning='#efa31d',
             danger='#fc3939',
             bg='#ffffff',
             fg='#444444',
             selectbg='#009cdc',
             selectfg='#ffffff',
             light='#fdfdfe',
             dark='#444444',
             active='#dadada',
             border='#cbc8d0',
             inputfg='#444444'
         ), 'Helvetica')

UNITED = ('united',
         Colors(
             primary='#e95420',
             secondary='#aea79f',
             success='#38b44a',
             info='#17a2b8',
             warning='#efb73e',
             danger='#df382c',
             bg='#ffffff',
             fg='#333333',
             selectbg='#17a2b8',
             selectfg='#ffffff',
             light='#f9fafb',
             dark='#333333',
             active='#dadada',
             border='#ced4da',
             inputfg='#333333'
         ), 'Helvetica')

JOURNAL = ('journal',
         Colors(
             primary='#eb6864',
             secondary='#aaaaaa',
             success='#22b24c',
             info='#336699',
             warning='#f5e625',
             danger='#f57a00',
             bg='#ffffff',
             fg='#222222',
             selectbg='#336699',
             selectfg='#ffffff',
             light='#f9fafb',
             dark='#222222',
             active='#dadada',
             border='#ced4da',
             inputfg='#222222'
         ), 'Helvetica')

DARKLY = ('darkly',
          Colors(
              primary='#375a7f',
              secondary='#444444',
              success='#00bc8c',
              info='#3498db',
              warning='#f39c12',
              danger='#e74c3c',
              bg='#222222',
              fg='#ffffff',
              selectbg='#3498db',
              selectfg='#ffffff',
              light='#adb5bd',
              dark='#ffffff',
              active='#1d1d1d',
              border='#222222',
              inputfg='#444444'
          ), 'Helvetica', 'dark')

SUPERHERO = ('superhero',
          Colors(
              primary='#df691a',
              secondary='#4e5d6c',
              success='#5cb85c',
              info='#5bc0de',
              warning='#f0ad4e',
              danger='#d9534f',
              bg='#2b3e50',
              fg='#ffffff',
              selectbg='#5bc0de',
              selectfg='#ffffff',
              light='#adb5bd',
              dark='#ffffff',
              active='#4a5969',
              border='#222222',
              inputfg='#444444'
          ), 'Helvetica', 'dark')

SOLAR = ('solar',
          Colors(
              primary='#bc951a',
              secondary='#94a2a4',
              success='#44aca4',
              info='#3f98d7',
              warning='#d05e2f',
              danger='#d95092',
              bg='#002b36',
              fg='#ffffff',
              selectbg='#3f98d7',
              selectfg='#ffffff',
              light='#adb5bd',
              dark='#ffffff',
              active='#254a53',
              border='#00252e',
              inputfg='#495063'
          ), 'Helvetica', 'dark')

CYBORG = ('cyborg',
          Colors(
              primary='#2a9fd6',
              secondary='#555555',
              success='#77b300',
              info='#9933cc',
              warning='#ff8800',
              danger='#cc0000',
              bg='#060606',
              fg='#ffffff',
              selectbg='#9933cc',
              selectfg='#ffffff',
              light='#222222',
              dark='#ffffff',
              active='#2a2a2a',
              border='#060606',
              inputfg='#555555'
          ), 'Helvetica', 'dark')