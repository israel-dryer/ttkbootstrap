# ユーザー入力の検証

`Entry` を継承するウィジェットは、ユーザー入力を検証する機能を備えています。
ウィジェットが **無効** 状態になると、境界線の色が **警告** 色に変わります。

![無効な入力](../assets/cookbook/entry-validation.gif)

この例では、検証タイプは `focus` です。これは、ウィジェットがフォーカスを取得または喪失するたびに
検証関数が実行されることを意味します。 他にもいくつかの
検証タイプがあり、検証を設定する方法も多数あります。今後の
チュートリアルでこれについて詳しく説明しますが、それまでは、
[tcl/tkのドキュメント](https://tcl.tk/man/tcl8.6/TkCmd/ttk_entry.htm)を参照して、
利用可能な検証機能に関する詳細情報を確認してください。

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def validate_number(x) -> bool:
    """入力が数値であるかを確認します"""
    if x.isdigit():
        return True
    elif x == "":
        return True
    else:
        return False

def validate_alpha(x) -> bool:
    """入力がアルファベットであるか検証する"""
    if x.isdigit():
        return False
    elif x == "":
        return True
    else:
        return True

# トップレベルウィンドウを作成
root = ttk.Window()
frame = ttk.Frame(root, padding=10)
frame.pack(fill=BOTH, expand=YES)

# 検証コールバックを登録
digit_func = root.register(validate_number)
alpha_func = root.register(validate_alpha)

# 数値入力の検証
ttk.Label(frame, text="数字を入力してください").pack()
num_entry = ttk.Entry(frame, validate="focus", validatecommand=(digit_func, '%P'))
num_entry.pack(padx=10, pady=10, expand=True)

# アルファベット入力の検証
ttk.Label(frame, text="文字を入力してください").pack()
let_entry = ttk.Entry(frame, validate="focus", validatecommand=(alpha_func, '%P'))
let_entry.pack(padx=10, pady=10, expand=True)

root.mainloop()
```
