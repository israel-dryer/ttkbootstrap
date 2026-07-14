# エントリ

このウィジェットスタイルは、装飾された境界線を持つ入力ボックスが特徴です。境界線の色は
デフォルトでは控えめな色ですが、_hover_時に**primary**または
[選択された色](index.md#colors)に変わります。境界線の太さは
_focus_時に増します。 

また、このウィジェットは[無効状態](#disabled-entry)、
[読み取り専用状態](#readonly-entry)、および[無効な状態](#invalid-entry)に対する特別なスタイルもサポートしています。

![entry](../assets/widget-styles/entries.gif)

```python
# デフォルトのエントリスタイル
Entry()

# 危険色（danger）のエントリスタイル
Entry(bootstyle="danger")
```

## その他のエントリスタイル

#### 無効なエントリ

このスタイルは_キーワードでは適用できません_。ウィジェットの
設定を通じて設定します。

```python
# 無効な状態でウィジェットを作成する
Entry(state="disabled")

# 作成後にウィジェットを無効化
e = Entry()
e.configure(state="disabled")
```

#### 読み取り専用エントリー

このスタイルは_キーワードでは適用できません_。ウィジェットの
設定を通じて設定します。

```python
# ウィジェットを読み取り専用状態で作成
Entry(state="readonly")

# 作成後にウィジェットを読み取り専用に設定
e = Entry()
e.configure(state="readonly")
```

#### 無効な入力

このスタイルは_キーワードでは適用できません_。これは、ウィジェットに実装された
検証プロセスの結果として適用されます。**Cookbook**には、
`Entry`ベースのウィジェットに[検証を適用する方法](../cookbook/validate-user-input.md)の
例が掲載されています。
