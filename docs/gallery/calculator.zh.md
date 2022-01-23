# 计算器
这个基本的计算器 UI 演示了如何使用不同的颜色来区分按钮功能。

![文件搜索图像示例](../assets/gallery/calculator.png)

## 风格总结
此示例中使用的主题是 **flatly**。

|项目 |类 |配色风格 |
| --- | --- |--- |
|数字 | `按钮` |primary |
|运算符 | `按钮` |secondary |
|等于 | `按钮` |success|

## 示例代码
[在 repl.it 上实时运行此代码](https://replit.com/@israel-dryer/calculator#main.py)

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Calculator(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=10, **kwargs)
        ttk.Style().configure("TButton", font="TkFixedFont 12")
        self.pack(fill=BOTH, expand=YES)
        self.digitsvar = ttk.StringVar(value=0)
        self.xnum = ttk.DoubleVar()
        self.ynum = ttk.DoubleVar()
        self.operator = ttk.StringVar(value="+")

        if "bootstyle" in kwargs:
            self.bootstyle = kwargs.pop("bootstyle")
        else:
            self.bootstyle = None
        self.create_num_display()
        self.create_num_pad()

    def create_num_display(self):
        container = ttk.Frame(master=self, padding=2, bootstyle=self.bootstyle)
        container.pack(fill=X, pady=20)
        digits = ttk.Label(
            master=container,
            font="TkFixedFont 14",
            textvariable=self.digitsvar,
            anchor=E,
        )
        digits.pack(fill=X)

    def create_num_pad(self):
        container = ttk.Frame(master=self, padding=2, bootstyle=self.bootstyle)
        container.pack(fill=BOTH, expand=YES)
        matrix = [
            ("%", "C", "CE", "/"),
            (7, 8, 9, "*"),
            (4, 5, 6, "-"),
            (1, 2, 3, "+"),
            ("±", 0, ".", "="),
        ]
        for i, row in enumerate(matrix):
            container.rowconfigure(i, weight=1)
            for j, num_txt in enumerate(row):
                container.columnconfigure(j, weight=1)
                btn = self.create_button(master=container, text=num_txt)
                btn.grid(row=i, column=j, sticky=NSEW, padx=1, pady=1)

    def create_button(self, master, text):
        if text == "=":
            bootstyle = SUCCESS
        elif not isinstance(text, int):
            bootstyle = SECONDARY
        else:
            bootstyle = PRIMARY
        return ttk.Button(
            master=master,
            text=text,
            command=lambda x=text: self.on_button_pressed(x),
            bootstyle=bootstyle,
            width=2,
            padding=10,
        )

    def reset_variables(self):
        self.xnum.set(value=0)
        self.ynum.set(value=0)
        self.operator.set("+")

    def on_button_pressed(self, txt):
        """Handles and routes all button press events."""
        display = self.digitsvar.get()

        # remove operator from screen after button is pressed
        if len(display) > 0:
            if display[0] in ["/", "*", "-", "+"]:
                display = display[1:]

        if txt in ["CE", "C"]:
            self.digitsvar.set("")
            self.reset_variables()
        elif isinstance(txt, int):
            self.press_number(display, txt)
        elif txt == "." and "." not in display:
            self.digitsvar.set(f"{display}{txt}")
        elif txt == "±":
            self.press_inverse(display)
        elif txt in ["/", "*", "-", "+"]:
            self.press_operator(txt)
        elif txt == "=":
            self.press_equals(display)

    def press_number(self, display, txt):
        """A digit button is pressed"""
        if display == "0":
            self.digitsvar.set(txt)
        else:
            self.digitsvar.set(f"{display}{txt}")

    def press_inverse(self, display):
        """The inverse number button is pressed"""
        if display.startswith("-"):
            if len(display) > 1:
                self.digitsvar.set(display[1:])
            else:
                self.digitsvar.set("")
        else:
            self.digitsvar.set(f"-{display}")

    def press_operator(self, txt):
        """An operator button is pressed"""
        self.operator.set(txt)
        display = float(self.digitsvar.get())
        if self.xnum.get() != 0:
            self.ynum.set(display)
        else:
            self.xnum.set(display)
        self.digitsvar.set(txt)

    def press_equals(self, display):
        """The equals button is pressed."""
        if self.xnum.get() != 0:
            self.ynum.set(display)
        else:
            self.xnum.set(display)
        x = self.xnum.get()
        y = self.ynum.get()
        op = self.operator.get()
        if all([x, y, op]):
            result = eval(f"{x}{op}{y}")
            self.digitsvar.set(result)
            self.reset_variables()


if __name__ == "__main__":

    app = ttk.Window(
        title="Calculator",
        themename="flatly",
        size=(350, 450),
        resizable=(False, False),
    )
    Calculator(app)
    app.mainloop()
```