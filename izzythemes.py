from theme import Theme, Colors, ttk


class Style(ttk.Style):
    def __init__(self):
        super().__init__()
        Theme(self, *FLATLY)


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
              dark='#7b8a8b',
              active='#dadada'
          ), 'Roboto')
