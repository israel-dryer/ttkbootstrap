from tkinter.ttk import Entry


class EntryMixin:
    """A mixin that exposes the functionality of entry-like widgets. Can be used with any widget
    that exposes entry behavior (i.e. Spinbox, TextEntry, etc...)"""

    widget: Entry

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enable(self):
        """Enable the widget"""
        self.widget.state(['!disabled', '!readonly'])

    def disable(self):
        """Disable the widget"""
        self.widget.state(['disabled'])

    def bbox(self, index):
        """Return the bounding box of character at index"""
        return self.widget.bbox(index)

    def delete(self, first, last):
        """Delete text between indices"""
        return self.widget.delete(first, last)

    def insert(self, index, text):
        """Insert text at index"""
        return self.widget.insert(index, text)

    def icursor(self, index):
        """Set the cursor position"""
        self.widget.icursor(index)

    def index(self, index="insert"):
        """Return the character at index (defaults to 'cursor')"""
        return self.widget.index(index)

    def scan_mark(self, x):
        """Start drag-to-scroll behavior"""
        return self.widget.scan_mark(x)

    def scan_dragto(self, x):
        """Continue drag-to-scroll behavior"""
        return self.widget.scan_dragto(x)

    def selection_adjust(self, index):
        """Adjust selection endpoint"""
        return self.widget.selection_adjust(index)

    def selection_clear(self):
        """Clear text selection"""
        return self.widget.selection_clear()

    def selection_from(self, index):
        """Select text starting from index"""
        return self.widget.selection_from(index)

    def selection_to(self, index):
        """Extend selection to index"""
        return self.widget.selection_to(index)

    def selection_range(self, first, last):
        """Select text between first and last"""
        return self.widget.selection_range(first, last)

    def selection_present(self):
        return self.widget.selection_present()

    def selection_all(self):
        """Select all text"""
        return self.widget.selection_range(0, 'end')
