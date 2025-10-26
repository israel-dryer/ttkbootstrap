from ttkbootstrap.dialogs import Messagebox, Querybox
from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.window import Window


def run_test():
    MessageCatalog.locale('zh_cn')
    Messagebox.ok("Testing first item", parent=root)
    Messagebox.ok("Messagebox.ok")

    Messagebox.okcancel("Messagebox.okcancel")
    Messagebox.retrycancel("Messagebox.retrycancel")
    Messagebox.yesno("Messagebox.yesno")
    Messagebox.yesnocancel("Messagebox.yesnocancel")

    Messagebox.show_error("Messagebox.show_error")
    Messagebox.show_info("Messagebox.show_info")
    Messagebox.show_question("Messagebox.show_question")
    Messagebox.show_warning("Messagebox.show_warning")

    Querybox.get_date(title="Querybox.get_date")
    Querybox.get_float("Querybox.get_float")
    Querybox.get_integer("Querybox.get_integer")
    Querybox.get_string("Querybox.get_string")
    Querybox.get_font(title="Querybox.get_font")
    Querybox.get_item(
        "Querybox.get_item", initialvalue="apple",
        items=["apple", "banana", "grape", "kiwi", "orange", "pear"],
        position=(500, 500))


root = Window()
root.geometry("1000x1000+1000+500")

root.after(100, run_test)

root.mainloop()
