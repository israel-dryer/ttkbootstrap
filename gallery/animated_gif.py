# https://dribbble.com/shots/1237618--Gif-Spinner
from pathlib import Path
from itertools import cycle
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageSequence


class AnimatedGif(ttk.Toplevel):

    def __init__(self):
        super().__init__(
            title="Animated GIF", 
            width=400, 
            height=300, 
            overrideredirect=True,
        )
        self.withdraw()
        self.position_center()

        # bind the escape key to exit the application
        self.bind('<Escape>', lambda _: self.destroy())

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
    
    app = ttk.Window('Animated GIF Demo', themename="superhero")

    btn = ttk.Button(app, text="Play GIF", command=lambda:AnimatedGif())
    btn.pack(padx=20, pady=20)

    app.mainloop()

