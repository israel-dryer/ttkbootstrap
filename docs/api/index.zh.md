# API 文档

ttkbootstrap 是 tkinter 的封装。任何未在此库中专门定义的小部件或功能都可以在 [其他参考](#other-references) 中找到。

##🌈[Colorutils模块]（Colorutils.md）
此模块包含用于帮助操纵颜色的各种方法。

## 💬 对话模块
该模块包含各种基本对话框基类（以“Dialog”结尾），可用于为最终用户创建自定义对话框。这些基类作为 `Messagebox` 和 `Querybox` 容器类中预定义的静态帮助方法的基础，其中包括许多预定义的消息和查询对话框配置。

❯ [颜色选择对话框](dialogs/colorchooser.md)  
❯ [颜色滴管对话框](dialogs/colordropper.md)  
❯ [对话框](dialogs/dialog.md)
❯ [字体对话框](dialogs/fontdialog.md)
❯ [消息框](dialogs/messagebox.md)
❯ [消息对话框](dialogs/messagedialog.md)  
❯ [查询框](dialogs/querybox.md)
❯ [查询对话框](dialogs/querydialog.md)  

## 😉 图标模块
此模块包含为您的应用程序提供表情符号或图像图标的类。它们可以在文本中用作`图标`或在`PhotoImage`类中用作`图标`。

❯ [表情符号](icons/emoji.md)
❯ [图标](icons/icon.md)

## 🈚 本地化模块
该模块包括用于本地化 gui 小部件中的文本的方法和类。 [需要您的帮助](https://github.com/israel-dryer/ttkbootstrap/blob/master/src/ttkbootstrap/localization/msgs/README.md)来添加用于翻译文本的 msg 文件！

## 📜 滚动模块
该模块包含各种滚动小部件，例如 `ScrolledText` 和 `ScrolledFrame`。

❯ [ScrolledFrame](scrolled/scrolledframe.md)
❯ [ScrolledText](scrolled/scrolledtext.md)

## 🎨 样式模块
该模块包含构成 ttkbootstrap 主题和样式引擎的类。根据您使用 ttkbootstrap 的方式，您可能永远不需要直接使用这些类中的任何一个，但话又说回来，您可能会这样做，因此这里的文档供您参考。

❯ [风格](style/style.md)
❯ [颜色](style/colors.md)
❯ [主题定义](style/themedefinition.md)
❯ [Tk样式生成器](style/stylebuildertk.md)
❯ [TTk样式生成器](style/stylebuilderttk.md)
❯ [配色风格](style/bootstyle.md)

## 🪟 [tableview 模块](tableview/tableview.md)
❯ [表视图](tableview/tableview.md)
❯ [表列](tableview/tablecolumn.md)
❯ [表行](tableview/tablerow.md)

## 🛎️ [toast 模块](toast.md)
该模块有一个名为`ToastNotification`的类，它为临时警报或消息提供了一个半透明的弹出窗口。

## 📝 [工具提示模块](tooltip.md)
这个模块包含一个同名的类，它提供了一个半透明的工具提示弹出窗口，当鼠标悬停在小部件上时显示文本，当鼠标不再悬停在小部件上时关闭。

## ☑️ 小部件模块
此模块包含下面链接的自定义 ttkbootstrap 小部件。

❯ [日期文本框](widgets/dateentry.md)
❯ [水尺](widgets/floodgauge.md)
❯ [仪表](widgets/meter.md)  

## 🗔 窗口模块
该模块包含一个同名的类，包装了`tkinter.Tk`和[Style](style/style.md)类，为初始应用程序启动提供更方便的api。这也适用于 `Toplevel` 类。

❯ [窗口](window/window)
❯ [顶级窗口](window/toplevel)


## ⚙️ [实用模块](utility.md)
该模块包括对最终用户可能有用也可能没有用的各种实用功能。单击标题以阅读更多信息。

## ❓其他参考
此 api 参考不包括从 **tkinter** 继承的类、方法和函数。要了解有关如何使用 tkinter 的更多信息，您可以查阅下面列出的任何资源：

❯ [docs.python.org](https://docs.python.org/3/library/tkinter.html)
❯ [tkdocs](https://tkdocs.com/)
❯ [pythontutorial.net](https://www.pythontutorial.net/tkinter/)
❯ [anzeljg](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/)
❯ [tcl/tk](https://www.tcl.tk/man/tcl8.6/TkCmd/contents.html)