"""Demo script for NumberEntryPart widget.

This script demonstrates the various features of the NumberEntryPart widget
including numeric constraints, stepping, wrapping, and formatting.
"""
import ttkbootstrap as ttk
from ttkbootstrap.widgets.parts.numberentry_part import NumberEntryPart


def create_demo():
    """Create the demo window with various NumberEntryPart examples."""
    root = ttk.Window(theme="darkly", title="NumberEntryPart Demo")

    # Title
    ttk.Label(
        root,
        text="NumberEntryPart Widget Demo",
        font=('Helvetica', 16, 'bold')
    ).pack(pady=(10, 5), padx=10)

    instructions = """
Try these features:
- Type numbers and press Enter or Tab
- Use Up/Down arrow keys to step through values
- Use mouse wheel to increment/decrement
- Try exceeding min/max bounds (values are clamped or wrapped)
- Try the wrapping entry (values cycle from max back to min)
"""

    ttk.Label(
        root,
        text=instructions,
        justify='left',
        font=('Courier', 9)
    ).pack(pady=(0, 10), padx=10, anchor='w')

    ttk.Separator(root).pack(fill='x', pady=5)

    # Example 1: Basic integer entry with default bounds (0-100)
    frame1 = ttk.Frame(root, padding=10)
    frame1.pack(fill='x', padx=10, pady=5)

    ttk.Label(
        frame1,
        text="1. Integer (0-100, step=1):",
        width=30,
        anchor='w'
    ).pack(side='left')

    entry1 = NumberEntryPart(
        frame1,
        value=50,
        minvalue=0,
        maxvalue=100,
        increment=1,
        width=20
    )
    entry1.pack(side='left', padx=5)

    label1 = ttk.Label(frame1, text="Value: 50", width=20)
    label1.pack(side='left', padx=5)

    def on_change1(event):
        label1.config(text=f"Value: {event.data['value']}")

    entry1.on_changed(on_change1)

    # Example 2: Decimal entry with custom format
    frame2 = ttk.Frame(root, padding=10)
    frame2.pack(fill='x', padx=10, pady=5)

    ttk.Label(
        frame2,
        text="2. Decimal (0.0-10.0, step=0.1):",
        width=30,
        anchor='w'
    ).pack(side='left')

    entry2 = NumberEntryPart(
        frame2,
        value=5354,
        minvalue=0.0,
        maxvalue=500120.0,
        increment=10,
        value_format='$#,##0',
        width=20
    )
    entry2.pack(side='left', padx=5)

    label2 = ttk.Label(frame2, text="Value: 3.14", width=20)
    label2.pack(side='left', padx=5)

    def on_change2(event):
        label2.config(text=f"Value: {event.data['value']}")

    entry2.on_changed(on_change2)

    # Example 3: Percentage entry
    frame3 = ttk.Frame(root, padding=10)
    frame3.pack(fill='x', padx=10, pady=5)

    ttk.Label(
        frame3,
        text="3. Percentage (0-100%, step=5):",
        width=30,
        anchor='w'
    ).pack(side='left')

    entry3 = NumberEntryPart(
        frame3,
        value=50,
        minvalue=0,
        maxvalue=100,
        increment=5,
        value_format='#,##0',
        width=20
    )
    entry3.pack(side='left', padx=5)

    label3 = ttk.Label(frame3, text="Value: 50%", width=20)
    label3.pack(side='left', padx=5)

    def on_change3(event):
        label3.config(text=f"Value: {event.data['value']}%")

    entry3.on_changed(on_change3)

    # Example 4: Large step increment
    frame4 = ttk.Frame(root, padding=10)
    frame4.pack(fill='x', padx=10, pady=5)

    ttk.Label(
        frame4,
        text="4. Large step (0-1000, step=50):",
        width=30,
        anchor='w'
    ).pack(side='left')

    entry4 = NumberEntryPart(
        frame4,
        value=500,
        minvalue=0,
        maxvalue=1000,
        increment=50,
        value_format='#,##0',
        width=20
    )
    entry4.pack(side='left', padx=5)

    label4 = ttk.Label(frame4, text="Value: 500", width=20)
    label4.pack(side='left', padx=5)

    def on_change4(event):
        label4.config(text=f"Value: {event.data['value']}")

    entry4.on_changed(on_change4)

    # Example 5: Wrapping entry (like a clock hour selector)
    frame5 = ttk.Frame(root, padding=10)
    frame5.pack(fill='x', padx=10, pady=5)

    ttk.Label(
        frame5,
        text="5. Wrapping (0-23 hours, wraps):",
        width=30,
        anchor='w'
    ).pack(side='left')

    entry5 = NumberEntryPart(
        frame5,
        value=12,
        minvalue=0,
        maxvalue=23,
        increment=1,
        wrap=True,
        width=20
    )
    entry5.pack(side='left', padx=5)

    label5 = ttk.Label(frame5, text="Value: 12", width=20)
    label5.pack(side='left', padx=5)

    def on_change5(event):
        label5.config(text=f"Value: {event.data['value']}")

    entry5.on_changed(on_change5)

    # Example 6: Negative range
    frame6 = ttk.Frame(root, padding=10)
    frame6.pack(fill='x', padx=10, pady=5)

    ttk.Label(
        frame6,
        text="6. Negative range (-100 to 100):",
        width=30,
        anchor='w'
    ).pack(side='left')

    entry6 = NumberEntryPart(
        frame6,
        value=0,
        minvalue=-100,
        maxvalue=100,
        increment=10,
        value_format='#,##0',
        width=20
    )
    entry6.pack(side='left', padx=5)

    label6 = ttk.Label(frame6, text="Value: 0", width=20)
    label6.pack(side='left', padx=5)

    def on_change6(event):
        label6.config(text=f"Value: {event.data['value']}")

    entry6.on_changed(on_change6)

    ttk.Separator(root).pack(fill='x', pady=10)

    # Event log
    ttk.Label(
        root,
        text="Event Log:",
        font=('Helvetica', 11, 'bold')
    ).pack(padx=10, anchor='w')

    log_frame = ttk.Frame(root)
    log_frame.pack(fill='both', expand=True, padx=10, pady=(5, 10))

    log_text = ttk.Text(log_frame, height=8, width=60)
    log_text.pack(side='left', fill='both', expand=True)

    scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=log_text.yview)
    scrollbar.pack(side='right', fill='y')
    log_text.config(yscrollcommand=scrollbar.set)

    def log_event(entry_name, event_type, event):
        """Log events to the text widget."""
        value = event.data.get('value', 'N/A')
        log_text.insert('end', f"{entry_name} - {event_type}: {value}\n")
        log_text.see('end')

    # Attach increment/decrement loggers
    entry1.on_increment(lambda e: log_event("Entry 1", "INCREMENT", e))
    entry1.on_decrement(lambda e: log_event("Entry 1", "DECREMENT", e))

    entry5.on_increment(lambda e: log_event("Entry 5 (wrap)", "INCREMENT", e))
    entry5.on_decrement(lambda e: log_event("Entry 5 (wrap)", "DECREMENT", e))

    print("=" * 60)
    print("NumberEntryPart Demo")
    print("=" * 60)
    print("Try the different number entries:")
    print("- Use Up/Down arrow keys")
    print("- Use mouse wheel")
    print("- Type values and press Enter")
    print("=" * 60)

    root.mainloop()


if __name__ == '__main__':
    create_demo()