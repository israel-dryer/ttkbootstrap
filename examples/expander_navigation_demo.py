"""
Expander Navigation Demo

Tests the enhanced Expander widget with:
- Icon support in header
- Signal/variable for selection state (radio-group behavior)
- Collapsible control to hide/show chevron
"""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.expander import Expander


class ExpanderNavigationDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Expander Navigation Demo")
        self.root.geometry("600x500")

        # Shared variable for selection (radio-group behavior)
        self.nav_var = tk.StringVar(value='home')

        self._setup_ui()

    def _setup_ui(self):
        # Main container
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill='both', expand=True)

        # Left panel - Navigation using Expanders
        nav_frame = ttk.LabelFrame(main, text="Navigation (Expander)", padding=10)
        nav_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Right panel - Info display
        info_frame = ttk.LabelFrame(main, text="Selection Info", padding=10)
        info_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        self.info_label = ttk.Label(info_frame, text="Selected: home")
        self.info_label.pack(anchor='w', pady=5)

        # Track selection changes
        self.nav_var.trace_add('write', self._on_selection_changed)

        # Create navigation items using Expanders
        self._create_nav_items(nav_frame)

    def _create_nav_items(self, parent):
        container = ttk.Frame(parent)
        container.pack(fill='both', expand=True)

        # Home - leaf item (not collapsible, no chevron)
        home = Expander(
            container,
            title="Home",
            icon="house",
            collapsible=False,
            variable=self.nav_var,
            value="home",
        )
        home.pack(fill='x', pady=2)
        home.on_selected(self._on_item_selected)

        # Documents - leaf item
        docs = Expander(
            container,
            title="Documents",
            icon="file-earmark-text",
            collapsible=False,
            variable=self.nav_var,
            value="documents",
        )
        docs.pack(fill='x', pady=2)
        docs.on_selected(self._on_item_selected)

        # Downloads - leaf item
        downloads = Expander(
            container,
            title="Downloads",
            icon="cloud-download",
            collapsible=False,
            variable=self.nav_var,
            value="downloads",
        )
        downloads.pack(fill='x', pady=2)
        downloads.on_selected(self._on_item_selected)

        # Separator
        ttk.Separator(container, orient='horizontal').pack(fill='x', pady=8)

        # Files - parent item with children (collapsible)
        files = Expander(
            container,
            title="Files",
            icon="folder",
            expanded=False,
            collapsible=True,
            variable=self.nav_var,
            value="files",
        )
        files.pack(fill='x', pady=2)
        files.on_selected(self._on_item_selected)

        # Add children to Files
        files_content = files.add()

        local = Expander(
            files_content,
            title="Local Files",
            icon="hdd",
            collapsible=False,
            variable=self.nav_var,
            value="local",
        )
        local.pack(fill='x', pady=1)
        local.on_selected(self._on_item_selected)

        cloud = Expander(
            files_content,
            title="Cloud Storage",
            icon="cloud",
            collapsible=False,
            variable=self.nav_var,
            value="cloud",
        )
        cloud.pack(fill='x', pady=1)
        cloud.on_selected(self._on_item_selected)

        # Separator
        ttk.Separator(container, orient='horizontal').pack(fill='x', pady=8)

        # Settings - leaf item
        settings = Expander(
            container,
            title="Settings",
            icon="gear",
            collapsible=False,
            variable=self.nav_var,
            value="settings",
        )
        settings.pack(fill='x', pady=2)
        settings.on_selected(self._on_item_selected)

    def _on_item_selected(self, event):
        value = event.data.get('value', '')
        print(f"<<Selected>> event: {value}")

    def _on_selection_changed(self, *args):
        selected = self.nav_var.get()
        self.info_label.configure(text=f"Selected: {selected}")
        print(f"Variable changed: {selected}")


def main():
    root = ttk.Window(theme="cosmo")
    app = ExpanderNavigationDemo(root)
    root.mainloop()


if __name__ == '__main__':
    main()
