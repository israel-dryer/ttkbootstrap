from json import load
from pathlib import Path
import pathlib
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import ctypes
import string
from ctypes import windll
from typing import List
from math import ceil
from datetime import datetime

class PathItem:

    def __init__(self, path: pathlib.Path):
        self.path = path
        self.name = path.name
        self.uri = path.absolute()
        self.tag = ['file', 'dir'][path.is_dir()]
        self.size: int = None
        self.type: str = None
        self.modified: str = None
        self.get_item_stats()

    @property
    def values(self):
        return self.modified, self.type, self.size

    def get_item_stats(self):
        stats = self.path.stat()
        # file size & type
        if self.path.is_dir():
            self.size = ''
            self.type = 'File Folder'
        else:
            self.size = f'{ceil(stats.st_size * 0.001):,d} KB'
            self.type = f'{self.path.suffix[1:].upper()} File'.strip()
        # last modified
        timestamp = datetime.fromtimestamp(stats.st_mtime)
        self.modified = timestamp.strftime("%m/%d/%Y %I:%M %p")

def get_folder_contents(pathname):
    """Return a list of Path items"""
    try:
        path = Path(pathname)
    except PermissionError:
        return []
    contents = []
    for item in path.iterdir():
        contents.append(PathItem(item))
    contents = sorted(contents, key=lambda x: x.tag) # dir is first
    return contents

def load_treeview_items(pathname):
    treeview: ttk.Treeview = app.nametowidget('contentsview')
    # remove existing items
    children  = treeview.get_children('')
    treeview.delete(*children)
    # get and load new items
    items: List[PathItem] = get_folder_contents(pathname)
    for item in items:
        treeview.insert('','end', iid=item.uri, text=item.name, tags=[item.tag], values=item.values)
    # update_breadcrumbs()

def on_click_sidebar_btn(event):
    treeview = app.nametowidget('folderview')
    iid = treeview.identify_row(event.y)
    app.setvar('contentspath', iid)
    load_treeview_items(iid)

def on_click_parent_dir():
    path = Path(app.getvar('contentspath'))
    app.setvar('contentspath', path.parent)
    load_treeview_items(path)

def on_click_treeview_dir(event):
    treeview = app.nametowidget('contentsview')
    iid = treeview.identify_row(event.y)
    app.setvar('contentspath', iid)
    load_treeview_items(iid)

# def update_breadcrumbs():
#     path = Path(app.getvar('contentspath'))
#     widgets = [
#         crumbframe.children['crumb1'],
#         crumbframe.children['crumb2'],
#         crumbframe.children['crumb3'],
#         crumbframe.children['crumb4']
#     ]

#     def goto_path(path):
#         app.setvar('contentspath', path.absolute())
#         load_path_items(path)

#     crumb_depth = 4
#     p = path
#     for i in range(crumb_depth):
#         widgets[i].pack_forget()
#         if i > 3:
#             continue
#         if p.name != '':
#             if len(p.name) > 15:
#                 name = f'{p.name[:15]}... > '
#             else:
#                 name = f'{p.name} > '
#             widgets[i].configure(text=name, command=lambda x=p: goto_path(x))
#             widgets[i].pack(side=RIGHT)
#         p = p.parent

def load_sidebar():

    folders = [
        'Desktop', 'Documents', 'Music', 'Pictures', 
        'Videos', 'Downloads'
    ]

    if app.winsys == 'x11':
        sidebar: ttk.Frame = app.nametowidget('sidebar')
        home = pathlib.Path.home()
        b_ = ttk.Button(
            master=sidebar, 
            text=home.parent.name, 
            image=images['Home'], 
            compound=LEFT, 
            bootstyle=LINK,
            command=lambda x=home: load_treeview_items(x)
        )
        b_.pack(anchor=W)

        sidebar: ttk.Frame = app.nametowidget('sidebar')
        home = pathlib.Path.home()
        b_ = ttk.Button(
            master=sidebar, 
            text=home.parent.name, 
            image=images['User'], 
            compound=LEFT, 
            bootstyle=LINK,
            command=lambda x=home: load_treeview_items(x)
        )
        b_.pack(anchor=W)
    else:
        sidebar: ttk.Frame = app.nametowidget('sidebar')
        home = pathlib.Path.home()
        b_ = ttk.Button(
            master=sidebar, 
            text=home.name, 
            image=images['Home'], 
            compound=LEFT, 
            bootstyle=LINK,
            command=lambda x=home: load_treeview_items(x)
        )
        b_.pack(anchor=W)        

    for folder in folders:
        p = Path(home / folder)
        if p.exists():
            b_ = ttk.Button(
                master=sidebar,
                text=p.name,
                image=images[p.name],
                compound=LEFT,
                bootstyle=LINK,
                command=lambda x=p: load_treeview_items(x)
            )
            b_.pack(anchor=W)
                
