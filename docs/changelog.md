# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1](https://github.com/israel-dryer/ttkbootstrap/compare/v1.0.0...v1.0.1) - 2021-12-19
### Added
- added new themes [cerculean](https://github.com/israel-dryer/ttkbootstrap/blob/master/docs/assets/themes/cerculean.png) and [simplex](https://github.com/israel-dryer/ttkbootstrap/blob/master/docs/assets/themes/simplex.png)


### Fixed
- fixed several linux-related bugs noticed from repli.it by @israel-dryer in https://github.com/israel-dryer/ttkbootstrap/pull/94

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

