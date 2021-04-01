"""
A simple data entry form that prints the values to the screen when submitted
"""
from ttkbootstrap import Style
from tkinter import ttk
import tkinter

style = Style()
window = style.master
window.title('Simple data entry form')

# add frame in order to add padding on inside of window
frame = ttk.Frame(window, padding=(20, 10))
frame.pack(fill='both', expand='yes')
frame.columnconfigure(2, weight=1)

name = tkinter.StringVar(value='')
address = tkinter.StringVar(value='')
phone = tkinter.StringVar(value='')

# form header
ttk.Label(frame, text='Please enter your contact information', width=60).grid(columnspan=3, pady=10)

# name
ttk.Label(frame, text='Name').grid(row=1, column=0, sticky='ew', pady=10, padx=(0, 10))
ttk.Entry(frame, textvariable=name).grid(row=1, column=1, columnspan=2, sticky='ew')

# address
ttk.Label(frame, text='Address').grid(row=2, column=0, sticky='ew', pady=10, padx=(0, 10))
ttk.Entry(frame, textvariable=address).grid(row=2, column=1, columnspan=2, sticky='ew')

# phone number
ttk.Label(frame, text='Phone').grid(row=3, column=0, pady=10, sticky='ew', padx=(0, 10))
ttk.Entry(frame, textvariable=phone).grid(row=3, column=1, columnspan=2, sticky='ew')

# submit
print_form_data = lambda: print(name.get(), address.get(), phone.get())
submit_btn = ttk.Button(frame, text='Submit', style='success.TButton', command=print_form_data)
submit_btn.grid(row=4, column=0, sticky='ew', pady=10, padx=(0, 10))

# cancel
ttk.Button(frame, text='Cancel', style='danger.TButton', command=window.quit).grid(row=4, column=1, sticky='ew')

window.mainloop()
