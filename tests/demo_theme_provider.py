import tkinter as tk

from ttkbootstrap.style.theme_provider import ThemeProvider

tk.Tk()

tp = ThemeProvider.instance()
tp.use('dark')

print('theme', tp)
print('typography', tp.typography)
