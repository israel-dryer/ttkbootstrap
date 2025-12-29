import tkinter as tk
from tkinter import ttk, TclError

app = tk.Tk()

style = ttk.Style()
style.theme_use('clam')

focus_state_map = [
    ('background focus', 'blue'),
    ('', '')
]

style.map('TButton', focuscolor=focus_state_map)

def detect_tab_focus(e):

    def set_focus_state():
        widget = app.focus_get()
        print(widget, 'as focus')
        try:
            widget.state(['background'])
        except TclError:
            pass # not supported

    app.after_idle(set_focus_state)

app.bind('<Tab>', detect_tab_focus)

for x in range(5):
    ttk.Button(app, text=f'Button {x}').pack(padx=16, pady=16)

app.bind_all('<FocusOut>', lambda e: e.widget.state(['!background']))

app.mainloop()