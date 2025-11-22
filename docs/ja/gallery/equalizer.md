# イコライザー

この例では、スタイルを使用してスケール機能を区別する方法を示します。
コードに関するコメントとして、スケール値をスケールの下にあるラベルに反映させたいので、
このアプリケーションは `Scale` 実装の特異性により、必要以上に複雑になっています。
`Scale` ウィジェットは double 型を出力するため、整数に丸めて表示するには値を変換する必要があります。
幸い、スケールウィジェットにはコマンドパラメータがあり、コールバックを設定できます。
コールバックはスケール値を取得し、それをきれいな形式に変換できます。

![イコライザーの例](../assets/gallery/equalizer.png)

## スタイル概要
この例で使用されているテーマは **litera** です。

| 項目           | クラス    | Bootstyle |
| ---            | ---       | ---       |
| ボリュームスケール | `Scale`  | success   |
| ゲインスケール    | `Scale`  | success   |
| その他のスケール   | `Scale`  | info      |

!!! 注意
垂直方向の場合、`from_` パラメータはウィジェットの上部に対応し、`to` は下部に対応します。
したがって、スケール範囲の最小値と最大値を設定する際に考慮する必要があります。

## サンプルコード
[このコードをReplitで実行](https://replit.com/@israel-dryer/equalizer#main.py)

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
