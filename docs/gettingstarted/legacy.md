# Legacy support

While `tkinter` widgets are not the focus of the library, I applied some default
styling for each theme to legacy widgets so that they didn't stick out. A large
reason for this is that several `ttk` widgets use `tkinter` widget components
under the hood. So it was necessary to style these as well so that, for example, 
the popdown list in the **Combobox**, or the **Menu** in the menubutton are
styled appropriate.

Below are examples of a light and dark themes using legacy `tkinter` widgets.

![legacy light theme](../assets/themes/legacy_light.png)

![legacy dark theme](../assets/themes/legacy_dark.png)