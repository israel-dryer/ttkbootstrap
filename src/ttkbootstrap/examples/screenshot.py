from ttkbootstrap import Style
from tkinter import ttk

# --------------------------ONLY FOR SCREENSHOTS------------------------
import pathlib
from PIL import ImageGrab


def get_bounding_box(event):
    """
    Take a screenshot of the current demo window and save to images
    """
    # bounding box
    titlebar = 31
    x1 = window.winfo_rootx() - 1
    y1 = window.winfo_rooty() - titlebar
    x2 = x1 + window.winfo_width() + 2
    y2 = y1 + window.winfo_height() + titlebar + 1

    window.after_idle(save_screenshot, [x1, y1, x2, y2])


def save_screenshot(bbox):
    # screenshot
    img = ImageGrab.grab(bbox=bbox)

    # image name
    filename = 'images/' + pathlib.Path(__file__).stem + '.png'
    img.save(filename, 'png')

    # --------------------------ONLY FOR SCREENSHOTS------------------------

style = Style()
window = style.master
ttk.Label(window, text='Hello world!', font='-size 40').pack()
# use the code below in other programs to take snapshots
window.bind("<Insert>", get_bounding_box)  # only for grabbing screenshots
window.mainloop()