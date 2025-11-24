import ttkbootstrap as ttk

root = ttk.Window()

# Create labeled scales with different compounds
scale1 = ttk.LabeledScale(root, minvalue=0, maxvalue=100, compound='before')
scale1.pack(padx=10, pady=10, fill='x')

scale2 = ttk.LabeledScale(root, minvalue=0, maxvalue=100, compound='after')
scale2.pack(padx=10, pady=10, fill='x')

# Access the current value
print("Scale 1 value:", scale1.value)
print("Scale 2 value:", scale2.value)

root.mainloop()