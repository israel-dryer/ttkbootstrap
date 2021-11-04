import pathlib

from PIL import ImageGrab


class Screenshot:

    def __init__(self, parent, filename):
        self.parent = parent
        self.parent.bind("<Insert>", self.get_bounding_box)
        self.filename = filename

    def get_bounding_box(self, event):
        """
        Take a screenshot of the current demo window and save to images
        """
        # bounding box
        titlebar = 31
        x1 = self.parent.winfo_rootx() - 1
        y1 = self.parent.winfo_rooty() - titlebar
        x2 = x1 + self.parent.winfo_width() + 2
        y2 = y1 + self.parent.winfo_height() + titlebar + 1
        self.parent.after_idle(self.save_screenshot, [x1, y1, x2, y2])

    def save_screenshot(self, bbox):
        # screenshot
        img = ImageGrab.grab(bbox=bbox)

        # image name
        img.save(self.filename, 'png')
        print(self.filename)
