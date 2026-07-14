# プログレスバー

このウィジェットには、デフォルトで**プライマリ**カラーのインジケーター
バーを持つスタイルタイプがいくつか用意されていますが、
[利用可能な色](index.md#colors)のいずれかを使用してスタイルを変更することも可能です。

## 単色（デフォルト）

デフォルトのウィジェットスタイルでは、単色のインジケーターバーが表示されます。

![ソリッドプログレスバー](../assets/widget-styles/solid-progressbar.gif)

```python
# デフォルトのソリッド・プログレスバー・スタイル
Progressbar()

# 成功色の一色塗りプログレスバースタイル
Progressbar(bootstyle="success")
```


## ストライプ

このウィジェットスタイルは、メインカラーにデフォルト色または 
[選択した色](index.md#colors) を使用し、交互のストライプには 
その色の彩度を下げたバージョンを使用したストライプ状のインジケーターバーが特徴です。

![ストライプ型プログレスバー](../assets/widget-styles/striped-progressbar.gif)

```python
# デフォルトのストライプ型プログレスバースタイル
Progressbar(bootstyle="striped")

# 警告色のストライプ型プログレスバースタイル
Progressbar(bootstyle="danger-striped")
```
