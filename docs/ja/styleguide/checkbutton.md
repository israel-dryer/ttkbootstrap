# チェックボタン

このウィジェットには、デフォルトで**プライマリ**
カラー、または[選択した色](index.md#colors)が適用された、さまざまなスタイルのチェックボタンが用意されています。

このウィジェットは、
[無効状態](#other-checkbutton-styles)用の特別なスタイルをサポートしています。

## チェックボタン（デフォルト）

デフォルトのスタイルは、正方形のチェックボックスとラベルで構成されています。チェックボックスは、
選択されていないときは淡い色のアウトラインが表示され、選択されると
チェックマーク付きの塗りつぶされた正方形になります。

![checkbutton](../assets/widget-styles/checkbuttons.png)

```python
# デフォルトのチェックボタンスタイル
Checkbutton()

# 成功時のチェックボタンスタイル
Checkbutton(bootstyle="success")
```

## ツールボタン

このスタイルは、_off_と_on_の色を切り替える、塗りつぶされた長方形のボタンが特徴です。
背景色は、_off_のときは淡いグレーで、_on_または_active_のときはデフォルト色
または[選択色](index.md#colors)になります。

![solid toolbuttons](../assets/widget-styles/solid-toolbuttons.gif)

```python
# デフォルトのツールボタンスタイル
Checkbutton(bootstyle="toolbutton")

# 成功時のツールボタンスタイル
Checkbutton(bootstyle="success-toolbutton")
```

## アウトライン・ツールボタン

このスタイルは、_off_のときはスタイル化された
**アウトライン**、_on_または
_active_のときは**ソリッド**な背景に切り替わる長方形のボタンが特徴です。

![アウトライン・ツールボタン](../assets/widget-styles/outline-toolbuttons.gif)

```python
# デフォルトのアウトライン・ツールボタン・スタイル
Checkbutton(bootstyle="outline-toolbutton")

# 成功時のアウトライン・ツールボタン・スタイル
Checkbutton(bootstyle="success-outline-toolbutton")
```

## 丸型トグルボタン

このスタイルは、丸みを帯びたボタンと、トグルが_off_および_on_の状態で
色と位置が変わる**丸い**インジケーターが特徴です。_off_の状態では、ボタンは淡い色のアウトラインで、
インジケーターも淡い色になります。_on_の状態では、ボタンはデフォルト色または[選択された色](index.md#colors)で塗りつぶされ、
インジケーターにはアクセントカラーが適用されます。

![round toggles](../assets/widget-styles/round-toggles.gif)

```python
# デフォルトの丸型トグルスタイル
Checkbutton(bootstyle="round-toggle")

# 成功時のラウンドトグルスタイル
Checkbutton(bootstyle="success-round-toggle")
```

## スクエア・トグルボタン

このスタイルは、**四角形**のインジケーターを備えた四角いボタンが特徴で、
トグルが_オフ_または_オン_になると色と位置が変化します。_オフ_のときは、ボタンは淡い輪郭線
で、インジケーターも淡い色になります。_オン_のときは、ボタンはデフォルト
または [選択した色](index.md#colors)で塗りつぶされ、インジケーターにはアクセントが付きます。

![square toggles](../assets/widget-styles/square-toggles.gif)

```python
# デフォルトのスクエア・トグルスタイル
Checkbutton(bootstyle="square-toggle")

# 成功時のスクエアトグルスタイル
Checkbutton(bootstyle="success-square-toggle")
```

## その他のチェックボタンスタイル

#### 無効状態のチェックボタン
このスタイルは_キーワードでは適用できません_。ウィジェットの
設定を通じて構成します。

```python
# 無効な状態でチェックボタンを作成
Checkbutton(state="disabled")

# 作成後にチェックボタンを無効にする
cb = Checkbutton()
cb.configure(state="disabled")
```
