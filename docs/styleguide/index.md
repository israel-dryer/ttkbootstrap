# Style guide

This is a style guide for applying ttkbootstrap styles. All ttkbootstrap styles
are applied using the **bootstyle** parameter that has been injected into the
**ttk** widget constructor.

ℹ️ [Learn more about styling legacy widgets](legacywidgets.md).

## Colors

The following color options are available on _all_ widgets, except where 
excluded, and can be used along with widget specific style keywords which 
are described for each widget. Keywords are not required for default styles. 

The actual color value of the keywords below are 
[defined in each specific theme](../themes/definitions.md), but the 
descriptions below are what you can expect typically from each color keyword.

| Keyword      | Description                           | Example |
| ---          | ---                                   | ---      |
| primary    | The default color for most widgets    | ![primary](../assets/colors/primary.png) |
| secondary  | Typically a _gray_ color              | ![secondary](../assets/colors/secondary.png) |
| success    | Typically a _green_ color             | ![success](../assets/colors/success.png) |
| info       | Typically a _blue_ color              | ![info](../assets/colors/info.png) |
| warning    | Typically an _orange_ color           | ![warning](../assets/colors/warning.png) |
| danger     | Typically a _red_ color               | ![danger](../assets/colors/danger.png) |
| light      | Typically a _light gray_ color        | ![light](../assets/colors/light.png) |
| dark       | Typically a _dark gray_ color         | ![dark](../assets/colors/dark.png) |


```python
# info colored button style
Button(bootstyle="info")

# warning colored scale style
Scale(bootstyle="warning")

# success colored progressbar
Progressbar(bootstyle="success")
```