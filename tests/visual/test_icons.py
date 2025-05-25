from ttkbootstrap.window import Window
from ttkbootstrap.icons import Icon
from ttkbootstrap.widgets import Button, CheckBoxToggle, IconButton
from tkinter.ttk import Button as ttkButton
from tkinter import Label

# Use in your GUI
root = Window()

IconButton(root, icon="house").pack(padx=10, pady=10)
IconButton(root, icon="envelope-paper-heart-fill", color="secondary", variant="text").pack(padx=10, pady=10)
Button(root, icon="apple", text="Apple", color="danger", variant="text").pack(padx=10, pady=10)
IconButton(root, icon="apple", color="danger").pack(padx=10, pady=10)
IconButton(root, icon="key", variant="outline").pack(padx=10, pady=10)
IconButton(root, icon="android2", color="success", variant="outline").pack(padx=10, pady=10)

Button(root, text="Button", image=Icon("house", color="orange"), compound="left").pack(padx=10, pady=10)
Button(root, text="Home", icon="house", variant="text").pack(padx=10, pady=10)

CheckBoxToggle(root, text="Verified", icon="fingerprint").pack(padx=10, pady=10)
CheckBoxToggle(root, text="Verified", icon="key").pack(padx=10, pady=10)

Button(root, icon="android2", text="Button", variant="outline").pack(padx=10, pady=10)

root.mainloop()
