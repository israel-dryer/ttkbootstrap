import ttkbootstrap as ttk
from ttkbootstrap import DropdownButton

app = ttk.Window(theme="darkly")

# DropdownButton uses ContextMenu internally
dropdown = DropdownButton(app, text="Actions")
dropdown.add_command(text="New File", command=lambda: print("New File"))
dropdown.add_command(text="Open File", command=lambda: print("Open File"))
dropdown.add_command(text="Save", command=lambda: print("Save"))
dropdown.add_separator()
dropdown.add_command(text="Cut", command=lambda: print("Cut"))
dropdown.add_command(text="Copy", command=lambda: print("Copy"))
dropdown.add_command(text="Paste", command=lambda: print("Paste"))
dropdown.add_separator()
dropdown.add_command(text="Exit", command=app.quit)

dropdown.pack(padx=20, pady=20)

ttk.Label(app, text="Click button or press Enter, then:\n- Arrow Up/Down to navigate\n- Enter to select\n- Escape to close").pack(padx=20, pady=10)

app.mainloop()
