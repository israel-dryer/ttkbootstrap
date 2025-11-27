from tkinter.ttk import Entry


class EntryMixin:
    """A mixin that exposes the functionality of entry-like widgets on composite widgets"""

    _entry: Entry

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def bbox(self, index):
        """Return the bounding box of character at index"""
        return self._entry.bbox(index)

    def delete(self, first, last):
        """Delete text between indices"""
        return self._entry.delete(first, last)

    def insert(self, index, text):
        """Insert text at index"""
        return self._entry.insert(index, text)

    def icursor(self, index):
        """Set the cursor position"""
        self._entry.icursor(index)

    def index(self, index="insert"):
        """Return the character at index (defaults to 'cursor')"""
        return self._entry.index(index)

    def scan_mark(self, x):
        """Start drag-to-scroll behavior"""
        return self._entry.scan_mark(x)

    def scan_dragto(self, x):
        """Continue drag-to-scroll behavior"""
        return self._entry.scan_dragto(x)

    def selection_adjust(self, index):
        """Adjust selection endpoint"""
        return self._entry.selection_adjust(index)

    def selection_clear(self):
        """Clear text selection"""
        return self._entry.selection_clear()

    def selection_from(self, index):
        """Select text starting from index"""
        return self._entry.selection_from(index)

    def selection_to(self, index):
        """Extend selection to index"""
        return self._entry.selection_to(index)

    def selection_range(self, first, last):
        """Select text between first and last"""
        return self._entry.selection_range(first, last)

    def selection_present(self):
        return self._entry.selection_present()

    def selection_all(self):
        """Select all text"""
        return self._entry.selection_range(0, 'end')
