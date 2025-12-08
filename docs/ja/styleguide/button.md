# ボタン

このウィジェットは、デフォルトで**プライマリ**カラー、
または[選択したカラー](index.md#colors)を持つ様々なボタンスタイルタイプを備えています。

このウィジェットは、[無効状態](#other-button-styles) 用の特別なスタイルをサポートしています。

## ソリッドボタン（デフォルト）

デフォルトスタイルは、_ホバー_時に明るくなり、_押下_時に暗くなるソリッド背景が特徴です。
ウィジェットがフォーカスを持つと、ボタン内部に破線のリングが表示されます。

![solid button](../assets/widget-styles/solid-buttons.gif)

```python
# デフォルトスタイル
Button()

# 成功スタイル
Button(bootstyle="success")
```

## アウトラインボタン

このスタイルは細いアウトラインが特徴です。
押下時またはホバー時には、デフォルトボタンと同様の単色に変化します。
ウィジェットがフォーカスを得ると、ボタン内部に破線のリングが表示されます。

![アウトラインボタン](../assets/widget-styles/outline-buttons.gif)

```python
# デフォルトのアウトラインスタイル
Button(bootstyle="outline")

# 成功アウトラインスタイル
Button(bootstyle="success-outline")
```

## リンクボタン

このスタイルはラベルのような外観のボタンを特徴とします。テキストカラーは
_ホバー_時または_押下_時に**info**色に変化し、HTMLハイパーリンクで期待される効果を
再現します。ボタン押下時にはわずかな浮き上がりが生じ、動きのある外観を演出します。
ウィジェットがフォーカスを取得すると、ボタン内部に破線のリングが表示されます。

![リンクボタン](../assets/widget-styles/link-buttons.gif)

```python
# デフォルトリンクスタイル
Button(bootstyle="link")

# 成功リンクスタイル
Button(bootstyle="success-link")
```

## その他のボタンスタイル

#### 無効化ボタン
このスタイルは_キーワード経由では適用不可_です。ウィジェット設定で構成します。

```python
# 無効状態でボタンを作成
Button(state="disabled")

# 作成後にボタンを無効化
b = Button()
b.configure(state="disabled")
```
