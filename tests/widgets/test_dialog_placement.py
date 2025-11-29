import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageBox

window = ttk.Window()

window.title("$Shopkeeper")
window.geometry("800x600")
window.resizable(False, False)
window.place_window_center()

window.update_idletasks()

def confirm_shutdown():
    x0 = window.winfo_rootx()
    y0 = window.winfo_rooty()

    w = window.winfo_rootx()
    h = window.winfo_rooty()

    # coordinates
    x = x0 + w // 6
    y = y0 + h // 6

    if MessageBox.yesno("Message text here", "Confirm", parent=window) == "Yes":
        print("Confirmed")
    else:
        print("Not confirmed")

ttk.Button(window, text="Confirm", command=confirm_shutdown).pack(padx=15, pady=16)

window.mainloop()

