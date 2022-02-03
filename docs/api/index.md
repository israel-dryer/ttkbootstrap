# API Documentation

ttkbootstrap is a wrapper on tkinter. Any widget or function not defined
specifically in this library can be found in [other references](#other-references).

## 🌈 [colorutils module](colorutils.md)
This module contains various helper methods for manipulating colors.

## 💬 dialogs module
This module contains various base dialog base classes (ending in "Dialog") 
that can be used to create custom dialogs for the end user. These base 
classes serve as the basis for the pre-defined static helper methods in 
the `Messagebox`, and `Querybox` container classes, which include many
pre-defined message and query dialog configurations.

❯ [ColorChooserDialog](dialogs/colorchooser.md)  
❯ [ColorDropperDialog](dialogs/colordropper.md)  
❯ [Dialog](dialogs/dialog.md)  
❯ [FontDialog](dialogs/fontdialog.md)  
❯ [MessageBox](dialogs/messagebox.md)  
❯ [MessageDialog](dialogs/messagedialog.md)  
❯ [QueryBox](dialogs/querybox.md)  
❯ [QueryDialog](dialogs/querydialog.md)  

## 😉 icons module
This module contains classes that provide emojis or image icons for your
application. They can be used in text as `Emoji` or in the 
`PhotoImage` class as `Icon`.

❯ [Emoji](icons/emoji.md)  
❯ [Icon](icons/icon.md)  

## 🈚 localization module
The module includes methods and classes for localizing the text in gui
widgets. [Your help is needed](https://github.com/israel-dryer/ttkbootstrap/blob/master/src/ttkbootstrap/localization/msgs/README.md) 
to add to the msg files used to translate the text!

## 📜 scrolled module
This module contains various scrolled widgets such as `ScrolledText` and
`ScrolledFrame`.

❯ [ScrolledFrame](scrolled/scrolledframe.md)  
❯ [ScrolledText](scrolled/scrolledtext.md)  

## 🎨 style module
This module contains the classes that make up the ttkbootstrap theme and
style engine. Depending on how you use ttkbootstrap, you may never need
to use any of these classes directly, but then again, you may, so the 
docs are here for your reference.  

❯ [Style](style/style.md)  
❯ [Colors](style/colors.md)  
❯ [ThemeDefinition](style/themedefinition.md)  
❯ [StyleBuilderTk](style/stylebuildertk.md)  
❯ [StyleBuilderTTK](style/stylebuilderttk.md)  
❯ [Bootstyle](style/bootstyle.md)  

## 🪟 [tableview module](tableview/tableview.md)
❯ [Tableview](tableview/tableview.md)  
❯ [TableColumn](tableview/tablecolumn.md)  
❯ [TableRow](tableview/tablerow.md)

## 🛎️ [toast module](toast.md)
This module has a class called `ToastNotification` which provides a 
semi-transparent popup window for temporary alerts or messages.

## 📝 [tooltip module](tooltip.md)
This module contains a class of the same name that provides a 
semi-transparent tooltip popup window that shows text when the
mouse is hovering over the widget and closes when the mouse is no
longer hovering over the widget.

## ☑️ widgets module
This module contains the custom ttkbootstrap widgets linked below.  

❯ [DateEntry](widgets/dateentry.md)  
❯ [Floodgauge](widgets/floodgauge.md)  
❯ [Meter](widgets/meter.md)  

## 🗔 window module
This module contains a class of the same name that wraps the `tkinter.Tk` 
and [Style](style/style.md) classes to provide a more
convenient api for initial application startup. This also applies to the
`Toplevel` class.  

❯ [Window](window/window)  
❯ [Toplevel](window/toplevel)   


## ⚙️ [utility module](utility.md)
This module includes various utility functions that may or may not be useful
to the end user. Click the header to read more.

## ❓other references
This api reference does not include classes, methods, and functions
inherited from **tkinter**. To learn more about how to use tkinter, you can
consult any of the resources listed below:

❯ [docs.python.org](https://docs.python.org/3/library/tkinter.html)  
❯ [tkdocs](https://tkdocs.com/)  
❯ [pythontutorial.net](https://www.pythontutorial.net/tkinter/)  
❯ [anzeljg](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/)  
❯ [tcl/tk](https://www.tcl.tk/man/tcl8.6/TkCmd/contents.html)  