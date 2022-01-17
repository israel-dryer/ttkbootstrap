import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog


app = ttk.Window()

cd = ColorChooserDialog(app)
cd.show()

app.mainloop()