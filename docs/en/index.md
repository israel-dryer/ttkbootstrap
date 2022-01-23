# ttkbootstrap
![](https://img.shields.io/github/release/israel-dryer/ttkbootstrap.svg)
[![Downloads](https://pepy.tech/badge/ttkbootstrap)](https://pepy.tech/project/ttkbootstrap)
[![Downloads](https://pepy.tech/badge/ttkbootstrap/month)](https://pepy.tech/project/ttkbootstrap)
![](https://img.shields.io/github/issues/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/issues-closed/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/license/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/stars/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/forks/israel-dryer/ttkbootstrap.svg)

A supercharged theme extension for tkinter that enables on-demand modern 
flat style themes inspired by [Bootstrap](https://getbootstrap.com/).

## 📦 Features

✔️ [**Built-in Themes**](themes/index.md)   
Over a dozen curated [dark](themes/dark.md) and [light](themes/light.md) themes  

✔️ [**Pre-defined Styles:**](styleguide/index.md)  
Loads of beautiful [pre-defined widget styles](styleguide/index.md) such 
as **outline** and **round toggle** buttons.

✔️ [**Simple keyword API:**](gettingstarted/tutorial/#use-themed-widgets)  
Apply colors and types using [simple keywords](gettingstarted/tutorial/#use-themed-widgets) 
such as **primary** and **striped** instead of the legacy approach of 
**primary.Striped.Horizontal.TProgressbar**. If you've used Bootstrap for
web development, you are already familiar with this approach using css classes.

✔️ [**Lots of new Widgets:**](api/widgets/dateentry)  
ttkbootstrap comes with several new beautifully designed widgets such 
as [Meter](api/widgets/meter), [DateEntry](api/widgets/dateentry), 
and [Floodgauge](api/widgets/floodgauge). Additionally, [dialogs](api/dialogs/dialog) 
are now themed and fully customizable.

✔️ [**Built-in Theme Creator:**](themes/themecreator.md)  
Want to create your own theme? Easy! ttkbootstrap includes a built-in 
[theme creator](themes/themecreator.md) that enables you to easily build, 
load, expore, and apply your own custom themes.

!!! warning "Breaking changes in 1.0"
    Version 1.0 is a complete rebuild of the library. If you are using [version 0.5](https://github.com/israel-dryer/ttkbootstrap/tree/version-0.5) you may run into issues trying to import themes with the themes.json as this has been removed from 1.0. You can now import and save themes directly using the ttkcreator.


## 🎨 Sample Themes

![themes](./assets/themes/themes.gif)
