"""Test the refactored DateDialog using the new Dialog class."""

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import DateDialog
from datetime import date


def demo_datedialog():
    """Test DateDialog with the new Dialog-based implementation."""
    root = ttk.Window()
    root.title("DateDialog Test")
    root.geometry("600x400")

    result_label = ttk.Label(
        root,
        text="Click the button to select a date",
        padding=20,
        wraplength=450,
    )
    result_label.pack(pady=20)

    def show_date_dialog():
        """Show the date dialog and display result."""
        dialog = DateDialog(
            master=root,
            title="Select a Date",
            first_weekday=6,  # Sunday
            initial_date=date.today()
        )
        dialog.on_result(lambda d: print(f"DialogResult: {d}"))
        dialog.show()

        if dialog.result:
            result_text = (
                f"Date Selected:\n"
                f"{dialog.result.strftime('%A, %B %d, %Y')}"
            )
            result_label.configure(text=result_text)
        else:
            result_label.configure(text="Date selection cancelled")

    button = ttk.Button(
        root,
        text="Select Date",
        command=show_date_dialog,
        bootstyle="primary",
    )
    button.pack(pady=10)

    info_label = ttk.Label(
        root,
        text=(
            "Features:\n"
            "• Left-click arrows: Navigate by month\n"
            "• Right-click arrows: Navigate by year\n"
            "• Click title: Reset to start date\n"
            "• Chevron icons instead of text"
        ),
        padding=20,
        justify="left",
        bootstyle="secondary",
    )
    info_label.pack(pady=10, padx=20, fill="x")

    root.mainloop()


if __name__ == "__main__":
    demo_datedialog()
