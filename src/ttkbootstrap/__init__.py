"""
    Why does this project exist?
    ============================
    The purpose of this project is create a set of beautifully designed 
    and easy to apply styles for your tkinter applications. Ttk can be 
    very time-consuming to style if you are just a casual user. This 
    project takes the pain out of getting a modern look and feel so 
    that you can focus on designing your application. This project was 
    created to harness the power of ttk's (and thus Python's) existing 
    built-in theme engine to create modern and professional-looking 
    user interfaces which are inspired by, and in many cases, 
    whole-sale rip-off's of the themes found on Bootswatch_. Even 
    better, you have the abilty to 
    :ref:`create and use your own custom themes <tutorial:create a new theme>` 
    using TTK Creator.

    A bootstrap approach to style
    =============================
    Many people are familiar with bootstrap for web developement. It 
    comes pre-packaged with built-in css style classes that provide a 
    professional and consistent api for quick development. I took a 
    similar approach with this project by pre-defining styles for 
    nearly all ttk widgets. This makes is very easy to apply the 
    theme colors to various widgets by using style declarations. If 
    you want a button in the `secondary` theme color, simply apply the
    **secondary.TButton** style to the button. Want a blue outlined 
    button? Apply the **info.Outline.TButton** style to the button.

    What about the old tkinter widgets?
    ===================================
    Some of the ttk widgets utilize existing tkinter widgets. For 
    example: there is a tkinter popdown list in the ``ttk.Combobox`` 
    and a legacy tkinter widget inside the ``ttk.OptionMenu``. To 
    make sure these widgets didn't stick out like a sore thumb, I 
    created a ``StyleTK`` class to apply the same color and style to 
    these legacy widgets. While these legacy widgets are not 
    necessarily intended to be used (and will probably not look as 
    nice as the ttk versions when they exist), they are available if 
    needed, and shouldn't look completely out-of-place in your 
    ttkbootstrap themed application.  
    :ref:`Check out this example <themes:legacy widget styles>` to 
    see for yourself.

    .. _Bootswatch: https://bootswatch.com/

"""
from ttkbootstrap.style.style import Style
from ttkbootstrap.style import bootstyle
from ttkbootstrap.widgets import *
bootstyle.setup_ttkbootstap_api()
