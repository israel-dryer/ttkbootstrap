# メニューボタン

このウィジェットは、矢印付きのスタイリングされたボタンを備えており、
[利用可能な色](index.md#colors)のいずれかを使用してスタイルを設定できます。 

このウィジェットは、[無効状態](#disabled-menubutton) 用の特別なスタイルをサポートしています。

## ソリッド（デフォルト）

このスタイルは、_ホバー_時に明るくなり、_押下_時に暗くなる単色背景を採用しています。 

![solid menubutton](../assets/widget-styles/menubutton.gif)

```python
# デフォルトのソリッドメニューボタンスタイル
Menubutton()

# 成功色ソリッドメニューボタンスタイル
Menubutton(bootstyle="success")
```

## アウトライン

このスタイルは細いアウトラインが特徴です。押下時またはホバー時には、
デフォルトのメニューボタンスタイルと同様の単色に変化します。 

![outline menubutton](../assets/widget-styles/outline-menubutton.gif)

```python
# デフォルトのアウトラインメニューボタンスタイル
Menubutton(bootstyle="outline")

# 情報色のアウトラインメニューボタンスタイル
Menubutton(bootstyle="info-outline")
```

## その他のメニューボタンスタイル

#### 無効化メニューボタン
このスタイルは_キーワード経由では適用不可_です。ウィジェット設定で構成します。

```python
# 無効状態でメニューボタンを作成
Menubutton(state="disabled")

# 作成後にメニューボタンを無効化
b = Menubutton()
b.configure(state="disabled")
```
