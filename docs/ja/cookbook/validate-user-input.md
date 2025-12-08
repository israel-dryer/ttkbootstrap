# ユーザー入力の検証

`Entry`を継承するウィジェットは、ユーザー入力を検証する機能を備えています。ウィジェットが
**無効**状態になると、境界線の色が**危険**色に変化します。

![無効な入力例](../assets/cookbook/entry-validation.gif)

この例では検証タイプが`focus`です。
つまり、ウィジェットがフォーカスを取得/喪失するたびに検証関数が実行されます。
他にもいくつかの検証タイプがあり、検証を設定する方法は多数存在します。
詳細については今後のチュートリアルで説明しますが、
それまでは検証で利用可能な機能について詳しくは[tcl/tkドキュメント](https://tcl.tk/man/tcl8.6/TkCmd/ttk_entry.htm)を参照してください。

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def validate_number(x) -> bool:
    """入力が数字であるか検証"""
    if x.isdigit():
        return True
    elif x == "":
        return True
    else:
        return False

def validate_alpha(x) -> bool:
    """入力がアルファベットであることを検証"""
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
ttk.Label(frame, text="アルファベットを入力してください").pack()
let_entry = ttk.Entry(frame, validate="focus", validatecommand=(alpha_func, '%P'))
let_entry.pack(padx=10, pady=10, expand=True)

root.mainloop()
```
