import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.notebook import Notebook
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.label import Label

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Notebook Test")

    Style("journal")  # Try "minty", "superhero", etc.

    nb = Notebook(root, color="primary", padding=10)
    nb.pack(fill="both", expand=True, padx=20, pady=20)

    tab1 = Frame(nb, padding=10)
    tab2 = Frame(nb, padding=10)
    tab3 = Frame(nb, padding=10)

    Label(tab1, text="Tab One Content", color="success").pack()
    Label(tab2, text="Tab Two Content", color="info").pack()
    Label(tab3, text="Tab Three Content", color="danger").pack()

    nb.add(tab1, text="Tab 1")
    nb.add(tab2, text="Tab 2")
    nb.add(tab3, text="Tab 3")

    root.mainloop()
