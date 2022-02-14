![](https://img.shields.io/github/release/israel-dryer/ttkbootstrap.svg)
[![Downloads](https://pepy.tech/badge/ttkbootstrap)](https://pepy.tech/project/ttkbootstrap)
[![Downloads](https://pepy.tech/badge/ttkbootstrap/month)](https://pepy.tech/project/ttkbootstrap)
![](https://img.shields.io/github/issues/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/issues-closed/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/license/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/stars/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/forks/israel-dryer/ttkbootstrap.svg)

# ttkbootstrap
[English](README.md) | 中文

tkinter的超强主题扩展，可实现受[Bootstrap](https://getbootstrap.com/)启发的按需现代平面风格主题。 

👀 阅读[文档](https://ttkbootstrap.readthedocs.io/en/latest/zh/)。


> **版本 1.0 是库的完全重建。** 如果您使用的是[0.5版本](https://github.com/israel-dryer/ttkbootstrap/tree/version-0.5)
   ，则在尝试使用themes.json导入主题时可能会遇到问题，因为这已从1.0中删除。现在，您可以使用 ttkcreator 直接导入和保存主题。

![](https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/assets/themes/themes.gif)

## 📦 特点

✔️ [**内置主题**](https://ttkbootstrap.readthedocs.io/en/latest/zh/themes/index.md)   
十几个精心策划的[深色](https://ttkbootstrap.readthedocs.io/en/latest/zh/themes/dark.md)和[浅色](https://ttkbootstrap.readthedocs.io/en/latest/zh/themes/light.md)主题

✔️ [**预定义样式：**](https://ttkbootstrap.readthedocs.io/en/latest/zh/styleguide/index.md)  
大量漂亮的[预定义构件样式](https://ttkbootstrap.readthedocs.io/en/latest/zh/styleguide/index.md)，如**轮廓**和**圆形切换**按钮。

✔️ [**简单的关键字 API：**](https://ttkbootstrap.readthedocs.io/en/latest/zh/gettingstarted/tutorial/#use-themed-widgets)  
使用[简单的关键字](https://ttkbootstrap.readthedocs.io/en/latest/zh/gettingstarted/tutorial/#use-themed-widgets)（如**primary**和**striped**）应用颜色和类型，而不是使用主要的旧方法**Striped.Horizontal.TProgressbar**。如果您已经使用Bootstrap进行Web开发，那么您已经熟悉了使用css类的这种方法。

✔️ [**许多新的小部件：**](https://ttkbootstrap.readthedocs.io/en/latest/zh/api/widgets/dateentry)  
ttkbootstrap附带了几个设计精美的新小部件，如[Meter](https://ttkbootstrap.readthedocs.io/en/latest/zh/api/widgets/meter)，[DateEntry](https://ttkbootstrap.readthedocs.io/en/latest/zh/api/widgets/dateentry)和[Floodgauge](https://ttkbootstrap.readthedocs.io/en/latest/zh/api/widgets/floodgauge)。 此外，[对话框](https://ttkbootstrap.readthedocs.io/en/latest/zh/api/dialogs/dialog)现在具有主题和完全可自定义性。

✔️ [**内置主题创建器：**](https://ttkbootstrap.readthedocs.io/en/latest/zh/themes/themecreator.md)  
想要创建自己的主题？容易！ttkbootstrap附带一个内置的[主题创建器](https://ttkbootstrap.readthedocs.io/en/latest/zh/themes/themecreator.md)，使您能够轻松构建，加载，浏览和应用自己的自定义主题。

## 安装

```python
python -m pip install ttkbootstrap
```

## 简单示例
您可以使用带有“bootstyle”参数的简单关键字，而不是使用长而复杂的ttk样式类。

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(themename="superhero")

b1 = ttk.Button(root, text="Submit", bootstyle="success")
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Submit", bootstyle="info-outline")
b2.pack(side=LEFT, padx=5, pady=10)

root.mainloop()
```

新的关键字API非常灵活。以下示例均产生相同的结果：
- `bootstyle="info-outline"`
- `bootstyle="info outline"`
- `bootstyle=("info", "outline")`
- `bootstyle=(INFO, OUTLINE)`

## 链接：
- **文档：** https://ttkbootstrap.readthedocs.io/en/latest/zh/  
- **GitHub：** https://github.com/israel-dryer/ttkbootstrap
