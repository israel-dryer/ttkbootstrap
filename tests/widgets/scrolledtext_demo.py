import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import ScrolledText

app = ttk.Window("ScrolledText Demo", themename="flatly", size=(600, 300))

# Create a ScrolledText widget with both scrollbars and autohide
st = ScrolledText(
    app,
    height=10,
    width=60,
    wrap="none",          # Disable wrapping for horizontal scrolling
    autohide=True,
    vbar=True,
    hbar=True,
    color="info",
    variant="round"
)
st.pack(fill=BOTH, expand=YES)

# Insert sample content
for i in range(100):
    st.insert(END, f"Line {i+1}: This is a long line of sample text that should require horizontal scrolling.\n")

app.mainloop()
