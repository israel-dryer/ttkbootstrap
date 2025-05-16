import unittest
import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import ScrolledFrame

style = Style("flatly")

class TestScrolledFrame(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window during tests


    def tearDown(self):
        self.root.update_idletasks()
        self.root.destroy()

    def test_scrolled_frame_creation(self):
        sf = ScrolledFrame(self.root)
        sf.pack()
        self.assertTrue(sf.container.winfo_exists())
        self.assertTrue(sf.vscroll.winfo_exists())
        self.assertEqual(sf.container.master, self.root)

    def test_autohide_toggle(self):
        sf = ScrolledFrame(self.root, autohide=True)
        self.assertTrue(sf.autohide)
        sf.autohide_scrollbar()
        self.assertFalse(sf.autohide)

    def test_scrolling_behavior(self):
        sf = ScrolledFrame(self.root, height=100, scrollheight=500)
        sf.pack()

        # Add enough widgets to exceed the visible area
        for i in range(30):
            tk.Label(sf, text=f"Item {i}").pack()

        self.root.update_idletasks()  # Force layout update
        sf.yview_moveto(0.5)
        first, last = sf.vscroll.get()

        self.assertGreater(first, 0)
        self.assertLess(last, 1)

    def test_geometry_methods_delegate(self):
        sf = ScrolledFrame(self.root)
        sf.pack()
        # Should still have access to content_place and pack
        self.assertTrue(hasattr(sf, "content_place"))
        self.assertTrue(hasattr(sf, "pack"))


if __name__ == "__main__":
    unittest.main()
