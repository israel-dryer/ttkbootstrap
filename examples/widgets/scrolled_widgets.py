import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledText

app = ttk.Window()

st = ScrolledText(app, padding=5, height=10, autohide=True)
st.text.configure(padx=8, pady=8)
st.pack(fill=BOTH, expand=YES)
st.insert(END, 'Insert your text here.')
# st.text.configure(state=DISABLED)

app.mainloop()

# app = ttk.Window()

# sf = ScrolledFrame(app, autohide=True)
# sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

# for x in range(20):
#     ttk.Checkbutton(sf, text=f"Checkbutton {x}").pack(anchor=W)

# app.mainloop()
