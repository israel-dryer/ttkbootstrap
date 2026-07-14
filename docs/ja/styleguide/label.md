# ラベル

このウィジェットには2種類のスタイルがあり、どちらも
[利用可能な色](index.md#colors)のいずれかを使用してカスタマイズできます。

## デフォルトのラベル

デフォルトのスタイルでは、テーマで定義されたデフォルトの
前景色と背景色が使用されます。前景色は[選択した色](index.md#colors)を使用して変更できます。

![通常のラベル](../assets/widget-styles/label.png)

```python
# デフォルトのラベルスタイル
Label()

# 危険色ラベルスタイル
Label(bootstyle="danger")
```

## 反転ラベル

このスタイルでは、デフォルトの色の反転版がラベルに使用されます。
[選択した色](index.md#colors)は、前景色ではなく背景色を変更します。 

これは、スタイルが適用された `Frame` にラベルを追加する場合や、
デフォルトの背景色を持たない [ラベル見出し](../gallery/mediaplayer.md) を追加したい場合に
特に便利です。

![逆色ラベル](../assets/widget-styles/inverse-label.png)

```python
# デフォルトの反転ラベルスタイル
Label(bootstyle="inverse")

# 危険色を使用した反転ラベルスタイル
Label(bootstyle="inverse-danger")
```
