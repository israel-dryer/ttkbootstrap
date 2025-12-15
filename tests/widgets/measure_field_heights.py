"""Measure and compare field heights."""

import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.textentry import TextEntry
from ttkbootstrap.widgets.composites.spinnerentry import SpinnerEntry

root = ttk.Window()
root.title("Field Height Measurement")
root.geometry("400x300")

ttk.Label(root, text="Field Height Comparison", font=("", 14, "bold")).pack(pady=10)

# TextEntry
text_entry = TextEntry(root, label="TextEntry", value="Sample text", message="Regular text field")
text_entry.pack(padx=20, pady=10, fill='x')

# SpinnerEntry
spinner_entry = SpinnerEntry(root, label="SpinnerEntry", values=['A', 'B', 'C'], value='B', message="Spinner field")
spinner_entry.pack(padx=20, pady=10, fill='x')

def measure_heights():
    """Measure heights after widgets are rendered."""
    print("\n=== Field Height Measurements ===")

    # Overall widget heights
    text_height = text_entry.winfo_height()
    spinner_height = spinner_entry.winfo_height()

    print(f"TextEntry total height: {text_height}px")
    print(f"SpinnerEntry total height: {spinner_height}px")
    print(f"Difference: {abs(text_height - spinner_height)}px")

    # Field container heights (the bordered frame)
    text_field_height = text_entry._field.winfo_height()
    spinner_field_height = spinner_entry._field.winfo_height()

    print(f"\nTextEntry field container height: {text_field_height}px")
    print(f"SpinnerEntry field container height: {spinner_field_height}px")
    print(f"Difference: {abs(text_field_height - spinner_field_height)}px")

    # Entry widget heights
    text_entry_widget_height = text_entry.entry_widget.winfo_height()
    spinner_entry_widget_height = spinner_entry.entry_widget.winfo_height()

    print(f"\nTextEntry entry widget height: {text_entry_widget_height}px")
    print(f"SpinnerEntry entry widget height: {spinner_entry_widget_height}px")
    print(f"Difference: {abs(text_entry_widget_height - spinner_entry_widget_height)}px")

    if text_height == spinner_height:
        print("\n✓ Heights are identical!")
    else:
        print(f"\n✗ Heights differ by {abs(text_height - spinner_height)}px")

    if text_field_height == spinner_field_height:
        print("✓ Field container heights are identical!")
    else:
        print(f"✗ Field container heights differ by {abs(text_field_height - spinner_field_height)}px")

# Measure after window is fully rendered
root.after(100, measure_heights)

root.mainloop()