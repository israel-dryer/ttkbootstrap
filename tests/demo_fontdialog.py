"""Test the refactored FontDialog using the new Dialog class."""

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import FontDialog


def demo_fontdialog():
    """Test FontDialog with the new Dialog-based implementation."""
    root = ttk.App(theme="darkly", title="FontDialog Text", size=(400, 300))

    result_label = ttk.Label(
        root,
        text="Click the button to select a font",
        padding=20,
        wraplength=350,
    )
    result_label.pack(pady=20)

    def show_font_dialog():
        """Show the font dialog and display result."""
        dialog = FontDialog(
            title="Select Font",
            master=root,
            default_font="TkDefaultFont",
        )
        dialog.show()

        if dialog.result:
            font_obj = dialog.result
            actual = font_obj.actual()
            result_text = (
                f"Font Selected:\n"
                f"Family: {actual['family']}\n"
                f"Size: {actual['size']}\n"
                f"Weight: {actual['weight']}\n"
                f"Slant: {actual['slant']}\n"
                f"Underline: {actual['underline']}\n"
                f"Overstrike: {actual['overstrike']}"
            )
            result_label.configure(text=result_text, font=font_obj)
        else:
            result_label.configure(text="Font selection cancelled")

    button = ttk.Button(
        root,
        text="Select Font",
        command=show_font_dialog,
        bootstyle="primary",
    )
    button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    demo_fontdialog()