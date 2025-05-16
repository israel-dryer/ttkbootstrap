# 文本阅读器
此应用程序打开一个文本文件并将数据放入滚动的`文本`小部件中。

![文件搜索图像示例](../assets/gallery/text_reader.png)

## 风格总结
应用的主题是**sandstone**。

| 项目          | 类     | 配色样式 |
| ---           | ---       | --- |
| 文件文本框    | `Entry`   | default |
| 选择文件按钮  | `Button`  | default |

## 示例代码
[在 repl.it 上实时运行此代码](https://replit.com/@israel-dryer/text-reader#main.py)

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText


class TextReader(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=15)
        self.filename = ttk.StringVar()
        self.pack(fill=BOTH, expand=YES)
        self.create_widget_elements()

    def create_widget_elements(self):
        """Create and add the widget elements"""
        style = ttk.Style()
        self.textbox = ScrolledText(
            master=self,
            highlightcolor=style.colors.primary,
            highlightbackground=style.colors.border,
            highlightthickness=1
        )
        self.textbox.pack(fill=BOTH)
        default_txt = "Click the browse button to open a new text file."
        self.textbox.insert(END, default_txt)

        file_entry = ttk.Entry(self, textvariable=self.filename)
        file_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 5), pady=10)

        browse_btn = ttk.Button(self, text="Browse", command=self.open_file)
        browse_btn.pack(side=RIGHT, fill=X, padx=(5, 0), pady=10)

    def open_file(self):
        path = askopenfilename()
        if not path:
            return

        with open(path, encoding='utf-8') as f:
            self.textbox.delete('1.0', END)
            self.textbox.insert(END, f.read())
            self.filename.set(path)


if __name__ == '__main__':
    
    app = ttk.Window("Text Reader", "sandstone")
    TextReader(app)
    app.mainloop()
```