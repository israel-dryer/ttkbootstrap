import tkinter as tk
from datetime import datetime
from ttkbootstrap import Style
from ttkbootstrap.widgets.dateentry import DateEntry


def test_dateentry():
    root = tk.Tk()
    root.title("DateEntry Test")
    root.geometry("300x150")

    Style("flatly")

    def on_date_selected(event):
        selected = entry.entry.get()
        print("Selected date:", selected)
        label.config(text=f"Selected: {selected}")

    entry = DateEntry(
        root,
        startdate=datetime(2023, 12, 25),
        color="success",
        dateformat="%Y-%m-%d",
        popuptitle="Choose a date",
    )
    entry.pack(padx=20, pady=10, fill="x")
    entry.bind("<<DateEntrySelected>>", on_date_selected)

    label = tk.Label(root, text="Pick a date", anchor="center")
    label.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    test_dateentry()
