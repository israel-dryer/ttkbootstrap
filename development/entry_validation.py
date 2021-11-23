"""
    Simple Entry validation example

    In this example, the entry is validated every time the widget focus is 
    changed using the `focus` validation type. Consult the documentation for 
    more information on options and usage. 
    
    https://tcl.tk/man/tcl8.6/TkCmd/ttk_entry.htm
"""
import tkinter as tk
import ttkbootstrap as ttk

def validate_number(x) -> bool:
    """Validates that the input is a number"""
    if x.isdigit():
        return True
    elif x == "":
        return True
    else:
        return False

def validate_alpha(x) -> bool:
    """Validates that the input is alpha"""
    if x.isdigit():
        return False
    elif x == "":
        return True
    else:
        return True

# create the toplevel window
root = tk.Tk()
style = ttk.Style()

# register the validation callback
digit_func = root.register(validate_number)
alpha_func = root.register(validate_alpha)

# validate numeric entry
ttk.Label(root, text="Enter a number").pack()
num_entry = ttk.Entry(root, validate="focus", validatecommand=(digit_func, '%P'))
num_entry.pack(padx=10, pady=10, expand=True)

# validate alpha entry
ttk.Label(root, text="Enter a letter").pack()
let_entry = ttk.Entry(root, validate="focus", validatecommand=(alpha_func, '%P'))
let_entry.pack(padx=10, pady=10, expand=True)

root.mainloop()