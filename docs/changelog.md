# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Full Changelog**: 

## [1.5.1](https://github.com/israel-dryer/ttkbootstrap/compare/v1.5.0...v1.5.1) - 2022-01-18
Miscellaneous bug fixes

### Fixed
- Irregular behavior when mixing pack and place geometry managers inside the `ScrolledFrame` widget [#140](https://github.com/israel-dryer/ttkbootstrap/issues/140)
- Missing font caused failure on certain linux distributions when drawing the checkbutton assets [#143](https://github.com/israel-dryer/ttkbootstrap/issues/143).

## [1.5.0](https://github.com/israel-dryer/ttkbootstrap/compare/v1.4.0...v1.5.0) - 2022-01-09
New `validation` module and several bug-fixes for the `Tableview` widget.

### Added
- Add validation module by @israel-dryer in [#129](https://github.com/israel-dryer/ttkbootstrap/pull/129). The user can now easily add validation to any Entry type widget such as Entry, Combobox, and Spinbox. Several pre-defined validation functions are included by default, but instructions are in the API for how to easily build new custom validations.
- Add `Colors.make_transparent` method to improve color handling. This will eventually replace the `Colors.update_hsv` method for building various widget colors that are not in the standard color scheme.

### Fixed
- Fix disabled widget colors by @israel-dryer in [#128](https://github.com/israel-dryer/ttkbootstrap/pull/128)
- Custom stripecolors were not being applied in Tableview [#130](https://github.com/israel-dryer/ttkbootstrap/issues/130) 
- Tableview now reverts to prev page if all rows are hidden or deleted on current page [#130](https://github.com/israel-dryer/ttkbootstrap/issues/130) 
- Page number entered into Entry was adding 1 page to number [#130](https://github.com/israel-dryer/ttkbootstrap/issues/130)

## [1.4.0](https://github.com/israel-dryer/ttkbootstrap/compare/v1.3.1...v1.4.0) - 2022-01-08
* Tableview bug fixes and feature upgrades by @israel-dryer in [#124](https://github.com/israel-dryer/ttkbootstrap/pull/124)
* Enable tableview value updates with property setter by @israel-dryer in [#125](https://github.com/israel-dryer/ttkbootstrap/pull/125)

### Fixed
- Entering a page less than 1 or greater than the max in the page entry no longer returns an empty or invalid page
- The +/- column options in the right-click menu now update when columns are deleted or inserted into the table
- Other miscellaneous not worthy of a write-up

### Added
- Default stripe colors are added for all themes
- Bulk delete and insert is now available via the `Tableview.purge_table_data` and `Tableview.build_table_data` methods. Along with the existing insert methods, delete methods have been added for columns and rows to make the data handling full-featured.
- New command in the right-click cell menu
  * delete selected rows
- New commands in the right-click header menu
  * delete column
  * hide column
  * show all columns
- Table rows [can now be updated](https://github.com/israel-dryer/ttkbootstrap/issues/121) with the TableRows.values property 

### Changed
- The `stripecolor` parameter is enhanced so that passing in a tuple with `None` for background and foreground colors will now cause that element to use a default color. For example: `stripecolor=(None, None)` will cause a default foreground and background color while `stripecolor=('yellow', None)` will cause a yellow background and default foreground color. The default setting of `stripecolor=None` will disabled stripecolors altogether.

## [1.3.1](https://github.com/israel-dryer/ttkbootstrap/compare/v1.3.0...v1.3.1) - 2022-01-04
### Fixed
- Internal resizing issue, missing args in internal frame on ScrolledFrame by @israel-dryer in [#120](https://github.com/israel-dryer/ttkbootstrap/pull/120)

## [1.3.0](https://github.com/israel-dryer/ttkbootstrap/compare/v1.2.0...v1.3.0) - 2022-01-03
### Added
- ScrolledFrame and ScrolledText by @israel-dryer in [#102](https://github.com/israel-dryer/ttkbootstrap/pull/102), [#104](https://github.com/israel-dryer/ttkbootstrap/pull/104)
- Tableview by @israel-dryer in [#110](https://github.com/israel-dryer/ttkbootstrap/pull/110), [#117](https://github.com/israel-dryer/ttkbootstrap/pull/117)
- disabled and readonly state cursor for entry type widgets by @israel-dryer in [#111](https://github.com/israel-dryer/ttkbootstrap/pull/111)

### Fixed
- window module api issues by @israel-dryer in [#109](https://github.com/israel-dryer/ttkbootstrap/pull/109)
- disabled fg color for entry, combobox, spinbox by @israel-dryer in [#112](https://github.com/israel-dryer/ttkbootstrap/pull/112)

### Changed
Removed black dependency with json formatter by @israel-dryer in [#107](https://github.com/israel-dryer/ttkbootstrap/pull/107)

## [1.2.0](https://github.com/israel-dryer/ttkbootstrap/compare/v1.1.0...v1.2.0) - 2021-12-25
### Added
- `autostyle` flag added to legacy tkinter widgets by @israel-dryer in [#101](https://github.com/israel-dryer/ttkbootstrap/pull/101).
    This will enable you to turn off the default ttkbootstrap styling to legacy
    widgets so that you can apply your own customizations.

### Fixed
- predefined styles are now configureable even if not yet created by @israel-dryer in [#100](https://github.com/israel-dryer/ttkbootstrap/pull/100).

## [1.1.0](https://github.com/israel-dryer/ttkbootstrap/compare/v1.0.1...v1.1.0) - 2021-12-21
### Added
- toast and tooltip modules by @israel-dryer in [#97](https://github.com/israel-dryer/ttkbootstrap/pull/97).
  
## [1.0.1](https://github.com/israel-dryer/ttkbootstrap/compare/v1.0.0...v1.0.1) - 2021-12-19
### Changed
- updated `themes/standard.py` with [cerculean](https://github.com/israel-dryer/ttkbootstrap/blob/master/docs/assets/themes/cerculean.png) and [simplex](https://github.com/israel-dryer/ttkbootstrap/blob/master/docs/assets/themes/simplex.png)

### Fixed
- fixed several linux-related bugs noticed from repli.it by @israel-dryer in [#94](https://github.com/israel-dryer/ttkbootstrap/pull/94).
  
## [1.0.0](https://github.com/israel-dryer/ttkbootstrap/compare/v0.5.1...v1.0.0) - 2021-12-19
### Added
- new keyword api added with `bootstyle` parameter which allows for true _Bootstrap_ style widget styling
- high dpi scaling for high resolution displays
- new `Window` class parameterizes commonly used `tkinter.Tk` methods and attaches a `Style` property to eliminate the need for creating two objects; also has a stock ttkbootstrap icon
- new themed dialog classes + two container classes `Messagebox` and `Querybox` that include dozens of static convenience methods
- new rounded scrollbars style
- new styles added for **invalid** and **readonly** widget states (ex. invalid input will show a _danger_ colored highlight)

### Changed
- styles and themes are created _on-demand_ with the new style engine instead of being loaded all at once
- ttkcreator is completely redesigned
- update theme colors to improve look & feel, especially dark themes

### Removed
- json themes file is no longer used; this was converted to a python file
- no longer use an embedded font file, OS specific fonts are selected by default
- style no longer accepts a user defined font, the OS default font is used

