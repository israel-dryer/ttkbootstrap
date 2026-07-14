# スピンボックス

このウィジェットスタイルは、装飾された枠線と矢印を備えた入力ボックスが特徴です。 境界線の色はデフォルトでは控えめな色ですが、_hover_時に**プライマリ**または
[選択した色](index.md#colors)に変わります。_focus_時には境界線の太さが増します。
矢印の色は、_hover_時または_focus_時にデフォルト色または[選択した色](index.md#colors)に
変わります。

また、このウィジェットは [無効状態](#disabled-spinbox)、
[読み取り専用状態](#readonly-spinbox)、および [無効な状態](#invalid-spinbox) に対する特別なスタイルもサポートしています。

![spinbox](../assets/widget-styles/spinbox.gif)

```python
# デフォルトのスピンボックススタイル
Spinbox()

# 危険色を使用したスピンボックスのスタイル
Spinbox(bootstyle="danger")
```

## その他のスタイル

#### 無効状態のスピンボックス

このウィジェットは、**無効**状態専用のスタイルをサポートしており、
上の図で確認できます。このスタイルは_キーワードでは適用できません_。
無効スタイルを適用するには：

```python
# 無効状態のウィジェットを作成する
Spinbox(state="disabled")

# 作成後にウィジェットを無効化する
e = Spinbox()
e.configure(state="disabled")
```

#### 読み取り専用スピンボックス

このウィジェットは、**readonly** 状態専用のスタイルをサポートしており、
上の図で確認できます。このスタイルは _キーワードでは適用できません_。
readonly スタイルを適用するには：

```python
# ウィジェットを読み取り専用状態で作成する
Spinbox(state="readonly")

# 作成後にウィジェットを読み取り専用状態に設定
e = Spinbox()
e.configure(state="readonly")
```

#### 無効なスピンボックス

このスタイルは_キーワードでは適用できません_。これは、
ウィジェットに実装された検証プロセスの結果として適用されるものです。**Cookbook**には、
`Entry`ベースのウィジェットに[検証を適用する方法](../cookbook/validate-user-input.md)の
例が掲載されています。
