"""Demo for Tabs and TabView widgets."""
import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.widgets.composites.tabs import Tabs, TabView

app = ttk.App("Tabs Demo", size=(900, 800))

# =============================================================================
# TABS WIDGET DEMOS
# =============================================================================

ttk.Label(app, text="Tabs Widget", font='title').pack(anchor='w', padx=8, pady=(16, 8))

# --- Basic Tabs with different variants ---
variants_frame = ttk.Frame(app)
variants_frame.pack(anchor='w', padx=8, fill='x')

# Bar variant (default)
bar_frame = ttk.Frame(variants_frame)
bar_frame.pack(side='left', padx=(0, 24))
ttk.Label(bar_frame, text="Bar (default):").pack(anchor='w')
bar_tabs = Tabs(bar_frame, variant='bar')
bar_tabs.add_tab(text='Home', value='home', icon='house')
bar_tabs.add_tab(text='Files', value='files', icon='folder2')
bar_tabs.add_tab(text='Settings', value='settings', icon='gear')
bar_tabs.pack(anchor='w')

# Pill variant
pill_frame = ttk.Frame(variants_frame)
pill_frame.pack(side='left')
ttk.Label(pill_frame, text="Pill:").pack(anchor='w')
pill_tabs = Tabs(pill_frame, variant='pill')
pill_tabs.add_tab(text='Dashboard', value='dashboard')
pill_tabs.add_tab(text='Projects', value='projects')
pill_tabs.pack(anchor='w')

# --- Tabs with enable_adding ---
ttk.Label(app, text="Tabs with enable_adding:", font='heading').pack(anchor='w', padx=8, pady=(16, 4))

adding_tabs = Tabs(app, enable_adding=True, enable_closing='hover')
tab_counter = [0]  # Use list to allow modification in closure

def on_add_tab(event):
    tab_counter[0] += 1
    value = f'Document {tab_counter[0] + 1}'
    adding_tabs.add_tab(text=f'Document {tab_counter[0] + 1}', icon='file-text', value=value)

adding_tabs.add_tab(text='Document 1', value='initial', icon='file-text')
adding_tabs.on_tab_added(on_add_tab)
adding_tabs.pack(anchor='w', padx=8, fill='x')

# --- Stretch tabs ---
ttk.Label(app, text="Stretch tabs (tab_width='stretch'):", font='heading').pack(anchor='w', padx=8, pady=(16, 4))

stretch_tabs = Tabs(app, tab_width='stretch')
stretch_tabs.add_tab(text='First', value='first')
stretch_tabs.add_tab(text='Second', value='second')
stretch_tabs.add_tab(text='Third', value='third')
stretch_tabs.pack(anchor='w', padx=8, fill='x')

# =============================================================================
# TABVIEW WIDGET DEMOS
# =============================================================================

ttk.Label(app, text="TabView Widget", font='title').pack(anchor='w', padx=8, pady=(24, 8))

# --- Basic TabView ---
ttk.Label(app, text="Basic TabView:", font='heading').pack(anchor='w', padx=8, pady=(8, 4))

tabview = TabView(app, height=100)

home_page = tabview.add('home', text='Home', icon='house')
ttk.Label(home_page, text='Welcome to the Home page!', font='heading').pack(padx=16, pady=16)

files_page = tabview.add('files', text='Files', icon='folder2')
ttk.Label(files_page, text='Browse your files here.').pack(padx=16, pady=16)

settings_page = tabview.add('settings', text='Settings', icon='gear')
ttk.Label(settings_page, text='Configure your settings.').pack(padx=16, pady=16)

tabview.pack(anchor='w', padx=8, fill='x')

# --- TabView with closable and addable tabs ---
ttk.Label(app, text="TabView with enable_closing and enable_adding:", font='heading').pack(anchor='w', padx=8, pady=(16, 4))

dynamic_tabview = TabView(app, height=100, enable_closing=True, enable_adding=True)
dynamic_counter = [0]

def on_add_page(event):
    dynamic_counter[0] += 1
    key = f'doc{dynamic_counter[0]}'
    page = dynamic_tabview.add(key, text=f'Document {dynamic_counter[0]}', icon='file-text')
    ttk.Label(page, text=f'Content for Document {dynamic_counter[0]}').pack(padx=16, pady=16)

# Add initial tabs
for i in range(1, 3):
    dynamic_counter[0] = i
    page = dynamic_tabview.add(f'doc{i}', text=f'Document {i}', icon='file-text')
    ttk.Label(page, text=f'Content for Document {i}').pack(padx=16, pady=16)

dynamic_tabview.on_tab_added(on_add_page)
dynamic_tabview.pack(anchor='w', padx=8, fill='x')

# --- Vertical TabView with enable_adding ---
ttk.Label(app, text="Vertical TabView with enable_adding:", font='heading').pack(anchor='w', padx=8, pady=(16, 4))

vert_tabview = TabView(app, orient='vertical', variant='bar', height=160, enable_adding=True)
vert_counter = [0]

def on_add_vert(event):
    vert_counter[0] += 1
    key = f'page{vert_counter[0]}'
    page = vert_tabview.add(key, text=f'Page {vert_counter[0]}', icon='file')
    ttk.Label(page, text=f'Content for Page {vert_counter[0]}').pack(padx=16, pady=16)



general = vert_tabview.add('general', text='General', icon='sliders')
ttk.Label(general, text='General settings and preferences.').pack(padx=16, pady=16)

account = vert_tabview.add('account', text='Account', icon='person')
ttk.Label(account, text='Account information and profile.').pack(padx=16, pady=16)

vert_tabview.on_tab_added(on_add_vert)
vert_tabview.pack(anchor='w', padx=8, fill='x')


# Measure TabItem height after rendering
def measure_tab_height():
    app.update_idletasks()
    # Get first tab from bar_tabs
    tabs = bar_tabs.items()
    if tabs:
        tab = tabs[0]
        print(f"TabItem dimensions:")
        print(f"  winfo_height: {tab.winfo_height()}")
        print(f"  winfo_reqheight: {tab.winfo_reqheight()}")
        print(f"  winfo_width: {tab.winfo_width()}")
        print(f"  winfo_reqwidth: {tab.winfo_reqwidth()}")

app.after(100, measure_tab_height)

app.mainloop()
