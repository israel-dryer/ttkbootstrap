import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame

app = ttk.Window()

st = ScrolledText(app, padding=20, width=30, height=10, hbar=True, autohide=True)
st.pack(fill=BOTH, expand=YES)

for x in range(25):
    st.insert(END, f'This is a really long line of text... it is {x+1} of 25!\n')

app.mainloop()


# app = ttk.Window()

# sf = ScrolledFrame(app, autohide=True)
# sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

# for x in range(20):
#     ttk.Button(sf, text=f"button {x}").pack(anchor=W)

# app.mainloop()