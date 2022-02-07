import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Querybox, Messagebox
from ttkbootstrap.icons import Icon
import tkinter as tk

from ttkbootstrap.localization import MessageCatalog
MessageCatalog.locale('zh_cn')
Messagebox.ok("Messagebox.ok", position=(500, 500))

Messagebox.okcancel("Messagebox.okcancel", position=(500, 500))
Messagebox.retrycancel("Messagebox.retrycancel", position=(500, 500))
Messagebox.yesno("Messagebox.yesno", position=(500, 500))
Messagebox.yesnocancel("Messagebox.yesnocancel", position=(1000, 1000))

Messagebox.show_error("Messagebox.show_error", position=(500, 500))
Messagebox.show_info("Messagebox.show_info", position=(500, 500))
Messagebox.show_question("Messagebox.show_question", position=(500, 500))
Messagebox.show_warning("Messagebox.show_warning", position=(500, 500))

Querybox.get_date(title="Querybox.get_date")
Querybox.get_float("Querybox.get_float", position=(500, 500))
Querybox.get_integer("Querybox.get_integer", position=(500, 500))
Querybox.get_string("Querybox.get_string", position=(500, 500))
Querybox.get_font(title="Querybox.get_font", position=(500, 500))