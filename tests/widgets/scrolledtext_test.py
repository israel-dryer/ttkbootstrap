import unittest
import tkinter as tk
from ttkbootstrap import Window
from ttkbootstrap.widgets import ScrolledText

class TestScrolledText(unittest.TestCase):

    def setUp(self):
        self.root = Window()
        self.widget = ScrolledText(
            master=self.root,
            padding=10,
            height=5,
            width=40,
            autohide=True,
            vbar=True,
            hbar=False,
        )
        self.widget.pack()
        self.root.update_idletasks()

    def tearDown(self):
        self.widget.destroy()
        self.root.destroy()

    def test_widget_initialization(self):
        self.assertIsInstance(self.widget.text, tk.Text)
        self.assertIsNotNone(self.widget.vbar)
        self.assertIsNone(self.widget.hbar)

    def test_text_insertion(self):
        self.widget.insert("end", "Hello world")
        content = self.widget.get("1.0", "end-1c")
        self.assertEqual(content, "Hello world")

    def test_autohide_events(self):
        bindings = self.widget.bind()
        self.assertIn("<Enter>", bindings)
        self.assertIn("<Leave>", bindings)

    def test_scrollbar_visibility_methods(self):
        # These should run without error
        self.widget.show_scrollbars()
        self.widget.hide_scrollbars()

if __name__ == "__main__":
    unittest.main()
