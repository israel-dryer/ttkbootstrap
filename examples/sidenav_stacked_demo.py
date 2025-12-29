"""Demo showing stacked SideNavs for multi-level navigation.

This demonstrates using multiple SideNav widgets side-by-side:
- Icon-only SideNav for primary navigation
- Full list SideNav for secondary navigation
- ListView for detailed item navigation (title, text, caption)

This pattern is common in apps like Outlook, Teams, and Discord.
"""

import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites import SideNav, ListView


def main():
    root = ttk.Window(theme="light")
    root.title("Stacked SideNavs Demo")
    root.geometry("1100x600")

    # Shared selection signal for primary nav
    primary_var = ttk.StringVar(value='mail')

    # --- Primary Navigation (icon-only with dark background) ---
    primary_nav = SideNav(
        root,
        icon_only=True,
        variable=primary_var,
        item_bootstyle='primary-ghost',
        surface_color='background[+1]',
        padding=8,
    )
    primary_nav.pack(side='left', fill='y')

    primary_nav.add_item('mail', icon='envelope')
    primary_nav.add_item('calendar', icon='calendar')
    primary_nav.add_item('contacts', icon='people')
    primary_nav.add_separator()
    primary_nav.add_item('settings', icon='gear')

    # --- Secondary Navigation Container ---
    secondary_container = ttk.Frame(root, width=200)
    secondary_container.pack(side='left', fill='y')
    secondary_container.pack_propagate(False)

    # Secondary nav frames (one for each primary item)
    secondary_navs = {}

    # Mail secondary nav
    mail_nav = SideNav(secondary_container, item_bootstyle='primary-ghost', padding=8)
    mail_nav.add_header('Mail')
    mail_nav.add_item('inbox', text='Inbox', icon='inbox')
    mail_nav.add_item('sent', text='Sent', icon='send')
    mail_nav.add_item('drafts', text='Drafts', icon='file-earmark')
    mail_nav.add_separator()
    mail_nav.add_item('archive', text='Archive', icon='archive')
    mail_nav.add_item('trash', text='Trash', icon='trash')
    secondary_navs['mail'] = mail_nav

    # Calendar secondary nav
    calendar_nav = SideNav(secondary_container, item_bootstyle='primary-ghost', padding=8)
    calendar_nav.add_header('Calendar')
    calendar_nav.add_item('today', text='Today', icon='calendar-day')
    calendar_nav.add_item('week', text='Week', icon='calendar-week')
    calendar_nav.add_item('month', text='Month', icon='calendar-month')
    calendar_nav.add_separator()
    calendar_nav.add_item('events', text='Events', icon='calendar-event')
    secondary_navs['calendar'] = calendar_nav

    # Contacts secondary nav
    contacts_nav = SideNav(secondary_container, item_bootstyle='primary-ghost', padding=8)
    contacts_nav.add_header('Contacts')
    contacts_nav.add_item('all', text='All Contacts', icon='people')
    contacts_nav.add_item('favorites', text='Favorites', icon='star')
    contacts_nav.add_item('groups', text='Groups', icon='diagram-3')
    secondary_navs['contacts'] = contacts_nav

    # Settings secondary nav
    settings_nav = SideNav(secondary_container, item_bootstyle='primary-ghost', padding=8)
    settings_nav.add_header('Settings')
    settings_nav.add_item('account', text='Account', icon='person')
    settings_nav.add_item('appearance', text='Appearance', icon='palette')
    settings_nav.add_item('notifications', text='Notifications', icon='bell')
    settings_nav.add_item('privacy', text='Privacy', icon='shield-lock')
    secondary_navs['settings'] = settings_nav

    # Show initial secondary nav
    current_secondary = [mail_nav]
    mail_nav.pack(fill='both', expand=True)

    def on_primary_changed(*args):
        """Switch secondary nav based on primary selection."""
        key = primary_var.get()
        if key in secondary_navs:
            # Hide current
            if current_secondary:
                current_secondary[0].pack_forget()
            # Show new
            secondary_navs[key].pack(fill='both', expand=True)
            current_secondary[0] = secondary_navs[key]

    primary_var.trace_add('write', on_primary_changed)

    # --- Third Level: ListView with title, text, caption ---
    list_container = ttk.Frame(root, width=280)
    list_container.pack(side='left', fill='y')
    list_container.pack_propagate(False)

    # Sample email data with title, text, caption
    emails = [
        {
            'id': 1,
            'title': 'John Smith',
            'text': 'Meeting tomorrow at 10am',
            'caption': '2 hours ago',
            'icon': 'person-circle',
        },
        {
            'id': 2,
            'title': 'Jane Doe',
            'text': 'Project update - Phase 2 complete',
            'caption': '5 hours ago',
            'icon': 'person-circle',
        },
        {
            'id': 3,
            'title': 'Marketing Team',
            'text': 'Q4 Campaign Results',
            'caption': 'Yesterday',
            'icon': 'people-fill',
        },
        {
            'id': 4,
            'title': 'HR Department',
            'text': 'Holiday schedule reminder',
            'caption': 'Yesterday',
            'icon': 'building',
        },
        {
            'id': 5,
            'title': 'Alex Johnson',
            'text': 'Code review requested',
            'caption': '2 days ago',
            'icon': 'person-circle',
        },
        {
            'id': 6,
            'title': 'Support Ticket #1234',
            'text': 'Customer issue resolved',
            'caption': '3 days ago',
            'icon': 'ticket-detailed',
        },
    ]

    email_list = ListView(
        list_container,
        items=emails,
        selection_mode='single',
        show_scrollbar=False,
        alternating_row_mode='none',
    )
    email_list.pack(fill='both', expand=True)

    # --- Content Area ---
    content = ttk.Frame(root, padding=20)
    content.pack(side='right', fill='both', expand=True)

    title = ttk.Label(content, text="Stacked SideNavs Demo", font='title')
    title.pack(anchor='nw', pady=(0, 10))

    description = ttk.Label(
        content,
        text="This demo shows how to stack navigation widgets:\n\n"
             "1. Icon-only SideNav for primary categories\n"
             "2. SideNav with text for secondary navigation\n"
             "3. ListView with title, text, caption for detailed items\n\n"
             "Click the icons on the left to switch between sections.",
        wraplength=400,
        justify='left'
    )
    description.pack(anchor='nw')

    # Show selection info
    info_frame = ttk.Frame(content)
    info_frame.pack(anchor='nw', pady=20)

    primary_label = ttk.Label(info_frame, text="Primary: mail")
    primary_label.pack(anchor='w')

    def update_info(*args):
        primary_label.configure(text=f"Primary: {primary_var.get()}")

    primary_var.trace_add('write', update_info)

    root.mainloop()


if __name__ == '__main__':
    main()
