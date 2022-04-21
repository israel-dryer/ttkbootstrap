import ttkbootstrap as ttk
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog


app = ttk.Window()

cd = ColorChooserDialog(app, initialcolor='#adadad')
cd.show()

app.mainloop()