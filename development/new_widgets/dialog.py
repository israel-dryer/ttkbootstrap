from tkinter import Toplevel
from tkinter import _get_default_root

class Dialog:

    def __init__(
        self,
        parent=None,
        title=None,
        alert=False
    ):
        """A dialog base class.

        Parameters:

            master (Widget, optional):
                Makes the window the logical parent of the message box. 
                The messagebox is displayed on top of its parent window.
        
            title (str):
                The string displayed as the title of the message box. 
                This option is ignored on Mac OS X, where platform 
                guidelines forbid the use of a title on this kind of 
                dialog.

            alert (bool):
                Ring the display's bell when the dialog is shown. 
        """
        self.master = parent or _get_default_root('Dialog')
        self._winsys = self.master.tk.call('tk', 'windowingsystem')
        self._toplevel = None
        self._title = title
        self._result = None
        self._alert = alert

    def _locate(self):
        toplevel = self._toplevel
        master = toplevel.master
        screen_height = toplevel.winfo_screenheight()
        screen_width = toplevel.winfo_screenwidth()

        toplevel.update_idletasks()
        if master.winfo_viewable():
            m_width = master.winfo_width()
            m_height = master.winfo_height()
            m_x = master.winfo_rootx()
            m_y = master.winfo_rooty()
        else:
            m_width = screen_width
            m_height = screen_height
            m_x = m_y = 0
        w_width = toplevel.winfo_reqwidth()
        w_height = toplevel.winfo_reqheight()
        x = int(m_x + (m_width - w_width) * 0.45)
        y = int(m_y + (m_height - w_height) * 0.3)
        if x+w_width > screen_width:
            x = screen_width - w_width
        elif x < 0:
            x = 0
        if y+w_height > screen_height:
            y = screen_height - w_height
        elif y < 0:
            y = 0
        toplevel.geometry(f'+{x}+{y}')

    def show(self):
        """Show the popup dialog"""

        self._result = None
        self.build()
        self._locate()
        self._toplevel.deiconify()
        if self._alert:
            self._toplevel.bell()
            self._toplevel.grab_set()
            self._toplevel.wait_window()
            return self._result

    def create_body(self, master):
        """Create the dialog body.
        Return the widget that should have initial focus. This method
        should be overriden and is called by the `build` method.
        """
        print('creating the body')
        #raise NotImplementedError

    def create_buttonbox(self, master):
        """Create the dialog button box"""
        print('creating button box')
        #raise NotImplementedError

    def build(self):
        """Build the dialog from settings"""

        # setup toplevel based on widowing system

        if self._winsys == 'win32':
            self._toplevel = Toplevel(self.master)
            self._toplevel.attributes('-toolwindow')
            self._toplevel.minsize(250, 15)
        else:
            self._toplevel = Toplevel(self.master)
            self._toplevel.attributes('-type', 'dialog')

        self._toplevel.withdraw() # hide until drawn
        self._toplevel.resizable(0, 0)
        self._toplevel.transient(self.master)
        self._toplevel.title(self._title)

        # bind <Escape> event to window close
        self._toplevel.bind("<Escape>", lambda _: self._toplevel.destroy())

        # set position of popup from parent window
        #self._locate()

        # create widgets
        initial_focus = self.create_body(self._toplevel)
        self.create_buttonbox(self._toplevel)

        # set initial focus
        if initial_focus is not None:
            initial_focus.focus_set()

        # update the window before showing
        self._toplevel.update_idletasks()

    @property
    def result(self):
        return self['result']


if __name__ == '__main__':
    import tkinter as tk
    import tkinter as ttk
    root = tk.Tk()
    dialog = Dialog()
    btn = ttk.Button(text='push', command=dialog.show)
    btn.pack()
    root.mainloop()
