"""Test script for enhanced QueryDialog with value_format support."""

from datetime import date
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryBox


def enhanced_query_dialogs(root):
    """Test enhanced query dialogs with value_format."""
    frame = ttk.Labelframe(root, text="Enhanced Query Dialogs", padding=10)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Test basic dialogs (backward compatibility)
    def get_basic_string():
        result = QueryBox.get_string(
            "Enter your name:",
            "Basic String Input",
            "John Doe"
        )
        print(f"Basic string result: {result}")

    def get_basic_integer():
        result = QueryBox.get_integer(
            "Enter your age:",
            "Basic Integer Input",
            value=25,
            minvalue=0,
            maxvalue=120
        )
        print(f"Basic integer result: {result}")

    # Test new formatted dialogs
    def get_formatted_currency():
        result = QueryBox.get_float(
            "Enter price:",
            "Currency Input",
            value=1234.56,
            minvalue=0,
            value_format='$#,##0.00'
        )
        print(f"Currency result: {result}")

    def get_formatted_percentage():
        result = QueryBox.get_float(
            "Enter percentage:",
            "Percentage Input",
            value=85.5,
            minvalue=0,
            maxvalue=100,
            value_format='#,##0.##%'
        )
        print(f"Percentage result: {result}")

    def get_formatted_decimal():
        result = QueryBox.get_float(
            "Enter a decimal number:",
            "Decimal Input",
            value=3.14159,
            value_format='#,##0.####'
        )
        print(f"Decimal result: {result}")

    def get_date_short():
        result = QueryBox.get_string(
            "Enter a date:",
            "Short Date Input",
            value=date.today(),
            datatype=date,
            value_format='shortDate'
        )
        print(f"Short date result: {result}")

    def get_date_long():
        result = QueryBox.get_string(
            "Enter a date:",
            "Long Date Input",
            value=date.today(),
            datatype=date,
            value_format='longDate'
        )
        print(f"Long date result: {result}")

    def get_date_custom():
        result = QueryBox.get_string(
            "Enter a date (ISO format):",
            "Custom Date Input",
            value=date.today(),
            datatype=date,
            value_format='yyyy-MM-dd'
        )
        print(f"Custom date result: {result}")

    # Basic dialogs (backward compatibility)
    ttk.Label(frame, text="Basic Dialogs (Backward Compatible):", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(5, 2))
    basic_frame = ttk.Frame(frame)
    basic_frame.pack(fill="x", pady=5)
    ttk.Button(basic_frame, text="Basic String", command=get_basic_string).pack(side="left", padx=2)
    ttk.Button(basic_frame, text="Basic Integer", command=get_basic_integer).pack(side="left", padx=2)

    ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

    # Formatted numeric dialogs
    ttk.Label(frame, text="Formatted Numeric Dialogs:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(5, 2))
    numeric_frame = ttk.Frame(frame)
    numeric_frame.pack(fill="x", pady=5)
    ttk.Button(numeric_frame, text="Currency ($#,##0.00)", command=get_formatted_currency).pack(side="left", padx=2)
    ttk.Button(numeric_frame, text="Percentage (#,##0.##%)", command=get_formatted_percentage).pack(side="left", padx=2)
    ttk.Button(numeric_frame, text="Decimal (#,##0.####)", command=get_formatted_decimal).pack(side="left", padx=2)

    ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

    # Formatted date dialogs
    ttk.Label(frame, text="Formatted Date Dialogs:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(5, 2))
    date_frame = ttk.Frame(frame)
    date_frame.pack(fill="x", pady=5)
    ttk.Button(date_frame, text="Short Date", command=get_date_short).pack(side="left", padx=2)
    ttk.Button(date_frame, text="Long Date", command=get_date_long).pack(side="left", padx=2)
    ttk.Button(date_frame, text="ISO Date (yyyy-MM-dd)", command=get_date_custom).pack(side="left", padx=2)


if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    root.title("Enhanced QueryDialog Test")
    root.geometry("700x450")

    ttk.Label(
        root,
        text="Test Enhanced QueryDialog with value_format Support",
        font=("Helvetica", 14, "bold")
    ).pack(pady=10)

    enhanced_query_dialogs(root)

    ttk.Label(
        root,
        text="Check console for results. New dialogs use specialized Field widgets!",
        font=("Helvetica", 10, "italic")
    ).pack(pady=10)

    root.mainloop()