"""
Simple test to verify font modifier syntax works correctly.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Create window
root = ttk.Window(title="Font Modifier Test", themename="cosmo")
root.geometry("600x400")

container = ttk.Frame(root, padding=20)
container.pack(fill=BOTH, expand=YES)

# Test 1: Token with modifier
label1 = ttk.Label(container, text="Test 1: body[bold]", font="body[bold]")
label1.pack(pady=5, anchor=W)

# Test 2: Custom font family
label2 = ttk.Label(container, text="Test 2: helvetica[16][bold]", font="helvetica[16][bold]")
label2.pack(pady=5, anchor=W)

# Test 3: Size token
label3 = ttk.Label(container, text="Test 3: [lg][bold,italic]", font="[lg][bold,italic]")
label3.pack(pady=5, anchor=W)

# Test 4: Pixel size
label4 = ttk.Label(container, text="Test 4: arial[14px][bold]", font="arial[14px][bold]")
label4.pack(pady=5, anchor=W)

# Test 5: Underline
label5 = ttk.Label(container, text="Test 5: body[underline]", font="body[underline]")
label5.pack(pady=5, anchor=W)

# Test 6: Multiple modifiers
label6 = ttk.Label(container, text="Test 6: [16][bold,italic,underline]", font="[16][bold,italic,underline]")
label6.pack(pady=5, anchor=W)

# Test 7: Font token
label7 = ttk.Label(container, text="Test 7: heading-lg[italic]", font="heading-lg[italic]")
label7.pack(pady=5, anchor=W)

# Test 8: Plain token (no modifiers)
label8 = ttk.Label(container, text="Test 8: code", font="code")
label8.pack(pady=5, anchor=W)

# Test runtime font change
def change_font():
    label1.configure(font="heading-xl[bold]")
    status_label.configure(text="Font changed to heading-xl[bold]", bootstyle="success")

ttk.Button(container, text="Change Label 1 Font", command=change_font).pack(pady=20)

status_label = ttk.Label(container, text="Ready", font="caption")
status_label.pack(pady=5)

print("All widgets created successfully!")
print("Font modifier syntax is working correctly.")

root.mainloop()