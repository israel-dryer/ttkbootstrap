import ttkbootstrap as ttk

root = ttk.Window()

# Create a labeled scale
scale = ttk.LabeledScale(root, from_=0, to=100)
scale.pack(padx=10, pady=10)

# Access the current value
print(scale.value)

root.mainloop()
