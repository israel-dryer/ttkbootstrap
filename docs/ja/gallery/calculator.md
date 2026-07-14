# 電卓
この基本的な電卓のUIは、異なる色を使って
ボタンの機能を区別する方法を示しています。 

![ファイル検索画像の例](../assets/gallery/calculator.png)

## スタイルの概要
この例で使用されているテーマは **flatly** です。

| 項目      | クラス     | ブートスタイル |
| ---       | ---       |---        |
| 数字      | `Button`  | primary   |
| 演算子    | `Button`  | secondary |
| 等号     | `Button`  | success   |

## サンプルコード
repl.itで[このコードを実行](https://replit.com/@israel-dryer/calculator#main.py)

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
        container.pack(fill=X, padding=20)
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
        """すべてのボタン押下イベントを処理し、ルーティングします。"""
        display = self.digitsvar.get()

        # ボタンが押された後、画面から演算子を削除する
        if len(display) > 0:
            if display[0] in ["/", "*", "-", "+"]:
                display = display[1:]

        if txt in ["CE", "C"]:
            self.digitsvar.set("")
            self.reset_variables()
        elif isinstance(txt, int):
            self.press_number(display, txt)
        elif txt == "." かつ "." が display に含まれない場合:
            self.digitsvar.set(f"{display}{txt}")
        elif txt == "±":
            self.press_inverse(display)
        elif txt in ["/", "*", "-", "+"]:
            self.press_operator(txt)
        elif txt == "=":
            self.press_equals(display)

    def press_number(self, display, txt):
        """数字ボタンが押された"""
        if display == "0":
            self.digitsvar.set(txt)
        else:
            self.digitsvar.set(f"{display}{txt}")

    def press_inverse(self, display):
        """逆数ボタンが押された"""
        if display.startswith("-"):
            if len(display) > 1:
                self.digitsvar.set(display[1:])
            else:
                self.digitsvar.set("")
        else:
            self.digitsvar.set(f"-{display}")

    def press_operator(self, txt):
        """演算子ボタンが押された"""
        self.operator.set(txt)
        display = float(self.digitsvar.get())
        if self.xnum.get() != 0:
            self.ynum.set(display)
        else:
            self.xnum.set(display)
        self.digitsvar.set(txt)

    def press_equals(self, display):
        """イコールボタンが押された"""
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
