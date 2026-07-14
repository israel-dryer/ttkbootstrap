# DateEntry

このウィジェットは、**Entry** ウィジェットと **Button**
ウィジェットの 2 つのウィジェットで構成されています。**Entry** コンポーネントの動作は 
[デフォルトの入力ウィジェット](entry.md) と同様であり、カレンダーボタンの動作は 
[デフォルトのソリッドボタン](button.md) と同じです。

カレンダー
ボタンが押されると、[DatePickerPopup](datepickerpopup.md)が呼び出されます。ポップアップに適用されるデフォルトの色は**primary**です。

また、このウィジェットは、[無効状態](#disabled-date-entry)、
[読み取り専用状態](#readonly-date-entry)、および[無効な状態](#invalid-date-entry)に対する特別なスタイルもサポートしています。

![日付入力](../assets/widget-styles/date-entries.gif)

```python
# デフォルトの日付入力
DateEntry()

# 成功時のカラー日付入力
DateEntry(bootstyle="success")
```

## その他の日付入力スタイル

#### 無効な日付入力

このスタイルは_キーワードでは適用できません_。ウィジェットの
設定を通じて設定します。

```python
# 無効な状態で日付入力フィールドを作成
DateEntry(state="disabled")

# 作成後に日付入力フィールドを無効化する
d = DateEntry()
d.configure(state="disabled")
```

#### 読み取り専用日付入力

このスタイルは_キーワードでは適用できません_。ウィジェットの
設定を通じて設定します。

```python
# 読み取り専用状態で日付入力フィールドを作成する
DateEntry(state="readonly")

# 作成後に日付入力フィールドを読み取り専用に設定
d = DateEntry()
d.configure(state="readonly")
```

#### 無効な日付入力

このスタイルは_キーワードでは適用できません_。これは、ウィジェットに実装された
検証プロセスの結果として適用されます。**Cookbook**には、
`Entry`ベースのウィジェットに[検証を適用する方法](../cookbook/validate-user-input.md)の
例が掲載されています。
