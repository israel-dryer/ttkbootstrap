# About this project
  
I set the following goals for myself when creating and updating this project;
especially for version 1.0. It is a work in progress, but hopefully I've 
achieved most or all of these.

## Create a set of beautifully designed and easy-to-use styles

As you may know, creating ttk styles can be _very time-consuming_. This library 
takes the pain out of creating a modern look and feel so that you can focus on 
_designing your application_ instead of adjusting 25 style settings on a submit 
button.

## Set the widget style with keywords

Keep it simple. Set styles with keywords. Instead of using ttk style 
classes such as **success.Horizontal.TProgressbar**, use **success**, 
which is a keyword that can indicate the same semantic meaning for _all_ 
widgets.

Many people are familiar with bootstrap for web development which comes 
pre-packaged with built-in css style classes that provide a professional and 
consistent api for quick development. I took a similar approach with this 
project by pre-defining styles for nearly all ttk widgets and by enabling
style customization with _simple keywords_.

## Only create themes and styles that are actually used

If you're not using it, then it shouldn't be taking up memory in your
application. Nothing bogs down your application more than a bunch of 
boilerplate assets that you may or may not use. 

To fix this, I've designed a styling engine for ttk that builds ttk styles and 
themes _on demand_. If a style is not used, it will not be created. This adds a 
tremendous amount of flexibility in theme and style design as I am no longer 
limited by the memory limits of _pre-loaded image-based widget styles_. 

To put this into perspective... in version 0.5, if I had a single scale widget 
in my application, I would need to load 288 images to account for all potential 
theme and color combinations!! This is how styles are handled traditionally in 
ttk. In version 1.0, I only need to load 3 or 4 images for this example to 
account for hover effects, etc...  Only the styles actually used are built. 
