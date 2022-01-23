# 更新日志
对此项目的所有值得注意的更改都将记录在此文件中。

该格式基于[Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，并且该项目遵循[语义化版本控制](https://semver.org/spec/v2.0.0.html)。

**完整更新日志**：

## [1.5.1](https://github.com/israel-dryer/ttkbootstrap/compare/v1.5.0...v1.5.1) - 2022-01-18
其它错误修复

### 修复
- 在`ScrolledFrame`小部件中混合打包和放置geometry managers时的不规则行为[#140](https://github.com/israel-dryer/ttkbootstrap/issues/140)
- 缺少字体导致某些 linux 发行版在绘制checkbutton资源时失败。[#143](https://github.com/israel-dryer/ttkbootstrap/issues/143)

## [1.5.0](https://github.com/israel-dryer/ttkbootstrap/compare/v1.4.0...v1.5.0) - 2022-01-09
`Tableview`小部件的新`验证模块`和几个错误修复。

### 添加
- @israel-dryer在[#129](https://github.com/israel-dryer/ttkbootstrap/pull/129)中添加验证模块。用户现在可以轻松地将验证添加到任何文本框类型小部件，例如文本框、下拉框和数字框。默认情况下，包含多个预定义的验证函数，但 API 中提供了有关如何轻松构建新的自定义验证的说明。
- 添加`Colors.make_transparent`方法以改善颜色处理。这最终将取代构建不在标准配色方案中的各种小部件颜色的方法`Colors.update_hsv`。
### 修复
- 修复[#128](https://github.com/israel-dryer/ttkbootstrap/pull/128)中@israel-dryer禁用的小部件颜色
- Tableview[#130](https://github.com/israel-dryer/ttkbootstrap/issues/130)中未应用自定义条纹颜色
- 如果当前页面上的所有行都被隐藏或删除，Tableview现在将恢复到上一页[#130](https://github.com/israel-dryer/ttkbootstrap/issues/130) 
- 在文本框中输入页码将会向页码添加1页[#130](https://github.com/israel-dryer/ttkbootstrap/issues/130)

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
