import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.treeview import Treeview
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.label import Label


def on_select(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], "values")
        status_label.config(text=f"Selected: {values[0]}, Age: {values[1]}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Treeview Test")

    Style("journal")

    frame = Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    tree = Treeview(
        frame,
        columns=["Name", "Age"],
        show="headings",
        color="info",
        height=5,
        selectmode="browse"
    )
    tree.pack(fill="both", expand=True)

    # Define headings
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.column("Name", width=150)
    tree.column("Age", width=100)

    # Insert rows
    data = [("Alice", 28), ("Bob", 34), ("Cleo", 22), ("Daniel", 45)]
    for name, age in data:
        tree.insert("", "end", values=(name, age))

    tree.bind("<<TreeviewSelect>>", on_select)

    status_label = Label(root, text="Select a row", padding=10)
    status_label.pack()

    root.mainloop()
