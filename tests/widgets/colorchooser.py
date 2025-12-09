import ttkbootstrap as ttk
from ttkbootstrap.dialogs import ColorChooserDialog

app = ttk.Window(theme="dark")

cd = ColorChooserDialog(app, initial_color='#adadad')
cd.on_dialog_result(print)

ttk.Button(app, text="Show Dialog", command=cd.show).pack()
app.mainloop()
