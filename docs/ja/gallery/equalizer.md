# イコライザー
この例では、スタイルを使用してスケール関数を区別する方法を示しています。
ここでコードについて少し解説します。スケール値をスケール下のラベルに反映させたかったため、
`Scale`の実装上のいくつかの奇妙な点により、このアプリケーションは本来必要以上に
複雑になっています。 `Scale`ウィジェットはdouble型を出力します。つまり、
見栄えの良い丸めた整数を表示するためには、更新時にその数値を変換する必要があります。
幸いなことに、スケールウィジェットにはコールバックを設定するためのコマンドパラメータがあります。
コールバックはスケール値を受け取り、それを
見栄えの良い整形式に変換することができます。 

![ファイル検索画像の例](../assets/gallery/equalizer.png)

## スタイルの概要
使用しているテーマは **litera** です。

| 項目          | クラス     | ブートスタイル |
| ---           | ---       | ---       |
| ボリューム・スケール | `Scale`   | success   |
| ゲイン・スケール    | `Scale`   | success   |
| その他のスケール  | `Scale`   | info      |

!!! 注意
    縦方向の場合、`from_`パラメータはウィジェットの上端に、
    `to`パラメータは下端に対応するため、
    スケール範囲の最小値と最大値を設定する際は、
    この点を考慮する必要があります。

## サンプルコード
[このコードを repl.it で実行](https://replit.com/@israel-dryer/equalizer#main.py)

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
        """イコライザーバンドを作成して配置する"""
        value = randint(1, 99)
        self.setvar(text, value)

        container = ttk.Frame(master)
        container.pack(side=LEFT, fill=Y, padx=10)

        # ヘッダーラベル
        hdr = ttk.Label(container, text=text, anchor=CENTER)
        hdr.pack(side=TOP, fill=X, pady=10)

        # 音量スライダー
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

        # 値のラベル
        val = ttk.Label(master=container, textvariable=text)
        val.pack(pady=10)

    def update_value(self, value, name):
        self.setvar(name, f"{float(value):.0f}")


if __name__ == "__main__":

    app = ttk.Window("Equalizer", "litera", resizable=(False, False))
    Equalizer(app)
    app.mainloop()
```
