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
              fg='#2c3e50',
              selectbg='#3498db',
              selectfg='#ffffff',
              light='#ecf0f1',
              dark='#888888',
              active='#dadada',
              border='#ced4da'
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
             border='#ced4da'
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
              border='#e5e5e5'
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
             fg='#c7c8c8',
             selectbg='#3fb618',
             selectfg='#ffffff',
             light='#fdfdfe',
             dark='#c7c8c8',
             active='#dadada',
             border='#ced4da'
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
             border='#ced4da'
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
               border='#bbbbbb'
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
               border='#ced4da'
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
               border='#cccccc'
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
               border='#cbc8d0'
           ), 'Helvetica')

