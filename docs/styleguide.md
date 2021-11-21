# Style Guide

This is a style guide for applying ttkbootstrap styles. All ttkbootstrap styles
are applied using the `bootstyle` parameter that has been injected into the
`ttk` widget constructor.

As this is a style guide, you will need to consult the references at the bottom
of each widget section for information on how to _use_ the widget and to determine
what ttk option are available. 

## Colors

The following color options are available on all widgets, except where excluded,
and can be used along with widget specific style keywords which are described for
each widget. Keywords are not required for default styles. 

The actual color value of the color keywords are defined in each specific theme, 
but the descriptions below are what you can expect typically from each color keyword.

| Keyword      | Description                           | Example |
| ---          | ---                                   | ---      |
| `primary`    | The default color for most widgets    | ![primary](./assets/colors/primary.png) |
| `secondary`  | Typically a _gray_ color              | ![secondary](./assets/colors/secondary.png) |
| `success`    | Typically a _green_ color             | ![success](./assets/colors/success.png) |
| `info`       | Typically a _blue_ color              | ![info](./assets/colors/info.png) |
| `warning`    | Typically an _orange_ color           | ![warning](./assets/colors/warning.png) |
| `danger`     | Typically a _red_ color               | ![danger](./assets/colors/danger.png) |
| `light`      | Typically a _light gray_ color        | ![light](./assets/colors/light.png) |
| `dark`       | Typically a _dark gray_ color         | ![dark](./assets/colors/dark.png) |


```python
# info colored button style
Button(bootstyle="info")

# warning colored scale style
Scale(bootstyle="warning")

# success colored progressbar
Progressbar(bootstyle="success")
```

---
## Button

ttkbootstrap includes many predefined button styles that provide quick 
access to a varied color palette and semantic meaning to your application
design.

### Solid buttons (default)

A solid background color that lightens on _hover_ and darkens on _press_. When
the widget has focus, a dashed focus ring appears in the same color as the
text foreground.

![solid button](./assets/widget-styles/solid-buttons.gif)

```python
# default style
Button()

# success style
Button(bootstyle="success")
```

### Outline buttons

A thin outline with a background color that matches the theme default. When the
widget has focus, a dashed focus ring appears in the same color as the text 
foreground.

![outline buttons](./assets/widget-styles/outline-buttons.gif)

```python
# default outline style
Button(bootstyle="outline")

# success outline style
Button(bootstyle="success-outline")
```

### Link buttons

A button with the appearance of a label. The text color changes to **info** on 
_hover_. When the widget has focus, a dashed focus ring appears in the same color 
as the foreground. 

![link buttons](./assets/widget-styles/link-buttons.gif)

```python
# default link style
Button(bootstyle="link")

# success link style
Button(bootstyle="success-link")
```

---
## Checkbutton

ttkbootstrap includes many types of checkbutton styles. In addition to the
traditional checkbutton and toolbutton styles, round and square toggle buttons
have been added.

### Checkbutton (default)

A standard checkbutton which displays a checkmark when invoked. The indicator
color is set by the selected color keyword.

![checkbutton](./assets/widget-styles/checkbuttons.gif)

```python
# default checkbutton style
Checkbutton()

# success checkbutton style
Checkbutton(bootstyle="success")
```

### Toolbutton

