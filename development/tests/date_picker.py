import tkinter as tk
from ttkbootstrap.widgets import DateEntry

root = tk.Tk()

de = DateEntry()
de.pack(padx=10, pady=10)

de.configure(bootstyle='danger')
assert de['bootstyle'] == 'danger'
assert de.button.cget('style') == 'danger.Date.TButton'
assert de.configure('bootstyle') == 'danger'

