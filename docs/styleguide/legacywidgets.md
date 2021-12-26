# Legacy widgets

ttkbootstrap applies a default style to legacy tkinter widgets so that they do
not look out-of-place when used with themed ttk widgets. The `Text` and `Canvas`
widgets are commonly used with themed `ttk` widgets for example.

## Themed legacy widgets

To ensure the styles are updated when the theme is changed, each legacy widget
is registered with the `Publisher` which sends an update message to each legacy
widget when the theme is changed in order to initiate a theme configuration on
the widget. 

## Customizing legacy widgets
While the theming functionality is appropriate in most cases, it also prevents
the user from making custom changes to the widget. However, in version 1.2 an
`autostyle` parameter was added to all legacy widgets. By default, `autostyle`
is implicitly **True**. This means, that ttkbootstrap will handle all of the
styling on legacy widgets. However, if you set the `autostyle` parameter to
**False**, the widget styling will be delegated to the user. This will enable
you to make custom changes to legacy widgets.

!!! warning "Turning off autostyle should be used with caution"
    If you turn off autostyle on a widget, it will no longer receive theme
    change updates; no styling will be applied by default, including fonts,
    relief, etc...
