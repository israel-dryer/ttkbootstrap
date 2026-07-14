# コンボボックス

このウィジェットスタイルは、装飾された境界線と矢印が付いた入力ボックスが特徴です。 境界線の色はデフォルトでは控えめな色ですが、_hover_時に**primary**または
[選択した色](index.md#colors)に変わります。_focus_時には境界線の太さが増します。
矢印の色は、_hover_時または_focus_時にデフォルト色または[選択した色](index.md#colors)に変わります。

また、このウィジェットは[無効状態](#disabled-combobox)、
[読み取り専用状態](#readonly-combobox)、および[無効な状態](#invalid-combobox)に対する特別なスタイルもサポートしています。

![combobox](../assets/widget-styles/combos.gif)

```python
# デフォルトのコンボボックススタイル
Combobox()

# 危険色を使用したコンボボックススタイル
Combobox(bootstyle="danger")
```

## その他のコンボボックススタイル

#### 無効化されたコンボボックス

このスタイルは_キーワードでは適用できません_。ウィジェットの
設定を通じて設定します。

```python
# 無効な状態でコンボボックスを作成
Combobox(state="disabled")

# 作成後にコンボボックスを無効化
cb = Combobox()
cb.configure(state="disabled")
```

#### 読み取り専用コンボボックス

このスタイルは_キーワードでは適用できません_。ウィジェットの
設定を通じて設定します。


```python
# 読み取り専用状態でコンボボックスを作成する
Combobox(state="readonly")

# 作成後にコンボボックスを読み取り専用状態に設定
cb = Combobox()
cb.configure(state="readonly")
```

#### 無効なコンボボックス

このスタイルは_キーワードでは適用できません_。これは、ウィジェットに実装された
検証プロセスの結果として適用されるものです。**Cookbook**には、
`Entry`ベースのウィジェットに[検証を適用する方法](../cookbook/validate-user-input.md)の
例が掲載されています。
