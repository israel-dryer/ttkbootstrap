from ttkbootstrap.dialogs import Dialog
from ttkbootstrap import Frame, Label, Button, Separator
from ttkbootstrap.constants import *
import textwrap


class MessageDialog(Dialog):
    """A simple modal dialog class that can be used to build simple 
    message dialogs.
    
    Displays a message and a set of buttons. Each of the buttons in the 
    message window is identified by a unique symbolic name. After the 
    message window is popped up, the message box awaits for the user to 
    select one of the buttons. Then it returns the symbolic name of the 
    selected button. Use a `Toplevel` widget for more advanced modal 
    dialog designs.    
    """

    def __init__(
        self,
        title=None,
        message=None,
        buttons=['Cancel:secondary', 'OK:primary'],
        command=None,
        width=50,
        parent=None,
        alert=False,
        default=None,
        padding=(20, 20)
    ):
        """
        Parameters:
            
            title (str):
                The string displayed as the title of the message box. 
                This option is ignored on Mac OS X, where platform 
                guidelines forbid the use of a title on this kind of 
                dialog.

            message (str):
                A message to display in the message box.

            buttons (List[str]):
                A list of buttons to appear at the bottom of the popup
                messagebox. The buttons can be a list of strings which 
                will define the symbolic name and the button text.
                `['OK', 'Cancel']`. Alternatively, you can assign a
                bootstyle to each button by using the colon to separate the
                button text and the bootstyle. If no colon is found, then
                the style is set to 'primary' by default. 
                `['OK:success','Cancel:danger']`. 

            command (Tuple[Callable, str]):
                The function to invoke when the user closes the dialog. 
                The actual command is a tuple that consists of the 
                function to call and the symbolic name of the button that 
                closes the dialog.

            width (int):
                The maximum number of characters per line in the message.
                If the text stretches beyond the limit, the line will break
                at the word.

            parent (Widget):
                Makes the window the logical parent of the message box. 
                The messagebox is displayed on top of its parent window.

            alert (bool):
                Ring the display's bell when the dialog is shown. 

            default (str):
                The symbolic name of the default button. The default 
                button is invoked when the the <Return> key is pressed. 
                If no default is provided, the right-most button in the 
                button list will be set as the default.,

            padding  (Union[int, Tuple[int]]):
                The amount of space between the border and the widget
                contents.

        Example:

            ```python
            root = tk.Tk()
            
            md = MessageDialog(message="Displays a message with buttons.")
            md.show()
            
            root.mainloop()
            ```
        """
        super().__init__(parent, title)
        self._message = message
        self._buttons = buttons
        self._command = command
        self._width = width
        self._alert = alert
        self._default = default,
        self._padding = padding
        
    def create_body(self, master):
        """Overrides the parent method; adds the message section."""
        frame = Frame(master, padding=self._padding)
        if self._message:
            for i, msg in enumerate(self._message.split('\n')):
                message = '\n'.join(textwrap.wrap(msg, width=self._width))
                message_label = Label(frame, text=message)
                message_label.pack(pady=(0, 5), fill=X, anchor=N)
        frame.pack(fill=X, expand=True)
        return frame

    def create_buttonbox(self, master):
        """Overrides the parent method; adds the message buttonbox"""
        frame = Frame(master, padding=(5, 10))

        button_list = []

        for i, button in enumerate(self._buttons[::-1]):
            cnf = button.split(':')
            if len(cnf) == 2:
                text, bootstyle = cnf
            else:
                text = cnf[0]
                bootstyle = 'secondary'

            btn = Button(frame, bootstyle=bootstyle, text=text)
            btn.bind('<Return>', lambda _: btn.invoke())
            btn.configure(command=lambda b=btn: self.on_button_press(b))
            btn.pack(padx=5, side=RIGHT)
            btn.lower()  # set focus traversal left-to-right
            button_list.append(btn)

            if self._default is not None and text == self._default:
                self._default_button = btn
            elif self._default is None and i == 0:
                self._default_button = btn
            else:
                self._default_button = button_list[0]
        
        # bind default button to return key press and set focus
        self._toplevel.bind('<Return>', lambda _, b=btn: b.invoke())
        self._toplevel.bind('<KP_Enter>', lambda _, b=btn: b.invoke())

        Separator(self._toplevel).pack(fill=X)
        frame.pack(side=BOTTOM, fill=X, anchor=S)

    def on_button_press(self, button):
        """Save result, destroy the toplevel, and execute command."""
        self._result = button['text']
        command = self._command
        if command is not None:
            command()
        self._toplevel.destroy()

    def show(self):
        """Create and display the popup messagebox."""
        super().show()
        self._default_button.focus()

