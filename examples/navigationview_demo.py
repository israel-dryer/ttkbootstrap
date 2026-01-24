"""
NavigationView Demo

Demonstrates the NavigationView container with actual page navigation:
- Toolbar at the top spanning full width
- Clicking nav items switches the content area
- Groups with expand/collapse and compact mode popup
- Display mode switching (expanded, compact, minimal)
"""

import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.navigationview import NavigationView
from ttkbootstrap.widgets.composites.toolbar import Toolbar


def create_page(parent, title, description):
    """Create a demo page with title and content."""
    page = ttk.Frame(parent, padding=20)

    ttk.Label(page, text=title, font='heading-xl').pack(anchor='w', pady=(0, 10))
    ttk.Label(page, text=description, wraplength=500).pack(anchor='w', pady=(0, 20))

    # Add some demo content
    demo_frame = ttk.LabelFrame(page, text='Page Content', padding=20)
    demo_frame.pack(fill='both', expand=True)
    ttk.Label(
        demo_frame,
        text=f'This is the {title} page.\n\nAdd your content here.',
    ).pack(expand=True)

    return page


def main():
    root = ttk.App(theme="rose-light", title="NavigationView Demo", size=(1000, 650))

    container = ttk.Frame(root).pack(fill='both', expand=True)

    # --- Toolbar at the top (spans full width) ---
    toolbar = Toolbar(container, padding=(5, 0), surface='chrome', show_window_controls=False)
    toolbar.pack(fill='x')

    # --- Main container below toolbar ---
    main_container = ttk.Frame(container)
    main_container.pack(fill='both', expand=True)

    # NavigationView on the left (no internal header - using external toolbar)
    nav = NavigationView(main_container, show_header=False, collapsible=False)
    nav.pack(side='left', fill='y')

    # Add toolbar buttons that control the navigation
    toolbar.add_button(
        icon='arrow-left',
        command=lambda: nav.select('home'),
    )
    toolbar.add_button(
        icon='list',
        command=nav.toggle_pane,
    )

    toolbar.add_spacer()
    toolbar.add_button(icon='sun', command=ttk.toggle_theme)

    # Content container on the right (routed page content)
    content_container = ttk.Frame(main_container, surface='content')
    content_container.pack(side='right', fill='both', expand=True)

    # Page definitions (lazy creation for better startup performance)
    page_definitions = {
        'home': ('Home', 'Welcome to the app! This is your home dashboard.'),
        'documents': ('Documents', 'View and manage your documents here.'),
        'downloads': ('Downloads', 'Access your downloaded files.'),
        'photos': ('Photos', 'Browse your photo collection.'),
        'music': ('Music', 'Listen to your music library.'),
        'videos': ('Videos', 'Watch your video collection.'),
        'local': ('Local Files', 'Files stored on this device.'),
        'cloud': ('Cloud Storage', 'Files stored in the cloud.'),
        'network': ('Network', 'Files on network drives.'),
        'account': ('Account', 'Manage your account settings.'),
        'settings': ('Settings', 'Configure application settings.'),
    }

    # Cache for created pages (lazy creation)
    pages = {}
    current_page = [None]  # Use list to allow mutation in closure

    def get_or_create_page(key):
        """Get existing page or create it on first access (lazy loading)."""
        if key not in pages and key in page_definitions:
            title, description = page_definitions[key]
            pages[key] = create_page(content_container, title, description)
        return pages.get(key)

    def show_page(key):
        """Switch to the specified page."""
        if current_page[0]:
            current_page[0].pack_forget()
        page = get_or_create_page(key)
        if page:
            page.pack(fill='both', expand=True)
            current_page[0] = page

    # --- Add navigation items ---

    # Main items at root level (using default icon size - no size specified)
    nav.add_item('home', text='Home', icon='house')
    nav.add_item('documents', text='Documents', icon='file-earmark-text')
    nav.add_item('downloads', text='Downloads', icon='cloud-download')

    nav.add_separator()
    nav.add_header('Favorites')

    nav.add_item('photos', text='Photos', icon='image')
    nav.add_item('music', text='Music', icon='music-note-beamed')
    nav.add_item('videos', text='Videos', icon='camera-video')

    nav.add_separator()
    nav.add_header('Storage')

    # Create a group for file locations
    nav.add_group('files', text='Files', icon='folder')
    nav.add_item('local', text='Local Files', icon='hdd', group='files')
    nav.add_item('cloud', text='Cloud Storage', icon='cloud', group='files')
    nav.add_item('network', text='Network', icon='diagram-3', group='files')

    # Footer items
    nav.add_footer_item('account', text='Account', icon='person-circle')
    nav.add_footer_item('settings', text='Settings', icon='gear')

    # Select home by default
    nav.select('home')
    show_page('home')

    # --- Event handlers ---

    def on_selection_changed(event):
        key = event.data.get('key', '')
        show_page(key)

    def on_back_requested(event):
        nav.select('home')

    nav.on_selection_changed(on_selection_changed)
    nav.on_back_requested(on_back_requested)

    root.mainloop()



if __name__ == '__main__':
    main()