A solid color button with a background that alternates between colors when invoked.
The _off_ state color is always the **secondary** color of the selected theme. The 
_on_ state color is based on the [color keyword](#colors) as indicated below.

![solid toolbuttons](./assets/widget-styles/solid-toolbuttons.gif)

```python
# default toolbutton style
Checkbutton(bootstyle="toolbutton")

# success toolbutton style
Checkbutton(bootstyle="success-toolbutton")
```

### Outline toolbutton

A thin outlined button with a background color that alternates between the theme
background color and the outline color. The _on_ state color is based on the 
[color keyword](#colors) as indicated below.

![outline toolbuttons](./assets/widget-styles/outline-toolbuttons.gif)

```python
# default outline toolbutton style
Checkbutton(bootstyle="outline-toolbutton")

# success outline toolbutton style
Checkbutton(bootstyle="success-outline-toolbutton")
```

### Round toggle button

A rounded toggle button with an indicator that shifts left and right as it is toggled
on and off. The background color alternates between the theme background color and
the [color keyword](#colors) as indicated below.

![round toggles](./assets/widget-styles/round-toggles.gif)

```python
# default round toggle style
Checkbutton(bootstyle="round-toggle")

# success round toggle style
Checkbutton(bootstyle="success-round-toggle")
```

### Square toggle button

A square toggle button with an indicator that shifts left and right as it is toggled
on and off. The background color alternates between the theme background color and
the [color keyword](#colors) as indicated below.

![square toggles](./assets/widget-styles/square-toggles.gif)

```python
# default square toggle style
Checkbutton(bootstyle="square-toggle")

# success square toggle style
Checkbutton(bootstyle="success-square-toggle")
```

---
## Combobox

By default, the combobox widget has a light colored border. On _hover_ this border
changes to a thin **primary** color by default or the selected [color](#colors). 
On _focus_ the border becomes twice a thick.

![combobox](./assets/widget-styles/combos.gif)

```python
# default combobox style
Combobox()

# danger colored combobox style
Combobox(bootstyle="danger")
```

---
## DateEntry

This widget is composed of two widgets, the `Entry` widget and the `Button` 
widget. Both the `Entry` widget and the `Button` widget use the same default
styles as their independent versions.

The [DatePickerPopup](#datepickerpopup) is invoked when the calendar
button is pressed. The default color applied to the popup is **primary**.

![date entries](./assets/widget-styles/date-entries.gif)

```python
# default dateentry
DateEntry()

# success colored dateentry
DateEntry(bootstyle="success")
```

---
## DatePickerPopup

By default, this widget uses the `primary` color for the _header_ and
_active date_. The _weekdays header_ and _current date_ use the `secondary`
color by default.

**add detail here**

![date picker](./assets/widget-styles/date-picker-popup.gif)

```python
# default popup
DatePickerPopup()

# warning colored popup
DatePickerPopup(bootstyle="warning")
```

---
## Entry

**add detail here**

![entry](./assets/widget-styles/entries.gif)

```python
# default entry style
Entry()

# danger colored entry style
Entry(bootstyle="danger")
```

---
## Floodgauge

**add detail here**

![floodguage](./assets/widget-styles/floodgauge.gif)

```python
# default floodgauge style
Floodgauge()

# success colored floodguage style
Floodgauge(bootstyle="success")
```

---
## Frame

**add detail here**

![frame](./assets/widget-styles/frame.png)

```python
# default frame style
Frame()

# info colored frame style
Frame(bootstyle="info")
```

---
## Label

**add detail here**

### Normal (default)
![normal label](./assets/widget-styles/label.png)

### Inverse
![inverse label](./assets/widget-styles/inverse-label.png)

```python
# default label style
Label()

# danger colored label style
Label(bootstyle="danger")

# default inverse label style
Label(bootstyle="inverse")

# danger colored inverse label style
Label(bootstyle="inverse-danger")
```

---
## Labelframe

**add detail here**

![labelframe](./assets/widget-styles/labelframe.png)

```python
# default labelframe style
Labelframe()

# info colored labelframe style
Labelframe(bootstyle="info")
```

## Menubutton

**add detail here**

### Solid (default)

**add detail here**

![solid menubutton](./assets/widget-styles/menubutton.gif)

### Outline

**add detail here**

![outline menubutton](./assets/widget-styles/outline-menubutton.gif)

```python
# default solid menubutton style
Menubutton()

# success colored solid menubutton style
Menubutton(bootstyle="success")

# default outline menubutton style
Menubutton(bootstyle="outline")

# info colored outline menubutton style
Menubutton(bootstyle="info-outline")
```

## Meter

By default, the background color for this widget is the same as the theme 
background color, the _indicator_ and _text_ are set to `primary`. 
The _subtext_ is set to `secondary` if the theme is _light_ or `selectbg` 
if the theme is _dark_, which is a color not accessible via keywords. 

In the widget constructor, use the `bootstyle` parameter to customize the 
_indicator_ and _text_ element colors. Use the `subtextstyle` to customize 
the _subtext_ element color.

![meter](./assets/widget-styles/meter.png)

```python
# default meter style
Meter()

# info colored meter
Meter(bootstyle="info")

# danger color subtext
Meter(subtextstyle="danger")

# success colored meter with warning colored subtext
Meter(bootstyle="success", subtextstyle="warning")
```

## Notebook

**add detail here**

![notebook](./assets/widget-styles/notebook.png)

```python
# default notebook style
Notebook()

# info colored notebook style - inactive tab color
Notebook(bootstyle="info")
```

## Panedwindow

**add detail here**

![paned widow](./assets/widget-styles/panedwindow.gif)

```python
# default panedwindow style
Panedwindow()

# info colored panedwindow style
Panedwindow(bootstyle="info")
```

## Progressbar

**add detail here**

### Solid (default)

**add detail here**

![solid progressbar](./assets/widget-styles/solid-progressbar.gif)

### Striped

**add detail here**

![striped progressbar](./assets/widget-styles/striped-progressbar.gif)

```python
# default solid progressbar style
Progressbar()

# success colored solid progressbar style
Progressbar(bootstyle="success")

# default striped progressbar style
Progressbar(bootstyle="striped")

# danger colored striped progressbar style
Progressbar(bootstyle="danger-striped")
```

## Radiobutton

**add detail here**

### Radio (default)

**add detail here**

![radiobutton](./assets/widget-styles/radiobutton.gif)

### Solid toolbutton

**add detail here**

![toolbutton](./assets/widget-styles/radio-toolbutton.gif)

### Outline toolbutton

**add detail here**

![outline toolbutton](./assets/widget-styles/outline-radio-toolbutton.gif)

```python
# default radiobutton style
Radiobutton()

# secondary colored radiobutton style
Radiobutton(bootstyle="secondary")

# default toolbutton style
Radiobutton(bootstyle="toolbutton")

# danger colored radio toolbutton style
Radiobutton(bootstyle="danger-toolbutton")

# default outline radio toolbutton style
Radiobutton(bootstyle="outline-toolbutton")

# info colored outline radio toolbutton style
Radiobutton(bootstyle="info-outline-toolbutton")
```

## Scale

**add detail here**

![scale](./assets/widget-styles/scale.gif)

```python
# default Scale style
Scale()

# info colored label style
Scale(bootstyle="info")
```

## Scrollbar

**add detail here**

### Square (default)
**add detail here**
![scrollbar](./assets/widget-styles/square-scrollbars.gif)

### Round
**add detail here**
![round scrollbar](./assets/widget-styles/round-scrollbars.gif)

```python
# default scrollbar style
Scrollbar()

# success colored default scrollbar style
Scrollbar(bootstyle="success")

# default round scrollbar style
Scrollbar(bootstyle="round")

# danger colored round scrollbar style
Scrollbar(bootstyle="danger-round")
```

## Separator
**add detail here**
![separator](./assets/widget-styles/separator.png)

```python
# default separator style
Separator()

# info colored separator style - handle color
Separator(bootstyle="info")
```

## Sizegrip
**add detail here**
![sizegrip](./assets/widget-styles/sizegrip.gif)

```python
# default separator style
Sizegrip()

# info colored separator style - handle color
Sizegrip(bootstyle="info")
```

## Spinbox
**add detail here**
![spinbox](./assets/widget-styles/spinbox.gif)

```python
# default spinbox style
Spinbox()

# danger colored spinbox style
Spinbox(bootstyle="danger")
```

## Treeview

**add detail here**

![treeview](./assets/widget-styles/treeview.gif)

```python
# default Treeview style
Treeview()

# info colored treeview style
Treeview(bootstyle='info')
```


