# 均衡器
此示例演示了使用样式来区分scale函数。现在对代码进行一些评论；因为我希望比例值反映在比例下方的标签中，所以这个应用程序比它真正需要的复杂得多，因为 `Scale` 实现的一些奇怪之处。 `Scale` 小部件输出一个 double 类型，这意味着为了显示一个漂亮的舍入整数，该数字必须在更新时进行转换。幸运的是，scale 小部件有一个用于设置回调的命令参数。回调将获取比例值，然后可以将其转换为干净的格式。

![文件搜索图像示例](../assets/gallery/equalizer.png)

## 风格总结
使用的主题是**litera**。

|项目 |类 |配色风格 |
| --- | --- | --- |
|音量滑动块 | `Scale` |success|
|总滑动块 | `Scale` |success|
|其它滑动块 | `Scale` |info |

!!! note
    对于垂直方向，`from_` 参数对应于顶部，而 `to` 对应于小部件的底部，因此在设置缩放范围的最小和最大数字时需要考虑到这一点。

## 示例代码
[在 repl.it 上实时运行此代码](https://replit.com/@israel-dryer/equalizer#main.py)

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import randint


class Equalizer(ttk.Frame):
    
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.pack(fill=BOTH, expand=YES)

        controls = ["VOL", "31.25", "62.5", "125", "250",
                    "500", "1K", "2K", "4K", "8K", "16K", "GAIN"]

        for control in controls:
            self.create_band(self, control)

    def create_band(self, master, text):
        """Create and pack an equalizer band"""
        value = randint(1, 99)
        self.setvar(text, value)

        container = ttk.Frame(master)
        container.pack(side=LEFT, fill=Y, padx=10)

        # header label
        hdr = ttk.Label(container, text=text, anchor=CENTER)
        hdr.pack(side=TOP, fill=X, pady=10)

        # volume scale
        if text in ["VOL", "GAIN"]:
            bootstyle = SUCCESS
        else:
            bootstyle = INFO

        scale = ttk.Scale(
            master=container,
            orient=VERTICAL,
            from_=99,
            to=1,
            value=value,
            command=lambda x=value, y=text: self.update_value(x, y),
            bootstyle=bootstyle,
        )
        scale.pack(fill=Y)

        # value label
        val = ttk.Label(master=container, textvariable=text)
        val.pack(pady=10)

    def update_value(self, value, name):
        self.setvar(name, f"{float(value):.0f}")


if __name__ == "__main__":

    app = ttk.Window("Equalizer", "litera", resizable=(False, False))
    Equalizer(app)
    app.mainloop()
```