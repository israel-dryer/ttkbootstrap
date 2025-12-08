# チェックボタン

このウィジェットは、デフォルトで**プライマリ**カラーまたは[選択色](index.md#colors)で表示される様々なチェックボタンスタイルを備えています。

このウィジェットは、
[無効状態](#other-checkbutton-styles)用の特殊スタイルをサポートしています。

## チェックボタン（デフォルト）

デフォルトスタイルは正方形のチェックボックスとラベルで構成されます。
チェックボックスは未選択時に淡色枠線、選択時に塗りつぶされたチェックマーク付き正方形を表示します。

![checkbutton](../assets/widget-styles/checkbuttons.png)

```python
# デフォルトのチェックボタンスタイル
Checkbutton()

# 成功状態用チェックボタンスタイル
Checkbutton(bootstyle="success")
```

## ツールボタン

このスタイルは、_オフ_と_オン_の色を切り替えるソリッドな長方形ボタンを特徴とします。
背景は_オフ_時は淡いグレー、_オン_または_アクティブ_時はデフォルト色または[選択色](index.md#colors)になります。

![solid toolbuttons](../assets/widget-styles/solid-toolbuttons.gif)

```python
# デフォルトツールボタンスタイル
Checkbutton(bootstyle="toolbutton")

# 成功ツールボタンスタイル
Checkbutton(bootstyle="success-toolbutton")
```

## アウトラインツールボタン

このスタイルは長方形のボタンで、_off_時はスタイリングされた
**アウトライン**、_on_または_active_時は**ソリッド**背景に切り替わります。

![アウトラインツールボタン](../assets/widget-styles/outline-toolbuttons.gif)

```python
# デフォルトのアウトラインツールボタンスタイル
Checkbutton(bootstyle="outline-toolbutton")

# 成功時のアウトラインツールボタンスタイル
Checkbutton(bootstyle="success-outline-toolbutton")
```

## 丸形トグルボタン

このスタイルは丸みを帯びたボタンと、トグルの_オフ_時と_オン_時に色と位置が変化する**丸型**インジケーターが特徴です。
_オフ_時は淡いアウトラインのボタンに淡い色のインジケーターが表示されます。
_オン_時はデフォルト色または[選択色](index.md#colors)で塗りつぶされ、強調されたインジケーターが表示されます。

![round toggles](../assets/widget-styles/round-toggles.gif)

```python
# デフォルトの丸型トグルスタイル
Checkbutton(bootstyle="round-toggle")

# 成功状態用丸形トグルスタイル
Checkbutton(bootstyle="success-round-toggle")
```

## スクエアトグルボタン

このスタイルは四角いボタンと**四角**のインジケーターを備え、
トグルが_オフ_と_オン_で色と位置が変化します。_オフ_時は
淡いアウトラインに淡い色のインジケーターです。_オン_時は
デフォルト色または[選択色](index.md#colors)で塗りつぶされ、
強調されたインジケーターが表示されます。

![square toggles](../assets/widget-styles/square-toggles.gif)

```python
# デフォルトのスクエア・トグルスタイル
Checkbutton(bootstyle="square-toggle")

# 成功状態のスクエアトグルスタイル
Checkbutton(bootstyle="success-square-toggle")
```

## その他のチェックボタンスタイル

#### 無効化チェックボタン
このスタイルは_キーワード経由では適用不可_です。ウィジェット設定で構成します。

```python
# 無効状態でチェックボタンを作成
Checkbutton(state="disabled")

# 作成後に無効化する
cb = Checkbutton()
cb.configure(state="disabled")
```
