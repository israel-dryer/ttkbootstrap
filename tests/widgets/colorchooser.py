import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog


app = ttk.Window(hdpi=0)

cd = ColorChooserDialog(app)
cd.show()

app.mainloop()