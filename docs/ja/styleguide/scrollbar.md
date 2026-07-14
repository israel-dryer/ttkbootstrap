# スクロールバー

このウィジェットスタイルは、薄い灰色の溝と、デザインが施されたサムおよび矢印
ボタンが特徴です。サムと矢印は、_hover_時に色が薄くなり、_press_時に色が濃くなります。
サムと矢印は、[利用可能な色](index.md#colors)のいずれかでスタイルを設定できます。 

## 正方形（デフォルト）

デフォルトのスタイルでは、角が四角いスライダーが採用されています。

![scrollbar](../assets/widget-styles/square-scrollbars.png)

```python
# デフォルトのスクロールバースタイル
Scrollbar()

# 成功色を使用したデフォルトのスクロールバースタイル
Scrollbar(bootstyle="success")
```

## 丸型

**丸型**スタイルは、角が丸いスクロールバーを特徴としています。

![丸型スクロールバー](../assets/widget-styles/round-scrollbars.png)

```python
# デフォルトのラウンドスクロールバースタイル
Scrollbar(bootstyle="round")

# 危険色（danger）のラウンドスクロールバースタイル
Scrollbar(bootstyle="danger-round")
```
