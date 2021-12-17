from ttkbootstrap.dialogs import Querybox, Messagebox
from ttkbootstrap.icons import Icon

Messagebox.ok("Do you want to continue?", icon=Icon.question)
Messagebox.retrycancel("Should I retry?")
Messagebox.okcancel("A message here")
Messagebox.show_error("You did this wrong!")
Messagebox.show_info("This is an info message")
Messagebox.show_warning("This is a warning message")
Messagebox.show_question("Do you want to continue?")
Querybox.get_date()
Querybox.get_font()
