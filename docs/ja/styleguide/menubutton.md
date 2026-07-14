# メニューボタン

このウィジェットは、[利用可能な色](index.md#colors)のいずれかを使用してスタイルを設定できる、矢印付きのスタイリッシュなボタンが特徴です。 

このウィジェットは、[無効状態](#disabled-menubutton)用の特別なスタイルに対応しています。

## ソリッド（デフォルト）

このウィジェットスタイルは、_hover_時に明るくなり、_pressed_時に暗くなる
単色の背景色が特徴です。 

![ソリッド・メニューボタン](../assets/widget-styles/menubutton.gif)

```python
# デフォルトのソリッド・メニューボタンスタイル
Menubutton()

# 成功時の色付きソリッドメニューボタンスタイル
Menubutton(bootstyle="success")
```

## アウトライン

このスタイルは、細い装飾のアウトラインが特徴です。_押下_時または_ホバー_時に、
ボタンはデフォルトのメニューボタンスタイルと同様に単色に変わります。 

![アウトライン・メニューボタン](../assets/widget-styles/outline-menubutton.gif)

```python
# デフォルトのアウトライン・メニューボタンスタイル
Menubutton(bootstyle="outline")

# info色のアウトラインメニューボタンスタイル
Menubutton(bootstyle="info-outline")
```

## その他のメニューボタンのスタイル

#### 無効状態のメニューボタン
このスタイルは_キーワードでは適用できません_。ウィジェットの
設定を通じて構成します。

```python
# 無効状態のメニューボタンを作成
Menubutton(state="disabled")

# 作成後にメニューボタンを無効にする
b = Menubutton()
b.configure(state="disabled")
```
