import ttkbootstrap as ttk
from ttkbootstrap import Entry, Frame, Label
from ttkbootstrap.constants import *
from tkinter import Event

class InputGroup(Frame):
    def __init__(
        self,
        master=None,
        widget=Entry,
        labeltext=None,
        defaultvalue=None,
        validatetype=None,
        validateregx=None,
        validatecommand=None,
        activemessage=None,
        errormessage=None,
        confirmmessage=None,
        **kw
    ):
        super().__init__(master, padding=10)
        self._widget = widget(self)
        self._label = Label(self)
        self._message = Label(self)

        # configuration
        self._labeltext = labeltext
        self._defaultvalue = defaultvalue
        self._validatetype = validatetype
        self._validateregx = validateregx
        self._validatecommand = validatecommand
        self._activemessage = activemessage
        self._errormessage = errormessage
        self._confirmmessage = confirmmessage

        self.setup_widget()

    def setup_widget(self):
        self._widget.pack(fill=X)
        if self._defaultvalue:
            self._widget.insert(END, self._defaultvalue)

        self._widget.bind("<FocusIn>", self.on_focus_in)
        self._widget.bind("<FocusOut>", self.on_focus_out)
        self._padding = int(self._message.winfo_reqheight())//3
        self.configure(padding=self._padding)


    def on_focus_in(self, _):
        if self._activemessage is not None:
            self._message.configure(text=self._activemessage)
            self._message.pack(after=self._widget, fill=X)
            self._padding = p = int(self._message.winfo_reqheight())//3
            p = self._padding
            padding = (p, p, p, 0)
            self.configure(padding=padding)

    def on_focus_out(self, _):
        print("you just focused out")
        if self._activemessage is not None:
            self._message.pack_forget()
            self.configure(padding=self._padding)


if __name__ == '__main__':

    app = ttk.Window()

    g = InputGroup(app, labeltext='First Name', activemessage='Enter your first name')
    g.pack(padx=10, pady=10)
    g = InputGroup(app, labeltext='Last Name', activemessage='Enter your last name')
    g.pack(padx=10, pady=10)

    app.mainloop()