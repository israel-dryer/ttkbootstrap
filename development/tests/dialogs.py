from tkinter import Message
from ttkbootstrap.dialogs import Querybox, Messagebox
from ttkbootstrap.icons import Icon

# Messagebox.ok("Messagebox.ok")
# Messagebox.okcancel("Messagebox.okcancel")
# Messagebox.retrycancel("Messagebox.retrycancel")
# Messagebox.yesno("Messagebox.yesno")
# Messagebox.yesnocancel("Messagebox.yesnocancel")

# Messagebox.show_error("Messagebox.show_error")
# Messagebox.show_info("Messagebox.show_info")
# result = Messagebox.show_question("Messagebox.show_question")

# Messagebox.show_warning("Messagebox.show_warning")

# Querybox.get_date(title="Querybox.get_date")
# Querybox.get_float("Querybox.get_float")
# Querybox.get_integer("Querybox.get_integer")
# Querybox.get_string("Querybox.get_string")
# Querybox.get_font(title="Querybox.get_font")
result = Querybox.get_color()
print(result)