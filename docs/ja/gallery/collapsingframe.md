# 折りたたみ可能なフレーム
この例では、折りたたみ可能なフレームウィジェットの作成方法を示します。ウィジェットに追加された各 `Frame` 
には、タイトルやスタイルを割り当てることができます。各オプショングループには、
さまざまなブートスタイルが適用されます。 

![ファイル検索画像の例](../assets/gallery/collapsing_frame.png)
 
## スタイル概要
使用しているテーマは **litera** です。

| 項目              | クラス             | ブートスタイル |
| ---               | ---               | --- |
| オプショングループ 1 | `CollapsingFrame` | primary |
| オプショングループ 2 | `CollapsingFrame` | danger |
| オプショングループ 3 | `CollapsingFrame` | success |

## サンプルコード
repl.itでこのコードを実行する[(https://replit.com/@israel-dryer/collapsing-frame#main.py)]

```python
from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle


IMG_PATH = Path(__file__).parent / 'assets'


class CollapsingFrame(ttk.Frame):
    """クリックで展開・折りたたみが可能なフレームウィジェットです。"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        # ウィジェットの画像
        self.images = [
            ttk.PhotoImage(file=IMG_PATH/'icons8_double_up_24px.png'),
            ttk.PhotoImage(file=IMG_PATH/'icons8_double_right_24px.png')
        ]

    def add(self, child, title="", bootstyle=PRIMARY, **kwargs):
        """折りたたみ可能なフレームに子要素を追加する

        パラメータ:

            child (Frame):
                ウィジェットに追加する子フレーム。

            title (str):
                折りたたみ可能なセクションのヘッダーに表示されるタイトル。

            bootstyle (str):
                折りたたみセクションのヘッダーに適用するスタイル。

            **kwargs (Dict):
                その他のオプションのキーワード引数。
        """
        if child.winfo_class() != 'TFrame':
            return
        
        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # ヘッダーのタイトル
        header = ttk.Label(
            master=frm,
            text=title,
            bootstyle=(style_color, INVERSE)
        )
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # ヘッダーのトグルボタン
        def _func(c=child): return self._toggle_open_close(c)
        btn = ttk.Button(
            master=frm,
            image=self.images[0],
            bootstyle=style_color,
            command=_func
        )
        btn.pack(side=RIGHT)

        # トグル操作が可能になるよう、トグルボタンを子ウィンドウに割り当てる
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

        # 行の割り当てをインクリメント
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """セクションを開閉し、それに応じてトグルボタンの
        画像を変更します。

        パラメータ:
            
            child (Frame):
                グリッドマネージャーに追加または削除する子要素。
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.images[1])
        else:
            child.grid()
            child.btn.configure(image=self.images[0])


if __name__ == '__main__':

    app = ttk.Window(minsize=(300, 1))

    cf = CollapsingFrame(app)
    cf.pack(fill=BOTH)

    # オプショングループ 1
    group1 = ttk.Frame(cf, padding=10)
    for x in range(5):
        ttk.Checkbutton(group1, text=f'Option {x + 1}').pack(fill=X)
    cf.add(child=group1, title='Option Group 1')

    # オプショングループ 2
    group2 = ttk.Frame(cf, padding=10)
    for x in range(5):
        ttk.Checkbutton(group2, text=f'Option {x + 1}').pack(fill=X)
    cf.add(group2, title='Option Group 2', bootstyle=DANGER)

    # オプショングループ 3
    group3 = ttk.Frame(cf, padding=10)
    for x in range(5):
        ttk.Checkbutton(group3, text=f'Option {x + 1}').pack(fill=X)
    cf.add(group3, title='Option Group 3', bootstyle=SUCCESS)

    app.mainloop()
```
