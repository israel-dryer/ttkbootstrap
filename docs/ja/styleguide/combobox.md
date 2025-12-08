# コンボボックス

このウィジェットスタイルは、装飾された境界線と矢印を備えた入力ボックスを特徴とします。
境界線の色はデフォルトで控えめであり、ホバー時に**プライマリ**色または[選択色](index.md#colors)に変化します。
フォーカス時には境界線の太さが増します。
矢印の色はホバー時またはフォーカス時にデフォルト色または[選択色](index.md#colors)に変化します。

このウィジェットは、[無効状態](#disabled-combobox)、
[読み取り専用状態](#readonly-combobox)、[無効状態](#invalid-combobox) 向けの特殊スタイルもサポートしています。

![combobox](../assets/widget-styles/combos.gif)

```python
# デフォルトのコンボボックススタイル
Combobox()

# 危険色コンボボックススタイル
Combobox(bootstyle="danger")
```

## その他のコンボボックススタイル

#### 無効化コンボボックス

このスタイルは_キーワード経由では適用できません_。ウィジェット設定を通じて構成します。

```python
# 無効状態でコンボボックスを作成
Combobox(state="disabled")

# 作成後にコンボボックスを無効化
cb = Combobox()
cb.configure(state="disabled")
```

#### 読み取り専用コンボボックス

このスタイルは_キーワード経由では適用できません_。ウィジェット設定を通じて構成します。


```python
# 読み取り専用状態でコンボボックスを作成
Combobox(state="readonly")

# 作成後に読み取り専用状態を設定
cb = Combobox()
cb.configure(state="readonly")
```

#### 無効なコンボボックス

このスタイルは_キーワード経由では適用できません_。
代わりに、ウィジェットに実装された検証プロセスの結果として生成されます。
**Cookbook**では、`Entry`ベースのウィジェットに[検証を適用する方法](../cookbook/validate-user-input.md)の例を確認できます。
