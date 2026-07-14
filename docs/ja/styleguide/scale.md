# スケール

このウィジェットスタイルは、細い灰色の溝と丸いスライダーハンドルが特徴で、
スライダーハンドルはデフォルトで**プライマリ**カラー、または[選択した色](index.md#colors)になります。
スライダーハンドルは_ホバー_時に明るくなり、_押下_時に暗くなります。 

このウィジェットは、
[無効状態](#other-scale-styles)用の特別なスタイルをサポートしています。

![scale](../assets/widget-styles/scale.gif)

```python
# デフォルトのスケールスタイル
Scale()

# 情報色のラベルスタイル
Scale(bootstyle="info")
```

## その他のスケールスタイル

#### 無効状態のスケール
このスタイルは _キーワードでは適用できません_。ウィジェットの
設定を通じて設定します。

```python
# 無効な状態でスケールを作成する
Scale(state="disabled")

# 作成後にスケールを無効にする
scale = Scale()
scale.configure(state="disabled")
```
