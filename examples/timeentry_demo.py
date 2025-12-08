"""TimeEntry widget demonstration.

Demonstrates various configurations of the TimeEntry widget including:
- Different time formats (12-hour, 24-hour)
- Different intervals (15, 30, 60 minutes)
- Time range constraints (business hours)
- Custom format patterns
"""

import datetime

import ttkbootstrap as ttk
from ttkbootstrap import TimeEntry


def main():
    root = ttk.Window()
    root.title("TimeEntry Demo")
    root.geometry("400x550")

    ttk.Label(
        root,
        text="TimeEntry Widget Demo",
        font=("Helvetica", 16, "bold")
    ).pack(pady=10)

    # Example 1: Default 12-hour format with 30-minute intervals
    te1 = TimeEntry(
        root,
        label="Appointment Time",
        message="Select or enter a time"
    )
    te1.pack(padx=20, pady=10, fill='x')

    # Example 2: 24-hour format with 15-minute intervals
    te2 = TimeEntry(
        root,
        label="24-Hour Format",
        value_format='HH:mm',
        interval=15,
        message="15-minute intervals"
    )
    te2.pack(padx=20, pady=10, fill='x')

    # Example 3: Business hours only (9 AM to 5 PM)
    te3 = TimeEntry(
        root,
        label="Business Hours",
        value_format='h:mm a',
        interval=30,
        min_time=datetime.time(9, 0),
        max_time=datetime.time(17, 0),
        message="9 AM to 5 PM only"
    )
    te3.pack(padx=20, pady=10, fill='x')

    # Example 4: Long time format with seconds
    te4 = TimeEntry(
        root,
        label="Long Time Format",
        value_format='longTime',
        interval=60,
        message="With seconds and timezone"
    )
    te4.pack(padx=20, pady=10, fill='x')

    # Show values button
    def show_values():
        print("\n=== TimeEntry Values ===")
        print(f"Appointment Time: {te1.value}")
        print(f"24-Hour Format: {te2.value}")
        print(f"Business Hours: {te3.value}")
        print(f"Long Format: {te4.value}")

    ttk.Button(
        root,
        text="Show Values",
        command=show_values,
        bootstyle="info"
    ).pack(pady=20)

    root.mainloop()


if __name__ == '__main__':
    main()
