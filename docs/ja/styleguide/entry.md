# エントリー

このウィジェットスタイルは、装飾された境界線を持つ入力ボックスを特徴とします。
境界線の色はデフォルトで控えめな色合いで、ホバー時に**プライマリ**色または[選択色](index.md#colors)に変化します。
フォーカス時には境界線の太さが増します。 

このウィジェットは[無効状態](#disabled-entry)、
[読み取り専用状態](#readonly-entry)、[無効状態](#invalid-entry)の特殊スタイルもサポートします。

![entry](../assets/widget-styles/entries.gif)

```python
# デフォルトのエントリスタイル
Entry()

# 危険色エントリースタイル
Entry(bootstyle="danger")
```

## その他のエントリスタイル

#### 無効化エントリー

このスタイルは_キーワード経由では適用できません_。ウィジェット設定を通じて構成します。

```python
# 無効状態でウィジェットを作成
Entry(state="disabled")

# 作成後にウィジェットを無効化
e = Entry()
e.configure(state="disabled")
```

#### 読み取り専用エントリー

このスタイルは_キーワード経由では適用できません_。ウィジェットの設定を通じて構成します。

```python
# ウィジェットを読み取り専用状態で作成
Entry(state="readonly")

# 作成後にウィジェットを読み取り専用状態に設定
e = Entry()
e.configure(state="readonly")
```

#### 無効な入力

このスタイルは_キーワード経由では適用できません_。
代わりに、ウィジェットに実装された検証プロセスの結果として生成されます。
**Cookbook**では、`Entry`ベースのウィジェットに[検証を適用する方法](../cookbook/validate-user-input.md)の例を確認できます。
