from ttkbootstrap import Style
import tkinter
from tkinter import ttk


def toggle_button():
    """Toggle between start and paused"""
    if running.get():
        pause_timer()
        running.set(False)
        toggle_btn.configure(text='Start', style='info.TButton')
    else:
        start_timer()
        running.set(True)
        toggle_btn.configure(text='Pause', style='info.Outline.TButton')


def start_timer():
    after_id.set(window.after(1, increment_timer))


def pause_timer():
    window.after_cancel(after_id.get())


def increment_timer():
    """Add one second to timer"""
    current = seconds_var.get() + 1
    seconds_var.set(current)
    time_string = '{:02d}:{:02d}:{:02d}'.format((current // 100) // 60, (current // 100) % 60, current % 100)
    timer_var.set(time_string)
    after_id.set(window.after(100, increment_timer))


def reset_timer():
    seconds_var.set(0)
    timer_var.set('00:00:00')


# instantiate the window
style = Style()
window = style.master
window.title('Timer')

# variables
seconds_var = tkinter.IntVar(value=0)
timer_var = tkinter.StringVar(value='00:00:00')
after_id = tkinter.StringVar()
running = tkinter.BooleanVar(value=False)

# timer label
timer_lbl = ttk.Label(window, font='-size 32', anchor='center', textvariable=timer_var)
timer_lbl.pack(side='top', fill='x', padx=60, pady=20)

# control buttons
toggle_btn = ttk.Button(window, text='Start', width=10, style='info.TButton', command=toggle_button)
toggle_btn.pack(side='left', fill='x', expand='yes', padx=10, pady=10)

reset_btn = ttk.Button(window, text='Reset', width=10, style='success.TButton', command=reset_timer)
reset_btn.pack(side='left', fill='x', expand='yes', pady=10)

exit_btn = ttk.Button(window, text='Exit', width=10, style='danger.TButton', command=window.quit)
exit_btn.pack(side='left', fill='x', expand='yes', padx=10, pady=10)

window.mainloop()
