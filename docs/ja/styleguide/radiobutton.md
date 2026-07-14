# ラジオボタン

このウィジェットには、デフォルトで**プライマリ**
カラー、または[選択した色](index.md#colors)が適用された、さまざまなスタイルのラジオボタンが用意されています。

このウィジェットは、
[無効状態](#other-radiobutton-styles)用の特別なスタイルをサポートしています。

## ラジオボタン（デフォルト）

デフォルトのウィジェットスタイルは、
丸いインジケーターを持つ従来の**ラジオボタン**を採用しています。インジケーターは、_選択状態_のときに
デフォルト色または選択された色で塗りつぶされます。

![radiobutton](../assets/widget-styles/radiobuttons.png)

```python
# デフォルトのラジオボタンスタイル
Radiobutton()

# セカンダリカラーのラジオボタンスタイル
Radiobutton(bootstyle="secondary")
```

## ソリッド・ツールボタン

このスタイルは、_選択されていない_ときは落ち着いたグレーの背景を持ち、
_選択されている_または_アクティブ_なときはデフォルト色または[選択色](index.md#colors)で塗りつぶされる、
実線の長方形のボタンが特徴です。

![toolbutton](../assets/widget-styles/radio-toolbutton.gif)

```python
# デフォルトのツールボタンスタイル
Radiobutton(bootstyle="toolbutton")

# 警告色のラジオツールボタンスタイル
Radiobutton(bootstyle="danger-toolbutton")
```

## アウトライン・ツールボタン

このスタイルは、_選択されていない_ときは**アウトライン**があり、
_選択されている_または
_アクティブ_のときは**塗りつぶし**の背景を持つ長方形のボタンが特徴です。

![アウトライン・ツールボタン](../assets/widget-styles/outline-radio-toolbutton.gif)

```python
# デフォルトのアウトライン・ラジオツールボタンスタイル
Radiobutton(bootstyle="outline-toolbutton")

# 情報色のアウトライン付きラジオツールボタンスタイル
Radiobutton(bootstyle="info-outline-toolbutton")
```

## その他のラジオボタンのスタイル

#### 無効状態のラジオボタン
このスタイルは_キーワードでは適用できません_。ウィジェットの
設定を通じて構成されます。

```python
# 無効状態のラジオボタンを作成する
Radiobutton(state="disabled")

# 作成後にラジオボタンを無効にする
rb = Radiobutton()
rb.configure(state="disabled")
```
