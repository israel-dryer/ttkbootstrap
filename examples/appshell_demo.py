"""
AppShell Demo

Demonstrates the AppShell application window which provides a standard
desktop app layout: toolbar at top, sidebar navigation on the left,
and page content on the right.

Features shown:
- AppShell with toolbar + nav + pages
- Groups, headers, separators, footer items
- Custom toolbar buttons (theme toggle)
- Page content for each nav item
- Page change event handling
"""

import ttkbootstrap as ttk


def create_page_content(parent, title, description):
    """Create demo content for a page."""
    ttk.Label(parent, text=title, font='heading-xl').pack(
        anchor='w', padx=20, pady=(20, 10)
    )
    ttk.Label(parent, text=description, wraplength=500).pack(
        anchor='w', padx=20, pady=(0, 20)
    )

    content = ttk.LabelFrame(parent, text='Page Content', padding=20)
    content.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    ttk.Label(
        content,
        text=f'This is the {title} page.\n\nAdd your content here.',
    ).pack(expand=True)


def main():
    shell = ttk.AppShell(
        title='AppShell Demo',
        theme='rose-light',
        size=(1000, 650),
    )

    # Add a theme toggle button to the toolbar (after the auto-spacer)
    shell.toolbar.add_button(icon='sun', command=ttk.toggle_theme)

    # --- Main navigation items ---
    home = shell.add_page('home', text='Home', icon='house')
    create_page_content(home, 'Home', 'Welcome to the app! This is your home dashboard.')

    docs = shell.add_page('documents', text='Documents', icon='file-earmark-text')
    create_page_content(docs, 'Documents', 'View and manage your documents here.')

    dl = shell.add_page('downloads', text='Downloads', icon='cloud-download')
    create_page_content(dl, 'Downloads', 'Access your downloaded files.')

    # --- Favorites section ---
    shell.add_separator()
    shell.add_header('Favorites')

    photos = shell.add_page('photos', text='Photos', icon='image')
    create_page_content(photos, 'Photos', 'Browse your photo collection.')

    music = shell.add_page('music', text='Music', icon='music-note-beamed')
    create_page_content(music, 'Music', 'Listen to your music library.')

    videos = shell.add_page('videos', text='Videos', icon='camera-video')
    create_page_content(videos, 'Videos', 'Watch your video collection.')

    # --- Storage section with a group ---
    shell.add_separator()
    shell.add_header('Storage')

    shell.add_group('files', text='Files', icon='folder', is_expanded=True)

    local = shell.add_page('local', text='Local Files', icon='hdd', group='files')
    create_page_content(local, 'Local Files', 'Files stored on this device.')

    cloud = shell.add_page('cloud', text='Cloud Storage', icon='cloud', group='files')
    create_page_content(cloud, 'Cloud Storage', 'Files stored in the cloud.')

    network = shell.add_page('network', text='Network', icon='diagram-3', group='files')
    create_page_content(network, 'Network', 'Files on network drives.')

    # --- Footer items ---
    account = shell.add_page('account', text='Account', icon='person-circle', is_footer=True)
    create_page_content(account, 'Account', 'Manage your account settings.')

    settings = shell.add_page('settings', text='Settings', icon='gear', is_footer=True)
    create_page_content(settings, 'Settings', 'Configure application settings.')

    # --- Event handling ---
    def on_page_changed(event):
        page = event.data.get('page', '')
        prev = event.data.get('prev_page', '')
        print(f'Page changed: {prev} -> {page}')

    shell.on_page_changed(on_page_changed)

    shell.mainloop()


if __name__ == '__main__':
    main()