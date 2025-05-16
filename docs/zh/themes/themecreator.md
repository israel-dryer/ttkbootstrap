# TTK创建器

TTK创建器 与 ttkbootstrap 打包，以便您可以修改、保存、导出和导入您创建的主题。

要运行该程序，请 _在您安装**ttkbootstrap**后_ 在控制台中键入以下命令：

```shell
python -m ttkcreator
```

![TTK创建器](../assets/ttkcreator/creator.png)

## 创建一个新主题

所有用于更改主题的控件都在左侧控制框架上。

1. 使用 **name** 条目命名您的主题

2. 选择一个**基础主题**；这将设置 _初始_ 颜色

3. 使用两个选项之一为每个颜色 _关键字_ 选择一种颜色
    
    * 单击🎨按钮从颜色对话框中选择一种颜色
    * 或者，输入 _十六进制_ 或有效颜色 _名称_

4. 点击**保存**按钮

您的主题现在保存在文件“ttkbootstrap.themes.user.py”中

!!! tip "重置主题"
    如果要重置颜色选择，可以单击
    **重置**选项从顶部菜单重置所有颜色
    到**基本主题**颜色。

## 导入用户主题

如果您有以下指定格式的用户主题文件，您可以
将该文件导入 ttkbootstrap。

1.单击顶部菜单上的**导入**按钮

2.选择你要导入的主题文件，然后点击**确定**导入

!!! warning
    导入用户主题文件将覆盖现有的用户定义
    ttkbootstrap 中的主题；所以确保先**导出**现有的
    你想要保留的主题

`user.py` 文件包含用户定义主题的字典。
您导入的那个文件必须符合下图所示的模式。

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

## 导出用户主题

用户定义的主题可以导出为上面指定的格式

1.单击顶部菜单中的**导出**按钮

2.导航到您要导出的位置

3.选择一个有效的文件名；默认情况下，扩展名是`.py`

4.点击**确定**保存导出的设置
