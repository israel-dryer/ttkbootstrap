# https://dribbble.com/shots/1237618--Gif-Spinner
from pathlib import Path
from itertools import cycle
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageSequence
from ttkbootstrap.style import utility
utility.enable_high_dpi_awareness()

class AnimatedGif(tk.Tk):

    def __init__(self):
        super().__init__()
        
        self.geometry('400x300')

        # remove the window decorations, titlebar, etc...
        self.overrideredirect(True)

        # center the window in the center of the screen
        self.eval('tk::PlaceWindow . center')

        # bind the escape key to exit the application
        self.bind('<Escape>', lambda _: self.quit())

        # open the GIF and create a cycle iterator
        file_path = Path(__file__).parent / 'images/spinners.gif'
        with Image.open(file_path) as im:
            # create a sequence
            sequence = ImageSequence.Iterator(im)
            images = [ImageTk.PhotoImage(s) for s in sequence]
            self.image_cycle = cycle(images)

            # length of each frame
            self.framerate = im.info['duration']

        self.img_container = ttk.Label(self, image=next(self.image_cycle))
        self.img_container.pack(fill='both', expand='yes')
        self.after(self.framerate, self.next_frame)

    def next_frame(self):
        """Update the image for each frame"""
        self.img_container.configure(image=next(self.image_cycle))
        self.after(self.framerate, self.next_frame)


if __name__ == '__main__':
    AnimatedGif().mainloop()
