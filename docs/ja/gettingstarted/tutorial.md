# チュートリアル

## アプリケーションの作成

ttkbootstrap アプリケーションを構築する際には、2つのアプローチがあります。1つ目は、
**tkinter** や **ttk** を使ったことがある方なら馴染みのある方法です。2つ目は、
新しい [Window](../api/window/window.md) クラスを使用して、プロセス全体を簡略化するものです。

### 従来のアプローチ

このアプローチでは、おなじみのパターンが使用されます。ただし、いくつかの違いがあります：

- `ttk`の代わりに`ttkbootstrap`をインポートする
- `style`パラメータの代わりに`bootstyle`パラメータを使用してキーワードを追加する

!!! 注：「定数の使用が推奨されます」
    コード内では文字列よりも定数を使用することを推奨します。ただし、ご自身が
    使いやすいコーディングスタイルを自由に選んでください。bootstyleキーワード
    APIは非常に柔軟ですので、必ず[構文オプションを確認してください](#keyword-usage)。

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

上記のコードを実行すると、2つのボタンがあるこのウィンドウが表示されます。

![simple usage window](../assets/tutorial/simple-usage.png)

### 新しいアプローチ

APIドキュメントで解説されている新しい [Window](../api/window/window.md) 
クラスを使用しても、同じ結果を得ることができます。違いは
一見些細なものに思えるかもしれませんが、後で見るように、`Window` クラスはパラメータを使用して
多くの属性や特性を設定しますが、`Tk` クラスを使用する場合はメソッドでしか設定できません。 さらに、後の例で見るように、`Style` オブジェクトは
自動的に `Window` オブジェクトに紐付けられます。

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

デフォルトのテーマは **litera** ですが、`Style` オブジェクトを単独で、または `Window` クラス経由で指定することで、
[組み込みテーマ](../themes/index.md) のいずれかを使用してアプリケーションを起動できます。

```python
import ttkbootstrap as ttk

# 従来のアプローチ
root = ttk.Tk()
style = ttk.Style("darkly")

# 新しい方法
root = ttk.Window(themename="darkly")
```

## テーマ付きウィジェットの使用

ttkbootstrapのウィジェットには[数十種類の定義済みスタイル](../styleguide/index.md)があり、
これらはウィジェットの**タイプ**と**色**の両方を変更する**キーワード**を使用して適用されます。
実際の色値は各テーマごとに定義されています。

たとえば、キーワード **outline** を使用すると、アウトライン付きのボタンが描画されますが、
キーワード **info** を使用すると、アウトラインとテキストの _色_ が変更されます。

### スタイルの色
以下の例は、各色に対応するボタンを示しています。

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

テーマで使用されるすべての色への参照を含み、かつ_イテレータ_でもある
`Style.colors` オブジェクトを使用すれば、これらのボタンをもっと簡単に作成できたでしょう。 

`Style`オブジェクトについては、`Style`クラスを使用してスタイルオブジェクトを作成するか、`Window`オブジェクトの`style`プロパティを使用することができます。

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

for color in root.style.colors:
    b = ttk.Button(root, text=color, bootstyle=color)
    b.pack(side=LEFT, padx=5, pady=5)
```

### スタイルの種類

**キーワード**を使用することで、表示されるウィジェットの**タイプ**を制御できます。
以下の例では、**実線**と**輪郭線**のボタンを表示しています。
どちらもボタンですが、**タイプ**が異なります。

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
ご覧の通り、**outline** キーワードを追加することで、ボタンは
**solid** タイプから **outline** タイプに変更されました。

![ボタンのスタイル](../assets/tutorial/solid-outline-button-styles.png)

### キーワードの使用方法

キーワードの使用に関する最後の注意点として… **bootstyle** パラメータは非常に柔軟です。
キーワードの表記形式は、実際にはあまり重要ではありません。
バックグラウンドでは正規表現（regex）が入力を解析し、適切な ttk スタイルに変換しています。
キーワードの _文字列_ を渡すことも、`list` や `tuple` などのキーワードの _反復可能オブジェクト_ を渡すことも可能です。
以下のすべてのバリエーションは有効であり、同じスタイルになります。

以下のすべてのバリエーションが有効であり、同じスタイルになります。

* `"info-outline"`
* `"infooutline"`
* `"info outline"`
* `"outline-info"`
* `("info", "outline")`
* `(INFO, OUTLINE)`

!!! 注：「推奨されるキーワードの区切り文字はダッシュです」
    キーワードに**文字列**を使用する場合、上記の_最初の_例のように、
    可能な限りダッシュでキーワードを区切ることを推奨します。 
    
    **定数**を使用し、かつ複数のキーワードを使用する場合は、
    上記の_最後の_例のように `list` または `tuple` を使用します。
