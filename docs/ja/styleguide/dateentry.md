# DateEntry

このウィジェットは、**Entry**ウィジェットと**Button**ウィジェットの2つのウィジェットで構成されています。
**Entry**コンポーネントは
[デフォルトの入力ウィジェット](entry.md)と全く同じ動作をし、カレンダーボタンは
[デフォルトのソリッドボタン](button.md)として動作します。

カレンダーボタンが押されると、[DatePickerPopup](datepickerpopup.md) が呼び出されます。
ポップアップに適用されるデフォルトの色は **primary** です。

このウィジェットは、[無効状態](#disabled-date-entry)、
[読み取り専用状態](#readonly-date-entry)、[無効状態](#invalid-date-entry) に対する特別なスタイルもサポートしています。

![date entries](../assets/widget-styles/date-entries.gif)

```python
# デフォルトの日付入力
DateEntry()

# 成功色の日付入力
DateEntry(bootstyle="success")
```

## その他日付入力スタイル

#### 無効な日付入力

このスタイルは_キーワード経由では適用できません_。ウィジェット設定を通じて構成します。

```python
# 無効状態で日付入力を作成
DateEntry(state="disabled")

# 作成後に日付入力フィールドを無効化
d = DateEntry()
d.configure(state="disabled")
```

#### 読み取り専用日付入力

このスタイルは_キーワード経由では適用できません_。ウィジェット設定を通じて構成します。

```python
# 読み取り専用状態で日付入力を作成
DateEntry(state="readonly")

# 作成後に読み取り専用状態を設定
d = DateEntry()
d.configure(state="readonly")
```

#### 無効な日付入力

このスタイルは_キーワード経由では適用できません_。
代わりに、ウィジェットに実装された検証プロセスの結果として生成されます。
**Cookbook**では、`Entry`ベースのウィジェットに[検証を適用する方法](../cookbook/validate-user-input.md)の例を確認できます。
