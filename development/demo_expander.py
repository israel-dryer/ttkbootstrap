import ttkbootstrap as ttk
from ttkbootstrap import Expander, Label, CheckButton, Entry, Button


app = ttk.Window(theme="darkly")
app.title("Expander Demo")

# Basic expander with add() returning a frame
exp1 = Expander(app, title="Settings", show_border=True)
exp1.pack(fill='x', padx=10, pady=5)

content1 = exp1.add()
CheckButton(content1, text="Enable notifications").pack(anchor='w')
CheckButton(content1, text="Dark mode").pack(anchor='w')
CheckButton(content1, text="Auto-save").pack(anchor='w')

# Expander starting collapsed
exp2 = Expander(app, title="Advanced Options", expanded=False)
exp2.pack(fill='x', padx=10, pady=5)

content2 = exp2.add()
Label(content2, text="Timeout (seconds):").pack(anchor='w')
Entry(content2).pack(fill='x', pady=(0, 5))
Label(content2, text="Max retries:").pack(anchor='w')
Entry(content2).pack(fill='x')

# Expander with icon on the left
exp3 = Expander(app, title="Icon Before", icon_position="before")
exp3.pack(fill='x', padx=10, pady=5)

content3 = exp3.add()
Label(content3, text="The chevron is on the left side.").pack()

# Non-collapsible expander (always expanded, no chevron)
exp4 = Expander(app, title="Always Visible (collapsible=False)", collapsible=False)
exp4.pack(fill='x', padx=10, pady=5)

content4 = exp4.add()
Label(content4, text="This section cannot be collapsed.").pack()

# Toggle event demo
exp5 = Expander(app, title="With Event Callback")
exp5.pack(fill='x', padx=10, pady=5)

content5 = exp5.add()
Label(content5, text="Watch the console for toggle events.").pack()

def on_toggle(event):
    print(f"Toggled! Expanded: {event.data['expanded']}")

exp5.on_toggle(on_toggle)

# Control buttons
control_frame = ttk.Frame(app)
control_frame.pack(fill='x', padx=10, pady=10)

Button(control_frame, text="Expand All", command=lambda: [e.expand() for e in [exp1, exp2, exp3, exp5]]).pack(side='left', padx=5)
Button(control_frame, text="Collapse All", command=lambda: [e.collapse() for e in [exp1, exp2, exp3, exp5]]).pack(side='left', padx=5)

app.mainloop()
