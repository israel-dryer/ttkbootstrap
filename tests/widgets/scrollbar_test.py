import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets.scrollbar import Scrollbar
from ttkbootstrap.widgets.frame import Frame


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollbar Test")

    Style("minty")

    # Container frame
    frame = Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    # Create Text widget
    text = tk.Text(frame, wrap="none", width=50, height=10)
    text.grid(row=0, column=0, sticky="nsew")

    # Populate with sample content
    for i in range(50):
        text.insert("end", f"Line {i + 1}: Hello, world!\n")

    # Vertical scrollbar
    vscroll = Scrollbar(
        frame,
        orient="vertical",
        command=text.yview,
        color="primary",
        variant="round"
    )
    vscroll.grid(row=0, column=1, sticky="ns")
    text.config(yscrollcommand=vscroll.set)

    # Horizontal scrollbar
    hscroll = Scrollbar(
        frame,
        orient="horizontal",
        command=text.xview,
        color="secondary",
        variant="default"
    )
    hscroll.grid(row=1, column=0, sticky="ew")
    text.config(xscrollcommand=hscroll.set)

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    root.mainloop()
