"""Demo for Accordion widget."""
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites import Accordion
from ttkbootstrap.widgets.primitives import Label, Button

app = ttk.App(title="Accordion Demo", size=(400, 500), theme="dark")

# Basic accordion (single selection, collapsible)
Label(app, text="Basic Accordion (single selection)", font='heading').pack(pady=(10, 5))

accordion1 = Accordion(app, separators=True, show_border=True)
accordion1.pack(fill='x', padx=10, pady=5)

section1 = accordion1.add(title="Section 1", icon={'name': 'house', 'size': 16})
Label(section1.content, text="Content for section 1").pack(pady=10)

section2 = accordion1.add(title="Section 2", icon={'name': 'gear', 'size': 16})
Label(section2.content, text="Content for section 2").pack(pady=10)

section3 = accordion1.add(title="Section 3", icon={'name': 'info-circle', 'size': 16})
Label(section3.content, text="Content for section 3").pack(pady=10)

# Multiple selection accordion
Label(app, text="Multiple Selection Accordion", font='heading').pack(pady=(20, 5))

accordion2 = Accordion(app, multiple=True, bootstyle='success-solid')
accordion2.pack(fill='x', padx=10, pady=5)

s1 = accordion2.add(title="Option A", expanded=True)
Label(s1.content, text="Option A is selected").pack(pady=10)

s2 = accordion2.add(title="Option B", expanded=True)
Label(s2.content, text="Option B is also selected").pack(pady=10)

s3 = accordion2.add(title="Option C")
Label(s3.content, text="Option C content").pack(pady=10)

# Non-collapsible accordion (at least one must be open)
Label(app, text="Non-collapsible (one must stay open)", font='heading').pack(pady=(20, 5))

accordion3 = Accordion(app, collapsible=False, bootstyle='warning-solid')
accordion3.pack(fill='x', padx=10, pady=5)

p1 = accordion3.add(title="Panel 1")
Label(p1.content, text="Panel 1 - try to collapse all!").pack(pady=10)

p2 = accordion3.add(title="Panel 2")
Label(p2.content, text="Panel 2 content").pack(pady=10)

# Event handling
def on_change(event):
    expanded = event.data.get('expanded', [])
    titles = [exp.cget('title') for exp in expanded]
    print(f"Expanded sections: {titles}")

accordion1.on_change(on_change)

app.mainloop()