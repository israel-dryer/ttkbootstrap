# チュートリアル

## アプリケーションの作成

ttkbootstrapアプリケーションを構築する際には、2つのアプローチがあります。
1つ目は、**tkinter**や**ttk**を使用したことがある方に馴染みのある方法です。
2つ目は、新しい[Window](../api/window/window.md)クラスを使用して、全体のプロセスを簡略化する方法です。

### 従来のアプローチ

この方法は馴染みのあるパターンを使用しますが、いくつかの違いがあります：

- `ttk`の代わりに`ttkbootstrap`をインポートします
- `style`パラメータの代わりに`bootstyle`パラメータを使用してキーワードを追加します

!!! note "定数の使用を推奨"
コード内で文字列よりも定数を使用することを推奨します。
ただし、快適なコーディングスタイルを選んでください。
bootstyleキーワードAPIは非常に柔軟なので、[構文オプション](#keyword-usage)を確認してください。

```python
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = tk.Tk()

b1 = ttk.Button(root, text="Button 1", bootstyle=SUCCESS)
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Button 2", bootstyle=(INFO, OUTLINE))
b2.pack(side=LEFT, padx=5, pady=10)

root.mainloop()
```

上記のコードは、2つのボタンを持つウィンドウを生成します。

![シンプルな使用例ウィンドウ](../assets/tutorial/simple-usage.png)

### 新しいアプローチ

同じ結果は、新しい[Window](../api/window/window.md)クラスを使用することで得られます。
このクラスについてはAPIドキュメントで確認できます。
違いは小さく見えるかもしれませんが、`Window`クラスは多くの属性をメソッドではなくパラメータで設定でき、
`Style`オブジェクトが自動的に`Window`オブジェクトに関連付けられます。

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

b1 = ttk.Button(root, text="Button 1", bootstyle=SUCCESS)
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Button 2", bootstyle=(INFO, OUTLINE))
b2.pack(side=LEFT, padx=5, pady=10)

root.mainloop()
```

## テーマの選択

デフォルトのテーマは**litera**ですが、`Style`オブジェクトや`Window`クラスを使用して、
[組み込みテーマ](../themes/index.md)のいずれかでアプリケーションを開始できます。

```python
import ttkbootstrap as ttk

# 従来の方法
root = ttk.Tk()
style = ttk.Style("darkly")

# 新しい方法
root = ttk.Window(themename="darkly")
```

## テーマ付きウィジェットの使用

ttkbootstrapウィジェットには[多数の事前定義スタイル](../styleguide/index.md)があり、**タイプ**と**カラー**を変更するキーワードで適用します。
色の値はテーマごとに定義されています。

例えば、キーワード**outline**を使用するとアウトラインタイプのボタンが描画され、**info**を使用するとアウトラインとテキストの色が変更されます。

### スタイルカラー
以下の例は、すべてのカラーのボタンを表示します。

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

b1 = ttk.Button(root, text='primary', bootstyle=PRIMARY)
b1.pack(side=LEFT, padx=5, pady=5)

b2 = ttk.Button(root, text='secondary', bootstyle=SECONDARY)
b2.pack(side=LEFT, padx=5, pady=5)

b3 = ttk.Button(root, text='success', bootstyle=SUCCESS)
b3.pack(side=LEFT, padx=5, pady=5)

b4 = ttk.Button(root, text='info', bootstyle=INFO)
b4.pack(side=LEFT, padx=5, pady=5)

b5 = ttk.Button(root, text='warning', bootstyle=WARNING)
b5.pack(side=LEFT, padx=5, pady=5)

b6 = ttk.Button(root, text='danger', bootstyle=DANGER)
b6.pack(side=LEFT, padx=5, pady=5)

b7 = ttk.Button(root, text='light', bootstyle=LIGHT)
b7.pack(side=LEFT, padx=5, pady=5)

b8 = ttk.Button(root, text='dark', bootstyle=DARK)
b8.pack(side=LEFT, padx=5, pady=5)

root.mainloop()
```

![ボタンカラー](../assets/tutorial/button-colors.png)

`Style.colors`オブジェクトを使用すれば、より簡単に作成できます。
このオブジェクトはテーマで使用されるすべての色を参照し、イテレータとしても機能します。

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

for color in root.style.colors:
    b = ttk.Button(root, text=color, bootstyle=color)
    b.pack(side=LEFT, padx=5, pady=5)
```

### スタイルタイプ
キーワードはウィジェットの**type**を制御できます。
次の例では、**solid**と**outline**ボタンを示します。

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

b1 = ttk.Button(root, text="Solid Button", bootstyle=SUCCESS)
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Outline Button", bootstyle=(SUCCESS, OUTLINE))
b2.pack(side=LEFT, padx=5, pady=10)

root.mainloop()
```

![ボタンスタイル](../assets/tutorial/solid-outline-button-styles.png)

### キーワードの使用
bootstyleパラメータは非常に柔軟です。キーワードの形式は重要ではありません。
背景で正規表現が入力を解析し、適切なttkスタイルに変換します。

以下のすべてのバリエーションは同じスタイルになります：

* `"info-outline"`
* `"infooutline"`
* `"info outline"`
* `"outline-info"`
* `("info", "outline")`
* `(INFO, OUTLINE)`

!!! note "推奨されるキーワード区切りはハイフン"
文字列を使用する場合、可能であればキーワードをハイフンで区切ることを推奨します。
定数を使用する場合、複数のキーワードはリストまたはタプルで渡します。
