# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Full Changelog**: 

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

