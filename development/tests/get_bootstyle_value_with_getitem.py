import tkinter as tk
import ttkbootstrap as ttk

"""
    Test that the `Widget.configure` method is able to change the widget
    style via the `bootstyle` parameter.
"""

root = tk.Tk()
style = ttk.Style()
colors = style.theme.colors

btn = ttk.Button(root, text="Push Button", bootstyle='outline-danger')
btn.pack(padx=10, pady=10)

ttkstyle = btn['style']
assert ttkstyle == 'danger.Outline.TButton'
