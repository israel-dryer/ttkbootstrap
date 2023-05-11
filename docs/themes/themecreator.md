# TTK Creator

TTK Creator is packaged with ttkbootstrap so that you can modify, save, 
export, and import themes that you have created.

To run the program, type the following command in the console _after_ you
have installed **ttkbootstrap**:

```shell
python -m ttkcreator
```

![creator](../assets/ttkcreator/creator.png)

## Create a new theme

All of the controls for changing the theme are on the left-side control 
frame. 

1. Name your theme using the **name** entry

2. Select a **base theme**; this will setup the _initial_ colors

3. Select a color for each color _keyword_ using one of two options
    
    * Click the 🎨 button to choose a color from the color dialog
    * Or, type a _hexadecimal_ or valid color _name_ 

4. Click the **Save** button

Your theme is now saved in the file `ttkbootstrap.themes.user.py`

!!! tip "Reset your theme"
    If you want to reset your color choices, you can click the 
    **Reset** option from the top menu to reset all of the colors
    to the **base theme** colors.

## Import TTK Creator themes

If you have a user themes file that is in the format specified below, you can 
import that file into ttkbootstrap. 

1. Click the **Import** button on the top menu

2. Select the themes file you wish to import, then click **Ok** to import

!!! warning
    Importing a user themes file will overwrite the existing user defined
    themes within ttkbootstrap; so make sure you **export** your existing
    theme set if you wish to keep it

The `user.py` file contains a dictionary of user defined themes. The file that
you import must match the pattern illustrated below.

```python
USER_THEMES = {
    "supercosmo": {
        "type": "light",
        "colors": {
            "primary": "#2780e3",
            "secondary": "#7E8081",
            "success": "#3fb618",
            "info": "#9954bb",
            "warning": "#ff7518",
            "danger": "#ff0039",
            "light":"#F8F9FA",
            "dark": "#373A3C",
            "bg": "#ffffff",
            "fg": "#373a3c",
            "selectbg": "#7e8081",
            "selectfg": "#ffffff",
            "border": "#ced4da",
            "inputfg": "#373a3c",
            "inputbg": "#fdfdfe"
        }
    }
}
```


## Import User Themes from JSON

You can import themes using the `Style.load_user_themes` method. Importing themes
with this method only affects the project at run-time and does not change the
ttkbootstrap source files as does the previous example. This is handy if you have
themes stored in JSON format, or if you want a theme available for a specific project
but not others, etc...

The format of the JSON file must match the following:
```json
{
  "themes": [
    {
      "midnight": {
        "type": "dark",
        "colors": {
          "primary": "#0a21f5",
            "secondary": "#555555",
            "success": "#77b300",
            "info": "#c6c6c6",
            "warning": "#ff8800",
            "danger": "#cc0000",
            "light": "#adafae",
            "dark": "#000000",
            "bg": "#000000",
            "fg": "#ffffff",
            "selectbg": "#454545",
            "selectfg": "#ffffff",
            "border": "#060606",
            "inputfg": "#ffffff",
            "inputbg": "#191919",
            "active": "#282828"
        }
      }
    },
    {
      "nightout": {
        "type": "dark",
        "colors": {
          "primary": "#164fe2",
            "secondary": "#555555",
            "success": "#77b300",
            "info": "#c0c0c0",
            "warning": "#ff8800",
            "danger": "#cc0000",
            "light": "#ADAFAE",
            "dark": "#222222",
            "bg": "#000000",
            "fg": "#ffffff",
            "selectbg": "#454545",
            "selectfg": "#ffffff",
            "border": "#060606",
            "inputfg": "#ffffff",
            "inputbg": "#191919",
            "active": "#282828"
        }
      }
    }
  ]
}
```


## Export TTK Creator themes

User defined themes can be exported into the format specified above

1. Click the **Export** button from the top menu

2. Navigate to the location that you wish to export

3. Select a valid file name; the extension is `.py` by default

4. Click **Ok** to save the exported settings
    
