# Style Guide

This is a style guide for applying ttkbootstrap styles. All ttkbootstrap styles
are applied using the **bootstyle** parameter that has been injected into the
**ttk** widget constructor.

## Colors

The following color options are available on _all_ widgets, except where 
excluded, and can be used along with widget specific style keywords which 
are described for each widget. Keywords are not required for default styles. 

The actual color value of the keywords below are 
[defined in each specific theme](themes.md#how-are-themes-created), but the 
descriptions below are what you can expect typically from each color keyword.

| Keyword      | Description                           | Example |
| ---          | ---                                   | ---      |
| primary    | The default color for most widgets    | ![primary](./assets/colors/primary.png) |
| secondary  | Typically a _gray_ color              | ![secondary](./assets/colors/secondary.png) |
| success    | Typically a _green_ color             | ![success](./assets/colors/success.png) |
| info       | Typically a _blue_ color              | ![info](./assets/colors/info.png) |
| warning    | Typically an _orange_ color           | ![warning](./assets/colors/warning.png) |
| danger     | Typically a _red_ color               | ![danger](./assets/colors/danger.png) |
| light      | Typically a _light gray_ color        | ![light](./assets/colors/light.png) |
| dark       | Typically a _dark gray_ color         | ![dark](./assets/colors/dark.png) |


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

This widget features a variety of button style types that have a **primary**
color by default, or the [selected color](#colors).

This widget supports a special style for [disabled state](#other-button-styles).

### Solid button (default)

The default style features a solid background that lightens on _hover_ and 
darkens when _pressed_. A dashed ring appears inside the button when the widget
has focus.

![solid button](./assets/widget-styles/solid-buttons.gif)

```python
# default style
Button()

# success style
Button(bootstyle="success")
```

### Outline button

This style features a thin styled outline. When _pressed_ or on _hover_, the
button changes to a solid color similar to the default button style. A dashed
ring appears inside the button when the widget has focus.

![outline buttons](./assets/widget-styles/outline-buttons.gif)

```python
# default outline style
Button(bootstyle="outline")

# success outline style
Button(bootstyle="success-outline")
```

### Link button

This style features a button with the appearance of a label. The text color changes
to **info** on _hover_ or when _pressed_ to simulate the effect you would expect on
an HTML hyperlink. There is a slight shift-relief when the button is pressed that 
gives the appearance of movement. A dashed ring appears inside the button when the
widget has focus.

![link buttons](./assets/widget-styles/link-buttons.gif)

```python
# default link style
Button(bootstyle="link")

# success link style
Button(bootstyle="success-link")
```

### Other button styles

##### Disabled button
This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the button in a disabled state
Button(state="disabled")

# disable a button after creation
b = Button()
b.configure(state="disabled")
```

---
## Checkbutton

This widget features a variety of checkbutton style types that are **primary**
colored by default or the [selected color](#colors).

This widget supports a special style for 
[disabled state](#other-checkbutton-styles).

### Checkbutton (default)

The default style features a square checkbox and label. The checkbox has a
muted color outline when not selected, and a filled square with checkmark when
selected.

![checkbutton](./assets/widget-styles/checkbuttons.png)

```python
# default checkbutton style
Checkbutton()

# success checkbutton style
Checkbutton(bootstyle="success")
```

### Toolbutton

This style features a solid rectangular button that toggles between an _off_ 
and _on_ color. The background is a muted gray when _off_ and a default
or [selected color](#colors) when _on_ or _active_.

![solid toolbuttons](./assets/widget-styles/solid-toolbuttons.gif)

```python
# default toolbutton style
Checkbutton(bootstyle="toolbutton")

# success toolbutton style
Checkbutton(bootstyle="success-toolbutton")
```

### Outline toolbutton

This style features a rectangular button that toggles between a styled 
**outline** when _off_ and a **solid** background when _on_ or 
_active_.

![outline toolbuttons](./assets/widget-styles/outline-toolbuttons.gif)

```python
# default outline toolbutton style
Checkbutton(bootstyle="outline-toolbutton")

# success outline toolbutton style
Checkbutton(bootstyle="success-outline-toolbutton")
```

### Round toggle button

This style features a rounded button with a **round** indicator that changes
color and position when toggled _off_ and _on_. The button is a muted outline
with a muted color indicator when _off_. The button is filled with the default
or [selected color](#colors) with an accented indicator when _on_.

![round toggles](./assets/widget-styles/round-toggles.gif)

```python
# default round toggle style
Checkbutton(bootstyle="round-toggle")

# success round toggle style
Checkbutton(bootstyle="success-round-toggle")
```

### Square toggle button

This style features a squared button with a **square** indicator that changes
color and position when toggled _off_ and _on_. The button is a muted outline
with a muted color indicator when _off_. The button is filled with the default
or [selected color](#colors) with an accented indicator when _on_.

![square toggles](./assets/widget-styles/square-toggles.gif)

```python
# default square toggle style
Checkbutton(bootstyle="square-toggle")

# success square toggle style
Checkbutton(bootstyle="success-square-toggle")
```

### Other checkbutton styles

##### Disabled checkbutton
This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the checkbutton in a disabled state
Checkbutton(state="disabled")

# disable a checkbutton after creation
cb = Checkbutton()
cb.configure(state="disabled")
```

---
## Combobox

This widget style features a input box with a styled border and arrow. The 
border color is muted by default and changes to **primary** or the 
[selected color](#colors) on _hover_. The border increases in thickness on 
_focus_. The arrow color changes to the default or [selected color](#colors) 
on _hover_ or on _focus_.

This widget also supports special styles for [disabled state](#disabled-combobox), 
[readonly state](#readonly-combobox), and [invalid state](#invalid-combobox).

![combobox](./assets/widget-styles/combos.gif)

```python
# default combobox style
Combobox()

# danger colored combobox style
Combobox(bootstyle="danger")
```

### Other combobox styles

##### Disabled combobox

This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the combobox in a disabled state
Combobox(state="disabled")

# disable a combobox after creation
cb = Combobox()
cb.configure(state="disabled")
```

##### Readonly combobox

This style _cannot be applied via keywords_; it is configured through widget 
settings.


```python
# create the combobox in a readonly state
Combobox(state="readonly")

# set the combobox readonly state after creation
cb = Combobox()
cb.configure(state="readonly")
```

##### Invalid combobox

This style _cannot be applied via keywords_, but rather is the result of a 
validation process implemented on the widget. In the **Cookbook** you will find 
an example of [how to apply validation](cookbook.md#validate-user-input) to an 
`Entry` based widget.

---
## DateEntry

This widget is composed of two widgets, the **Entry** widget and the **Button**
widget. The **Entry** component behaves identically to the 
[default entry widget](#entry), and the calendar button behaves as the 
[default solid button](#button).

The [DatePickerPopup](#datepickerpopup) is invoked when the calendar
button is pressed. The default color applied to the popup is **primary**.

This widget also supports special styles for [disabled state](#disabled-date-entry), 
[readonly state](#readonly-date-entry),  and [invalid state](#invalid-date-entry).

![date entries](./assets/widget-styles/date-entries.gif)

```python
# default date entry
DateEntry()

# success colored date entry
DateEntry(bootstyle="success")
```

### Other date entry styles

##### Disabled date entry

This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the date entry in a disabled state
DateEntry(state="disabled")

# disable a date entry after creation
d = DateEntry()
d.configure(state="disabled")
```

##### Readonly date entry

This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the date entry in a readonly state
DateEntry(state="readonly")

# set the date entry readonly state after creation
d = DateEntry()
d.configure(state="readonly")
```

##### Invalid date entry

This style _cannot be applied via keywords_, but rather is the result of a 
validation process implemented on the widget. In the **Cookbook** you will find 
an example of [how to apply validation](cookbook.md#validate-user-input) to an 
`Entry` based widget.

---
## DatePickerPopup

This widget style encomposses a collection of button and label widgets. The 
_header_ and _active date_ are **primary** colored (default) or the 
[selected color](#colors). The _weekdays header_ and _current date_ use the 
`secondary` color.

![date picker](./assets/widget-styles/date-picker-popup.gif)

```python
# default popup
DatePickerPopup()

# warning colored popup
DatePickerPopup(bootstyle="warning")
```

---
## Entry

This widget style features a input box with a styled border. The border color 
is muted by default and changes to **primary** or the [selected color](#colors) 
on _hover_. The border increases in thickness on _focus_. 

This widget also supports special styles for [disabled state](#disabled-entry), 
[readonly state](#readonly-entry), and [invalid state](#invalid-entry).

![entry](./assets/widget-styles/entries.gif)

```python
# default entry style
Entry()

# danger colored entry style
Entry(bootstyle="danger")
```

### Other entry styles

##### Disabled entry

This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the widget in a disabled state
Entry(state="disabled")

# disable the widget after creation
e = Entry()
e.configure(state="disabled")
```

##### Readonly entry

This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the widget in a readonly state
Entry(state="readonly")

# set the widget readonly state after creation
e = Entry()
e.configure(state="readonly")
```

##### Invalid entry

This style _cannot be applied via keywords_, but rather is the result of a 
validation process implemented on the widget. In the **Cookbook** you will find 
an example of [how to apply validation](cookbook.md#validate-user-input) to an 
`Entry` based widget.

---
## Floodgauge

A progressbar with an optional display text.

This widget style features an indicator that is **primary** colored (default) 
or the [selected color](#colors). The trough color is a desaturated variation 
of the indicator color. 

![floodguage](./assets/widget-styles/floodgauge.gif)

```python
# default floodgauge style
Floodgauge()

# success colored floodguage style
Floodgauge(bootstyle="success")
```

---
## Frame

This widget style features a default background color that matches the theme
background by default, or the [selected color](#colors).

![frame](./assets/widget-styles/frame.png)

```python
# default frame style
Frame()

# info colored frame style
Frame(bootstyle="info")
```

---
## Label

This widget features two style types that can both be customized using any of
the [available colors].

### Default label

The default style features a default theme defined foreground and background
color. The foreground can be changed using a [selected color](#colors).

![normal label](./assets/widget-styles/label.png)

```python
# default label style
Label()

# danger colored label style
Label(bootstyle="danger")
```

### Inverse label

This style features a label with colors that are inverted versions of the default
colors. The [selected color](#colors) changes the background color instead of the
foreground color. 

This is especially useful when you are adding labels to a styled `Frame`, or you 
want to add a [label heading](gallery.md#media-player) that does not have a default 
background color.

![inverse label](./assets/widget-styles/inverse-label.png)

```python
# default inverse label style
Label(bootstyle="inverse")

# danger colored inverse label style
Label(bootstyle="inverse-danger")
```

---
## Labelframe

This widget style features a styled border and label. By default, the border 
and label use theme defined defaults for border and foreground colors. When a
[selected color](#colors) is used, both the label text and the border use this
color.

![labelframe](./assets/widget-styles/labelframe.png)

```python
# default labelframe style
Labelframe()

# info colored labelframe style
Labelframe(bootstyle="info")
```

## Menubutton

This widget features a styled button with an arrow that can be styled using
any of the [available colors](#colors). 

This widget supports a special style for [disabled state](#disabled-menubutton).

### Solid (default)

This widget style features a solid background color that lightens on _hover_ 
and darkens when _pressed_. 

![solid menubutton](./assets/widget-styles/menubutton.gif)

```python
# default solid menubutton style
Menubutton()

# success colored solid menubutton style
Menubutton(bootstyle="success")
```

### Outline

This style features a thin styled outline. When _pressed_ or on _hover_, the
button changes to a solid color similar to the default menubutton style. 

![outline menubutton](./assets/widget-styles/outline-menubutton.gif)

```python
# default outline menubutton style
Menubutton(bootstyle="outline")

# info colored outline menubutton style
Menubutton(bootstyle="info-outline")
```

### Other menubutton styles

##### Disabled menubutton
This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the menubutton in a disabled state
Menubutton(state="disabled")

# disable a menubutton after creation
b = Menubutton()
b.configure(state="disabled")
```

## Meter

This widget style encompasses a collection of components. The indicator and 
main label are **primary** by default, or the [selected color](#colors).
If provided, the subtext is **secondary** for light themes and **light** for 
dark themes. However, all of these elements can be configured using the 
[available colors](#colors).

![meter colors](./assets/widget-styles/meter.gif)

The meter widget is highly configurable, and can produce a diversity of
interesting meters by mixing colors and other widget specific settings.

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

This widget style features minimal styling by default. However, you can add some
flair to the _inactive_ tab by using any of the [available colors](#colors) as 
demonstrated in the exhibit below.

![notebook](./assets/widget-styles/notebook.png)

```python
# default notebook style
Notebook()

# info colored notebook style - inactive tab color
Notebook(bootstyle="info")
```

## Panedwindow

This widget style features containers with the themed defined background color 
separated by a styled sash that is grayish by default or of the
[selected color](#Colors).

![paned widow](./assets/widget-styles/panedwindow.gif)

```python
# default panedwindow style
Panedwindow()

# info colored panedwindow style
Panedwindow(bootstyle="info")
```

## Progressbar

This widget features a few style types that have **primary** colored indicator
bars by default, but can by styled using any of the [available colors](#colors).

### Solid (default)

The default widget style features a solid color indicator bar.

![solid progressbar](./assets/widget-styles/solid-progressbar.gif)

```python
# default solid progressbar style
Progressbar()

# success colored solid progressbar style
Progressbar(bootstyle="success")
```


### Striped

This widget style features a striped indicator bar that uses the default or 
[selected color](#colors) for the main color, and a desaturated version of
this color for the alternating stripe.

![striped progressbar](./assets/widget-styles/striped-progressbar.gif)

```python
# default striped progressbar style
Progressbar(bootstyle="striped")

# danger colored striped progressbar style
Progressbar(bootstyle="danger-striped")
```

## Radiobutton

This widget features a variety of radiobutton style types that are **primary**
colored by default or the [selected color](#colors).

This widget supports a special style for 
[disabled state](#other-radiobutton-styles).

### Radio (default)

The default widget style features the traditional **radiobutton** which has a
round indicator. The indicator is filled with the default or selected color 
when in a _selected state_.

![radiobutton](./assets/widget-styles/radiobuttons.png)

```python
# default radiobutton style
Radiobutton()

# secondary colored radiobutton style
Radiobutton(bootstyle="secondary")
```

### Solid toolbutton

This style features a solid rectangular button that has a muted gray background
when _not selected_ and a default or [selected color](#colors) when _selected_
or _active_.

![toolbutton](./assets/widget-styles/radio-toolbutton.gif)

```python
# default toolbutton style
Radiobutton(bootstyle="toolbutton")

# danger colored radio toolbutton style
Radiobutton(bootstyle="danger-toolbutton")
```

### Outline toolbutton

This style features a rectangular button that has an **outline** 
when _not selected_ and a **solid** background when _selected_ or 
_active_.

![outline toolbutton](./assets/widget-styles/outline-radio-toolbutton.gif)

```python
# default outline radio toolbutton style
Radiobutton(bootstyle="outline-toolbutton")

# info colored outline radio toolbutton style
Radiobutton(bootstyle="info-outline-toolbutton")
```

### Other radiobutton styles

##### Disabled radiobutton
This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the radiobutton in a disabled state
Radiobutton(state="disabled")

# disable a radiobutton after creation
rb = Radiobutton()
rb.configure(state="disabled")
```

## Scale

This widget style features a thin gray trough with a round slider handle that is 
**primary** color by default or the [selected color](#colors). The 
slider handle lightens on _hover_ and darkens when _pressed_. 

This widget supports a special style for 
[disabled state](#other-scale-styles).

![scale](./assets/widget-styles/scale.gif)

```python
# default Scale style
Scale()

# info colored label style
Scale(bootstyle="info")
```

### Other scale styles

##### Disabled scale
This style _cannot be applied via keywords_; it is configured through widget 
settings.

```python
# create the scale in a disabled state
Scale(state="disabled")

# disable a scale after creation
scale = Scale()
scale.configure(state="disabled")
```

## Scrollbar

This widget style features a light gray trough with a styled thumb and arrow 
buttons. The thumb and arrows lighten on _hover_ and darken on _press_. The
thumb and arrows can be styled with any of the [available colors](#colors). 

### Square (default)

The default style features a thumb with squared edges.

![scrollbar](./assets/widget-styles/square-scrollbars.png)

```python
# default scrollbar style
Scrollbar()

# success colored default scrollbar style
Scrollbar(bootstyle="success")
```

### Round

The **round** style features a thumb with rounded edges.

![round scrollbar](./assets/widget-styles/round-scrollbars.png)

```python
# default round scrollbar style
Scrollbar(bootstyle="round")

# danger colored round scrollbar style
Scrollbar(bootstyle="danger-round")
```

## Separator

This widget style features a thin horizontal _or_ vertical line drawn in the 
default color (typically gray) or the [selected color](#colors).

![separator](./assets/widget-styles/separator.png)

```python
# default separator style
Separator()

# info colored separator style - handle color
Separator(bootstyle="info")
```

## Sizegrip

This widget style features a pattern of squares in a default muted color
by default, or the [selected color](#colors).

![sizegrip](./assets/widget-styles/sizegrip.gif)

```python
# default separator style
Sizegrip()

# info colored separator style - handle color
Sizegrip(bootstyle="info")
```

## Spinbox

This widget style features a input box with a styled border and arrows. The 
border color is muted by default and changes to **primary** or the 
[selected color](#colors) on _hover_. The border increases in thickness on 
_focus_. The arrow color changes to the default or [selected color](#colors) 
on _hover_ or on _focus_.

This widget also supports special styles for [disabled state](#disabled-spinbox), 
[readonly state](#readonly-spinbox), and [invalid state](#invalid-combobox).

![spinbox](./assets/widget-styles/spinbox.gif)

```python
# default spinbox style
Spinbox()

# danger colored spinbox style
Spinbox(bootstyle="danger")
```

### Other styles

##### Disabled spinbox

This widget supports a style reserved for the **disabled** state, which you 
can see in the exhibit above. This style _cannot be applied via keywords_. To 
apply the disabled style:

```python
# create the widget in a disabled state
Spinbox(state="disabled")

# disable the widget after creation
e = Spinbox()
e.configure(state="disabled")
```

##### Readonly spinbox

This widget supports a style reserved for the **readonly** state, which you 
can see in the exhibit above. This style _cannot be applied via keywords_.  To 
apply the readonly style:

```python
# create the widget in a readonly state
Spinbox(state="readonly")

# set the widget readonly state after creation
e = Spinbox()
e.configure(state="readonly")
```

##### Invalid spinbox

This style _cannot be applied via keywords_, but rather is the result of a 
validation process implemented on the widget. In the **Cookbook** you will find 
an example of [how to apply validation](cookbook.md#validate-user-input) to an 
`Entry` based widget.

## Treeview

This widget style features a solid background header that is the default theme
background by default or the [selected color](#colors). 

The border color is muted by default and changes to **primary** or the 
[selected color](#colors) on _hover_. The border increases in thickness on 
_focus_. 

![treeview](./assets/widget-styles/treeview.gif)

```python
# default Treeview style
Treeview()

# info colored treeview style
Treeview(bootstyle='info')
```


