# ラベル

このウィジェットには2種類のスタイルタイプがあり、いずれも
[利用可能な色](index.md#colors)でカスタマイズできます。

## デフォルトラベル

デフォルトスタイルでは、デフォルトテーマで定義された前景色と背景色が使用されます。
前景色は[選択した色](index.md#colors)で変更可能です。

![通常ラベル](../assets/widget-styles/label.png)

```python
# デフォルトラベルスタイル
Label()

# 危険色ラベルスタイル
Label(bootstyle="danger")
```

## 反転ラベル

このスタイルは、デフォルト色の反転版を用いたラベルを特徴とします。
[選択色](index.md#colors)は前景色ではなく背景色を変更します。 

これは、スタイル付き`Frame`にラベルを追加する場合や、
デフォルトの背景色を持たない[ラベル見出し](../gallery/mediaplayer.md)を追加したい場合に特に有用です。

![inverse label](../assets/widget-styles/inverse-label.png)

```python
# デフォルトの反転ラベルスタイル
Label(bootstyle="inverse")

# 危険色逆ラベルスタイル
Label(bootstyle="inverse-danger")
```
