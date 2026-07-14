# 簡単なデータ入力
このシンプルなデータ入力フォームは、ユーザーからの入力を受け付け、送信されると画面に表示します。 

![ファイル検索画像の例](../assets/gallery/simple_data_entry_light.png)

![ファイル検索画像の例](../assets/gallery/simple_data_entry_dark.png)

## スタイルの概要
上記の2つの例では、**litera**と**superhero**というテーマを使用しています。

| 項目          | クラス     | ブートスタイル |
| ---           | ---       | ---|
| 送信ボタン | `Button`  | success |
| キャンセルボタン | `Button`  | danger |
| 入力フィールド | `Entry`   | default |

## サンプルコード
[repl.itでこのコードを実行](https://replit.com/@israel-dryer/data-entry#main.py)

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class DataEntryForm(ttk.Frame):
    
    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)

        # フォーム変数
        self.name = ttk.StringVar(value="")
        self.address = ttk.StringVar(value="")
        self.phone = ttk.StringVar(value="")

        # フォームヘッダー
        hdr_txt = "連絡先情報を入力してください" 
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, padding=10)

        # フォーム項目
        self.create_form_entry("name", self.name)
        self.create_form_entry("address", self.address)
        self.create_form_entry("phone", self.phone)
        self.create_buttonbox()

    def create_form_entry(self, label, variable):
        """単一のフォーム入力項目を作成する"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_buttonbox(self):
        """アプリケーションのボタンボックスを作成する"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="Submit",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        cnl_btn = ttk.Button(
            master=container,
            text="Cancel",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=6,
        )
        cnl_btn.pack(side=RIGHT, padx=5)

    def on_submit(self):
        """内容をコンソールに出力し、値を返す。"""
        print("名前:", self.name.get())
        print("住所:", self.address.get())
        print("電話番号:", self.phone.get())
        return self.name.get(), self.address.get(), self.phone.get()

    def on_cancel(self):
        """キャンセルしてアプリケーションを終了する。"""
        self.quit()


if __name__ == "__main__":

    app = ttk.Window("Data Entry", "superhero", resizable=(False, False))
    DataEntryForm(app)
    app.mainloop()
```
