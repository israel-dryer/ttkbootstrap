from theme import Theme, Colors, ttk

# TODO the fg needs to be the same color as the main font folor
# TODO the input-fg needs to be a % lighter than the fg color
# TODO consider adding an input background color... which may always be white?

class Style(ttk.Style):
    def __init__(self):
        super().__init__()
        Theme(self, *FLATLY)
        Theme(self, *MINTY)
        Theme(self, *LITERA)
        Theme(self, *COSMO)
        Theme(self, *LUMEN)
        Theme(self, *SIMPLEX)


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
          ), 'Roboto')

MINTY = ('minty',
          Colors(
              primary='#78c2ad',
              secondary='#f3969a',
              success='#56cc9d',
              info='#6cc3d5',
              warning='#ffce67',
              danger='#ff7851',
              bg='#ffffff',
              fg='#888888',
              selectbg='#6cc3d5',
              selectfg='#ffffff',
              light='#f8f9fa',
              dark='#888888',
              active='#dadada',
              border='#ced4da'
          ), 'Roboto')

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
          ), 'Roboto')

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
          ), 'Roboto')

LUMEN = ('lumen',
          Colors(
              primary='#158cba',
              secondary='#e3e3e3',
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
          ), 'Roboto')

SIMPLEX = ('simplex',
          Colors(
              primary='#d7220e',
              secondary='#f8f8f8',
              success='#459307',
              info='#0282ae',
              warning='#cd7c1d',
              danger='#9a469e',
              bg='#fcfcfc',
              fg='#212529',
              selectbg='#0282ae',
              selectfg='#ffffff',
              light='#ffffff',
              dark='#cccccc',
              active='#d8d8d8',
              border='#bbbbbb'
          ), 'Roboto')