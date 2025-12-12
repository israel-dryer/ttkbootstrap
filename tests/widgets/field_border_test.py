"""Visual test to compare field borders across different field types."""

import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.textentry import TextEntry
from ttkbootstrap.widgets.composites.numericentry import NumericEntry
from ttkbootstrap.widgets.composites.spinnerentry import SpinnerEntry

root = ttk.Window()
root.title("Field Border Comparison")
root.geometry("500x400")

ttk.Label(root, text="Field Border Comparison", font=("", 14, "bold")).pack(pady=10)

# TextEntry
te = TextEntry(root, label="TextEntry", value="Sample text", message="This is a text entry")
te.pack(padx=20, pady=10, fill='x')

# NumericEntry
ne = NumericEntry(root, label="NumericEntry", value=42, minvalue=0, maxvalue=100, message="This is a numeric entry")
ne.pack(padx=20, pady=10, fill='x')

# SpinnerEntry with text values
se1 = SpinnerEntry(root, label="SpinnerEntry (Text)", values=['A', 'B', 'C'], value='B', message="This is a spinner with text")
se1.pack(padx=20, pady=10, fill='x')

# SpinnerEntry with numeric range
se2 = SpinnerEntry(root, label="SpinnerEntry (Numeric)", from_=0, to=100, value=50, message="This is a spinner with numbers")
se2.pack(padx=20, pady=10, fill='x')

# Print styling info
print("\n=== Styling Information ===")
print(f"TextEntry field class: {te._field.cget('class')}, bootstyle: {te._field.cget('bootstyle')}")
print(f"NumericEntry field class: {ne._field.cget('class')}, bootstyle: {ne._field.cget('bootstyle')}")
print(f"SpinnerEntry field class: {se1._field.cget('class')}, bootstyle: {se1._field.cget('bootstyle')}")

root.mainloop()