if __name__ == '__main__':

    app = ttk.Window(themename='darkly')
    item_path = Path.home()
    img_path = Path(__file__).parent
    app.setvar(name='contentspath', value=item_path.absolute())

    SIDEBAR_IMG_SIZE = (36, 36)
    TREEVIEW_IMG_SIZE = (24, 24)

    images = {
        'File': ImageTk.PhotoImage(Image.open(img_path / 'assets/icons8_folder_40px.png').resize(TREEVIEW_IMG_SIZE, Image.LANCZOS)),
        'Dir': ImageTk.PhotoImage(Image.open(img_path / 'assets/icons8_file_40px.png').resize(TREEVIEW_IMG_SIZE, Image.LANCZOS)),

        'Home': ImageTk.PhotoImage(Image.open(img_path / 'assets/icons8_home_40px.png').resize(SIDEBAR_IMG_SIZE, Image.LANCZOS)),
        'User': ImageTk.PhotoImage(Image.open(img_path / 'assets/icons8_user_folder_40px.png').resize(SIDEBAR_IMG_SIZE, Image.LANCZOS)),        
        'Desktop': ImageTk.PhotoImage(Image.open(img_path / 'assets/icons8_desktop_40px.png').resize(SIDEBAR_IMG_SIZE, Image.LANCZOS)),        
        'Videos': ImageTk.PhotoImage(Image.open(img_path / 'assets/icons8_movies_folder_40px.png').resize(SIDEBAR_IMG_SIZE, Image.LANCZOS)),        
        'Music': ImageTk.PhotoImage(Image.open(img_path / 'assets/icons8_music_folder_40px.png').resize(SIDEBAR_IMG_SIZE, Image.LANCZOS)),        
        'Pictures': ImageTk.PhotoImage(Image.open(img_path / 'assets/icons8_pictures_folder_40px.png').resize(SIDEBAR_IMG_SIZE, Image.LANCZOS)),        
        'Documents': ImageTk.PhotoImage(Image.open(img_path / 'assets/icons8_documents_folder_40px.png').resize(SIDEBAR_IMG_SIZE, Image.LANCZOS)),                
        'Downloads': ImageTk.PhotoImage(Image.open(img_path / 'assets/icons8_downloads_folder_40px.png').resize(SIDEBAR_IMG_SIZE, Image.LANCZOS)),                
    }


    sidebar = ttk.Frame(name='sidebar')
    sidebar.pack(side=LEFT, fill=X, anchor=N)

    contents_tv = ttk.Treeview(name='contentsview', show=TREEHEADINGS, columns=[0, 1, 2])
    contents_tv.pack(side=LEFT, fill=ttk.BOTH, expand=ttk.YES)    
    contents_tv.column('#0', width=500)
    contents_tv.heading('#0', text='Name', anchor=W)
    contents_tv.heading(0, text='Date modified', anchor=W)
    contents_tv.column(0, stretch=False)
    contents_tv.column(1, stretch=False, width=125)
    contents_tv.heading(1, text='Type', anchor=W)
    contents_tv.column(2, width=125, anchor=E, stretch=False)
    contents_tv.heading(2, text='Size', anchor=E)

    contents_tv.tag_configure('dir', image=images['File'])
    contents_tv.tag_configure('file', image=images['Dir'])
    ttk.Button(text='Prev', command=on_click_parent_dir).pack()

    # crumbframe = ttk.Frame()
    # crumbframe.pack(side=BOTTOM, fill=X)
    # ttk.Button(crumbframe, name='crumb1', text='crumb1', bootstyle=LINK, padding=0).pack(side=LEFT)
    # ttk.Button(crumbframe, name='crumb2', text='crumb2', bootstyle=LINK, padding=0).pack(side=LEFT)
    # ttk.Button(crumbframe, name='crumb3', text='crumb3', bootstyle=LINK, padding=0).pack(side=LEFT)
    # ttk.Button(crumbframe, name='crumb4', text='crumb4', bootstyle=LINK, padding=0).pack(side=LEFT)

    load_sidebar()
    app.update_idletasks()

    load_treeview_items(item_path)
    contents_tv.tag_bind('dir', '<Double-Button-1>', on_click_treeview_dir)

    app.mainloop()


