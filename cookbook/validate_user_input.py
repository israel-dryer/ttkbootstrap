import ttkbootstrap as ttk
from ttkbootstrap.constants import *

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
root = ttk.Window()
frame = ttk.Frame(root, padding=10)
frame.pack(fill=BOTH, expand=YES)

# register the validation callback
digit_func = root.register(validate_number)
alpha_func = root.register(validate_alpha)

# validate numeric entry
ttk.Label(frame, text="Enter a number").pack()
num_entry = ttk.Entry(frame, validate="focus", validatecommand=(digit_func, '%P'))
num_entry.pack(padx=10, pady=10, expand=True)

# validate alpha entry
ttk.Label(frame, text="Enter a letter").pack()
let_entry = ttk.Entry(frame, validate="focus", validatecommand=(alpha_func, '%P'))
let_entry.pack(padx=10, pady=10, expand=True)

root.mainloop()