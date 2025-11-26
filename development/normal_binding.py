import tkinter as tk



root = tk.Tk()

btn = tk.Button(root, text='Generate')
btn.bind('<Button-1>', lambda x: print(x))
btn.pack()

root.mainloop()