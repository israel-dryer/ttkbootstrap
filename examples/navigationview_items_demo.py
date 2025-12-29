"""
NavigationView Items Demo

This demo showcases the NavigationView item widgets:
- NavigationViewItem: Selectable items with icons, text, and nested children
- NavigationViewHeader: Section labels
- NavigationViewSeparator: Visual dividers
"""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.navigationview import (
    NavigationViewItem,
    NavigationViewHeader,
    NavigationViewSeparator,
)


class NavigationItemsDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("NavigationView Items Demo")
        self.root.geometry("500x700")

        # Shared variable for radio group selection
        self.nav_var = tk.StringVar(value='home')

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        # Main container with two columns
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill='both', expand=True)

        # Left panel - Navigation items
        nav_frame = ttk.LabelFrame(main, text="Navigation Items", padding=10)
        nav_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Right panel - Event log
        log_frame = ttk.LabelFrame(main, text="Event Log", padding=10)
        log_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        self.log_text = ttk.Text(log_frame, width=25, height=20, state='disabled')
        self.log_text.pack(fill='both', expand=True)

        # Track selection changes
        self.nav_var.trace_add('write', self._on_selection_changed)

        # Create navigation items
        self._create_nav_items(nav_frame)

    def _create_nav_items(self, parent):
        # Container for items
        container = ttk.Frame(parent)
        container.pack(fill='both', expand=True)

        # --- Main items ---
        home = NavigationViewItem(
            container,
            key='home',
            text='Home',
            icon='house',
            variable=self.nav_var,
        )
        home.pack(fill='x')
        home.on_invoked(self._on_item_invoked)

        documents = NavigationViewItem(
            container,
            key='documents',
            text='Documents',
            icon='file-earmark-text',
            variable=self.nav_var,
        )
        documents.pack(fill='x')
        documents.on_invoked(self._on_item_invoked)

        downloads = NavigationViewItem(
            container,
            key='downloads',
            text='Downloads',
            icon='cloud-download',
            variable=self.nav_var,
        )
        downloads.pack(fill='x')
        downloads.on_invoked(self._on_item_invoked)

        # --- Separator ---
        sep1 = NavigationViewSeparator(container)
        sep1.pack(fill='x')

        # --- Header ---
        header1 = NavigationViewHeader(container, text='Favorites')
        header1.pack(fill='x')

        # --- More items ---
        photos = NavigationViewItem(
            container,
            key='photos',
            text='Photos',
            icon='image',
            variable=self.nav_var,
        )
        photos.pack(fill='x')
        photos.on_invoked(self._on_item_invoked)

        music = NavigationViewItem(
            container,
            key='music',
            text='Music',
            icon='music-note-beamed',
            variable=self.nav_var,
        )
        music.pack(fill='x')
        music.on_invoked(self._on_item_invoked)

        # --- Another separator ---
        sep2 = NavigationViewSeparator(container)
        sep2.pack(fill='x')

        # --- Item with children ---
        files = NavigationViewItem(
            container,
            key='files',
            text='Files',
            icon='folder',
            variable=self.nav_var,
        )
        files.pack(fill='x')
        files.on_invoked(self._on_item_invoked)

        # Add child items
        local = files.add_child('local', text='Local Files', icon='hdd')
        local.on_invoked(self._on_item_invoked)

        cloud = files.add_child('cloud', text='Cloud Storage', icon='cloud')
        cloud.on_invoked(self._on_item_invoked)

        network = files.add_child('network', text='Network', icon='diagram-3')
        network.on_invoked(self._on_item_invoked)

        # Nested child (cloud has sub-items)
        onedrive = cloud.add_child('onedrive', text='OneDrive')
        onedrive.on_invoked(self._on_item_invoked)

        gdrive = cloud.add_child('gdrive', text='Google Drive')
        gdrive.on_invoked(self._on_item_invoked)

        # --- Footer separator ---
        sep3 = NavigationViewSeparator(container)
        sep3.pack(fill='x')

        # --- Footer item ---
        settings = NavigationViewItem(
            container,
            key='settings',
            text='Settings',
            icon='gear',
            variable=self.nav_var,
        )
        settings.pack(fill='x')
        settings.on_invoked(self._on_item_invoked)

    def _on_item_invoked(self, event):
        key = event.data['key']
        self._log_event(f"Invoked: {key}")

    def _on_selection_changed(self, *args):
        selected = self.nav_var.get()
        self._log_event(f"Selected: {selected}")

    def _log_event(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.configure(state='disabled')


def main():
    root = ttk.Window(theme="cosmo")
    app = NavigationItemsDemo(root)
    root.mainloop()


if __name__ == '__main__':
    main()
