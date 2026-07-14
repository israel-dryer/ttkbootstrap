# ボタン

このウィジェットには、デフォルトで**プライマリ**
カラー、または[選択したカラー](index.md#colors)が設定された、さまざまなスタイルのボタンが用意されています。

このウィジェットは、[無効状態](#other-button-styles)用の特別なスタイルをサポートしています。

## ソリッドボタン（デフォルト）

デフォルトのスタイルでは、背景が単色で、_ホバー_時に明るくなり、
_押下_時に暗くなります。ウィジェットにフォーカスが当たると、
ボタンの内部に点線のリングが表示されます。

![ソリッドボタン](../assets/widget-styles/solid-buttons.gif)

```python
# デフォルトのスタイル
Button()

# 成功スタイル
Button(bootstyle="success")
```

## アウトラインボタン

このスタイルは、細い装飾線（アウトライン）が特徴です。_押下_時または_ホバー_時に、
ボタンはデフォルトのボタンスタイルと同様に単色に変わります。ウィジェットにフォーカスが当たると、
ボタンの内部に点線のリングが表示されます。

![アウトラインボタン](../assets/widget-styles/outline-buttons.gif)

```python
# デフォルトのアウトラインスタイル
Button(bootstyle="outline")

# 成功時のアウトラインスタイル
Button(bootstyle="success-outline")
```

## リンクボタン

このスタイルは、ラベルのような外観を持つボタンが特徴です。_hover_ または _pressed_ 時にテキストの色が
**info** に変更され、HTML のハイパーリンクで期待されるような効果を再現します。ボタンが押された際にはわずかな浮き上がりがあり、
動きのある外観を与えます。ウィジェットにフォーカスが当たると、
ボタンの内部に点線のリングが表示されます。

![link buttons](../assets/widget-styles/link-buttons.gif)

```python
# デフォルトのリンクスタイル
Button(bootstyle="link")

# 成功時のリンクスタイル
Button(bootstyle="success-link")
```

## その他のボタンスタイル

#### 無効なボタン
このスタイルは_キーワードでは適用できません_。ウィジェットの
設定を通じて構成します。

```python
# 無効な状態でボタンを作成
Button(state="disabled")

# 作成後にボタンを無効にする
b = Button()
b.configure(state="disabled")
```
