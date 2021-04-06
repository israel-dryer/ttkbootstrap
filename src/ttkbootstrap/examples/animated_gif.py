import tkinter
from itertools import cycle
from tkinter import ttk

from PIL import Image, ImageTk, ImageSequence


class AnimatedGif(tkinter.Tk):

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
        with Image.open('images/spinners.gif') as im:
            # create a sequence
            sequence = ImageSequence.Iterator(im)

            # use the cycle iterator to convert each frame to a tk photoimage
            self.image_cycle = cycle([ImageTk.PhotoImage(s) for s in sequence])

            # length of each frame
            self.framerate = im.info['duration']

        self.image_container = ttk.Label(self, image=next(self.image_cycle))
        self.image_container.pack(fill='both', expand='yes')
        self.after(self.framerate, self.next_frame)

    def next_frame(self):
        """Update the image for each frame"""
        self.image_container.configure(image=next(self.image_cycle))
        self.after(self.framerate, self.next_frame)


if __name__ == '__main__':
    Animation().mainloop()
