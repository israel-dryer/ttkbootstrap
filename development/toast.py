import tkinter as tk

class Toast(tk.Toplevel):
    def __init__(self, master, message, duration=3000, position="bottom-right", **kwargs):
        super().__init__(master, **kwargs)
        self.withdraw()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg="black")

        self.message = message
        self.duration = duration
        self.position = position

        self.label = tk.Label(
            self,
            text=message,
            fg="white",
            bg="black",
            font=("Segoe UI", 10),
            padx=10,
            pady=5
        )
        self.label.pack()

    def show(self):
        self._place_toast(self.position)
        self.after(self.duration, self.destroy)

    def _place_toast(self, position):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        margin = 20

        match position:
            case "bottom-right":
                x = screen_width - width - margin
                y = screen_height - height - margin
            case "bottom-left":
                x = margin
                y = screen_height - height - margin
            case "top-right":
                x = screen_width - width - margin
                y = margin
            case "top-left":
                x = margin
                y = margin
            case "top-center":
                x = (screen_width - width) // 2
                y = margin
            case "bottom-center":
                x = (screen_width - width) // 2
                y = screen_height - height - margin
            case "center":
                x = (screen_width - width) // 2
                y = (screen_height - height) // 2
            case _:
                x = (screen_width - width) // 2
                y = screen_height - height - margin

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()


if __name__ == "__main__":
    root = tk.Tk()  # keep root visible

    toast = Toast(root, "Toast message", position="center")
    toast.show()

    root.mainloop()

