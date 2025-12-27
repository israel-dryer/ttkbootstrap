"""
PageStack Widget Demo

This demo showcases the PageStack widget's navigation features including:
- Creating and adding pages
- Navigation with data passing
- Back/forward navigation with history
- Page lifecycle events
- Navigation state queries (can_back, can_forward)
"""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import PageStack


class PageStackDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("PageStack Widget Demo")
        self.root.geometry("800x600")

        # Navigation history display
        self.history_var = tk.StringVar(value="History: Empty")

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        # Main container
        container = ttk.Frame(self.root, padding=10)
        container.pack(fill='both', expand=True)

        # Navigation controls at top
        nav_frame = ttk.Frame(container)
        nav_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(nav_frame, text="Navigation Controls:",
                 font=('TkDefaultFont', 10, 'bold')).pack(side='left', padx=(0, 10))

        self.back_btn = ttk.Button(nav_frame, text="← Back",
                                   command=self._on_back, state='disabled')
        self.back_btn.pack(side='left', padx=2)

        self.forward_btn = ttk.Button(nav_frame, text="Forward →",
                                      command=self._on_forward, state='disabled')
        self.forward_btn.pack(side='left', padx=2)

        ttk.Separator(nav_frame, orient='vertical').pack(side='left',
                                                         fill='y', padx=10)

        # Quick navigation buttons
        ttk.Button(nav_frame, text="Home",
                  command=lambda: self.stack.navigate('home')).pack(side='left', padx=2)
        ttk.Button(nav_frame, text="Profile",
                  command=lambda: self.stack.navigate('profile',
                                                     data={'user': 'John Doe'})).pack(side='left', padx=2)
        ttk.Button(nav_frame, text="Settings",
                  command=lambda: self.stack.navigate('settings')).pack(side='left', padx=2)
        ttk.Button(nav_frame, text="Details",
                  command=lambda: self.stack.navigate('details',
                                                     data={'item': 'Widget Demo'})).pack(side='left', padx=2)

        # History display
        history_label = ttk.Label(container, textvariable=self.history_var,
                                 relief='sunken', padding=5)
        history_label.pack(fill='x', pady=(0, 10))

        # Event log
        log_frame = ttk.LabelFrame(container, text="Event Log", padding=5)
        log_frame.pack(fill='x', pady=(0, 10))

        self.event_log = tk.Text(log_frame, height=6, wrap='word',
                                state='disabled', font=('Courier', 9))
        self.event_log.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(log_frame, orient='vertical',
                                 command=self.event_log.yview)
        scrollbar.pack(side='right', fill='y')
        self.event_log.configure(yscrollcommand=scrollbar.set)

        # PageStack
        self.stack = PageStack(container, padding=10)
        self.stack.pack(fill='both', expand=True)

        # Create pages
        self._create_pages()

        # Bind to page change event
        self.stack.on_page_changed(self._on_page_changed)

        # Navigate to home page
        self.stack.navigate('home')

    def _create_pages(self):
        """Create all the demo pages"""

        # Home Page
        home = self.stack.add('home', sticky='nsew')
        home.columnconfigure(0, weight=1)
        home.rowconfigure(1, weight=1)

        ttk.Label(home, text="🏠 Home Page",
                 font=('TkDefaultFont', 24, 'bold')).grid(row=0, column=0, pady=20)

        info = ttk.Frame(home)
        info.grid(row=1, column=0, sticky='nsew', padx=20)

        ttk.Label(info, text="Welcome to the PageStack Demo!",
                 font=('TkDefaultFont', 12)).pack(pady=10)
        ttk.Label(info, text="Use the navigation buttons above to explore different pages.",
                 wraplength=400).pack(pady=5)
        ttk.Label(info, text="The PageStack widget manages page history like a web browser.",
                 wraplength=400).pack(pady=5)

        # Profile Page
        profile = self.stack.add('profile', sticky='nsew')
        profile.columnconfigure(0, weight=1)
        profile.rowconfigure(1, weight=1)

        ttk.Label(profile, text="👤 Profile Page",
                 font=('TkDefaultFont', 24, 'bold')).grid(row=0, column=0, pady=20)

        profile_info = ttk.Frame(profile)
        profile_info.grid(row=1, column=0, sticky='nsew', padx=20)

        self.profile_label = ttk.Label(profile_info, text="Profile data will appear here",
                                       font=('TkDefaultFont', 12))
        self.profile_label.pack(pady=10)

        ttk.Button(profile_info, text="Edit Profile",
                  command=lambda: self.stack.navigate('settings',
                                                     data={'from': 'profile'})).pack(pady=5)

        # Bind to PageWillMount event for this page
        profile.bind('<<PageWillMount>>', self._on_profile_mount)

        # Settings Page
        settings = self.stack.add('settings', sticky='nsew')
        settings.columnconfigure(0, weight=1)
        settings.rowconfigure(1, weight=1)

        ttk.Label(settings, text="⚙️ Settings Page",
                 font=('TkDefaultFont', 24, 'bold')).grid(row=0, column=0, pady=20)

        settings_info = ttk.Frame(settings)
        settings_info.grid(row=1, column=0, sticky='nsew', padx=20)

        self.settings_label = ttk.Label(settings_info, text="Settings options",
                                        font=('TkDefaultFont', 12))
        self.settings_label.pack(pady=10)

        ttk.CheckButton(settings_info, text="Enable notifications").pack(pady=5, anchor='w')
        ttk.CheckButton(settings_info, text="Dark mode").pack(pady=5, anchor='w')
        ttk.CheckButton(settings_info, text="Auto-save").pack(pady=5, anchor='w')

        ttk.Button(settings_info, text="Save & Return",
                  command=lambda: self.stack.back()).pack(pady=10)

        settings.bind('<<PageWillMount>>', self._on_settings_mount)

        # Details Page
        details = self.stack.add('details', sticky='nsew')
        details.columnconfigure(0, weight=1)
        details.rowconfigure(1, weight=1)

        ttk.Label(details, text="📄 Details Page",
                 font=('TkDefaultFont', 24, 'bold')).grid(row=0, column=0, pady=20)

        details_info = ttk.Frame(details)
        details_info.grid(row=1, column=0, sticky='nsew', padx=20)

        self.details_label = ttk.Label(details_info, text="Details will appear here",
                                       font=('TkDefaultFont', 12))
        self.details_label.pack(pady=10)

        ttk.Button(details_info, text="Navigate with Replace",
                  command=lambda: self.stack.navigate('home', replace=True),
                  bootstyle='warning').pack(pady=5)
        ttk.Label(details_info, text="(Replace won't add to history)",
                 font=('TkDefaultFont', 8)).pack()

        details.bind('<<PageWillMount>>', self._on_details_mount)

    def _on_page_changed(self, event):
        """Handle page change event"""
        data = event.data

        # Log the event
        self._log_event(f"PageChanged: {data['prev_page']} → {data['page']} "
                       f"(nav={data['nav']}, index={data['index']}/{data['length']-1})")

        # Update history display
        current = self.stack.current()
        if current:
            page_key, page_data = current
            history_text = f"History: Position {data['index']+1}/{data['length']} | "
            history_text += f"Current: {page_key}"
            if page_data:
                history_text += f" | Data: {page_data}"
            self.history_var.set(history_text)

        # Update button states
        self.back_btn.configure(state='normal' if data['can_back'] else 'disabled')
        self.forward_btn.configure(state='normal' if data['can_forward'] else 'disabled')

    def _on_profile_mount(self, event):
        """Handle profile page mount"""
        data = event.data
        self._log_event(f"Profile PageWillMount")

        if 'user' in data:
            self.profile_label.configure(text=f"Welcome, {data['user']}!")
        else:
            self.profile_label.configure(text="Welcome, Guest!")

    def _on_settings_mount(self, event):
        """Handle settings page mount"""
        data = event.data
        self._log_event(f"Settings PageWillMount")

        if 'from' in data:
            self.settings_label.configure(text=f"Settings (accessed from {data['from']})")
        else:
            self.settings_label.configure(text="Settings")

    def _on_details_mount(self, event):
        """Handle details page mount"""
        data = event.data
        self._log_event(f"Details PageWillMount")

        if 'item' in data:
            self.details_label.configure(text=f"Details for: {data['item']}")
        else:
            self.details_label.configure(text="No item specified")

    def _on_back(self):
        """Navigate back"""
        if self.stack.can_back():
            self._log_event("User clicked Back button")
            self.stack.back()

    def _on_forward(self):
        """Navigate forward"""
        if self.stack.can_forward():
            self._log_event("User clicked Forward button")
            self.stack.forward()

    def _log_event(self, message):
        """Add event to log"""
        self.event_log.configure(state='normal')
        self.event_log.insert('end', f"{message}\n")
        self.event_log.see('end')
        self.event_log.configure(state='disabled')


def main():
    root = ttk.Window(theme="cosmo")
    app = PageStackDemo(root)
    root.mainloop()


if __name__ == '__main__':
    main()
